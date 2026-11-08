---
name: reel-render
description: Render a deterministic vertical video (Instagram Reel / YouTube Short / any mp4) from code on this Mac — "render a video", "make an mp4", "turn this animation into a video", "export frames", "the video renderer". Canvas render(t) → puppeteer frames → ffmpeg h264. No After Effects, no cloud, fully reproducible. Also the QA method (read frames back) and the player-cache trap.
---

# reel-render — deterministic video from a canvas function

The whole pipeline is three artifacts:

1. **`reel.html`** — a single `<canvas>` plus a pure `window.render(t)` that
   draws the complete frame for time `t` (seconds). Pure means: no
   `requestAnimationFrame`, no `Date.now()`, no randomness — `render(3.5)`
   yields the identical frame forever. Data is injected by string-replacing a
   `__PLACEHOLDER__` token with JSON at build time, so the html stays inspectable
   in a browser during development.
2. **`render.js`** — puppeteer: viewport = canvas size (1080×1920 for vertical),
   loop `i/FPS` over `N = FPS × DUR` frames (30 × 8.0 = 240), screenshot the
   canvas element per frame into `frames/f%04d.png`. Install with
   `npm init -y && npm install puppeteer` in the working dir. Register
   `page.on('pageerror', …)` and exit non-zero — otherwise a JS syntax error
   renders 240 identical blank frames and you learn it from the video.
3. **ffmpeg** (brew): 
   `ffmpeg -y -framerate 30 -i frames/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart out.mp4`
   `yuv420p` is required — without it iOS/Instagram silently reject the file.

Animation vocabulary that made 8 seconds feel authored, all pure functions of t:
window `w(t,start,end)→0..1`, `easeOut` cubed, typed-text via
`cmd.slice(0, floor((t-start)*cps))`, caret blink `floor(t/0.55)%2` (steps(1)),
count-up numbers `value*easeOut(w(...))`, staggered reveals by index/distance.

## The traps (each cost real time on the first run)

- **`node render.js | tail -1` lies.** The pipe's exit code is `tail`'s, so
  `&&` chains continue after node fails. Symptom: ffmpeg errors about missing
  frames while the real error scrolled away. Run node un-piped, or rely on the
  pageerror hook's hard exit.
- **cwd drift breaks the chain silently.** The render chain assumes the reel's
  dir; an earlier `cd` elsewhere in the session leaves `frames/` unfound. `cd`
  into the reel dir in the same compound command.
- **QA by reading frames, not by trusting the code.** Downscale key frames
  (`sips -Z 500 frames/f0130.png --out qa.png`) and *look* at them at each
  story beat. Every real defect found this way was a layout collision between
  phases — text stacking instead of replacing — plus right-edge overflow.
  Check width before shipping copy: `measureText` vs `W - margin`.
- **An overwritten mp4 shows its OLD cut in an already-open player.**
  QuickTime caches by filename; a stale version showed up twice after in-place
  re-renders and a correct file got debugged. Verify from the artifact itself —
  `ffmpeg -y -ss 7.8 -i out.mp4 -frames:v 1 check.png` plus `md5` against the
  render output — then rename (`_FINAL`, `_v2`) to cache-bust before handing it
  over. Never burn time on the player's word alone.
- **Real geometry beats decoration.** The strongest visuals were actual
  centerlines / lot polygons / boundary files drawn as glowing vectors
  (`shadowBlur` on strokes). An isometric world from flat polygons is just
  rotate θ, squash y (~0.52), extrude z, painter-sort by pre-extrusion screen
  y — no three.js needed. Draw order for assembles: sort by a real axis
  (north→south, along-street), never dict order — random flicker reads as a bug.

## Delivery

Encode → copy into a folder the user can find (a project folder, not loose
files) → `open` it. 8s @ 1080×1920 crf18
lands ~0.4–2 MB.

Content rules (story grammar, sourcing, honesty) belong in a separate task skill;
this skill only owns the rendering.
