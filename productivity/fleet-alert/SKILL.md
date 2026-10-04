---
name: fleet-alert
description: >
  Raise a proactive alert when you notice a security vulnerability, quality
  issue, missing capability, workflow problem, or architecture concern.
  Routes to the correct surfaces based on severity: IRC, board memory,
  and optionally task blocker.
  Triggers on: "alert", "warning", "security issue", "fleet alert",
  "raise alert", "cve", "vulnerability".
user-invocable: true
---

# Fleet Alert

Raise alerts when you notice problems the fleet or human should know about.

## Severity Routing

| Severity | Board Memory | IRC #alerts | IRC #fleet | Task Blocker |
|----------|-------------|-------------|------------|--------------|
| 🔴 Critical | ✅ | ✅ | ✅ | ✅ (if task-related) |
| 🟠 High | ✅ | ✅ | — | Optional |
| 🟡 Medium | ✅ | — | ✅ | — |
| 🟢 Low | ✅ | — | — | — |

## Alert Categories

| Category | Examples |
|----------|---------|
| **security** | CVE in dependency, exposed secret in code, auth bypass, insecure config |
| **quality** | No tests for critical module, <50% coverage, code smell, missing validation |
| **architecture** | Tight coupling, scaling concern, design debt, circular dependency |
| **workflow** | Broken automation, manual step that should be scripted, missing tooling |
| **tooling** | Missing skill, agent can't complete task due to tool gap, broken script |

## How to Alert

### Step 1: Post to board memory

Use template `agents/_template/markdown/memory-alert.md`:

```bash
curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/memory" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "content": "## ⚠️ {severity}: {title}\n\n**Project:** {project}\n**Found by:** {agent_name}\n**Severity:** {severity}\n**Category:** {category}\n\n### Details\n{evidence with URLs}\n\n### Recommended Action\n{what should be done}\n\n### References\n- {urls}\n\n---\nTags: alert, {severity}, {category}, project:{project}",
    "tags": ["alert", "{severity}", "{category}", "project:{project}"],
    "source": "{agent_name}"
  }'
```

### Step 2: Post to IRC (if severity warrants it)

```bash
# Critical → #alerts
bash scripts/notify-irc.sh --agent "{agent_name}" --event "CRITICAL" --title "{title}" --url "{reference_url}"

# High → #alerts
bash scripts/notify-irc.sh --agent "{agent_name}" --event "HIGH" --title "{title}" --url "{reference_url}"

# Medium → #fleet
bash scripts/notify-irc.sh --agent "{agent_name}" --event "MEDIUM" --title "{title}" --url "{reference_url}"
```

### Step 3: If task-related and critical, add blocker

```bash
curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/tasks/$TASK_ID/comments" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{"message": "## 🚫 Blocked by Alert\n\n**Alert:** {title}\n**Severity:** {severity}\n\n{details}\n\nThis task cannot safely proceed until the alert is resolved."}'
```

### Step 4: Optionally create a remediation task

If the alert requires specific work, use fleet-task-create to propose a task.

## What to Include in Alerts

**Good alert:**
```
## ⚠️ HIGH: NNRT dependency `pydantic` has known CVE-2024-XXXXX

**Project:** nnrt
**Severity:** high
**Category:** security

### Details
`pydantic==2.5.0` in pyproject.toml has CVE-2024-XXXXX (arbitrary code execution
via crafted JSON). See: https://nvd.nist.gov/vuln/detail/CVE-2024-XXXXX

### Recommended Action
Upgrade to `pydantic>=2.5.3` which patches the vulnerability.

### References
- [pyproject.toml](https://github.com/cyberpunk042/Narrative-to-Neutral-Report-Transformer/blob/main/pyproject.toml)
- [CVE-2024-XXXXX](https://nvd.nist.gov/vuln/detail/CVE-2024-XXXXX)
```

**Bad alert:**
```
Found a security issue in the project.
```

## Rules

- **Be specific** — include evidence, file paths (as URLs), CVE IDs
- **Be actionable** — say what should be done, not just what's wrong
- **Use the right severity** — critical means "stop and fix NOW"
- **Don't alert for known issues** — check board memory first
- **Include references** — URLs to files, CVEs, docs, issues