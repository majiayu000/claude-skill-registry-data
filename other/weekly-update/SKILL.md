---
name: weekly-update
description: |
  Team weekly update with wins, blockers, upcoming work, and metrics.
  Use for "weekly update", "week in review", "team update", "status report".
triggers:
  - "weekly update"
  - "week in review"
  - "team update"
  - "status report"
  - "weekly report"
df:
  mode: document
  platform: desktop
  scenario: productivity
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# Weekly Update Skill

Produce a team weekly update document.

## Sections
1. **Header**: week range, team name, author.
2. **Summary**: 2–3 sentence narrative.
3. **Wins**: 3–5 bullets with 🎯 emoji or accent dot.
4. **Blockers**: 1–3 items with owner and ETA.
5. **This week**: planned work as a compact list.
6. **Metrics**: 2–4 mini sparkline charts (inline SVG) showing trends.
7. **Shoutouts**: 1–2 teammate recognitions.

## Rules
- Friendly but professional tone.
- Metrics sparklines: 20px tall, no axes, just the line.
- `data-df-id` on each section.

## Output
Single `index.html`, inline CSS.
