---
name: codex-status
description: Check the current status of Codex collaboration. Use when user says codex status, check codex, or collaboration status.
---

# Codex Status Skill

Check the current state of the Claude-Codex collaboration.

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
- `idle`: No active task, ready for requests
- `pending`: Task sent, waiting for Codex
- `working`: Codex actively processing
- `done`: Codex finished, response ready

### 2. Show Current Task

If status is not `idle`, read and summarize `$AGENT_COLLAB_DIR/requests/task.md`:
- Task type
- Brief description

### 3. Show Response Preview

If status is `done`, show brief preview of `$AGENT_COLLAB_DIR/responses/response.md`

### 4. Suggest Action

Based on status:
- `idle`: Ready to delegate with /codex-review, /codex-implement, or /codex-plan-review
- `pending`: Check Codex pane or wait
- `working`: Codex is working, wait for completion
- `done`: Use /codex-read to see results
