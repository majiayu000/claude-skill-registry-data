---
name: analyze_region_heat
description: Use this skill when the user wants to compute regional activity heat, check-in volume, point density, unique users, or Top-K active geohash regions from trajectory records.
metadata:
  short-description: Aggregate trajectory activity by region and time bucket.
---

# analyze_region_heat

Use this Skill to aggregate point-level or evidence-level trajectory records into regional heat indicators.

## Command

```bash
cd /mnt/skills/custom/analyze_region_heat
python3 scripts/analyze_region_heat.py \
  --input /path/to/cleaned_points.jsonl \
  --output-dir /path/to/output \
  --geohash-precision 6 \
  --time-bucket hour
```

Useful filters:

```bash
--time-start 2012-06-01T00:00:00 --time-end 2012-06-30T23:59:59
--hour-start 7 --hour-end 9 --geohash wx4
```

## Outputs

- `region_heat.jsonl`
- `summary.json`

## Algorithm

- Optional time/space filtering
- Geohash region aggregation
- Activity count
- Unique user count
- Optional category Top-N statistics

## Next Skills

Use `region_heat.jsonl` with `$detect_flow_anomaly` for regional flow anomaly detection.
