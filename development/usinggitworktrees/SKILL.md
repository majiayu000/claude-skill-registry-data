---
name: UsingGitWorktrees
description: Creates isolated git worktrees with smart directory selection and safety verification for parallel development. USE WHEN starting feature work that needs isolation from current workspace OR before executing implementation plans OR working on multiple branches simultaneously OR need clean test environment. Creates isolated workspaces sharing the same repository.
---

# UsingGitWorktrees

Create isolated git workspaces for parallel development without switching branches.

## Overview

Git worktrees create isolated working directories that share the same repository, allowing:
- Work on multiple branches simultaneously
- Isolated test environments
- Clean baseline for new features
- No stashing or switching required

**Core principle:** Systematic directory selection + safety verification = reliable isolation

**Announce at start:** "I'm using the UsingGitWorktrees skill to set up an isolated workspace."

## Why Use Git Worktrees?

### Benefits

✅ **Multiple branches active**: Work on feature branch while keeping main branch clean
✅ **Isolated testing**: Each worktree has its own working directory and build artifacts
✅ **No switching**: No need to stash changes or switch branches
✅ **Clean baselines**: Start new work with verified clean state
✅ **Parallel CI**: Run tests in multiple worktrees simultaneously

### vs. Branch Switching

| Aspect | Branch Switching | Git Worktrees |
|--------|------------------|---------------|
| Working directory | One (must switch) | Multiple (parallel) |
| Uncommitted changes | Must stash | Keep in original worktree |
| Dependencies | Reinstall on switch | Separate per worktree |
| Build artifacts | Shared (conflicts) | Isolated |
| Test runs | Sequential only | Parallel capable |

## Directory Selection Process

Follow this priority order:

### 1. Check for Existing Worktree Directory

```bash
# Check in priority order
if [ -d .worktrees ]; then
    WORKTREE_DIR=".worktrees"
elif [ -d worktrees ]; then
    WORKTREE_DIR="worktrees"
fi
```

**If found:** Use that directory (`.worktrees` takes priority over `worktrees`)

### 2. Check CLAUDE.md for Preference

```bash
if [ -f CLAUDE.md ]; then
    grep -i "worktree.*director" CLAUDE.md
fi
```

**If preference specified:** Use it without asking user

### 3. Ask User

If no directory exists and no CLAUDE.md preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden, recommended)
2. worktrees/ (project-local, visible)
3. ~/worktrees/<project-name>/ (global location)

Which would you prefer?
```

**Recommendation:** `.worktrees/` keeps project directory clean while remaining local

## Safety Verification

### For Project-Local Directories (.worktrees or worktrees)

**MUST verify directory is git-ignored before creating worktree:**

```bash
# Check if directory is properly ignored
if ! git check-ignore -q .worktrees && ! git check-ignore -q worktrees; then
    echo "WARNING: Worktree directory is not ignored!"
    # Must fix before proceeding
fi
```

**Why critical:** Prevents accidentally committing worktree contents to repository

**If NOT ignored - MUST fix immediately:**

```bash
# Add to .gitignore
echo ".worktrees/" >> .gitignore
# OR
echo "worktrees/" >> .gitignore

# Commit the change
git add .gitignore
git commit -m "chore: ignore git worktree directory"
```

### For Global Directory (~/worktrees)

No .gitignore verification needed - outside project entirely

## Worktree Creation Steps

### Step 1: Detect Project Name

```bash
PROJECT=$(basename "$(git rev-parse --show-toplevel)")
```

### Step 2: Determine Branch Name

```bash
# Sanitize branch name for filesystem
BRANCH_NAME="feature/user-authentication"
BRANCH_PATH=$(echo "$BRANCH_NAME" | tr '/' '-')  # feature-user-authentication
```

### Step 3: Construct Worktree Path

```bash
case $WORKTREE_DIR in
  .worktrees|worktrees)
    WORKTREE_PATH="$WORKTREE_DIR/$BRANCH_PATH"
    ;;
  ~/worktrees/*)
    WORKTREE_PATH="$HOME/worktrees/$PROJECT/$BRANCH_PATH"
    ;;
esac
```

### Step 4: Create Worktree with New Branch

```bash
# Create worktree and branch in one command
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"

# Navigate to new worktree
cd "$WORKTREE_PATH"
```

**Alternative - checkout existing branch:**
```bash
# If branch already exists
git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"
```

### Step 5: Auto-Detect and Run Project Setup

Detect project type and install dependencies:

```bash
# Node.js / JavaScript
if [ -f package.json ]; then
    npm install
fi

# Rust
if [ -f Cargo.toml ]; then
    cargo build
fi

# Python
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

if [ -f pyproject.toml ]; then
    poetry install
    # OR
    pip install -e .
fi

# Go
if [ -f go.mod ]; then
    go mod download
fi

# NixOS (from home repository pattern)
if [ -f flake.nix ]; then
    nix develop --command bash -c "echo 'Development environment ready'"
fi
```

### Step 6: Verify Clean Baseline

Run tests to ensure worktree starts in working state:

```bash
# Node.js
npm test

# Rust
cargo test

# Python
pytest

# Go
go test ./...

# NixOS
nix build
# OR
make build
```

**If tests fail:**
- Report failures clearly
- Ask whether to proceed or investigate
- Document known issues

**If tests pass:**
- Report success
- Show test count and duration
- Confirm ready for work

### Step 7: Report Worktree Ready

```
Worktree created successfully

Location: /path/to/project/.worktrees/feature-user-authentication
Branch: feature/user-authentication
Tests: ✓ 47 passing (2.3s)

Ready to implement user authentication feature
```

## Managing Worktrees

### List All Worktrees

```bash
git worktree list
```

**Output:**
```
/path/to/project        abc1234 [main]
/path/to/.worktrees/feature-auth  def5678 [feature/user-authentication]
/path/to/.worktrees/bugfix-db     ghi9012 [bugfix/database-connection]
```

### Remove Worktree

```bash
# Remove worktree (keeps branch)
git worktree remove .worktrees/feature-auth

# Force remove (even with uncommitted changes)
git worktree remove --force .worktrees/feature-auth
```

### Prune Deleted Worktrees

```bash
# Clean up references to manually deleted worktrees
git worktree prune
```

### Move to Different Worktree

```bash
# Just cd to it - no branch switching needed
cd .worktrees/feature-auth
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` (takes priority) |
| Neither exists | Check CLAUDE.md → Ask user |
| Directory not ignored | Add to `.gitignore` + commit immediately |
| Tests fail during setup | Report failures + ask user |
| No package.json/Cargo.toml | Skip dependency install |
| Worktree no longer needed | `git worktree remove <path>` |
| Manual deletion cleanup | `git worktree prune` |

## Common Patterns for Your Home Repository

Based on your NixOS home repository structure:

### Building a NixOS Configuration

```bash
# Create worktree for system change
git worktree add .worktrees/sakhalin-upgrade -b feature/sakhalin-upgrade

cd .worktrees/sakhalin-upgrade

# Build without switching main worktree
make host/sakhalin/build

# If successful, deploy
make host/sakhalin/switch
```

### Working on Multiple Hosts

```bash
# Multiple worktrees for different hosts
git worktree add .worktrees/rhea-config -b feature/rhea-jellyfin
git worktree add .worktrees/aion-config -b feature/aion-audio

# Work on both simultaneously
cd .worktrees/rhea-config
make host/rhea/build

cd ../aion-config
make host/aion/build
```

### Testing Flake Changes

```bash
# Isolated worktree for flake updates
git worktree add .worktrees/flake-update -b chore/flake-update

cd .worktrees/flake-update

# Update and test
nix flake update
make dry-build

# If successful, merge to main
```

## Common Mistakes

### ❌ Skipping Ignore Verification

**Problem:** Worktree contents get tracked, pollute `git status` in main worktree
**Fix:** Always use `git check-ignore` before creating project-local worktree

### ❌ Assuming Directory Location

**Problem:** Creates inconsistency, violates project conventions
**Fix:** Follow priority: existing → CLAUDE.md → ask user

### ❌ Proceeding with Failing Tests

**Problem:** Can't distinguish new bugs from pre-existing issues
**Fix:** Report failures, get explicit permission to proceed

### ❌ Hardcoding Setup Commands

**Problem:** Breaks on projects using different tools
**Fix:** Auto-detect from project files (package.json, Cargo.toml, etc.)

### ❌ Forgetting to Remove Old Worktrees

**Problem:** Disk space waste, confusion about active work
**Fix:** Regularly run `git worktree list` and remove completed work

### ❌ Committing from Wrong Worktree

**Problem:** Changes go to wrong branch
**Fix:** Always verify current branch before committing: `git branch --show-current`

## Integration with Other Skills

**Before UsingGitWorktrees:**
- Use **Brainstorming** to clarify what feature needs isolation
- Ensure design is validated before creating worktree

**After UsingGitWorktrees:**
- Use **WritingPlans** to create implementation plan
- Use **TestDrivenDevelopment** for implementation in worktree
- Use **Git** skill for branching and commit workflows

**Cleanup after work:**
```bash
# Merge work back to main
git checkout main
git merge feature/user-authentication

# Remove worktree
git worktree remove .worktrees/feature-user-authentication

# Delete branch if done
git branch -d feature/user-authentication
```

## Examples

**Example 1: Feature development in isolation**
```
User: "Set up isolated workspace for authentication feature"

→ Invoke UsingGitWorktrees skill
→ Announce: "I'm using the UsingGitWorktrees skill to set up an isolated workspace"
→ Check for existing worktree directory
→ Find: .worktrees/ exists
→ Verify: git check-ignore confirms .worktrees/ is ignored
→ Create: git worktree add .worktrees/feature-auth -b feature/user-authentication
→ Setup: npm install
→ Test: npm test → 47 passing
→ Report: "Worktree ready at /path/to/project/.worktrees/feature-auth"
→ Ready for implementation
```

**Example 2: Parallel host configurations**
```
User: "I need to work on both rhea and aion configurations simultaneously"

→ Invoke UsingGitWorktrees skill
→ Create worktree for rhea: .worktrees/rhea-jellyfin
→ Create worktree for aion: .worktrees/aion-audio
→ Both worktrees have clean baselines
→ Can build and test both in parallel
→ Switch between with cd, no branch switching needed
```

**Example 3: First-time setup with no worktree directory**
```
User: "Create worktree for database migration"

→ Invoke UsingGitWorktrees skill
→ Check: No .worktrees/ or worktrees/ directory exists
→ Check: No CLAUDE.md preference
→ Ask user: "Where should I create worktrees?"
→ User selects: .worktrees/ (hidden)
→ Verify: Not in .gitignore
→ Fix: Add .worktrees/ to .gitignore
→ Commit: "chore: ignore git worktree directory"
→ Create: git worktree add .worktrees/db-migration -b feature/db-migration
→ Setup and verify
→ Ready for work
```

**Example 4: Cleanup after merge**
```
User: "Clean up the authentication worktree now that it's merged"

→ Navigate to main worktree
→ Verify feature branch merged: git branch --merged
→ Remove worktree: git worktree remove .worktrees/feature-auth
→ Delete branch: git branch -d feature/user-authentication
→ Confirm: git worktree list shows worktree removed
```

## Red Flags

**Never:**
- Create worktree without verifying it's ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without explicit permission
- Assume directory location when ambiguous
- Leave old worktrees around indefinitely
- Commit to wrong branch (verify with `git branch --show-current`)

**Always:**
- Follow directory priority: existing → CLAUDE.md → ask
- Verify directory is ignored for project-local
- Auto-detect and run project setup
- Verify clean test baseline
- Report clear status when worktree is ready
- Clean up worktrees when work is merged
