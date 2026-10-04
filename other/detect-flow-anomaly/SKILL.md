---
name: detect_flow_anomaly
description: Use this skill when the user wants to detect macro-level mobility flow anomalies, including abnormal region heat, check-in spikes, OD flow spikes, sudden decreases, or unusual time-window activity.
metadata:
  short-description: Detect regional or OD flow anomalies.
---

# detect_flow_anomaly

Use this Skill after `$analyze_region_heat` or `$analyze_od_flow`.

## Command

```bash
cd /mnt/skills/custom/detect_flow_anomaly
python3 scripts/detect_flow_anomaly.py \
  --input /path/to/region_heat.jsonl \
  --output-dir /path/to/output \
  --group-col geohash \
  --metric-col activity_count
```

For OD flow anomalies:

```bash
python3 scripts/detect_flow_anomaly.py --input /path/to/od_matrix.jsonl --output-dir /path/to/output --group-col od_pair --metric-col flow_count
```

## Outputs

- `flow_anomalies.jsonl`
- `summary.json`

## Algorithm

- Region or OD grouping
- Activity/flow metric scoring
- Robust MAD/z-score fallback scoring
- High/low anomaly ranking

## Next Skills

Use anomaly outputs as evidence for final trajectory reports or event-impact analysis.
