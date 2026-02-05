---
name: working-in-git-worktrees
description: Working in isolated worktree directories for parallel work - work normally, tests isolated, orchestrator handles cleanup
---

# Working in Git Worktrees

## Purpose

Git worktrees create isolated working directories on separate branches. Enables parallel work without conflicts.

**Why you're in a worktree:**
- Parallel work with other agents
- Test/lint isolation
- Independent branch work

## Check if in Worktree

```bash
git rev-parse --git-dir
# .git → main repo
# ../path/.git/worktrees/name → worktree

git branch  # Shows your feature branch
```

## Working Normally

**Everything works normally!**
- Commit, push, pull as usual
- Run tests in isolation
- Create PRs
- All git operations work

**What's different:**
- Separate working directory
- Changes don't affect parallel work
- Tests/lint see only your changes

## Workflow

```bash
# Delegated to worktree
cd ../worktree-42

# Verify
git branch  # feature-branch-42
git status  # Clean

# Work normally
# Edit files
git add .
git commit -m "feat: implement"
just check-all
git push -u origin HEAD

# Create PR
gh pr create --draft
```

## Comparison

| Aspect | Main Repo | Worktree |
|--------|-----------|----------|
| Location | Original path | Separate directory |
| Tests | May conflict | Fully isolated |
| Files | Shared | Independent |
| Git history | Shared | Shared |

## After Complete

**Don't manually delete!**

Orchestrator handles cleanup after merge. Just return to main:

```bash
cd ../main-repo
git checkout main
git pull
```

## Commands

```bash
# Create (usually orchestrator does this)
git worktree add ../worktree-42 -b feature-42

# List
git worktree list

# Remove (orchestrator does this)
git worktree remove ../worktree-42
```

## Troubleshooting

**"Branch already checked out"** - Switch branch in other worktree first
**Changes not showing** - Check `pwd` and `git branch`
**Tests failing** - Verify with `git pull`
