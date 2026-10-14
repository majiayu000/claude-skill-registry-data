---
name: tdd
description: Run one RED→GREEN cycle (test-author then implementer) for a single named task, outside of a full /implement batch. Use to work one task at a time interactively.
user-invocable: true
argument-hint: <feature-slug> <task-id>
---

Given a feature slug and task id (from `$ARGUMENTS`):

1. Read that one task from `specs/<feature>/tasks.md`.
2. Spawn `test-author` for it (fresh context) — must produce a RED test.
3. Spawn `implementer` for it (fresh context) — iterates until `verify-gate.sh` reports GREEN
   or hands off.
4. Mark the task done in `tasks.md` on success.

This is the same mechanics as one iteration of `/implement`'s loop, scoped to a single task —
use it when you want to work through tasks one at a time with a checkpoint in between, rather
than batching the whole feature.
