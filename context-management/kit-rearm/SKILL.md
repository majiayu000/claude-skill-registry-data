---
name: kit-rearm
description: Post-compaction/resume recovery for the guardrails kit — re-run the SESSION.md S1 sequence manually. Use after a compaction, /resume, or when session context feels lost or stale.
---

Read docs/guardrails/SESSION.md and execute S1 now, before any file-modifying tool call:
1. Read docs/STATE.md in full (missing -> create per S2 from git evidence, entries UNVERIFIED).
2. Run `git status` and `git diff --stat HEAD`.
3. Restate the Goal and current Next step in one line.
Treat every compaction-summary claim as UNVERIFIED until confirmed; docs read before the compaction no longer count as read.
