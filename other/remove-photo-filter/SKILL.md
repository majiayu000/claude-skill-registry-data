---
name: remove-photo-filter
description: Neutralize an applied photographic filter or color grade and recover a natural-looking color, contrast, white balance, and texture while preserving scene content and acknowledging that hidden original colors may be uncertain. Use for exaggerated tints, matte looks, heavy contrast, grain, vignettes, or beauty-filter color treatment.
---
# Remove Photo Filter
## Catalog
- Display name: Remove Photo Filter
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: sky
- Short description: Remove an artificial grade and restore a natural look.
- Similar skills: apply-photo-filter, recolor-object
## What this skill does
- Identifies visible filter symptoms and asks the image model to neutralize them coherently.
- Preserves people, geometry, objects, text, crop, and genuine scene lighting.
## How to use
Provide filtered image, known original references if available, and desired natural-light target.
#### Remove a heavy filter
```text
Remove the strong orange-teal grade, crushed blacks, vignette, and added grain; restore plausible daylight color.
```
## Workflow
1. Describe filter symptoms: cast, curve, saturation, clipping, grain, bloom, vignette, and beauty effects.
2. Record any known neutral references; state that unrecoverable hidden colors are inferred.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Forbid content, face, texture, crop, pose, background, and lighting-direction changes.
5. Inspect neutrals, skin, highlights, shadows, banding, residual cast, texture, and content stability.
## User-facing output
- Media type: One naturalized photograph
- Default quantity: 1
- Content per image: Same source with filter symptoms reduced
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Photo correction and asset normalization
