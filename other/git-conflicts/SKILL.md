---
name: git-conflicts
description: "Resolve merge/rebase/cherry-pick conflicts: understand both sides, resolve minimally, verify with tests. No blind ours/theirs."
---

# git-conflicts

Conflicts are review decisions, not typing exercises: understand intent on both sides first.
## Inspection

Read both sides' intent (log --merge) and the conflicted hunks before touching anything; note which side the PR's purpose favors.

## Decision rules

Resolve per hunk with intent preserved; never blanket ours/theirs on unread code; abort and split when the surface exceeds understanding.


## Activate when

- Merge, rebase, or cherry-pick stops with conflicts.

## Do NOT activate for

- Clean merges/rebases (git-workflow, git-rebase) or lost work (git-recovery).

## Procedure

1. Orient: `git status` for conflicted paths; `git log --merge --oneline` for both sides' intent.
2. Resolve per hunk: keep the intent of both where compatible; where incompatible, choose the side matching the PR's purpose and note why. Never blanket `ours`/`theirs` on code you haven't read.
3. Mark resolved (`git add`), continue (`--continue`), and re-run the affected tests before pushing.
4. Abort criteria: if the conflict surface exceeds understanding, `git merge --abort` / `git rebase --abort` and split the change smaller.
5. Verify: full diff re-read, tests green, no conflict markers (`grep -r '<<<<<<<'`).

## Failure modes

Auto-resolving with ours/theirs; resolving without running tests; leaving markers in; pushing conflicted merges to shared branches.

## Escalation

Lost work during resolution → git/git-recovery.
