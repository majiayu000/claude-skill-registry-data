---
name: git-spice
description: Manage Git branches and pull requests using git-spice (gs). Use when user says "/gs", "create branch", "new branch", "switch branch", "checkout branch", "rebase branch", "update branch from main", "create PR", "submit PR", "open pull request", needs to manage multiple related branches, wants stacked PRs or PR chains, or asks about rebasing and branch dependencies. Handles branch creation, navigation, rebasing, and PR submission.
argument-hint: "[branch-name or command]"
context: fork
allowed-tools:
  - Bash(gs:*)
  - Bash(git:*)
  - Read
  - Edit
---

# Git Spice Skill

This skill helps you manage stacked Git branches using git-spice (`gs`), a CLI tool for creating, navigating, and submitting branch stacks as pull requests.

## When to Use This Skill

Use this skill when the user wants to:
- Create a new feature branch ("create a branch", "new branch called X")
- Switch to another branch ("switch branch", "checkout branch")
- Update a branch with latest main ("rebase my branch", "update from main")
- Create a pull request ("create PR", "submit PR", "open pull request")
- Manage multiple related changes ("I have several related changes")
- Work with stacked branches for large features broken into reviewable chunks
- Navigate up/down through branch stacks
- Submit multiple related PRs as a stack
- Manage branch dependencies and PR chains on GitHub/GitLab

## Core Concepts

**Stacked Branches**: A series of branches where each branch is based on the previous one, forming a dependency chain rooted at trunk (main/master).

```
    ┌── feat3 (#3)    <- top of stack
  ┌─┴ feat2 (#2)
┌─┴ feat1 (#1)        <- bottom of stack
main                  <- trunk
```

**Trunk**: The main development branch (main, master, or configured trunk).

**Upstack/Downstack**: Branches above/below the current branch in the stack.

## Quick Start

### 1. Initialize Repository

```bash
gs repo init
```

This sets up git-spice tracking in your repository. You'll be prompted to select the trunk branch and remote.

### 2. Create a Branch Stack

```bash
# Start from trunk
git checkout main

# Create first branch in stack
gs branch create feat1 -m "Add user model"

# Create second branch stacked on feat1
gs branch create feat2 -m "Add user API"

# Create third branch stacked on feat2
gs branch create feat3 -m "Add user tests"
```

### 3. Navigate the Stack

```bash
gs up        # Move up one branch (u)
gs down      # Move down one branch (d)
gs top       # Jump to top of stack (U)
gs bottom    # Jump to bottom of stack (D)
gs trunk     # Return to trunk branch
```

### 4. View Your Stack

```bash
gs log short    # List all tracked branches (ls)
gs log long     # Show branches with commits (ll)
```

### 5. Submit PRs

```bash
gs stack submit     # Submit entire stack as PRs (ss)
gs branch submit    # Submit current branch only (bs)
gs upstack submit   # Submit current and all above (uss)
gs downstack submit # Submit current and all below (dss)
```

### 6. Sync and Restack

```bash
gs repo sync       # Pull latest, delete merged branches (rs)
gs stack restack   # Rebase all branches onto latest (sr)
```

## Command Reference (Shorthands)

| Command | Shorthand | Description |
|---------|-----------|-------------|
| `gs branch create` | `gs bc` | Create new branch |
| `gs branch checkout` | `gs bco` | Switch to branch |
| `gs branch submit` | `gs bs` | Submit branch as PR |
| `gs branch restack` | `gs br` | Rebase branch on base |
| `gs branch delete` | `gs bd` | Delete branch |
| `gs branch onto` | `gs bon` | Move branch onto another |
| `gs branch edit` | `gs be` | Interactive rebase |
| `gs stack submit` | `gs ss` | Submit entire stack |
| `gs stack restack` | `gs sr` | Restack entire stack |
| `gs upstack submit` | `gs uss` | Submit upstack |
| `gs upstack restack` | `gs usr` | Restack upstack |
| `gs downstack submit` | `gs dss` | Submit downstack |
| `gs repo sync` | `gs rs` | Sync with remote |
| `gs repo init` | `gs ri` | Initialize repo |
| `gs commit create` | `gs cc` | Create commit |
| `gs commit amend` | `gs ca` | Amend commit |
| `gs log short` | `gs ls` | List branches |
| `gs log long` | `gs ll` | List with commits |

## Common Workflows

### Creating a Feature Stack

```bash
# Start from updated trunk
gs trunk
git pull

# Create logical branches for each reviewable piece
gs bc api-models -m "Add data models for new API"
gs bc api-handlers -m "Implement API handlers"
gs bc api-tests -m "Add API integration tests"

# View your stack
gs ll
```

### Updating After Review Feedback

```bash
# Navigate to branch that needs changes
gs bco api-handlers

# Make changes, then amend or create new commit
gs ca  # amend current commit
# or
gs cc -m "Address review feedback"

# Restack all branches above to incorporate changes
gs usr  # upstack restack
```

### Syncing with Upstream Changes

```bash
# Sync repo - pulls trunk, deletes merged branches
gs rs

# Restack all tracked branches onto new trunk
gs repo restack
# or for just current stack:
gs sr
```

### Moving a Branch

```bash
# Move current branch onto a different base
gs bon main           # Move onto main directly
gs bon other-feature  # Move onto another branch

# Insert a new branch in the middle of a stack
gs bc new-branch --insert  # Restacks upstack onto new branch
```

### Handling Conflicts

When restacking encounters conflicts:

```bash
# Resolve conflicts in your editor
git status  # See conflicted files
# ... fix conflicts ...
git add <resolved-files>

# Continue the restack operation
gs rebase continue  # (gs rbc)

# Or abort if needed
gs rebase abort     # (gs rba)
```

### Submitting PRs

```bash
# Submit all branches in stack as linked PRs
gs ss

# Submit with draft PRs
gs ss --draft

# Submit only current branch
gs bs

# Update PR after changes
gs bs  # Re-run submit updates existing PR
```

## Branch Operations

### Track Existing Branches

```bash
# Track a single branch
gs branch track feature-branch --base main

# Track all branches in a downstack
gs downstack track
```

### Split and Squash

```bash
# Split current branch into multiple commits
gs branch split

# Squash branch into single commit
gs branch squash
```

### Delete Branches

```bash
# Delete a single branch
gs bd feature-branch

# Delete entire upstack
gs upstack delete

# Delete entire stack
gs stack delete
```

## Authentication

```bash
gs auth login   # Authenticate with GitHub/GitLab
gs auth status  # Check current auth status
gs auth logout  # Clear credentials
```

## Configuration

Git-spice uses git config for settings:

```bash
# Set branch name prefix
git config spice.branchCreate.prefix "username/"

# Configure navigation comment style
git config spice.submit.navigationComment multiple

# View all spice config
git config --get-regexp spice
```

## Troubleshooting

### Branch Not Tracked

```bash
# Track an existing branch
gs branch track my-branch --base main
```

### Rebase Conflicts

```bash
# After resolving conflicts
gs rebase continue

# To abort and try different approach
gs rebase abort
```

### Out of Sync with Remote

```bash
gs repo sync    # Fetch and sync
gs repo restack # Restack all branches
```

### Force Push After Restack

After restacking, branches need force push:
```bash
gs bs --force  # Submit handles force push
# or manually:
git push --force-with-lease
```

## Reference Documentation

For detailed information on specific topics, see:
- [Command Reference](references/commands.md) - Complete command documentation
- [Workflows](references/workflows.md) - Advanced workflow patterns

## Key Principles

1. **Atomic branches**: Each branch should be one logical, reviewable change
2. **Stack from trunk**: Build stacks starting from main/master
3. **Restack often**: Keep branches rebased on latest changes
4. **Submit together**: Use `gs ss` to create linked PRs
5. **Sync regularly**: Use `gs rs` to stay current with upstream
