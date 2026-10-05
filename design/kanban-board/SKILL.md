---
name: kanban-board
description: |
  Kanban board UI with columns, cards, tags, and avatars. Use for
  "kanban", "task board", "project board", "trello-style".
triggers:
  - "kanban"
  - "task board"
  - "project board"
  - "trello"
  - "board"
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

# Kanban Board Skill

Produce a kanban board interface.

## Layout
- **Top bar**: project name, search, filter dropdowns, "New task" button.
- **Board**: horizontal scroll of 3–5 columns.
  - Each column: header with count badge, color-coded tag.
  - Cards: title, description (2 lines), 1–2 tags, 1–2 avatars (colored circles
    with initials), due date.
  - Cards stacked vertically with 12px gap.

## Rules
- Column min-width 280px. Board scrolls horizontally on overflow.
- Cards have subtle shadow + hover lift.
- Tags: small pills with background tints.
- Avatars: 28px circles, 2px white border, slight overlap (-8px margin).
- `data-df-id` on each column and card.

## Output
Single `index.html`, inline CSS.
