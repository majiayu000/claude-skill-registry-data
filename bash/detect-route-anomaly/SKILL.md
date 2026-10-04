---
name: detect_route_anomaly
description: Use this skill when the user wants to detect individual trip or route anomalies, such as unusually long distance, unusually long/short duration, abnormal average speed, detours, or trips that deviate from a user's usual behavior.
metadata:
  short-description: Detect route-level trip anomalies.
---

# detect_route_anomaly

Use this Skill for micro-level trajectory anomaly detection over trip records.

## Command

```bash
cd /mnt/skills/custom/detect_route_anomaly
python3 scripts/detect_route_anomaly.py \
  --input /path/to/trips.jsonl \
  --output-dir /path/to/output \
  --group-col user_id \
  --threshold 3.5
```

## Outputs

- `route_anomalies.jsonl`
- `summary.json`

## Algorithm

- Per-user or global grouping
- Distance anomaly detection
- Duration anomaly detection
- Average-speed anomaly detection
- Robust MAD/z-score fallback scoring

## Next Skills

Combine with `$search_similar_trajectory` to explain whether an anomalous trip has comparable historical trips.
