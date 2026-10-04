---
name: git-worktrees
description: >-
  Multiple AI agent sessions working on the same repository cause chaos. Session
  A is on branch feature/auth. Session B switches to main to check something.
  Session A's next tool call fails because the branch disappeared. Or worse:
  Session B force-pushes over Session A's work.
---
# Git Worktrees for Concurrent AI Agent Work

> One worktree per agent session. Zero merge conflicts. Full isolation.

## The Problem

Multiple AI agent sessions working on the same repository cause chaos. Session A is on branch `feature/auth`. Session B switches to `main` to check something. Session A's next tool call fails because the branch disappeared. Or worse: Session B force-pushes over Session A's work.

Traditional solutions don't work:
- Separate clones: waste disk space, slow sync
- Branch locking: blocks parallelism
- Careful coordination: requires manual intervention

The insight: Git worktrees provide isolated working directories sharing the same `.git` repository. Each AI session gets its own worktree. They can't interfere with each other.

## The Pattern

### Worktree Basics

A worktree is a separate working directory linked to the same Git repository.

**Create a worktree:**
```bash
git worktree add ~/worktrees/feature-auth feature/auth
```

This creates:
- Working directory at `~/worktrees/feature-auth`
- Checked out to branch `feature/auth`
- Shares `.git` with main repository
- Independent of other worktrees

**List worktrees:**
```bash
git worktree list
```

**Remove a worktree:**
```bash
git worktree remove ~/worktrees/feature-auth
```

### One Worktree Per AI Session

**Pattern: Isolated Feature Development**

Session A wants to work on authentication:
```bash
cd ~/code/myapp
git worktree add ~/.claude/worktrees/auth feature/auth
cd ~/.claude/worktrees/auth
# AI agent works here, isolated from other sessions
```

Session B wants to work on payments:
```bash
cd ~/code/myapp
git worktree add ~/.claude/worktrees/payments feature/payments
cd ~/.claude/worktrees/payments
# AI agent works here, completely independent
```

**Benefits:**
- Sessions can't switch each other's branches
- No conflicts from simultaneous edits
- No force-push overwrites
- Clean separation of concerns

### Worktree Lifecycle

**1. Create worktree for new feature:**
```bash
# From main repository
git worktree add ~/.claude/worktrees/feature-name -b feature/name
```

**2. AI agent works in worktree:**
```bash
cd ~/.claude/worktrees/feature-name
# Agent makes changes, commits, pushes
git add .
git commit -m "feat: implement feature"
git push origin feature/name
```

**3. Create PR, merge, cleanup:**
```bash
# After PR is merged
git worktree remove ~/.claude/worktrees/feature-name
git branch -d feature/name
```

### Detached HEAD for Safety

Use detached HEAD when multiple sessions might access the same branch.

**Problem:**
```bash
# Session A
git worktree add ~/.claude/worktrees/review-pr-123 feature/auth

# Session B tries same branch
git worktree add ~/.claude/worktrees/session-b feature/auth
# ERROR: 'feature/auth' is already checked out at '~/.claude/worktrees/review-pr-123'
```

**Solution: Detached HEAD**
```bash
# Session A
git worktree add ~/.claude/worktrees/review-pr-123 feature/auth

# Session B uses detached HEAD
git worktree add ~/.claude/worktrees/session-b --detach feature/auth
cd ~/.claude/worktrees/session-b
# Make changes
git add .
git commit -m "fix: resolve issue"
git push origin HEAD:feature/auth-session-b
```

### Worktree Location Strategy

**Never use `/tmp/`:**
```bash
# BAD: Other sessions run cleanup scripts
git worktree add /tmp/feature-auth feature/auth
# Session B runs: rm -rf /tmp/worktree-*
# Session A's work is gone!
```

**Use dedicated worktree directory:**
```bash
# GOOD: Persistent location
mkdir -p ~/.claude/worktrees
git worktree add ~/.claude/worktrees/feature-auth feature/auth
```

**Naming convention:**
```bash
~/.claude/worktrees/
  ├── auth-session-1/
  ├── auth-session-2/
  ├── payments-fix/
  └── review-pr-456/
```

Pattern: `~/.claude/worktrees/<feature>-<session-id>`

### Integration with AI Tools

**Claude Code worktree isolation:**
```bash
# Session A
claude --worktree ~/.claude/worktrees/feature-a

# Session B (different worktree)
claude --worktree ~/.claude/worktrees/feature-b
```

Each session works in its own worktree, zero interference.

**OpenCode multi-session pattern:**
```bash
# Terminal 1: Frontend work
cd ~/.claude/worktrees/frontend-dashboard
opencode

# Terminal 2: Backend work
cd ~/.claude/worktrees/backend-api
opencode

# Terminal 3: Bug fix
cd ~/.claude/worktrees/fix-auth-bug
opencode
```

Three agents, three worktrees, no conflicts.

### Worktree Cleanup Automation

**Manual cleanup:**
```bash
# After PR merged
git worktree remove ~/.claude/worktrees/feature-name
git branch -d feature/name
git remote prune origin
```

**Automated cleanup script:**
```bash
#!/bin/bash
# cleanup-worktrees.sh

WORKTREE_DIR="$HOME/.claude/worktrees"

# Find all worktrees
git worktree list --porcelain | grep -E '^worktree' | cut -d' ' -f2 | while read -r worktree; do
  if [[ "$worktree" != *"$WORKTREE_DIR"* ]]; then
    continue
  fi

  cd "$worktree" || continue
  branch=$(git rev-parse --abbrev-ref HEAD)

  # Check if branch merged to main
  if git merge-base --is-ancestor HEAD origin/main; then
    echo "Removing merged worktree: $worktree"
    git worktree remove "$worktree"
    git branch -d "$branch" 2>/dev/null
  fi
done

# Prune deleted worktrees
git worktree prune
```

**Add to cron (weekly cleanup):**
```bash
0 2 * * 0 cd ~/code/myapp && ~/scripts/cleanup-worktrees.sh
```

### Worktree for Code Review

**Pattern: Review PR in isolated worktree**

```bash
# PR #456 needs review
gh pr checkout 456 --worktree ~/.claude/worktrees/review-pr-456

cd ~/.claude/worktrees/review-pr-456

# AI agent reviews code, suggests changes
# Create review comments
gh pr review 456 --comment -b "Suggested changes"

# Cleanup after review
cd ~/code/myapp
git worktree remove ~/.claude/worktrees/review-pr-456
```

**Benefits:**
- Don't pollute main working directory
- Can review multiple PRs concurrently
- Easy cleanup after review

### Worktree for Hotfixes

**Pattern: Emergency fix in production**

```bash
# Production is broken, need hotfix
git worktree add ~/.claude/worktrees/hotfix-auth --detach production

cd ~/.claude/worktrees/hotfix-auth

# AI agent fixes the bug
git add .
git commit -m "fix: resolve auth crash"
git push origin HEAD:hotfix/auth-crash

# Create PR to production
gh pr create --base production --head hotfix/auth-crash

# After merge, cleanup
cd ~/code/myapp
git worktree remove ~/.claude/worktrees/hotfix-auth
```

**Benefits:**
- Don't disrupt ongoing feature work
- Fast context switch to production
- Clean separation from dev branches

## Anti-Patterns

### 1. Shared Branches Between Agents

**Bad:**
```bash
# Session A
cd ~/code/myapp
git checkout feature/auth
# AI works here

# Session B (same repo)
cd ~/code/myapp
git checkout main
# Session A's checkout is now broken!
```

**Why bad:**
- Sessions overwrite each other's branch checkouts
- Agent A's next tool call fails (unexpected branch)
- Force-push from one session overwrites the other

**Fix:**
```bash
# Session A
git worktree add ~/.claude/worktrees/session-a feature/auth
cd ~/.claude/worktrees/session-a

# Session B
git worktree add ~/.claude/worktrees/session-b feature/payments
cd ~/.claude/worktrees/session-b

# Fully isolated
```

### 2. Using /tmp for Worktrees

**Bad:**
```bash
git worktree add /tmp/feature-auth feature/auth
```

**Why bad:**
- Other sessions might run `rm -rf /tmp/worktree-*`
- System cleanup scripts delete /tmp on reboot
- Work is lost unexpectedly

**Fix:**
```bash
# Use persistent directory
git worktree add ~/.claude/worktrees/feature-auth feature/auth
```

### 3. No Cleanup After Completion

**Bad:**
```bash
# Create worktree
git worktree add ~/.claude/worktrees/feature-auth feature/auth

# Finish work, merge PR, forget to cleanup
# Weeks later: dozens of stale worktrees
git worktree list
# ~/.claude/worktrees/feature-auth (merged 3 weeks ago)
# ~/.claude/worktrees/feature-payments (merged 2 weeks ago)
# ~/.claude/worktrees/fix-bug (merged 1 week ago)
```

**Why bad:**
- Wasted disk space
- Confusing to know which worktrees are active
- Stale branches not cleaned up

**Fix:**
```bash
# After PR merged
git worktree remove ~/.claude/worktrees/feature-auth
git branch -d feature/auth

# Or use automated cleanup script (see above)
```

### 4. Force-Pushing Over Each Other

**Bad:**
```bash
# Session A (worktree A)
git push origin feature/auth

# Session B (worktree B, same branch via --detach)
git push --force origin feature/auth
# Session A's commits are gone!
```

**Why bad:**
- Force-push overwrites other session's work
- No warning or conflict resolution
- Data loss

**Fix:**
```bash
# Session A
git push origin feature/auth

# Session B: use different branch
git push origin HEAD:feature/auth-session-b

# Then reconcile via PR
```

### 5. Forgetting Which Worktree You're In

**Bad:**
```bash
# In worktree A
cd ~/.claude/worktrees/feature-auth
# ... work ...

# Later, forget which worktree
cd ~/code/myapp
git status
# On branch main (not feature/auth!)
# Make changes to wrong branch
```

**Why bad:**
- Changes go to wrong branch
- Confusion about current state
- Hard to track which session did what

**Fix:**
```bash
# Add worktree info to prompt
PS1='[$(basename $(git worktree list | grep $(pwd) | awk "{print \$1}"))] \w $ '

# Or use git status
git worktree list
# /Users/user/code/myapp              abc123 [main]
# /Users/user/.claude/worktrees/auth  def456 [feature/auth]

# Always check before committing
git branch --show-current
```

### 6. Not Syncing Worktrees

**Bad:**
```bash
# Session A worktree
cd ~/.claude/worktrees/feature-auth
# Work, commit, push

# Session B worktree (same repo)
cd ~/.claude/worktrees/feature-payments
git status
# Doesn't see Session A's commits to main
```

**Why bad:**
- Worktrees share `.git` but not working directories
- Changes in one worktree don't auto-appear in others
- Can lead to merge conflicts

**Fix:**
```bash
# In each worktree, fetch regularly
git fetch origin

# Or rebase on updated main
git rebase origin/main
```

### 7. Creating Worktrees Inside Worktrees

**Bad:**
```bash
cd ~/.claude/worktrees/feature-auth
git worktree add ./nested feature/nested
```

**Why bad:**
- Confusing nested structure
- Hard to track and cleanup
- Can cause Git to behave unexpectedly

**Fix:**
```bash
# All worktrees at same level
git worktree add ~/.claude/worktrees/feature-auth feature/auth
git worktree add ~/.claude/worktrees/feature-nested feature/nested
```

## Practical Workflow

### Daily Worktree Routine

**Morning: Create worktree for today's work**
```bash
cd ~/code/myapp
git fetch origin
git worktree add ~/.claude/worktrees/feature-dashboard -b feature/dashboard origin/main
cd ~/.claude/worktrees/feature-dashboard
```

**During day: Work in worktree**
```bash
# AI agent makes changes
git add .
git commit -m "feat: add dashboard component"
git push origin feature/dashboard
```

**Evening: Cleanup if merged**
```bash
# Check if merged
git log origin/main --oneline | grep "dashboard"

# If merged, cleanup
cd ~/code/myapp
git worktree remove ~/.claude/worktrees/feature-dashboard
git branch -d feature/dashboard
```

### Multi-Agent Workflow

**3 agents, 3 worktrees, parallel work:**

```bash
# Terminal 1: Frontend dashboard
git worktree add ~/.claude/worktrees/frontend-dashboard feature/dashboard
cd ~/.claude/worktrees/frontend-dashboard
claude-agent "Build user dashboard UI"

# Terminal 2: Backend API
git worktree add ~/.claude/worktrees/backend-api feature/api-dashboard
cd ~/.claude/worktrees/backend-api
claude-agent "Build dashboard API endpoints"

# Terminal 3: Tests
git worktree add ~/.claude/worktrees/tests-dashboard feature/test-dashboard
cd ~/.claude/worktrees/tests-dashboard
claude-agent "Write E2E tests for dashboard"
```

Each agent works independently, no conflicts.

### Emergency Hotfix Workflow

**Production broken, need immediate fix:**

```bash
# Don't touch main working directory
git worktree add ~/.claude/worktrees/hotfix-urgent --detach production

cd ~/.claude/worktrees/hotfix-urgent

# Fix the bug
git add .
git commit -m "fix: critical auth bug"
git push origin HEAD:hotfix/auth-urgent

# Create and merge PR
gh pr create --base production --head hotfix/auth-urgent
gh pr merge hotfix/auth-urgent --admin --squash

# Cleanup
cd ~/code/myapp
git worktree remove ~/.claude/worktrees/hotfix-urgent

# Resume normal work in main directory
cd ~/code/myapp
git pull origin main
```

### Worktree Status Script

Track all active worktrees:

```bash
#!/bin/bash
# worktree-status.sh

echo "Active worktrees:"
git worktree list --porcelain | awk '
  /^worktree/ { path=$2 }
  /^branch/ { branch=$2; print "  " path " → " branch }
  /^detached/ { print "  " path " → (detached)" }
'

echo ""
echo "Merged and ready for cleanup:"
git worktree list --porcelain | grep -E '^worktree' | cut -d' ' -f2 | while read -r worktree; do
  if [[ "$worktree" == *".claude/worktrees"* ]]; then
    cd "$worktree" || continue
    if git merge-base --is-ancestor HEAD origin/main 2>/dev/null; then
      echo "  $(basename $worktree)"
    fi
  fi
done
```

**Usage:**
```bash
./worktree-status.sh

# Output:
# Active worktrees:
#   /Users/user/code/myapp → main
#   /Users/user/.claude/worktrees/feature-auth → feature/auth
#   /Users/user/.claude/worktrees/feature-dashboard → feature/dashboard
#
# Merged and ready for cleanup:
#   feature-auth
```

## Gotchas and Edge Cases

1. **Can't checkout same branch twice:** Use `--detach` for second checkout
2. **Disk space:** Each worktree is a full working directory (plan ~500MB per worktree)
3. **IDE confusion:** Some IDEs don't handle worktrees well (VS Code needs separate windows)
4. **Hooks:** Pre-commit hooks run independently in each worktree
5. **Submodules:** Must be initialized separately in each worktree
6. **Lock files:** `package-lock.json`, `yarn.lock` can diverge between worktrees (sync carefully)

Worktrees give AI agents their own playground. No more stepping on each other's toes. One worktree per session, clean isolation, zero conflicts.
