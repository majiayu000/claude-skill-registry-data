---
name: pre-presentation-cleanup
description: Complete mandatory cleanup before presenting changes for user approval in AWAITING_USER_APPROVAL state
allowed-tools: Bash, Read
---

# Pre-Presentation Cleanup Skill

**Purpose**: Ensure all cleanup is completed BEFORE presenting changes to user for final approval
in AWAITING_USER_APPROVAL state.

**Why This Matters**: Presenting changes with unsquashed commits or lingering agent branches
requires rework and creates a poor user experience. Complete cleanup first, then present clean
commits for review.

**Commit Structure**: Task branch should have TWO commits (or one if no config changes):
1. **Config commit** (first, if applicable): `.claude/`, `docs/project/`, `CLAUDE.md` changes
2. **Implementation commit** (second): Source code, tests, `changelog.md`, `todo.md` changes

## When to Use This Skill

### Use pre-presentation-cleanup When:

- Task is in AWAITING_USER_APPROVAL state (after validation passes)
- About to present changes to user for final approval
- Before showing commit SHA and `git diff --stat`

### Do NOT Use When:

- Still in IMPLEMENTATION or VALIDATION state
- Already presented and awaiting user response
- Task cleanup already completed

## Mandatory Cleanup Steps

Execute ALL steps before presenting changes to user:

### Step 1: Remove Agent Worktrees

**CRITICAL**: Use FULL ABSOLUTE PATHS for worktree removal. Git worktree commands require the exact path.

**⚠️ IMPORTANT**: Execute each worktree removal as a SEPARATE bash command to avoid multi-line parse errors.
Do NOT combine multiple `git worktree remove` commands in a single multi-line bash call.

```bash
# ✅ CORRECT: Separate bash calls (each command standalone)
TASK_NAME="{task-name}"
git worktree remove /workspace/tasks/$TASK_NAME/agents/architect/code --force 2>/dev/null || true

# Second separate call
git worktree remove /workspace/tasks/$TASK_NAME/agents/tester/code --force 2>/dev/null || true

# Third separate call
git worktree remove /workspace/tasks/$TASK_NAME/agents/formatter/code --force 2>/dev/null || true

# ❌ WRONG: Multi-line command (causes parse errors)
# git worktree remove /path1 --force
# git worktree remove /path2 --force
# git worktree remove /path3 --force
```

**Alternative - Single Line with Chaining**:
```bash
TASK_NAME="{task-name}"
git worktree remove /workspace/tasks/$TASK_NAME/agents/architect/code --force 2>/dev/null || true && git worktree remove /workspace/tasks/$TASK_NAME/agents/tester/code --force 2>/dev/null || true && git worktree remove /workspace/tasks/$TASK_NAME/agents/formatter/code --force 2>/dev/null || true
```

### Step 2: Delete Subagent Branches

```bash
# Delete agent branches (task branch preserved)
git branch -D ${TASK_NAME}-architect 2>/dev/null || true
git branch -D ${TASK_NAME}-tester 2>/dev/null || true
git branch -D ${TASK_NAME}-formatter 2>/dev/null || true
```

### Step 3: Update Archival Files (MANDATORY)

**⚠️ CRITICAL**: The task branch commit MUST include todo.md and changelog.md updates.
This ensures the atomic commit includes both implementation AND archival.

```bash
TASK_NAME="{task-name}"
cd /workspace/tasks/$TASK_NAME/code

# Update todo.md: Mark task complete (change status from IN_PROGRESS to DONE)
# Update changelog.md: Add task completion entry with date and summary

# Stage archival files
git add todo.md changelog.md
```

**Archival Content Requirements**:

**todo.md update**:
- Change task status from `IN_PROGRESS` to `DONE`
- Add completion date
- Keep task entry for reference (will be cleaned in CLEANUP)

**changelog.md update**:
- Add entry under current date section
- Format: `- [task-name] Brief description of what was accomplished`
- Include key deliverables

### Step 4: Squash Commits (Two-Commit Structure)

Squash task branch commits into TWO commits (or one if no config changes):

**Step 4a: Identify file categories**
```bash
# From task worktree
cd /workspace/tasks/$TASK_NAME/code

# List all changed files
git diff --name-only main...HEAD

# Categorize:
# CONFIG FILES: .claude/*, docs/project/*, CLAUDE.md
# IMPLEMENTATION FILES: Everything else (*.java, tests, changelog.md, todo.md)
```

**Step 4b: Create config commit (if config files changed)**
```bash
# If any .claude/, docs/project/, or CLAUDE.md files changed:
# 1. Create a separate commit with ONLY config files
# 2. Use git rebase -i to reorder/squash config changes into first commit

# Example: If you have mixed commits, use interactive rebase to:
# - Move all config file changes into first commit
# - Move all implementation changes into second commit
```

**Step 4c: Create implementation commit**
```bash
# Squash all implementation changes (source, tests, changelog, todo) into second commit
# Use git-squash skill for the implementation portion

# IMPORTANT: Ensure todo.md and changelog.md are in the implementation commit
git status  # Should show todo.md and changelog.md staged
```

**Post-Squash Verification**:
```bash
# Count commits (should be 1 or 2)
git rev-list --count main..$TASK_NAME
# Expected: 1 (no config changes) or 2 (has config changes)

# Verify commit structure
git log --oneline main..$TASK_NAME
# Expected format:
#   abc123 Implement feature X (implementation commit - LAST)
#   def456 Update config for feature X (config commit - FIRST, if applicable)

# Verify archival files are in IMPLEMENTATION commit (last commit)
git show --stat HEAD | grep "todo.md" || echo "❌ ERROR: todo.md not in commit"
git show --stat HEAD | grep "changelog.md" || echo "❌ ERROR: changelog.md not in commit"

# Verify config files are in CONFIG commit (if applicable)
if git rev-list --count main..$TASK_NAME | grep -q "2"; then
  git show --stat HEAD~1 | grep -E "\.claude|docs/project|CLAUDE\.md"
fi
```

### Step 5: Verify Cleanup

```bash
# Verify only task branch remains (no agent branches)
git branch | grep $TASK_NAME
# Expected output: ONLY "{task-name}" (no -architect, -tester, -formatter suffixes)
```

### Step 6: Verify Commit Structure

```bash
# Count commits ahead of main
COMMIT_COUNT=$(git rev-list --count main..$TASK_NAME)
echo "Commits: $COMMIT_COUNT"
# Expected output: 1 (no config) or 2 (with config)

# If 2 commits, verify structure:
if [ "$COMMIT_COUNT" -eq 2 ]; then
  echo "Config commit (first):"
  git show --stat HEAD~1 | head -10
  echo ""
  echo "Implementation commit (second):"
  git show --stat HEAD | head -15
fi

# MANDATORY: Verify archival files are in implementation commit (HEAD)
git show --stat HEAD | grep -E "todo.md|changelog.md"
# Expected: Both todo.md and changelog.md appear in HEAD commit
```

## Complete Cleanup Script

```bash
#!/bin/bash
set -euo pipefail

TASK_NAME="${1:?Task name required}"
TASK_DIR="/workspace/tasks/$TASK_NAME"

echo "=== Pre-Presentation Cleanup for $TASK_NAME ==="

# Step 1: Remove agent worktrees
echo "Step 1: Removing agent worktrees..."
for agent in architect tester formatter; do
  WORKTREE="$TASK_DIR/agents/$agent/code"
  if [ -d "$WORKTREE" ]; then
    git worktree remove "$WORKTREE" --force 2>/dev/null && echo "  Removed $agent worktree" || true
  fi
done

# Step 2: Delete agent branches
echo "Step 2: Deleting agent branches..."
for agent in architect tester formatter; do
  BRANCH="${TASK_NAME}-${agent}"
  if git branch --list "$BRANCH" | grep -q .; then
    git branch -D "$BRANCH" && echo "  Deleted $BRANCH" || true
  fi
done

# Step 3: Squash commits (two-commit structure)
echo "Step 3: Organizing commits (config first, implementation second)..."
echo "  → Check for config files: .claude/*, docs/project/*, CLAUDE.md"
echo "  → Squash config changes into first commit (if any)"
echo "  → Squash implementation changes into second commit"

# Step 4: Verify cleanup
echo "Step 4: Verifying cleanup..."
REMAINING=$(git branch | grep "$TASK_NAME" | grep -v "^  $TASK_NAME$" || true)
if [ -n "$REMAINING" ]; then
  echo "  ❌ ERROR: Found remaining agent branches:"
  echo "$REMAINING"
  exit 1
else
  echo "  ✅ Only task branch remains"
fi

# Step 5: Verify commit structure
echo "Step 5: Verifying commit structure..."
COMMIT_COUNT=$(git rev-list --count main..$TASK_NAME)
if [ "$COMMIT_COUNT" -eq 1 ]; then
  echo "  ✅ Single commit (no config changes)"
elif [ "$COMMIT_COUNT" -eq 2 ]; then
  echo "  ✅ Two commits (config + implementation)"
else
  echo "  ❌ ERROR: Found $COMMIT_COUNT commits (expected 1 or 2)"
  echo "  Squash into: 1. config commit, 2. implementation commit"
  exit 1
fi

echo ""
echo "=== Cleanup Complete ==="
echo "Ready to present changes for user approval"
```

## Common Mistakes

### Mistake: Presenting Unsquashed Commits

```
❌ WRONG:
User, here are the changes:
  commit abc123 - Architect implementation
  commit def456 - Tester additions
  commit ghi789 - Formatter fixes
  commit jkl012 - Merge agent work
```

```
✅ CORRECT (with config changes):
[Complete all cleanup steps first]
User, here are the changes:
  commit def456 - Update hook for X handling (config)
  commit xyz789 - Implement feature X with tests (implementation)
```

```
✅ CORRECT (no config changes):
[Complete all cleanup steps first]
User, here is the change:
  commit xyz789 - Implement feature X with tests and formatting
```

### Mistake: Mixing Config and Implementation in Same Commit

```
❌ WRONG: Single commit with mixed files
$ git show --stat HEAD
  .claude/hooks/my-hook.sh   | 10 ++++
  Parser.java                | 50 +++++++
  Test.java                  | 30 +++++

✅ CORRECT: Separate commits
$ git log --oneline main..HEAD
  xyz789 Implement parser feature
  def456 Add validation hook

$ git show --stat HEAD~1  # Config commit
  .claude/hooks/my-hook.sh   | 10 ++++

$ git show --stat HEAD      # Implementation commit
  Parser.java                | 50 +++++++
  Test.java                  | 30 +++++
```

### Mistake: Subagent Branches Still Visible

```bash
# ❌ WRONG: Agent branches still exist
$ git branch | grep my-task
  my-task
  my-task-architect
  my-task-formatter
  my-task-tester

# ✅ CORRECT: Only task branch remains
$ git branch | grep my-task
  my-task
```

### Mistake: Missing Archival Files in Commit

```bash
# ❌ WRONG: Presenting without archival
$ git show --stat
  Parser.java   | 10 ++++
  Test.java     | 50 +++++++++++
  2 files changed, 60 insertions(+)
# Missing: todo.md and changelog.md!

# ✅ CORRECT: Commit includes archival files
$ git show --stat
  Parser.java   | 10 ++++
  Test.java     | 50 +++++++++++
  todo.md       |  2 +-
  changelog.md  |  3 +++
  4 files changed, 63 insertions(+), 1 deletion(-)
```

**Why This Matters**: The merge commit MUST be atomic - including both implementation
AND archival. Presenting without archival requires rework after user approval.

## Workflow Integration

```
[VALIDATION state: All tests pass]
        ↓
[Transition to AWAITING_USER_APPROVAL]
        ↓
[Invoke pre-presentation-cleanup skill] ← THIS SKILL
        ↓
Step 1: Remove agent worktrees
Step 2: Delete agent branches
Step 3: Update archival files (todo.md + changelog.md) ← CRITICAL
Step 4: Squash into two commits:
        4a. Config commit (if .claude/docs changes exist)
        4b. Implementation commit (source, tests, archival)
Step 5: Verify only task branch
Step 6: Verify commit structure (1 or 2 commits)
        ↓
[Present clean commits to user]
        ↓
[Wait for user approval]
```

## Related Skills

- **git-squash**: Used in Step 4 to squash commits
- **archive-task**: Alternative skill for archival (updates todo.md + changelog.md atomically)
- **task-cleanup**: Used AFTER merge to main (removes task branch and worktree)
- **state-transition**: Manages state machine transitions

## Verification Checklist

Before presenting to user, confirm:

- [ ] All agent worktrees removed
- [ ] All agent branches deleted
- [ ] **todo.md updated** (task status changed to DONE)
- [ ] **changelog.md updated** (task completion entry added)
- [ ] Config files (if any) squashed into FIRST commit
- [ ] Implementation files squashed into LAST commit (including archival)
- [ ] `git branch | grep {task}` shows ONLY task branch
- [ ] `git rev-list --count main..{task}` returns `1` or `2`
- [ ] `git show --stat HEAD` shows todo.md AND changelog.md in implementation commit
- [ ] If 2 commits: `git show --stat HEAD~1` shows ONLY config files (.claude/, docs/project/, CLAUDE.md)
