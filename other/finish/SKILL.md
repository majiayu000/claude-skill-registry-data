---
name: finish
description: Use when the MR has been merged by a human, clean up the worktree and update the integration branch. Closes the pipeline loop.
---

# finish

Step 11 of the pipeline (`WORKFLOW.md`). Post-merge: tidying up behind you.

## When
Once the MR has been **merged by a human** (never before).

## Steps
1. **Stop what the worktree was running** (dev server, watchers), so nothing holds files open or keeps a
   port bound.
2. **Remove the worktree**: `git worktree remove <path>`, then prune. Never `rm -rf` on it — that leaves
   git's metadata pointing at a path that no longer exists.
3. **Update the integration branch** locally (fast-forward). The base is **read from the repo**, not
   assumed: `develop` on some, `main` on others.
4. **Delete the merged branch** if the merge didn't (squash-and-delete usually has).
5. **Close the task's trail**: mark it finished wherever it was tracked. If a local orchestrator holds
   that state, this is where it's told; if not, the todo list or the ticket is the trail.

## Output / checkpoint
Worktree gone, base branch up to date, branch deleted, task marked finished. Nothing left running.

## Guardrails
- **Never run any of this before the human merge.**
- **Never delete the worktree by hand with `rm -rf`**; use `git worktree remove` so git's metadata stays
  consistent.
- **Never hard-code the integration base.** Read it; guessing `develop` on a `main` repo silently updates
  the wrong branch.
- Never leave a server or watcher running from a worktree you just removed.

## Origin
Internal, rewritten our way from a local orchestrator's task-teardown step. The mechanism is plain git
here: **no dependency on that tool**, same reason as `start-feature` (rule B).
