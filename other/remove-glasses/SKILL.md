---
name: remove-glasses
description: Remove eyeglasses from a supplied portrait and reconstruct naturally visible eyes, brows, nose bridge, temples, skin, and lighting while preserving identity, gaze, expression, pose, hair, and background. Use for eyewear removal, not face replacement or beauty filtering.
---
# Remove Glasses
## Catalog
- Display name: Remove Glasses
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: blue
- Short description: Remove glasses and naturally restore the eye area.
## What this skill does
- Removes frames, lenses, nose pads, temple arms, glare, lens tint, refraction, and frame shadows.
- Reconstructs occluded face regions without changing identity or expression.
## How to use
Provide one supplied portrait with visible glasses and state any eye traits that must remain.
#### Remove eyeglasses
```text
Remove the eyeglasses, lens glare, and frame shadows; preserve gaze, eye color, expression, and identity.
```
## Workflow
1. Inspect frame path, lens distortion, glare, shadow, occluded brows, nose bridge, temples, and hair.
2. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
3. Request face-aware reconstruction; forbid eye enlargement, makeup, skin smoothing, face reshaping, or expression changes.
4. Compare eye spacing, gaze, iris color, eyelids, brows, bridge, temples, ears, hair, and facial symmetry.
5. Reject frame remnants, phantom glare, mismatched eyes, invented eyelashes, skin seams, or identity drift.
## User-facing output
- Media type: One glasses-free portrait
- Default quantity: 1
- Content per image: Same person without eyewear
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Portrait and profile-photo repair
