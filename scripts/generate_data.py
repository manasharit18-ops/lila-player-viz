"""
Parse LILA BLACK parquet telemetry into static JSON files for the visualizer.

Requires: duckdb (and numpy dependency).
"""

import json
import os
from datetime import datetime
import duckdb

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_ROOT = os.path.join(ROOT, "player_data", "player_data")
PUBLIC = os.path.join(ROOT, "public")
DATA_DIR = os.path.join(PUBLIC, "data")
MATCH_DIR = os.path.join(DATA_DIR, "matches")

MAP_CONFIGS = {
    "AmbroseValley": {
        "id": "AmbroseValley",
        "name": "Ambrose Valley",
        "minimap": "minimaps/AmbroseValley_Minimap.png",
        "scale": 900,
        "origin_x": -370,
        "origin_z": -473,
        "size": 1024,
    },
    "GrandRift": {
        "id": "GrandRift",
        "name": "Grand Rift",
        "minimap": "minimaps/GrandRift_Minimap.png",
        "scale": 581,
        "origin_x": -290,
        "origin_z": -290,
        "size": 1024,
    },
    "Lockdown": {
        "id": "Lockdown",
        "name": "Lockdown",
        "minimap": "minimaps/Lockdown_Minimap.jpg",
        "scale": 1000,
        "origin_x": -500,
        "origin_z": -500,
        "size": 1024,
    },
}

DATE_MAP = {
    "February_10": "2026-02-10",
    "February_11": "2026-02-11",
    "February_12": "2026-02-12",
    "February_13": "2026-02-13",
    "February_14": "2026-02-14",
}

POSITION_EVENTS = {"Position", "BotPosition"}
EVENT_MAP = {
    "Kill": "kill",
    "BotKill": "kill",
    "Killed": "death",
    "BotKilled": "death",
    "KilledByStorm": "storm_death",
    "Loot": "loot",
}


def is_bot(user_id: str) -> bool:
    return str(user_id).isdigit()


def date_from_filename(filename: str) -> str:
    for key, value in DATE_MAP.items():
        if key in filename:
            return value
    return "unknown"


def write_json(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def parse_parquet() -> None:
    if not os.path.isdir(DATA_ROOT):
        raise SystemExit("player_data folder not found. Unzip player_data.zip into lila-player-viz/player_data/")

    os.makedirs(MATCH_DIR, exist_ok=True)

    glob_path = os.path.join(DATA_ROOT, "February_*", "*").replace("\\", "/")

    con = duckdb.connect()
    query = f"""
        SELECT
            user_id,
            match_id,
            map_id,
            x,
            z,
            epoch_ms(ts) AS ts_ms,
            CAST(event AS VARCHAR) AS event,
            filename
        FROM read_parquet('{glob_path}', filename=true)
        ORDER BY match_id, ts_ms
    """

    cursor = con.execute(query)

    matches_index = []
    dates_set = set()

    current_match_id = None
    match_payload = None

    def finalize_match(payload):
        if not payload:
            return
        payload["duration"] = int((payload["end_ts"] - payload["start_ts"]) / 1000)
        players = list(payload["players"].values())
        players.sort(key=lambda p: (p["is_bot"], p["id"]))
        payload["players"] = players
        del payload["start_ts"]
        del payload["end_ts"]

        match_id = payload["id"]
        write_json(os.path.join(MATCH_DIR, f"{match_id}.json"), payload)

        matches_index.append(
            {
                "id": match_id,
                "map": payload["map"],
                "date": payload["date"],
                "duration": payload["duration"],
                "players": len(players),
            }
        )

    for row in cursor.fetchall():
        user_id, match_id, map_id, x, z, ts_ms, event, filename = row
        match_id = str(match_id)
        map_id = str(map_id)

        if current_match_id != match_id:
            finalize_match(match_payload)
            current_match_id = match_id
            match_payload = {
                "id": match_id,
                "map": map_id,
                "date": date_from_filename(str(filename)),
                "duration": 0,
                "players": {},
                "positions": [],
                "events": [],
                "start_ts": ts_ms,
                "end_ts": ts_ms,
            }
            dates_set.add(match_payload["date"])

        match_payload["end_ts"] = ts_ms

        player_id = str(user_id)
        if player_id not in match_payload["players"]:
            match_payload["players"][player_id] = {
                "id": player_id,
                "is_bot": is_bot(player_id),
                "name": player_id,
            }

        t = (ts_ms - match_payload["start_ts"]) / 1000.0
        if event in POSITION_EVENTS:
            match_payload["positions"].append(
                {"t": round(t, 3), "player_id": player_id, "x": float(x), "y": float(z)}
            )
        elif event in EVENT_MAP:
            match_payload["events"].append(
                {"t": round(t, 3), "type": EVENT_MAP[event], "x": float(x), "y": float(z), "player_id": player_id}
            )

    finalize_match(match_payload)

    maps_list = [MAP_CONFIGS[key] for key in MAP_CONFIGS]
    index_payload = {
        "maps": maps_list,
        "dates": sorted(dates_set),
        "matches": matches_index,
    }
    write_json(os.path.join(DATA_DIR, "index.json"), index_payload)

    print(f"Wrote {len(matches_index)} matches to public/data/")


if __name__ == "__main__":
    parse_parquet()
