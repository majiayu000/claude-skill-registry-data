---
name: profile_urban_region
description: Use this skill when the user wants to identify urban functional regions such as residential, commercial, transit, leisure, or mixed-use areas by combining trajectory activity and POI evidence.
metadata:
  short-description: Identify urban functional attributes by region.
---

# profile_urban_region

Use this Skill to classify region functions from activity time signatures and optional POI category distributions.

## Command

```bash
cd /mnt/skills/custom/profile_urban_region
python3 scripts/profile_urban_region.py \
  --input /path/to/cleaned_points.jsonl \
  --output-dir /path/to/output \
  --time-col utc \
  --lat-col Latitude \
  --lon-col Longitude \
  --user-col user_id \
  --poi-input /path/to/pois.csv \
  --poi-category-col "Venue Category Name"
```

## Outputs

- `region_profiles.jsonl`
- `summary.json`

## Algorithm

- Geohash region aggregation
- Morning/workday/evening/night activity signature
- POI category keyword scoring
- Functional label ranking with mixed-use fallback

## Next Skills

Use profile outputs with `$fuse_spatial_evidence`, or combine with hotspots and anomaly outputs for region portraits.
