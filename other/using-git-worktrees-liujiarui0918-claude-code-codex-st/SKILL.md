---
name: using-git-worktrees
description: Use when starting a feature. Isolate work in a worktree to keep main clean.
---

# Using Git Worktrees

A worktree is a separate working directory tied to the same repo. It lets you have multiple branches checked out simultaneously, each in its own folder. Your main checkout stays clean. Always.

## Iron Law

**Never `git checkout -b feature/x` in your main working directory.** Spawn a worktree. Main stays on `main`, no exceptions.

## Why worktrees beat branch-switching

| Pain with `checkout` | How worktrees solve it |
|---|---|
| Stash dance when interrupted | Other worktree exists; just `cd` to it |
| Half-applied changes leak between features | Filesystem isolation, impossible to mix |
| `node_modules` / build artifacts thrash | Each worktree has its own build state |
| Hard to compare current vs. proposed | Open both in two editors side-by-side |
| Discarding a branch is scary | Just `rm` the worktree dir, branch optional |

## Red Flags

- Working on a new feature in the same directory you used yesterday.
- A `git stash list` longer than two entries.
- "Let me switch branches" mid-task — that's the moment to spin a worktree instead.
- Uncommitted changes hanging around because switching loses them.

## Standard Flow

### 1. Start

```powershell
# from repo root
git fetch origin
git worktree add ../repo-feature-x -b feature/x origin/main
cd ../repo-feature-x
```

Now you're on a fresh `feature/x` branch in an isolated directory, branched from latest `origin/main`.

If your harness has an `EnterWorktree` tool, use it — it manages the lifecycle for you.

### 2. Work

Develop normally. Commit on `feature/x`. Run tests in this directory.

Main directory remains on `main`, untouched. You can `cd` back at any time to check something on `main` without losing state.

### 3. Finish

Hand off to [[finishing-a-development-branch]] when tests pass and verification is done.

### 4. Clean up

After the branch is merged / abandoned:

```powershell
git worktree remove ../repo-feature-x
git branch -d feature/x   # if merged, otherwise -D to force
git worktree prune
```

## Parallel features

Worktrees shine when you have:
- Long-running feature A and a quick hotfix B
- A WIP exploration alongside a clean baseline for comparison
- Reviewing PR C while feature A continues

Spin one per workstream. Cost is disk space + initial setup. Benefit is zero context-switch cost.

## What lives where

- Repo metadata (`.git`): in the main checkout (worktrees point to it via `.git` file).
- Per-worktree state (HEAD, index): inside the worktree folder.
- `node_modules`, `target`, `__pycache__`: per-worktree, won't conflict.
- `.env`, local config: per-worktree — copy or symlink from main if needed.

## MUST

- MUST branch from a fresh `origin/main` (or your repo's base), not stale local main.
- MUST NOT delete a worktree directory with `rm -rf` directly — use `git worktree remove` so git's tracking stays clean.
- MUST `git worktree prune` periodically to clean orphaned entries.

## Cross-references

- [[finishing-a-development-branch]] — what to do when the feature is ready.
- [[verification-before-completion]] — gate before declaring the worktree finished.
