---
name: mysql-patterns
description: "Use when designing MySQL schema features or applying advanced MySQL patterns in Laravel — upserts, JSON columns, full-text search, partitioning, replication/read-write splitting, and deadlock handling — beyond the query tuning already in the SQL rules."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/sql/optimalize.md` — it already owns indexing, SARGable WHERE, seek/keyset pagination, EXPLAIN, transactions/locking basics, batch-over-per-row, CTE/window/recursive queries, schema basics, DB-level caching, and the **Performance Non-Regression on Query Changes** gate. Do not re-explain those here; defer to it. When a pattern in this skill *changes an existing query* (e.g. swapping `LIKE` for a FULLTEXT match, moving a filter onto a generated column, introducing partition pruning), capture the original query's baseline and confirm the new shape is equal or faster — if it is slower, document the reason and the remaining optimization options per that gate.
- For diagnosing an existing slow query, use `@skills/mysql-problem-solver/SKILL.md`. In `MODE=design` this skill designs features rather than investigating regressions; in `MODE=cr` it reviews the shape of those same features on a diff (see *Modes*). Query diagnosis stays with that skill in both modes.
- If the project uses Laravel, also apply `@rules/laravel/laravel.md` and `@rules/laravel/architecture.md`.
- Apply `@rules/security/backend.md` — parameterized queries / ORM only, least-privilege DB users, never hardcode credentials.
- `final` classes, `declare(strict_types=1)`, Pest tests for any data-access code added.
- Verify the engine/version before using a version-specific feature (`SELECT VERSION();`). MySQL 8 and MariaDB diverge on JSON, `ON DUPLICATE KEY` aliases, and `SKIP LOCKED`.

## Modes

This skill runs in one of two modes, selected by the caller via `MODE` (default `design`):

- **`design` (default)** — full design work: write migrations, add generated columns and indexes, change connection configuration, and apply the patterns below to the project. Every section below behaves as written unless it is explicitly flagged for `MODE=cr`.
- **`cr` (read-only lens — invoked by `@skills/code-review/SKILL.md`, `code-review-github`, `code-review-jira`, and `code-review-bugsnag` when the diff touches a MySQL schema-feature surface)** — **never modify code, never author a migration or a test, never stage / commit / push, never run fixers or checkers, and never chain a follow-up review.** Scope the analysis to the lines added or modified by the PR diff and return the findings as markdown only, for the CR to fold into its single `## Database Analysis` section.
Every instruction below that would touch the database, a migration, or configuration — create, add, alter, index, enable, set, or any other such verb — is emitted as a written proposal carrying a concrete SQL / query-builder snippet, never applied to the project.

> **What this lens owns in a CR:** the shape of the schema feature and of the data-access pattern built on it — whether an upsert runs as one statement over a backing unique index, whether a JSON path is indexed through a generated column, whether full-text search replaces a leading-wildcard `LIKE`, whether the partition key matches the predicate the queries filter on, whether read/write splitting keeps `sticky` on a read-after-write path, and whether a concurrent transaction carries a deadlock retry.
> It **defers the performance of a query and its plan** — index usage, rows examined, `EXPLAIN` shape, `filesort` / `temporary`, and the non-regression gate on a rewritten query — to `@skills/mysql-problem-solver/SKILL.md`, and never raises a finding that skill owns. On a MySQL diff that skill runs in the advisory `casey` report, beside this lens in the review; the two divide the *dimensions* of a DB change, never its lines: a slow query over a new partition carries one performance item in the `casey` report and one partition-shape finding from this lens.

## Use when
- Adding upserts, JSON columns, full-text search, generated columns, or partitioning to a Laravel app.
- Setting up read/write splitting against replicas, or hardening against deadlocks and connection exhaustion.
- Reviewing a migration that introduces any of the above on a large table.

These topics complement the query-tuning rules; they are not covered there.

## Upserts

Pick the narrowest tool. All run as single statements — never loop per row.

```php
// Insert-or-update many rows in ONE statement.
// 2nd arg = unique-by columns; 3rd = columns to overwrite on conflict.
Product::upsert(
    [['sku' => 'A1', 'price' => 10], ['sku' => 'B2', 'price' => 20]],
    uniqueBy: ['sku'],
    update: ['price'],
);

// Insert, silently skip rows that violate a unique key. No update.
DB::table('tags')->insertOrIgnore([['name' => 'php'], ['name' => 'sql']]);

// Single row: fetch-or-create-then-update. Fires model events; runs SELECT + INSERT/UPDATE.
Product::updateOrCreate(['sku' => 'A1'], ['price' => 10]);
```

- `upsert()` / `insertOrIgnore()` are bulk and do **not** fire model events or touch timestamps automatically (set them yourself). Prefer them for large batches.
- `updateOrCreate()` is per-row, fires events, and is race-prone under concurrency unless a unique index backs the match columns. Wrap in a deadlock retry (below) when concurrent.
- Raw form: `INSERT ... ON DUPLICATE KEY UPDATE price = VALUES(price)` (MariaDB) / `... AS new ON DUPLICATE KEY UPDATE price = new.price` (MySQL 8, `VALUES()` deprecated).
- A unique index on the conflict columns is mandatory or the upsert degrades to plain inserts.

## JSON Columns + Indexes

JSON columns cannot be indexed directly. Index a **generated column** extracted from the JSON, or a multi-valued index for arrays.

```php
Schema::table('products', function (Blueprint $table): void {
    $table->json('attributes');
    // Stored generated column promotes attributes->'$.color' to an indexable scalar.
    $table->string('color')->storedAs("attributes->>'$.color'");
    $table->index('color');
});
```

```php
// Querying JSON paths in Eloquent:
Product::where('attributes->color', 'red')->get();
Product::whereJsonContains('attributes->tags', 'sale')->get();
```

- `->>` (or `JSON_UNQUOTE(JSON_EXTRACT(...))`) returns the unquoted scalar; index that, not the raw `->`.
- `VIRTUAL` columns compute on read (no storage, index still allowed); `STORED` persists (faster read, costs disk + write). Default to `VIRTUAL` unless the column is read-heavy.
- Validate JSON shape in the application; MySQL only enforces well-formedness, not structure.

## Full-Text Search

For natural-language search on TEXT columns, a `FULLTEXT` index beats `LIKE '%term%'` (which is non-SARGable, see `@rules/sql/optimalize.md`).

```php
Schema::table('articles', function (Blueprint $table): void {
    $table->fullText(['title', 'body']);
});
```

```php
// Boolean mode supports +required -excluded "phrase" operators.
Article::whereFullText(['title', 'body'], 'laravel +redis', ['mode' => 'boolean'])->get();
// Or raw:
Article::whereRaw(
    'MATCH(title, body) AGAINST(? IN NATURAL LANGUAGE MODE)',
    ['laravel redis'],
)->get();
```

- Default `innodb_ft_min_token_size` is 3 — shorter terms are ignored unless you lower it and rebuild the index.
- FULLTEXT covers basic relevance ranking only. For typo tolerance, facets, or large corpora, reach for a dedicated engine (Meilisearch/Elasticsearch via Laravel Scout). Note the tradeoff; do not over-engineer for small tables.

## Generated / Virtual Columns

Beyond JSON, generated columns normalize derived values so they stay consistent and become indexable.

```php
$table->decimal('net', 15, 2);
$table->decimal('vat_rate', 5, 4);
$table->decimal('gross', 15, 2)->virtualAs('net * (1 + vat_rate)');
```

- A generated column cannot reference another generated column defined after it, nor non-deterministic functions (`NOW()`, `RAND()`).
- Use them to enforce an invariant in one place instead of recomputing it in every query.

## Partitioning

Partitioning splits one logical table across physical segments to prune scans and cheapen bulk drops. Use it for genuinely large, time- or range-sliced tables — not by default.

```sql
-- RANGE: time-series; drop old data instantly with ALTER TABLE ... DROP PARTITION.
CREATE TABLE events (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id, created_at)         -- partition key MUST be in every unique key
) PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);

-- LIST: discrete buckets (e.g. region/tenant).
PARTITION BY LIST (region_id) (
    PARTITION eu VALUES IN (1, 2, 3),
    PARTITION us VALUES IN (4, 5)
);
```

- Every UNIQUE / PRIMARY key must include the partition column — this often forces a composite PK and reshapes the schema. Decide early.
- Partition pruning only triggers when the partition key appears in the `WHERE`; a query without it scans every partition.
- Laravel migrations have no partition DSL — use `DB::statement(...)` with raw SQL.

## Replication & Read/Write Splitting

Route reads to replicas, writes to the primary, with a single connection config.

```php
// config/database.php — 'mysql' connection
'read'  => ['host' => ['10.0.0.2', '10.0.0.3']],
'write' => ['host' => ['10.0.0.1']],
'sticky' => true,
```

- `sticky => true` routes reads back to the **write** host for the rest of the request after any write, so a just-written row is read back consistently despite replication lag. Keep it on for typical web flows.
- Force a specific connection when needed: `Model::on('mysql::read')` or `DB::connection('mysql')->select(...)`.
- Replicas are eventually consistent. Never read a balance/counter you just wrote from a replica without `sticky` or an explicit write-connection read.

## Deadlock Retry

InnoDB aborts one transaction in a deadlock (SQLSTATE `40001`, error `1213`). The correct response is to **retry the whole transaction**, not to catch-and-continue.

```php
DB::transaction(function (): void {
    // ... ordered, consistent locking; lock rows in a stable order to reduce deadlocks
}, attempts: 3); // Laravel retries the closure on deadlock up to `attempts` times.
```

- Keep transactions short, lock rows in a consistent order across code paths, and touch the fewest rows possible.
- Idempotency matters: the closure runs up to N times, so it must be safe to re-run.
- See `@rules/sql/optimalize.md` for the transaction/locking fundamentals this builds on.

## Connection Config & Timeouts

```php
// config/database.php 'mysql' → 'options'
PDO::ATTR_TIMEOUT => 3,              // connect timeout (seconds)
PDO::ATTR_PERSISTENT => false,       // avoid stale persistent conns behind PgBouncer-style poolers
```

- Set `wait_timeout` / `interactive_timeout` server-side to reclaim idle connections; size `max_connections` to `(workers + queue workers + scheduler) × pool`.
- Enable the slow query log (`slow_query_log = 1`, `long_query_time = 1`) to surface candidates for `@skills/mysql-problem-solver/SKILL.md`.

## Diagnostics Cheatsheet

```sql
SHOW ENGINE INNODB STATUS\G          -- LATEST DETECTED DEADLOCK + lock waits
SHOW FULL PROCESSLIST;               -- live queries, state, time, lock waits
SHOW INDEX FROM orders;              -- existing indexes (verify before adding one)
SELECT * FROM information_schema.innodb_trx;          -- open transactions
SELECT * FROM performance_schema.data_lock_waits;     -- who blocks whom (MySQL 8)
SELECT table_name, data_length, index_length
  FROM information_schema.tables WHERE table_schema = DATABASE();  -- sizes
```

## Done when
- The chosen feature is verified against the actual engine/version.
- Any pattern that changed an existing query was benchmarked against its baseline and is equal or faster; a slower result carries the documented reason and remaining optimization options (`@rules/sql/optimalize.md` "Performance Non-Regression on Query Changes").
- Upserts run as single statements with a backing unique index; concurrent ones are deadlock-retried.
- JSON / FULLTEXT / partition queries are confirmed to hit the intended index (EXPLAIN — see `@rules/sql/optimalize.md`).
- Read/write splitting keeps `sticky` on for read-after-write paths.
- Pest tests cover the new data-access paths; no secrets are hardcoded.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
