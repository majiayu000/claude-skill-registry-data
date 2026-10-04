---
name: fleet-gap
description: >
  Identify and report missing capabilities in the fleet: missing agents,
  skills, knowledge, automation, or documentation. Posts structured gap
  reports to board memory and IRC so the fleet evolves over time.
  Triggers on: "gap", "missing skill", "missing agent", "fleet gap",
  "we need", "we lack", "missing capability".
user-invocable: true
---

# Fleet Gap Detection

Identify what the fleet is missing. **The fleet should constantly evolve —
agents who notice gaps help it improve.**

## Gap Categories

| Category | Examples |
|----------|---------|
| **Missing agent** | "We need a database specialist agent for migration tasks" |
| **Missing skill** | "There's no skill for database migration — agents do it manually" |
| **Missing knowledge** | "No documentation about the NNRT pipeline architecture — agents keep re-discovering it" |
| **Missing automation** | "PR review is manual — should be triggered automatically on task→review" |
| **Missing documentation** | "No runbook for incident response" |
| **Missing tooling** | "No way to run integration tests across projects" |

## How to Report

### Post to board memory

Use `agents/_template/markdown/memory-suggestion.md` adapted for gaps:

```bash
curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/memory" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "content": "## 💡 Gap: {title}\n\n**From:** {agent_name}\n**Category:** {missing agent / skill / knowledge / automation / docs / tooling}\n\n### What I Noticed\n{concrete observation — what happened that revealed the gap}\n\n### What\u0027s Missing\n{specific capability that doesn\u0027t exist}\n\n### Impact\n{what this gap causes — wasted time, errors, manual work}\n\n### Suggested Resolution\n{what would fix it — new agent, new skill, new doc, new script}\n\n### Effort Estimate\n{low / medium / high}\n\n---\nTags: gap, {category}, project:{project}",
    "tags": ["gap", "{category}", "project:{project}"],
    "source": "{agent_name}"
  }'
```

### Post to IRC

```bash
bash scripts/notify-irc.sh --agent "{agent_name}" --event "GAP" --title "{what's missing}" --url "{relevant_url_if_any}"
```

### Optionally create a proposed task

If the gap is concrete enough to act on, use fleet-task-create to propose a task.

## When to Report Gaps

- **While working:** You hit a wall because something doesn't exist
- **After completing a task:** You reflect on what would have made it easier
- **During review:** You see another agent's work and notice a pattern of gaps
- **On heartbeat:** Periodic check — "what could be better?"

## Good Gap Reports

**Good:**
```
## 💡 Gap: No database migration skill

**From:** software-engineer
**Category:** missing skill

### What I Noticed
While working on NNRT task [task:3402f526], I needed to modify the schema
but had to manually write Alembic migration commands. Other ORMs and
migration tools also lack skill support.

### What's Missing
A skill that guides agents through database migration workflows:
creating migrations, reviewing them, applying them safely.

### Impact
Every database task requires agents to re-learn migration patterns.
Risk of incorrect migrations that break data.

### Suggested Resolution
Create a `fleet-db-migrate` skill covering Alembic, Django migrations,
and raw SQL migration patterns.

### Effort Estimate
Medium — skill definition + templates for each migration tool
```

**Bad:**
```
We need a database skill.
```

## Rules

- **Be specific** — "we need X" with evidence from real work
- **Include impact** — why does this gap matter
- **Suggest resolution** — don't just complain, propose a fix
- **Don't duplicate** — check board memory for existing gap reports first
- **Tag properly** — gap, {category}, project:{name}