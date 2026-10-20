---
name: write-postgresql-code
description: >-
  Load this skill when writing PostgreSQL code in a Python service: tables, indexes, entity IDs,
  status enums, asyncpg queries and transactions, tenant isolation, pools, Alembic migrations.
  Auto-load when a table is added, asyncpg is imported, SQL is written, or alembic runs.
disable-model-invocation: false
user-invocable: false
compatibility: >-
  Requires Python 3.12+ and the `uv` package manager on PATH, plus network access to PyPI.
  `asyncpg` and `alembic` are project dependencies installed by `uv sync`, not assumed globally;
  every command runs via `uv run`. Running queries and migrations needs a reachable PostgreSQL
  server (14+) and a valid `DATABASE_URL`; `psql` is optional for ad-hoc queries. PostgreSQL is a
  separate server, not a Python package.
license: Apache-2.0
---

# Write PostgreSQL Code

Schema, queries, and migrations move together: a new table needs its DDL, the migration that creates
it, and the queries that read it. Use **asyncpg** directly — no ORM — and **Alembic** for every
schema change. Plain parameterized SQL keeps every query visible in review, where an ORM hides it.
Never modify the database schema by hand. Done when every
schema change is an Alembic migration with a working `downgrade()` and every query is parameterized
and scoped by `owner_id`.

## Procedure

1. Design the table with an application-generated ID, `owner_id`, a bounded status enum, and
   `TIMESTAMPTZ` timestamps.
2. Create or change it only through an Alembic migration with a working `downgrade()`.
3. Write the queries with parameterized placeholders, scoped by `owner_id`, with multi-step writes in a
   transaction.
4. Check the migration against deploy safety: backward-compatible, and two-step for anything destructive.

## Rules

### Schema design

```sql
CREATE TABLE entities (
    entity_id      TEXT PRIMARY KEY,
    owner_id       TEXT NOT NULL,
    status         TEXT NOT NULL DEFAULT 'active',
    state_snapshot JSONB NOT NULL DEFAULT '{}',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_entities_owner_id ON entities(owner_id);
CREATE INDEX idx_entities_status ON entities(status) WHERE status != 'deleted';
```

- `TIMESTAMPTZ` (not `TIMESTAMP`) for all timestamps. Store UTC; display local in UI.
- `JSONB` for flexible/evolving data. Typed columns for fields you filter or sort on.
- All names: `snake_case`. Table names: plural.
- Every user-owned table carries an `owner_id` column so queries can enforce tenant isolation (see
  Tenant isolation below).
- Schema changes are Alembic-managed, backward-compatible, and destructive changes are two-step (see
  Migrations below).

#### Immutable identifiers

Every entity has an application-generated, prefixed, URL-safe identifier. Never use database auto-increment as the public ID — leaks row counts and is meaningless in logs.

```python
import secrets


def generate_id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_urlsafe(12)}"


session_id = generate_id("sess")  # sess_abc123...
resource_id = generate_id("res")  # res_xyz456...
```

#### Bounded status enums

Status values must come from an explicit, closed set. Never trust free-form strings from external callers for status fields.

```python
from enum import StrEnum


class ResourceStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
```

#### Immutability rules

- IDs are set once at creation, never changed
- `created_at` timestamps are set once, never updated
- Status transitions must be validated — not all transitions are legal
- Document all legal and illegal transitions explicitly

### Queries

Explicit SQL with parameterized placeholders. Never interpolate values into the query string.

```python
row = await conn.fetchrow(
    "SELECT session_id, topic FROM sessions WHERE session_id = $1", session_id
)
```

Page a list with a keyset scan on a unique sort key, never `OFFSET`: an offset re-reads every
skipped row, so page 1,000 costs a thousand pages, and a concurrent insert shifts rows between
pages. Back the sort key with an index on the same columns in the same order.

```python
rows = await conn.fetch(
    "SELECT session_id, topic, created_at FROM sessions"
    " WHERE (created_at, session_id) < ($1, $2)"
    " ORDER BY created_at DESC, session_id DESC LIMIT $3",
    cursor_created_at,
    cursor_session_id,
    limit,
)
```

### Tenant isolation

Every query on user-owned data must filter by the owning user's ID. One user's data must never be reachable by another.

```python
await conn.fetchrow(
    "SELECT * FROM resources WHERE resource_id = $1 AND owner_id = $2",
    resource_id,
    current_user_id,
)
```

### Atomic transactions

Use transactions for all multi-step writes:

```python
async with pool.acquire() as conn:
    async with conn.transaction():
        await conn.executemany(
            "INSERT INTO order_items (order_id, sku, qty) VALUES ($1, $2, $3)",
            [(order_id, i.sku, i.qty) for i in items],
        )
        await conn.execute(
            "UPDATE orders SET total = $1, updated_at = NOW() WHERE order_id = $2",
            new_total,
            order_id,
        )
```

Never assign an ordered number with `SELECT MAX(n) + 1`: two concurrent transactions read the same
maximum and write the same number. Use an identity column or a sequence, or lock the parent row
with `SELECT ... FOR UPDATE` inside the transaction that assigns it.

### Connection pool

```python
pool = await asyncpg.create_pool(
    dsn=settings.database_url,
    min_size=5,
    max_size=20,
    command_timeout=30,
)
```

Create the pool in the FastAPI lifespan function and expose it via `app.state.db_pool`. Never create a pool per request.

### Migrations

#### Setup

```bash
uv add alembic
uv add --dev psycopg2-binary   # sync driver for Alembic; asyncpg is for runtime only
uv run alembic init alembic
```

Configure `alembic/env.py` to use a sync URL (Alembic does not support asyncpg):

```python
sync_url = str(settings.database_url).replace("+asyncpg", "")
config.set_main_option("sqlalchemy.url", sync_url)
```

#### Commands

```bash
uv run alembic revision --autogenerate -m "add users table"
uv run alembic upgrade head
uv run alembic downgrade -1
uv run alembic current
uv run alembic history
```

Apply before integration/system tests:

```bash
DATABASE_URL=$TEST_DATABASE_URL uv run alembic upgrade head
```

#### Migration rules

- Always implement `downgrade()` — every migration must be reversible
- Never edit an applied migration — create a new one instead
- Review every autogenerated file before committing: Alembic misses index names, check constraints, and custom types
- One logical schema change per migration file

#### Deploy safety

- Migrations run **before** the new application version deploys (blue-green safe)
- Every migration must be backward-compatible — the **old** app version must still work after the migration runs
- Never run a migration and a code deploy simultaneously
- Test the migration against a copy of production data before deploying

#### Zero-downtime DDL

A migration that holds a strong lock on a busy table blocks every query behind it. On any table
that serves traffic:

- Set `SET lock_timeout = '5s'` at the top of the migration, so a blocked `ALTER` fails fast and
  can be retried instead of queueing every read behind it.
- Create indexes with `CREATE INDEX CONCURRENTLY`, inside
  `with op.get_context().autocommit_block():`, because it cannot run in a transaction.
- Add a foreign key or check constraint as `NOT VALID`, then `VALIDATE CONSTRAINT` in a separate
  migration. Validation takes a weaker lock than adding a validated constraint.
- Add a `NOT NULL` column in three steps: add it nullable, backfill in batches of a few thousand
  rows per transaction, then set `NOT NULL`. On PostgreSQL 12+, add a `CHECK (col IS NOT NULL)
NOT VALID` and validate it first, so `SET NOT NULL` skips the full-table scan.
- Never backfill a large table in the migration itself. Run it as a separate batched script, so a
  slow backfill does not hold the deploy.

#### Two-step destructive changes

Never drop a column, rename a column, or remove a table in a single release.

**Step 1 (this release):** Deploy code that no longer uses the old structure. Old structure stays in place.

**Step 2 (next release):** Drop the old structure now that no code references it.

```sql
-- Step 1 migration: add new column
ALTER TABLE resources ADD COLUMN new_column TEXT;

-- Step 2 migration (next release only): drop old column
ALTER TABLE resources DROP COLUMN old_column;
```
