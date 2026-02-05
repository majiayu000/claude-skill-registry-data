---
name: codex-read
description: Read and integrate response from Codex. Use when user says codex read, get codex response, or check codex results.
---

# Codex Read Skill

Read the response from Codex and integrate findings.

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

### 1. Check Status

Read `$AGENT_COLLAB_DIR/status`:
- `idle`: No pending task. Inform user.
- `pending`: Codex hasn't started. Check Codex pane.
- `working`: Codex still processing. Wait.
- `done`: Proceed to read response.

### 2. Read Response

Read `$AGENT_COLLAB_DIR/responses/response.md` and parse:
- Task type completed
- Findings/output
- Any code produced
- Recommendations

### 3. Present to User

Summarize clearly based on task type:

**For CODE_REVIEW:**
- Bugs/issues with severity
- Security concerns
- Performance issues
- Suggested improvements

**For IMPLEMENT:**
- What was implemented
- Approach taken
- Integration instructions

**For PLAN_REVIEW:**
- Critique summary
- Identified risks
- Alternative suggestions

### 4. Integrate (if applicable)

For implementations:
- Ask if user wants to integrate
- Apply changes if yes
- Run relevant tests

### 5. Reset Status

Write `idle` to `$AGENT_COLLAB_DIR/status`

### 6. Next Steps

Suggest appropriate follow-up:
- Reviews: Address issues found
- Implementations: Test and validate
- Plan reviews: Iterate on plan
