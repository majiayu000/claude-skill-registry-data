---
name: wt
description: Manage git worktrees with the wt CLI - create, switch, list, and delete worktrees with automatic dependency installation and graphite tracking
---

# When to Use This Skill

**Proactively use this skill when:**
- User wants to create a new feature branch or worktree
- User wants to switch between worktrees
- User wants to list existing worktrees
- User wants to clean up or delete a worktree
- User mentions working on multiple branches simultaneously

# Overview

The `wt` CLI is a git worktree management tool that automates:
- Creating worktrees in a standardized location
- Setting up dependencies with `bun install`
- Tracking branches with graphite (`gt track`)
- Copying files specified in `.worktreeinclude`
- Running type checks before creating worktrees

# CLI Reference

## Create a Worktree

```bash
wt create <path> [-b <branch>] [-p parent] [-r]
wt create -r <workspace-name> [-b <branch>] [-p parent]
```

Creates a new worktree with automatic setup:
1. Runs type check (`bun run check-types`) to ensure main branch is clean
2. Creates worktree at the specified path
3. Copies files from `.worktreeinclude` if present
4. Runs `bun install` to set up dependencies
5. Tracks branch with graphite using specified parent (default: `develop`)

**Arguments:**
- `<path>` - Path where the worktree should be created (required unless using `-r`)
- `-b, --branch <branch>` - Name of the branch to create (optional, defaults to last component of path)
- `-p, --parent <parent>` - Parent branch for graphite tracking (default: `develop`)
- `-r, --ralph` - Create in `~/.ralph/projects/<repo>/<workspace-name>` directory

**Examples:**
```bash
wt create ../deal-deploy-feature-auth                              # Branch: feature-auth, Parent: develop
wt create ../deal-deploy-fix-login -p main                         # Branch: fix-login, Parent: main
wt create ~/projects/deal-deploy-ui -b custom-name --parent main   # Branch: custom-name, Parent: main
wt create -r workspace-1                                           # Ralph: ~/.ralph/projects/deal-deploy/workspace-1, Branch: workspace-1
wt create -r workspace-1 -b feature-auth -p main                   # Ralph with custom branch and parent
```

**Notes:**
- Path can be relative or absolute
- If `-b` is not specified, branch name is inferred from the last component of the path/workspace name
- The `-r` flag automatically creates worktrees in `~/.ralph/projects/<repo>/` for easier project organization
- If worktree already exists at the path, suggests using `wt go` instead
- Type check must pass before worktree creation proceeds
- Automatically changes to the new worktree directory on success

## Switch to a Worktree

```bash
wt go <branch>
```

Changes to an existing worktree directory.

**Arguments:**
- `<branch>` - Name of the branch/worktree to switch to (required)

**Examples:**
```bash
wt go feature-auth
wt go fix-login
```

**Notes:**
- Worktree must already exist
- Works with worktrees in any location (standard paths, ralph paths, custom paths)
- If worktree doesn't exist, suggests using `wt create` instead
- Changes current directory to the worktree location
- Autocomplete available - press Tab to see available branches

## List Worktrees

```bash
wt list
wt ls
```

Shows all git worktrees with their paths and branches.

**Examples:**
```bash
wt list
wt ls
```

**Output:** Standard `git worktree list` output showing paths, commit hashes, and branches

## Delete a Worktree

```bash
wt delete <branch> [-f]
```

Removes a worktree and its associated branch.

**Arguments:**
- `<branch>` - Name of the branch/worktree to delete (required)
- `-f, --force` - Force deletion even if worktree has uncommitted changes

**Examples:**
```bash
wt delete feature-auth        # Normal deletion
wt delete feature-auth -f     # Force deletion
wt delete feature-auth --force  # Force deletion
```

**Notes:**
- Worktree must exist
- Works with worktrees in any location (standard paths, ralph paths, custom paths)
- Without `-f`, deletion fails if there are uncommitted changes
- Use `-f` cautiously as it will discard uncommitted work
- Autocomplete available - press Tab to see available branches

# Worktree Include File

The `.worktreeinclude` file (optional) specifies files/patterns to copy to new worktrees:

**Example `.worktreeinclude`:**
```
.env
.env.local
config/*.local.json
# Comments are ignored
```

**Behavior:**
- Each line is a glob pattern relative to repo root
- Files matching patterns are copied to the new worktree
- Preserves directory structure
- Lines starting with `#` are ignored
- Blank lines are ignored

# Workflow Examples

## Starting a new feature

```bash
# From main repo
wt create ../deal-deploy-feature-auth

# Automatically:
# - Checks types
# - Creates worktree at ../deal-deploy-feature-auth
# - Creates branch named 'feature-auth' (inferred from path)
# - Copies .env and other included files
# - Runs bun install
# - Tracks with graphite (parent: develop)
# - Switches to new worktree

# Start coding!
```

## Using Ralph directories for organized workspaces

```bash
# Create a ralph worktree
wt create -r workspace-1

# Automatically:
# - Creates worktree at ~/.ralph/projects/deal-deploy/workspace-1
# - Creates branch named 'workspace-1'
# - Rest is the same as above

# Custom branch name with ralph
wt create -r workspace-1 -b feature-auth
# Path: ~/.ralph/projects/deal-deploy/workspace-1
# Branch: feature-auth
```

## Working on a hotfix from main

```bash
wt create ../deal-deploy-hotfix-critical -p main

# Creates worktree tracking main branch
# Branch name 'hotfix-critical' inferred from path
```

## Switching between features

```bash
wt go feature-auth    # Switch to auth feature
wt go feature-ui      # Switch to UI feature
wt go main            # Switch back to main worktree
```

## Cleaning up completed work

```bash
wt delete feature-auth     # After merging feature
wt list                    # See remaining worktrees
```

## Checking all active worktrees

```bash
wt ls

# Example output:
# /home/user/myrepo              abc123 [main]
# /home/user/myrepo-feature-auth def456 [feature-auth]
# /home/user/myrepo-feature-ui   ghi789 [feature-ui]
```

# Integration Points

## Type Checking
- Runs `bun run check-types` before creating worktrees
- Prevents creating worktrees when main branch has type errors
- Ensures clean starting point for new work

## Graphite
- Automatically runs `gt track -p <parent>` after worktree creation
- Integrates worktree workflow with graphite stacking
- Default parent: `develop`
- Override with `-p` flag

## Bun
- Uses `bun install` for dependency installation
- Runs in each new worktree automatically
- Ensures dependencies are up to date

# Error Handling

**Not in a git repository:**
```
Error: Not in a git repository
```
Solution: Run from within a git repository

**Type check fails:**
```
Type check failed. Fix errors before creating worktree.
```
Solution: Fix type errors in current worktree before creating new one

**Worktree already exists:**
```
Worktree already exists at ../myrepo-feature-auth
Use: wt go feature-auth
```
Solution: Use `wt go` to switch to existing worktree

**Worktree not found:**
```
Worktree 'feature-auth' not found
Use: wt create feature-auth
```
Solution: Create the worktree first with `wt create`

# Instructions for Claude

1. **Determine the user's intent** - What do they want to do with worktrees?
2. **Check current context** - Are they in a git repository? What's the main repo name?
3. **Run the appropriate wt command** using the Bash tool
4. **Handle errors gracefully** - Suggest fixes based on error messages
5. **Report the outcome** - Clearly communicate what happened and next steps

# Common Patterns

**User wants to start new work:**
```bash
wt create ../deal-deploy-feature-name
```

**User wants to work from a different parent branch:**
```bash
wt create ../deal-deploy-feature-name -p main
```

**User wants a different branch name than the path:**
```bash
wt create ../deal-deploy-workspace-1 -b feature-name
```

**User wants to see what they're working on:**
```bash
wt ls
```

**User finished with a feature:**
```bash
wt delete feature-name
```

**User wants to switch context:**
```bash
wt go other-feature
```
