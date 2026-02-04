---
name: julien-notion-inbox-to-github
description: Move a GitHub repo entry from Notion Inbox [DB] to Github [DB]. Use when user wants to route a GitHub URL from inbox to the dedicated GitHub database, migrate inbox entry to github database, or move github link.
---

# Notion Inbox to GitHub

Move GitHub repository entries from Inbox [DB] to Github [DB].

## Prerequisites

- `NOTION_TOKEN` environment variable set
- `requests` package: `pip install requests`

## Usage

Run the migration script with a page ID or URL:

```bash
python ~/.claude/skills/notion-inbox-to-github/scripts/migrate.py <page_id_or_url>
```

**Arguments:**
- `page_id_or_url`: Notion page ID (UUID) or full URL of the Inbox entry

**Example:**
```bash
python ~/.claude/skills/notion-inbox-to-github/scripts/migrate.py 12345678-1234-1234-1234-123456789abc
```

## Output

- On success: URL of created Github [DB] entry
- On failure: Error message with reason

## Workflow

1. Script reads the Inbox entry properties
2. Extracts GitHub URL from URL or Link property
3. Checks for duplicates in Github [DB]
4. Creates new entry with Name, URL, Source DB = "Inbox"
5. Returns new page URL

## Error Handling

| Error | Meaning |
|-------|---------|
| `DUPLICATE` | Entry already exists in Github [DB] |
| `NO_GITHUB_URL` | Entry doesn't have a github.com URL |
| `PAGE_NOT_FOUND` | Invalid page ID or no access |
| `NOT_INBOX_ENTRY` | Page is not from Inbox [DB] |

## Database IDs

- **Inbox [DB]**: `e50fb9d3-5d64-4601-a2f2-c0ac80d84d86`
- **Github [DB]**: `2cacdc04-12e3-81cc-a84e-fdbba086ab29`
