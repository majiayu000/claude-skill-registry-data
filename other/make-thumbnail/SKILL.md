---
name: make-thumbnail
description: Research current requirements of a named platform and placement, then create one legible, safe-area-aware cover or video thumbnail. Use for YouTube, marketplace, course, podcast, or social cover imagery where dimensions, file rules, and UI occlusion may change; do not use for banners, posters, video title sequences, or generic image resizing.
---
# Make Thumbnail
## Catalog
- Display name: Make Thumbnail
- Categories: Social Media, Layout & Design
- Status: Ready
- Route label: Platform research plus GPT Image 2
- Tone: amber
- Short description: Create a platform-aware cover or thumbnail.
- Similar skills: ai-banner-design, poster-design, product-detail-page
## What this skill does
- Checks current official size, ratio, file, and safe-area rules before design.
- Creates one focal image with mobile-readable copy and protected UI zones.
## How to use
Provide platform, placement, market, topic, exact copy, assets, and tone.
#### Make a video thumbnail
```text
Check current YouTube requirements and create one thumbnail titled 7 DESK FIXES.
```
## Workflow
1. Research official current documentation; record date, dimensions, ratio, file limits, and occluded zones.
2. Freeze exact copy; choose one focal subject, one promise, and one contrast system.
3. Use `gpt-image` v1.0, GPT Image 2 Medium, supplied assets, platform ratio, `batchCount: 1`.
4. Keep text and faces out of unsafe zones; avoid misleading imagery and unprovided logos.
5. Inspect at native size and small mobile preview for exact copy, crop resilience, contrast, and compliance.
When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output
- Media type: One platform thumbnail image
- Default quantity: 1
- Content per image: One focal subject and concise message
- Default layout: Current platform ratio and safe zones
- Model policy: GPT Image 2 Medium
- Downstream use: Video, podcast, and platform covers
