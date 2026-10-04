---
name: forecast_region_flow
description: Use this skill when the user wants to predict future people or vehicle flow for target regions, based on historical regional activity series or raw trajectory points.
metadata:
  short-description: Forecast future regional flow trends.
---

# forecast_region_flow

Use this Skill after `$analyze_region_heat`, or run it directly on cleaned trajectory/check-in points.

## Command

```bash
cd /mnt/skills/custom/forecast_region_flow
python3 scripts/forecast_region_flow.py \
  --input /path/to/region_heat.jsonl \
  --output-dir /path/to/output \
  --group-col geohash \
  --metric-col activity_count \
  --time-col time_bucket \
  --time-bucket day \
  --forecast-steps 3
```

For raw trajectory points:

```bash
python3 scripts/forecast_region_flow.py \
  --input /path/to/cleaned_points.jsonl \
  --output-dir /path/to/output \
  --time-col utc \
  --lat-col Latitude \
  --lon-col Longitude \
  --user-col user_id \
  --time-bucket day
```

## Outputs

- `region_forecasts.jsonl`
- `summary.json`

## Algorithm

- Region/time aggregation
- Rolling baseline estimation
- Trend extrapolation
- Volatility interval estimation

## Next Skills

Use forecast outputs with `$fuse_spatial_evidence` or combine with anomaly/event analysis for regional decision support.
