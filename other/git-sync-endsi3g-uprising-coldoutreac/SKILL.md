---
name: Git Sync
description: Synchronize with remote repository before starting tasks
---

# Git Sync Skill

## Purpose

Ensure the local repository is synchronized with the remote before starting any development work. This prevents merge conflicts and ensures you're working with the latest code.

## When to Use

- At the **start of any new task** or user request
- Before making significant code changes
- When resuming work after a break

## Pre-Task Checklist

Before beginning any coding task, run these commands in order:

```bash
# 1. Check current branch and status
git status

# 2. Stash any uncommitted changes (if any)
git stash --include-untracked

# 3. Pull latest changes from remote
git pull --rebase origin main

# 4. Restore stashed changes (if any were stashed)
git stash pop
```

## Quick Sync Command

For a fast sync when you have no local changes:

```bash
git pull --rebase origin main
```

## After Task Completion

When finishing a task, commit and push changes:

```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: description of changes"

# Push to remote
git push origin main
```

## Commit Message Convention

Use conventional commits format:

| Prefix | Usage |
|--------|-------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code refactoring |
| `style:` | Formatting, no logic change |
| `test:` | Adding tests |
| `chore:` | Maintenance tasks |

## Handling Conflicts

If `git pull --rebase` results in conflicts:

1. Resolve conflicts in affected files
2. Stage resolved files: `git add <file>`
3. Continue rebase: `git rebase --continue`
4. If needed, abort: `git rebase --abort`
