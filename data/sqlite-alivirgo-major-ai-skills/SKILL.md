---
name: sqlite
description: "Design SQLite schemas and migrations, configure WAL and pragmas, and plan backups within its concurrency limits."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["sqlite", "sql", "embedded-db", "wal", "migrations", "local-dev"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# SQLite Embedded Database AI Skill Guide

## Overview

SQLite is an embedded SQL engine in a single file (plus optional WAL sidecars). It shines for local apps, tests, edge devices, and low-to-moderate concurrency services. Agents should enable **WAL** for readers-alongside-a-writer, set busy timeouts, and treat the database file as the backup unit - copying while a writer is active without backup APIs risks corruption.

```
Application (sqlite3 / better-sqlite3 / sqlx)
        |
        v
database.db  (+ database.db-wal + database.db-shm in WAL mode)
```

## When to use

- Local development databases and unit/integration tests
- Single-node apps where ops simplicity beats client/server DB
- Shipping desktop/mobile/edge data stores
- Prototyping schema before graduating to MySQL/Postgres

## Operational directives

1. Prefer WAL mode for multi-reader workloads: `PRAGMA journal_mode=WAL;`.
2. Set `PRAGMA busy_timeout=5000;` (or app equivalent) to reduce flaky locks.
3. Always back up with `sqlite3 .backup` or the backup API - not naive `cp` under write load.
4. Use migrations with a schema version table; avoid ad-hoc ALTER chaos.
5. Do not assume multi-writer scalability - one writer at a time is the model.

## Concrete examples

### Create schema

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;

CREATE TABLE notes (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_notes_updated ON notes(updated_at);
```

### CLI migration + backup

```bash
sqlite3 app.db < migrations/001_init.sql
sqlite3 app.db "PRAGMA integrity_check;"
sqlite3 app.db ".backup 'app-backup.db'"
sqlite3 app.db ".schema"
```

### Concurrent read pattern (conceptual)

```text
Writer: BEGIN IMMEDIATE; ... COMMIT;
Readers: can proceed in WAL while writer holds write lock (with caveats)
```

### Explain query plan

```sql
EXPLAIN QUERY PLAN
SELECT * FROM notes WHERE updated_at > '2026-01-01' ORDER BY updated_at DESC;
```

## Decision table

| Need | SQLite fit | Prefer server DB when |
| :--- | :--- | :--- |
| Single node app | Excellent | Multi-writer horizontal scale |
| Tests / CI | Excellent | Need exact prod engine quirks |
| Huge analytics | Weak | Columnar / warehouse |
| Zero ops | Excellent | Managed HA / replicas required |

## Best practices

1. Keep foreign keys on; many drivers disable them by default.
2. Store timestamps in UTC ISO-8601 text or integer Unix time consistently.
3. Vacuum only with understanding of locks and file rewrite cost.
4. Document file path permissions - SQLite needs write access for journal/WAL.

## Limitations

- Limited concurrent writes; easy to hit `SQLITE_BUSY` under load.
- Network access requires your app - there is no native multi-host server mode.
- Some SQL dialect differences vs MySQL/Postgres (types are flexible/affinity-based).

## Related skills

- `mysql` - when graduating beyond embedded
- `docker` - optional; often unnecessary for SQLite apps
- `makefile-automation` - `make db-migrate` / `make db-backup` targets
- `trivy` - not DB-specific, but scan apps bundling SQLite libs
