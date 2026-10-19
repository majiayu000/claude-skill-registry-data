---
name: git-branching-worktrees
description: >
  Manage Git feature branches and isolated Git worktrees for concurrent tasks
  without context-switching overhead or stashing conflicts. Use when creating
  feature branches, running multi-agent tasks simultaneously, managing multiple
  isolated workspaces, or cleaning up obsolete worktrees and branches.
compatibility: >
  Agent Skills-compatible coding agents operating in a Git repository
  environment supporting Git 2.5+.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "git, branches, worktrees, concurrency, isolation"
  topics: "version-control, devtools"
---

# Git Branching and Worktrees

Managing parallel streams of development without polluting the working tree is essential for collaborative engineering and multi-agent workflows. This skill provides standard procedures for branch lifecycle management and Git worktrees—allowing multiple branches to be checked out simultaneously in separate directories sharing the same repository storage.

## Core Rules

1. **Base branches on fresh upstream state**: Never branch off an outdated local branch without fetching upstream first.
2. **Use descriptive branch naming conventions**: Follow `type/short-description` (e.g., `feat/auth-token-refresh`, `fix/null-pointer-header`).
3. **Never switch branches with dirty uncommitted changes**: Use commits, stashes, or better yet, Git worktrees.
4. **Clean up after merge**: Remove merged local and remote branches and pruned worktrees to prevent workspace clutter.
5. **Never delete a worktree directory manually**: Use `git worktree remove` to keep Git internal metadata synchronized.

---

## 1. Branch Management Workflow

### Creating a Feature Branch
```bash
# 1. Fetch latest upstream changes
git fetch origin

# 2. Create and switch to new branch based on up-to-date main
git switch -c feat/oauth-pkce-support origin/main
# Or in older Git:
# git checkout -b feat/oauth-pkce-support origin/main
```

### Inspecting Branch Status
```bash
# List local branches with their upstream tracking and commit status
git branch -vv

# Check which branches are merged into main
git branch --merged main

# Check which branches are not yet merged
git branch --no-merged main
```

### Cleaning Up Merged Branches
```bash
# Delete a merged local branch
git branch -d feat/oauth-pkce-support

# If remote branch was merged via PR on GitHub:
git remote prune origin
```

---

## 2. Git Worktrees: Parallel Workspace Isolation

Git worktrees allow having multiple working directories attached to the same `.git` repository. Each worktree is checked out to a different branch. This enables running tests, building, or running subagents in parallel without branch-switching collisions.

### Key Benefits for Agents
- No need to `git stash` when interrupted by a high-priority bugfix.
- Subagents can work in isolated directories without touching the primary branch.
- Zero extra disk clone overhead: object database is shared.

### Creating a Worktree
```bash
# Syntax: git worktree add <path> <branch>

# Option A: Create a worktree with a new branch based on origin/main
git worktree add ../worktrees/fix-auth-leak -b fix/auth-leak origin/main

# Option B: Checkout an existing branch into a worktree
git worktree add ../worktrees/review-pr-42 feat/user-dashboard
```

### Inspecting Worktrees
```bash
# List all active worktrees and their checked-out branches
git worktree list
# Output:
# /Users/dev/repo                     0a1b2c3 [main]
# /Users/dev/worktrees/fix-auth-leak  4d5e6f7 [fix/auth-leak]
```

### Safe Worktree Removal
```bash
# 1. Ensure any changes in the worktree are committed or discarded
cd ../worktrees/fix-auth-leak && git status

# 2. From the main repository directory, remove the worktree
cd /Users/dev/repo
git worktree remove ../worktrees/fix-auth-leak

# 3. Clean up internal metadata and stale worktree references
git worktree prune
```

---

## 3. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `rm -rf <worktree-dir>` | Leaves orphaned administrative files in `.git/worktrees` | Use `git worktree remove <path>` and `git worktree prune` |
| Checking out the same branch in 2 worktrees | Git prevents this to avoid index corruption | Always use a dedicated branch per worktree |
| Branching from dirty un-fetched local branch | Inherits stale commits or unintentional edits | Fetch first, then branch explicitly from `origin/main` |
| Using `git branch -D` blindly | Force deletes unmerged work permanently | Use `-d` first; verify with `git log` before forcing deletion |

---

## 4. Real-World Scenarios

### Scenario A: Urgent Production Hotfix While Working on a Large Feature
You are halfway through a refactor on `feat/data-pipeline` with multiple modified files. A critical bug is reported in production.

```bash
# Do NOT stash or discard your changes.
# Create an isolated worktree for the hotfix:
git worktree add ../hotfix-session-crash -b fix/session-crash origin/main

# Move to the isolated hotfix directory
cd ../hotfix-session-crash

# Implement fix, test, and commit
pytest tests/test_session.py
git commit -am "fix(session): handle unexpected null payload gracefully"

# Push hotfix branch
git push origin fix/session-crash

# Return to your main repository and remove hotfix worktree
cd /Users/dev/repo
git worktree remove ../hotfix-session-crash
# Your feature workspace in /Users/dev/repo is completely untouched!
```

### Scenario B: Pruning Stale Branches and Orphaned Worktree Records

```bash
# 1. Prune remote tracking branches deleted on GitHub
git fetch --prune origin

# 2. List worktrees to identify dead directories
git worktree list

# 3. Prune dangling worktree metadata
git worktree prune

# 4. Safely remove merged local branches
git branch --merged origin/main | grep -v '^[ *]*main$' | xargs git branch -d
```

---

## 5. Verification Checklist

- [ ] New branch is created from the correct upstream baseline (`origin/main`).
- [ ] `git branch -vv` confirms tracking configuration.
- [ ] `git worktree list` displays only active, existing directory paths.
- [ ] Removed worktrees leave no dangling administrative references (`git worktree prune` reports nothing).
