---
name: critique
description: |
  Run a 5-dimension expert design review on any HTML artifact.
  Scores: Philosophy, Visual hierarchy, Detail, Functionality, Innovation (0–10).
  Outputs a self-contained HTML report with radar chart and action lists.
triggers:
  - "critique"
  - "design review"
  - "design audit"
  - "audit my design"
  - "review my landing"
  - "review my deck"
df:
  mode: prototype
  platform: desktop
  scenario: design
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# Critique Skill · 5-Dimension Review

## Dimensions
1. **Philosophy consistency** — Does the artifact pick a direction and stick to it?
2. **Visual hierarchy** — Can a stranger read it first/second/third without help?
3. **Detail execution** — Alignment, leading, kerning, image framing, edge cases.
4. **Functionality** — Does it work for its intended use? Click targets, nav, mobile.
5. **Innovation** — Does it push past the median? One element that makes people lean in?

## Scoring discipline
- Always cite evidence with class names / line numbers.
- Don't average up — score is the worst sustained band.
- 7 = strong, not acceptable.

## Output
Single HTML report with:
- Header (artifact name, date, verdict).
- Inline SVG radar chart.
- 5 dimension cards (score + evidence paragraph).
- **Keep / Fix / Quick-wins** action lists.

## Rules
- 5 scores every time.
- Evidence per score — no "feels off".
- Single-file HTML only.
- Radar chart is mandatory.
