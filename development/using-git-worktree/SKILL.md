---
name: using-git-worktree
description: Create isolated git worktrees at bare repo root level
---

# Using Git Worktrees (Bare Repo Setup)

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Find bare repo root + create sibling worktree = reliable isolation.

**Announce at start:** "I'm using the Using Git Worktrees skill to set up an isolated workspace."

## Bare Repo Structure

This skill assumes a bare git repository setup:

```
project-root/
├── .bare/          # Actual git repository
├── .git            # Points to .bare
├── main/           # Worktree for main branch
├── feature-a/      # Worktree for feature-a branch
└── feature-b/      # Worktree for feature-b branch
```

Worktrees are created as siblings at the root level, not in subdirectories.

## Bare Repo Detection

### 1. Find Bare Repo Root

```bash
# Walk up directory tree to find .bare directory
current_dir=$(pwd)
bare_root=""

while [ "$current_dir" != "/" ]; do
  if [ -d "$current_dir/.bare" ]; then
    bare_root="$current_dir"
    break
  fi
  current_dir=$(dirname "$current_dir")
done

if [ -z "$bare_root" ]; then
  echo "Error: Not in a bare git repository setup (no .bare directory found)"
  exit 1
fi
```

**If `.bare` not found:** Report error - this skill requires bare repo setup.

## Creation Steps

### 1. Navigate to Bare Root

```bash
cd "$bare_root"
```

### 2. Create Worktree

```bash
# Create worktree as sibling directory at bare root
git worktree add "$BRANCH_NAME" -b "$BRANCH_NAME"
cd "$BRANCH_NAME"
```

**Note:** No .gitignore verification needed - worktrees at bare root are managed by `.bare/`, not tracked by individual worktree git status.

### 3. Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verify Clean Baseline

Run tests to ensure worktree starts clean:

```bash
# Examples - use project-appropriate command
npm test
cargo test
pytest
go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.

**If tests pass:** Report ready.

### 5. Report Location

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Inside worktree | Walk up to find `.bare/` directory |
| `.bare/` not found | Report error - requires bare repo |
| `.bare/` found | Create worktree as sibling at that level |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |

## Common Mistakes

**Not detecting bare repo root**

- **Problem:** Creates worktree in wrong location
- **Fix:** Always walk up to find `.bare/` directory first

**Proceeding with failing tests**

- **Problem:** Can't distinguish new bugs from pre-existing issues
- **Fix:** Report failures, get explicit permission to proceed

**Hardcoding setup commands**

- **Problem:** Breaks on projects using different tools
- **Fix:** Auto-detect from project files (package.json, etc.)

## Example Workflow

```
You: I'm using the Using Git Worktrees skill to set up an isolated workspace.

[Current directory: /Users/hmps/myproject/main/src]
[Walk up tree looking for .bare/]
[Found .bare at /Users/hmps/myproject/]
[Navigate to bare root: cd /Users/hmps/myproject]
[Create worktree: git worktree add feature-auth -b feature-auth]
[Navigate to worktree: cd feature-auth]
[Run npm install]
[Run npm test - 47 passing]

Worktree ready at /Users/hmps/myproject/feature-auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

## Red Flags

**Never:**

- Create worktree without finding `.bare/` root first
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume you're at bare root without checking

**Always:**

- Walk up directory tree to find `.bare/`
- Create worktree at bare root level as sibling
- Auto-detect and run project setup
- Verify clean test baseline

## Integration

**Called by:**

- skills/collaboration/brainstorming (Phase 4)
- Any skill needing isolated workspace

**Pairs with:**

- skills/collaboration/finishing-a-development-branch (cleanup)
- skills/collaboration/executing-plans (work happens here)
