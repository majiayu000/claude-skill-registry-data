---
name: web-prototype-taste-brutalist
description: |
  Brutalist web prototype — raw borders, system fonts, high contrast,
  asymmetric grids, no gradients. Use for "brutalist", "raw", "experimental".
triggers:
  - "brutalist"
  - "brutalism"
  - "raw web"
  - "experimental"
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

# Brutalist Web Prototype Skill

Produce a brutalist web page.

## Rules
- **Borders**: 2–4px solid black. No rounded corners.
- **Typography**: system fonts only (Arial, Times, Courier). No webfonts.
- **Colors**: pure black, pure white, one accent (red or blue).
- **Layout**: asymmetric, overlapping elements allowed.
- **Images**: no external images. CSS patterns or ASCII art placeholders.
- **Animations**: none. Static and immediate.
- `data-df-id` on every block.

## Output
Single `index.html`, inline CSS.
