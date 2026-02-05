---
name: git-worktree
description: Manages git worktrees including listing, creating, removing, and switching between worktrees. Use when the user mentions creating worktrees, create a work tree, create worktree, new worktrees, parallel branches, or working on multiple branches simultaneously. 
---

# Git Worktree Management Skill

This skill helps you manage git worktrees efficiently. Git worktrees allow you to check out multiple branches simultaneously in different directories, which is useful for:

- Working on multiple features in parallel
- Testing different branches without losing work-in-progress
- Reviewing code while continuing development
- Quick bug fixes on main while working on a feature branch

## Naming Convention

Worktrees should be created as sibling directories with a clear naming pattern:

**Pattern**: `../<repo-name>-wt-<branch-name>`

**Example**: For a repo named "MyProject" with branch "feature/new-login":
```
/Users/username/source/myproject/              # Main repo
/Users/username/source/myproject-wt-feature-new-login/  # Worktree
```

## Available Operations

### List Worktrees

Show all existing worktrees with their paths and branches:

```bash
git worktree list
```

Example output:
```
/Users/username/source/myproject        c5b174796b4 [main]
/Users/username/source/myproject-wt-feature-auth   def5378 [feature/new-login]
/Users/username/source/myproject-wt-hotfix-crash   ghi9022 [hotfix/button-crash-fix]
```

### Create a New Worktree

When creating worktrees, automatically use the naming convention:

**For existing branches:**
```bash
git worktree add ../<repo-name>-wt-<sanitized-branch-name> <branch-name>
```

**For new branches:**
```bash
git worktree add -b <new-branch-name> ../<repo-name>-wt-<sanitized-branch-name> <base-branch>
```

**Note**: Branch names with slashes (e.g., `feature/new-login`) should be sanitized by replacing `/` with `-` for the directory name.

Examples:
```bash
# Checkout existing feature branch
git worktree add ../myproject-wt-feature-auth feature/auth

# Create new feature branch from main
git worktree add -b feature/new-payment ../myproject-wt-feature-new-payment main

# Create hotfix worktree
git worktree add -b hotfix/critical-bug ../myproject-wt-hotfix-critical-bug main
```

### Remove a Worktree

When you're done with a worktree:

```bash
# Remove worktree (must not have uncommitted changes)
git worktree remove ../<repo-name>-wt-<branch-name>

# Force remove even with uncommitted changes
git worktree remove --force ../<repo-name>-wt-<branch-name>
```

### Prune Stale Worktrees

Clean up worktree metadata for manually deleted directories:

```bash
git worktree prune
```

### Move a Worktree

Relocate an existing worktree (maintaining naming convention):

```bash
git worktree move <old-path> <new-path>
```

### Lock/Unlock Worktrees

Prevent accidental deletion:

```bash
git worktree lock <path>
git worktree unlock <path>
```

## Helper Functions

When creating worktrees, the skill should:

1. **Get the repository name**: Extract from the current directory name
2. **Sanitize the branch name**: Replace `/` with `-` for the path
3. **Build the path**: `../<repo-name>-wt-<sanitized-branch-name>`

Example logic:
```bash
REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
BRANCH_NAME="feature/new-login"
SANITIZED_BRANCH=$(echo "$BRANCH_NAME" | sed 's/\//-/g')
WORKTREE_PATH="../${REPO_NAME}-wt-${SANITIZED_BRANCH}"

git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"
```

## Best Practices

1. **Naming Convention**: Always use `<repo-name>-wt-<branch-name>` pattern
2. **Location**: Keep worktrees as siblings to the main repo directory
3. **Cleanup**: Remove worktrees when done to avoid clutter
4. **Branch Tracking**: Each worktree tracks a different branch
5. **Shared Objects**: Worktrees share the same .git repository, saving disk space
6. **Multiple Repos**: The naming convention prevents confusion when multiple repos are in the same parent directory

## Troubleshooting

### Worktree Already Exists

If you get an error that a worktree already exists for a branch, you can:
1. Use `git worktree list` to find where it is
2. Remove the existing worktree first
3. Check out a different branch in the existing worktree

### Locked Worktree

If removal fails due to a lock:
```bash
git worktree unlock <path>
git worktree remove <path>
```

### Stale Worktree References

If worktrees were manually deleted:
```bash
git worktree prune
```

### Branch Name Sanitization

Remember to replace `/` with `-` when creating directory names from branch names like `feature/new-login` → `feature-new-login`.

## Integration with This Skill

When you ask me to:
- "List my worktrees" - I'll run `git worktree list`
- "Create a worktree for feature X" - I'll use the `<repo-name>-wt-X` naming pattern
- "Clean up worktrees" - I'll help remove old ones safely
- "Switch to worktree Y" - I'll navigate to the properly named directory
- "What worktrees exist?" - I'll list and explain them with full paths

This skill automatically applies the naming convention to keep your workspace organized, especially when managing multiple repositories in the same parent directory.
