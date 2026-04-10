# LILA BLACK - Player Journey Visualization Tool
LIVE URL : [https://lila-player-viz.vercel.app/]

A browser-based tool for Level Designers to explore player behavior across LILA BLACK's three extraction shooter maps.

## Live Demo
Deploy the `public/` folder to Netlify via drag-and-drop. The tool works immediately with no build step.

## What It Does

- Player paths: Visualizes every player's movement trail on the correct minimap. Humans = bright colored solid lines; Bots = dashed gray lines.
- Heatmaps: Three overlay modes - Kill zones (red), Death zones (orange), Traffic density (purple).
- Timeline playback: Scrub or play through the match at 0.5x/1x/2x/4x speed.
- Event markers: Kill, Death, Loot, Storm death rendered as distinct markers with tooltips.
- Filters: Map, date, match, and player type toggles.
- Stats panel: Match summary, top killers, and a live event feed tied to the timeline.

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Vanilla JS + HTML | Zero-config Netlify deploy; no build step |
| Map Rendering | Leaflet.js CRS.Simple | Built for custom image overlays |
| Paths + Events | HTML5 Canvas | Smooth redraw of thousands of points |
| Heatmaps | Canvas radial gradients | GPU-friendly and portable |
| Data | Static JSON files | Served as static assets; no backend |
| Data Pipeline | Python + DuckDB | Reads parquet directly and fast |

## Project Structure

```
public/                      <- Netlify deploy this folder
  index.html                 <- Entire app (single file, CDN deps)
  minimaps/
    AmbroseValley_Minimap.png
    GrandRift_Minimap.png
    Lockdown_Minimap.jpg
  data/
    index.json               <- Match manifest (maps, dates, match list)
    matches/
      <match_id>.json        <- Per-match data (positions + events)

scripts/
  generate_data.py           <- Parquet -> JSON pipeline
  generate_minimaps.py       <- (optional) synthetic SVG minimaps

ARCHITECTURE.md
INSIGHTS.md
README.md
```

## Setup (Local)

```bash
# 1. Generate data
cd lila-player-viz
python scripts/generate_data.py

# 2. Serve locally (any static server)
cd public
python -m http.server 8080
# Open: http://localhost:8080
```

## Deploy to Netlify (Drag-and-Drop)

1. Run the Python script above to generate all data files
2. Go to https://app.netlify.com/drop
3. Drag the entire `public/` folder onto the drop zone
4. Done - you will get a live URL instantly

## Data Notes

- Parquet files are stored without a `.parquet` extension.
- `event` is stored as bytes; the pipeline decodes to strings.
- Use `x` and `z` for 2D plotting. `y` is elevation.
- Map configs are in `ARCHITECTURE.md`.

## Walkthrough

1. Open the deployed URL. The tool loads the match manifest automatically.
2. Use the Map, Date, and Match selectors to load a specific match.
3. Use the Heatmap selector to toggle kill zones, death zones, or traffic density.
4. Use the Event Types toggles to show or hide kill, death, loot, and storm markers.
5. Use the Play button and timeline slider to scrub through the match.
6. Use Human/Bot toggles to compare player behavior.

## Coordinate System

See `ARCHITECTURE.md` for the detailed coordinate mapping and Y-axis flip.

## Environment Variables

None required. This is a pure static site.

## Browser Support

Chrome 90+, Firefox 88+, Safari 14+, Edge 90+.
