---
name: postgres-patterns
description: "Use when designing PostgreSQL schema features or applying advanced Postgres patterns in Laravel — GIN/BRIN/partial/covering indexes, jsonb, ON CONFLICT upserts, SKIP LOCKED queue workers, cursor pagination, RLS, and timestamptz/numeric typing — beyond the query tuning already in the SQL rules."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/sql/optimalize.md` — it already owns indexing fundamentals, SARGable WHERE, seek/keyset pagination, EXPLAIN, transactions/locking basics, and batch-over-per-row. Do not re-explain those; defer to it. Note it is written for MySQL — translate engine-specific syntax (`EXPLAIN ANALYZE`, plan flags) to Postgres equivalents here.
- **Its schema-design block is MySQL-only — do not defer to it on Postgres.** Everything in that rule from `## Schema Design` through `## When to Break These Rules` is scoped to MySQL 8.0.16+ on InnoDB, and several of its mandates are not a syntax translation but the opposite advice on Postgres: `TIMESTAMP` is banned there (a 32-bit type with a 2038 limit) while both Postgres timestamp types are 64-bit and carry no such limit — so the MySQL prohibition does not transfer, and the type to reach for here is `timestamptz` per **Data Type Discipline** below, never plain `timestamp`. `UNSIGNED` does not exist at all, and neither does `utf8mb4` or its collation family.
The engine-neutral half — naming discipline, nullability semantics, `CHECK` as invariant-not-policy, foreign-key actions, explicit constraint names, `numeric` over float for money — still applies; take that, and use **Data Type Discipline** below plus the sections in this skill for the rest.
- This skill is the Postgres counterpart to `@skills/mysql-patterns/SKILL.md`. It is for *designing* features. For diagnosing an existing slow query, the closest fit is `@skills/mysql-problem-solver/SKILL.md` (apply its method; substitute Postgres EXPLAIN/`pg_stat_statements`).
- If the project uses Laravel, also apply `@rules/laravel/laravel.md` and `@rules/laravel/architecture.md`.
- Apply `@rules/security/backend.md` — parameterized queries / Eloquent only, least-privilege DB users, never hardcode credentials.
- `final` classes, `declare(strict_types=1)`, Pest tests for any data-access code added.
- Confirm the major version (`SELECT version();`) before using version-specific features — `MERGE` (15+), covering `INCLUDE` indexes (11+), and `NULLS NOT DISTINCT` (15+) are not in older servers.

## Modes

This skill runs in one of two modes, selected by the caller via `MODE` (default `design`):

- **`design` (default)** — full design work: write migrations, add indexes, change column types, and set connection configuration. Every section below behaves as written unless it is explicitly flagged for `MODE=cr`.
- **`cr` (read-only lens — invoked by `@skills/code-review/SKILL.md`, `code-review-github`, `code-review-jira`, and `code-review-bugsnag` when the reviewed project's database engine resolves to `pgsql`)** — **never modify code, never author a migration or a test, never stage / commit / push, never run fixers or checkers, and never chain a follow-up review.** Scope the analysis to the lines added or modified by the PR diff and return the findings as markdown only, for the CR to fold into its single `## Database Analysis` section.
Every instruction below that would touch the database, a migration, or configuration — create, add, alter, index, enable, set, or any other such verb — is emitted as a written proposal carrying a concrete SQL / query-builder snippet, never applied to the project.

## Use when
- Adding jsonb columns, GIN/BRIN/partial/covering indexes, or full-text search to a Laravel app on Postgres.
- Building a queue/worker that pulls jobs with `FOR UPDATE SKIP LOCKED`, or paginating large result sets by cursor.
- Adding `ON CONFLICT` upserts, Row-Level Security for multi-tenancy, or correct `timestamptz`/`numeric` typing.
- Reviewing a migration that introduces any of the above on a large table.

Set `DB_CONNECTION=pgsql`. These topics complement the query-tuning rules; they are not covered there.

## Data Type Discipline

Pick the right type once — wrong choices are expensive to migrate later.

```php
Schema::create('orders', function (Blueprint $table): void {
    $table->id();                                  // bigint identity
    $table->decimal('amount', 12, 2);              // numeric — never float/double for money
    $table->timestampTz('placed_at');              // timestamptz — stores UTC instant
    $table->jsonb('meta')->default('{}');          // jsonb (binary, indexable), not json
    $table->boolean('is_paid')->default(false);
});
```

- `timestampTz` maps to `timestamptz`: it stores a UTC instant and converts on read. Plain `timestamp` drops the zone and is a recurring bug source. Set `'timezone' => 'UTC'` server-side.
- `numeric`/`decimal` for money and exact values; `float`/`double` lose precision.
- `jsonb` over `json`: binary form supports GIN indexing and `@>`/`?` operators; plain `json` only stores text.
- `text` has no performance cost over `varchar(n)` in Postgres — use `text` unless a length cap is a real constraint.

## Upserts (ON CONFLICT)

```php
// Eloquent upsert compiles to INSERT ... ON CONFLICT DO UPDATE.
// 2nd arg = conflict target (must be backed by a unique index); 3rd = columns to overwrite.
Product::upsert(
    [['sku' => 'A1', 'price' => 10], ['sku' => 'B2', 'price' => 20]],
    uniqueBy: ['sku'],
    update: ['price'],
);

// Insert, skip rows that violate a unique constraint:
DB::table('tags')->insertOrIgnore([['name' => 'php'], ['name' => 'sql']]);
```

```sql
-- Raw equivalent. EXCLUDED = the row that failed to insert.
INSERT INTO products (sku, price) VALUES ('A1', 10)
ON CONFLICT (sku) DO UPDATE SET price = EXCLUDED.price;
```

- The conflict target **must** be backed by a unique index/constraint, or the statement errors. `upsert()` and `insertOrIgnore()` are bulk single statements and do not fire model events or set timestamps — set them yourself.
- `updateOrCreate()` is per-row, fires events, and is race-prone unless a unique index backs the match columns; wrap concurrent use in a transaction retry.

## Indexing Beyond B-tree

> **`MODE=cr`:** this section carries the deploy-safety answer `@rules/code-review/core-analysis.md` *Deploy-safe schema changes (issue #20)* redirects a PostgreSQL project to. Raise a blocking index build on a populated table as a finding whose **Suggested Fix** is `CREATE INDEX CONCURRENTLY` with the migration's wrapping transaction disabled (`public $withinTransaction = false;`) — never `ALGORITHM=INPLACE, LOCK=NONE`, `pt-online-schema-change`, or `gh-ost`, none of which PostgreSQL parses or supports. Name the reversal too: a failed `CONCURRENTLY` build leaves an invalid index behind, so `down()` drops that index explicitly.

B-tree (the default) covers equality/range. Reach for these when the access pattern differs:

```sql
-- GIN: jsonb containment and array/full-text membership.
CREATE INDEX idx_orders_meta ON orders USING gin (meta jsonb_path_ops);

-- BRIN: huge, naturally-ordered columns (append-only time series). Tiny index, range scans only.
CREATE INDEX idx_events_created ON events USING brin (created_at);

-- Partial: index only the rows you actually query — smaller, cheaper to maintain.
CREATE INDEX idx_users_active ON users (email) WHERE deleted_at IS NULL;

-- Covering (11+): satisfy a query from the index alone (index-only scan).
CREATE INDEX idx_orders_lookup ON orders (customer_id) INCLUDE (status, amount);
```

```php
// In a Laravel migration, raw index types go through DB::statement.
DB::statement('CREATE INDEX idx_orders_meta ON orders USING gin (meta jsonb_path_ops)');
DB::statement('CREATE INDEX idx_users_active ON users (email) WHERE deleted_at IS NULL');
```

- `jsonb_path_ops` is smaller and faster for `@>` containment than the default `jsonb_ops` (which also supports key-existence `?`). Pick by the operators you use.
- BRIN only helps when physical row order tracks the column (insert order ≈ time order). On randomly-ordered data it is useless.
- A partial index matching the model's default scope (e.g. soft-delete `WHERE deleted_at IS NULL`) is often the highest-leverage index on a soft-deleted table.
- On large/live tables build with `CREATE INDEX CONCURRENTLY` (cannot run inside a transaction — disable the migration's wrapping transaction with `public $withinTransaction = false;`).

## jsonb Querying

```php
Product::where('meta->color', 'red')->get();              // ->  meta->>'color' = 'red'
Product::whereJsonContains('meta->tags', 'sale')->get();  // ->  meta @> '{"tags":["sale"]}'
```

- `->` returns jsonb, `->>` returns text. Index and compare on `->>` (text) for scalar lookups; use the GIN `@>` containment path for membership.
- Validate jsonb shape in the application; Postgres enforces only that it is valid JSON, not its structure.

## Queue Workers (FOR UPDATE SKIP LOCKED)

Lets N workers each grab a distinct unlocked row with no contention or double-processing.

```php
$job = DB::transaction(function () {
    $row = DB::table('jobs')
        ->where('status', 'pending')
        ->orderBy('id')
        ->lockForUpdate()          // FOR UPDATE
        ->limit(1)
        ->skipLocked()             // SKIP LOCKED — skip rows another worker holds
        ->first();

    if ($row !== null) {
        DB::table('jobs')->where('id', $row->id)->update(['status' => 'processing']);
    }
    return $row;
});
```

- `skipLocked()` makes workers ignore rows already locked instead of blocking — the core primitive for a Postgres-backed work queue.
- Keep the transaction short: lock, claim status, commit; do the actual work outside the lock.
- Laravel's `QUEUE_CONNECTION=database` driver already uses this internally; hand-roll only for custom claim logic.

## Cursor Pagination

For large/deep result sets, keyset (cursor) pagination is O(1) per page vs OFFSET's O(n) scan-and-discard.

```php
// Laravel's built-in keyset paginator (opaque cursor over the ORDER BY columns).
Order::orderBy('id')->cursorPaginate(20);
```

```sql
-- Raw seek: carry the last row's key forward instead of OFFSET.
SELECT * FROM orders WHERE id > :last_id ORDER BY id LIMIT 20;
```

- The cursor columns must match the `ORDER BY` and be backed by an index (composite for multi-column sorts, including a unique tiebreaker).
- See seek-pagination guidance in `@rules/sql/optimalize.md`; this is its Postgres-native form.

## Row-Level Security (multi-tenancy)

Enforce per-tenant isolation in the database so a missing WHERE clause cannot leak rows.

```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON invoices
    USING (tenant_id = current_setting('app.tenant_id')::bigint);
```

```php
// Set the session variable per request before any tenant query.
// SET takes no bind parameters; set_config() does.
DB::select("SELECT set_config('app.tenant_id', ?, false)", [(string) $tenantId]);
```

- Wrap the auth check in a subquery / `SELECT` of `current_setting(...)` so the planner caches it once per query rather than re-evaluating per row.
- RLS is enforcement-in-depth, not a substitute for application authorization — keep both. The connecting DB role must not have `BYPASSRLS`.
- Application-level scoping (global Eloquent scopes) is simpler for most apps; reach for RLS when defense-in-depth against a buggy query is required.

## Connection & Timeout Config

```php
// config/database.php — 'pgsql' connection
'options' => [
    PDO::ATTR_TIMEOUT => 3,
],
// Per-connection statement guards (also settable via 'options' / a session SET):
// statement_timeout, idle_in_transaction_session_timeout
```

- Set `statement_timeout` and `idle_in_transaction_session_timeout` so a runaway query or stuck transaction cannot hold locks indefinitely.
- Behind PgBouncer in transaction-pooling mode, disable persistent connections and avoid session-level state (prepared statements, `SET`) that outlives a transaction.
- Size `max_connections` to `(web workers + queue workers + scheduler) × pool`; front it with PgBouncer rather than raising `max_connections` unbounded.

## Diagnostics Cheatsheet

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;        -- real plan + actual rows + I/O
-- Top time-consuming queries (extension must be enabled):
SELECT query, calls, total_exec_time, mean_exec_time
  FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;
-- Dead-tuple bloat / vacuum health:
SELECT relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC;
-- Unindexed foreign keys and blocking locks:
SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';
```

- Enable `pg_stat_statements` (`shared_preload_libraries`) to find the queries worth tuning.
- Watch `n_dead_tup` — high dead-tuple counts mean autovacuum is falling behind, which degrades plans and inflates table size.

## Done when
- Columns use `timestamptz`, `numeric`, and `jsonb` correctly; money is never a float.
- Each specialized index (GIN/BRIN/partial/covering) matches a real access pattern and is verified with `EXPLAIN (ANALYZE)`.
- Upserts run as single `ON CONFLICT` statements backed by a unique index; queue claims use `SKIP LOCKED` in a short transaction.
- Large-set reads use cursor pagination over an indexed key; RLS (if used) sets the tenant variable per request and the role lacks `BYPASSRLS`.
- `statement_timeout` is set; Pest tests cover the new data-access paths; no secrets are hardcoded.

## Related skills
- `@skills/mysql-patterns/SKILL.md` — the MySQL counterpart to this skill.
- `@skills/mysql-problem-solver/SKILL.md` — method for diagnosing an existing slow query (adapt EXPLAIN/`pg_stat_statements` for Postgres).
- `@skills/redis-patterns/SKILL.md` — caching/locking in front of the database.
- `@skills/latency-critical-systems/SKILL.md` — when p95 latency on these query paths matters.

## References
- PostgreSQL index types: https://www.postgresql.org/docs/current/indexes-types.html
- `INSERT ... ON CONFLICT`: https://www.postgresql.org/docs/current/sql-insert.html

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
