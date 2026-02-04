---
name: mc-local-grid-visualize
type: python
description: "Generates interactive 3D HTML visualization of the session-local occupancy grid. Opens in browser."
---

# Minecraft Local Grid Visualization Tool

Generates an interactive 3D HTML visualization of the session-local rolling occupancy grid using Three.js. Displays voxels as colored cubes with rotation, zoom, and pan controls.

## Purpose

Visualize the transient 3D occupancy grid for debugging navigation, collision recovery, and planning decisions. Shows what the agent "knows" about nearby blocks.

## Input

- `output_file`: Optional output file path (default: `/tmp/local_grid_viz.html`)

## Output

Returns uniform_return format with:
- `value`: Summary text with file path and voxel count
- `data`: `{success, file_path, cell_count, center, radius}`

Also opens generated HTML file in default browser.

## Visualization Features

Interactive 3D viewer:
- **Rotate**: Left-click and drag
- **Pan**: Right-click and drag  
- **Zoom**: Mouse wheel
- **Hover**: Shows block name and position

Visual elements:
- **Voxels**: Colored cubes (block-name → color mapping)
- **Agent center**: Red sphere marker
- **Radius boundary**: Green wireframe cube (radius 10)
- **Grid helper**: Reference grid at agent Y-level

## Behavior & Performance

- Reads grid directly from `executor.get_world_state("local_grid")`
- Generates self-contained HTML file (Three.js via CDN)
- Auto-opens in default browser
- Static snapshot (refresh browser and re-run tool for updates)

## Guidelines

- Use after `mc-observe` / `mc-dig` / `mc-place` to see updated grid state
- Keep browser open and refresh page after re-running tool for latest snapshot
- Hover over voxels to see block names and coordinates
- Use zoom to inspect specific regions

## Usage Examples

Visualize current grid state:
```json
{"type":"mc-local-grid-visualize","out":"$viz"}
```

Specify output file:
```json
{"type":"mc-local-grid-visualize","output_file":"/tmp/my_grid.html","out":"$viz"}
```
