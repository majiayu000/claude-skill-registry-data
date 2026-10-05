---
name: team-okrs
description: |
  OKR (Objectives and Key Results) dashboard with progress bars, owner avatars,
  and quarterly grouping. Use for "OKRs", "goals", "objectives", "Q1 goals".
triggers:
  - "okr"
  - "okrs"
  - "objectives"
  - "key results"
  - "team goals"
  - "quarterly goals"
df:
  mode: prototype
  platform: desktop
  scenario: productivity
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Team OKRs Skill

Produce an OKR tracking page.

## Layout
- **Header**: quarter selector, team name, overall progress ring.
- **Objectives**: one card per objective.
  - Title, owner avatar + name.
  - Progress bar (0–100%).
  - Key Results list: each with mini progress bar, target metric,
    current metric, confidence score (0.0–1.0).
  - Status badge: On track / At risk / Behind.

## Rules
- Progress bars use accent color. Behind status uses subtle red.
- Confidence score as small mono number.
- Cards have subtle left border colored by status.
- `data-df-id` on each objective card and key result.

## Output
Single `index.html`, inline CSS.
