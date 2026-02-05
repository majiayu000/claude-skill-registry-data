---
name: git-worktree-setup
description: Automates creation and management of headless git worktree structures. Use when the user requests to clone a repository with worktree setup, convert an existing repository to use worktrees, or add new worktrees to a bare repository. Triggers on requests like "set up worktrees", "headless git setup", "bare repo with worktrees", or "add a worktree for branch X".
---

# Git Worktree Setup

## Overview

Automate the creation and management of git repositories using a bare repository with worktrees structure. This approach allows working on multiple branches simultaneously without switching contexts, stashing changes, or reinstalling dependencies.

## When to Use This Skill

Invoke this skill when users request:
- Setting up a new repository from GitHub with worktree structure
- Converting an existing cloned repository to use worktrees
- Adding new worktrees to an existing bare repository setup
- Explaining or troubleshooting worktree configurations

## Core Workflows

### 1. Clone and Setup from GitHub

When the user provides a GitHub URL and wants worktree structure:

1. Use `scripts/setup_bare_repo.sh`:
   ```bash
   bash setup_bare_repo.sh <github-url> <target-dir> [default-branch]
   ```

2. The script will:
   - Clone the repository as bare (`.bare/`)
   - Configure remote tracking
   - Create the default branch worktree
   - Set up the directory structure

3. Result structure:
   ```
   target-dir/
   ├── .bare/        # Bare repository
   ├── .git          # Pointer to .bare
   └── main/         # Default branch worktree
   ```

**Example request:** "Clone my-org/my-repo and set it up with worktrees"

### 2. Convert Existing Repository

When the user has an existing cloned repository to convert:

1. Use `scripts/convert_to_worktree.sh`:
   ```bash
   bash convert_to_worktree.sh <repo-path> [default-branch]
   ```

2. The script will:
   - Warn about uncommitted changes (user must confirm)
   - Create a bare repository from the existing repo
   - Restructure to use `.bare/` directory
   - Create worktree for the default branch
   - Clean up the old working directory

3. The conversion is done in-place, preserving remote configuration

**Example request:** "Convert my existing project to use worktrees"

### 3. Add New Worktrees

When adding branches to an existing worktree-structured repository:

1. Navigate to the repository root (where `.bare/` exists)

2. Use `scripts/add_worktree.sh`:
   ```bash
   # Create new branch from base
   bash add_worktree.sh feature/new-api main

   # Checkout existing remote branch
   bash add_worktree.sh bugfix/urgent

   # Create new branch from HEAD
   bash add_worktree.sh experimental
   ```

3. The script intelligently:
   - Checks if branch exists locally or remotely
   - Creates new branch if needed
   - Sets up tracking appropriately
   - Creates worktree directory with branch name

**Example request:** "Add a worktree for the feature/auth branch"

## Manual Worktree Operations

For operations not covered by scripts, use git worktree commands directly:

**List all worktrees:**
```bash
git worktree list
```

**Remove a worktree:**
```bash
git worktree remove branch-name
# Optionally delete the branch
git branch -d branch-name
```

**Prune stale worktrees:**
```bash
git worktree prune
```

**Move a worktree:**
```bash
git worktree move old-path new-path
```

## Understanding Worktree Benefits

For detailed explanation of worktree patterns, benefits, and best practices, reference `references/worktree_patterns.md`. Load this reference when:
- User asks "why use worktrees?"
- User wants to understand the trade-offs
- Troubleshooting issues
- Explaining the directory structure

Key benefits:
- Work on multiple branches simultaneously
- No need to stash changes when switching branches
- Clean isolation (separate node_modules, build artifacts per branch)
- Better IDE integration (separate language server instances)
- Simplified local testing of multiple branches

## Common Troubleshooting

**Script not executable:**
```bash
chmod +x scripts/*.sh
```

**"Not in a bare repository setup" error:**
Ensure running from the root directory containing `.bare/` and `.git` file (not `.git` directory).

**Worktree already exists:**
```bash
git worktree list  # Check existing worktrees
git worktree remove old-worktree  # Remove if needed
```

**Submodules not initialized:**
Each worktree needs its own submodule initialization:
```bash
cd worktree-directory
git submodule update --init --recursive
```

## Implementation Notes

When implementing worktree setups:
1. Always check if `.bare/` already exists before converting
2. Make scripts executable after writing them
3. Provide clear feedback about directory structure after setup
4. Remind users to `cd` into the worktree directory to start working
5. Handle both SSH and HTTPS GitHub URLs
6. Default to `main` branch, but allow override for repos using `master` or other default branches

## Resources

### scripts/
- `setup_bare_repo.sh` - Clone from GitHub and create bare + worktree structure
- `convert_to_worktree.sh` - Convert existing repository to worktree structure
- `add_worktree.sh` - Add new worktrees intelligently

### references/
- `worktree_patterns.md` - Comprehensive guide to worktree patterns, benefits, gotchas, and best practices
