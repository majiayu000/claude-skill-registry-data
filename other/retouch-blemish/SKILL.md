---
name: retouch-blemish
description: Remove named temporary skin blemishes from a supplied portrait while preserving identity, pores, skin texture, age, facial structure, marks not requested for removal, lighting, and background. Use for restrained portrait retouching, not beauty filtering or face reshaping.
---
# Retouch Blemish
## Catalog
- Display name: Retouch Blemish
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Remove temporary blemishes without plastic-looking skin.
- Similar skills: apply-makeup, smooth-wrinkles
## What this skill does
- Removes only specified temporary spots, redness, or small imperfections.
- Preserves identity, pores, natural tonal variation, freckles, moles, and age unless explicitly targeted.
## How to use
Provide a supplied portrait and specify which temporary blemishes to remove and which marks to keep.
#### Retouch one portrait
```text
Remove the temporary forehead and chin blemishes; keep freckles, pores, mole, face shape, and lighting.
```
## Workflow
1. Separate temporary targets from protected permanent traits; do not infer that every mark is unwanted.
2. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
3. Request localized healing with source-consistent texture and lighting; forbid smoothing, makeup, reshaping, whitening, or age change.
4. Compare eyes, nose, mouth, jaw, freckles, moles, pores, hair, background, and light direction.
5. Reject waxy skin, erased texture, face drift, broad color changes, or removal of protected marks.
## User-facing output
- Media type: One retouched portrait
- Default quantity: 1
- Content per image: Same person with specified blemishes removed
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Portrait and profile-photo cleanup
