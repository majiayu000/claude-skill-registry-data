---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

## Directory Selection Process

Follow this priority order:

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

### 3. Ask User

If no directory exists and no CLAUDE.md preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/wrangler/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## Safety Verification

### For Project-Local Directories (.worktrees or worktrees)

**MUST verify .gitignore before creating worktree:**

```bash
# Check if directory pattern in .gitignore
grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
```

**If NOT in .gitignore:**

Per our rule "Fix broken things immediately":

1. Add appropriate line to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents to repository.

### For Global Directory (~/.config/wrangler/worktrees)

No .gitignore verification needed - outside project entirely.

## Creation Steps

### 1. Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create Worktree

```bash
# Determine full path
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/wrangler/worktrees/*)
    path="~/.config/wrangler/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Create worktree with new branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

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

### 5. Store Absolute Path

**CRITICAL:** Capture and store the absolute path for subagent use:

```bash
# Store absolute path (resolves any symlinks)
WORKTREE_ABSOLUTE="$(cd "$path" && pwd -P)"
WORKTREE_BRANCH="$BRANCH_NAME"

echo "WORKTREE_ABSOLUTE=$WORKTREE_ABSOLUTE"
echo "WORKTREE_BRANCH=$WORKTREE_BRANCH"
```

**These values MUST be passed to all subagents** working in this worktree.

### 6. Report Location

```
Worktree ready at: $WORKTREE_ABSOLUTE
Branch: $WORKTREE_BRANCH
Tests passing (<N> tests, 0 failures)

IMPORTANT: For all work in this worktree, use this command pattern:
  cd $WORKTREE_ABSOLUTE && [command]

Ready to implementing-issue <feature-name>
```

## Quick Reference

| Situation                   | Action                      |
| --------------------------- | --------------------------- |
| `.worktrees/` exists        | Use it (verify .gitignore)  |
| `worktrees/` exists         | Use it (verify .gitignore)  |
| Both exist                  | Use `.worktrees/`           |
| Neither exists              | Check CLAUDE.md → Ask user  |
| Directory not in .gitignore | Add it immediately + commit |
| Tests fail during baseline  | Report failures + ask       |
| No package.json/Cargo.toml  | Skip dependency install     |

## Common Mistakes

**Skipping .gitignore verification**

- **Problem:** Worktree contents get tracked, pollute git status
- **Fix:** Always grep .gitignore before creating project-local worktree

**Assuming directory location**

- **Problem:** Creates inconsistency, violates project conventions
- **Fix:** Follow priority: existing > CLAUDE.md > ask

**Proceeding with failing tests**

- **Problem:** Can't distinguish new bugs from pre-existing issues
- **Fix:** Report failures, get explicit permission to proceed

**Hardcoding setup commands**

- **Problem:** Breaks on projects using different tools
- **Fix:** Auto-detect from project files (package.json, etc.)

## Example Workflow

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Check .worktrees/ - exists]
[Verify .gitignore - contains .worktrees/]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test - 47 passing]

Worktree ready at /Users/jesse/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implementing-issue auth feature
```

## Red Flags

**Never:**

- Create worktree without .gitignore verification (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip CLAUDE.md check

**Always:**

- Follow directory priority: existing > CLAUDE.md > ask
- Verify .gitignore for project-local
- Auto-detect and run project setup
- Verify clean test baseline

## Worktree Isolation (CRITICAL)

**Problem:** Claude Code resets working directory between Bash calls. Subagents don't inherit your location context.

**Solution:** See `isolating-worktrees` skill for the full protocol. Key points:

1. **Always chain commands:** `cd $WORKTREE && git status` (not separate calls)
2. **Pass absolute path to subagents:** Include verification in every subagent prompt
3. **Verify before git operations:** Check you're in the right place before committing

**Required subagent prompt pattern:**
```markdown
## Working Directory (CRITICAL)

Worktree: [WORKTREE_ABSOLUTE]
Branch: [WORKTREE_BRANCH]

### Verify First (MANDATORY)
```bash
cd [WORKTREE_ABSOLUTE] && \
  echo "Directory: $(pwd)" && \
  echo "Branch: $(git branch --show-current)" && \
  test "$(pwd)" = "[WORKTREE_ABSOLUTE]" && echo "VERIFIED" || echo "FAILED"
```

### Command Pattern
ALL commands: `cd [WORKTREE_ABSOLUTE] && [command]`
```

## Integration

**Called by:**

- **brainstorming** (Phase 5) - Optional for isolation when design is approved and implementation follows
- **implementing-issue** - When user wants isolated workspace for implementation
- Any skill needing isolated workspace

**Pairs with:**

- **isolating-worktrees** - MUST use when dispatching subagents to work in worktree
- **finishing-a-development-branch** - Optional cleanup after work complete (handles both worktree and non-worktree cases)
- **implementing-issue** - Work happens in worktree with isolation protocol
