---
name: colorize-image
description: Add plausible, context-aware color to a black-and-white or grayscale image while preserving identity, content, tonal structure, texture, era cues, and damage. Use for archival-style, family, editorial, or creative colorization; disclose when colors are inferred rather than documented.
---
# Colorize Image
## Catalog
- Display name: Colorize Image
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 contextual colorization
- Tone: gold
- Short description: Add plausible color while preserving the original photograph.
## What this skill does
- Uses whole-image context to infer coherent skin, fabric, object, and environment colors.
- Distinguishes documented color references from plausible creative inference.
## How to use
Provide grayscale image, known colors or references, desired realism, and disclosure needs.
#### Colorize a grayscale photo
```text
Colorize this grayscale 1950s-style family photo naturally; preserve faces, grain, contrast, clothing, and background.
```
## Workflow
1. Record known colors and protected monochrome evidence; mark all unsupported colors as inferred.
2. Use `gpt-image` v1.0, GPT Image 2 Medium, source, original ratio, `batchCount: 1`.
3. Request restrained context-aware color without sharpening, restoration, face changes, object additions, or modernized styling.
4. Compare geometry, identity, tonal hierarchy, grain, damage, edges, and era plausibility.
5. Reject neon casts, uniform skin, color bleed, changed objects, cleaned damage, or false claims of historical certainty.
When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output
- Media type: One colorized image
- Default quantity: 1
- Content per image: Source content with plausible color
- Default layout: Source composition
- Model policy: GPT Image 2 Medium
- Downstream use: Family, archive-style, and editorial imagery
