---
name: magazine-poster
description: |
  Editorial magazine cover or poster with bold typography, asymmetric layout,
  and dramatic negative space. Use for "magazine cover", "poster", "editorial".
triggers:
  - "magazine cover"
  - "poster"
  - "editorial poster"
  - "cover design"
  - "flyer"
df:
  mode: prototype
  platform: desktop
  scenario: design
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Magazine Poster Skill

Produce a magazine cover or editorial poster.

## Composition
- **Asymmetric grid** — 60/40 or 70/30 split. No centering.
- **Masthead** — publication name at top, display font, oversized tracking.
- **Cover line** — 1‒3 lines of massive display type, breaking across the fold.
- **Sub-lines** — 2–4 smaller headlines scattered asymmetrically.
- **Issue meta** — date, volume, price in mono, tucked into a corner.
- **Visual element** — CSS gradient block or geometric SVG shape (no external images).

## Rules
- Display font for everything large; mono for meta only.
- Negative space is intentional — don't fill corners.
- Accent color appears once (cover line highlight or masthead underline).
- `data-df-id` on masthead, cover line, sub-lines.

## Output
Single `index.html`, inline CSS. Aspect-ratio 3:4 or 2:3 via wrapper.
