---
name: git-workflow-manager
description: Manage git worktrees with GitFlow conventions for parallel development. This skill should be used when creating, managing, or cleaning up git worktrees, following standard GitFlow branch naming (feature/, fix/, hotfix/). 100% generic and reusable across all projects.
---

# Git Workflow Manager Skill

## Purpose

Manage git worktrees following GitFlow conventions, enabling parallel development workflows. Create, list, switch between, and clean up worktrees with standardized naming and directory structure. Pure Git implementation, works with any project.

## When to Use This Skill

Use this skill when:

- Need to work on multiple features/fixes in parallel
- Want to preserve working state while switching tasks
- Team members need separate worktrees for different features
- Need to quickly switch between features without stashing
- Want to maintain clean branch organization with GitFlow

## GitFlow Branch Conventions

### Branch Types

**1. Feature Branches**
- **Pattern:** `feature/{feature-name}`
- **Purpose:** New features, enhancements
- **Base:** Usually `main` or `develop`
- **Example:** `feature/email-notifications`, `feature/user-dashboard`

**2. Fix Branches**
- **Pattern:** `fix/{fix-name}` or `bugfix/{fix-name}`
- **Purpose:** Bug fixes
- **Base:** Usually `main` or `develop`
- **Example:** `fix/login-timeout`, `bugfix/form-validation`

**3. Hotfix Branches**
- **Pattern:** `hotfix/{hotfix-name}`
- **Purpose:** Critical production fixes
- **Base:** `main`
- **Example:** `hotfix/security-patch`, `hotfix/data-corruption`

**4. Release Branches** (optional)
- **Pattern:** `release/{version}`
- **Purpose:** Preparing releases
- **Base:** `develop`
- **Example:** `release/1.2.0`, `release/v2.0.0-beta`

### Naming Conventions

**Good Names:**
- Descriptive: `feature/email-notifications` ✅
- Kebab-case: `feature/user-profile-page` ✅
- Concise: `fix/timeout-error` ✅

**Bad Names:**
- Too generic: `feature/new-stuff` ❌
- Spaces: `feature/email notifications` ❌
- Too long: `feature/implement-email-notifications-with-microsoft-graph-for-form-submissions` ❌

## Worktree Directory Structure

### Standard Location

Worktrees are created in a sibling directory to the main repository:

```
project-root/               ← Main repository
project-root-worktrees/     ← Worktree parent directory
├── feature/
│   ├── email-notifications/   ← Worktree for feature/email-notifications
│   └── user-dashboard/        ← Worktree for feature/user-dashboard
├── fix/
│   └── login-timeout/         ← Worktree for fix/login-timeout
└── hotfix/
    └── security-patch/        ← Worktree for hotfix/security-patch
```

**Rationale:**
- ✅ Keeps worktrees separate from main repo
- ✅ Easy to find and manage
- ✅ Mirrors branch structure visually
- ✅ Works across all projects (generic)

### Path Calculation

Given repository at `/path/to/my-project`:
- Main repo: `/path/to/my-project`
- Worktrees: `/path/to/my-project-worktrees`

Example:
- Main: `/d/bovis-creation-forms`
- Worktrees: `/d/bovis-creation-forms-worktrees`

## Worktree Operations

### Creating a Worktree

**Command:**
```bash
# Usage: create-worktree <type> <name> [base-branch]
# Types: feature, fix, hotfix, release
# Name: descriptive name (kebab-case)
# Base: main, develop, etc. (default: main)
```

**Examples:**
```bash
# Create feature worktree
create-worktree feature email-notifications

# Result:
# - Branch: feature/email-notifications
# - Worktree: ../my-project-worktrees/feature/email-notifications/

# Create fix worktree from develop
create-worktree fix login-timeout develop

# Result:
# - Branch: fix/login-timeout (from develop)
# - Worktree: ../my-project-worktrees/fix/login-timeout/
```

**Steps Performed:**
1. Determine repository name
2. Calculate worktree parent path
3. Create worktree directory structure
4. Create git branch: `{type}/{name}`
5. Create worktree linked to branch
6. Output worktree path

**Script:** `scripts/create_worktree.sh`

### Listing Worktrees

**Command:**
```bash
# List all worktrees
list-worktrees

# Output:
# Main: /d/bovis-creation-forms [main]
# Worktrees:
#   1. feature/email-notifications → ../bovis-creation-forms-worktrees/feature/email-notifications
#   2. fix/login-timeout → ../bovis-creation-forms-worktrees/fix/login-timeout
```

**Information Displayed:**
- Branch name
- Worktree path
- Commit hash (optional)
- Status (clean/dirty)

**Script:** `scripts/list_worktrees.sh`

### Switching to Worktree

**Manual Switch:**
```bash
# Option 1: Change directory
cd ../project-worktrees/feature/email-notifications

# Option 2: Open in new terminal/IDE
code ../project-worktrees/feature/email-notifications
```

**Note:** Worktrees are independent directories. No special "switch" command needed, just `cd` to the path.

### Removing Worktrees

**When to Remove:**
- Feature/fix is complete and merged
- Branch is no longer needed
- Want to clean up disk space

**Command:**
```bash
# Remove specific worktree
remove-worktree feature/email-notifications

# Or use git directly
git worktree remove ../project-worktrees/feature/email-notifications
```

**Script:** Part of `scripts/cleanup_worktrees.sh`

### Cleaning Up Stale Worktrees

**What are Stale Worktrees?**
- Worktrees whose branches have been merged and deleted
- Worktrees manually deleted from filesystem but still registered

**Command:**
```bash
# Clean up stale worktrees
cleanup-worktrees

# Options:
# --merged: Remove worktrees for merged branches
# --stale: Remove worktree registrations for deleted directories
# --dry-run: Show what would be removed
```

**Steps Performed:**
1. List all worktrees
2. Check which branches are merged into main
3. Ask for confirmation
4. Remove worktree and delete directory
5. Prune git worktree list

**Script:** `scripts/cleanup_worktrees.sh`

## Git Worktree Basics

### What is a Worktree?

A git worktree is a linked working tree that allows you to have multiple branches checked out simultaneously.

**Without Worktrees:**
```
project/     ← Only one branch at a time
  (on main)  ← Must switch branches, stash changes
```

**With Worktrees:**
```
project/              ← Main worktree (main branch)
project-worktrees/
  feature/
    email-notif/      ← feature/email-notifications branch
  fix/
    login-timeout/    ← fix/login-timeout branch
```

Each worktree is independent, allowing simultaneous work.

### Benefits of Worktrees

✅ **Parallel Development:** Work on multiple features simultaneously
✅ **No Stashing:** Each worktree has its own working directory
✅ **Fast Switching:** Just `cd` to different directory
✅ **Isolated Builds:** Build artifacts don't interfere
✅ **Team Collaboration:** Easy to share specific feature states

### Git Worktree Commands

**Core Commands Used:**

```bash
# Create worktree
git worktree add <path> -b <branch>

# List worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Prune stale worktree entries
git worktree prune
```

## Integration with Feature Implementation Workflow

### Typical Workflow

1. **Start Feature:**
   ```bash
   # Create worktree
   create-worktree feature email-notifications
   cd ../bovis-worktrees/feature/email-notifications
   ```

2. **Implement:**
   ```bash
   # Make changes, commit
   git add .
   git commit -m "Implement email service"
   git push -u origin feature/email-notifications
   ```

3. **Complete:**
   ```bash
   # Create PR, get merged
   # Switch back to main worktree
   cd /d/bovis-creation-forms

   # Clean up
   cleanup-worktrees --merged
   ```

### Multiple Parallel Features

**Scenario:** Working on 3 features simultaneously

```bash
# Developer A
create-worktree feature email-notifications
cd ../proj-worktrees/feature/email-notifications
# [work on feature A]

# Developer A (or B)
create-worktree feature user-dashboard
cd ../proj-worktrees/feature/user-dashboard
# [work on feature B]

# Developer C
create-worktree fix login-timeout
cd ../proj-worktrees/fix/login-timeout
# [work on fix]
```

All three can progress independently without conflicts.

## Best Practices

### 1. One Feature Per Worktree

Don't mix multiple features in one worktree. Keep focused.

### 2. Regular Cleanup

Clean up merged worktrees regularly to avoid clutter:
```bash
# Weekly cleanup
cleanup-worktrees --merged
```

### 3. Descriptive Names

Use clear, descriptive names:
- ✅ `feature/real-time-notifications`
- ❌ `feature/stuff`

### 4. Commit Before Switching

Always commit or stash before switching worktrees (though each is independent):
```bash
git add .
git commit -m "WIP: partial implementation"
```

### 5. Push Regularly

Push worktree branches to remote for backup:
```bash
git push -u origin feature/my-feature
```

### 6. Keep Main Worktree Clean

Use main worktree for stable work, use feature worktrees for active development.

## Troubleshooting

### Issue: "Worktree already exists"

**Cause:** Branch already has a worktree

**Solution:**
```bash
# List worktrees to find existing one
git worktree list

# Use existing worktree or remove it first
git worktree remove <path>
```

### Issue: "Branch already exists"

**Cause:** Branch name conflicts with existing branch

**Solution:**
```bash
# Choose different name or delete old branch
git branch -d feature/old-name

# Or use existing branch
git worktree add <path> feature/existing-name
```

### Issue: "Cannot remove worktree (dirty)"

**Cause:** Uncommitted changes in worktree

**Solution:**
```bash
# Commit changes
cd <worktree-path>
git add .
git commit -m "Final changes"

# Or stash
git stash

# Then remove
git worktree remove <path>
```

### Issue: Orphaned Worktree Directory

**Cause:** Worktree directory deleted manually without `git worktree remove`

**Solution:**
```bash
# Prune stale worktree entries
git worktree prune
```

## Advanced Usage

### Creating Worktree from Specific Commit

```bash
# Create worktree at specific commit
git worktree add <path> -b <branch> <commit-hash>
```

### Creating Worktree without Creating Branch

```bash
# Checkout existing remote branch
git worktree add <path> existing-branch
```

### Detached HEAD Worktree

```bash
# Create worktree in detached HEAD state
git worktree add <path> <commit-hash>
```

## GitFlow Integration

This skill implements a simplified GitFlow:

```
main
  ├── feature/A ──┐
  ├── feature/B ──┤
  └── fix/C ───────┤
                   ├──> merge to main
  hotfix/D ────────┘
```

**Standard Flow:**
1. Create feature/fix branch from main
2. Develop in worktree
3. Create PR to merge back to main
4. Clean up worktree after merge

## Cross-Project Usage

This skill is 100% generic:

```bash
# Project A
cd /path/to/project-a
create-worktree feature new-feature

# Project B
cd /path/to/project-b
create-worktree feature another-feature

# Both use same workflow and conventions
```

## Bundled Resources

- `scripts/create_worktree.sh` - Create worktree with GitFlow conventions
- `scripts/list_worktrees.sh` - List all worktrees with status
- `scripts/cleanup_worktrees.sh` - Clean up merged and stale worktrees
- `references/gitflow-conventions.md` - Complete GitFlow reference
