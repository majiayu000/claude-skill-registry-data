---
name: worktrees
description: Use when working on multiple branches simultaneously, context switching without stashing, reviewing PRs while developing, testing in isolation, or comparing implementations across branches - provides git worktree commands and workflow patterns for parallel development with multiple working directories.
---

# Git Worktrees

## Overview

Git worktrees enable checking out multiple branches simultaneously in separate directories, all sharing the same repository. Create a worktree instead of stashing changes or cloning separately.

**Core principle:** One worktree per active branch. Switch contexts by changing directories, not branches.

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Main worktree** | Original working directory from `git clone` or `git init` |
| **Linked worktree** | Additional directories created with `git worktree add` |
| **Shared `.git`** | All worktrees share same Git object database (no duplication) |
| **Branch lock** | Each branch can only be checked out in ONE worktree at a time |
| **Worktree metadata** | Administrative files in `.git/worktrees/` tracking linked worktrees |

## Essential Commands

### Create a Worktree

```bash
# Create worktree with existing branch
git worktree add ../feature-x feature-x

# Create worktree with new branch from current HEAD
git worktree add -b new-feature ../new-feature

# Create worktree with new branch from specific commit
git worktree add -b hotfix-123 ../hotfix origin/main

# Create worktree tracking remote branch
git worktree add --track -b feature ../feature origin/feature

# Create worktree with detached HEAD (for experiments)
git worktree add --detach ../experiment HEAD~5
```

### List Worktrees

```bash
# Simple list
git worktree list

# Verbose output with additional details
git worktree list -v

# Machine-readable format (for scripting)
git worktree list --porcelain
```

**Example output:**

```
/home/user/project           abc1234 [main]
/home/user/project-feature   def5678 [feature-x]
/home/user/project-hotfix    ghi9012 [hotfix-123]
```

### Remove a Worktree

```bash
# Remove worktree (working directory must be clean)
git worktree remove ../feature-x

# Force remove (discards uncommitted changes)
git worktree remove --force ../feature-x
```

### Move a Worktree

```bash
# Relocate worktree to new path
git worktree move ../old-path ../new-path
```

### Lock/Unlock Worktrees

```bash
# Lock worktree (prevents pruning if on removable storage)
git worktree lock ../feature-x
git worktree lock --reason "On USB drive" ../feature-x

# Unlock worktree
git worktree unlock ../feature-x
```

### Prune Stale Worktrees

```bash
# Remove stale worktree metadata (after manual directory deletion)
git worktree prune

# Dry-run to see what would be pruned
git worktree prune --dry-run

# Verbose output
git worktree prune -v
```

### Repair Worktrees

```bash
# Repair worktree links after moving directories manually
git worktree repair

# Repair specific worktree
git worktree repair ../feature-x
```

## Workflow Patterns

### Pattern 1: Feature + Hotfix in Parallel

To fix a bug while feature work is in progress:

```bash
# Create worktree for hotfix from main
git worktree add -b hotfix-456 ../project-hotfix origin/main

# Switch to hotfix directory, fix, commit, push
cd ../project-hotfix
git add . && git commit -m "fix: resolve critical bug #456"
git push origin hotfix-456

# Return to feature work
cd ../project

# Clean up when done
git worktree remove ../project-hotfix
```

### Pattern 2: PR Review While Working

To review a PR without affecting current work:

```bash
# Fetch PR branch and create worktree
git fetch origin pull/123/head:pr-123
git worktree add ../project-review pr-123

# Review: run tests, inspect code
cd ../project-review

# Return to work, then clean up
cd ../project
git worktree remove ../project-review
git branch -d pr-123
```

### Pattern 3: Compare Implementations

To compare code across branches side-by-side:

```bash
# Create worktrees for different versions
git worktree add ../project-v1 v1.0.0
git worktree add ../project-v2 v2.0.0

# Diff, compare, or run both simultaneously
diff ../project-v1/src/module.js ../project-v2/src/module.js

# Clean up
git worktree remove ../project-v1
git worktree remove ../project-v2
```

### Pattern 4: Long-Running Tasks

To run tests/builds in isolation while continuing development:

```bash
# Create worktree for CI-like testing
git worktree add ../project-test main

# Start long-running tests in background
cd ../project-test && npm test &

# Continue development in main worktree
cd ../project
```

### Pattern 5: Stable Reference

To maintain a clean main checkout for reference:

```bash
# Create permanent worktree for main branch
git worktree add ../project-main main

# Lock to prevent accidental removal
git worktree lock --reason "Reference checkout" ../project-main
```

## Directory Structure Conventions

Organize worktrees predictably:

```
~/projects/
  myproject/              # Main worktree (main/master branch)
  myproject-feature-x/    # Feature branch worktree
  myproject-hotfix/       # Hotfix worktree
  myproject-review/       # Temporary PR review worktree
```

**Naming convention:** `<project>-<purpose>` or `<project>-<branch>`

## Best Practices

| Practice | Rationale |
|----------|-----------|
| **Use sibling directories** | Keep worktrees at same level as main project for easy navigation |
| **Name by purpose** | `project-review` is clearer than `project-pr-123` |
| **Clean up promptly** | Remove worktrees when done to avoid confusion |
| **Lock remote worktrees** | Prevent pruning if worktree is on network/USB storage |
| **Use `--detach` for experiments** | Avoid creating throwaway branches |
| **Commit before removing** | Always commit or stash before `git worktree remove` |

## Common Issues and Solutions

### Issue: "Branch is already checked out"

**Cause:** Attempting to checkout a branch that's active in another worktree.

**Solution:**

```bash
# Find where the branch is checked out
git worktree list

# Either work in that worktree or remove it first
git worktree remove ../other-worktree
```

### Issue: Stale worktree after manual deletion

**Cause:** Deleted worktree directory without using `git worktree remove`.

**Solution:**

```bash
# Clean up stale metadata
git worktree prune
```

### Issue: Worktree moved manually

**Cause:** Moved worktree directory without using `git worktree move`.

**Solution:**

```bash
# Repair the worktree links
git worktree repair
# Or specify the new path
git worktree repair /new/path/to/worktree
```

### Issue: Worktree on removed drive

**Cause:** Worktree was on removable storage that's no longer connected.

**Solution:**

```bash
# If temporary, lock it to prevent pruning
git worktree lock ../usb-worktree

# If permanent, prune it
git worktree prune
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `rm -rf` to delete worktree | Always use `git worktree remove`, then `git worktree prune` if needed |
| Forgetting branch is locked to worktree | Run `git worktree list` before checkout errors |
| Not cleaning up temporary worktrees | Remove worktrees immediately after task completion |
| Creating worktrees in nested locations | Use sibling directories (`../project-feature`) not subdirs |
| Moving worktree directory manually | Use `git worktree move` or run `git worktree repair` after |

## Agent Workflow Integration

To isolate parallel agent tasks:

```bash
# Create worktree for isolated task
git worktree add -b task-123 ../project-task-123
cd ../project-task-123
# Make changes, run tests, return
cd ../project
```

To experiment safely with detached HEAD:

```bash
# Create detached worktree (no branch to clean up)
git worktree add --detach ../project-experiment
cd ../project-experiment
# Experiment, then discard or commit to new branch
git worktree remove --force ../project-experiment
```

## Quick Reference

| Task | Command |
|------|---------|
| Create worktree (existing branch) | `git worktree add <path> <branch>` |
| Create worktree (new branch) | `git worktree add -b <branch> <path>` |
| Create worktree (new branch from ref) | `git worktree add -b <branch> <path> <start>` |
| Create detached worktree | `git worktree add --detach <path> <commit>` |
| List all worktrees | `git worktree list` |
| Remove worktree | `git worktree remove <path>` |
| Force remove worktree | `git worktree remove --force <path>` |
| Move worktree | `git worktree move <old> <new>` |
| Lock worktree | `git worktree lock <path>` |
| Unlock worktree | `git worktree unlock <path>` |
| Prune stale worktrees | `git worktree prune` |
| Repair worktree links | `git worktree repair` |

## Verification Checklist

Before using worktrees:

- [ ] Understand that branches can only be checked out in one worktree
- [ ] Know where worktrees will be created (use sibling directories)
- [ ] Plan cleanup strategy for temporary worktrees

When creating worktrees:

- [ ] Use descriptive directory names
- [ ] Verify branch is not already checked out elsewhere
- [ ] Consider using `--detach` for experiments

When removing worktrees:

- [ ] Commit or stash any uncommitted changes
- [ ] Use `git worktree remove`, not `rm -rf`
- [ ] Run `git worktree prune` if directory was deleted manually
