---
name: scm
description: Source Code Management skill for the ikigai project
---

# Source Code Management

## Description
jj workflow for preserving all work. Nothing is ever lost.

## Core Principle

**Every change is automatically tracked. Nothing is ever lost.**

In jj, the working copy (`@`) is always a commit. There's no staging area. Every file save is immediately part of the current commit. This makes "losing work" nearly impossible.

## Rules

### 1. Commit After Every Testable Change

After each TDD cycle (Red → Green → Verify), finalize and start fresh:

```bash
jj commit -m "descriptive message"
```

This creates a new empty working copy. Don't batch commits. Don't wait for "a good stopping point." The worktree will be squash-merged anyway - frequent commits only help you.

### 2. jj Auto-Tracks Everything

Unlike git, jj has no "uncommitted code at risk" - your working copy IS a commit being edited. However, before operations that modify history:
- Before running `jj restore` (discards working copy changes)
- Before running `jj abandon` (removes commits)
- Before closing the session (commit to finalize)

Finalize with `jj commit` or `jj describe` first.

### 3. Experiments: Commit, Try, Backout

When experimenting:

```bash
# 1. Commit the experiment
jj commit -m "experiment: trying X approach"

# 2. Test/evaluate the experiment

# 3a. If keeping: continue working
# 3b. If discarding: backout cleanly
jj backout -r @-
```

The experiment is preserved in history even after backing out. You can always recover it.

### 4. Unknown Changes: Describe First, Understand Later

If you encounter changes you don't understand:

```bash
# Wrong: discard unknown changes
jj restore  # DANGEROUS - loses working copy changes

# Right: preserve then investigate
jj commit -m "checkpoint: unknown changes"
jj diff -r @-  # examine what changed
# Later: backout if unwanted
```

### 5. Discarding Code: Commit, Then Delete

Even when intentionally removing code:

```bash
# 1. Commit current state
jj commit -m "checkpoint before removing X"

# 2. Delete the code
# 3. Commit the deletion
jj commit -m "remove X"
```

Now you can recover the deleted code from history if needed.

## Why This Matters

- **Recovery**: Any past state is one `jj edit` away
- **Debugging**: Use `jj log` and manual bisection to find issues
- **Confidence**: Experiment freely knowing nothing is lost
- **Squash merge**: All these commits collapse to one clean commit at release

## Key Commands

| Task | Command |
|------|---------|
| Finalize and start new | `jj commit -m "message"` |
| Update current commit message | `jj describe -m "message"` |
| Squash into parent | `jj squash` |
| Discard working copy changes | `jj restore` |
| Backout a commit | `jj backout -r <revision>` |
| View recent history | `jj log` |
| View diff of revision | `jj diff -r <revision>` |

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| `jj restore` without thinking | Commit first, then restore |
| `jj abandon` without checking | Ensure commit is truly unwanted |
| Batch multiple changes in one commit | Commit after each testable change |
| Leave session without finalizing | Commit or describe before stopping |
