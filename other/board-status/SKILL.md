---
name: board-status
description: Show read-only status for an AgentBoard workspace board. Use when the user wants card counts, bottlenecks, blocking settings, or work-in-progress visibility.
---

# Board Status

Use this skill for workspace-board visibility.

## Workflow

1. Load the `agentboard` skill first.
2. Select the app and board.
3. Fetch the board settings and card list.
4. Present:
   - counts by column
   - completion percentage
   - blocking toggles
   - cards needing attention

## Rules

- Do not move cards.
- If no app or board exists, tell the user to start with `foundation` or `sweep`.
