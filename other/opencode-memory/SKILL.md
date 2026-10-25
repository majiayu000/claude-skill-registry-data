---
name: opencode-memory"
description: >
  Browse local OpenCode history: sessions, messages, plans, prompt history, and
  prior decisions. Use when the user says history, previous session, last time,
  remember, recall, plans, prior work, or when resuming/debugging repeated work
  where earlier OpenCode context may help. Do not use for fresh tasks or when
  current files/git already answer the question.
license: Apache-2.0
compatibility: opencode
---

# OpenCode Memory Browser

Read-only lookup for local OpenCode history. Use it only when prior sessions,
plans, or decisions would help. Do not inject history by default.

## Use When

- User asks for history, previous sessions, last time, plans, recall, or memory.
- Resuming a project where prior OpenCode context may matter.
- Debugging a repeat issue that may have appeared earlier.

Do not use when repo files/git already answer the question or the task is new.

## Rules

- Read-only. Never modify OpenCode DB/files.
- Use `sqlite3` with read-only URI. Do not read the DB with file-read tools.
- Keep results small with `LIMIT` and targeted `LIKE`.
- Summarize relevant findings; do not dump raw history.
- Avoid auth/provider tables: `account`, `credential`, `control_account`, `account_state`.

## Setup

Run this first in bash:

```bash
DATA_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/opencode"
STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/opencode"
DB="$(opencode db path 2>/dev/null || true)"
[ -n "$DB" ] || DB="${OPENCODE_DB:-$DATA_ROOT/opencode.db}"
case "$DB" in :memory:|/*) ;; *) DB="$DATA_ROOT/$DB" ;; esac
if [ ! -f "$DB" ]; then
  for candidate in "$DATA_ROOT"/opencode*.db; do
    [ -f "$candidate" ] && DB="$candidate" && break
  done
fi
DB_URI="file:${DB}?mode=ro"
```

Useful files:

- Plans: `$DATA_ROOT/plans/*.md`
- Prompt history: `$STATE_ROOT/prompt-history.jsonl`
- Session diffs: `$DATA_ROOT/storage/session_diff/<session-id>.json`

## Queries

### Summary

```bash
sqlite3 "$DB_URI" "
  SELECT 'projects', COUNT(*) FROM project
  UNION ALL SELECT 'main sessions', COUNT(*) FROM session WHERE parent_id IS NULL
  UNION ALL SELECT 'messages', COUNT(*) FROM message
  UNION ALL SELECT 'parts', COUNT(*) FROM part
  UNION ALL SELECT 'todos', COUNT(*) FROM todo;
"
```

### Recent sessions

```bash
sqlite3 "$DB_URI" "
  SELECT s.id, COALESCE(s.title, 'untitled') AS title,
    COALESCE(p.name, p.worktree, '') AS project,
    datetime(s.time_updated/1000, 'unixepoch', 'localtime') AS updated,
    (SELECT COUNT(*) FROM message m WHERE m.session_id = s.id) AS messages
  FROM session s
  LEFT JOIN project p ON p.id = s.project_id
  WHERE s.parent_id IS NULL
  ORDER BY s.time_updated DESC
  LIMIT 10;
"
```

### Search text

Replace `SEARCH_TERM` first.

```bash
sqlite3 "$DB_URI" "
  SELECT s.id, COALESCE(s.title, 'untitled') AS title,
    json_extract(m.data, '$.role') AS role,
    datetime(m.time_created/1000, 'unixepoch', 'localtime') AS time,
    substr(json_extract(p.data, '$.text'), 1, 200) AS snippet
  FROM part p
  JOIN message m ON m.id = p.message_id
  JOIN session s ON s.id = m.session_id
  WHERE s.parent_id IS NULL
    AND json_extract(p.data, '$.type') = 'text'
    AND json_extract(p.data, '$.text') LIKE '%SEARCH_TERM%'
  ORDER BY m.time_created DESC
  LIMIT 10;
"
```

### Read session text

Replace `SESSION_ID_HERE` first. Text parts only; use the reference for tool,
patch, file, reasoning, or V2 internals.

```bash
sqlite3 "$DB_URI" "
  SELECT json_extract(m.data, '$.role') AS role,
    datetime(m.time_created/1000, 'unixepoch', 'localtime') AS time,
    GROUP_CONCAT(json_extract(p.data, '$.text'), char(10)) AS text
  FROM message m
  LEFT JOIN part p ON p.message_id = m.id
    AND json_extract(p.data, '$.type') = 'text'
  WHERE m.session_id = 'SESSION_ID_HERE'
  GROUP BY m.id
  ORDER BY m.time_created ASC
  LIMIT 50;
"
```

## Plans And Prompt History

```bash
ls -lt "$DATA_ROOT"/plans/*.md 2>/dev/null | head -20
tail -20 "$STATE_ROOT"/prompt-history.jsonl 2>/dev/null
```

Prompt history entries currently use `input`, `mode`, and `parts[]`; do not
assume root `text`.

## Deep Reference

Use [references/storage-format.md](references/storage-format.md) only when you
need table details, part/tool shapes, legacy JSON paths, or debug queries.
