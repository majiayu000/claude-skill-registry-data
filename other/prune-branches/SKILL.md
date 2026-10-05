---
name: prune-branches
effort: low
allowed-tools: Bash(git branch:*), Bash(git worktree:*), Bash(git rev-parse:*)
description: >
  Cleans up local git branches marked as [gone] (deleted on the remote but still
  present locally), including removing any associated worktrees.
  Use when the user says "prune branches", "clean up gone branches", "/prune-branches",
  or asks to delete stale local branches whose remotes are gone.
---

## Your task

Delete every local branch whose upstream is gone, removing any attached worktree first. If nothing is marked `[gone]`, report that and stop.

## Steps

1. **List branches with verbose status** to surface `[gone]` markers and any `+` prefix indicating an attached worktree:

   ```bash
   git branch -v
   ```

2. **List worktrees** so you know which paths will be removed:

   ```bash
   git worktree list
   ```

3. **Remove worktrees and delete `[gone]` branches** in one pass. Strips the `+`/`*`/space prefix, finds the worktree (if any), and force-deletes the branch:

   ```bash
   git branch -v | grep '\[gone\]' | sed 's/^[+* ]//' | awk '{print $1}' | while read branch; do
     echo "Processing branch: $branch"
     worktree=$(git worktree list | grep "\\[$branch\\]" | awk '{print $1}')
     if [ ! -z "$worktree" ] && [ "$worktree" != "$(git rev-parse --show-toplevel)" ]; then
       echo "  Removing worktree: $worktree"
       git worktree remove --force "$worktree"
     fi
     echo "  Deleting branch: $branch"
     git branch -D "$branch"
   done
   ```

## Reporting

- Print which worktrees were removed and which branches were deleted.
- If no `[gone]` branches exist, say "No cleanup needed" and stop.
- Never delete branches that are not marked `[gone]`.
- Never touch the current working tree's root path.
