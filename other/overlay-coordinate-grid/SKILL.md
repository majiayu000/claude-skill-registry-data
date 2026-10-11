---
name: overlay-coordinate-grid
description: Place and verify every overlay by reading exact coordinates off a labelled coordinate grid instead of estimating positions. Grid the real footage frame when graphics must line up with something in shot, and grid the overlay's own renders to measure where things actually landed — text bounds, collisions, margins, centring. Use for every overlay composition, whether or not it's tied to footage.
metadata:
  tags: remotion, overlay, layout, measurement, compositing, verification
---

## When to use

**Every overlay.** Estimating positions is the most common way these compositions go
wrong, and a grid replaces the estimate with a measurement. That covers two
situations, which often come up in the same build:

1. **Graphics that must line up with something in the footage** — a hat on a head, a
   prop in a hand, an arrow at an object, a label on a product. Grid the footage frame.
2. **Any overlay at all, including ones with no footage** — grid your own renders to
   see where elements really are. Font metrics, `letterSpacing`, `textAnchor`, stroke
   widths and rotations all move things away from where the code suggests.

Real misses from this project that a grid catches immediately:
- `IdentityShell` — the word was assumed to start at x≈460. Gridded, `RUNNER` spans
  x 330–1597, so the crack origin and bounds were 125px short and the first letter
  never cracked.
- `UnattachedGate` — a gate swing arc drawn from assumed geometry ran straight through
  the `JOY` label.

Pair with `remotion-house-style` for brand, export settings, folders and naming, and
for its propose-first rule. This skill covers where things go and proving it.

## The rule

**Never estimate a position. Read it off a grid, then prove it on a grid.**
Images shown in chat are downscaled, and code-level geometry isn't where the pixels
end up, so "looks about right" is routinely 50–150px out. Don't report a layout or
placement you haven't seen on a gridded render.

Run everything from the Remotion project directory and keep review files in
`out/checks/<composition>/` (gitignored). Scripts need Python 3 with Pillow.

## 1. Get a reference image

- **Your own render** (always available): render in composition pixels —
  ```bash
  npx remotion still <CompositionId> out/checks/<name>/still-<frame>.png --frame=<frame> --scale=1
  ```
  `--scale=1` matters: the project renders at 2x by default, which would put every
  coordinate at double.
- **A pasted screenshot of footage.** The attachment note gives its original size
  (e.g. `original 2158x1208`); find the file by exact dimensions:
  ```bash
  mdfind "kMDItemPixelWidth == 2158 && kMDItemPixelHeight == 1208"
  ```
  macOS screenshots usually land on the Desktop.
- **A clip.** No system `ffmpeg` here, but Remotion bundles one:
  ```bash
  npx remotion ffmpeg -y -ss <seconds> -i <clip.mp4> -frames:v 1 out/checks/<name>/source.png
  ```
  It prints a version-mismatch banner first; that's noise, go by the exit code.
- **Footage needed but not available** — ask for it. Don't place off the chat image.

## 2. Grid it

```bash
# Whole frame, labelled every 100px:
python3 .claude/skills/overlay-coordinate-grid/scripts/grid.py <image> out/checks/<name>/grid.png

# Zoomed, finer grids on the areas that need precision:
python3 .claude/skills/overlay-coordinate-grid/scripts/grid.py <image> out/checks/<name>/grid.png \
  --region head=720,0,1240,330,25,2 --region hands=420,840,1520,1080,50,1 \
  --save-normalised out/checks/<name>/frame.png
```

- Every label is in composition pixels (the image is normalised to `--size`,
  default 1920x1080), so numbers go straight into code.
- A region is `NAME=x0,y0,x1,y1[,step[,zoom]]`. Grid the whole frame first to find the
  area, then tighten the box and raise the zoom.
- Transparent renders are flattened onto `--background` (`dark` by default; use
  `light` when checking dark elements).
- `--save-normalised` keeps a resized copy of a footage frame to composite onto later.
- It warns when the source aspect ratio is more than 1% off target. For a screenshot
  that almost always means player chrome or letterboxing — crop it out first or every
  coordinate is skewed.

**What to write down:**
- **Bounds** of text and shapes — the real left/right/top/bottom, not the `x`/`y` you
  passed in.
- **Anchor points** for footage — where a graphic makes contact: crown of the hair,
  hairline, palm centres, thumb tips, an object's corner.
- **Tilt** from a rigid feature pair. For a head, use the eyes, *never the eyebrows* —
  a raised brow reads as a 13° tilt on a head tilted 4°.
- **Scale** from a known span: head width, distance between hands, an element's width.
- **Clearances** between elements that mustn't touch, and to the frame edges.

## 3. Build with measured numbers

- Put measured values in **named constants at the top of `Main.tsx`, with a comment
  saying where they were measured** ("calibrated from a render: glyphs span x 335–1590").
  Re-fitting to a new shot or a copy change should be a constants edit.
- **Draw each object in its own local coordinates** (centred on 0,0, lying along +x)
  and place it with `translate(x y) rotate(angle) scale(s)`. Geometry stays independent
  of placement, and entrance animation composes onto the same transform.
- **Rotate about the point of contact**, not the object's centre — the bottom of a
  cap's band, the hand holding a prop — or tilting lifts it off what it rests on.
- **Hand-held props sit over the thumb or palm.** An overlay can't go behind a finger,
  so pick angles where covering the thumb reads as gripping.
- **Say whose left and right.** A person facing camera has their left hand on the
  right of the screen. Describing a screenshot, default to screen sides, say so, and
  make swapping a one-line change.
- Check rotated extents stay inside the frame.

## 4. Verify on a grid, then iterate

Re-render the key phases and lay them out gridded:

```bash
# Onto footage:
python3 .claude/skills/overlay-coordinate-grid/scripts/composite.py out/checks/<name>/review.png \
  out/checks/<name>/still-20.png out/checks/<name>/still-100.png \
  --base out/checks/<name>/frame.png --grid 100 --detail x0,y0,x1,y1

# No footage — over dark and light fields:
python3 .claude/skills/overlay-coordinate-grid/scripts/composite.py out/checks/<name>/review.png \
  out/checks/<name>/still-100.png --fields --grid 100
```

- `--grid` labels tiles and detail crops in composition pixels, so a correction is read
  straight off the sheet rather than guessed again.
- `--detail` appends full-resolution crops of the last composite, one per critical
  area — where you see whether a cap rests on the hair or floats, or whether a line
  clears a label by 4px or overlaps it.
- `--fields` is also the check for white-on-transparent elements, which are invisible
  against a white preview.

Adjust constants from the measurements and repeat until every critical area is right.

## 5. For footage-anchored overlays, flag the limitation

Placement is static: it lines up only while the subject stays near the measured pose,
and people move — hands most. Say so every time and offer:

1. **One overlay per anchor** (head, each hand) so each can be motion-tracked
   independently in the edit.
2. **Keyframed anchors** — extract frames across the clip, grid each, interpolate the
   constants over time.

## Worked examples

- `src/remotion/GraduationLesson/Main.tsx` — footage-anchored: a mortarboard placed from
  a gridded screenshot, tilted from the eye line, rotating about the band's contact point.
- `src/remotion/IdentityShell/Main.tsx` — no footage: the crack field's bounding box and
  impact corner are measured from a gridded render of the word, not from its font size.
