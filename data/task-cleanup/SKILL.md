---
name: task-cleanup
description: Clean up task branches and worktrees after merge to main
allowed-tools: Bash, Read
---

# Task Cleanup Skill

**Purpose**: Safely remove all task branches and worktrees after successful merge to main, preserving audit trail while reclaiming resources.

**Performance**: Prevents branch accumulation, reclaims disk space, maintains clean repository

## When to Use This Skill

### ✅ Use task-cleanup When:

- Task successfully merged to main (COMPLETE state)
- All validation passed and changes approved
- Ready to finalize task and archive artifacts
- Want to reclaim disk space and clean up branches

### ❌ Do NOT Use When:

- Task not yet merged to main
- Still in IMPLEMENTATION or VALIDATION state
- Need to preserve worktrees for additional work
- Task encountered errors (keep for debugging)

## What This Skill Does

### 1. Transitions State

```bash
# Updates task.json
BEFORE: {"state": "COMPLETE", ...}
AFTER:  {"state": "CLEANUP", "cleaned_at": "2025-11-11T12:34:56-05:00", ...}
```

### 2. Removes Worktrees

```bash
# Removes all task and agent worktrees
/workspace/tasks/{task-name}/code/                    # Task worktree
/workspace/tasks/{task-name}/agents/architect/code/   # Architect worktree
/workspace/tasks/{task-name}/agents/tester/code/      # Tester worktree
/workspace/tasks/{task-name}/agents/formatter/code/   # Formatter worktree
```

### 3. Deletes Branches

```bash
# Removes all task-related branches
{task-name}                # Main task branch
{task-name}-architect      # Architect agent branch
{task-name}-tester         # Tester agent branch
{task-name}-formatter      # Formatter agent branch
```

### 4. Preserves Audit Trail

```bash
# KEEPS task directory with audit files
/workspace/tasks/{task-name}/
├── task.json                          # Final state tracking
├── task.md                            # Requirements and plans
├── user-approved-synthesis.flag       # Approval checkpoints
└── user-approved-changes.flag         # Final approval
```

## Usage

### Basic Cleanup

```bash
# Step 1: Ensure we're in main repository
cd /workspace/main

# Step 2: Execute cleanup script
/workspace/main/.claude/scripts/task-cleanup.sh "{task-name}"
```

### With Verification

```bash
# Verify task is in COMPLETE state first
TASK_NAME="implement-formatter-api"
STATE=$(jq -r '.state' /workspace/tasks/$TASK_NAME/task.json)

if [ "$STATE" = "COMPLETE" ]; then
  /workspace/main/.claude/scripts/task-cleanup.sh "$TASK_NAME"
else
  echo "❌ Task not in COMPLETE state (current: $STATE)"
  exit 1
fi
```

### Batch Cleanup

```bash
# Clean up multiple completed tasks
for task in $(jq -r 'select(.state == "COMPLETE") | .task_name' /workspace/tasks/*/task.json); do
  echo "Cleaning up $task..."
  /workspace/main/.claude/scripts/task-cleanup.sh "$task"
done
```

## Workflow Integration

### Complete Task Finalization Sequence

```markdown
1. ✅ VALIDATION state: All tests pass
2. ✅ AWAITING_USER_APPROVAL: Present changes to user
3. ✅ User approves: Create user-approved-changes.flag
4. ✅ Transition to COMPLETE: Squash and merge to main
5. ✅ Update todo.md and changelog.md
6. ✅ Invoke task-cleanup skill ← THIS SKILL
7. ✅ Task finalized and archived
```

## Output Format

Script returns JSON:

```json
{
  "status": "success",
  "message": "Task cleaned up successfully",
  "task_name": "implement-formatter-api",
  "removed_worktrees": [
    "/workspace/tasks/implement-formatter-api/code",
    "/workspace/tasks/implement-formatter-api/agents/architect/code",
    "/workspace/tasks/implement-formatter-api/agents/tester/code",
    "/workspace/tasks/implement-formatter-api/agents/formatter/code"
  ],
  "deleted_branches": [
    "implement-formatter-api",
    "implement-formatter-api-architect",
    "implement-formatter-api-tester",
    "implement-formatter-api-formatter"
  ],
  "preserved_artifacts": "/workspace/tasks/implement-formatter-api",
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

## Safety Features

### Precondition Validation

- ✅ Verifies task exists
- ✅ Checks task is in COMPLETE state (blocks cleanup otherwise)
- ✅ Confirms we're in main repository
- ✅ Validates task merged to main (checks git log)

### Careful Removal

- ✅ Removes worktrees with --force if needed (handles dirty state)
- ✅ Deletes branches one by one (continues on errors)
- ✅ Preserves task directory with audit files
- ✅ Updates state tracking to CLEANUP

### Error Handling

On any error, script:
- Continues cleanup where possible (best-effort)
- Reports which items failed to clean
- Returns JSON with partial success status
- Leaves repository in consistent state

**Recovery**: Safe to retry cleanup after fixing issues

## Verification Steps

After cleanup, verify:

```bash
# 1. Check task.json updated to CLEANUP state
cat /workspace/tasks/{task-name}/task.json | jq '.state'
# Should output: "CLEANUP"

# 2. Verify worktrees removed
git worktree list | grep {task-name}
# Should output nothing

# 3. Verify branches deleted
git branch | grep {task-name}
# Should output nothing

# 4. Verify audit files preserved
ls -la /workspace/tasks/{task-name}/
# Should show: task.json, task.md, approval flags
```

## Common Patterns

### Pattern 1: Cleanup Immediately After Merge

```bash
# Typical workflow after successful merge
cd /workspace/main

# Merge task to main (with --ff-only, task branch already squashed)
git merge --ff-only implement-api
# Note: Commit already exists on task branch with todo.md + changelog.md updates

# Update task state
jq '.state = "COMPLETE"' /workspace/tasks/implement-api/task.json > tmp.json
mv tmp.json /workspace/tasks/implement-api/task.json

# Cleanup
/workspace/main/.claude/scripts/task-cleanup.sh "implement-api"
```

### Pattern 2: Delayed Cleanup

```bash
# Keep worktrees for a while, cleanup later
# (Useful if you might need to reference implementation)

# Mark complete but don't cleanup yet
jq '.state = "COMPLETE"' /workspace/tasks/my-task/task.json > tmp.json
mv tmp.json /workspace/tasks/my-task/task.json

# ... later, when ready to cleanup ...
/workspace/main/.claude/scripts/task-cleanup.sh "my-task"
```

### Pattern 3: Cleanup with Verification Report

```bash
# Cleanup and report detailed results
TASK="implement-api"
RESULT=$(/workspace/main/.claude/scripts/task-cleanup.sh "$TASK")

echo "$RESULT" | jq -r '
  "Cleanup Results:",
  "- Status: \(.status)",
  "- Removed \(.removed_worktrees | length) worktrees",
  "- Deleted \(.deleted_branches | length) branches",
  "- Preserved: \(.preserved_artifacts)"
'
```

## Integration with Task Protocol

### State Machine Integration

```
[COMPLETE state: Merged to main]
        ↓
[Invoke task-cleanup skill] ← THIS SKILL
        ↓
task.json: state = "CLEANUP"
        ↓
Worktrees removed
Branches deleted
Audit files preserved
        ↓
[Task finalized]
```

### What Gets Preserved

**Preserved for audit trail**:
- `task.json` - Complete state history
- `task.md` - Requirements and implementation plans
- `user-approved-synthesis.flag` - Plan approval evidence
- `user-approved-changes.flag` - Final approval evidence
- Agent requirement reports (if still present)

**Removed to save resources**:
- All worktrees (code directories)
- All task and agent branches
- Temporary coordination files

## Related Skills

- **task-init**: Initialization counterpart (INIT state)
- **git-merge-linear**: Merges task to main before cleanup
- **checkpoint-approval**: Creates approval flags preserved by cleanup

## Troubleshooting

### Error: "Task not in COMPLETE state"

```bash
# Check current state
jq -r '.state' /workspace/tasks/{task-name}/task.json

# If task is stuck, investigate why
# Common reasons:
# - Validation failures
# - Missing user approval
# - Merge not completed

# Only force cleanup if task is genuinely abandoned
```

### Error: "Worktree removal failed"

```bash
# Check if worktree is in use
git worktree list

# If worktree has uncommitted changes, you'll see them
# Worktree removal uses --force to handle this

# Manual removal if needed:
git worktree remove --force /workspace/tasks/{task-name}/code
git worktree remove --force /workspace/tasks/{task-name}/agents/*/code
```

### Error: "Branch deletion failed"

```bash
# Check if branch exists
git branch | grep {task-name}

# Force delete if needed
git branch -D {task-name}
git branch -D {task-name}-architect
git branch -D {task-name}-tester
git branch -D {task-name}-formatter

# Check for protected branches
# (version branches like v21 should NOT be deleted)
```

### Partial Cleanup Recovery

```bash
# If cleanup partially failed, check what's left:

# List remaining worktrees
git worktree list | grep {task-name}

# List remaining branches
git branch | grep {task-name}

# Remove manually:
# 1. Worktrees
for worktree in $(git worktree list | grep {task-name} | awk '{print $1}'); do
  git worktree remove --force "$worktree"
done

# 2. Branches
for branch in $(git branch | grep {task-name}); do
  git branch -D "$branch"
done

# 3. Update state
jq '.state = "CLEANUP"' /workspace/tasks/{task-name}/task.json > tmp.json
mv tmp.json /workspace/tasks/{task-name}/task.json
```

## Performance Impact

**Expected Usage**: 1-3 times per day (per completed task)

**Time Savings per Use**: ~1-2 minutes (manual cleanup avoided)

**Disk Space Reclaimed**: ~50-200 MB per task (worktree code directories)

**Error Prevention**: 100% fewer "forgot to cleanup" issues

## Implementation Details

The task-cleanup.sh script performs these steps:

1. **Validation Phase**
   - Check task exists
   - Verify task in COMPLETE state
   - Confirm we're in main repository
   - Validate task merged to main

2. **State Transition Phase**
   - Update task.json to CLEANUP state
   - Record cleanup timestamp

3. **Worktree Removal Phase**
   - Remove task worktree (with --force)
   - Remove architect worktree (with --force)
   - Remove tester worktree (with --force)
   - Remove formatter worktree (with --force)
   - Continue on errors (best-effort)

4. **Branch Deletion Phase**
   - Delete main task branch
   - Delete architect branch
   - Delete tester branch
   - Delete formatter branch
   - Skip version branches (protection)
   - Continue on errors (best-effort)

5. **Verification Phase**
   - Verify worktrees removed
   - Verify branches deleted
   - Verify audit files preserved
   - Report any failures

6. **Reporting Phase**
   - Return JSON with complete status
   - List removed worktrees
   - List deleted branches
   - Indicate preserved artifacts
