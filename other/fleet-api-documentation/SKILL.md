---
name: fleet-api-documentation
description: How the technical writer documents APIs — endpoint reference, request/response examples, error codes, authentication, and the context that turns a reference into a guide
user-invocable: false
---

# API Documentation

## What Makes API Docs Good

Bad API docs list endpoints. Good API docs help someone accomplish a task.

The difference:
- **Bad:** `POST /api/tasks — Creates a task`
- **Good:** `POST /api/tasks — Creates a task with required fields.
  The task starts in inbox state. Set task_type and delivery_phase
  to determine methodology requirements. Returns the created task
  with generated ID and initial state.`

## Documentation Layers

### Layer 1: Quick Reference
For the developer who knows the API and needs a reminder.

```
## POST /api/tasks
Creates a task.
Body: { title, description, task_type, delivery_phase, ... }
Returns: 201 { task }
Errors: 400 (validation), 401 (auth), 409 (duplicate)
```

### Layer 2: Full Reference
For the developer integrating for the first time.

```
## POST /api/tasks

Creates a new task in inbox state.

### Request
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | yes | Task title (max 200 chars) |
| description | string | no | Detailed description |
| task_type | enum | yes | epic/story/task/subtask/bug/spike/blocker |
| delivery_phase | enum | yes | poc/mvp/staging/production |
| agent_name | string | no | Assign to agent (null = unassigned) |
| parent_task | uuid | no | Parent task ID |
| story_points | int | no | 1/2/3/5/8/13 |

### Response (201)
{json example with all fields, annotated}

### Errors
| Code | Condition | Body |
|------|-----------|------|
| 400 | Missing required field | { "error": "title is required" } |
| 401 | Missing/invalid auth | { "error": "unauthorized" } |
| 409 | Duplicate title in sprint | { "error": "task already exists" } |
```

### Layer 3: Guide
For the developer who needs to understand HOW to use the API.

```
## Creating Tasks

Tasks flow through a lifecycle: inbox → accepted → in_progress → review → done.

To create a task:
1. POST /api/tasks with required fields
2. The task starts in inbox state
3. PM triages: sets fields, assigns agent
4. Agent accepts: POST /api/tasks/{id}/accept with plan
5. ...

### Common patterns:
- Creating an epic with subtasks: {example}
- Creating a contribution task: {example}
- Creating a bug from a failed review: {example}
```

## Fleet API Specifics

### Mission Control API
- Base URL: `http://localhost:8000`
- Auth: gateway token in header
- Endpoints documented in: `vendor/openclaw-mission-control/`

### MCP Tools (Agent-Facing)
- Not REST — tool calls via MCP protocol
- Each tool has: name, description, parameters, return value
- Documented in: `fleet/mcp/tools.py` docstrings + TOOLS.md per agent

### Gateway API
- WebSocket: `ws://localhost:18789`
- Agent sessions, heartbeats, CRONs
- Documented in: gateway-automation-capabilities.md

## Documentation Quality Checklist

For each endpoint or tool:
- [ ] Purpose is clear (what it does AND why you'd use it)
- [ ] All parameters documented with types and constraints
- [ ] Response format with example
- [ ] Error cases listed with codes and messages
- [ ] Authentication requirements stated
- [ ] Rate limits or constraints noted
- [ ] At least one complete request/response example
- [ ] Related endpoints cross-referenced

## Staleness Detection

API docs go stale when:
- New parameters added but docs not updated
- Error codes change
- Response format evolves
- Endpoints deprecated

The writer should periodically diff the actual API against the docs.
Use the `writer_staleness_scan` group call to automate this.
