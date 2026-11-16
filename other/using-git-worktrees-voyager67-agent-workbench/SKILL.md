---
name: using-git-worktrees
description: Use an isolated Git worktree when the current tree is dirty, parallel work is active, or branch isolation reduces risk.
---

# Using Git Worktrees

1. Inspect repository state, branch, untracked files, and local instructions. Never assume the current tree is disposable.
2. Choose the intended base and a descriptive branch/worktree path outside tracked project directories where practical.
3. Create the worktree and run the repository's documented setup and baseline checks.
4. Keep worktree ownership clear. Do not have two agents edit the same files or operate on the same branch concurrently.
5. Do not copy secrets, local environment files, credentials, or generated state into the worktree.
6. Before handoff, inspect status and diff, run relevant checks, and document the branch and worktree path.
7. Remove a worktree only when the user requested cleanup or it was created for this task and removal is clearly safe.

If the tool or environment does not support worktrees, continue in the current tree with stricter change isolation and say so. Never delete untracked user data.
