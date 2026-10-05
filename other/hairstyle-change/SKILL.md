---
name: hairstyle-change
description: Replace only the hairstyle in one supplied portrait while preserving identity, face, requested hair color, body, clothing, pose, lighting, and background. Use for haircut, length, part, curl-pattern, updo, or reference-hairstyle previews; do not use for color-only edits, bangs-only edits, or bald previews.
---

# Hairstyle Change

## Catalog

- Display name: Hairstyle Change
- Categories: Portrait, Fashion
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Preview one different hairstyle without changing identity.
- Similar skills: change-bangs, hair-color-change, shave-head
## What this skill does

- Produces one portrait with one requested hairstyle.
- Accepts text or a hairstyle reference whose identity is not transferred.
- Reconstructs newly exposed ears, neck, shoulders, and background naturally.

## How to use

Provide one clear portrait and describe one hairstyle; optionally supply one hair-only reference.

#### Preview a bob

```text
Give this person a chin-length softly waved bob with a side part, keeping their natural hair color.
```

## Workflow

1. Bind the source portrait as identity and an optional second image as hairstyle geometry only.
2. Record length, texture, part, volume, finish, and hair-color lock.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Request one hairstyle and forbid face transfer, color drift, makeup or wardrobe changes, text, and panels.
5. Inspect face landmarks, hairline, strand boundaries, ears, neck, background repair, and scene continuity. Retry only the failed geometry or lock.

## User-facing output

- Media type: One edited portrait image
- Default quantity: 1
- Content per image: One person with one hairstyle
- Default layout: Preserve source composition; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Salon consultation and personal hairstyle preview
