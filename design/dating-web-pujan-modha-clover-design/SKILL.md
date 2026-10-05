---
name: dating-web
description: |
  Dating app landing or profile page with card stack, matching UI, and
  messaging preview. Use for "dating app", "matching", "profile", "swipe".
triggers:
  - "dating app"
  - "dating"
  - "matching app"
  - "profile page"
  - "swipe"
df:
  mode: prototype
  platform: mobile
  scenario: social
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Dating Web Skill

Produce a dating app screen or landing page.

## Archetypes
| Brief | Screen |
|---|---|
| landing, homepage | Landing with hero, how-it-works, testimonials |
| profile, card | Profile card stack with like/pass buttons |
| match, success | Match celebration screen |
| messages, chat | Conversation list or chat thread |

## Rules
- Warm, inviting palette. Soft shadows, rounded corners.
- Photos as gradient placeholders with initials overlay.
- Action buttons: large, thumb-friendly (56px+).
- `data-df-id` on cards, buttons, messages.

## Output
Single `index.html`, inline CSS.
