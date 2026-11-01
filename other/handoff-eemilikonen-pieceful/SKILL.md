---
name: handoff
description: Wrap up a Pieceful session by updating the private progress log, task statuses, and open questions so the next session can continue. Use for /handoff or at the end of a session with changes.
---

# /handoff: end of session

1. In the private `planning/progress.md` (notes path in `CLAUDE.local.md`):
   - Rewrite **Current state**: phase, **Next up** (numbered, concrete), blockers. Keep it short; the SessionStart hook prints it.
   - Add a dated **Log** entry at the top: what was done, decisions made (with links), anything left uncommitted.
2. Make sure the task statuses in `docs/tasks/` match reality.
3. Add any unanswered questions to `planning/open-questions.md`.
4. Tell the owner what's uncommitted (in both repos) and still needs their review. Don't commit.
