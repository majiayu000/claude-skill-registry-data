---
name: tech-sharing
description: |
  Technical presentation / talk slides as HTML. Code snippets, diagrams,
  speaker notes. Use for "tech talk", "tech sharing", "presentation",
  "developer talk".
triggers:
  - "tech talk"
  - "tech sharing"
  - "developer talk"
  - "code presentation"
  - "engineering talk"
df:
  mode: deck
  platform: desktop
  scenario: engineering
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# Tech Sharing Skill

Produce a technical slide deck.

## Slide types
1. **Title**: talk name, speaker, date, company.
2. **Agenda**: 3–4 sections with time estimates.
3. **Concept**: big idea + one-sentence explanation.
4. **Code**: syntax-highlighted block, 10–15 lines max per slide.
5. **Diagram**: inline SVG architecture/flow diagram.
6. **Data**: chart or benchmark table.
7. **Quote**: notable quote, large type, attribution.
8. **Summary**: 3–5 key takeaways.

## Rules
- Dark theme default (easier on projectors).
- Code: mono font, line numbers, subtle highlight on current line.
- Diagrams: inline SVG, consistent color coding.
- `data-df-id` on each slide.

## Output
Single `index.html` with slide system (`.slide` + `is-active`).
