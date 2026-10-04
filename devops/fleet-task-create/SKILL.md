---
name: fleet-task-create
description: >
  Create a follow-up task for yourself or another agent when you discover
  work that is separate from your current task. Properly references the
  parent task, sets project tags, and notifies via board memory and IRC.
  Triggers on: "create task", "follow up task", "fleet task create",
  "new task for", "propose task".
user-invocable: true
---

# Fleet Task Creator

Create well-formed follow-up tasks when you discover work separate from your current task.

## When to Use

You're working on task A and discover that:
- There's a bug that's not part of task A → create a fix task
- Documentation is missing → create a docs task
- Tests are missing → create a test task
- An architecture concern needs review → create a review task
- Infrastructure needs updating → create an infra task

**Do NOT create tasks for sub-steps of your current work.** Only for SEPARATE work.

## How to Create

### Step 1: Determine the right agent

| Work Type | Agent |
|-----------|-------|
| Code implementation, bug fix | software-engineer |
| Architecture review, design | architect |
| Tests, quality checks | qa-engineer |
| Documentation | technical-writer |
| Infrastructure, CI/CD | devops |
| UI/UX design | ux-designer |
| Accountability systems | accountability-generator |

### Step 2: Create the task via MC API

```bash
PARENT_TASK_ID="{your current task ID}"
TARGET_AGENT_ID="{agent MC ID — look up from MC API or TOOLS.md}"

curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/tasks" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title": "{clear, specific title}",
    "description": "{detailed description with context from your current work}\n\nSpawned from: [task:{parent_task_short}]({parent_task_url})",
    "status": "inbox",
    "priority": "{low|medium|high|urgent}",
    "assigned_agent_id": "{target_agent_id}",
    "depends_on_task_ids": ["{parent_task_id}"],
    "custom_field_values": {
      "project": "{project_name}"
    },
    "tag_ids": ["{project_tag_id}", "{type_tag_id}"]
  }'
```

### Step 3: Notify via board memory

```bash
curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/memory" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "content": "## 📋 Proposed Task: {title}\n\n**For:** @{target_agent}\n**From:** {your_name}\n**Project:** {project}\n**Spawned from:** [{parent_task_title}]({parent_task_url})\n\n### Context\n{why this task is needed}\n\n---\nTags: proposed, project:{project}",
    "tags": ["proposed", "project:{project}"],
    "source": "{your_agent_name}"
  }'
```

### Step 4: Notify IRC

```bash
bash scripts/notify-irc.sh --agent "{your_name}" --event "PROPOSED TASK" --title "{title} for @{target_agent}" --url "{parent_task_url}"
```

### Step 5: Note in your current task comment

In your next progress or completion comment, mention:
```
**Follow-up created:** [{new_task_title}]({new_task_url}) for @{target_agent}
```

## Rules

- **ALWAYS** reference the parent task in the new task description
- **ALWAYS** set project custom field and tags
- **ALWAYS** notify board memory and IRC
- **ALWAYS** note the follow-up in your current task comment
- Title must be **specific and actionable** — not "fix stuff"
- Description must include **context** — why this task exists, what you found
- Priority should match the severity of what you found