---
name: sqlite
description: SQLite — WAL mode, JSON1, FTS5, indexes, CLI.
---

# SQLite Reference

## When to Load
Load when the project uses SQLite (signal: `sqlite3`, `better-sqlite3`, `SQLite`, `better_sqlite3`, `.db` / `.sqlite` file paths, `DATABASE_URL` with `sqlite://`).

## CLI Connection

```bash
# Open a database file:
sqlite3 "$DB_PATH"

# Run a query directly:
sqlite3 "$DB_PATH" "SELECT * FROM users LIMIT 5;"

# Read-only mode (safe for production inspection):
sqlite3 "file:${DB_PATH}?mode=ro"

# In-memory database (testing):
sqlite3 ":memory:"
```

Useful dot-commands inside `sqlite3`:
```
.schema              -- show all CREATE statements
.tables              -- list all tables
.indexes <table>     -- list indexes for a table
.mode column         -- columnar output
.headers on          -- show column names
.timer on            -- show query execution time
EXPLAIN QUERY PLAN SELECT ...;   -- show index usage
```

## Connection Modes

| URI | Behaviour |
|-----|-----------|
| `file:path/to/db` | Default read/write |
| `file:path/to/db?mode=ro` | Read-only — no write locks |
| `file:path/to/db?mode=memory` | Private in-memory DB |
| `file:dbname?mode=memory&cache=shared` | Shared in-memory DB (same process) |
| `:memory:` | Convenience alias for private in-memory |

Multiple connections to the same file: always enable WAL mode for concurrent readers.

## WAL Mode

Enable WAL (Write-Ahead Logging) for any concurrent workload:

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;  -- safe with WAL; 'FULL' for max durability
```

WAL benefits:
- Readers do not block writers; writers do not block readers
- Faster writes (sequential appends vs random page writes)
- Survives crashes without corruption (WAL is checkpointed periodically)

Checkpoint manually when needed:
```sql
PRAGMA wal_checkpoint(TRUNCATE);
```

## Pragmas Worth Knowing

```sql
PRAGMA foreign_keys = ON;       -- OFF by default — always enable
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;     -- wait 5 s before returning SQLITE_BUSY
PRAGMA cache_size = -64000;     -- 64 MB page cache (negative = kibibytes)
PRAGMA temp_store = MEMORY;     -- store temp tables in RAM
PRAGMA mmap_size = 134217728;   -- 128 MB memory-mapped I/O
```

These pragmas are session-level unless set in the connection setup. Set them immediately after `OPEN`.

## Indexes

```sql
-- Covering index (includes all queried columns):
CREATE INDEX idx_orders_user ON orders(user_id, created_at, status);

-- Partial index:
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;

-- Expression index:
CREATE INDEX idx_lower_email ON users(LOWER(email));
```

SQLite uses the query planner (`sqlite_stat1`): run `ANALYZE` after bulk inserts to update statistics.

## JSON1 Extension

Available in SQLite 3.9+; enabled by default in most distributions.

```sql
-- Extract a field:
SELECT json_extract(data, '$.name') FROM events;

-- Filter on JSON field:
SELECT * FROM events WHERE json_extract(data, '$.type') = 'purchase';

-- Index a JSON field via generated column (SQLite 3.31+):
ALTER TABLE events ADD COLUMN event_type TEXT
  GENERATED ALWAYS AS (json_extract(data, '$.type')) VIRTUAL;
CREATE INDEX idx_event_type ON events(event_type);
```

## FTS5 (Full-Text Search)

```sql
CREATE VIRTUAL TABLE docs_fts USING fts5(title, body, content='docs', content_rowid='id');

-- Query:
SELECT rowid, rank FROM docs_fts WHERE docs_fts MATCH 'sqlite performance' ORDER BY rank;

-- Keep FTS table in sync via triggers:
CREATE TRIGGER docs_ai AFTER INSERT ON docs BEGIN
  INSERT INTO docs_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;
```

## Concurrency Limits

SQLite is not designed for high write concurrency:
- One writer at a time (WAL allows concurrent readers + one writer)
- For > 1 writer or network-facing applications, consider PostgreSQL or MySQL
- Acceptable for: embedded apps, mobile, local-first, low-concurrency servers, test fixtures, CLI tools

## Common Gotchas

| Gotcha | Fix |
|--------|-----|
| Foreign keys off by default | `PRAGMA foreign_keys = ON` on every connection |
| `SQLITE_BUSY` under write contention | `PRAGMA busy_timeout = 5000`; serialize writes in application |
| Type affinity surprises (`1 = '1'` is true) | Use strict typing (SQLite 3.37+ `STRICT` tables) or validate in application |
| WAL file grows unbounded if checkpoint never runs | `PRAGMA wal_autocheckpoint = 1000` (default); or manual checkpoint |
| `INTEGER PRIMARY KEY` vs `ROWID` | `INTEGER PRIMARY KEY` is an alias for `rowid`; use it for efficient row lookup |
| No `ALTER TABLE … DROP COLUMN` before 3.35.0 | Upgrade or recreate the table via the rename-insert-drop-rename pattern |
