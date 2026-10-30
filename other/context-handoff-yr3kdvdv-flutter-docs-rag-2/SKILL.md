---
name: context-handoff
description: Write docs/handoffs/latest.md and update docs/PROJECT_STATE.md at the end of a task or before switching agents, following docs/HANDOFF_TEMPLATE.md.
---

# context-handoff

## Steps
1. Collect facts with commands: `git rev-parse HEAD`, `git status --porcelain`, branch, remote URL.
2. Fill every field of `docs/HANDOFF_TEMPLATE.md`. `working_tree_clean: true` only if the
   status output is empty; otherwise list the uncommitted files.
3. `verification`: only commands actually run, with result and exit code.
   `not_verified`: everything else. Access errors in `blockers`.
4. One concrete `next_action`. A short `student_explanation` in Russian.
5. Update `docs/PROJECT_STATE.md` (done / not done / environment / next action).

## Boundaries
No secrets, tokens or full sensitive logs in the handoff.
