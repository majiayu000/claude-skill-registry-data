---
name: claude-status
description: Check collaboration status from Codex side. Use when user says claude status, check status, or collaboration status.
---

# Claude Status Skill

Check the collaboration status from the Codex side.

## Steps

Before any file operations, resolve the `.agent-collab` directory so commands work outside the project root:

```bash
AGENT_COLLAB_DIR="${AGENT_COLLAB_DIR:-}"
if [ -n "$AGENT_COLLAB_DIR" ]; then
  if [ -d "$AGENT_COLLAB_DIR/.agent-collab" ]; then
    AGENT_COLLAB_DIR="$AGENT_COLLAB_DIR/.agent-collab"
  elif [ ! -d "$AGENT_COLLAB_DIR" ]; then
    AGENT_COLLAB_DIR=""
  fi
fi

if [ -z "$AGENT_COLLAB_DIR" ]; then
  AGENT_COLLAB_DIR="$(pwd)"
  while [ "$AGENT_COLLAB_DIR" != "/" ] && [ ! -d "$AGENT_COLLAB_DIR/.agent-collab" ]; do
    AGENT_COLLAB_DIR="$(dirname "$AGENT_COLLAB_DIR")"
  done
  AGENT_COLLAB_DIR="$AGENT_COLLAB_DIR/.agent-collab"
fi
```

If `$AGENT_COLLAB_DIR` does not exist, stop and ask for the project root.

### 1. Read Status

Read `$AGENT_COLLAB_DIR/status` and report:
- `idle`: No active task
- `pending`: Claude sent task, waiting for pickup with `/read-task`
- `working`: Currently processing a task
- `done`: Finished, waiting for Claude to read with `/codex-read`

### 2. Show Pending Task

If status is `pending`, read and summarize `$AGENT_COLLAB_DIR/requests/task.md`:
- What Claude is asking
- Task type
- Key details

### 3. Suggest Action

Based on status:
- `pending`: Run /read-task to pick up the task
- `working`: Continue working on current task
- `done`: Waiting for Claude - user should run /codex-read in Claude pane
- `idle`: No pending tasks, waiting for Claude to delegate
