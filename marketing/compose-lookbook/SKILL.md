---
name: compose-lookbook
description: Arrange several supplied outfit photographs into one intentional lookbook page with an editorial grid, hierarchy, spacing, and optional exact copy. Use after outfit images exist; do not invent outfits or collapse all looks into one person.
---
# Compose Lookbook
## Catalog
- Display name: Compose Lookbook
- Categories: Fashion, Social Media
- Status: Ready
- Route label: GPT Image 2 editorial layout
- Tone: plum
- Short description: Arrange several outfit photos into one editorial page.
- Similar skills: photo-collage, create-social-carousel, create-image-deck
## What this skill does
- Places multiple supplied looks into one ordered editorial page.
- Preserves each outfit and person while controlling crop, whitespace, captions, and reading order.
## How to use
Provide two to five outfit photos, ratio, visual direction, and exact copy.
#### Compose a lookbook
```text
Arrange these four outfit photos as one portrait lookbook page titled CITY LAYERS.
```
## Workflow
1. Inventory each look; lock order, crop-safe regions, exact copy, and ratio.
2. Choose hero-plus-support, equal grid, staggered editorial, or contact-sheet rhythm.
3. Use `gpt-image` v1.0, GPT Image 2 Medium, all references, requested ratio, `batchCount: 1`.
4. Keep garments, faces, colors, and proportions source-faithful; render exact text once.
5. Verify every photo is visible, order and margins are clear, copy is exact, and no extra look appears.
When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output
- Media type: One lookbook page image
- Default quantity: 1
- Content per image: All supplied looks in distinct regions
- Default layout: Editorial multi-photo page
- Model policy: GPT Image 2 Medium
- Downstream use: Fashion decks, social posts, and line sheets
