---
name: tasks
description: Re-list, reorder, or lightly edit an existing specs/<feature>/tasks.md without re-running the planner. Use for small manual adjustments to an already-approved task breakdown.
user-invocable: true
---

Read `specs/<feature>/tasks.md`, apply only the requested edit (reorder, split, tweak an
EARS line, adjust `critical: true`), and show the diff. Do not regenerate the whole file from
scratch — that is what `/plan` is for, and re-running `planner` would discard human edits
already made to `tasks.md`.

If the requested change is large enough to need re-planning (new acceptance criteria, a
different technical approach), say so and suggest `/plan` again instead.
