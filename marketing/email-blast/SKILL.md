---
name: email-blast
description: |
  Promotional email blast with hero image, headline, body, CTA button,
  and unsubscribe footer. Use for "promo email", "blast", "campaign email".
triggers:
  - "promo email"
  - "email blast"
  - "campaign email"
  - "promotional email"
  - "newsletter blast"
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

# Email Blast Skill

Produce a promotional email blast.

## Layout (600px centered column)
1. **Preheader**: hidden preview text.
2. **Header**: logo left, "View in browser" right.
3. **Hero image**: full-width gradient placeholder.
4. **Headline**: display font, 1–2 lines.
5. **Body**: 2–4 sentences, left-aligned.
6. **CTA**: single prominent button.
7. **Secondary content**: 2–3 small cards (image + title + link).
8. **Footer**: social icons (text placeholders), address, unsubscribe.

## Rules
- Table-based layout for email client compatibility.
- Inline CSS only.
- CTA button: 44px min height, high contrast.
- Alt text on all images (even placeholders).
- `data-df-id` on hero, headline, CTA.

## Output
Single `index.html`, inline CSS (table layout).
