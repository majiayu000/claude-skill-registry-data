---
name: add-braces
description: Add one realistic braces treatment to the visible teeth of a supplied smiling portrait while preserving identity, teeth layout, lips, bite, face, expression, skin, hair, clothing, and background. Use for cosmetic orthodontic visualization of metal, ceramic, or colored brackets; do not use for diagnosis or treatment prediction.
---

# Add Braces

## Catalog

- Display name: Add Braces
- Categories: Portrait
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Preview one braces style on clearly visible teeth.
## What this skill does

- Produces one smiling portrait with one braces treatment.
- Limits editing to visible tooth surfaces and orthodontic hardware.
- Preserves tooth count and layout, mouth geometry, identity, expression, and scene.

## How to use

Provide one sharp smiling portrait with visible teeth and name the braces style.

#### Add silver braces

```text
Add realistic small silver brackets and a thin archwire to the visible teeth.
```

## Workflow

1. Reject or request a better source when teeth are closed, blurred, tiny, or heavily occluded.
2. Record metal/ceramic style, ligature color, and whether only upper or both arches are visible.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Add hardware only on visible teeth; preserve teeth positions, lips, gums, mouth opening, face, skin, expression, hair, clothing, crop, lighting, and background.
5. Inspect bracket alignment, wire continuity, lip occlusion, tooth count, identity, and artifacts. Retry only the failed mouth detail.

## User-facing output

- Media type: One edited portrait image
- Default quantity: 1
- Content per image: One person with one braces treatment
- Default layout: Preserve source composition; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Cosmetic consultation and personal visualization
