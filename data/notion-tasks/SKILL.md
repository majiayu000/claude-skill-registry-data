---
name: notion-tasks
description: Interact with Notion databases and tasks. Auto-detects intent to read, create, update, or delete Notion tasks. Reads API key from NOTION_API_KEY environment variable. Supports full CRUD operations. Trigger phrases include "notion tasks", "show backlog", "create task in notion", "MoneyGraph tasks", "outstanding tasks".
---

# Notion Tasks Skill

Manage Notion databases and tasks directly from Claude Code.

## Prerequisites

### API Key Setup (One-time)

Before using this skill, ensure `NOTION_API_KEY` is set:

```bash
# Check if already set
echo $NOTION_API_KEY

# If not set, run the setup script:
~/.claude/scripts/notion-setup.sh

# Or manually add to ~/.zshrc:
export NOTION_API_KEY='secret_your_key_here'
```

### Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the "Internal Integration Secret"
4. Share your database with the integration (click "..." menu → "Add connections")

---

## Database Routing

The skill routes to the appropriate database based on user intent:

| User Intent | Database | Database ID |
|-------------|----------|-------------|
| General tasks | **Main Company** (default) | `1f4d767756ad80e6a76ff70490457673` |
| Dev work, bugs, features | **Dev Tracker** | `288d767756ad80b0ab61cc5cb5500315` |
| List/lookup projects | **Projects** | `1f4d767756ad808eb6d5f563b603db7f` |

### Routing Keywords

**→ Dev Tracker** when user mentions:
- `dev`, `development`, `engineering`
- `bug`, `feature`, `tech task`
- `dev task`, `dev tasks`
- `moneygraph` (project name)

**→ Projects DB** when user mentions:
- `projects`, `project list`, `list projects`

**→ Main Company** (default):
- All other task requests

---

## Auto-Detection Triggers

This skill activates when you mention:
- **Direct**: "notion", "notion tasks", "notion database"
- **Intent**: "show my tasks", "what's in backlog", "outstanding work"
- **Project**: "MoneyGraph tasks", "project backlog"
- **Actions**: "create task", "mark done", "update status"
- **Dev**: "create a bug", "new feature", "dev task"

---

## Operations

### 1. List Tasks from Database

Query a Notion database to show tasks:

```bash
# Main Company tasks (default)
~/.claude/scripts/notion-api.sh POST "/databases/1f4d767756ad80e6a76ff70490457673/query" '{}'

# Dev Tracker tasks
~/.claude/scripts/notion-api.sh POST "/databases/288d767756ad80b0ab61cc5cb5500315/query" '{}'
```

**Example: Query open dev tasks:**
```bash
~/.claude/scripts/notion-api.sh POST "/databases/288d767756ad80b0ab61cc5cb5500315/query" '{
  "filter": {
    "property": "Status",
    "status": {
      "does_not_equal": "Done"
    }
  },
  "sorts": [
    {"property": "Priority Level", "direction": "descending"}
  ]
}'
```

### 2. Get Single Task/Page

```bash
~/.claude/scripts/notion-api.sh GET "/pages/PAGE_ID"
```

### 3. Create a New Task

**Simple task (Main Company):**
```bash
~/.claude/scripts/notion-api.sh POST "/pages" '{
  "parent": {"database_id": "1f4d767756ad80e6a76ff70490457673"},
  "properties": {
    "Name": {
      "title": [{"text": {"content": "New Task Title"}}]
    },
    "Status": {
      "status": {"name": "Not started"}
    }
  }
}'
```

### 4. Update Task Status

```bash
~/.claude/scripts/notion-api.sh PATCH "/pages/PAGE_ID" '{
  "properties": {
    "Status": {
      "status": {"name": "Done"}
    }
  }
}'
```

### 5. Archive (Delete) Task

```bash
~/.claude/scripts/notion-api.sh PATCH "/pages/PAGE_ID" '{
  "archived": true
}'
```

---

## Creating Dev Tasks (Dev Tracker)

Typical dev task includes: **Name + Status + Type + Priority + Urgency**

Optional: Project, Assignee, Tags, Sprint, Effort

### Example: Create a Bug

```bash
~/.claude/scripts/notion-api.sh POST "/pages" '{
  "parent": {"database_id": "288d767756ad80b0ab61cc5cb5500315"},
  "properties": {
    "Name": {
      "title": [{"text": {"content": "Fix login timeout issue"}}]
    },
    "Status": {
      "status": {"name": "Backlog"}
    },
    "Type": {
      "select": {"name": "Bug"}
    },
    "Priority Level": {
      "select": {"name": "Hi"}
    },
    "Urgency": {
      "select": {"name": "Soon"}
    },
    "Tags": {
      "multi_select": [{"name": "backend"}]
    }
  }
}'
```

### Example: Create a Feature with Assignee

```bash
~/.claude/scripts/notion-api.sh POST "/pages" '{
  "parent": {"database_id": "288d767756ad80b0ab61cc5cb5500315"},
  "properties": {
    "Name": {
      "title": [{"text": {"content": "Add dark mode support"}}]
    },
    "Type": {
      "select": {"name": "Feature"}
    },
    "Priority Level": {
      "select": {"name": "Medium"}
    },
    "Urgency": {
      "select": {"name": "mid-term"}
    },
    "Effort": {
      "select": {"name": "days"}
    },
    "Assigned To": {
      "people": [{"id": "USER_ID_HERE"}]
    },
    "Project": {
      "relation": [{"id": "PROJECT_PAGE_ID_HERE"}]
    }
  }
}'
```

### Example: Create a Task with Sprint

```bash
~/.claude/scripts/notion-api.sh POST "/pages" '{
  "parent": {"database_id": "288d767756ad80b0ab61cc5cb5500315"},
  "properties": {
    "Name": {
      "title": [{"text": {"content": "Implement API caching"}}]
    },
    "Type": {
      "select": {"name": "Task"}
    },
    "Priority Level": {
      "select": {"name": "Medium"}
    },
    "Urgency": {
      "select": {"name": "Soon"}
    },
    "Sprint.": {
      "rich_text": [{"text": {"content": "Sprint 12"}}]
    }
  }
}'
```

---

## Working with Projects

### List All Projects

```bash
~/.claude/scripts/notion-api.sh POST "/databases/1f4d767756ad808eb6d5f563b603db7f/query" '{}'
```

### Find Project by Name (for relations)

```bash
~/.claude/scripts/notion-api.sh POST "/databases/1f4d767756ad808eb6d5f563b603db7f/query" '{
  "filter": {
    "property": "Name",
    "title": {"contains": "MoneyGraph"}
  }
}'
```

### Parse Project ID for Relations

```bash
~/.claude/scripts/notion-api.sh POST "/databases/1f4d767756ad808eb6d5f563b603db7f/query" '{
  "filter": {"property": "Name", "title": {"contains": "ProjectName"}}
}' | jq '.results[0].id'
```

---

## Dev Tracker Property Reference

### Priority Level
| Value | Color |
|-------|-------|
| Critical | red |
| Hi | green |
| Medium | yellow |
| Low | blue |

### Urgency
| Value | Color |
|-------|-------|
| now | green |
| Soon | blue |
| mid-term | pink |
| Someday | gray |

### Type
| Value | Color |
|-------|-------|
| Epic | purple |
| Task | blue |
| Improvement | green |
| Feature | green |
| Bug | red |

### Tags (multi-select)
- UI/UX (purple)
- infra (brown)
- backend (orange)
- frontend (green)
- bug (gray)
- AI (red)
- Test (blue)

### Effort
| Value | Color |
|-------|-------|
| weeks | yellow |
| days | red |
| hours | orange |
| mins | gray |

### Status
| Value | Group |
|-------|-------|
| Not started | to_do |
| Backlog | to_do |
| In progress | in_progress |
| Done | complete |

---

## Response Formatting

When displaying tasks, format them as a readable table:

```
## Dev Tracker Tasks

| Status | Task | Type | Priority | Urgency |
|--------|------|------|----------|---------|
| 🔵 In Progress | Fix login timeout | Bug | Hi | Soon |
| 📋 Backlog | Add dark mode | Feature | Medium | mid-term |
| ⚪ Not started | Update docs | Task | Low | Someday |

**Summary**: 3 open tasks
```

### Status Icons
- ⚪ Not started / Todo
- 📋 Backlog
- 🔵 In Progress
- ✅ Done / Complete
- 🔴 Blocked
- 🟡 In Review

---

## Parsing Notion API Responses

The Notion API returns complex JSON. Here's how to extract key fields:

### Task Title
```
.properties.Name.title[0].plain_text
```

### Status
```
.properties.Status.status.name
```

### Priority Level
```
.properties["Priority Level"].select.name
```

### Urgency
```
.properties.Urgency.select.name
```

### Type
```
.properties.Type.select.name
```

### Due Date
```
.properties.Due.date.start
```

### Parse multiple fields with jq:
```bash
~/.claude/scripts/notion-api.sh POST "/databases/288d767756ad80b0ab61cc5cb5500315/query" '{}' | jq '.results[] | {
  id: .id,
  title: .properties.Name.title[0].plain_text,
  status: .properties.Status.status.name,
  type: .properties.Type.select.name,
  priority: .properties["Priority Level"].select.name,
  urgency: .properties.Urgency.select.name
}'
```

---

## Error Handling

### API Key Not Set
```
Error: NOTION_API_KEY not set
→ Run: ~/.claude/scripts/notion-setup.sh
```

### 401 Unauthorized
```
API key is invalid or expired.
→ Check key at https://www.notion.so/my-integrations
```

### 404 Not Found
```
Database or page not found.
→ Ensure the integration is shared with the database
→ Click "..." → "Add connections" → Select your integration
```

---

## Configuration

See `~/.claude/skills/notion-tasks/config.yaml` for:
- Database IDs and routing aliases
- Full schema with valid property options
- Status icons and property mappings

---

## Security Notes

- API key is stored in environment variable, never in code
- The helper script never logs or echoes the API key
- Always use the helper script for authenticated requests
