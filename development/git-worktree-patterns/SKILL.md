---
name: git-worktree-patterns
description: Git worktree patterns for parallel development. Use when working on multiple branches simultaneously or when you need to maintain separate working directories for different branches.
---

# Git Worktree Patterns

This skill provides patterns for using Git worktrees to enable parallel development across multiple branches.

## What are Git Worktrees?

Git worktrees allow you to have multiple working directories attached to the same repository. Each worktree can be on a different branch, enabling true parallel development without the need to stash or commit incomplete work.

## Use Cases

### Parallel Feature Development

Work on multiple features or branches simultaneously without context switching:

```bash
# Main working directory
/project (main branch)

# Additional worktrees
/project-worktrees/feature-a (feature/a branch)
/project-worktrees/feature-b (feature/b branch)
/project-worktrees/hotfix (hotfix/critical branch)
```

**Common scenarios**:
- **Urgent hotfix**: Need to fix production issue while working on a feature
- **PR review**: Review someone's PR without stashing your current work
- **Parallel testing**: Run tests on one branch while developing on another
- **Side-by-side comparison**: Compare different implementations or approaches
- **Long-running builds**: Continue working while a build/test runs elsewhere

## Basic Worktree Commands

### Creating Worktrees

```bash
# Create worktree from existing branch
git worktree add ../project-feature-a feature/a

# Create worktree and new branch
git worktree add -b feature/new-feature ../project-new-feature

# Create worktree from specific commit
git worktree add ../project-hotfix abc123

# Use absolute or relative paths
git worktree add /path/to/worktrees/feature-x feature/x
```

### Listing Worktrees

```bash
# List all worktrees with their branches and paths
git worktree list

# Example output:
# /project              abc123 [main]
# /project-feature-a    def456 [feature/a]
# /project-feature-b    ghi789 [feature/b]
```

### Removing Worktrees

```bash
# Remove worktree (must not have uncommitted changes)
git worktree remove ../project-feature-a

# Force remove (discards uncommitted changes)
git worktree remove --force ../project-feature-a

# Clean up stale worktree references
git worktree prune
```

### Moving Between Worktrees

```bash
# Simply cd to the worktree directory
cd ../project-feature-a

# All git commands work normally in each worktree
git status
git commit
git push
```

## Worktree Organization Patterns

### Directory Structure

**Option 1: Sibling directories**
```
/projects/
  ├─ myproject/          (main)
  ├─ myproject-feature-a/
  ├─ myproject-feature-b/
  └─ myproject-hotfix/
```

**Option 2: Nested structure**
```
/myproject/            (main)
  └─ .worktrees/
       ├─ feature-a/
       ├─ feature-b/
       └─ hotfix/
```

**Option 3: Centralized worktrees**
```
/worktrees/
  ├─ myproject-main/
  ├─ myproject-feature-a/
  ├─ myproject-feature-b/
  └─ other-project-main/
```

### Naming Conventions

```bash
# Project-branch pattern
git worktree add ../myproject-feature-auth feature/auth

# Purpose-based pattern
git worktree add ../myproject-review feature/pr-123

# Descriptive pattern
git worktree add ../myproject-hotfix-login-bug hotfix/login-bug
```

## Advanced Worktree Workflows

### Hotfix While Developing

```bash
# You're working in main worktree on feature/large-feature
cd /project

# Urgent bug reported!
# Create hotfix worktree
git worktree add ../project-hotfix main

# Switch to hotfix worktree
cd ../project-hotfix

# Fix the bug
git checkout -b hotfix/critical-bug
# ... make changes ...
git commit -m "fix: critical production bug"
git push

# Return to feature work without losing context
cd /project
```

### PR Review Workflow

```bash
# You're working on your feature
cd /project

# Need to review a PR (branch: feature/team-pr)
git fetch origin feature/team-pr
git worktree add ../project-review feature/team-pr

# Review in separate worktree
cd ../project-review
# ... test, review, run code ...

# Clean up after review
cd /project
git worktree remove ../project-review
```

### Parallel Testing

```bash
# Run long test suite in one worktree
cd /project-main
npm test  # Takes 10 minutes

# Continue development in another worktree
cd /project-feature-x
# ... keep coding ...
```

## Best Practices

### Do's

- ✅ Use worktrees for parallel work on different branches
- ✅ Keep worktree directories organized and named clearly
- ✅ Remove worktrees when done to avoid clutter
- ✅ Use `.git/worktrees` to track all worktrees in the main repository
- ✅ Share the same `.git` directory = shared configuration, hooks, and remotes

### Don'ts

- ❌ Don't check out the same branch in multiple worktrees (Git prevents this)
- ❌ Don't forget to remove worktrees - they consume disk space
- ❌ Don't create worktrees inside other worktrees
- ❌ Don't manually delete worktree directories (use `git worktree remove`)

## Troubleshooting

### Stale Worktree References

```bash
# If you manually deleted a worktree directory
git worktree prune

# Force unlock a worktree
git worktree unlock <path>
```

### Moving Worktrees

```bash
# Move worktree to new location
git worktree move <worktree> <new-path>

# Example:
git worktree move ../project-feature-a ../new-location/feature-a
```

### Checking Worktree Status

```bash
# See which branch each worktree is on
git worktree list

# Check worktree health
git worktree list --porcelain
```

## Integration with Plugin Commands

This skill complements the git-project-management plugin commands:
- `/create_worktree` - Automated worktree creation for parallel development
- `/merge_worktree` - Streamlined worktree merging and cleanup
- Use these commands for guided worktree operations
