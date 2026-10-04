---
name: extract_stay_points
description: Use this skill when the user wants to extract stay points, dwell events, OD endpoints, or meaningful stops from GPS, check-in, signaling, taxi, or cleaned trajectory data.
metadata:
  short-description: Extract stay points from trajectory records.
---

# extract_stay_points

Use this Skill to detect places where a user stayed within a spatial radius for a minimum dwell time.

## Command

```bash
cd /mnt/skills/custom/extract_stay_points
python3 scripts/extract_stay_points.py --input /path/to/raw_or_cleaned.csv --output-dir /path/to/output
```

Useful flags:

```bash
--stay-radius-m 200 --stay-min-minutes 20 --max-speed-kmh 200 --geohash-precision 6
```

## Outputs

- `staypoints.jsonl`
- `summary.json`

## Algorithm

- Reuses trajectory cleaning
- Sliding distance-radius stay detection
- Dwell-time threshold filtering
- Stay centroid calculation
- Geohash encoding

## Next Skills

Use `staypoints.jsonl` for OD endpoint reasoning, stay-duration anomaly checks, or urban region profiling.
