---
name: expand-image
description: Extend one supplied image to a new aspect ratio or larger canvas by generating only the added surroundings while preserving the existing subject, scene, copy, and composition. Use for outpainting, portrait-to-landscape or square-to-vertical conversion, platform-size adaptation, safe-area or copy-space creation, and fixing ratio mismatches after another image Skill; do not use for simple upscaling, ordinary cropping, background replacement, redesign, or adding new story content.
---

# Expand Image

Turn one accepted image into a larger canvas without stretching it. Treat the original image as the protected center of truth and generate only the new margins.

## Catalog

- Display name: Expand Image
- Kind: Atom
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 preservation-first outpainting with Expand Image fallback
- Tone: sky
- Short description: Extend an image to a new ratio without stretching it.
## What this skill does

- Converts an existing image to a requested ratio or pixel canvas by adding generated surroundings.
- Chooses target dimensions and original-image placement before execution.
- Preserves subjects, products, faces, garments, logos, readable copy, perspective, lighting, and the original scene.
- Restores the original pixel region after outpainting when exact source fidelity matters.
- Creates intentional safe area or copy space by placing the original off-center when requested.
- Validates dimensions, source continuity, seams, repeated objects, invented content, and output count.

## How to use

Provide one image and the target ratio or pixel size; optionally say where the existing subject should remain.

#### Convert square to portrait

```text
Expand this image to 4:5 and keep the existing composition centered.
```

#### Create banner copy space

```text
Expand this image to 16:9, keep the product on the right, and leave clean space on the left.
```

#### Fit a vertical placement

```text
Extend this poster to 9:16 without changing its existing subject or readable text.
```

## Workflow

### 1. Bind the protected image

Require one complete source image. Record its pixel dimensions, target ratio or exact dimensions, intended placement, protected subjects/copy/logos, and whether a platform safe area is required.

Route pure enlargement at the same ratio to an upscaler, a removable crop to deterministic cropping, and any redesign or new subject to the owning generation/editing Skill.

Read [references/geometry-and-routing.md](references/geometry-and-routing.md) before calculating the canvas. Read [references/edge-text.md](references/edge-text.md) whenever readable text, a logo, label, UI, or typography appears within the source. Read [references/acceptance.md](references/acceptance.md) before execution.

### 2. Calculate the smallest valid canvas

Never stretch the source. For target ratio `r = width / height`:

```text
if sourceWidth / sourceHeight < r:
  targetHeight = sourceHeight
  targetWidth = ceil(sourceHeight * r)
else:
  targetWidth = sourceWidth
  targetHeight = ceil(sourceWidth / r)
```

Adjust by at most one pixel to express the requested ratio, keep both target dimensions at or below 4096, and require the target canvas to contain the protected source area. Use explicit user pixel dimensions when valid.

### 3. Place the original deliberately

- center by default: omit `fillLeft` and `fillTop`, or use the calculated centered offsets;
- copy space left: place the original toward the right;
- copy space right: place it toward the left;
- copy space above: place it toward the bottom;
- copy space below: place it toward the top.

Do not use negative offsets as a hidden crop unless the user explicitly authorizes cropping and protected content remains intact.

### 4. Select the route

- **Default:** use GPT Image 2 medium/2K with the source as an edit reference. Compile one preservation-first outpainting Prompt containing target ratio, source placement, protected content, scene-continuity constraints, and an explicit ban on new text, logos, subjects, products, and props.
- **One fallback only:** if the GPT Image 2 result fails visual acceptance, use `expandimage` v1.0 once with `targetWidth`, `targetHeight`, optional `fillLeft`/`fillTop`, and `batchCount: 1`. Do not climb a model ladder or repeat identical runs.
- **Exact arbitrary pixels:** GPT Image 2 owns common ratio outputs; route exact nonstandard pixel canvases to `expandimage` when its geometry is required. The endpoint is parameter-only, so do not send `textDescription` to it.
- **Low-detail margin fallback:** when the requested side contains a verified subject-free, text-free, low-detail background strip, deterministic reflection/texture extension may replace generative filling. Use only the clean strip, preserve the full source layer, and reject visible repetition or seams.
- **Exact unchanged pixels required:** run the outpaint, then use `scripts/restore_original_region.py` to paste the original lossless pixels back at the verified offsets. Inspect the seam afterward.

### 5. Protect edge text before generation

- complete text away from the expansion boundary: outpaint, then restore the original region;
- complete text near an edge: prefer expanding the opposite side, restore the original, and never feather across glyphs;
- text already clipped by the source edge: do not invent the missing characters; request the uncropped source or hand exact copy and typography specifications to Layout Composition;
- text that must move or reflow: expand the visual base first, then rebuild the copy deterministically in the owning layout Skill.

Reject any pseudo-text, ghost letter, repeated word, continued logo stroke, or generated copy in the new margins.

### 6. Execute, restore, and accept

Submit one GPT Image 2 result with `batchCount: 1` and poll to terminal state. Accept it or make one justified fallback call; do not spend runs progressively testing multiple models. When source fidelity or text protection matters and the source mapping is known, run:

```text
python scripts/restore_original_region.py --original SOURCE.png --expanded OUTPAINT.png --output FINAL.png --fill-left X --fill-top Y
```

Apply every check in [references/acceptance.md](references/acceptance.md), including the restored-region and seam checks. API success is not visual acceptance.

The bundled script requires Pillow and writes a lossless PNG. If Pillow is unavailable, use an equivalent deterministic layer composite or report that pixel-identical restoration was not performed; never silently claim it.

### 7. Retry one failed property

- wrong dimensions: correct target geometry; do not alter the image request;
- subject shifted or cropped: correct `fillLeft`/`fillTop` and rerun;
- seam or texture break: retry once with centered placement or a smaller single-axis expansion;
- duplicated object: use the fallback editor with explicit source locks;
- invented or damaged text: restore the original region; if pseudo-text appears only in a low-detail new margin, replace that margin deterministically from a verified text-free edge strip; if text was clipped or must reflow, stop image generation and route to deterministic layout;
- severe source drift: stop using the specialized result and switch to deterministic preservation or a reference-aware editor;
- excessive expansion: split into staged expansions only when one large expansion fails, inspecting every intermediate result.

Never resend an identical failed request. Record source and target dimensions, offsets, route, execution ID, terminal state, acceptance failure, and fallback reason.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One expanded image plus original and acceptance record
- Default quantity: 1 separate image
- Content per image: One protected source composition with newly generated outer canvas
- Default layout: Centered source unless the user requests directional safe area or copy space
- Model policy: GPT Image 2 medium/2K first; one `expandimage` fallback only after visual failure or when exact arbitrary pixel geometry requires it
- Downstream use: Ratio correction for every image Skill, posters, banners, product pages, social placements, and campaign variants
