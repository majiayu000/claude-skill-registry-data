---
name: create-social-carousel
description: Plan and create one ordered, visually consistent multi-page social carousel with mobile-readable copy, a reusable visual master, and page-by-page acceptance. Use for Xiaohongshu, Instagram, LinkedIn, or similar swipeable educational and promotional posts; do not use for one poster, one thumbnail, unordered photo collages, product-detail pages, or automatic publishing.
---
# Create Social Carousel

## Catalog

- Display name: Create Social Carousel
- Categories: Social Media, Layout & Design
- Status: Ready
- Route label: GPT Image 2 ordered carousel
- Tone: amber
- Short description: Create a coherent mobile-first social carousel as separately generated ordered pages.
- Similar skills: compose-lookbook, photo-collage, create-image-deck
## What this skill does

- Turns one message into a cover, ordered content beats, and a closing CTA without repeating the same claim.
- Locks a visual master before generating separately numbered pages with shared layout, palette, typography intent, and subject anchors.
- Inspects both each page and the complete swipe sequence for exact count, legibility, continuity, and narrative progression.

## How to use

Provide platform, topic, audience, goal, language, page count, exact required copy, brand assets, and desired style. If the platform is named, verify its current official size and safe-area guidance before generation.

#### Example

```text
Create a seven-page Xiaohongshu carousel for first-time renters about avoiding deposit disputes. Use concise Chinese copy, warm editorial illustrations, and end with a save-and-share CTA.
```

## Workflow

1. Freeze the platform, placement, audience, single promise, page count, language, required claims, CTA, and supplied asset roles. Default to 6–8 pages and Xiaohongshu 3:4 only when that placement is explicit; otherwise ask or use the platform's current official guidance.
2. Write a numbered page manifest before generation: cover hook; one distinct idea per middle page; proof, recap, or transition where useful; and one final CTA. Keep visible copy short enough for a phone preview and mark every line that must be exact.
3. Define one visual master: grid, margins, safe zones, type hierarchy, palette, recurring shapes, illustration/photo treatment, and fixed brand or character anchors. Generate one representative page first when the user has not already approved a reference direction.
4. After visual-master approval, use `gpt-image` v1.0 / GPT Image 2 with `quality: "medium"`, `imageSize: "2K"`, the platform ratio, and `batchCount: 1`. Generate one page per run with the visual master and only that page's frozen content. Never request several carousel pages inside one image.
5. Persist a stable `operationKey` containing project and page number before every submission, require a non-empty `executionId`, and poll each accepted run to terminal state. Pages with no dependency may run in parallel only when each operation is independently recorded.
6. Inspect native size and a small phone preview. Check page number/order, exact requested copy, mobile legibility, safe zones, crop, subject/brand preservation, shared visual system, and a non-repetitive swipe narrative.
7. Preserve all terminal results. Retry only a failed or rejected page using a new linked operation key and a prompt changed for its observed defect. If generated lettering remains wrong, repair that page through a suitable deterministic text/layout step or report the limitation; do not regenerate accepted pages.


## User-facing output

- Media type: Ordered social carousel page images plus page manifest and operation receipt
- Default quantity: 6–8 pages; exact requested count wins
- Content per image: One numbered page with one primary communication job
- Default layout: Current platform ratio and safe zones; 3:4 for explicit Xiaohongshu placement
- Model policy: GPT Image 2 Medium/2K, one page per operation
- Downstream use: Human review and manual platform publishing
