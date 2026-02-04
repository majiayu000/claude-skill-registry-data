---
name: lotar-task-tracking
description: Use this to create and maintain LoTaR tasks for work tracking, with minimal friction and consistent updates.
---

## Quick start

- List tasks:
  - `lotar list`

- Create a task:
  - `lotar add "<title>" --priority=HIGH --type=feature`

- Update status:
  - `lotar status <ID> in_progress`

- Add a short progress note:
  - `lotar comment <ID> -m "what changed + where"`

## ID + project notes

- IDs look like `PROJ-123`. If you’re in a single-project repo (or have `default_project` set), many commands accept numeric-only IDs.
- When ambiguous, always use the fully-qualified ID or pass `--project`.

## Good “agent” update pattern

- Keep comments short and actionable:
  - What changed (1 sentence)
  - Where (paths/symbols)
  - Next step (1 line)

## Safety

- Don’t paste secrets/PII into task comments (tokens, auth headers, cookies).
