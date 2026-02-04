---
name: notion-changes
description: Query Notion for recent document changes
---

# Notion Changes Skill

Fetches recently edited pages from a Notion workspace.

## When to Use

Use this skill when you need to get:
- Pages created yesterday
- Pages edited yesterday
- Who made the changes

## How to Use

```bash
# Get yesterday's changes (default)
$CLAUDE_CONFIG_DIR/skills/notion-changes/scripts/get-changes.sh

# Get changes for a specific date
$CLAUDE_CONFIG_DIR/skills/notion-changes/scripts/get-changes.sh "2024-12-15"
```

### Arguments
- `date` (optional): Specific date in YYYY-MM-DD format. Defaults to yesterday.

### Prerequisites
- `NOTION_API_KEY` environment variable must be set
- The Notion integration must have access to the pages you want to query

## Output

Results are saved to `/tmp/data/notion_changes_[timestamp].json`:

```json
{
  "date": "2024-12-15",
  "pages_created": [
    {
      "id": "page-id-123",
      "title": "New Document",
      "url": "https://notion.so/...",
      "created_by": "user@email.com",
      "created_time": "2024-12-15T10:30:00Z"
    }
  ],
  "pages_edited": [
    {
      "id": "page-id-456",
      "title": "Existing Document",
      "url": "https://notion.so/...",
      "last_edited_by": "user@email.com",
      "last_edited_time": "2024-12-15T14:00:00Z"
    }
  ]
}
```

Console output summary:
```
Notion Changes for 2024-12-15

Pages Created (3):
  - New Document
  - Another Page
  - Meeting Notes

Pages Edited (5):
  - Project Plan
  - Roadmap
  - Team Updates
```

## Error Handling

- **401 Unauthorized**: Check that NOTION_API_KEY is set correctly
- **403 Forbidden**: The integration may not have access to the workspace
- **429 Rate Limited**: Too many requests, try again later
