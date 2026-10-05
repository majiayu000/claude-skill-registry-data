---
name: web-prototype-taste-editorial
description: |
  Editorial web prototype — magazine-style asymmetric layouts, serif headlines,
  generous whitespace, footnotes, pull quotes. Use for "editorial", "magazine",
  "publication", "journal".
triggers:
  - "editorial"
  - "magazine"
  - "publication"
  - "journal"
  - "long read"
df:
  mode: prototype
  platform: desktop
  scenario: content
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Editorial Web Prototype Skill

Produce a magazine-style editorial web page.

## Rules
- **Serif display** for headlines (large, tight leading).
- **Asymmetric grids**: 60/40 splits, text wrapping around floated elements.
- **Generous whitespace**: paragraphs separated by 2–3em.
- **Pull quotes**: left-floated, accent left border, 1.5× body size.
- **Footnotes**: small mono numbers linking to bottom notes.
- **No hero images**: typographic cover treatment instead.
- `data-df-id` on each paragraph, pull quote, and footnote.

## Output
Single `index.html`, inline CSS.
