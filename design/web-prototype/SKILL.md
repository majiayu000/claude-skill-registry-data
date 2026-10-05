---
name: web-prototype
description: |
  General-purpose desktop web prototype. Single self-contained HTML file
  with semantic markup, inline CSS, and responsive breakpoints. Default
  for landing, marketing, docs, or SaaS pages.
triggers:
  - "prototype"
  - "mockup"
  - "landing"
  - "single page"
  - "marketing page"
  - "homepage"
  - "web page"
  - "site"
df:
  mode: prototype
  platform: desktop
  scenario: design
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
---

# Web Prototype Skill

Produce a single self-contained HTML prototype using the active design system.

## Workflow

1. **Read DESIGN.md**. Map colors to `--df-color-*` and fonts to `--df-font-family`.
2. **Plan sections** before writing. State the list in one sentence.
3. **Default rhythms**:
   | Page kind | Rhythm |
   |---|---|
   | Landing | Hero → Features → Stats/Quote → Split → CTA → Footer |
   | Marketing | Hero → Logos → CTA → Footer |
   | Pricing | Hero → Comparison → CTA → Footer |
4. **Write** `index.html` with inline CSS, semantic HTML, `data-df-id` tags.
5. **Self-check**: meaningful text, valid colors, responsive at 920px/640px,
accent ≤2× per screen.

## Hard rules
- Single accent, max twice per screen.
- No external JS.
- No pure black (#000000).
- Placeholder images as CSS gradients/SVG only.

## Output
```
<artifact identifier="slug" type="text/html" title="Title">
<!doctype html><html>...</html>
</artifact>
```
