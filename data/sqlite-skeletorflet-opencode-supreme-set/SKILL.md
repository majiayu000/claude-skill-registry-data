---
name: sqlite
description: SQLite — zero-config embedded DB, WAL mode, CLI, SQL features, pragmas, extensions.
---

## sqlite

### Zero-Config Embedded DB
- Single-file database — no server, no config, no setup.
- `sqlite3 my.db` opens or creates a database.
- Perfect for mobile, desktop, embedded, and test environments.
- `PRAGMA journal_mode=WAL;` — Write-Ahead Log for concurrent reads.

### CLI
- `.tables` — list tables; `.schema tablename` — DDL for a table.
- `.dump` — full SQL dump for backup; `.import file.csv table` — CSV import.
- `.headers on` / `.mode column` for formatted output.
- `.output file.sql` — redirect query results to file.

### SQL Features
- Window functions: `RANK() OVER (ORDER BY score DESC)`, `LAG`, `LEAD`.
- CTEs: `WITH RECURSIVE` for hierarchical data (org trees, graphs).
- JSON: `json_extract`, `json_array`, `json_object`, `json_each`.
- `UPSERT` — `INSERT ... ON CONFLICT DO UPDATE SET ...`.
- Generated columns, partial indexes, `RETURNING` clause.

### Performance Pragmas
- `PRAGMA cache_size = -8000` — 8MB cache; `PRAGMA page_size = 4096`.
- `PRAGMA synchronous = NORMAL` — balance safety and speed.
- `PRAGMA foreign_keys = ON` — enforce FK constraints (off by default).
- `PRAGMA journal_mode = WAL` — better concurrency.

### Extensions
- FTS5: `CREATE VIRTUAL TABLE docs USING fts5(title, content)` for full-text search.
- SpatiaLite: spatial SQL functions and geometry types.
- `sqlean` bundle: crypto, math, fileio, regexp, stats extensions.

### Backup / Restore
- `.backup main backup.db` — online backup (safe during writes).
- `VACUUM INTO 'new.db'` — compact + copy.
- `.restore` from backup file.
