---
name: take-over
description: Take responsibility for an existing PR, branch, or agent handoff. Use when asked to finish inherited work without discarding its history or credit.
---

# Take Over Existing Work

1. Read the original request, PR/branch/thread, user corrections, review findings, commit history, and current worktree.
2. Verify the current head and target base; do not assume the branch state from an old handoff.
3. Reproduce the known failure or verify the unfinished acceptance criteria before editing.
4. Preserve authorship, commit history, and co-author credit where practical. Use a new branch for replacement work when overwriting would be risky.
5. Keep the original goal; make only changes needed to finish it. Reassess architecture if the base has moved materially.
6. Run targeted and integration checks. Inspect all inherited and new changes; do not assume prior work is correct.
7. Report inherited state, changes made, credit preserved, verification, and remaining decisions.

Do not force-push, close the original PR, discard another agent's work, or rewrite commit history without explicit approval.
