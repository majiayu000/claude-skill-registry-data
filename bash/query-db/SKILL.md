---
name: query-db
description: Inspect or query the SQLite databases under ~/databases (erp.db, solar.db, network.db, deebot, bridge). Use before any SELECT/UPDATE against a project database, and when hitting "no such column", "no such table", or an empty result you did not expect.
allowed-tools: Bash, Read, Grep
argument-hint: "target: local | server (default: local)"
model: claude-sonnet-5
---

# Querying the project databases

`~/databases` is the default DB directory for every project (invariant 3) — it is the
tree the `server-scripts/` systemd backup service zips. Per-project override is
`{PREFIX}_DB_DIR`.

**Schema first, always.** Writing a `SELECT` from a guessed column name is the single
most repeated wasted round trip in this codebase's history — `no such column: day`,
`no such column: ts`, `no such column: created_at` were all guesses.

## 1. Find the database and read its schema

```bash
ls -la ~/databases/
sqlite3 ~/databases/<name>.db '.tables'
sqlite3 ~/databases/<name>.db '.schema <table>'
```

Batch these — the listing and the schema of the table you already know you need can go
in one call.

## 2. Then query, read-only by default

```bash
sqlite3 ~/databases/<name>.db -header -column 'SELECT ... LIMIT 20;'
```

Prefer `-header -column` for anything a human will read.

## 3. Writes

- Never `UPDATE`/`DELETE` a real database to test a hypothesis. Copy it to the scratchpad
  first, or point the app at a temp dir with `{PREFIX}_DB_DIR=$(mktemp -d)`.
- Confirm with the user before any write to `~/databases`. That tree is backed up, but a
  restore is their afternoon, not yours.
- Schema changes belong in the project's migrations, not in an ad-hoc `ALTER TABLE`.

## 4. Reaching a DB through devkit rather than the CLI

`devkit.db` gives WAL, foreign keys, a `Row` factory and a 5s timeout — a bare
`sqlite3.connect` in a throwaway script gives none of those and can miss uncommitted WAL
state:

```python
from devkit.db import resolve_db_dir, db_path, connection

with connection(db_path(resolve_db_dir("SOLAR_DB_DIR"), "solar")) as conn:
    rows = conn.execute("select ...").fetchall()
```

`db_path(db_dir, name)` takes the directory first and normalizes `name` to a single
`<stem>.db`, so it cannot escape the directory.

Run it with the owning project's interpreter (`<repo>/.venv/bin/python`), not the system
one — devkit is only installed in the project venvs.

## Target

- `local` (default) — connect to the local DB directly.
- `server` — connect over SSH (tunnel or remote client). Follow `/home/rahul/Documents/code/claude_settings/policies/ssh-policy.md`:
  - **Reads** run freely.
  - **Writes** always confirm first — exact statement, rows/tables affected, reversibility.
  - Prefer a rollback-first check (`BEGIN`, show affected count, then ask before `COMMIT`)
    for anything destructive.

`local` also follows the read/write confirmation split above — the target only changes
*how* the DB is reached, not whether writes need confirmation