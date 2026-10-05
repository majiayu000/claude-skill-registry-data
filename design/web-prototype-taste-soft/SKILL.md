---
name: web-prototype-taste-soft
description: |
  Soft / pastel web prototype — rounded everything, gentle gradients, friendly
  typography, bouncy animations. Use for "soft", "pastel", "friendly", "cute".
triggers:
  - "soft"
  - "pastel"
  - "friendly"
  - "cute"
  - "gentle"
  - "warm"
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

# Soft Web Prototype Skill

Produce a soft, friendly web page.

## Rules
- **Border radius**: 16–32px on everything (cards, buttons, images).
- **Colors**: pastels, low saturation. No pure black — dark grays only.
- **Shadows**: large, soft, diffuse (`0 20px 60px rgba(0,0,0,0.08)`).
- **Typography**: rounded sans-serif feel. Generous line-height.
- **Animations**: gentle bounces, soft fades (`cubic-bezier(0.34, 1.56, 0.64, 1)`).
- **Icons**: rounded, filled, minimal.
- `data-df-id` on each card and button.

## Output
Single `index.html`, inline CSS.
