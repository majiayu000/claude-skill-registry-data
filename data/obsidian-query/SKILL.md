---
name: obsidian-query
description: Query Obsidian vault using local HTTP API. Use when user asks about tasks, goals, experiments, journals, people, or any vault data.
---

# Obsidian Query Skill

Local HTTP API running on `localhost:27180` for querying Obsidian vault data.

## Usage

```bash
# Generic query: query.py <Base> [View]
python3 .claude/skills/obsidian-query/scripts/query.py Tasks
python3 .claude/skills/obsidian-query/scripts/query.py Tasks "By Project"
python3 .claude/skills/obsidian-query/scripts/query.py Goals "Every morning"
python3 .claude/skills/obsidian-query/scripts/query.py Journals "Weekly Review"
python3 .claude/skills/obsidian-query/scripts/query.py Experiments
python3 .claude/skills/obsidian-query/scripts/query.py People

# Utility commands
python3 .claude/skills/obsidian-query/scripts/query.py bases              # List all bases & views
python3 .claude/skills/obsidian-query/scripts/query.py backlinks <file>   # Who links here?
python3 .claude/skills/obsidian-query/scripts/query.py frontmatter <file> # Get metadata
python3 .claude/skills/obsidian-query/scripts/query.py status             # API health check
```

## Discover Bases & Views

First, list available bases and their views:
```bash
python3 .claude/skills/obsidian-query/scripts/query.py bases
```

Output:
```
Goals: Current, Every morning, Every week, All
Journals: All Entries, Last 7 Days, Weekly Review
Tasks: Active Tasks, By Project, All Tasks
```

Then query any base with optional view:
```bash
query.py Tasks                  # All fields (auto-discovered)
query.py Tasks "Active Tasks"   # Fields from view's order config
query.py Tasks "By Project"     # Grouped by project
```

## How It Works

The script reads view configuration from the API:
- `order` - which fields to display (from view config)
- `groupBy` - how to group entries (from view config)
- If no view specified, auto-discovers all fields from entries

No hardcoded logic - all rendering driven by Base definition.

## API Endpoints

```
GET /status                      # Health check
GET /bases                       # List all bases
GET /bases/:name                 # Query base (default view)
GET /bases/:name?view=ViewName   # Query base with specific view
GET /backlinks/:path             # Who links to this file?
GET /frontmatter/:path           # Get file metadata
```

## Response Structure

```json
{
  "base": "Templates/Bases/Tasks.base",
  "views": ["Active Tasks", "By Project", "All Tasks"],
  "activeView": "By Project",
  "groupBy": {"property": "project", "direction": "ASC"},
  "order": ["file", "status", "due"],
  "count": 8,
  "entries": [...]
}
```

## When to Use

- "what are my tasks?" → `query.py Tasks`
- "tasks by project" → `query.py Tasks "By Project"`
- "daily goals" / "morning goals" → `query.py Goals "Every morning"`
- "weekly goals" → `query.py Goals "Every week"`
- "weekly review" / "journals" → `query.py Journals "Weekly Review"`
- "active experiments" → `query.py Experiments`
- "who should I reconnect with?" → `query.py People`
