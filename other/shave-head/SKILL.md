---
name: shave-head
description: Preview one supplied person with a natural bald or closely shaved scalp while preserving identity, face, age, head shape, skin tone, facial hair, clothing, pose, lighting, and background. Use for clean-shaven head, buzz cut, or hair-loss appearance previews; do not use for medical prediction.
---

# Shave Head

## Catalog

- Display name: Shave Head
- Categories: Portrait, Fashion
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Preview a natural bald or shaved-head appearance.
- Similar skills: change-bangs, hairstyle-change, hair-color-change
## What this skill does

- Produces one bald or shaved-head portrait.
- Reconstructs scalp, ears, neck, and background naturally.
- Preserves identity, head proportions, facial hair, age, skin, clothing, and scene.

## How to use

Provide one clear portrait and specify clean bald, stubble, or buzz length.

#### Preview a clean shaved head

```text
Show this person with a clean naturally shaved scalp while keeping their beard unchanged.
```

## Workflow

1. Confirm one visible head; note hats, hands, or other occlusions.
2. Record scalp finish, stubble amount, and facial-hair lock.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Remove only scalp hair; preserve skull proportions, face, brows, lashes, facial hair, skin tone, age, pose, clothing, lighting, crop, and background.
5. Inspect contour, former hair boundary, ears, shadows, background reconstruction, and identity. Retry only failed realism or preservation.

## User-facing output

- Media type: One edited portrait image
- Default quantity: 1
- Content per image: One person with one scalp treatment
- Default layout: Preserve source composition; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Grooming consultation and personal preview
