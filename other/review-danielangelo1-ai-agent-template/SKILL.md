---
name: review
description: Spawn reviewer and a11y-auditor in parallel against the current diff, after /implement reports GREEN. Use before /ship, never to replace it.
user-invocable: true
---

1. Spawn `reviewer` and `a11y-auditor` in parallel, both fresh (never `context: fork` for
   `reviewer` — it must not inherit the implementer's reasoning, see SPEC.md §5).
2. Collect findings. Each `reviewer` finding carries a verdict (CONFIRMED / PLAUSIBLE /
   not verified); each `a11y-auditor` finding carries an impact (critical / serious / minor).
3. Present all findings to the human. CONFIRMED findings of high severity, and any
   critical/serious a11y violation, block `/ship` until either fixed (loop back through
   `/implement` for that task) or explicitly waived by the human in `tasks.md`.
4. Do not fix findings yourself in this skill — that is `implementer`'s job on a follow-up
   task, not `reviewer`'s or this skill's.
