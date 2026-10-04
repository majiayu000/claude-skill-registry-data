---
name: go
description: >
  Act on the queued items. Works through every pending item on the working todo
  list (the queue built with /list), actually doing each one, marking it in_progress
  then completed as you go. Use after stacking items with /list.
---

# /go — act on the queue

Take every `pending` item on the working todo list (the queue built with `/list`)
and actually DO it.

- Work through them in order, unless the user's `/go` argument says otherwise
  (e.g. "go — bottom up", or names specific items).
- Mark each item `in_progress` before starting and `completed` when done, via
  TodoWrite, so progress is visible.
- If an item is ambiguous, make a sensible call and note it rather than stalling;
  surface anything that genuinely needs the user's decision.
- If the queue is empty, say so and stop.

When finished, give a brief summary — one line per item — of what was done.
