---
name: session-start
description: >
  At session start, read the session baton (docs/session/baton.md) and orient:
  restate this session's goal and the single next task, then open any doc listed
  under "Read first" before starting work. Does not start the task automatically.
disable-model-invocation: true
---

# Session Start

Orient from the baton the previous session left.

## Steps

1. Read `docs/session/baton.md`. If it is missing, say so and offer to start fresh
   (a `session-end` run creates it).
2. If **Read first** names a doc (not `None`), read that doc before anything else.
3. Restate to the user, in 2–3 lines: the **Goal** and the **Next task**.
4. Stop and confirm the next task with the user before acting — never auto-start it.
