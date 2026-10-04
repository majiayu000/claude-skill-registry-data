---
name: predict_next_location
description: Use this skill when the user asks to predict next location, next stop, future geohash, likely destination, destination inference, or Markov-chain mobility prediction from historical trajectories.
metadata:
  short-description: 基于历史驻留序列训练马尔可夫链，预测下一位置或目的地。
---

# predict_next_location

Use this Skill on staypoint history to train a first-order transition model and optionally predict from a current geohash.

## Command

```bash
cd /mnt/skills/custom/predict_next_location
python3 scripts/predict_next_location.py --input /path/to/staypoints.jsonl --output-dir /path/to/output --current-geohash wtw3s --top-k 5
```

Useful flags:

```bash
--current-time 2012-06-09T08:00:00 --geohash-precision 5 --train-only
```

## Outputs

- `transition_matrix.jsonl`
- `predictions.jsonl`
- `summary.json`

## Next Skills

Use predictions with `$analyze_spatiotemporal_accessibility` or `$fuse_spatial_evidence`.
