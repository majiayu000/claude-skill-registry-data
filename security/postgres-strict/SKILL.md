---
name: postgres-strict
description: >
  PostgreSQL strictness, schema design, indexing, migration safety, and operational
  rules. Use when designing schemas, writing queries, reviewing migrations, tuning
  performance, or hardening a Postgres deployment. Targets PostgreSQL 16-18, with
  notes on pgvector, partitioning, and RLS. Pairs with security-audit-standard and
  performance-audit-standard.
---

# PostgreSQL Strict Standard

Rules for production Postgres. Targets 16+ with notes for 17/18 features.

## Version Targets

PostgreSQL 18 is GA (released Sept 2025). New deployments should target 18. Highlights worth designing around:

- **Async I/O subsystem (AIO)**: sequential scans, bitmap heap scans, and `VACUUM` issue concurrent reads instead of blocking each one. Up to ~3x faster on bulk-read workloads. No code change required.
- **Skip scan on B-tree indexes**: multicolumn indexes can now be used when the leading column is not in the predicate, reducing the need for redundant index variants.
- **Parallel GIN index builds**: `CREATE INDEX ... USING gin` runs in parallel. Big win for JSONB and full-text builds on large tables.
- **`uuidv7()` native**: no extension required (see PG-26 below).
- **Virtual generated columns are the default**: stored columns require explicit `STORED`. Virtual columns compute on read, no write amplification.
- **`OLD` and `NEW` in `RETURNING`**: capture the row state before and after `UPDATE`/`DELETE`/`MERGE` in one statement.
- **OAuth 2.0 authentication in libpq**: easier SSO integration.
- **Planner stats survive major version upgrades**: post-upgrade clusters reach steady-state performance much faster, no immediate `ANALYZE` storm.

## CRITICAL: Migration Safety

A migration is a contract with a running system. The wrong migration takes prod down.

### PG-01: `CREATE INDEX CONCURRENTLY` on hot tables

```sql
-- BAD: takes ACCESS EXCLUSIVE lock for the duration of the build
CREATE INDEX events_user_id_idx ON events (user_id);

-- GOOD: short ACCESS EXCLUSIVE on metadata, no row lock during build
CREATE INDEX CONCURRENTLY events_user_id_idx ON events (user_id);
```

`CONCURRENTLY` cannot run inside a transaction block. Migration tools that wrap statements in BEGIN/COMMIT must opt out for these statements. Failed concurrent index builds leave an INVALID index, drop and retry.

### PG-02: Add NOT NULL columns in two steps

```sql
-- BAD: rewrites the whole table while holding ACCESS EXCLUSIVE
ALTER TABLE users ADD COLUMN status text NOT NULL DEFAULT 'active';

-- GOOD on PG 11+ for defaults, but still problematic if you need NOT NULL on existing nulls
ALTER TABLE users ADD COLUMN status text DEFAULT 'active';
-- Backfill in batches in app code
UPDATE users SET status = 'active' WHERE status IS NULL AND id BETWEEN $1 AND $2;
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
```

PG 11+ added fast non-volatile defaults. The lock duration for `SET NOT NULL` still scans the table, schedule it for a quiet window or use `NOT VALID` constraint pattern below.

### PG-03: Add CHECK / FOREIGN KEY as `NOT VALID`, then `VALIDATE`

```sql
ALTER TABLE orders
  ADD CONSTRAINT orders_amount_positive CHECK (amount > 0) NOT VALID;
-- Validates only new rows, completes instantly

ALTER TABLE orders VALIDATE CONSTRAINT orders_amount_positive;
-- Scans the table without an ACCESS EXCLUSIVE lock
```

Same pattern for foreign keys.

### PG-04: Set `lock_timeout` and `statement_timeout` in migrations

```sql
SET lock_timeout = '5s';
SET statement_timeout = '10min';
```

A migration that waits forever on a lock is worse than a migration that fails fast.

## CRITICAL: Indexing

### PG-05: Index every column used in `WHERE`, `JOIN`, or `ORDER BY` on hot queries

Use `EXPLAIN (ANALYZE, BUFFERS)` to verify plan. A `Seq Scan` on a million rows is not always wrong, but on a hot query it almost always is.

### PG-06: Composite index column order: equality first, then range

```sql
-- Query: WHERE user_id = $1 AND created_at > $2 ORDER BY created_at DESC
CREATE INDEX events_user_created_idx ON events (user_id, created_at DESC);
```

Equality on the leading column lets Postgres use the index for the range and the sort.

### PG-07: Partial indexes for skewed predicates

```sql
-- Most rows are processed, only a few are pending
CREATE INDEX jobs_pending_idx ON jobs (created_at) WHERE status = 'pending';
```

Smaller index, faster scans for the common query.

### PG-08: GIN for JSONB / array / full text

```sql
-- For @>, ?, ?| queries on JSONB
CREATE INDEX docs_data_gin ON docs USING gin (data jsonb_path_ops);

-- For arrays: WHERE tags @> ARRAY['urgent']
CREATE INDEX items_tags_gin ON items USING gin (tags);
```

`jsonb_path_ops` is smaller and faster than the default opclass when you only need containment.

### PG-09: HNSW (not IVFFlat) for new pgvector indexes

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE INDEX docs_embedding_hnsw ON docs
  USING hnsw (embedding vector_l2_ops)
  WITH (m = 16, ef_construction = 64);

-- Per-query recall/speed tradeoff
SET hnsw.ef_search = 100;
```

HNSW is the default recommendation in pgvector 0.5+. IVFFlat needs retraining as data changes.

## HIGH: Query Patterns

### PG-10: Never `SELECT *` in application queries

Selects every column even when only a few are needed. Breaks when columns are added (extra bandwidth, broken row decoders). List columns explicitly.

### PG-11: Parameterized queries always

```typescript
// BAD: SQL injection
db.query(`SELECT * FROM users WHERE email = '${email}'`);

// GOOD: parameterized
db.query("SELECT id, name FROM users WHERE email = $1", [email]);
```

Every driver supports `$1, $2, ...` placeholders. Use them.

### PG-12: `LIMIT` every unbounded query

```sql
-- BAD: a single misclick returns 50M rows
SELECT id, payload FROM events WHERE user_id = $1;

-- GOOD: paginate
SELECT id, payload FROM events WHERE user_id = $1 ORDER BY id LIMIT 100;
```

For pagination at scale, use keyset (`WHERE id > $last_id`), not `OFFSET`.

### PG-13: `MERGE` for upserts (PG 15+, with `RETURNING` in 17+)

```sql
MERGE INTO users u
USING (VALUES ($1, $2)) AS s(email, name) ON u.email = s.email
WHEN MATCHED THEN UPDATE SET name = s.name
WHEN NOT MATCHED THEN INSERT (email, name) VALUES (s.email, s.name)
RETURNING u.id;  -- PG 17+
```

`INSERT ... ON CONFLICT DO UPDATE` still works and is fine for simple upserts.

### PG-14: `EXPLAIN (ANALYZE, BUFFERS)` before declaring a query fast

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ... ;
```

`BUFFERS` shows how much you read from cache vs. disk. A query that is fast in dev with a hot cache can be slow in prod with a cold one.

## HIGH: Transactions

### PG-15: Default isolation level is `READ COMMITTED`, raise it deliberately

| Level | When |
|---|---|
| READ COMMITTED | Default, fine for most CRUD |
| REPEATABLE READ | Reports, batch jobs that need a stable view |
| SERIALIZABLE | Money transfers, balance updates, anything where lost updates corrupt state |

`SERIALIZABLE` can fail with `40001 serialization_failure`. Application must retry.

### PG-16: Lock rows you intend to update with `FOR UPDATE`

```sql
BEGIN;
SELECT balance FROM accounts WHERE id = $1 FOR UPDATE;
-- compute new balance
UPDATE accounts SET balance = $2 WHERE id = $1;
COMMIT;
```

Without `FOR UPDATE`, two concurrent transactions both read, both compute, last writer wins.

### PG-17: Keep transactions short

Every open transaction holds locks and prevents `VACUUM` from cleaning rows newer than its snapshot. Long-running transactions cause table bloat. No HTTP calls, no user-facing waits inside a transaction.

## HIGH: Connection Management

### PG-18: PgBouncer in transaction pooling mode for most apps

Postgres connections are heavyweight (10-20 MB each, fork per backend). A serverless or busy app saturates the server without a pooler.

| Pool mode | When |
|---|---|
| Session | Need session-state features (advisory locks, prepared statements, `SET`) |
| Transaction | Default for stateless apps |
| Statement | Rare, breaks transactions |

Transaction pooling forbids `LISTEN/NOTIFY`, session advisory locks, and certain `SET` calls in client code. Use `SET LOCAL` inside transactions instead.

### PG-19: Set per-role timeouts

```sql
ALTER ROLE app_user SET statement_timeout = '30s';
ALTER ROLE app_user SET lock_timeout = '5s';
ALTER ROLE app_user SET idle_in_transaction_session_timeout = '60s';
```

A runaway query should never take down the database.

## HIGH: Security

### PG-20: `scram-sha-256` for password auth, never `md5`

```ini
# postgresql.conf
password_encryption = scram-sha-256

# pg_hba.conf
hostssl all all 0.0.0.0/0 scram-sha-256
```

Rotate any md5-hashed passwords. They are downgrade-attackable.

### PG-21: TLS required for non-loopback connections

```ini
# postgresql.conf
ssl = on
ssl_min_protocol_version = 'TLSv1.2'
```

Reject `host` (plain) lines in `pg_hba.conf` for anything but `127.0.0.1` / Unix sockets.

### PG-22: Least-privilege roles, no app-as-superuser

```sql
CREATE ROLE app_readwrite;
GRANT CONNECT ON DATABASE mydb TO app_readwrite;
GRANT USAGE ON SCHEMA public TO app_readwrite;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_readwrite;

CREATE ROLE app_user LOGIN PASSWORD '...' IN ROLE app_readwrite;
```

Migration role is separate and more privileged. Application role cannot DROP, ALTER, or CREATE.

### PG-23: Row-Level Security for multi-tenant tables

```sql
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY projects_tenant_isolation ON projects
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Per request
SET LOCAL app.tenant_id = '...';
```

Defense in depth. Even an SQL injection that bypasses application checks cannot leak across tenants.

## MEDIUM: Observability

### PG-24: `pg_stat_statements` always enabled

```ini
shared_preload_libraries = 'pg_stat_statements'
```

```sql
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

Reveals the slow queries actually hitting the database. Read this before adding any optimization.

### PG-25: Track these baseline metrics

| Metric | Source | Alert if |
|---|---|---|
| Replication lag | `pg_stat_replication.replay_lag` | > 10s sustained |
| Connection count | `pg_stat_activity` | > 80% of `max_connections` |
| Cache hit ratio | `pg_stat_database.blks_hit / (blks_hit + blks_read)` | < 0.99 |
| Bloat | `pgstattuple` or pgbloat scripts | dead tuples > 20% of table |
| Long transactions | `pg_stat_activity` where `xact_start < now() - interval '5min'` | any |

## MEDIUM: Schema Design

### PG-26: UUIDv7 for new PKs (PG 18 native, otherwise extension)

```sql
-- PG 18+
CREATE TABLE events (id uuid PRIMARY KEY DEFAULT uuidv7(), ...);

-- PG <18: use uuid-ossp or app-side generation
CREATE TABLE events (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), ...);
```

UUIDv7 is time-ordered, gives B-tree-friendly inserts and works across services without coordination.

### PG-27: Use `timestamptz`, never `timestamp`

```sql
created_at timestamptz NOT NULL DEFAULT now()
```

`timestamp without time zone` discards offset and silently corrupts data when the server timezone changes.

### PG-28: Partition large append-only tables

```sql
CREATE TABLE events (
    id bigserial,
    created_at timestamptz NOT NULL,
    payload jsonb
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_01 PARTITION OF events
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

Drop a month by detaching a partition. `VACUUM` and indexes scale per-partition.

## Migration Tooling Baseline

Required regardless of tool (sqlx, Atlas, Flyway, Prisma Migrate):

- One forward migration per file, no destructive `DROP` without confirmation
- File names sortable (`0001_`, `0002_`, or timestamps)
- Migrations checked in, never edited after merge
- Tool runs on a dedicated migration role, not the app role
- CI runs migrations against a fresh DB on every PR

## Vulnerability Checklist

- [ ] All connections use TLS (`ssl = on`)
- [ ] Password auth is `scram-sha-256`, no `md5`
- [ ] App role is not superuser, cannot DROP/ALTER
- [ ] `pg_stat_statements` enabled and reviewed
- [ ] `lock_timeout` and `statement_timeout` set per role
- [ ] Long transactions monitored and alerted
- [ ] Backups: PITR or daily full + WAL archive
- [ ] Restore tested at least quarterly
- [ ] Index-creating migrations use `CONCURRENTLY`
- [ ] Multi-tenant tables use Row-Level Security
- [ ] Connection pooler (PgBouncer) sits between app and Postgres
