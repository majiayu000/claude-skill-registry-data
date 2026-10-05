---
name: sql-index-tuning
description: Diagnose slow SQL queries and add the right indexes without over-indexing — B-tree mechanics, composite ordering (equality-before-range), the leftmost-prefix rule, covering/index-only scans, reading EXPLAIN ANALYZE, selectivity, and write-amplification costs. Worked SQL examples and a runnable index-suggester.
type: skill
version: 2.0.0
updated: 2026-06-29
---
# SQL Index Tuning

Indexing is the highest-leverage performance work in most data-backed systems: the right index turns a
multi-second sequential scan into a sub-millisecond lookup, and the wrong one quietly taxes every write
forever. This skill is the deep reference for doing it deliberately — how B-tree indexes actually work,
how to order composite columns, how to read a query plan, and when an index is the wrong answer. Heavy
detail lives in `references/`; copy-paste DDL and plans in `examples/`; a runnable index-suggester in
`scripts/`.

## Mental model

An index is a **sorted, redundant copy** of one or more columns plus a pointer back to the row. The
database maintains that sort order on every write so reads can binary-search instead of scanning. Two
consequences follow directly and explain almost every tuning decision:

| Property | Why it matters |
|---|---|
| Indexes are **sorted** | They serve equality, range, prefix, `ORDER BY`, and `MIN/MAX` from order alone |
| Indexes are **redundant** | Every `INSERT`/`UPDATE`/`DELETE` must also update them — pure write cost |
| Indexes are **left-anchored** | A composite `(a, b, c)` can seek on `a`, `a,b`, `a,b,c` — never `b` or `c` alone |

Keep both halves in mind at once: you are buying read speed with write speed and storage. The job is to
buy only the indexes that pay for themselves.

## 1. B-tree basics

The default index type everywhere (`CREATE INDEX` builds a B-tree unless you ask otherwise) is a
balanced tree whose leaf nodes hold sorted key values. Lookups are `O(log n)` — a few page reads even
for billions of rows. Because the leaves are sorted and linked, a B-tree efficiently serves:

- **Equality**: `WHERE status = 'open'`
- **Range**: `WHERE created_at > '2026-01-01'`, `BETWEEN`, `<`, `>`
- **Sorted output**: `ORDER BY created_at` with no separate sort step
- **Prefix matches**: `WHERE email LIKE 'jay%'` (but not `'%jay'` — a leading wildcard cannot seek)

It cannot help with operations that don't respect that ordering: `WHERE lower(email) = ...` (unless you
index the expression), `!=`, or `%suffix` searches. Full mechanics, page splits, and why a low-cardinality
boolean is a poor leading column are in [`references/btree-internals.md`](references/btree-internals.md).

## 2. Composite indexes & the leftmost-prefix rule

A composite index `(a, b, c)` is sorted by `a`, then `b` within equal `a`, then `c`. This is the single
most misunderstood part of indexing. The index can satisfy a predicate only as a **left-anchored prefix**:

```sql
-- Index: (tenant_id, status, created_at)
WHERE tenant_id = 9 AND status = 'open'                  -- uses (tenant_id, status)      ✓
WHERE tenant_id = 9 AND status = 'open' AND created_at>… -- uses all three                ✓
WHERE tenant_id = 9                                      -- uses (tenant_id)              ✓
WHERE status = 'open'                                    -- CANNOT seek (skips tenant_id) ✗
WHERE tenant_id = 9 AND created_at > …                   -- seeks tenant_id, filters rest ◑
```

**Column ordering rule: equality columns first, then one range column, then columns needed only for
sort.** A range predicate (`>`, `<`, `BETWEEN`) "uses up" the index — columns after the range column
can no longer be used for seeking, only as a filter. So `(tenant_id, status, created_at)` is right for
`tenant_id = ? AND status = ? AND created_at > ?`, but putting `created_at` before `status` would waste
the `status` equality. Full reasoning, plus covering indexes and index-only scans, in
[`references/composite-and-covering.md`](references/composite-and-covering.md).

## 3. Covering indexes & index-only scans

If an index contains **every column a query touches** (in `SELECT`, `WHERE`, and `ORDER BY`), the engine
answers from the index alone and never visits the table heap — an **index-only scan**. This eliminates the
random I/O of fetching rows and is often a 5–50x win on hot read paths.

```sql
-- Query reads only id, tenant_id, status:
SELECT id, status FROM orders WHERE tenant_id = 9 AND status = 'open';

-- Covering index (Postgres INCLUDE keeps non-key columns in the leaf):
CREATE INDEX ix_orders_cover ON orders (tenant_id, status) INCLUDE (id);
```

The trade-off: covering indexes are wider, so they cost more to write and store. Add them only for
high-frequency queries you have measured. See `examples/index-ddl.sql` for `INCLUDE` vs composite forms.

## 4. Reading EXPLAIN / EXPLAIN ANALYZE

`EXPLAIN` shows the planner's chosen plan and **estimated** cost; `EXPLAIN ANALYZE` actually runs the
query and reports **real** timings and row counts. Always tune against `ANALYZE` output. What to look for:

- **`Seq Scan` on a large table** under a selective `WHERE` — the prime candidate for an index.
- **`rows` estimate vs `actual`** wildly diverging — stale statistics; run `ANALYZE <table>`.
- **`Sort` / `Hash` nodes with high cost** — an ordered index may remove the sort.
- **`Index Scan` vs `Index Only Scan`** — the latter means your index is covering.
- **`Rows Removed by Filter`** — rows read then thrown away; a better index seeks past them.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id FROM orders WHERE tenant_id = 9 AND created_at > now() - interval '7 days';
```

A full annotated walkthrough — before/after plans for the same query — is in `examples/explain-walkthrough.sql`
and the node-by-node guide in [`references/reading-explain.md`](references/reading-explain.md).

## 5. Selectivity & cardinality

**Selectivity** is the fraction of rows a predicate keeps; **cardinality** is the number of distinct
values in a column. An index helps in proportion to its selectivity — seeking to 50 rows out of 10M is a
huge win; seeking to 4M out of 10M is slower than a sequential scan, and the planner will (correctly)
ignore the index. Rules of thumb:

- Lead a composite index with the **most selective equality column** the query actually filters on.
- A boolean or low-cardinality status column is a poor standalone index but fine deeper in a composite.
- Watch for **skew**: `status = 'archived'` (95% of rows) is unselective; `status = 'pending'` (0.1%) is
  highly selective. Partial indexes (`WHERE status = 'pending'`) target exactly the selective slice.

Details and how the planner uses histograms: [`references/selectivity-and-cardinality.md`](references/selectivity-and-cardinality.md).

## 6. The write-amplification cost — when NOT to add an index

Every index is extra work on every write to the table. Five indexes mean an `INSERT` does roughly six
B-tree maintenance operations. This is **write amplification**, and it's the reason "just add an index"
is not free advice.

**Do NOT add an index when:**

- The table is **write-heavy and rarely read** on that column (a log/append table).
- The column has **very low cardinality** and the query isn't selective (a 2-value flag on its own).
- A **redundant** index already covers the need — `(a, b)` makes a separate `(a)` index unnecessary,
  since the composite serves `a`-only seeks via the leftmost prefix. Drop the narrower one.
- The table is **small** (a few thousand rows); a sequential scan is already fast and the planner skips
  the index anyway.
- You haven't measured. Speculative indexes accumulate into pure write tax and bloat.

## Common pitfalls (failure modes)

- **Wrapping the indexed column in a function**: `WHERE date(created_at) = '2026-06-29'` cannot use an
  index on `created_at`. Rewrite as a range, or build an expression index.
- **Leading wildcard `LIKE '%foo'`** — no prefix to seek; needs a trigram or full-text index instead.
- **Wrong composite order** — `(created_at, tenant_id)` for `tenant_id = ? AND created_at > ?` forces a
  scan; the equality column must lead. (See the leftmost-prefix rule above.)
- **Type/collation mismatch** — comparing a `bigint` column to a string literal, or a join across
  mismatched collations, silently disables the index.
- **Redundant overlapping indexes** — `(a)`, `(a, b)`, `(a, b, c)` where the widest alone suffices: pure
  write cost, no read benefit.
- **Trusting `EXPLAIN` over `EXPLAIN ANALYZE`** — estimates lie when statistics are stale; always verify
  with real timings, and `ANALYZE` the table after big data changes.
- **OR across columns** — `WHERE a = 1 OR b = 2` often can't use a single composite; consider a `UNION`
  of two indexed seeks or separate indexes.

## When NOT to use / trade-offs

Indexing is the wrong lever when the bottleneck is elsewhere: an `N+1` query pattern needs batching, not
an index; a query returning most of a table should be paginated and is already best served by a scan; and
analytical scans over whole tables belong in a column store, not a B-tree. Reach for a different index
type when B-tree can't help — GIN/trigram for substring and full-text search, GiST for geospatial,
BRIN for naturally-ordered append-only data (huge time-series tables) where a tiny block-range index
beats a full B-tree. And remember the meta-cost: every index slows writes and consumes storage and cache.
On a write-dominated workload, fewer, well-chosen indexes beat many.

Pairs with `database-scaling`, `data-modeling`, and `database-migrations` (add indexes concurrently /
online to avoid locking production tables during deploys).

## Files in this package

- `references/btree-internals.md` — how B-trees store keys, page splits, what they can and can't serve
- `references/composite-and-covering.md` — leftmost-prefix rule, equality-before-range, covering/index-only scans
- `references/reading-explain.md` — node-by-node guide to EXPLAIN / EXPLAIN ANALYZE output
- `references/selectivity-and-cardinality.md` — selectivity math, histograms, partial indexes, skew
- `examples/explain-walkthrough.sql` — before/after query plans for the same query, annotated
- `examples/index-ddl.sql` — composite, covering (`INCLUDE`), partial, and expression index DDL
- `scripts/suggest-index.mjs` — proposes a composite index from a query's columns (equality-before-range + leftmost-prefix); run `--selftest` to verify
