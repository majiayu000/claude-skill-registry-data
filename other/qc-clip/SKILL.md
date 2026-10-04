---
name: qc-clip
description: Sanity-check a rendered short with ffprobe. Verifies duration is in range and file size is non-trivial. Pass/fail boolean plus a short reason. Use as a final gate before saving a render.
---

# qc-clip

Lightweight sanity check. No quality metrics theatre.

## Inputs
- `input`: video path
- `min_duration` (optional): default `15`
- `max_duration` (optional): default `90`
- `min_size_kb` (optional): default `100`

## Output
```json
{
  "pass": true,
  "duration": 31.4,
  "size_kb": 4820,
  "reason": ""
}
```
On failure, `pass: false` and `reason` contains the first failing check (e.g. `"duration 9.2s below min 15s"`).

## How
1. `ffprobe -v error -show_entries format=duration,size -of json <in>`
2. Compare against thresholds.
3. Print/return verdict JSON.

## Status
Implemented — `qc-clip.sh`.
