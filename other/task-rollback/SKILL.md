---
name: task-rollback
description: Reverts the last task's file changes using git. Reads task history for modified files and git reference, shows a preview, requires user confirmation, then reverts and updates the index.
---

# Task Rollback - Undo Last Task

Reverts file changes made by the most recent `/crew task` execution using git.

## When to Activate

- User runs `/crew rollback`

## Prerequisites

- `.claude/crew-history.json` must exist with at least one entry
- Project must be a git repository
- The `gitRefBefore` field should be present in the last history entry (captured by execution-orchestrator before task execution)

If history is missing: "No task history found. Nothing to roll back."
If not a git repo: "Not a git repository. Rollback requires git."

## Rollback Process

### Step 1: Read Last Task

Read `.claude/crew-history.json` and get the last entry:
- Extract `filesModified` — the files that were changed
- Extract `gitRefBefore` — the git commit hash before the task started
- Extract `task` — the original task description
- Extract `timestamp` — when the task ran

### Step 2: Show Preview

Display what will be rolled back:

```
Rollback: "{task}" ({timestamp})
  Files: {file1}, {file2}, {file3}
  Revert to: {gitRefBefore}
```

### Step 3: Ask for Confirmation

**This is mandatory — never skip confirmation.**

Ask: "Proceed with rollback? (y/n)"

If user says no: "Cancelled."

### Step 4: Execute Rollback

Two strategies based on available data:

**Strategy A: gitRefBefore is available (preferred)**
```bash
git checkout {gitRefBefore} -- {file1} {file2} {file3}
```
This reverts only the specific files to their pre-task state without affecting other changes.

**Strategy B: gitRefBefore is not available (fallback)**
```bash
git diff HEAD -- {file1} {file2} {file3}  # Show what will change
git checkout HEAD~1 -- {file1} {file2} {file3}  # Revert to previous commit
```
Warning: This is less precise — only works if the task's changes are in the most recent commit.

**If files have been modified since the task** (additional changes on top):
- Warn the user: "Warning: {file} has been modified since the task. Rolling back will also undo those changes."
- Ask for confirmation again

### Step 5: Update Index

After rollback:
1. Invoke the `index-updater` skill for all reverted files
2. This ensures the index reflects the rolled-back state

### Step 6: Update History

Mark the last task entry in history:
```json
{
  "...existing fields...",
  "rolledBack": true,
  "rolledBackAt": "2026-04-04T13:00:00Z"
}
```

### Step 7: Report

```
Rolled back {count} files. Index updated.
```

## Safety Rules

- **Always show preview and ask for confirmation** — never auto-rollback
- **Only rollback the most recent task** by default
- **Warn about subsequent modifications** to the same files
- **If gitRefBefore is missing**, warn that the rollback may be imprecise
- **Never force-push or reset** — only checkout specific files
