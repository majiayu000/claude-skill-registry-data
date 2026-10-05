---
name: padosoft-database-design
description: >-
  Use this skill when writing or reviewing a migration or a table design — adding a table or a column,
  choosing indexes, deciding a primary key, partitioning a large table, adding a JSON column, planning for
  growth. Also when the user reports a slow query blamed on a missing index, a migration that fails because
  a table or column already exists (or does not), an index that is never used, a table too big to purge, or
  asks how to index a query they are about to write. It covers index selection and redundancy, the
  composite-prefix rule, covered indexes, partitioning constraints, JSON columns, and the guard clauses a
  migration needs to be re-runnable. Do not use it for writing the queries themselves
  (padosoft-query-performance), for ORM conventions, or for choosing a database engine.
license: MIT
compatibility: >-
  MySQL and MariaDB with InnoDB; the index reasoning transfers to other engines, the partitioning and
  generated-column constraints do not. Migration examples use Laravel's schema builder.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The index, the key and the partition are part of the table's design, not a later fix.
  profiles: data, laravel
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: mysql, innodb, index, composite index, partition, migration, schema, json column, primary key
---

# Database design

An index is not a performance tweak added later — it is part of the table's design, and so is the primary
key, the partition and the decision to put something in a JSON column. Getting them wrong is cheap to fix on
day one and expensive on day four hundred.

---

## 1. Which columns get an index by default

Always, unless there is a reason not to: **boolean and flag columns, dates and datetimes, and descriptive
text columns** (name, title, description) — because those are what the admin side filters, sorts and
searches on, systematically.

Then, without exception: **every column involved in a `JOIN`, `WHERE`, `ORDER BY`, `GROUP BY` or `HAVING`**.

Two exemptions: the column is already the **leftmost prefix** of an existing composite index, or the table
will never hold more than a few thousand rows.

```php
$table->index('active');
$table->index('starts_at');
$table->index(['brand_id', 'active'], 'idx_art_brand_active');   // idx_<table>_<col>_<col>
```

## 2. Designing the index for a query: three stars

| Star | Columns | Not available when |
|---|---|---|
| ★ | the equality predicates of the `WHERE`, joined by `AND` | the `WHERE` uses `OR` or complex expressions |
| ★★ | the `ORDER BY` / `GROUP BY` columns, **in their direction** | grouping and ordering differ |
| ★★★ | the remaining selected columns — a covered index | optional, but it removes the row lookup entirely |

```sql
-- SELECT name, price FROM articles WHERE brand_id = ? AND active = 1 ORDER BY name
-- INDEX(brand_id, active, name, price)
--        ★ equality        ★★ order  ★★★ covered
```

## 3. Composite indexes, and the redundancy they create

An index on `(a, b, c)` serves `(a)`, `(a, b)` and `(a, b, c)`. It does **not** serve `(b, c)` — the leftmost
prefix is not optional. Put the most selective equality columns first.

Which means: **if `(a, b)` exists, a separate index on `(a)` is redundant and should be removed.** A
redundant index costs write throughput and buffer pool for nothing.

Two engine facts that change the arithmetic:

- **A secondary index already contains the primary key.** `INDEX(email)` is effectively `INDEX(email, id)` —
  do not add the id yourself, and count it when judging whether an index is covered.
- **`COUNT(*)` usually picks the smallest index**, so the index you think it uses may not be the one.

## 4. The things that silently disable an index

```sql
-- ❌ a function on the column: the index on created_at is not used
WHERE YEAR(created_at) = 2026
-- ✅ a range on the raw column
WHERE created_at BETWEEN ? AND ?
```

Any wrapping of the indexed column — a cast, a concatenation, a date function, a case change — turns the
lookup into a scan. Rewrite the predicate, or index the expression if the engine supports it.

For a frequent `ORDER BY column DESC`, declare the direction in the index rather than hoping: it matters
when grouping and ordering disagree.

## 5. Two patterns for big tables

**Late row lookup.** For `ORDER BY ... LIMIT` over a large table, fetch the ids from the index first, then
join back for the row data. Without it the engine reads thousands of complete rows only to discard them.

```sql
SELECT id FROM articles WHERE brand_id = ? ORDER BY created_at DESC LIMIT 20;   -- index only
SELECT * FROM articles WHERE id IN (...);                                        -- 20 rows
```

**The clustered index is the physical order.** In InnoDB the primary key decides how rows are laid out on
disk, so range queries on it read only the pages they need. When the dominant query filters by date, that is
an argument for a composite primary key or a partition — decided at design time, not after.

## 6. Partitioning

**Consider it when** the table is in the millions and growing, the queries *always* filter on one dimension
(date, tenant, state), you need fast purging of history (`DROP PARTITION` is instant where `DELETE` is
row-by-row), or write locks are hurting reads on unrelated slices.

**Do not** when the table is under a few hundred thousand rows, when the queries do not filter on the
partition key, or when the table has many unique indexes — because of the constraint below.

| Type | For |
|---|---|
| `RANGE` | time and numeric ranges |
| `LIST` | a known discrete set (state, country) |
| `HASH` / `KEY` | even distribution with no logical dimension |

The constraints that catch people out:

- **Every unique index — the primary key included — must contain the partition key.** Put the id *first* in
  the composite primary key so `WHERE id = ?` stays fast and ids stay practically unique.
- If the key is not an existing column, add a **generated column**, and it must be `STORED`, not `VIRTUAL`,
  for the auto-increment and the primary key to work.
- Declare it in the ORM's guarded/fillable configuration, or a mass assignment will fight it.
- **Always keep a catch-all final partition** with the maximum bound, or an insert with an unanticipated
  value fails.
- Name the partition explicitly in queries where it matters, so the engine prunes instead of scanning all of
  them; combining partition selection with a covered index is what makes the difference.
- Maintenance is a scheduled job: split the catch-all forward, drop the oldest, and check the row
  distribution per partition periodically.

## 7. JSON columns

Use one when the data is **always read and written with the parent row** and never joined on. Do not, when
the inner fields are needed for joins or aggregates, or when the document grows past roughly a kilobyte —
at that point it is pushing everything else out of the buffer pool.

To filter on a field inside the document, add a **virtual** generated column and index that. Virtual is
enough here, and lighter than stored, because it is not part of the primary key.

## 8. A migration must survive a schema that does not match the ledger

In any environment with manual imports, partial rollbacks or a restored database, the schema and the
migration table disagree. Every statement therefore checks the current state first.

| Operation | Guard |
|---|---|
| Create a table | if it exists → return |
| Drop a table | use the *if exists* form, never the bare drop |
| Alter a table | if it does **not** exist → return |
| Add a column | if the column exists → skip |
| Drop or change a column | if the column does **not** exist → skip |

Early return at the top of the migration, not a conditional wrapped around the whole body — see
**`padosoft-laravel-conventions`** on guard clauses.

---

## Gotchas

- **An index nobody uses still costs every write**, and it is invisible in a read benchmark. Check actual
  usage before adding one "just in case", and again before keeping one.
- **The redundant single-column index is almost always there.** It was added first, and the composite came
  later.
- **Partitioning is not an index.** A query that does not filter on the partition key now touches every
  partition — it got slower, not faster.
- **A unique constraint is an index**, so it collides with the partition-key rule. This is the most common
  reason a table cannot be partitioned without redesigning it.
- **Adding a column to a huge table is a locking operation** on older engine versions. Check what your
  version does before running it on the live table.
- **A generated column marked virtual where stored was required** fails only when the partition or the
  auto-increment is exercised — not when the migration runs.

## Checklist

- [ ] Index on every flag, date and descriptive text column, unless exempt
- [ ] Index for every column in `JOIN` / `WHERE` / `ORDER BY` / `GROUP BY` / `HAVING`
- [ ] Three-star index designed for the main expected queries
- [ ] No redundant single-column index shadowed by a composite prefix
- [ ] Primary key not duplicated inside secondary indexes
- [ ] No function applied to an indexed column in a predicate
- [ ] Descending index where the frequent order is descending
- [ ] Naming convention followed
- [ ] Growth past a million rows considered: partition decided for or against, and why
- [ ] If partitioned: key stored, present in the primary key and every unique index, guarded in the model, catch-all partition present, maintenance scheduled
- [ ] JSON columns: justified, with a virtual column and index for any filtered field
- [ ] Every DDL statement guarded against the state actually on disk

## Final report

```
Table: <name>  ·  expected rows: <order of magnitude>
Indexes added: <list>   removed as redundant: <list>
Main queries covered: <query> → <index> (stars: ★/★★/★★★)
Primary key: <columns> — reason: <clustering / partition>
Partition: none | <type, key, maintenance plan>
JSON columns: none | <column, indexed fields>
Migration guards: create/drop/alter/add/drop-column all guarded: yes | no
```
