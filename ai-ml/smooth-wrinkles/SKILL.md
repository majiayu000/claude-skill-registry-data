---
name: smooth-wrinkles
description: Reduce specified skin lines or garment wrinkles in a supplied image while preserving identity, age cues, anatomy, fabric construction, texture, seams, folds needed for volume, lighting, and scene. Use only after the agent determines whether the target is skin or clothing.
---
# Smooth Wrinkles
## Catalog
- Display name: Smooth Wrinkles
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: sand
- Short description: Reduce chosen skin or clothing wrinkles without flattening structure.
- Similar skills: apply-makeup, retouch-blemish
## What this skill does
- Treats skin lines and fabric creases as different AI edits with different protected traits.
- Reduces distracting wrinkles while retaining realistic texture and form-defining folds.
## How to use
Provide image, target region, skin or garment type, and desired reduction strength.
#### Smooth garment wrinkles
```text
Reduce packing creases on the linen shirt body; keep seams, weave, collar structure, and natural elbow folds.
```
## Workflow
1. Classify target as skin or garment and identify structural lines that must remain.
2. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
3. For skin, preserve age and identity; for fabric, preserve weave, seams, drape, edges, and volume.
4. Forbid anatomy, silhouette, garment design, color, background, makeup, or relighting changes.
5. Reject plastic skin, iron-flat fabric, melted seams, lost texture, or unrelated edits.
## User-facing output
- Media type: One selectively smoothed image
- Default quantity: 1
- Content per image: Same image with one wrinkle treatment
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Portrait and apparel retouching
