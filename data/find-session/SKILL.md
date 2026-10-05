---
name: find-session
description: Find opencode sessions by name or content across ALL project directories, bypassing the cwd scoping of session_list/session_search. Use when looking for a session that was started in a different folder.
---

# Find Session Skill

The built-in `session_list` and `session_search` tools are scoped to the current working directory. This skill bypasses that by querying the opencode SQLite database directly.

## Database location

```
~/.local/share/opencode/opencode.db
```

## How to find a session

### 1. By title (fast — use this first)

```bash
sqlite3 ~/.local/share/opencode/opencode.db \
  "SELECT id, title, directory, datetime(time_updated/1000,'unixepoch') as last_active
   FROM session
   WHERE title LIKE '%<search term>%'
   ORDER BY time_updated DESC
   LIMIT 10;"
```

### 2. By content (slower — use if title search returns nothing)

```bash
sqlite3 ~/.local/share/opencode/opencode.db \
  "SELECT DISTINCT s.id, s.title, s.directory, datetime(s.time_updated/1000,'unixepoch') as last_active
   FROM session s
   JOIN part p ON p.session_id = s.id
   WHERE p.data LIKE '%<search term>%'
   ORDER BY s.time_updated DESC
   LIMIT 10;"
```

### 3. List all recent sessions across all projects

```bash
sqlite3 ~/.local/share/opencode/opencode.db \
  "SELECT id, title, directory, datetime(time_updated/1000,'unixepoch') as last_active
   FROM session
   ORDER BY time_updated DESC
   LIMIT 20;"
```

## Once you have the session ID

Read its recent messages via the `part` table (the `session_read` tool won't work cross-project):

```bash
sqlite3 ~/.local/share/opencode/opencode.db \
  "SELECT substr(p.data, 1, 800), datetime(p.time_created/1000,'unixepoch')
   FROM part p
   JOIN message m ON p.message_id = m.id
   WHERE m.session_id = '<session_id>'
   AND p.data LIKE '{\"type\":\"text\"%'
   ORDER BY p.time_created DESC
   LIMIT 20;"
```

To get tool calls and actions too (broader view):

```bash
sqlite3 ~/.local/share/opencode/opencode.db \
  "SELECT substr(p.data, 1, 1000), datetime(p.time_created/1000,'unixepoch')
   FROM part p
   JOIN message m ON p.message_id = m.id
   WHERE m.session_id = '<session_id>'
   ORDER BY p.time_created DESC
   LIMIT 30;"
```

## Workflow

1. Run the title search first — it's instant
2. If no match, run the content search (may be slow on large DBs)
3. Report: session ID, title, directory, and last active time
4. If user wants to know what's happening, read the last 15-20 parts and summarise
