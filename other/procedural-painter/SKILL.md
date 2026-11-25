---
name: procedural-painter
description: >-
  Paint finished, painterly images entirely with code, with no image model, reference
  images or downloaded assets. Builds a procedural underpainting (3D geometry, noise
  landscapes, mirrored water, lights), paints it with curved brush strokes along a
  style flow field, adds impasto, then inspects and iterates. Use for "paint X in the
  style of Y with code", "generative painting", "no-AI-image artwork", "made with
  Python" art, or procedural illustrations in post-impressionist, impressionist,
  ukiyo-e, or Northern Renaissance styles.
---

# Procedural Painter

Create a finished painterly image entirely through code.

## Core constraint

The final artwork must be rendered from code.

Do not:
- call an image-generation API or model
- download or use reference images, textures, stock art, or external visual assets
- trace an existing artwork
- hide image assets inside base64 or package files

Use Python with NumPy, SciPy and Pillow. Nothing else is needed.

## Bundled engine (use it, do not rewrite it)

`scripts/pp/` is a working engine; start from it and a matching example:

- `pp/core.py`: fBm value noise, colour ramps and HSV, supersampled masks, pinhole `Camera`.
- `pp/bridge.py`: an example 3D landmark model (the Golden Gate Bridge at real proportions) and a
  box/cable rasteriser with depth. Model new subjects the same way: boxes, extrusions, curves.
- `pp/strokes.py`: `Painter`, the stroke painter with coarse-to-fine layers, region-bounded
  strokes, per-region brush limits, colour jitter hooks, a rigger brush (`line`, `dab`), and the
  impasto finish (LIC bristles plus emboss lighting).
- `golden_gate_*.py`: four complete paintings, one per style below. Seeds are fixed, so the
  outputs are byte-identical on rerun. `grid.py` assembles a 2x2.

Run from anywhere: `python3 scripts/golden_gate_ukiyoe.py` writes `out/p3_ukiyoe.png`.
Pass `--under` to any stroke-based example to save only the underpainting (seconds).

## The method: underpainting, then strokes

Painting pixel by pixel with noise produces "generative art". What produces a painting is
**stroke-based rendering over a scene built in code**, the classic Hertzmann (SIGGRAPH '98)
algorithm with a code-built scene in place of the photograph it normally needs.

1. **Build the underpainting (the scene).** Render a plain, smooth image of the subject:
   - Landmarks and architecture: model them in 3D with real proportions (boxes, catenary
     cables) and project with a pinhole camera. Accurate proportions make the subject
     instantly recognisable.
   - Sky, hills, water: gradient ramps plus fBm value noise; ridgelines from 1D fBm.
   - Water: mirror the scene above the horizon, then displace it with horizontally stretched noise.
   - Lights: Gaussian glow fields plus vertical reflection streaks.
   - Keep a **region label map** (sky, water, land, subject, ...) alongside the colours.
2. **Define a flow field for the style.** A unit vector field for stroke direction:
   vortices (post-impressionist), diagonal hatching (impressionist), slope-following on
   hills, horizontal on water, vertical flames for cypresses.
3. **Paint coarse to fine (Hertzmann).** For each brush radius R, large to small:
   blur the reference by ~R/2, compute the error against the canvas on a grid of cell size R, and
   start strokes where the error exceeds a threshold. Trace each stroke along the flow field, blended
   with the edge tangent where the image gradient is strong, and stop when colour drifts or the
   **region label changes**, so strokes never bleed across the subject's outline.
   Per-region min/max brush radius keeps the subject crisp and big areas bold.
4. **Rigger pass.** Re-state thin structure (cables, lamps, figures, branches) with a thin
   brush after the strokes. Strokes wash out anything thinner than the brush.
5. **Impasto.** Record a per-stroke height; add bristle streaks with line-integral convolution
   of noise along the flow field; emboss-light it. That is what makes it read as paint.
6. **Finish.** Palette/contrast pass, varnish tint, craquelure (Voronoi edges) for old-master styles.

Vectorise stroke tracing in NumPy (all strokes of one layer step together) and draw with
`ImageDraw.line(width=2R, joint='curve')`. At 2400×1800, 100k–900k strokes render in 20–170 s.

## Style recipes (tested)

| Style | Scene choice | Strokes | Signature |
|---|---|---|---|
| Post-impressionist swirl | low camera, big sky; moon + haloed stars; cypress | R 26→2, maxlen 7–10, sat ×1.3, value jitter 0.16; min R 9 in sky | LIC swirl **bands baked into the sky** so the strokes pick up light and dark ribbons; vortex field |
| Impressionist broken colour | fog bank, afterglow, mirrored water | short dabs (maxlen 4), R 22→5, hue jitter ≈0.015, 7% warm and 7% cool flecks | depth haze on the subject; keep values close |
| Ukiyo-e woodblock | Fuji-like peak, moon, framing pine | **no strokes** | flat 2-tone blocks, bokashi ramps, sumi key lines from label borders (skip thin parts), kasumi bands, scalloped waves shrinking toward the horizon, paper fibre, baren mottling, misregistration |
| Northern Renaissance winter | elevated view, snow slope, hamlet, frozen pond | fine R 12→2, low jitter | many tiny narrative marks (hunters, dogs, skaters, fence, tracks, lit windows, smoke), varnish, faint craquelure |

## Failure modes seen and their fixes

- **Subject unrecognisable**: the camera saw the tower edge-on. Look roughly along the bridge axis so the portals show.
- **"Oil filter" look**: too many small strokes and uniform jitter. Set a minimum brush size in big regions, use longer strokes, and add value variation to the underpainting.
- **Confetti**: impressionist hue jitter set too high. Keep flecks rare and values close.
- **Cartoon or vector look**: flat fills with no stroke texture. Always run the impasto pass.
- **Dead snow and sky**: add narrative marks, cast shadows clipped to the surface, tufts, tracks.

## Workflow

1. Preview the underpainting only (`--under` flag, ~5 s) until composition, horizon and subject size are right.
2. Paint, then inspect the full frame **and** a 1:1 crop. Do at least two improvement passes.
3. Deterministic `SEED` in every source; save the PNG next to its source.

## Deliver

- final PNG (≥1600×1200)
- Python source + seed + dependencies
- 3–5 bullets on the procedural techniques used

## Quality bar

The artwork should be visually interesting before the viewer knows it was made with code.
If it looks like "generative art" rather than a painting, keep iterating.
