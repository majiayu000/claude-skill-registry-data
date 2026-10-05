---
name: task-management
description: Use when an agent needs current internal task, project, TODO, owner, deadline, follow-up, or progress context from the CEO agent service. It provides read-only local HTTP API lookup instructions for task context.
metadata:
  category: productivity
  stability: local
  requires:
    service: ceo-agent-service audit web on http://127.0.0.1:8765
---

# Task Management

Use this skill when a conversation asks about internal projects, tasks, TODOs,
owners, deadlines, status, blockers, follow-ups, task detail links, or progress
and the visible chat context is not enough.

## Read-only API

The local CEO agent service exposes task context as JSON:

```bash
curl -sS --get 'http://127.0.0.1:8765/api/task-management/search' \
  --data-urlencode 'q=<message text or project/task keywords>' \
  --data-urlencode 'conversation_id=<open conversation id if known>' \
  --data-urlencode 'owner_user_id=<sender or owner user id if known>' \
  --data-urlencode 'limit=3'
```

To fetch one project exactly:

```bash
curl -sS 'http://127.0.0.1:8765/api/task-management/projects/<project_id>'
```

## Result Use

- Treat API results as read-only evidence from the service database.
- Prefer matches supported by `match.reasons`, the conversation title, sender,
  message text, and owner fields.
- Use `project.detail_url`, `todo.detail_url`, and follow-up `detail_url` when a
  reply should point a user to the UI.
- If multiple returned projects are plausible and the exact task still cannot
  be identified, ask a clarifying question instead of guessing.
- Do not mutate tasks through this API. Task creation or updates still belong to
  the task agent or service workflow.
