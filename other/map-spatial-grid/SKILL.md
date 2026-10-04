---
name: map_spatial_grid
description: Use this skill when the user wants to map latitude/longitude trajectory records, staypoints, trips, or check-ins into spatial grids such as Geohash for aggregation and downstream spatial analysis.
metadata:
  short-description: Map trajectory coordinates to Geohash grids.
---

# map_spatial_grid

Use this Skill to normalize spatial positions into grid IDs before regional aggregation or retrieval.

## Command

```bash
cd /mnt/skills/custom/map_spatial_grid
python3 scripts/map_spatial_grid.py --input /path/to/cleaned_points.jsonl --output-dir /path/to/output --geohash-precision 6
```

Optional flags:

```bash
--lat-col lat --lon-col lon
```

## Outputs

- `grid_points.jsonl`
- `grid_summary.jsonl`
- `summary.json`

## Algorithm

- Latitude/longitude detection
- Pure-Python Geohash encoding
- Grid-level count aggregation

## Next Skills

Use `grid_points.jsonl` with `$search_spatiotemporal`, `$analyze_region_heat`, and `$mine_trajectory_patterns`.
