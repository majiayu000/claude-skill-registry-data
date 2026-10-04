---
name: gwt
description: |
  Manage git worktrees using a centralized worktrees folder. Use for parallel development,
  PR reviews, or isolated work.
author: Somto Odera
version: 1.1.0
date: 2026-02-01
---

# Git Worktree Manager (gwt)

## Problem

Nested worktree directories cause Next.js Turbopack to detect multiple lockfiles, IDE file watchers to get confused, and build tools to traverse into nested worktrees. Sibling worktrees clutter the code directory.

## Solution

Use a **centralized `worktrees/` folder** to keep all worktrees organized and your main code directory clean.

## Directory Structure

```
~/code/
├── my-project/                    # main repo
├── other-project/                 # another repo
└── worktrees/                     # all worktrees live here
    ├── my-project--feat-auth/
    ├── my-project--fix-bug/
    └── other-project--feat-x/
```

Naming: `{repo-name}--{branch-name}` (double dash separator, slashes become dashes)

## When to Use

- **Reviewing PRs** in isolation without switching branches
- **Parallel development** on multiple features
- **Testing changes** without affecting main branch state
- **Overnight/long-running** work that shouldn't block other work

## Commands

```bash
gwt new <branch> [from]   # Create worktree (copies .env files)
gwt ls                    # List worktrees for current repo
gwt go <branch>           # Output path (use: cd $(gwt go feat))
gwt switch <branch>       # Copy "cd <path> && claude" to clipboard
gwt rm <branch>           # Remove worktree + delete branch
gwt here                  # Show current worktree info
gwt path <branch>         # Alias for 'go'
```

### Flags

- `--json` - Machine-readable output
- `--no-env` - Skip .env file copying
- `--keep-branch` - Don't delete branch on rm

### Environment Variables

- `GWT_WORKTREE_DIR` - Override worktrees directory (default: `../worktrees`)

## Human Usage

### Starting a new session in a worktree

```bash
# Create worktree
gwt new feat/my-feature

# Copy switch command to clipboard and get instructions
gwt switch my-feature

# Paste the command to switch and start Claude session
# (command is already in clipboard)
```

### Quick switching

```bash
# Switch to existing worktree
gwt switch auth   # fuzzy matches feat-auth, fix-auth, etc.
```

## Agent Usage

### Working directory limitation

Claude Code's working directory resets between Bash calls. Two approaches:

**Option 1: New session (recommended for long work)**
```bash
gwt switch <branch>  # Copies command, tells user to paste
```
User starts new Claude session in the worktree.

**Option 2: Full paths (for quick operations)**
```bash
# Work with full paths from main session
WT=$(gwt go my-feature)
cd $WT && bun install
cd $WT && bun run check-types
```

### Parallel worktree operations

Agents can create and operate on multiple worktrees without switching sessions:

```bash
# Setup phase: create worktrees
gwt new feat/auth
gwt new feat/payments
gwt new fix/bug-123

# Get paths
AUTH_WT=$(gwt go auth)
PAY_WT=$(gwt go payments)
BUG_WT=$(gwt go bug)

# Install deps in parallel (if needed)
cd $AUTH_WT && bun install &
cd $PAY_WT && bun install &
cd $BUG_WT && bun install &
wait

# Work on each with full paths
# Read files
cat $AUTH_WT/src/lib/auth.ts

# Edit files (use full path in Edit tool)
# file_path: /Users/.../worktrees/project--feat-auth/src/lib/auth.ts

# Run commands
cd $AUTH_WT && bun run check-types
cd $PAY_WT && bun run test
```

### Spawning parallel agents

For complex parallel work, spawn subagents per worktree:

```bash
# Create worktrees first
gwt new feat/a
gwt new feat/b

# Then use Task tool to spawn agents:
# - Agent 1: "Work on feat/a at $(gwt go a)"
# - Agent 2: "Work on feat/b at $(gwt go b)"
```

Each subagent works independently with its worktree path.

### Programmatic access

```bash
# Get JSON list of worktrees
gwt ls --json

# Get current worktree info as JSON
gwt here --json

# Parse in scripts
gwt ls --json | jq '.[].path'
```

### Cleanup

```bash
# Remove worktree and branch
gwt rm my-feature

# Keep the branch, just remove worktree
gwt rm my-feature --keep-branch
```

## Git Operations

Worktrees share the same git database as the main repo:
- Same remotes (`origin`)
- Same refs (branches, tags)
- PRs created from worktrees target the same repository

```bash
# From worktree, PRs work normally
cd $(gwt go my-feature)
gh pr create --title "My feature"  # Creates PR against main repo
```

## Notes

- `.env` files are automatically copied from main repo on creation
- Fuzzy matching works: `gwt go auth` matches `feat-auth`
- Branch slashes become dashes: `feat/auth` → `repo--feat-auth`
- Always run `bun install` after creating a worktree
- Worktrees share git remotes/config with main repo
- All worktrees are in one place: `~/code/worktrees/`
