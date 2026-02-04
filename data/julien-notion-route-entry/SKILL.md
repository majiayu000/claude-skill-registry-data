---
name: julien-notion-route-entry
description: Route a Notion Inbox entry to the appropriate PKM database (Github, Videos, Articles, Podcasts, Formations, Lieux, Code, or Todos). Use when user wants to triage inbox, route entry, move to appropriate database.
---

# Notion Route Entry

Route Inbox entries to the appropriate PKM database based on URL patterns and keywords.

## Prerequisites

- `NOTION_TOKEN` environment variable set
- `requests` package: `pip install requests`

## Usage

Run the routing script with a page ID or URL:

```bash
python ~/.claude/skills/notion-route-entry/scripts/route.py <page_id_or_url>
```

**Arguments:**
- `page_id_or_url`: Notion page ID (UUID) or full URL of the Inbox entry

## Output

- Suggests destination based on routing rules
- Asks for confirmation or override
- Creates entry in destination database
- Returns URL of created entry

## Routing Rules

| Pattern | Destination |
|---------|-------------|
| github.com | Github [DB] |
| youtube.com | Videos [DB] |
| medium.com, dev.to | Articles [DB] |
| snipd, overcast | Podcasts [DB] |
| udemy, coursera | Formations [DB] |
| google.com/maps, komoot | Lieux [DB] |
| gist.github, codepen | Code [DB] |
| No URL | Todos [DB] |

## Destinations

| Database | ID |
|----------|----|
| Github [DB] | `2cacdc04-12e3-81cc-a84e-fdbba086ab29` |
| Videos [DB] | `2cacdc04-12e3-812d-959b-ce49a1ad0b3c` |
| Articles [DB] | `2cacdc04-12e3-8199-8ac1-e9c3007843a6` |
| Podcasts [DB] | `2cacdc04-12e3-81a1-bf23-c9b9f82208f2` |
| Formations [DB] | `2cacdc04-12e3-8168-b239-ff7e17742881` |
| Lieux [DB] | `2cacdc04-12e3-81ad-a743-cf2d2a241a0d` |
| Code [DB] | `2cacdc04-12e3-81db-aa22-dbac1beefcb1` |
| Todos [DB] | `9c9b8dcd-e01b-488f-aa87-eaaed7be9a52` |
