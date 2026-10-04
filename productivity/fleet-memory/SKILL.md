---
name: fleet-memory
description: >
  Post properly tagged and formatted entries to MC board memory. Use for
  alerts, decisions, suggestions, knowledge sharing, and PR notifications.
  Board memory is the fleet's persistent knowledge base — cross-task,
  cross-agent, searchable.
  Triggers on: "post memory", "fleet memory", "board memory", "alert",
  "decision record", "suggestion".
user-invocable: true
---

# Fleet Board Memory

Post structured entries to MC board memory. **Board memory is for information
that spans tasks — not for task-specific updates (use fleet-comment for those).**

## When to Use Board Memory

| Situation | Template | Required Tags |
|-----------|----------|---------------|
| Security/quality/architecture concern | memory-alert.md | alert, {severity}, {category}, project:{name} |
| Decision made that affects the project | memory-decision.md | decision, project:{name} |
| Improvement idea | memory-suggestion.md | suggestion, {area} |
| PR ready for review | (inline) | pr, review, project:{name} |
| Knowledge for other agents | (inline) | knowledge, project:{name} |

## Templates

All templates are in `agents/_template/markdown/`:
- `memory-alert.md` — security, quality, architecture alerts
- `memory-decision.md` — decision records with rationale and alternatives
- `memory-suggestion.md` — improvement proposals

## How to Post

```bash
# Build the content using the appropriate template
CONTENT="..."
TAGS='["alert", "high", "security", "project:nnrt"]'

curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/memory" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d "{\"content\": \"$CONTENT\", \"tags\": $TAGS, \"source\": \"{agent_name}\"}"
```

## Tag Taxonomy

**EVERY board memory entry MUST have tags. No exceptions.**

### Type tags (at least one required)
- `alert` — something needs attention
- `decision` — a decision was made
- `suggestion` — improvement proposed
- `knowledge` — information for other agents
- `report` — status report or digest
- `pr` — PR notification

### Scope tags (at least one required)
- `project:{name}` — project-specific (nnrt, fleet, aicp)
- `fleet` — fleet-wide
- `workflow` — workflow/process related
- `tooling` — tools and automation

### Severity tags (required for alerts)
- `critical` — needs immediate human action
- `high` — needs action soon
- `medium` — should be addressed
- `low` — nice to know

### Category tags (recommended for alerts)
- `security` — CVE, secrets, auth, vulnerabilities
- `quality` — tests, coverage, code smells
- `architecture` — design, coupling, scaling
- `workflow` — process, automation gaps
- `tooling` — missing tools, broken automation

## Rules

- **ALWAYS** include tags — untagged entries are useless
- **ALWAYS** use a template for alerts, decisions, and suggestions
- **NEVER** post task-specific updates to board memory (use task comments)
- **DO** post PR notifications to board memory (cross-agent awareness)
- **DO** post when you find something that affects other agents or the fleet
- Cross-reference with URLs (use fleet-urls skill)