---
name: hair-color-change
description: Change only the hair color in one supplied portrait while preserving identity, hairstyle geometry, face, skin, clothing, pose, lighting, and background. Use for salon color previews, dye simulations, root-to-tip recoloring, highlights, balayage, or natural fantasy-color previews; do not use to change the haircut or add hair.
---

# Hair Color Change

## Catalog

- Display name: Hair Color Change
- Categories: Portrait, Fashion
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Preview one new hair color without changing the person or cut.
- Similar skills: change-bangs, hairstyle-change, shave-head
## What this skill does

- Produces one recolored-hair portrait from one supplied source portrait.
- Changes pigment only; keeps length, texture, volume, part, hairline, and flyaways.
- Preserves identity and every non-hair region.

## How to use

Provide one clear portrait and name one target shade or coloring pattern.

#### Preview auburn hair

```text
Change this person’s hair to natural copper auburn with subtle root depth.
```

## Workflow

1. Confirm the portrait is supplied and contains one clearly visible person.
2. Record target color, distribution, intensity, and whether eyebrows must remain unchanged.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Recolor the existing hair while preserving hairstyle geometry, hairline, face, skin, eyes, clothing, pose, crop, lighting, and background. Forbid haircut changes, wigs, extra subjects, text, or panels.
5. Poll to terminal state and compare hair silhouette, facial landmarks, skin tone, and scene. Retry only the failed property with revised wording.

## User-facing output

- Media type: One edited portrait image
- Default quantity: 1
- Content per image: One person with one hair-color treatment
- Default layout: Preserve source composition; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Salon consultation, personal preview, and beauty creative
