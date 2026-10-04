---
name: analyze_od_flow
description: Use this skill when the user asks for OD flow analysis, origin-destination matrices, commute corridors, migration routes, or region-to-region movement aggregation from staypoints.
metadata:
  short-description: Build OD matrix and rank movement corridors.
---

# analyze_od_flow

Use this Skill after `$extract_stay_points`. Preferred input is `staypoints.jsonl`.

## Command

```bash
cd /mnt/skills/custom/analyze_od_flow
python3 scripts/analyze_od_flow.py --input /path/to/staypoints.jsonl --output-dir /path/to/output --geohash-precision 5 --top-k 20
```

## Outputs

- `od_matrix.jsonl`
- `top_corridors.jsonl`
- `summary.json`
- `viz_input.jsonl`

## Algorithm

- Consecutive staypoint OD construction
- Geohash aggregation
- Unique-user counting
- Average travel-duration statistics
- Corridor ranking with business landmark enrichment

## Next Skills

Use `od_matrix.jsonl` with `$analyze_spatiotemporal_accessibility` and `$measure_spatiotemporal_entropy`.
