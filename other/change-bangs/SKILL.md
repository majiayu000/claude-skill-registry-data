---
name: change-bangs
description: Add or change only bangs in one supplied portrait while preserving identity, the rest of the hairstyle, hair color, face, clothing, pose, and background. Use for curtain, blunt, wispy, side-swept, micro, or reference-fringe previews; do not use for a full haircut replacement.
---

# Change Bangs

## Catalog

- Display name: Change Bangs
- Categories: Portrait, Fashion
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Preview one fringe style without replacing the full haircut.
- Similar skills: hairstyle-change, hair-color-change, shave-head
## What this skill does

- Produces one portrait with one requested bangs style.
- Limits editing to the forehead and front hair section.
- Preserves the remaining cut, hair color, identity, face, and scene.

## How to use

Provide one front or three-quarter portrait and describe the fringe shape and length.

#### Add curtain bangs

```text
Add soft eyebrow-length curtain bangs with a light center opening.
```

## Workflow

1. Confirm forehead, hairline, eyebrows, and both eyes are sufficiently visible.
2. Record fringe type, opening, length, density, texture, and color lock.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Restrict the edit to front hair; preserve all other hair, eyes, facial proportions, skin, clothing, crop, lighting, and background.
5. Check hairline integration, eye visibility, requested shape, and identity. Retry only the failed local property.

## User-facing output

- Media type: One edited portrait image
- Default quantity: 1
- Content per image: One person with one bangs treatment
- Default layout: Preserve source composition; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Salon consultation and haircut planning
