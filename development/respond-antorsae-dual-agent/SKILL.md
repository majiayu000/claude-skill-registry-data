---
name: respond
description: Manually write response back to Claude. Use if read-task did not auto-complete or to finalize response.
---

# Respond Skill

Manually write response back to Claude.

## When to Use

- If `/read-task` didn't auto-complete
- To finalize or modify a response
- To manually send findings to Claude

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

### 1. Gather Response

If task not yet completed, finish it now.

Collect all findings, code, or analysis.

### 2. Write Response

Write to `$AGENT_COLLAB_DIR/responses/response.md`:

```markdown
# Codex Response

## Task Type
[CODE_REVIEW | IMPLEMENT | PLAN_REVIEW]

## Completed At
[Current timestamp]

## Summary
[Brief summary]

## Detailed Findings/Output
[Full response content]
```

### 3. Update Status

Write `done` to `$AGENT_COLLAB_DIR/status`

### 4. Confirm

Tell user: "Response written. Claude can now use /codex-read to retrieve it."
