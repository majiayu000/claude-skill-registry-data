---
name: email-marketing
description: |
  Brand product-launch email — masthead, hero, headline lockup, body, CTA,
  specs grid. Pure HTML email layout (centered single column).
triggers:
  - "email"
  - "email template"
  - "newsletter"
  - "email blast"
  - "product launch email"
  - "mjml"
df:
  mode: prototype
  platform: desktop
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Email Marketing Skill

Produce a single HTML email — centered, single column, one big idea, one CTA.

## Layout (600–680px column, centered)
1. **Masthead** — wordmark left, 3 nav links right, thin underline.
2. **Hero block** — 16:9 product placeholder (gradient or SVG silhouette).
3. **Eyebrow** — small caps accent, separated by · (e.g. "NEW · PRODUCT · COLOR").
4. **Headline lockup** — 2–3 lines, display font, all caps, tight tracking.
   Slight skew (`transform: skew(-6deg)`) on one accent word.
5. **Body** — 2–3 sentences, left-aligned.
6. **Primary CTA** — one solid pill or block button.
7. **Specs grid** — 2×2 (big number + unit + label).
8. **Footer** — wordmark, address, unsubscribe.

## Rules
- Reads top to bottom in 8–10 seconds.
- One CTA. Accent ≤2×.
- Legible at 480px (column reflows, type drops one step).
- No external images — inline SVG or gradient blocks.
- `data-df-id` on masthead, hero, headline, CTA, specs.

## Output
Single `index.html`, inline CSS.
