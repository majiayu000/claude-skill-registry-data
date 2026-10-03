---
name: workflow-implement
description: Use when the user explicitly asks to implement an approved workflow scope, PRD, or issue.
---

# Workflow Implement

This skill wraps the Matt Pocock `implement` phase.

## Required Flow

1. Read `.agents/skills/implement/SKILL.md`.
2. Confirm the scope has passed grilling and any required PRD/issues phase.
3. Checkpoint the run to `current_skill=implement`.
4. Implement only the approved scope.
5. Run relevant gates.
6. Hand off to `skills/workflow-code-review/SKILL.md`.

Do not implement from a raw first message or from a first grilling answer.
