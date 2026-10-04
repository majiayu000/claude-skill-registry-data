---
name: database-async-patterns
description: SQLite and async database patterns for VoxAgent's persistent storage. Use when writing database access code, managing connections, designing schemas, running migrations, or testing data layers. Triggers on tasks involving core/memory.py, any aiosqlite usage, or database-related modules.
---

# Database & Async SQLite Patterns for VoxAgent

Guidelines for writing correct, performant async database code in VoxAgent. Covers connection lifecycle, query safety, schema management, and test isolation using `aiosqlite`.

## When to Apply

Reference these guidelines when:
- Reading or writing to VoxAgent's conversation memory (`core/memory.py`)
- Adding new persistent storage (settings, skill history, analytics)
- Writing migrations or schema changes
- Building database fixtures for tests
- Debugging connection or locking issues

## Rule Categories by Priority

| Priority | Category | Impact | Applies to |
|----------|----------|--------|------------|
| 1 | Connection Management | CRITICAL | All DB code |
| 2 | Query Safety | HIGH | All DB code |
| 3 | Schema & Migrations | HIGH | Setup/deploy |
| 4 | Performance | MEDIUM | All DB code |
| 5 | Testing | MEDIUM | tests/ |

## Quick Reference

### 1. Connection Management (CRITICAL)

- `db-async-context` — ALWAYS use `async with` for database connections. Never hold connections open across request boundaries:
  ```python
  # Good: scoped connection
  async with aiosqlite.connect(db_path) as db:
      await db.execute("INSERT INTO logs VALUES (?)", (entry,))
      await db.commit()

  # Bad: connection leaked
  db = await aiosqlite.connect(db_path)
  await db.execute(...)  # connection never closed on error
  ```

- `db-single-writer` — SQLite allows only one writer at a time. Use `asyncio.Lock()` to serialize writes:
  ```python
  _write_lock = asyncio.Lock()

  async def save_entry(self, entry: ConversationEntry) -> None:
      async with self._write_lock:
          async with aiosqlite.connect(self._db_path) as db:
              await db.execute("INSERT INTO conversations ...", (...))
              await db.commit()
  ```

- `db-wal-mode` — Enable WAL mode for concurrent reads during writes. Set once on first connection:
  ```python
  async with aiosqlite.connect(db_path) as db:
      await db.execute("PRAGMA journal_mode=WAL")
      await db.execute("PRAGMA busy_timeout=5000")
  ```

- `db-connection-factory` — Centralize connection creation in a factory function with standard PRAGMAs:
  ```python
  async def create_connection(db_path: Path) -> aiosqlite.Connection:
      db = await aiosqlite.connect(db_path)
      await db.execute("PRAGMA journal_mode=WAL")
      await db.execute("PRAGMA foreign_keys=ON")
      await db.execute("PRAGMA busy_timeout=5000")
      db.row_factory = aiosqlite.Row
      return db
  ```

- `db-no-blocking` — Never use synchronous `sqlite3` in async code. Always use `aiosqlite` or wrap with `asyncio.to_thread()`.

### 2. Query Safety (HIGH)

- `db-parameterized` — ALWAYS use parameterized queries. Never use f-strings or string concatenation for SQL:
  ```python
  # Good: parameterized
  await db.execute("SELECT * FROM skills WHERE name = ?", (skill_name,))

  # Bad: SQL injection risk
  await db.execute(f"SELECT * FROM skills WHERE name = '{skill_name}'")
  ```

- `db-row-factory` — Set `row_factory = aiosqlite.Row` for dict-like access instead of tuple indexing:
  ```python
  db.row_factory = aiosqlite.Row
  async with db.execute("SELECT id, name FROM skills") as cursor:
      async for row in cursor:
          print(row["name"])  # not row[1]
  ```

- `db-fetch-bounded` — Always limit result sets. Never `fetchall()` without a LIMIT clause on unbounded tables:
  ```python
  # Good: bounded
  await db.execute("SELECT * FROM logs ORDER BY ts DESC LIMIT ?", (max_rows,))

  # Bad: unbounded — OOM risk on large tables
  rows = await cursor.fetchall()
  ```

- `db-dataclass-mapping` — Map rows to dataclasses/Pydantic models at the boundary, not raw dicts through the codebase:
  ```python
  @dataclass
  class ConversationEntry:
      id: str
      user_input: str
      response: str
      timestamp: float

  def _row_to_entry(row: aiosqlite.Row) -> ConversationEntry:
      return ConversationEntry(**dict(row))
  ```

### 3. Schema & Migrations (HIGH)

- `db-versioned-schema` — Track schema version in a `schema_version` table. Check on startup:
  ```python
  CURRENT_SCHEMA_VERSION = 3

  async def check_schema(db: aiosqlite.Connection) -> int:
      await db.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER)")
      cursor = await db.execute("SELECT version FROM schema_version")
      row = await cursor.fetchone()
      return row["version"] if row else 0
  ```

- `db-idempotent-init` — All CREATE statements must use `IF NOT EXISTS`. Schema init must be safe to run multiple times.

- `db-no-destructive-migration` — Never DROP columns or tables in migrations. Add new columns with defaults, deprecate old ones.

- `db-migration-transaction` — Wrap each migration step in a transaction. Rollback on failure:
  ```python
  async def migrate_v2_to_v3(db: aiosqlite.Connection) -> None:
      async with db.execute("BEGIN"):
          await db.execute("ALTER TABLE conversations ADD COLUMN model TEXT DEFAULT 'unknown'")
          await db.execute("UPDATE schema_version SET version = 3")
          await db.commit()
  ```

### 4. Performance (MEDIUM)

- `db-index-queries` — Add indexes for columns used in WHERE, ORDER BY, or JOIN. Name them clearly:
  ```sql
  CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
  CREATE INDEX IF NOT EXISTS idx_skills_name ON skills(name);
  ```

- `db-batch-inserts` — Use `executemany()` for bulk inserts instead of individual INSERT loops:
  ```python
  entries = [(e.id, e.text, e.ts) for e in batch]
  await db.executemany("INSERT INTO logs VALUES (?, ?, ?)", entries)
  await db.commit()
  ```

- `db-read-only-connection` — Use separate read-only connections for queries that don't mutate:
  ```python
  async with aiosqlite.connect(f"file:{db_path}?mode=ro", uri=True) as db:
      cursor = await db.execute("SELECT * FROM conversations LIMIT 100")
  ```

- `db-vacuum-schedule` — Schedule periodic VACUUM for databases with frequent deletes. Never VACUUM during active usage.

### 5. Testing (MEDIUM)

- `db-test-in-memory` — Use `:memory:` databases for unit tests. Fast and isolated:
  ```python
  @pytest.fixture
  async def memory():
      mem = Memory(db_path=":memory:")
      await mem.initialize()
      return mem
  ```

- `db-test-fixture-data` — Use factory functions for test data, not raw SQL inserts:
  ```python
  def make_conversation(user_input: str = "test", response: str = "ok") -> ConversationEntry:
      return ConversationEntry(
          id=str(uuid4()),
          user_input=user_input,
          response=response,
          timestamp=time.time(),
      )
  ```

- `db-test-isolation` — Each test gets its own database instance. Never share state between tests.

- `db-test-migration` — Test migrations by creating a database at version N, migrating to N+1, and verifying data integrity.

## Operational Procedure

### Before coding
1. Check if `core/memory.py` already handles the storage need
2. Identify if the operation is a read or write (affects locking strategy)
3. Determine if a new table or migration is needed

### During coding
1. Use the connection factory for all new connections
2. Apply parameterized queries everywhere — no exceptions
3. Set `row_factory` for readable code
4. Use `asyncio.Lock()` for write operations

### After coding
1. Verify no raw `sqlite3` calls exist in async code paths
2. Check that all connections use `async with` (no leaks)
3. Run tests with `:memory:` database
4. Verify schema migrations are idempotent
