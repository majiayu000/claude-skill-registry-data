---
name: todoist
description: "Reference for Todoist Sync API task management — reading, creating, updating, moving, and completing tasks using the sections-based status model (Triage/Do/Waiting/Defer). Use when managing Todoist tasks, creating batch task operations, checking task status, or building Todoist API payloads. Not a user-invocable skill."
---

# Todoist Task Management

Reference for managing tasks in this project's Todoist project via the Sync API. Provides patterns for reading, creating, updating, moving, and completing tasks, plus the sections-based status model used across all Outwork OS projects.

**This is not a user-invocable skill.** It's a reference that other skills and agents read when they need to interact with Todoist.

---

## Finding This Project's Todoist ID

The Todoist project ID is stored in `context-map.md` in the project root. Extract it with:

```bash
grep -o '\*\*Todoist Project[^:]*:\s*`[^`]*`' context-map.md | grep -o '`[^`]*`' | tr -d '`'
```

If that returns empty, fall back to the Data Source Registry section:
```bash
grep -A1 "^### Todoist" context-map.md | grep "Project ID" | grep -o '`[^`]*`' | tr -d '`'
```

If no Todoist project ID is found, this project doesn't have one yet. Run `/context-map` to set it up.

---

## Authentication

Token is in Vault:

```bash
TODOIST_API_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" todoist_api_token)
```

---

## API: Always Use Sync

**Endpoint:** `POST https://api.todoist.com/api/v1/sync`

Never use REST v2 (`/rest/v2/`) — it returns HTTP 410 Gone.

The Sync API batches up to 100 commands in a single request (counts as 1 toward rate limits). No MCP server exists for Todoist — all access is via `curl`.

**Rate limits:** 100 full syncs or 1,000 incremental syncs per 15 minutes. On HTTP 429, back off exponentially.

---

## Status Model: Sections

Every registered project has four standard sections that represent task status:

| Section | Meaning | Who moves tasks here |
|---------|---------|---------------------|
| **Triage** | New, unprocessed — needs a decision | Automated skills (inbox-zero, whats-next) |
| **Do** | Committed to doing, actively working | User or classification agent |
| **Waiting** | Blocked on someone else | User or classification agent |
| **Defer** | Parked for later, not urgent | User or classification agent |

**Lifecycle:** Tasks enter at **Triage** (created by automated skills or manual capture). During review, they move to **Do**, **Waiting**, or **Defer**. When complete, use `item_complete` — don't move to a "Done" section.

**Section IDs** are fetched at runtime (see Reading Data below). Never hardcode them.

---

## Reading Data

### Full Sync (first call or cold start)

```bash
curl -s -X POST https://api.todoist.com/api/v1/sync \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sync_token": "*", "resource_types": ["items", "sections"]}'
```

Save the returned `sync_token` for incremental sync on subsequent calls.

### Filter to This Project

```python
import json
data = json.loads(response_text)

PROJECT_ID = "YOUR_PROJECT_ID"

# Tasks for this project (open only)
tasks = [t for t in data["items"] if t["project_id"] == PROJECT_ID and not t["checked"]]

# Sections for this project
sections = {s["name"]: s["id"] for s in data["sections"] if s["project_id"] == PROJECT_ID}
# sections = {"Triage": "abc123", "Do": "def456", "Waiting": "ghi789", "Defer": "jkl012"}

# Group tasks by status
by_status = {}
section_id_to_name = {v: k for k, v in sections.items()}
for t in tasks:
    status = section_id_to_name.get(t.get("section_id"), "Unsectioned")
    by_status.setdefault(status, []).append(t)
```

### Key Task Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Task ID |
| `content` | string | Title (supports Markdown) |
| `description` | string | Extended description |
| `project_id` | string | Which project |
| `section_id` | string/null | Current status section |
| `labels` | string[] | Labels array |
| `priority` | int | 4=urgent, 3=high, 2=medium, 1=normal (inverted!) |
| `due` | object/null | `{date, string, datetime, timezone, is_recurring}` |
| `checked` | bool | True if completed |
| `added_at` | string | ISO timestamp |

---

## Writing Data

**Always build JSON payloads in Python** to avoid shell escaping issues. Write to a temp file, then curl it.

### Template: Build and Send a Batch

```python
import json, uuid

commands = []

# ... append commands here ...

with open("/tmp/todoist_batch.json", "w") as f:
    json.dump({"commands": commands}, f)
```

```bash
curl -s -X POST "https://api.todoist.com/api/v1/sync" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @/tmp/todoist_batch.json
```

### Verify Results

```python
response = json.loads(result_text)
status = response.get("sync_status", {})
ok = sum(1 for v in status.values() if v == "ok")
failed = len(status) - ok
print(f"Succeeded: {ok}, Failed: {failed}")
if failed:
    for uuid_val, result in status.items():
        if result != "ok":
            print(f"  FAILED {uuid_val}: {result}")
```

---

## Common Operations

### Create a Task

```python
commands.append({
    "type": "item_add",
    "uuid": str(uuid.uuid4()),
    "temp_id": str(uuid.uuid4()),  # MANDATORY — omitting causes error code 20
    "args": {
        "content": "Task title",
        "description": "Details about the task\n\nSource: where this came from",
        "project_id": PROJECT_ID,
        "section_id": sections["Triage"],  # New tasks go to Triage
        "priority": 2,                      # 1=normal, 2=medium, 3=high, 4=urgent
        "due": {"string": "tomorrow"},       # Omit entirely if no due date
        "labels": ["drafted"]                # Optional
    }
})
```

**Rules:**
- Every `item_add` MUST have `temp_id` (UUID) — omitting causes error code 20
- Use `temp_id` to reference newly created items in the same batch (e.g., as `section_id` or `parent_id`)
- New automated tasks always go to `Triage` section
- Use Python `uuid.uuid4()`, never bash `$(uuidgen)` in JSON

### Update a Task

```python
commands.append({
    "type": "item_update",
    "uuid": str(uuid.uuid4()),
    "args": {
        "id": "TASK_ID",          # Required
        "content": "New title",    # Only include fields you're changing
        "due": {"string": "Feb 25"}
    }
})
```

Only send the fields you want to change — unchanged fields should be omitted.

### Move a Task (Change Status)

Moving a task between sections changes its status:

```python
commands.append({
    "type": "item_move",
    "uuid": str(uuid.uuid4()),
    "args": {
        "id": "TASK_ID",
        "section_id": sections["Do"]  # Triage → Do, Waiting, or Defer
    }
})
```

### Complete a Task

```python
commands.append({
    "type": "item_complete",
    "uuid": str(uuid.uuid4()),
    "args": {"id": "TASK_ID"}
})
```

**Warning:** Completing a recurring task reschedules it instead of closing it. Use `item_delete` to permanently remove a recurring task.

### Delete a Task

```python
commands.append({
    "type": "item_delete",
    "uuid": str(uuid.uuid4()),
    "args": {"id": "TASK_ID"}
})
```

### Create Sections (if missing)

If the project doesn't have the standard sections yet:

```python
section_names = ["Triage", "Do", "Waiting", "Defer"]
for name in section_names:
    temp = str(uuid.uuid4())
    commands.append({
        "type": "section_add",
        "uuid": str(uuid.uuid4()),
        "temp_id": temp,
        "args": {"name": name, "project_id": PROJECT_ID}
    })
    if name == "Triage":
        triage_temp_id = temp  # Use in item_add commands in same batch
```

---

## Compound Patterns

### Close Task + Create Follow-Up

```python
commands = [
    {
        "type": "item_complete",
        "uuid": str(uuid.uuid4()),
        "args": {"id": "OLD_TASK_ID"}
    },
    {
        "type": "item_add",
        "uuid": str(uuid.uuid4()),
        "temp_id": str(uuid.uuid4()),
        "args": {
            "content": "Follow up on X",
            "project_id": PROJECT_ID,
            "section_id": sections["Waiting"],
            "due": {"string": "next Monday"}
        }
    }
]
```

### Bulk Status Change (Classification)

```python
# Move multiple tasks from Triage to their appropriate sections
moves = [
    ("TASK_1_ID", "Do"),
    ("TASK_2_ID", "Waiting"),
    ("TASK_3_ID", "Defer"),
]

for task_id, status in moves:
    commands.append({
        "type": "item_move",
        "uuid": str(uuid.uuid4()),
        "args": {"id": task_id, "section_id": sections[status]}
    })
```

---

## Priority Mapping

Priority values are **inverted** from what you'd expect:

| Value | Meaning | When to use |
|-------|---------|-------------|
| 4 | Urgent | Deadline within 24h, blocking others |
| 3 | High | Deadline within 3 days, time-sensitive |
| 2 | Medium | Standard work, moderate urgency |
| 1 | Normal | No deadline, informational, relationship-building |

---

## Due Dates

| Format | Example | Use for |
|--------|---------|---------|
| `{"string": "tomorrow"}` | Natural language | Most cases — Todoist parses it |
| `{"string": "every Monday"}` | Recurring | Repeating tasks |
| `{"date": "2026-02-25"}` | Exact date | Specific deadlines |
| `{"datetime": "2026-02-25T10:00:00", "timezone": "America/Halifax"}` | Date+time | Calendar-aligned tasks |

---

## Shell Escaping Rules

- **Never use inline `$(uuidgen)` in JSON strings** — causes escaping nightmares
- **Never use `!=` in Python inside bash heredocs** — bash escapes it as `\!=`
- **Always use single-quoted heredoc delimiters** (`<< 'PYEOF'`) for inline Python
- **Preferred pattern:** Build JSON in standalone Python, write to `/tmp/*.json`, then `curl -d @/tmp/file.json`
- **Use `str(uuid.uuid4())` in Python** for all UUID generation

---

## Error Reference

| Code | Meaning | Fix |
|------|---------|-----|
| 20 | Missing `temp_id` | Every `item_add` MUST have `temp_id` |
| 22 | Invalid `project_id` | Verify project ID exists |
| 410 | REST v2 deprecated | Use Sync API, never `/rest/v2/` |
| 429 | Rate limited | Back off exponentially, check `retry_after` |
