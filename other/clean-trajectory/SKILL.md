---
name: clean_trajectory
description: Use this skill when the user wants to clean raw GPS, check-in, signaling, taxi, or user mobility trajectory files by validating coordinates and timestamps, removing duplicates, filtering abnormal speed jumps, and exporting standardized cleaned trajectory points.
metadata:
  short-description: Clean raw trajectory data into standardized points.
---

# clean_trajectory

Use this Skill for the first step of the trajectory pipeline: raw trajectory points -> cleaned trajectory points.

## Command

```bash
cd /mnt/skills/custom/clean_trajectory
python3 scripts/clean_trajectory.py --input /path/to/raw.csv --output-dir /path/to/output
```

Optional flags:

```bash
--user-col user_id --trajectory-col trajectory_id --time-col timestamp --lat-col lat --lon-col lon
--max-speed-kmh 200 --geohash-precision 6
```

## Outputs

- `cleaned_points.jsonl`
- `summary.json`

## Algorithm

- Coordinate validation
- Timestamp normalization
- Duplicate removal
- Haversine distance
- Speed-threshold filtering
- Geohash encoding

## Next Skills

Use `cleaned_points.jsonl` with:

- `$map_spatial_grid`
- `$search_spatiotemporal`
- `$analyze_region_heat`
- `$mine_trajectory_patterns`
