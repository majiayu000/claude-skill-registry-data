---
name: emperor-worktree
description: >-
  Emperor Time worktree isolation. Use before standard or heavy BUILD so the
  client's current checkout stays clean. Detect isolation first, prefer native
  harness tools, verify check-ignore, create a git worktree only as fallback,
  prove a green baseline, then implement the work-order there.
license: MIT
metadata:
  version: 0.4.33
  part-of: emperor-time
---

# Worktree isolation

Standard and heavy tasks do not mutate the client's dirty tree.

## MUST — isolation checklist first

Before creating a worktree or starting standard/heavy BUILD, open
`skills/emperor-worktree/isolation-checklist.md`
(Chain Jail leaf from Superpowers `using-git-worktrees` → detect / create /
setup / baseline only)
and/or run `scripts/emperor iso` (prints the mechanical WORKTREE / STEP / MUST
card).

No `git worktree add` without Step 1 detect. Do not load whole
`using-git-worktrees`; ET + emperor-worktree orchestrate.

## Hard rules

1. Run `scripts/emperor iso` → quote `WORKTREE checklist=yes`. Advance with
   `scripts/emperor iso --advance N N+1` (skips fail). Blind create →
   `scripts/emperor iso --reject-blind-create` (HARD-GATE exit 1).
2. If already in a linked worktree (`git rev-parse --git-dir` !=
   `--git-common-dir`) and **not** a submodule, stay. Do not nest.
3. Prefer a native harness worktree tool when one exists. Else git fallback:
   ```bash
   mkdir -p .worktrees
   git check-ignore -q .worktrees || { echo ".worktrees/" >> .gitignore; }
   scripts/emperor worktree <task-id>  # Python core: scripts/lib/worktree.py
   # or: git worktree add .worktrees/<task-id> -b emperor/<task-id>
   ```
4. Install project deps in the worktree. Run the baseline suite. Quote the tail.
5. Implement only inside that worktree. Ledger the path + isolation mode.
6. Review pack diffs that worktree against the base branch SHA.
7. Merge/copy back only after G4 PASS (finish menu owns cleanup).

Trivial tasks may stay on the current tree. Record `worktree: skipped (trivial)`
and still quote Step 1 detect.
