---
name: cut-clip
description: Trim a video to a [t0, t1] time range using ffmpeg. Stream-copies where possible to avoid re-encoding. Use as the cheap building block for cutting source video into per-short slices.
---

# cut-clip

Thin ffmpeg trim wrapper.

## Inputs
- `input`: video path
- `t0`: start seconds (float)
- `t1`: end seconds (float)
- `out`: output path
- `reencode` (optional): bool, default `false`. Set true if cut must be frame-accurate at a non-keyframe.

## Output
mp4 cut to the requested range.

## How
- Default (stream copy, fast, ±1 keyframe accuracy):
  `ffmpeg -ss <t0> -to <t1> -i <in> -c copy -avoid_negative_ts make_zero <out>`
- Re-encode (frame-accurate):
  `ffmpeg -i <in> -ss <t0> -to <t1> -c:v libx264 -preset veryfast -crf 18 -c:a aac <out>`

## Invoke
`.claude/skills/cut-clip/cut-clip.sh <input> <t0> <t1> <out> [reencode]`

Idempotent via mtime check (skips when out is newer than input).
