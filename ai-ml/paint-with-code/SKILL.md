---
name: paint-with-code
description: "Repaint a picture, photo or render in watercolour with paintkit code brushes, where every pixel is a simulated stroke on simulated paper, and film it being painted stroke by stroke. Use for watercolour versions of artworks or photos, painterly stills, seamless carousel strips, 'process' proof videos ('repaint in watercolour', 'watercolour from code', 'painting process video', 'paintkit')."
license: MIT
---

# Paint With Code

paintkit (`github.com/codepawl/paintkit`) paints with simulated washes on cold-press paper: wet bleeds, dark dried
edges, back-runs, granulation, bare paper for the lights. The source picture only guides where strokes go and what
colour they carry. No image model, filter or style transfer touches the output.

## Install

```bash
uv tool install git+https://github.com/codepawl/paintkit   # or: pip install git+https://github.com/codepawl/paintkit
```

`film` needs ffmpeg on the PATH.

## Commands

```bash
paintkit paint picture.jpg -o painting.png --size 2048          # long side in px
paintkit film picture.jpg -o painting.mp4 --size 1024 --still painting.png
paintkit paint picture.jpg -o painting.png --size 2048 --painter glazing   # closer to the picture, deeper darks
```

`--painter glazing` (paintkit 0.2.0) glazes until the paper matches the picture: 40 washes, reserved lights, darker
darks. It is slower than the default `classic` painter: about 5 minutes for a 2048 px picture on one core.

Time on one CPU core: 1400 px about 30 s, 4096 px 8 to 12 min. Run several pictures as parallel processes at low
priority, not one big job.

## Rules

1. Use public-domain or owned references. For a famous artwork, the artist must be dead more than 100 years, and the
   photo must be a faithful copy of a 2D work. Keep a sources table with each page link and licence.
2. Never paste, filter or blend reference pixels into the output. The brushes lay every pixel, and that is the claim
   a post or reply can make.
3. Preview first: paint every frame at `--size 1024` or less, look at all of them, then paint full size.
4. Crop for the subject before painting. A small subject in a big frame turns to mud: a ship on a sunset sky, a
   figure on drapery of the same colour. Zoom in until the subject fills a third of the frame, or swap the picture.
5. High contrast and clear shapes paint best: woodblock prints, Van Gogh, bold portraits. Low-contrast hazy pictures
   (pastels, Turner sunsets) lose their subject at carousel size.
6. Check each frame against its reference at the size people will see it. Ask "do you know which painting this is?"
   for every frame, and name the frames where the answer is no.

## Carousels and strips

- X shows a multi-image carousel whole only from 3:4 to 4:3; anything taller is cropped top and bottom. Paint 3:4
  frames (3072 x 4096 for 4K) for an X carousel.
- For a seamless strip, paint each frame in a window that runs past both edges into its neighbours, then join
  neighbours along the least-difference path through the overlap and cut at exact frame boundaries. See
  `references/seamless-strip.md`.
- Order frames by their measured hue for a colour journey, and lean neutrals toward a hue that moves linearly
  across the strip. Measure. Hue by eye misjudges warm paintings with blue accents.

## Process video as proof

`paintkit film` records the pencil sketch, every wash drawn as growing strokes (wet paint a little darker), and each
wash drying. Post it as a reply under the finished piece. It answers "is this AI generated?" without words.

## Python

`paintkit.painterly.paint(target, scale, fallback_angle, fallback_weight, seam_zone, seed, recorder=...)` is the
painter. `scale` is the picture height over 4096. `paintkit.watercolour` is the paper and wash engine for hand-built
strokes (`Paper`, `new_wash`, `deposit`, `paint_stroke`, `dry`). Read the repo README for the full API.

## Checks

- Every frame is recognisable at phone size. Name the weak ones honestly.
- Full-size frames rejoin into the strip pixel for pixel, and the colour step across each cut is no bigger than an
  ordinary column step inside a frame.
- Exported JPEGs stay under the platform limit (X: 5 MB per image).
