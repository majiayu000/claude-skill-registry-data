---
name: clickup
description: 'Use when skill: clickup. See SKILL.md body for details. Use when this
  domain is relevant.'
domain: operations
author: oyi77
license: Apache-2.0
subdomain: business-operations
tags:
- business-ops
- clickup
- management
- operations
version: 1.0.0
category: operations
---


## When to Use

**Trigger phrases:**
- "clickup"
- "clickup api"
- "task management", "project management"
- "automate tasks"
- "clickup workflow"
- "clickup webhook"

**Situations:**
- Automating task creation, updates, and status transitions via the ClickUp API
- Building integrations that read/write ClickUp tasks, lists, folders, or spaces
- Setting up webhook-driven workflows for real-time ClickUp event processing
- Managing sprints, dependencies, or time tracking programmatically
- Migrating from another tool (Jira, Asana, Trello) to ClickUp
- Bulk operations on tasks — updating custom fields, reassigning, batch status changes

**API version reference:** This skill targets the ClickUp REST API v2 (`/api/v2/`). The API base URL is `https://api.clickup.com/api/v2`.

## When NOT to Use

- Real-time collaborative editing of ClickUp Docs (the API does not support inline doc editing — only create/read)
- ClickUp automations that are simpler to configure in the UI (the built-in Automation module handles triggers/actions without code)
- Large-scale data migration without testing rate limits first (100 req/min per workspace)
- When the team uses a fundamentally different paradigm (e.g., linear kanban-only flow) — ClickUp is optimized for hierarchy (Workspace → Space → Folder → List → Task)
- For embedding ClickUp in a public-facing product (the API is designed for internal tooling, not customer-facing SaaS)

## Overview

ClickUp is a unified project management platform built on a hierarchical structure: **Workspace → Space → Folder → List → Task**. The REST API v2 exposes CRUD operations at every level, plus specialized endpoints for time tracking, goals, docs, dependencies, and custom fields.

**API base URL:** `https://api.clickup.com/api/v2`

**Authentication:** Pass API token via `Authorization: pk_XXXXXXXX` header, or use OAuth 2.0 for user-installed integrations.

**Key design constraints:**
- Rate limit: **100 requests per minute** per workspace. Exceeding this returns HTTP 429 with a `Retry-After` header.
- All task IDs, list IDs, folder IDs, and space IDs are **workspace-scoped** — never assume IDs are global.
- The hierarchy path from Workspace down to Task is required for most write operations. Many endpoints accept either the location ID (list/folder/space) or a direct task ID.
- ClickUp uses **statuses** as strings, but they must match exactly the status names configured in the workspace (case-sensitive).

### Hierarchy Map

```
Workspace (team_id)
└── Space (space_id)
    ├── Folder (folder_id)
    │   └── List (list_id)
    │       └── Task (task_id)
    └── List (list_id) — a list can exist directly in a space without a folder
        └── Task (task_id)
```

Tasks can optionally have:
- **Subtasks** — child tasks linked to a parent
- **Checklists** — inline checklists within a task
- **Dependencies** — blocking/blocked-by relationships between tasks
- **Custom Fields** — typed fields (text, number, date, dropdown, labels, etc.)
- **Time Estimates & Time Tracked** — duration tracking per task

## Authentication

### API Token (Recommended for server-side automation)

1. Go to ClickUp Settings → ClickUp API → Generate API Token
2. The token is a string starting with `pk_`
3. Pass it in every request as a header:

```
Authorization: pk_XXXXXXXXXXXXXX
```

The API token has the same permissions as the user who generated it.

### OAuth 2.0 (For multi-user integrations)

OAuth is required if your integration will be installed by multiple ClickUp users (e.g., a marketplace app).

1. Register an app in ClickUp Settings → Integrations → OAuth Apps
2. Redirect URI: `https://your-app.com/oauth/callback`
3. Request URL: `https://app.clickup.com/api?client_id=CLIENT_ID&redirect_uri=REDIRECT_URI`
4. Token exchange: `POST https://api.clickup.com/api/v2/oauth/token` with `client_id`, `client_secret`, `code`

The OAuth token is used identically to an API token (passed as `Authorization: Bearer <token>`).

## Workflow

### 1. Identify Workspace Context

Before any API call, resolve the workspace and location IDs.

```python
# Get authenticated user's workspaces
import requests

API_TOKEN = "pk_xxxxxxxx"
HEADERS = {"Authorization": API_TOKEN}

resp = requests.get("https://api.clickup.com/api/v2/team", headers=HEADERS)
teams = resp.json()["teams"]
# teams[0]["id"] is your workspace_id
```

### 2. Resolve Space / Folder / List IDs

Map from names to IDs. Collect these once and cache them (they rarely change).

```python
def get_spaces(workspace_id: str) -> list[dict]:
    resp = requests.get(
        f"https://api.clickup.com/api/v2/team/{workspace_id}/space",
        headers=HEADERS
    )
    return resp.json()["spaces"]

def get_folders(space_id: str) -> list[dict]:
    resp = requests.get(
        f"https://api.clickup.com/api/v2/space/{space_id}/folder",
        headers=HEADERS
    )
    return resp.json()["folders"]

def get_lists(folder_id: str) -> list[dict]:
    resp = requests.get(
        f"https://api.clickup.com/api/v2/folder/{folder_id}/list",
        headers=HEADERS
    )
    return resp.json()["lists"]
```

### 3. Execute Task Operations

Create, read, update, delete, and query tasks.

### 4. Verify

Confirm the operation via the ClickUp UI or a GET request.

## Core API Endpoints

### Tasks

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v2/task/{task_id}` | Get a single task |
| `POST` | `/api/v2/list/{list_id}/task` | Create a task in a list |
| `PUT` | `/api/v2/task/{task_id}` | Update a task |
| `DELETE` | `/api/v2/task/{task_id}` | Delete a task |
| `GET` | `/api/v2/list/{list_id}/task` | Get tasks in a list (with filters) |
| `POST` | `/api/v2/task/{task_id}/checklist/{checklist_id}/checklist_item` | Add checklist item |
| `POST` | `/api/v2/task/{task_id}/link` | Create task dependency |

### Lists, Folders, Spaces

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v2/list/{list_id}` | Get list details |
| `POST` | `/api/v2/folder/{folder_id}/list` | Create a list |
| `PUT` | `/api/v2/list/{list_id}` | Update a list |
| `GET` | `/api/v2/space/{space_id}` | Get space details |
| `PUT` | `/api/v2/space/{space_id}` | Update space |

### Time Tracking

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v2/task/{task_id}/time` | Get time entries for a task |
| `POST` | `/api/v2/task/{task_id}/time` | Add time entry |
| `PUT` | `/api/v2/time/{time_entry_id}` | Update time entry |
| `DELETE` | `/api/v2/time/{time_entry_id}` | Delete time entry |

### Goals (formerly OKRs)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v2/team/{team_id}/goal` | List goals in workspace |
| `POST` | `/api/v2/team/{team_id}/goal` | Create a goal |
| `PUT` | `/api/v2/goal/{goal_id}` | Update a goal |
| `POST` | `/api/v2/goal/{goal_id}/key_result` | Add a key result to a goal |

### Custom Fields

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v2/list/{list_id}/field` | Get custom fields for a list |
| `POST` | `/api/v2/task/{task_id}/field/{field_id}` | Set a custom field value |

### Dependencies

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/v2/task/{task_id}/link` | Link tasks with dependency |
| `DELETE` | `/api/v2/task/{task_id}/link/{links_to}` | Remove a dependency link |

### Webhooks

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v2/team/{team_id}/webhook` | List registered webhooks |
| `POST` | `/api/v2/team/{team_id}/webhook` | Create a webhook |
| `DELETE` | `/api/v2/webhook/{webhook_id}` | Delete a webhook |

## Code Examples

### Python — Create a Task with Custom Fields

```python
import requests
import json

API_TOKEN = "pk_xxxxxxxx"
LIST_ID = "901234567890"
HEADERS = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

def create_task(list_id: str, name: str, description: str = "",
                assignees: list[int] | None = None,
                priority: int | None = None,
                due_date: int | None = None,
                custom_fields: list[dict] | None = None) -> dict:
    """Create a ClickUp task.
    
    Args:
        list_id: ID of the target list
        name: Task name (required)
        description: Markdown task description
        assignees: List of ClickUp user IDs
        priority: 1 (urgent), 2 (high), 3 (normal), 4 (low)
        due_date: Unix timestamp in milliseconds
        custom_fields: List of {id, value} dicts
    """
    payload = {"name": name}
    if description:
        payload["description"] = description
    if assignees:
        payload["assignees"] = assignees
    if priority:
        payload["priority"] = priority
    if due_date:
        payload["due_date"] = due_date

    resp = requests.post(
        f"https://api.clickup.com/api/v2/list/{list_id}/task",
        headers=HEADERS,
        json=payload
    )
    resp.raise_for_status()
    task = resp.json()

    # Set custom fields after creation
    if custom_fields:
        for field in custom_fields:
            set_custom_field(task["id"], field["id"], field["value"])

    return task

def set_custom_field(task_id: str, field_id: str, value):
    """Set a single custom field value on a task."""
    resp = requests.post(
        f"https://api.clickup.com/api/v2/task/{task_id}/field/{field_id}",
        headers=HEADERS,
        json={"value": value}
    )
    resp.raise_for_status()

def update_task_status(task_id: str, status: str):
    """Transition a task to a new status.
    
    Status must match exactly (case-sensitive) the status name configured
    in the ClickUp workspace.
    """
    resp = requests.put(
        f"https://api.clickup.com/api/v2/task/{task_id}",
        headers=HEADERS,
        json={"status": status}
    )
    resp.raise_for_status()

# Usage
task = create_task(
    list_id=LIST_ID,
    name="Implement auth middleware",
    description="- Add JWT verification\n- Add rate limiting\n- Write tests",
    assignees=[123456],
    priority=2,
    due_date=int(pd.Timestamp("2026-08-15").timestamp() * 1000),
    custom_fields=[{"id": "abc123", "value": "backend"}]
)
print(f"Created task: {task['id']} — {task['url']}")
```

### Python — Query Tasks with Filters

```python
def get_tasks(list_id: str, status: str | None = None,
              assignee: int | None = None,
              page: int = 0) -> list[dict]:
    """Get tasks from a list with optional filters.
    
    ClickUp paginates at 100 tasks per page. Use `page` to iterate.
    """
    params = {"page": page, "order_by": "updated"}
    if status:
        params["statuses[0]"] = status
    if assignee:
        params["assignees[0]"] = str(assignee)

    resp = requests.get(
        f"https://api.clickup.com/api/v2/list/{list_id}/task",
        headers=HEADERS,
        params=params
    )
    resp.raise_for_status()
    return resp.json()["tasks"]

# Get all "in progress" tasks
tasks = get_tasks(LIST_ID, status="in progress")
for t in tasks:
    print(f"{t['id']}: {t['name']} (updated {t['date_updated']})")
```

### JavaScript / Node.js — Task Management

```javascript
const API_TOKEN = 'pk_xxxxxxxx';
const LIST_ID = '901234567890';
const BASE = 'https://api.clickup.com/api/v2';

async function clickupFetch(endpoint, options = {}) {
  const url = `${BASE}${endpoint}`;
  const resp = await fetch(url, {
    ...options,
    headers: {
      'Authorization': API_TOKEN,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (!resp.ok) {
    const body = await resp.text();
    throw new Error(`ClickUp API ${resp.status}: ${body}`);
  }
  return resp.json();
}

// Create a task
async function createTask({ name, description, assignees, priority, dueDate }) {
  return clickupFetch(`/list/${LIST_ID}/task`, {
    method: 'POST',
    body: JSON.stringify({
      name,
      description,
      assignees,
      priority,
      due_date: dueDate ? new Date(dueDate).getTime() : undefined,
    }),
  });
}

// Bulk status update
async function bulkUpdateStatus(taskIds, status) {
  const results = [];
  for (const id of taskIds) {
    const task = await clickupFetch(`/task/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
    results.push(task);
    // Respect rate limits: 100 req/min = 600ms between requests minimum
    await new Promise(r => setTimeout(r, 700));
  }
  return results;
}

// Usage
(async () => {
  const task = await createTask({
    name: 'Deploy staging environment',
    description: 'Configure CI/CD pipeline for staging',
    assignees: [123456],
    priority: 1,
  });
  console.log(`Created: ${task.id} — ${task.url}`);
})();
```

### Bash (curl) — Quick API Operations

```bash
API_TOKEN="pk_xxxxxxxx"
WORKSPACE_ID="12345678"
LIST_ID="901234567890"
BASE="https://api.clickup.com/api/v2"

# Get all spaces in a workspace
curl -s -H "Authorization: $API_TOKEN" \
  "$BASE/team/$WORKSPACE_ID/space" | jq '.spaces[] | {id, name}'

# Create a task
curl -s -X POST \
  -H "Authorization: $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Fix login bug","priority":1,"assignees":[123456]}' \
  "$BASE/list/$LIST_ID/task" | jq '{id, name, url}'

# Update task status
curl -s -X PUT \
  -H "Authorization: $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"in review"}' \
  "$BASE/task/9abc1234" | jq '.status.status'

# Add time entry (duration in milliseconds)
curl -s -X POST \
  -H "Authorization: $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"duration":3600000,"description":"Code review session"}' \
  "$BASE/task/9abc1234/time" | jq '.id'

# Delete a task
curl -s -X DELETE \
  -H "Authorization: $API_TOKEN" \
  "$BASE/task/9abc1234"
```

## Webhook Integration

ClickUp webhooks fire HTTP POST requests to your endpoint when specified events occur. They are registered per workspace.

### Registering a Webhook

```python
def register_webhook(workspace_id: str, endpoint_url: str,
                     events: list[str] | None = None) -> dict:
    """Register a ClickUp webhook.
    
    Events: taskCreated, taskUpdated, taskDeleted, taskStatusUpdated,
            taskPriorityUpdated, taskAssigneedUpdated, listCreated,
            listUpdated, listDeleted, folderCreated, folderUpdated,
            folderDeleted, spaceCreated, spaceUpdated, spaceDeleted,
            goalCreated, goalUpdated, goalDeleted, goalTargetCreated,
            goalTargetUpdated, goalTargetDeleted
    """
    payload = {
        "endpoint": endpoint_url,
        "events": events or ["taskCreated", "taskUpdated", "taskDeleted"]
    }
    resp = requests.post(
        f"https://api.clickup.com/api/v2/team/{workspace_id}/webhook",
        headers=HEADERS,
        json=payload
    )
    resp.raise_for_status()
    return resp.json()

# Register to receive all task changes
webhook = register_webhook("12345678", "https://my-app.com/clickup-webhook")
print(f"Webhook ID: {webhook['id']} — secret: {webhook.get('secret', 'N/A')}")
```

### Webhook Payload Structure

ClickUp sends the following JSON body via POST to your endpoint:

```json
{
  "webhook_id": "abc-123-def",
  "event": "taskUpdated",
  "task_id": "9abc1234",
  "history_items": [
    {
      "id": "12345",
      "type": 1,
      "field": "status",
      "before": {"status": "to do"},
      "after": {"status": "in progress"}
    }
  ]
}
```

### Verifying Webhook Signature

ClickUp signs webhook payloads with HMAC-SHA256 using the webhook secret returned during registration.

```python
import hmac
import hashlib

def verify_clickup_webhook(payload_body: bytes, signature: str,
                           secret: str) -> bool:
    """Verify a ClickUp webhook HMAC signature.
    
    The signature is in the X-Signature header of the webhook request.
    """
    expected = hmac.new(
        secret.encode(), payload_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

# In your web handler (Fastify example):
# const signature = req.headers['x-signature'];
# const verified = verifySignature(JSON.stringify(req.body), secret, signature);
```

## Common Patterns

### Pattern 1: Sprint Management with Status Workflow

ClickUp does not have native "sprints" as a first-class concept. The pattern is to use a **list per sprint** or a **custom field for sprint name** with status transitions.

```python
def setup_sprint_list(workspace_id: str, space_id: str,
                      sprint_name: str) -> dict:
    """Create a sprint list inside a folder or space."""
    # 1. Create folder for the sprint cycle (optional)
    folder_resp = requests.post(
        f"https://api.clickup.com/api/v2/space/{space_id}/folder",
        headers=HEADERS,
        json={"name": f"Sprint {sprint_name}"}
    )
    folder = folder_resp.json()

    # 2. Create lists within the folder (Backlog, Current Sprint, Done)
    for list_name in ["Backlog", "Current Sprint", "Done"]:
        requests.post(
            f"https://api.clickup.com/api/v2/folder/{folder['id']}/list",
            headers=HEADERS,
            json={"name": list_name}
        )
    return folder

def move_task_to_sprint(task_id: str, sprint_list_id: str):
    """Move an existing task into a sprint list."""
    resp = requests.put(
        f"https://api.clickup.com/api/v2/task/{task_id}",
        headers=HEADERS,
        json={"list": {"id": sprint_list_id}}
    )
    resp.raise_for_status()
```

### Pattern 2: Task Dependencies

Tasks can be linked with "waiting on" / "blocking" relationships.

```python
def add_dependency(task_id: str, depends_on_id: str):
    """Make task_id depend on depends_on_id (task_id blocked by depends_on_id)."""
    resp = requests.post(
        f"https://api.clickup.com/api/v2/task/{task_id}/link",
        headers=HEADERS,
        json={
            "depends_on": depends_on_id,
            "depends_on_links_to": task_id
        }
    )
    resp.raise_for_status()

def get_dependent_tasks(task_id: str) -> dict:
    """Get dependency info for a task (included in the task response)."""
    resp = requests.get(
        f"https://api.clickup.com/api/v2/task/{task_id}",
        headers=HEADERS,
        params={"include": ["dependencies"]}
    )
    return resp.json().get("dependencies", {})
```

### Pattern 3: Time Tracking Automation

```python
def log_time(task_id: str, duration_minutes: int,
             description: str = "", billable: bool = True) -> dict:
    """Log time against a task.
    
    Duration is in milliseconds for the API.
    """
    duration_ms = duration_minutes * 60 * 1000
    resp = requests.post(
        f"https://api.clickup.com/api/v2/task/{task_id}/time",
        headers=HEADERS,
        json={
            "duration": duration_ms,
            "description": description,
            "billable": billable
        }
    )
    resp.raise_for_status()
    return resp.json()

def get_time_for_task(task_id: str) -> int:
    """Get total tracked time for a task in milliseconds."""
    resp = requests.get(
        f"https://api.clickup.com/api/v2/task/{task_id}/time",
        headers=HEADERS
    )
    entries = resp.json().get("data", [])
    return sum(e["duration"] for e in entries)
```

### Pattern 4: Permission Hierarchy Access

ClickUp permission levels cascade: **Workspace → Space → Folder → List → Task**. A user with access to a space automatically has access to all folders, lists, and tasks within it, unless restricted by sharing settings.

```python
def get_space_members(space_id: str) -> list[dict]:
    """Get all members of a space (includes all sub-folders/lists/tasks)."""
    resp = requests.get(
        f"https://api.clickup.com/api/v2/space/{space_id}",
        headers=HEADERS,
        params={"include": ["members"]}
    )
    return resp.json().get("members", [])
```

### Pattern 5: Bulk Operations with Rate Limit Handling

```python
import time

def bulk_update_tasks(tasks: list[dict], batch_size: int = 20):
    """Update multiple tasks with rate-limit awareness.
    
    Each update counts toward the 100 req/min per workspace limit.
    With n tasks and batch_size items per request (requires 1 req per task
    since ClickUp doesn't support batch update natively), space requests
    with batch_size × min_delay to stay under the limit.
    """
    results = []
    for i, task_update in enumerate(tasks):
        task_id = task_update.pop("id")
        resp = requests.put(
            f"https://api.clickup.com/api/v2/task/{task_id}",
            headers=HEADERS,
            json=task_update
        )
        resp.raise_for_status()
        results.append(resp.json())

        # Rate limit: 100 req/min → at most 1 req per 600ms
        # Be conservative: wait 700ms between writes
        if i < len(tasks) - 1:
            time.sleep(0.7)

    return results

def find_tasks_by_custom_field(list_id: str, field_id: str,
                               value) -> list[dict]:
    """Find tasks by a custom field value.
    
    ClickUp doesn't support filtering by custom field directly.
    Fetch all tasks and filter client-side.
    """
    tasks = []
    page = 0
    while True:
        resp = requests.get(
            f"https://api.clickup.com/api/v2/list/{list_id}/task",
            headers=HEADERS,
            params={"page": page, "order_by": "updated"}
        )
        batch = resp.json()["tasks"]
        if not batch:
            break
        for t in batch:
            cf = t.get("custom_fields", [])
            for f in cf:
                if f["id"] == field_id and f.get("value") == value:
                    tasks.append(t)
        page += 1
        time.sleep(0.35)  # read operations: 100 req/min → 600ms, reads half
    return tasks
```

### Pattern 6: Recurring Task Creation

```python
from datetime import datetime, timedelta

def create_recurring_tasks(list_id: str, base_name: str,
                           template: dict, weeks: int = 4) -> list[dict]:
    """Create a series of recurring tasks with offset due dates."""
    tasks = []
    for week in range(weeks):
        due = datetime.now() + timedelta(weeks=week)
        task_data = {
            "name": f"{base_name} — Week {week + 1}",
            "due_date": int(due.timestamp() * 1000),
            **template
        }
        resp = requests.post(
            f"https://api.clickup.com/api/v2/list/{list_id}/task",
            headers=HEADERS,
            json=task_data
        )
        resp.raise_for_status()
        tasks.append(resp.json())
        time.sleep(0.7)
    return tasks
```

## Red Flags

| Risk | Symptom | Mitigation |
|------|---------|------------|
| **Rate limit (HTTP 429)** | `"Rate limit exceeded"` with `Retry-After` header | Implement exponential backoff. Start with 700ms between write requests, 350ms between reads. Cache list/folder/space IDs. |
| **Stale API token** | HTTP 401 after token regeneration | Rotate tokens in a shared config (env var, vault) and restart any long-running processes. |
| **Wrong workspace ID** | HTTP 404 on team endpoints | The `team_id` is the workspace ID from `/team` endpoint. Always resolve dynamically rather than hardcoding. |
| **Invalid status name** | HTTP 400 "Invalid status" | Statuses are case-sensitive and must match exactly what's configured in the ClickUp workspace. Use `GET /list/{id}` to fetch available statuses. |
| **Assignee not in workspace** | HTTP 400 on assignee field | Verify user IDs belong to the workspace membership list before assigning. |
| **Missing custom field** | HTTP 400 "Field not found" | Custom field IDs are list-scoped. Fetch valid fields with `GET /list/{list_id}/field` before referencing them. |
| **Task moved to different list** | Task returns with different list_id | Always re-fetch the task before updating, or pass `list` in the update payload. |
| **Webhook secret changes** | Signature verification fails | Webhook secret is returned only at creation. Store it securely immediately. If lost, delete and re-create the webhook. |
| **Nested subtask depth limit** | Can't create subtask of subtask | ClickUp allows only one level of subtasks. Use checklists for deeper nesting within a subtask. |
| **ID type confusion** | Mixing up task vs. list vs. folder IDs | Prefix or track the type alongside the ID in your code. A task ID and a list ID can look identical (numeric string). |
| **Markdown in descriptions** | Formatting not rendering | ClickUp accepts markdown in descriptions. Test your markdown rendering — ClickUp's parser may differ from GitHub's. |

## Verification

- [ ] API token authenticates successfully (`GET /team` returns workspaces)
- [ ] Workspace ID resolves to a valid team
- [ ] Space / folder / list IDs exist in the target workspace
- [ ] Task creation creates a visible task in the target list (check via UI or GET)
- [ ] Status transitions match the exact (case-sensitive) status names configured
- [ ] Custom fields set correctly (verify via GET task or UI)
- [ ] Assignees are workspace members (user IDs exist in membership list)
- [ ] Rate limit does not trigger during bulk operations (<100 req/min sustained)
- [ ] Webhook registration receives test event within 30 seconds
- [ ] Webhook signature verification passes with the stored secret
- [ ] Time entries appear on the task's Time Tracking tab
- [ ] Dependency links appear on the task (check "waiting on" / "blocking")
- [ ] Error handling covers: 401 (bad token), 404 (wrong ID), 429 (rate limit), 400 (bad payload)
- [ ] Pagination works for lists with >100 tasks
- [ ] Permission checks: tasks created programmatically respect the hierarchy access levels

## Anti-Rationalization Table

| Rationalization | Reality |
|-------|---------|
| "ClickUp's API is just like Jira's" | ClickUp uses a hierarchical model (Space→Folder→List→Task). Jira uses a flat project→issue model. ID scoping, permission inheritance, and custom fields work differently. |
| "We can hardcode the workspace ID" | Workspace IDs change when migrating environments or restructuring. Always resolve `/team` dynamically. |
| "Rate limits won't affect us at our scale" | 100 req/min per workspace is tight. Two concurrent integrations can exhaust the limit. Every read operation counts. |
| "Status names are the same for all lists" | Each list can have its own set of statuses with different names across lists in the same workspace. Always verify per list. |
| "Custom field IDs are globally unique" | Custom field IDs are scoped to a list. The same field name in different lists has different IDs. Always fetch per list. |
| "OAuth is always better than API token" | For server-side automation, API tokens are simpler. OAuth adds redirect handling, token refresh, and scope management overhead. Use API tokens unless you need per-user authorization. |
| "ClickUp's API supports batch operations" | There is no batch endpoint for tasks. Each task create/update is a separate request. Batch must be implemented client-side with rate-limit pacing. |
| "Webhook guarantees delivery" | Webhooks are at-most-once delivery. If your endpoint is down, the event is lost. Build idempotent handlers and implement periodic reconciliation syncs. |
| "ClickUp vs Asana: Asana has better dependencies" | Asana has superior multi-level dependency tracking. ClickUp dependencies are one-to-one linking. For complex Gantt-style dependency chains, evaluate whether Asana is a better fit. |
| "ClickUp Docs API allows full editing" | The Docs API is read-only for content. You can create a new doc from a markdown template, but inline editing of existing docs requires the UI. |
| "We can move tasks between workspaces via API" | Tasks cannot be moved between workspaces via the API. Export/import is the only option for cross-workspace migration. |
| "The API token has no limits" | The API token inherits the user's role permissions. If the user lacks access to a space, the token can't access it either. |

## Process

### Phase 1: Discovery

1. **Authenticate** — Generate API token or complete OAuth flow
2. **Map workspace structure** — Resolve team_id, space IDs, folder IDs, list IDs
3. **Inspect schemas** — Fetch available statuses per list (`GET /list/{id}`), custom fields (`GET /list/{id}/field`), and members (`GET /space/{id}`)
4. **Set up environment** — Store API token in env var (`CLICKUP_API_TOKEN`), verify connectivity with a `GET /team` call

### Phase 2: Implementation

1. **Choose pattern** — Single task ops, bulk operations, webhook-driven, or recurrent scheduling
2. **Build CRUD wrappers** — Implement authenticated HTTP client with error retry logic
3. **Add rate-limit pacing** — Integrate delay logic or a simple token-bucket to stay under 100 req/min
4. **Handle errors** — Map HTTP status codes to actionable errors (401 → token refresh, 404 → re-resolve IDs, 429 → backoff, 400 → inspect payload)
5. **Test with a single operation** — Create one task, verify in UI, then delete

### Phase 3: Validation

1. **Run integration test** — Execute the full workflow (create → assign → set status → add time → verify via GET)
2. **Verify error paths** — Bad token, wrong ID, rate limit (burst 101 requests), invalid status
3. **Check webhook delivery** — Register a test webhook, trigger an event, confirm receipt on your endpoint
4. **Review rate limit compliance** — Count requests over a 60-second sliding window; if approaching 100, increase wait intervals
5. **Document assumptions** — Record which workspace, list IDs, and status names are assumed, and what to change if they vary
