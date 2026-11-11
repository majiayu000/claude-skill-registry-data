---
name: flicker-probe
description: "Use when a picture style, a layer or a shader term flickers, shimmers or crawls — in a still view or in motion — to find where it does and to prove a fix: renders consecutive frames on a held, fixed-step loop and diffs them."
---

# Finding flicker by diffing frames

Flicker is a pixel that changes when nothing should change it, or that
changes by more than the motion explains. Judged by eye it is easy to
miss and impossible to compare before and after; diffed, it is a number
and a red map.

## The hooks

`window.__poc` (a build with `NEXT_PUBLIC_POC_DEBUG=1`, `poc-debug.ts`):

- `hold = true` stops the loop; `step = n` lets it draw exactly `n` more
  frames (counted down by the frames drawn, `tickPocFrame`).
- `frameMs = 1000 / 60` puts the scene clock on a fixed step per drawn
  frame (`pocFrameTime`), so the wind, the water and the rain advance the
  same between any two frames however slow the renderer is.
- `window.__poc` is replaced on every patch: read it fresh, never keep it.

What still moves on a held clock, legitimately: the clouds (`SkyMesh`
runs on the renderer's real time), Sin City's rain, the near crowns' sway
in the styles that keep it. Mask or name them, never "fix" them.

## The procedure

1. `NEXT_PUBLIC_POC_DEBUG=1 bunx next build && bunx next start -p 3000`
   (after `bun run build`'s data preparation; headless SwiftShader is
   enough — this measures change, not light).
2. Render, per style, a still pair and three moved frames:

   ```bash
   node .claude/skills/flicker-probe/probe.mjs out/p1 pastel,comic,line
   POSE='{"mode":"walk","pos":{"x":-944.2,"y":116,"z":-549.5},"headingDeg":205,"pitchDeg":0,"fov":55}' \
     STEP_M=0.001 node .claude/skills/flicker-probe/probe.mjs out/p2 comic
   ```

   `POSE` is a camera state (`getCameraState()`); without it the site's
   initial view. In walk mode the eye sinks onto the ground for a while
   after a teleport: the probe steps until the camera holds still before
   it takes the still pair, or every "still" diff is motion.
3. Diff:
   - `python3 .claude/skills/flicker-probe/diff.py out/p1 comic` — the
     still pair (`a:b`): anything over 24 that is not on the list above
     is flicker. `b:m1` with `STEP_M=0.001` is the **sub-pixel test**: a
     millimetre moves the far city by a hundredth of a pixel and the near
     ground by a fraction, so an antialiased picture barely changes and
     every binary decision that flips (a stipple cell, a depth-stencil
     line, a dot under-sampled across a grazing plane) shows in red.
   - `python3 .claude/skills/flicker-probe/flicker.py out/p1 comic` — at
     walking pace (2.5 cm a frame), pixels whose change flips sign from
     one frame to the next. Near the camera a fine line moving a pixel a
     frame toggles too: read it far off, or use the sub-pixel test.
4. Read the red maps (`*.diff.png`, `*.flicker.png`) beside the frame,
   name the feature, fix it, and render the same pose again. Each run of
   five styles takes ~15 min in the container (boot ~8 min).

## What it found (2026-10)

- A sway or a stipple below a pixel shimmers: fade the sway with distance,
  draw a crown whole once its stipple cells are smaller than a pixel.
- A world-anchored screen on a swaying surface slides: print the surface
  flat (Comic's crowns) or hold it still (Strich's crowns, `sway`).
- A screen across a grazing plane: give it its mean tone once the
  pixel's long axis spans half a cell, and antialias over the footprint
  across the edge (`fwidth` of the distance), not the mean pixel.
