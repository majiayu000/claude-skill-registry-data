---
name: git-worktrees
description: Use when starting feature work that needs isolation from current workspace. Creates isolated git worktrees with smart directory selection and safety verification. Use for parallel development, feature branches, experiments without affecting main workspace.
---

# Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

## When to Use

- Starting new feature that needs isolation
- Working on multiple features in parallel
- Experimenting without affecting main workspace
- Running tests on different branches simultaneously
- PM assigns parallel tasks to multiple specialists

## Directory Selection Priority

### 1. Check Existing Directories

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found:** Use that directory. If both exist, `.worktrees` wins.

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**If preference specified:** Use it without asking.

### 3. Default to .worktrees/

If no directory exists and no preference, create `.worktrees/`.

## Safety Verification

### For Project-Local Directories

**MUST verify directory is ignored before creating worktree:**

```bash
# Check if directory is ignored
git check-ignore -q .worktrees 2>/dev/null
```

**If NOT ignored:**
1. Add to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents.

## Creation Steps

### Step 1: Prepare

```bash
# Get project name
project=$(basename "$(git rev-parse --show-toplevel)")

# Ensure .worktrees is ignored
if ! git check-ignore -q .worktrees 2>/dev/null; then
  echo ".worktrees/" >> .gitignore
  git add .gitignore
  git commit -m "chore: ignore .worktrees directory"
fi
```

### Step 2: Create Worktree

```bash
# Create worktree with new branch
BRANCH_NAME="feature/your-feature"
git worktree add .worktrees/$BRANCH_NAME -b $BRANCH_NAME

# Navigate to worktree
cd .worktrees/$BRANCH_NAME
```

### Step 3: Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
[ -f package.json ] && npm install

# Python
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f pyproject.toml ] && poetry install

# Go
[ -f go.mod ] && go mod download

# Rust
[ -f Cargo.toml ] && cargo build
```

### Step 4: Verify Clean Baseline

```bash
# Run tests to ensure worktree starts clean
npm test        # Node.js
pytest          # Python
go test ./...   # Go
cargo test      # Rust
```

**If tests fail:** Report failures, ask whether to proceed.
**If tests pass:** Ready to work.

### Step 5: Report Location

```
Worktree ready at /path/to/project/.worktrees/feature-name
Tests passing (N tests, 0 failures)
Ready to implement [feature-name]
```

## Managing Worktrees

### List All Worktrees

```bash
git worktree list
```

### Remove Worktree

```bash
# After merging feature branch
git worktree remove .worktrees/feature-name

# Force remove (if dirty)
git worktree remove --force .worktrees/feature-name

# Clean up stale worktrees
git worktree prune
```

### Switch Between Worktrees

```bash
# Each worktree is a separate directory
cd .worktrees/feature-auth     # Work on auth
cd .worktrees/feature-payment  # Work on payment
cd /path/to/main/repo          # Back to main
```

## Integration with Super Agent

### For PM

When assigning parallel tasks:

```markdown
## Task Assignment

**Task 1.1** - Backend API (James)
Worktree: `.worktrees/sprint-1-backend`
Branch: `feature/sprint-1-backend`

**Task 1.2** - Frontend UI (Sarah)
Worktree: `.worktrees/sprint-1-frontend`
Branch: `feature/sprint-1-frontend`
```

### For Specialists

Before starting isolated work:

```bash
# 1. Create worktree
git worktree add .worktrees/my-feature -b feature/my-feature

# 2. Setup dependencies
cd .worktrees/my-feature && npm install

# 3. Verify baseline
npm test

# 4. Start work
# ... implement feature ...

# 5. When done, merge and cleanup
git checkout main
git merge feature/my-feature
git worktree remove .worktrees/my-feature
git branch -d feature/my-feature
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Create `.worktrees/` |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail | Report failures + ask |
| Feature complete | Merge + remove worktree |

## Common Mistakes

### Skipping ignore verification

**Problem:** Worktree contents get tracked
**Fix:** Always `git check-ignore` before creating

### Not cleaning up worktrees

**Problem:** Stale worktrees accumulate
**Fix:** `git worktree remove` after merge

### Forgetting to setup dependencies

**Problem:** Build fails in worktree
**Fix:** Always run `npm install` / `pip install` after creation

## Red Flags

**Never:**
- Create worktree without verifying it's ignored
- Skip baseline test verification
- Leave stale worktrees after merge
- Commit from wrong worktree

**Always:**
- Follow directory priority
- Verify directory is ignored
- Run project setup
- Verify clean baseline
- Clean up after merge
