# ARCHITECTURE.md - LILA BLACK Player Journey Visualizer

## What I Built

A single-page, zero-backend visualization tool. Level Designers open one URL, select a match, and immediately see player paths, heatmaps, and event markers on the correct minimap with timeline playback.

## Tech Stack and Reasoning

| Layer | Choice | Alternatives Considered | Decision |
|---|---|---|---|
| Frontend framework | Vanilla JS + HTML | React+Vite, Svelte | No build step so Netlify drag-and-drop works instantly |
| Map rendering | Leaflet.js CRS.Simple | deck.gl, Three.js, SVG | CRS.Simple is purpose-built for custom image overlays |
| Paths + Events | HTML5 Canvas | SVG, Leaflet Polylines | Canvas redraws 10,000+ points in under 16ms |
| Heatmaps | Canvas radial gradients | deck.gl HeatmapLayer, Leaflet.heat | No WebGL dependency, stable across browsers |
| Data format | Static JSON per match | Live API, SQLite WASM | Frontend fetches only the selected match |
| Data pipeline | Python + DuckDB | Pandas-only, Spark | DuckDB reads parquet directly and is fast to script |
| Hosting | Netlify drag-and-drop | Vercel, Railway | Instant deploy of the public folder |

## Data Flow

```
Parquet files (player_data.zip)
          |
          v
scripts/generate_data.py
  - Reads parquet with DuckDB
  - Decodes event bytes to strings
  - Maps events -> kill / death / loot / storm_death
  - Outputs: public/data/index.json
             public/data/matches/*.json
          |
          v
public/index.html (browser)
  - Fetches data/index.json on load
  - Populates map/date/match dropdowns
  - On match select -> fetches match_*.json
  - Renders to two canvas layers on top of Leaflet
```

## Coordinate Mapping (The Tricky Part)

### The Problem

The dataset stores world coordinates in `x` and `z`. The `y` column is **elevation** and should be ignored for the 2D minimap. Each map has a unique origin and scale that must be applied.

### Map Configuration (From README)

| Map | Scale | Origin X | Origin Z |
|---|---:|---:|---:|
| AmbroseValley | 900 | -370 | -473 |
| GrandRift | 581 | -290 | -290 |
| Lockdown | 1000 | -500 | -500 |

Minimap images are 1024x1024 pixels.

### The Formula

```javascript
// Step 1: world -> UV
u = (x - origin_x) / scale
v = (z - origin_z) / scale

// Step 2: UV -> pixel with Y-flip
pixel_x = u * 1024
pixel_y = (1 - v) * 1024

// Step 3: Leaflet CRS.Simple uses [lat, lng] = [pixel_y, pixel_x]
```

### Why This Works

- `v = 0` maps to the bottom edge of the image
- `v = 1` maps to the top edge of the image
- Y is flipped because image coordinates grow downward

### Validation Method

Drop a known event (or a dense cluster) and confirm it lands on the intended POI in the minimap. If mirrored vertically, the Y-flip is missing.

## Timestamp Handling

`ts` is stored as a timestamp (ms) representing time within the match. The pipeline converts it to milliseconds via `epoch_ms(ts)` and normalizes each match to start at `t=0`. The UI uses these relative times for timeline playback.

## Bot Detection

Bots are detected by `user_id` format:
- UUID -> human
- numeric string -> bot

In the UI:
- Humans: bright solid paths and filled markers
- Bots: dashed gray paths and hollow markers

## Canvas Architecture

Two stacked canvas elements sit above the Leaflet map:

```
z=400: path-canvas   - player paths and event markers
z=390: heat-canvas   - heatmap overlay
z=200: Leaflet panes - minimap image overlay
```

Heatmaps are expensive to recompute, while paths change every frame. Splitting the canvases avoids redundant work.

## Timeline / Playback

Playback uses requestAnimationFrame with wall-clock delta time:

```javascript
const dt = (timestamp - lastTimestamp) / 1000
currentTime += dt * speed
```

At each frame we filter positions and events where `t <= currentTime` and redraw the path canvas.

## Heatmap Rendering

Each event point draws a radial gradient with additive blending. Overlapping points increase intensity naturally. Modes:

- Kill zones: type === 'kill'
- Death zones: type === 'death' or 'storm_death'
- Traffic: sampled player positions

## Major Tradeoffs

| Decision | Tradeoff |
|---|---|
| No build step | Less component structure than React |
| Canvas over SVG | Great performance, harder hit-testing |
| Static JSON | No real-time data, acceptable for LD analysis |

## Assumptions

1. Event definitions match README (Kill/BotKill/Killed/BotKilled/KilledByStorm/Loot).
2. Minimap images are 1024x1024 and aligned to the provided origin/scale values.
