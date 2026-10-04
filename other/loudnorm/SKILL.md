---
name: loudnorm
description: Normalize audio loudness to broadcast levels using ffmpeg's two-pass loudnorm filter. Measures the input, then applies normalization with the measured parameters. Use as a final-stage audio leveling step.
---

# loudnorm

ffmpeg two-pass loudnorm. Outputs broadcast-safe audio (default targets: I=-14 LUFS, TP=-1.5 dBTP, LRA=11).

## Inputs
- `input`: video or audio path
- `out`: output path
- `I` (optional): integrated loudness target, default `-14`
- `TP` (optional): true peak target, default `-1.5`
- `LRA` (optional): loudness range, default `11`

## Output
Media file with normalized audio. Video stream copied (no re-encode).

## How
1. **Measure pass**: `ffmpeg -i <in> -af loudnorm=I=<I>:TP=<TP>:LRA=<LRA>:print_format=json -f null -` → parse the JSON block from stderr.
2. **Apply pass**: `ffmpeg -i <in> -af loudnorm=I=<I>:TP=<TP>:LRA=<LRA>:measured_I=<>:measured_TP=<>:measured_LRA=<>:measured_thresh=<>:offset=<>:linear=true:print_format=summary -c:v copy <out>`.

## Status
Stub. Salvageable command construction in `archive/pre-pivot:pipeline_v2.py:672-778`.
