---
name: worktree-cleanup
description: >
  Enforce the correct order when removing a branch that's pinned by a git
  worktree: `git worktree remove --force <path>` THEN `git branch -D <branch>`.
  Trying to delete the branch first fails with `error: cannot delete branch X
  used by worktree at Y`.

  Trigger this skill when:
  - User says "remove branch", "delete branch", "cleanup worktree", "prune
    branches".
  - `gh pr merge --delete-branch` errors with `worktree` in the message.
  - `git branch -D` errors with `used by worktree`.
  - After merging a PR that has an associated worktree.
---

## The rule

**Sequence is ALWAYS:**

```
git worktree remove --force <path>   # step 1
git branch -D <branch>               # step 2
```

If you skip step 1, step 2 fails. `gh pr merge --delete-branch` behaves like
step 2 — it also fails when a worktree pins the branch.

## Behavior

1. **Detect** the branch to clean up (from user's message or the PR).
2. **List worktrees** touching the branch:
   ```
   git worktree list --porcelain | grep -B2 "branch refs/heads/<branch>"
   ```
3. **If a worktree exists** at path `<path>`:
   - Show it to the user.
   - Run `git worktree remove --force <path>` (the `--force` handles dirty state
     in the worktree; warn user if there are uncommitted changes).
   - THEN run `git branch -D <branch>`.
4. **If no worktree exists** for the branch:
   - Just `git branch -D <branch>`.
5. **Report** what was removed.

## Multiple worktrees on one branch

Impossible under git (each worktree pins its own unique branch). If detection
shows multiple, that's a stale entry — clean with `git worktree prune` first,
then retry.

## Batch cleanup

If user asks "cleanup all merged branches with worktrees":

1. `git branch --merged dev` (or `main`) for merged branches.
2. For each: check worktree via `git worktree list --porcelain`.
3. Run sequence per branch.
4. Report tally: N branches removed, M worktrees pruned.

## Do not

- Never `git branch -D` before `worktree remove` — always error, waste of round-trip.
- Never `git worktree remove <path>` without `--force` unless the worktree is
  spotless — the flag is standard in Nimbus flow.
- Never delete a branch with unmerged commits without warning the user + showing
  them the commits that would be lost.
- Never touch `main`, `dev`, `master` — those are protected default branches.

## Cross-repo cleanup

If user asks "cleanup old branches across all my repos", iterate:

```
for r in ~/Development/cidca/cidca-platform ~/Development/cidca/cidca-services \
         ~/Development/horus/horus-v2 ~/Development/zotea; do
  cd "$r" && echo "=== $(basename $r) ===" && git branch --merged | grep -v -E "(main|dev|master|\*)"
done
```

Then present the list and let user choose which to remove.
