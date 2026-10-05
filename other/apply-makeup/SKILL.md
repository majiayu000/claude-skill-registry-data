---
name: apply-makeup
description: Apply one makeup look to a supplied portrait while preserving identity, facial structure, natural skin texture, hair, clothing, pose, lighting, and background. Use for beauty, bridal, editorial, stage, product-shade, or reference-makeup previews; do not use to reshape the face or change skin identity.
---

# Apply Makeup

## Catalog

- Display name: Apply Makeup
- Categories: Portrait, Fashion
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Preview one makeup look without replacing or reshaping the face.
- Similar skills: retouch-blemish, smooth-wrinkles
## What this skill does

- Produces one portrait with one coherent makeup treatment.
- Separates eye, brow, cheek, complexion, and lip instructions.
- Preserves pores, facial landmarks, age, expression, hair, wardrobe, and scene.

## How to use

Provide one clear portrait and describe the finish, palette, and intensity.

#### Apply natural editorial makeup

```text
Apply soft editorial makeup with brown liner, muted rose lips, subtle blush, and natural skin texture.
```

## Workflow

1. Confirm adequate face resolution; record finish, palette, intensity, and no-change regions.
2. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
3. Prompt makeup by facial region and preserve facial geometry, skin tone, pores, age, expression, hair, clothing, crop, lighting, and background.
4. Forbid face slimming, eye enlargement, skin bleaching, plastic smoothing, identity replacement, text, or panels unless separately requested.
5. Inspect placement, bilateral consistency, skin texture, lip and lash edges, and identity. Retry only the failed region or intensity.

## User-facing output

- Media type: One edited portrait image
- Default quantity: 1
- Content per image: One person with one makeup look
- Default layout: Preserve source composition; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Beauty consultation, campaign planning, and personal preview
