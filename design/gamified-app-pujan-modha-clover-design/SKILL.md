---
name: gamified-app
description: |
  Gamified interface with points, badges, progress bars, leaderboards, and
  achievement cards. Use for "gamification", "rewards", "points", "badges".
triggers:
  - "gamification"
  - "gamified"
  - "rewards"
  - "points"
  - "badges"
  - "leaderboard"
df:
  mode: prototype
  platform: desktop
  scenario: engagement
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Gamified App Skill

Produce a gamified dashboard or profile page.

## Elements
- **Level badge**: large circle with level number, XP bar underneath.
- **Stats row**: streak, total points, quests completed.
- **Achievement grid**: 3×4 cards with icon, title, progress ring, locked state.
- **Leaderboard**: ranked list with avatar, name, score, trend arrow.
- **Quests**: checklist with XP rewards, progress bars.

## Rules
- Celebrate with accent color (gold/yellow) sparingly.
- Locked achievements: grayscale + lock icon.
- Progress rings: inline SVG `stroke-dasharray`.
- `data-df-id` on each achievement and quest.

## Output
Single `index.html`, inline CSS.
