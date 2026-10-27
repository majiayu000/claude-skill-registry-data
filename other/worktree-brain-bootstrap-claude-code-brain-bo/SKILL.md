---
name: worktree
description: Manage git worktrees for parallel work on multiple branches simultaneously. Use when you need to work on two features at once without stashing or branch-switching.
---

# Worktree Skill

Manage git worktrees for parallel, isolated work.

## When to use
- Need to review a PR while working on a feature
- Running a long test suite on one branch while developing on another
- Comparing behavior between two branches side-by-side
- Agent team work where each agent operates on a separate branch

## Create a worktree
```bash
# Create a worktree for an existing branch
git worktree add ../project-feature feature/my-feature

# Create a worktree for a new branch
git worktree add -b feature/new-thing ../project-new-thing main
```

## List active worktrees
```bash
git worktree list
```

## Remove a worktree (when done)
```bash
# 1. Confirm the work is committed or merged
# 2. Remove the worktree
git worktree remove ../project-feature

# Force remove if needed (work is intentionally discarded)
git worktree remove --force ../project-feature
```

## Prune stale worktree references
```bash
git worktree prune
```

## Rules
- NEVER remove a worktree without confirming all work is committed
- Each worktree has its own working directory — changes don't bleed between them
- Worktrees share the same git history — commits on one branch are visible from all
- Name worktrees consistently: `../project-<branch-slug>`

## For agent team workflows
When spawning multiple subagents for parallel work:
1. Create one worktree per agent before spawning
2. Give each agent its worktree path as its working directory
3. After all agents finish, review each worktree's changes
4. Merge or cherry-pick as needed
5. Clean up all worktrees after merge
