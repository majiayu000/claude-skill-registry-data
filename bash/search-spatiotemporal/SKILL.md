---
name: search_spatiotemporal
description: Use this skill when the user wants to search or recall trajectory records by time window, hour range, geohash prefix, bounding box, city, or semantic text condition.
metadata:
  short-description: Search trajectory records by temporal and spatial filters.
---

# search_spatiotemporal

Use this Skill for bottom-layer trajectory evidence recall.

## Command

```bash
cd /mnt/skills/custom/search_spatiotemporal
python3 scripts/search_spatiotemporal.py \
  --input /path/to/cleaned_points.jsonl \
  --output-dir /path/to/output \
  --time-start 2012-06-01T07:00:00 \
  --time-end 2012-06-30T09:00:00 \
  --geohash wx4 \
  --top-k 50
```

Useful filters:

```bash
--query "commute subway" --city Beijing --hour-start 7 --hour-end 9
--bbox min_lon,min_lat,max_lon,max_lat
```

## Outputs

- `matches.jsonl`
- `summary.json`

## Algorithm

- Time-window filtering
- Daily hour-window filtering
- Geohash prefix filtering
- BBox spatial filtering
- Lightweight text matching over record fields

## Next Skills

Feed `matches.jsonl` into `$analyze_region_heat`, `$mine_trajectory_patterns`, or anomaly Skills.
