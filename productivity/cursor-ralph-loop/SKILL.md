---
name: cursor-ralph-loop
description: Start a Ralph Loop for iterative self-referential development. Use when the user asks to run a ralph loop, start an iterative loop, or wants repeated autonomous iteration on a task until completion.
---

# Ralph Loop with native Codex continuation

Use only when the user explicitly asks for a Ralph loop or repeated autonomous iteration.

## Workflow

1. Record the exact task, project scope, completion promise, and a finite `max_iterations`. An unbounded loop requires a separate explicit user request.
2. Start one bounded native worker and retain its returned child identity. The root coordinator owns iteration state and review.
3. After each completed iteration, verify the result and update a small project-local or task-local state record with child identity, iteration count, maximum, promise, status, and evidence.
4. If the promise is not yet true and the maximum is not reached, continue the same child with the native follow-up surface. Stop when the promise is proved, the maximum is reached, the user cancels, the child needs attention, or verification fails.
5. Report the final stop reason and evidence. Never emit a completion promise that is not true.

This adaptation uses explicit coordinator-driven follow-ups. It does not install or claim an automatic Stop hook. The observed proof resumed the same child twice, preserved its identity, reached iteration 2 of 2 with `PROOF_DONE`, and recorded both state hashes.
