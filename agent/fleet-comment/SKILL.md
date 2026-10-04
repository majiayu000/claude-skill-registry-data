---
name: fleet-comment
description: >
  Post structured, formatted task comments to Mission Control. Use for
  acceptance, progress, completion, and blocker updates. Produces properly
  formatted markdown with cross-references and URLs.
  Triggers on: "post comment", "update task", "fleet comment", "task update".
user-invocable: true
---

# Fleet Task Comment

Post properly structured comments to MC tasks. **Use this instead of raw curl.**

## Comment Types

### Acceptance (starting work)

Use template: `agents/_template/markdown/comment-progress.md`

```
## ▶️ Accepted

**Plan:** {brief description of approach}
**Estimated scope:** {files/areas to touch}

---
<sub>{agent_name} · [{task_short}]({task_url})</sub>
```

### Progress Update

Use template: `agents/_template/markdown/comment-progress.md`

### Completion

Use template: `agents/_template/markdown/comment-completion.md`

**All URLs must be resolved using fleet-urls skill.**

### Blocker

Use template: `agents/_template/markdown/comment-blocker.md`

## How to Post

```bash
# Read TOOLS.md values
BASE_URL="..."   # from TOOLS.md
AUTH_TOKEN="..."  # from TOOLS.md
BOARD_ID="..."    # from TOOLS.md
TASK_ID="..."     # from task assignment

# Build the comment body using the appropriate template
COMMENT="..."

# Post
curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/tasks/$TASK_ID/comments" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d "{\"message\": \"$COMMENT\"}"
```

## Rules

- **EVERY** comment must use a template — no freeform text dumps
- **EVERY** comment must end with the agent/task footer
- **EVERY** reference must be a clickable URL (use fleet-urls skill)
- Completion comments MUST include: PR link, branch link, file list, commit list
- Blocker comments MUST include: reason, impact, needed action
- Keep it SCANNABLE — a reviewer should understand in 5 seconds