---
name: design-brief
description: |
  Structured design brief document — problem statement, goals, audience,
  competitive landscape, mood board, and success metrics.
triggers:
  - "design brief"
  - "creative brief"
  - "project brief"
  - "design proposal"
  - "mood board"
df:
  mode: document
  platform: desktop
  scenario: strategy
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# Design Brief Skill

Produce a single-page design brief document.

## Sections
1. **Project title + meta** — client, date, version, author.
2. **Problem statement** — 2–4 sentences on what needs solving.
3. **Goals** — 3–5 bullet objectives, prioritized.
4. **Audience** — primary and secondary personas with 1-sentence descriptions.
5. **Competitive landscape** — 3–4 competitors in a grid (name, url,
   one strength, one weakness).
6. **Mood direction** — 3–4 adjectives + a 2-sentence rationale.
7. **Success metrics** — 2–4 measurable KPIs.
8. **Timeline** — simple 3–4 phase bar.

## Rules
- Clean, editorial typography. No decorative noise.
- Color used sparingly — accent only for section headers and timeline.
- `data-df-id` on each section.

## Output
Single `index.html`, inline CSS.
