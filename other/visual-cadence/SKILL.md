---
name: visual-cadence
description: Measure the longest stretch of a rendered clip with NO visual change (the union of jump-cut/zoom/b-roll cuts) via ffmpeg scene detection. Emits a JSON verdict + a non-fatal WARN when the max static gap exceeds MAX_STATIC_GAP. Diagnostic only — never alters or rejects the clip. VISUAL_CADENCE=0 skips.
---

# visual-cadence

Static-gap measurement. Runs in the finishing phase right AFTER `qc-clip`
passes, on the final clip. It is the union-of-all-visual-changes counterpart to
the per-skill cut planners — `jump-cut`, `zoom-punch`, and b-roll each place
cuts blind to one another, so only a post-render measure tells you what a viewer
actually sees. It is the keystone signal for the "12 seconds without a pattern
interrupt" retention leak diagnosed on the channel.

```
visual-cadence.sh <clip.mp4> [out.json=<clip>.cadence.json] [max_gap=5.0]
```

- **How.** `ffmpeg ... -vf select='gt(scene,VCAD_SCENE)',showinfo` flags frames
  whose scene-change score exceeds the threshold; the script parses their
  `pts_time`, treats `[0, ...cuts..., dur]` as boundaries, and reports the
  largest gap. Hard cuts (b-roll) and strong reframes (jump-cut) register;
  gradual zoom-punch pulses intentionally do not count as a "change."
- **Output.** `{pass, duration, threshold, scene, n_changes, max_gap,
  gap_window:[a,b], changes:[...]}`.
- **Diagnostic only.** Always exits 0 (usage/missing-input aside); it writes the
  verdict and logs a `WARN` when `max_gap > MAX_STATIC_GAP`, but never blocks the
  save. The real fix lives upstream in `jump-cut` coverage; this surfaces
  regressions.
- **Idempotent** via `.vcadmeta`. `VISUAL_CADENCE=0` disables.

Knobs: `VISUAL_CADENCE` (0 disables), `MAX_STATIC_GAP` (default 5.0s),
`VCAD_SCENE` (scene-detect threshold, default 0.3).
