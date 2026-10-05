---
name: recreate-social-photo
description: Recreate the composition, camera feel, lighting, color treatment, and mood of a supplied social-photo reference with a supplied everyday source photo while preserving source identity. Use for reference-led casual social photos, not generic studio shoots or filter-only edits.
---
# Recreate Social Photo
## Catalog
- Display name: Recreate Social Photo
- Categories: Social Media, Portrait
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Turn an everyday photo into a reference-led social photo.
## What this skill does
- Maps source identity and reference visual grammar separately.
- Recreates framing, pose energy, lens feel, light, grade, texture, and mood without copying reference identity.
## How to use
Provide one supplied person photo and one visual reference; state protected traits.
#### Recreate a social photo
```text
Use my portrait as the person and image 2 only for composition, light, color, and mood.
```
## Workflow
1. Label identity source and visual reference; never swap roles.
2. Inspect crop, viewpoint, subject scale, gesture, light direction, palette, contrast, grain, and background rhythm.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Preserve identity; reproduce visual grammar rather than the reference face, logos, or text.
5. Reject identity drift, generic studio posing, filter-only output, collage, duplicates, or copied text.
## User-facing output
- Media type: One recreated social photograph
- Default quantity: 1
- Content per image: One coherent social-photo frame
- Default layout: Single image; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Personal and brand social posts
