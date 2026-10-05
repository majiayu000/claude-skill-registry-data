---
name: recolor-object
description: Change only a named object or PNG element to a target color while preserving shape, material texture, luminance, highlights, shadows, transparency, and everything outside the target. Use for product colorways and local color edits.
---
# Recolor Object
## Catalog
- Display name: Recolor Object
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: violet
- Short description: Recolor one object without tinting the whole image.
- Similar skills: apply-photo-filter, remove-photo-filter
## What this skill does
- Identifies one target region and changes hue/chroma without flattening material.
- Keeps untargeted objects, people, background, lighting, and geometry unchanged.
## How to use
Provide image, target object, and color name, swatch, RGB, or hex.
#### Recolor one product
```text
Change only the yellow chair to #174A36; preserve grain, highlights, and shadow.
```
## Workflow
1. Bind target by object, location, and optional mask; define trim, logo, hardware, and reflection scope.
2. Preserve the original luminance structure and material response.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Forbid global grade, material replacement, geometry drift, or background edits.
5. Compare coverage, edge halos, texture, highlights, shadows, and neutral regions.
## User-facing output
- Media type: One locally recolored image
- Default quantity: 1
- Content per image: Original scene with one target recolored
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Product colorways and previews
