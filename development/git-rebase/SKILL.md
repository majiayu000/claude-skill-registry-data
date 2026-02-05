---
name: git-rebase
description: Safely rebase, reorder, or squash commits with automatic backup and verification
allowed-tools: Bash, Read, Edit
---

# Git Rebase Skill

<!-- PATTERN EVOLUTION:
     - 2025-11-02: Fixed hardcoded v21 bug (line 117), enforced backup creation, added inline safety reminders
     - 2025-11-05: Added Scenario 4 (reorder and squash) with real example, documented GIT_SEQUENCE_EDITOR pattern, captured anti-pattern from failed shell script approach
-->

**Purpose**: Safely perform git rebases to reorder commits, squash history, or update branch base, with automatic backup and validation.

**When to Use**:
- Squashing multiple commits into one before merge
- Reordering commits to improve chronology
- Updating branch to latest main (rebasing onto main)
- Separating interleaved concerns into sequential commits
- Cleaning up commit history before push

## ⚡ Performance: Optimized Script Available

**RECOMMENDED**: Use the optimized batch script for 87% faster execution

**Performance Comparison**:
- Traditional workflow: 8-10 LLM round-trips, 40-80 seconds
- Optimized script: 2-3 LLM round-trips, 5-10 seconds
- Safety checks: All preserved (no reduction)

**When to use optimized script**:
- ✅ Interactive rebase with pre-planned todo list
- ✅ Reordering, squashing, or editing commits
- ✅ Want atomic execution with minimal LLM involvement

**When to use manual workflow**:
- Complex conflicts requiring human judgment
- Need to understand each step in detail
- Learning the git rebase process

**Optimized Script**: `/workspace/main/.claude/scripts/git-rebase-optimized.sh`

## ⚠️ Critical Safety Rules

**MANDATORY BACKUP**: Always create backup branch before rebasing
**BRANCH PRESERVATION**: NEVER delete version branches (v1, v13, v21, etc.) - update them with `git branch -f`
**VALIDATION**: Verify branch patterns before any deletion
**WORKING DIRECTORY**: Must be clean (no uncommitted changes)

## Prerequisites

Before using this skill, verify:
- [ ] Working directory is clean: `git status` shows no uncommitted changes
- [ ] Know which commits to rebase: `git log --oneline -10`
- [ ] Have clear goal: squash/reorder/update base
- [ ] Understand branch purpose (version vs temporary)

## Common Rebase Scenarios

### Scenario 1: Squash All Task Commits

**Goal**: Combine multiple commits on task branch into single commit

**Use Case**: Before merging task branch to main

### Scenario 2: Reorder Commits

**Goal**: Change commit order while preserving history

**Use Case**: Documentation commit should come before implementation

### Scenario 3: Update Branch Base

**Goal**: Rebase feature branch onto latest main

**Use Case**: Main has moved ahead, need to update feature branch

### Scenario 4: Reorder and Squash Commits

**Goal**: Move a commit to a different position in history AND squash it with another commit

**Use Case**: Archive commit (db9eee3) needs to move before style commit (27c4674) and squash with implementation commit (23b5ee3)

**✅ RECOMMENDED APPROACH**: Pre-create todo file + GIT_SEQUENCE_EDITOR

**Why**: Simple, reliable, easy to verify before execution

**❌ ANTI-PATTERN**: Complex shell scripting to manipulate git-rebase-todo in-flight

**Why fails**: Timing issues, rebase completes without applying modifications, hard to debug

## Skill Workflow

### Step 1: Backup Current State

**⚠️ MANDATORY - Create Safety Backup BEFORE ANY git reset --hard**:
```bash
# CRITICAL: Create timestamped backup FIRST - rebase destroys commits!
# DO NOT skip this step or jump to Step 3
BACKUP_BRANCH="backup-before-rebase-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_BRANCH"

# Verify backup created
if ! git rev-parse --verify "$BACKUP_BRANCH" >/dev/null 2>&1; then
  echo "❌ ERROR: Failed to create backup - STOP"
  exit 1
fi
echo "✅ Backup created: $BACKUP_BRANCH"
echo "   Restore command if needed: git reset --hard $BACKUP_BRANCH"
```

### Step 2: Analyze Current State

**Understand What You're Rebasing**:
```bash
# Count commits ahead of main
COMMIT_COUNT=$(git rev-list --count main..<branch>)

# List commits with dates
git log --oneline --graph --date=short --format="%h %ad %s" <base>..<branch>
```

### Step 3: Execute Rebase

**Method A: Interactive Rebase**:
```bash
git rebase -i <base-commit>
# Editor opens - change "pick" to "squash" or reorder lines
```

**Method B: Reset and Squash**:
```bash
git reset --soft <base-commit>
git commit -m "Combined commit message"
```

**Method C: Cherry-Pick Reorder**:
```bash
git reset --hard <base-commit>
git cherry-pick <commit-1>  # Pick in desired order
git cherry-pick <commit-2>
```

### Step 4: Validate Rebase Success

```bash
# Verify commit count
git rev-list --count <base>..<branch>

# Check build
./mvnw clean compile test
```

### Step 5: Update Related Branches

**⚠️ CRITICAL: Version Branch Management**

```bash
# SAFETY: Always check if branch is version marker before deleting
BRANCH_NAME="v21"  # Example - replace with actual branch

# Check pattern
if [[ "$BRANCH_NAME" =~ ^v[0-9]+$ ]]; then
  echo "⚠️  VERSION BRANCH - UPDATE, don't delete"
  # BUG FIX (2025-11-02): Use $BRANCH_NAME variable, not hardcoded v21
  git branch -f "$BRANCH_NAME" HEAD
else
  echo "Temporary branch - safe to delete"
  git branch -D "$BRANCH_NAME"
fi
```

### Step 6: Cleanup

```bash
# Delete backup after verification
git branch -D "$BACKUP_BRANCH"
```

**⚠️ CRITICAL: Do NOT Run Immediate Reflog/GC Cleanup**

<!-- ADDED: 2026-01-05 after agent ran reflog expire immediately after filter-branch,
     permanently destroying the safety net for recovery. -->

**NEVER** run these commands immediately after rebase or filter-branch:
```bash
# ❌ DANGEROUS - Destroys recovery safety net
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

**Why this is dangerous:**
- The reflog is your PRIMARY recovery mechanism after history-rewriting operations
- If the rebase had subtle issues (lost commits, wrong content), reflog lets you recover
- Running `reflog expire --expire=now` PERMANENTLY destroys this safety net

**Safe approach:**
1. Keep the backup branch for at least 24-48 hours
2. Let git's natural gc handle cleanup (90-day default expiration)
3. Only consider aggressive cleanup after verifying operation was 100% correct
4. If you MUST cleanup immediately, ensure you have an external backup (remote, clone)

## Complete Examples

### Example: Reorder Commits (Docs Before Implementation)

```bash
# Current: base → formatter → docs
# Want: base → docs → formatter

# Step 1: Backup
git branch backup-reorder-$(date +%Y%m%d-%H%M%S)

# Step 2: Reset to base
git reset --hard <base>

# Step 3: Cherry-pick in order
git cherry-pick <docs-commit>
git cherry-pick <formatter-commit>

# Step 4: Update version branch (NOT delete!)
git branch -f v21 HEAD

# Step 5: Validate
git log --oneline --graph -3
```

### Example: Using Optimized Script

**✅ RECOMMENDED for atomic execution**:

```bash
# 1. Create rebase todo file with desired operations
cat > /tmp/rebase-todo.txt <<'EOF'
pick abc1234 First commit
squash def5678 Second commit (squash into first)
pick ghi9012 Third commit
reword jkl3456 Fourth commit (will prompt for new message)
EOF

# 2. Execute with optimized script
/workspace/main/.claude/scripts/git-rebase-optimized.sh \
  <base-commit> \
  /tmp/rebase-todo.txt \
  main

# Script executes atomically:
# ✅ Create backup
# ✅ Validate preconditions
# ✅ Execute rebase with todo file
# ✅ Detect conflicts (outputs recovery commands)
# ✅ Update branch pointer
# ✅ Cleanup backup
# ✅ Output JSON result

# 3. Check result
git log --oneline -5
```

**Parameters**:
- `base_commit` - Parent of first commit to rebase
- `todo_file` - File containing git-rebase-todo operations
- `branch` - Optional branch to update (default: current branch)

**Supported todo operations**:
- `pick` - Use commit as-is
- `squash` - Combine with previous commit
- `reword` - Edit commit message
- `edit` - Stop for amendments
- `fixup` - Like squash but discard message
- `drop` - Remove commit

**Output**: JSON with status, duration, new commit count

### Example: Reorder and Squash (2025-11-05 Real Case)

**✅ Manual Approach - Pre-create Todo + GIT_SEQUENCE_EDITOR**:

```bash
# Goal: Move db9eee3 before 27c4674, then squash with 23b5ee3
# Original order:
#   23b5ee3 Add index-overlay parser module
#   27c4674 Update style guide and tooling
#   db9eee3 Archive task completion
#   ... (42 more commits)
#
# Desired order:
#   (23b5ee3 + db9eee3 squashed)
#   27c4674 Update style guide and tooling
#   ... (42 more commits)

# Step 1: Backup
BACKUP_BRANCH="backup-before-reorder-squash-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_BRANCH"

# Step 2: Create desired todo list
cat > /tmp/rebase-todo-modified.txt <<'EOF'
pick 23b5ee3 Add index-overlay parser module with comprehensive security controls
squash db9eee3 Archive implement-index-overlay-parser task completion
pick 27c4674 Update style guide and tooling for parser implementation
pick 3a47920 Centralize agent scope enforcement and workflow patterns
# ... (paste remaining 41 commits as-is)
EOF

# Step 3: Verify todo file before using
cat /tmp/rebase-todo-modified.txt

# Step 4: Execute rebase with GIT_SEQUENCE_EDITOR
# BASE_COMMIT is the commit BEFORE 23b5ee3 (the first commit to modify)
BASE_COMMIT="b9eb99d"
GIT_SEQUENCE_EDITOR="cp /tmp/rebase-todo-modified.txt" git rebase -i "$BASE_COMMIT"

# ⚠️ CRITICAL: If using Python/script instead of pre-created file:
# See git-squash/SKILL.md § "Automating Reorder with GIT_SEQUENCE_EDITOR"
# for critical warnings about commit order assumptions that can silently drop commits

# Step 5: Verify result
git log --oneline -5
# Should show:
#   03d995d (squashed 23b5ee3 + db9eee3)
#   27c4674 Update style guide...
#   ... (other commits)

# Step 6: Cleanup
git branch -D "$BACKUP_BRANCH"
```

**❌ ANTI-PATTERN - Complex Shell Scripting (DO NOT USE)**:

```bash
# This approach FAILED - rebase completed but didn't apply changes
# Kept for reference to avoid repeating mistake

# DON'T: Try to manipulate git-rebase-todo in-flight with complex script
git rebase -i --no-autosquash "$BASE_COMMIT" --edit-todo 2>/dev/null || true
TODO_FILE="$(git rev-parse --git-dir)/rebase-merge/git-rebase-todo"
awk '/^pick 23b5ee3/ { print $0; print "squash db9eee3"; next }
     /^pick db9eee3/ { next }
     {print}' /tmp/original-todo.txt > "$TODO_FILE"
# Result: Rebase completes but modifications aren't applied
```

**Key Lessons**:
- Pre-creating the todo file allows verification BEFORE execution
- GIT_SEQUENCE_EDITOR is simpler and more reliable than in-flight manipulation
- Complex shell scripts add timing dependencies and failure modes
- Always verify the todo file content before executing rebase

## Safety Rules Summary

**DO**:
- ✅ Create backup before every rebase
- ✅ Update version branches with `git branch -f`
- ✅ Delete only temporary branches
- ✅ Run tests after rebase

**DON'T**:
- ❌ Rebase without backup
- ❌ Delete version branches (v1, v13, v21, etc.)
- ❌ Skip validation
- ❌ Force push to shared branches

## Related Documentation

- git-workflow.md: Git workflows and squashing
- main-agent-coordination.md: Merge requirements
- CLAUDE.md: Branch management rules
