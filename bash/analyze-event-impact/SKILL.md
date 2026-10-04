---
name: analyze_event_impact
description: Use this skill when the user wants to evaluate the impact of an external event such as rainstorm, sports event, traffic control, holiday, emergency, or policy intervention on regional trajectory volume.
metadata:
  short-description: Compare before/during/after regional activity around an event.
---

# analyze_event_impact

Use this Skill on spatiotemporal trajectory evidence or regional activity evidence. It compares treatment and control regions around an event window with a simplified DID-style calculation.

## Command

```bash
cd /mnt/skills/custom/analyze_event_impact
python3 scripts/analyze_event_impact.py \
  --input /path/to/evidence.jsonl \
  --output-dir /path/to/output \
  --event-start 2012-06-09T00:00:00 \
  --event-end 2012-06-10T00:00:00 \
  --treatment-geohash wtw1z,wtw3s \
  --event-name "大型活动影响"
```

## Outputs

- `region_impacts.jsonl`
- `summary.json`
- `viz_input.jsonl`

## Algorithm

- Treatment/control split
- Event-window comparison
- Welch-style t statistic
- DID estimate where controls are available
- Landmark-enriched impact evidence

## Next Skills

Use event-impact outputs with `$fuse_spatial_evidence`, or pair them with hotspot/anomaly results for causal interpretation.
