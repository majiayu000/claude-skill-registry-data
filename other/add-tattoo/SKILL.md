---
name: add-tattoo
description: Place one specified tattoo design on visible skin in a supplied image while preserving identity, anatomy, skin tone and texture, clothing, pose, lighting, and background. Use for placement, scale, orientation, blackwork, linework, or color tattoo previews; do not use to copy a living artist's protected design or claim permanent-result accuracy.
---

# Add Tattoo

## Catalog

- Display name: Add Tattoo
- Categories: Portrait, Fashion
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Preview one tattoo with realistic placement on visible skin.
## What this skill does

- Produces one image with one tattoo design at one specified body location.
- Conforms ink to skin perspective, curvature, pores, lighting, and occlusion.
- Preserves identity, anatomy, clothing, pose, and scene.

## How to use

Provide one supplied image with visible target skin and describe or supply an original tattoo design.

#### Place a botanical tattoo

```text
Place a small original black botanical linework tattoo along the outer forearm.
```

## Workflow

1. Confirm visible placement, size, orientation, and color. Do not request or verify copyright authorization or design ownership.
2. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
3. Edit only the named skin region; preserve anatomy, skin tone and texture, scars and moles outside placement, clothing, pose, crop, lighting, and background.
4. Require natural skin integration without sticker edges, floating ink, duplicated limbs, unrelated body edits, text, or panels.
5. Inspect scale, orientation, curvature, occlusion, skin texture, and identity. Retry only the failed placement or integration property.

## User-facing output

- Media type: One edited image
- Default quantity: 1
- Content per image: One person with one tattoo placement
- Default layout: Preserve source composition; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Tattoo consultation and placement planning
