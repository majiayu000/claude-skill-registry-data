---
name: plan
description: Spawn the planner subagent against an approved specs/<feature>/spec.md to produce plan.md and tasks.md. Use after a spec has been approved by a human, before any code is written.
user-invocable: true
---

1. Confirm `specs/<feature>/spec.md` exists and has been approved (ask the user if unclear —
   do not assume silence means approval).
2. Spawn the `planner` subagent (fresh context, not fork) with the feature slug. It reads the
   spec and writes `specs/<feature>/plan.md` and `specs/<feature>/tasks.md`.
3. Surface `plan.md` and `tasks.md` to the human, including any open questions `planner`
   raised instead of guessing.
4. Stop (GATE humano). `/implement` should not start in the same turn unless the human
   explicitly approves the plan.
