---
name: using-git-worktrees
description: >
  Create isolated git worktree workspaces for feature development.
  Use before starting any implementation to ensure work happens on
  a clean branch with an isolated workspace. Prevents main branch
  pollution and enables parallel workstreams.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "starting implementation"
  - context: "creating a feature branch"
  - command: "/build"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 2
---

## Overview

Git worktrees provide isolated workspaces for feature development. Instead of switching branches (which can lose context and break builds), worktrees create separate directories linked to the same repository. Each worktree has its own working tree and branch — perfect for parallel development.

## When to Use

- Before starting ANY implementation (not on main/master)
- When you need to work on multiple features simultaneously
- When you want to preserve main branch for quick reference
- When subagents need isolated environments
- NOT for trivial single-file changes (use a simple branch)

## Process

### 1. Create the Worktree

```bash
# From the main repository
git worktree add ../project-feature-name feature/feature-name
cd ../project-feature-name
```

This creates a NEW directory with a NEW branch, linked to the same repo.

### 2. Verify the Setup

Before writing any code:

```bash
# Confirm you're on the right branch
git branch --show-current  # → feature/feature-name

# Confirm clean state
git status  # → nothing to commit

# Run existing tests to establish baseline
npm test  # All existing tests should pass
```

> **If existing tests fail, STOP.** Fix the baseline before starting new work. Do not build on broken foundations.

### 3. Develop in the Worktree

Work normally with TDD in the worktree. Changes in the worktree do NOT affect the main checkout.

### 4. Clean Up

After merging or when done:

```bash
# Remove the worktree
git worktree remove ../project-feature-name

# Or if already deleted
git worktree prune
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll just work on main, it's faster" | Working on main risks unfinished code blocking other work. Worktrees take 5 seconds to create. |
| "Git worktrees are complex" | Three commands: `add`, develop, `remove`. That's it. |
| "The user wants me to start coding immediately" | Creating a worktree IS starting. It's the first step of implementation. |

## Red Flags

- Implementation starting directly on main/master without explicit user consent
- Branch switching instead of worktree creation (loses working tree state)
- Not running tests in the new worktree before starting

## Verification

- [ ] Worktree created on a feature branch (not main/master)
- [ ] Clean git status in the worktree
- [ ] Existing tests pass in the worktree (clean baseline)
- [ ] Worktree cleaned up after merge/completion

## See Also

- `codehands:finishing-a-development-branch` — Complete the work in the worktree
- `codehands:git-workflow-and-versioning` — Git conventions
