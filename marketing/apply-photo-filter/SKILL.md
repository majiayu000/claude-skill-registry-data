---
name: apply-photo-filter
description: Apply one controlled photographic color-and-texture treatment while preserving subjects, geometry, identity, and scene. Use for film emulation, monochrome, faded, warm, cool, matte, grain, or reference-led grading; not content transformation.
---
# Apply Photo Filter
## Catalog
- Display name: Apply Photo Filter
- Categories: Social Media, Portrait
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: orange
- Short description: Apply one filter without changing scene content.
- Similar skills: remove-photo-filter, recolor-object
## What this skill does
- Changes palette, tone curve, saturation, grain, bloom, and vignette as one treatment.
- Preserves people, objects, text, crop, and spatial structure.
## How to use
Provide image, filter recipe or reference, intensity, and protected colors.
#### Apply a film look
```text
Apply a restrained 1990s film look with warm highlights, cool shadows, and fine grain at 40%.
```
## Workflow
1. Separate invariants from white balance, contrast, black point, saturation, grain, bloom, and vignette.
2. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
3. Forbid pose, face, object, background, text, or crop changes.
4. Compare landmarks for drift; inspect skin, neutrals, clipping, banding, noise, and intensity.
5. Retry with narrower controls if content or composition changes.
## User-facing output
- Media type: One filtered photograph
- Default quantity: 1
- Content per image: Unchanged source content with one grade
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Social, editorial, and campaign grading
