---
name: session-protocol
description: Session management protocol. Use for saving and loading session state.
---

# Session Protocol

## 1. Session State Location

```
.claude/session-state.json
```

**DO NOT commit this file** - it's local workspace state.

## 2. Session State Format (FULL)

```json
{
  "mode": "quick|sync|full",
  "saved_at": "2025-12-06T11:30:00",
  "git_commit": "abc1234",
  "git_pushed": true,
  "openspec": "00027",
  "openspec_status": "PENDING|IN_PROGRESS|DEPLOYED",
  "working_on": "Brief description of current work",
  "next_steps": ["Step 1", "Step 2"],
  "blocker": {
    "type": "vscode_terminal|build_error|test_failure|other",
    "description": "What is blocking progress",
    "resolution": "How to resolve it",
    "appeared_after": "Context when blocker appeared"
  },
  "implementation_status": "IN_PROGRESS|COMPLETE|BLOCKED",
  "completed_tasks": [
    "Task description 1",
    "Task description 2"
  ],
  "pending_tasks": [
    "Task description 3",
    "Task description 4"
  ],
  "task_progress": {
    "completed": 17,
    "total": 22,
    "percentage": 77
  }
}
```

### Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| mode | ✅ | Save mode: quick, sync, full |
| saved_at | ✅ | ISO timestamp of save |
| git_commit | ✅ | Last commit hash (null if none) |
| git_pushed | ✅ | Whether pushed to remote |
| openspec | ✅ | Current OpenSpec number |
| openspec_status | ✅ | OpenSpec status |
| working_on | ✅ | Brief description of work |
| next_steps | ✅ | Array of next actions |
| blocker | ❌ | Object describing any blockers |
| implementation_status | ❌ | Overall implementation status |
| completed_tasks | ❌ | Array of completed task descriptions |
| pending_tasks | ❌ | Array of pending task descriptions |
| task_progress | ❌ | Progress tracking object |

## 3. Save Modes

| Mode | Duration | Use Case |
|------|----------|----------|
| **quick** | ~15s | Hourly checkpoints, WIP, before risky changes |
| **sync** | ~30s | End of day, subtask complete |
| **full** | ~4min | Task/phase complete, milestone |

## 4. Integration with OpenSpec

When tracking status (`status taska`):
1. Read session-state.json first (if exists)
2. Cross-reference with active OpenSpec
3. Report both session state and task progress

When closing task (`zamknij task`):
1. Verify OpenSpec completeness
2. Suggest `/save-session --full` after successful close

## 5. Commands

- `/save-session` - Save current state (see save-session.md for details)
- `/load-session` - Restore previous state (see load-session.md for details)

## 6. Key Rules

2. **OpenSpec = truth for tasks** - Session state only tracks "where we are"
3. **Always suggest save** - Before ending work, remind about `/save-session`
4. **Gap detection** - On load, check for commits made outside sessions
5. **Track blockers** - Always document blockers with resolution steps
6. **Track progress** - Use completed_tasks/pending_tasks for detailed tracking
