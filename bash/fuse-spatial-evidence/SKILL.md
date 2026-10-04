---
name: fuse_spatial_evidence
description: Use this skill when the user wants to combine hotspot, anomaly, profile, forecast, and event-impact outputs into a unified ranked regional evidence view.
metadata:
  short-description: Fuse multi-source spatial evidence into one ranked view.
---

# fuse_spatial_evidence

Use this Skill after any combination of `$analyze_region_heat`, `$detect_flow_anomaly`, `$forecast_region_flow`, `$profile_urban_region`, and `$analyze_event_impact`.

## Command

```bash
cd /mnt/skills/custom/fuse_spatial_evidence
python3 scripts/fuse_spatial_evidence.py \
  --input /path/to/flow_anomalies.jsonl \
  --input /path/to/region_profiles.jsonl \
  --input /path/to/event_impacts.jsonl \
  --output-dir /path/to/output
```

## Outputs

- `fused_evidence.jsonl`
- `evidence_details.jsonl`
- `summary.json`

## Algorithm

- Evidence standardization
- Region/time alignment
- Cross-source score accumulation
- Dominant signal summarization

## Next Skills

Use fused evidence as the final evidence layer for reports, briefings, or LLM-grounded answer generation.
