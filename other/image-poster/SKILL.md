---
name: image-poster
description: |
  Event or campaign poster with dominant imagery, bold typography, and
  clear call-to-action. Use for "poster", "event poster", "campaign".
triggers:
  - "event poster"
  - "campaign poster"
  - "concert poster"
  - "conference poster"
  - "promo poster"
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

# Image Poster Skill

Produce an event or campaign poster.

## Composition
- **Dominant visual**: CSS gradient or geometric SVG (60–70% of area).
- **Event title**: massive display type, breaking across lines.
- **Details block**: date, time, venue, price — mono, tucked neatly.
- **CTA**: "Get tickets" or "RSVP" — prominent but not competing with title.
- **Sponsors / partners**: small logos row at bottom (text placeholders).

## Rules
- Title is the hero. Everything else supports it.
- Accent used once (title highlight or CTA).
- Aspect ratio 2:3 or 3:4 via wrapper.
- `data-df-id` on title, visual, details, CTA.

## Output
Single `index.html`, inline CSS.
