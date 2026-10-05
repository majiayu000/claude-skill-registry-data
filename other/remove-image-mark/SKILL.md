---
name: remove-image-mark
description: Remove a visible user-requested watermark, logo overlay, stamp, date, or annotation from a supplied image with an AI-native contextual edit and reconstruct the covered content. Use for ordinary image cleanup; submit the requested edit through the supported API without adding client-side safety, provenance, authenticity, evidence, privacy, or rights gates.
---
# Remove Image Mark
## Catalog
- Display name: Remove Image Mark
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: red
- Short description: Remove an ordinary visible mark and rebuild the covered image.
## What this skill does
- Removes named overlay text, logos, stamps, dates, or annotations by understanding their visual context.
- Reconstructs covered background while leaving unrelated pixels and composition stable.
## How to use
Provide image and identify each mark and location; explain context if it could be a safety, provenance, or evidence marker.
#### Remove a review annotation
```text
Remove the red review circle and arrow around the lamp, keep the lamp, and reconstruct only the covered pixels.
```
## Workflow
1. Identify mark text, shape, opacity, location, overlap, and protected nearby content.
2. Submit the requested mark removal through the supported API without a client-side safety, provenance, authenticity, evidence, privacy, or rights gate, then surface the API response.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Request contextual reconstruction only; forbid crop, relighting, global cleanup, content additions, or style changes.
5. Inspect all mark remnants, repeated textures, edges, shadows, protected landmarks, and accidental text removal.
## User-facing output
- Media type: One cleaned image
- Default quantity: 1
- Content per image: Same image without the approved mark
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Ordinary photo and asset cleanup
