---
name: implement
description: Run the RED→GREEN loop (test-author then implementer) over every not-yet-done task in specs/<feature>/tasks.md, one task at a time, gated by verify-gate.sh's ratchet. Use after a plan has been approved.
user-invocable: true
---

1. Write the feature slug to `.claude/state/active-feature` (plain text, no newline) —
   `verify-gate.sh` reads this to know where to write `HANDOFF_NEEDED.md` if the ratchet
   exhausts its attempts (SPEC.md §5).
2. For each task in `specs/<feature>/tasks.md` not yet marked done, in order:
   a. Spawn `test-author` for that task (fresh context). It must produce a RED test.
   b. Spawn `implementer` for that task (fresh context). It iterates against
   `scripts/verify.sh`; the `Stop`/`SubagentStop` hook enforces the ratchet automatically —
   you do not manage retries yourself.
   c. If the hook writes a `HANDOFF_NEEDED.md`, stop the loop immediately and surface it to
   the human. Do not skip to the next task.
   d. On success, mark the task done in `tasks.md`.
3. When every task is done, report a summary and suggest `/review`. Do not call `/review`
   automatically — that is a separate step with its own gate.

Never mark a task done without `scripts/verify.sh` having actually reported 0 for it — the
hook is the source of truth, not your own judgment of "this looks right."
