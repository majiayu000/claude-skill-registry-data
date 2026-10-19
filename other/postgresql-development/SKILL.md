---
name: postgresql-development
description: >
  Design, optimize, migrate, and secure PostgreSQL databases (supported majors 14-18,
  18 current). Use when indexing JSONB with GIN or expression indexes, reading query
  plans with EXPLAIN (ANALYZE, BUFFERS), writing low-lock schema migrations
  (CREATE INDEX CONCURRENTLY, NOT VALID constraints), diagnosing lock waits and
  invalid indexes, configuring Row-Level Security for multi-tenant apps, or choosing
  transaction isolation and retry behavior. Do not use for MySQL/SQLite dialects,
  ORM-only questions with no SQL decision, or managed-service operations such as
  backup and failover runbooks.
compatibility: >
  Agent Skills-compatible coding agents writing SQL or migrations for PostgreSQL 14+.
  Facts checked against PostgreSQL 18 documentation (October 2026; 18.x current,
  14 reaches end of life on 2026-11-12). Executing statements needs a database the
  user has authorized; never run DDL against production without explicit approval.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "postgresql, postgres, jsonb, explain, gin, rls, migrations, locking, sql"
  topics: "databases, software-development"
---

# PostgreSQL Development and Optimization

PostgreSQL offers GIN/GiST/BRIN/B-tree indexes, `JSONB`, ranges, Row-Level Security (RLS), and detailed plan diagnostics. Most production incidents come from three things: a migration that takes a stronger lock than expected, a plan chosen on bad statistics, and a security policy that silently does not apply. This skill teaches how to avoid and diagnose those.

Deeper material:
- [Migration locking cheat sheet](references/migration-locking.md)
- [Diagnosing slow queries, lock waits, and invalid indexes](references/troubleshooting.md)

## When to use / not use

Use for PostgreSQL schema, query, index, migration, and RLS decisions. For application-level injection review use `security-code-review`; for generic SQL comment style use `code-comments`. Do not apply Postgres-only syntax (`CONCURRENTLY`, `JSONB`, `ON CONFLICT`) to other databases.

## Core rules

1. **Read-only first.** Diagnose with `EXPLAIN`, `pg_stat_activity`, and catalog views before changing anything. Never run DDL, `VACUUM FULL`, or `REINDEX` on a production system without the user's explicit approval.
2. **`EXPLAIN ANALYZE` executes the statement.** For `INSERT/UPDATE/DELETE`, wrap it: `BEGIN; EXPLAIN (ANALYZE, BUFFERS) ...; ROLLBACK;`.
3. **Know the lock before you run DDL.** Plain `CREATE INDEX` takes a `SHARE` lock: reads continue, writes block until it finishes. `CREATE INDEX CONCURRENTLY` (SHARE UPDATE EXCLUSIVE) avoids blocking writes but is slower, cannot run inside a transaction block, and can fail leaving an `INVALID` index that you must drop and retry.
4. **Always set `lock_timeout` for migrations** (for example `SET lock_timeout = '3s'`) and retry. A DDL statement waiting for a lock queues every later query behind it, so a "fast" migration behind one long transaction becomes an outage.
5. **Use `JSONB`, not `json` or `text`, when you query inside the document.** Use plain columns for fields you filter or join on constantly.
6. **Parameterize all queries.** Never build SQL by string concatenation with user data; identifiers need `format('%I')` or an allow-list.
7. **RLS is a safety net with sharp edges** (owner bypass, superuser bypass, views, empty-string settings). Test it as the application role.
8. **Fix statistics before blaming the planner.** Large gaps between estimated and actual rows mean run `ANALYZE`, raise statistics targets, or add extended statistics.

## 1. JSONB indexing: pick the index for the operator

```sql
CREATE TABLE audit_events (
    id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type text NOT NULL,
    metadata   jsonb NOT NULL DEFAULT '{}',
    created_at timestamptz NOT NULL DEFAULT now()
);

-- Containment queries (@>) only: smaller and faster than the default operator class
CREATE INDEX CONCURRENTLY idx_audit_events_meta_pathops
    ON audit_events USING gin (metadata jsonb_path_ops);

-- One hot key filtered with equality: an expression B-tree is smaller and faster than GIN
CREATE INDEX CONCURRENTLY idx_audit_events_tenant
    ON audit_events ((metadata ->> 'tenant_id'));
```

- Default GIN (`jsonb_ops`) also supports key-existence operators (`?`, `?|`, `?&`); `jsonb_path_ops` supports `@>` and jsonpath match operators but not key existence.
- The query must use the same expression as the index (`metadata ->> 'tenant_id' = 'cust_441'`).
- `gen_random_uuid()` is built in since PostgreSQL 13. PostgreSQL 18 adds `uuidv7()`, which is time-ordered and friendlier to B-tree locality; random UUIDs scatter inserts.
- GIN indexes slow writes; measure before adding several.

## 2. Reading a plan

```sql
EXPLAIN (ANALYZE, BUFFERS, SETTINGS)
SELECT u.id, count(o.id)
FROM users u JOIN orders o ON o.user_id = u.id
WHERE u.created_at >= '2026-01-01'
GROUP BY u.id;
```

PostgreSQL 18 adds `BUFFERS` automatically with `ANALYZE`; keep it explicit so the command works on 14-17. What to read:

- **Estimated vs actual rows** per node: a 100x gap points to stale or insufficient statistics (`ANALYZE`, `ALTER TABLE ... ALTER COLUMN ... SET STATISTICS`, `CREATE STATISTICS` for correlated columns).
- **`Buffers: shared hit` vs `read`**: `read` counts blocks fetched outside shared buffers (possibly the OS cache), so it is not proof of physical disk I/O.
- **Seq Scan is not automatically wrong.** For small tables or queries returning a large fraction of rows it is the cheapest plan. Investigate when a selective filter scans a big table and the index you expect exists.
- **`Rows Removed by Filter`** large relative to rows returned suggests a missing or unusable index (function wrapped around the column, type mismatch, leading-column mismatch in a composite index).
- **Loops**: multiply per-loop times by `loops` when judging a nested loop's inner side.
- Compare cold and warm runs; one timing is not evidence.

## 3. Low-lock migrations (summary; details in the reference)

```sql
SET lock_timeout = '3s';   -- per migration session; retry on failure

-- Index without blocking writes (outside a transaction block)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_customer_date
    ON orders (customer_id, ordered_at DESC);
-- Afterwards verify it is valid:
-- SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;

-- Foreign key in two steps
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
    REFERENCES customers (id) NOT VALID;      -- brief lock, no scan
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_customer;  -- scans, allows writes
```

- Adding a column with a constant (or stable-function) default is a metadata-only change since PostgreSQL 11, with or without `NOT NULL`. A *volatile* default (for example `random()`, `clock_timestamp()`) rewrites the table.
- `ALTER COLUMN ... SET NOT NULL` scans the table under a strong lock unless a validated `CHECK (col IS NOT NULL)` already exists (PostgreSQL 12+): add the check `NOT VALID`, validate it, then set NOT NULL, then drop the check.
- Changing a column type often rewrites the table; use add-column, backfill in batches, swap.
- Index on a foreign-key column in the child table is not automatic; add it or deletes on the parent will scan the child.

## 4. Row-Level Security

```sql
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents FORCE ROW LEVEL SECURITY;   -- applies to the table owner too

CREATE POLICY tenant_isolation ON documents
    USING      (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid)
    WITH CHECK (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);
```

Set the tenant per transaction with a parameterizable call (SET cannot take bind parameters):

```sql
BEGIN;
SELECT set_config('app.current_tenant_id', $1, true);  -- true = local to this transaction
SELECT id FROM documents;
COMMIT;
```

Gotchas:
- Superusers and roles with `BYPASSRLS` ignore policies; table owners ignore them unless `FORCE` is set. The application must connect as a plain, non-owner role.
- After a custom setting has been used once in a session, `current_setting(..., true)` can return an empty string rather than NULL. Casting `''` to `uuid` raises an error, so use `NULLIF(..., '')`. Missing context then yields NULL and no rows (fails closed).
- `USING` filters rows read or targeted; `WITH CHECK` validates new rows. Without `WITH CHECK` on a `FOR ALL` policy the `USING` expression is reused, but state it explicitly.
- Views run with the owner's rights and can bypass RLS; use `security_invoker = true` on views (PostgreSQL 15+) for tenant tables.
- With transaction-mode connection poolers, use the transaction-local form above; session-level `SET` leaks to the next client.
- RLS does not protect against covert channels such as unique-constraint errors; it is defense in depth, not a substitute for authorization in the application.

## 5. Transactions and isolation

- Default `READ COMMITTED`: each statement sees a fresh snapshot. `REPEATABLE READ`: one snapshot per transaction; concurrent updates to a row you changed raise serialization failures. `SERIALIZABLE`: strongest; may abort any transaction.
- Code using `REPEATABLE READ` or `SERIALIZABLE` must retry on SQLSTATE `40001` (and `40P01` for deadlocks) with a bounded retry loop.
- Keep transactions short; long idle-in-transaction sessions hold back vacuum and block DDL. Consider `idle_in_transaction_session_timeout`.
- Use `statement_timeout` per role or transaction for application traffic; do not set it globally low for migrations and maintenance.

## 6. Anti-patterns

| Anti-pattern | Risk | Instead |
| :--- | :--- | :--- |
| Plain `CREATE INDEX` on a busy table | Blocks writes for the whole build | `CREATE INDEX CONCURRENTLY`, then check `indisvalid` |
| Migration without `lock_timeout` | Lock queue outage | Short `lock_timeout` and retry |
| `EXPLAIN ANALYZE` of a DELETE on production | The delete happens | Wrap in a transaction and roll back, or use a copy |
| Treating every Seq Scan as a bug | Needless indexes, slower writes | Check selectivity and row counts first |
| `OFFSET 100000` pagination | Scans and discards rows | Keyset pagination on an indexed, unique ordering |
| `uuid` stored as `varchar(36)` | Double the size, slower compares | Native `uuid` |
| `WHERE id IN (...)` with thousands of literals | Huge plans | `id = ANY($1::bigint[])` |
| RLS tested as superuser | Policies appear to work but are bypassed | Test as the application role |
| `SET app.tenant = ...` on pooled connections | Cross-tenant leak | `set_config(..., true)` inside a transaction |

## 7. Verification checklist

- [ ] Plans were read with `ANALYZE` (inside a rollback for writes) and compared estimate vs actual.
- [ ] New indexes built `CONCURRENTLY` and confirmed valid; unused/duplicate indexes considered.
- [ ] Migration has `lock_timeout`, avoids table rewrites, and was rehearsed on production-sized data.
- [ ] RLS tested as the application role with missing, valid, and foreign tenant context.
- [ ] Retry logic exists for `40001`/`40P01` where needed.
- [ ] The PostgreSQL major version in use is supported (14 ends 2026-11-12).

## Sources

- PostgreSQL documentation (current): https://www.postgresql.org/docs/current/
- Versioning policy: https://www.postgresql.org/support/versioning/
- EXPLAIN, CREATE INDEX, ALTER TABLE, Row Security Policies, Explicit Locking chapters of the manual.
