---
name: speed-up
description: Globally retime a finished short by SPEED (default 1.25x) — the LAST step of the per-span edit chain. Video setpts + pitch-corrected audio atempo, so every relative beat (captions, zoom punches, b-roll windows, CTA, end-card) compresses uniformly and stays in sync. Deterministic, non-fatal. SPEED=1 or SPEED_UP=0 passes through.
---

# speed-up

Final retime of a finished short. Runs AFTER `end-card` and BEFORE `qc-clip` so
the QC gate and `visual-cadence` measure (and `save-local` saves) the actual
delivered, sped-up clip.

```bash
speed-up.sh <in.mp4> <out.mp4> [speed=1.25]
```

- `speed` — playback multiplier; `1.25` ships ~20% faster. Read from arg 3 or
  the `SPEED` env (default `1.25`).
- Video is retimed with `setpts=PTS/SPEED`; audio with `atempo` (chained into
  0.5–2.0 stages for out-of-range speeds) so pitch is preserved.
- Because it is a single uniform retime applied last, ALL upstream relative
  timing is preserved — nothing else in the pipeline needs to know about it.
  Note the cold-open title hold (`TITLE_SWAP`) is set pre-speed, so its
  on-screen time is `TITLE_SWAP / SPEED`.
- Deterministic (no Claude), idempotent (`.spmeta` mtime+param signature),
  non-fatal (probe/ffmpeg failure → passthrough copy).
- `SPEED=1` or `SPEED_UP=0` → passthrough.
