---
name: zero-downtime-migrations
description: Writes and reviews PostgreSQL schema migrations that run against large, busy production tables without blocking reads or writes. Covers CREATE INDEX CONCURRENTLY outside transactions, foreign keys and CHECKs added NOT VALID then validated in a later transaction, NOT NULL the PostgreSQL 18 way (NOT VALID) and the PG 12-17 way, unique constraints USING INDEX, which ADD COLUMN and ALTER TYPE forms rewrite the table, batched backfills that COMMIT, lock_timeout and the lock queue, and expand/contract for renames and type changes. Use when adding or changing an index, constraint, column, default or type on an existing Postgres table, when a migration must be online, zero-downtime or non-blocking, when backfilling data, or when reviewing migration SQL from Rails, Django, Drizzle, node-pg-migrate, dbmate, graphile-migrate or plain .sql files.
license: MIT
---

# Zero-downtime Postgres migrations

A migration causes an outage in one of two ways. Either a statement takes a lock that conflicts with
the application's queries and holds it while it does work proportional to the table size (a scan, a
rewrite, an index build), or a statement waits for a lock and every query behind it in the queue
waits too. Everything below is about avoiding those two things. Facts are for PostgreSQL 18
(18.6 is current as of November 2026), with notes where 12-17 differ.

## Ask two questions of every statement

1. **Which lock does it take, on which tables, and until when?** Table locks are held until the
   transaction ends, not until the statement ends. The transaction is the unit you reason about.
2. **Does it do O(rows) work while that lock is held?** Scanning to validate, rewriting the heap, or
   building an index.

The app's writes take `ROW EXCLUSIVE`. Reads take `ACCESS SHARE`. What conflicts:

| Lock | Typical sources | Blocks reads | Blocks writes |
| --- | --- | --- | --- |
| `SHARE UPDATE EXCLUSIVE` | `CREATE INDEX CONCURRENTLY`, `VALIDATE CONSTRAINT`, `VACUUM`, `ANALYZE` | no | no |
| `SHARE` | `CREATE INDEX` (not concurrent) | no | **yes** |
| `SHARE ROW EXCLUSIVE` | `ADD FOREIGN KEY` (both tables), `CREATE TRIGGER` | no | **yes** |
| `ACCESS EXCLUSIVE` | most `ALTER TABLE`, `DROP`, `TRUNCATE`, `REINDEX` (on the index), `VACUUM FULL` | **yes** | **yes** |

**Rule:** a statement on a live table is safe when it either takes `SHARE UPDATE EXCLUSIVE` or weaker
(long work is fine), or takes something stronger only for a catalog-only change (milliseconds), with
`lock_timeout` set. Anything that scans, rewrites or builds under `SHARE` or stronger blocks writes
for the whole duration. [references/lock-matrix.md](references/lock-matrix.md) has the per-statement
table, measured on 18.6.

## The lock queue: why "instant" DDL still takes production down

`ALTER TABLE shipments ADD COLUMN signed_by text` is a catalog change, but it needs `ACCESS EXCLUSIVE`. If a
long query or an idle-in-transaction session holds any lock on `shipments`, the ALTER waits. While it
waits, every new query on `shipments`, plain SELECTs included, queues behind it. Reproduced on 18.6: a
reader holding a 6-second transaction plus a waiting ALTER made an unrelated `SELECT count(*)` wait
the full 6 seconds.

Fix: cap the wait and retry.

```sql
-- Inside a transactional migration: SET LOCAL ends with the transaction.
SET LOCAL lock_timeout = '5s';
ALTER TABLE shipments ADD COLUMN signed_by text;
```

- With `lock_timeout` the ALTER fails with `canceling statement due to lock timeout` and the queue
  drains. Retry the migration (with backoff) from the deploy tool, or let it fail loudly.
- In a file that runs outside a transaction, `SET LOCAL` does nothing (Postgres only warns), and
  plain `SET` is session-wide, so it leaks into the next files. Use `SET`, then
  `RESET lock_timeout` afterwards.
- Set timeouts per migration session, not in `postgresql.conf`; the docs advise against that because
  it affects every session.
- **Do not give `CREATE INDEX CONCURRENTLY` a short `lock_timeout`.** It waits for older transactions
  that touched the table, and that wait counts. On timeout it leaves an `INVALID` index behind
  (reproduced on 18.6). Let it wait, and watch for long transactions instead.
- `statement_timeout` caps the whole statement, lock wait included; `transaction_timeout` (PG 17+)
  caps a whole transaction. Neither replaces `lock_timeout`.

## Change → safe recipe

| You want to | Unsafe form (why) | Safe form |
| --- | --- | --- |
| Add an index | `CREATE INDEX` (`SHARE` for the whole build: no writes) | `CREATE INDEX CONCURRENTLY`, outside a transaction, one statement per call |
| Drop an index | `DROP INDEX` (`ACCESS EXCLUSIVE`) | `DROP INDEX CONCURRENTLY` (not for indexes backing a constraint) |
| Rebuild an index | `REINDEX INDEX` (blocks writes; `ACCESS EXCLUSIVE` on the index) | `REINDEX INDEX CONCURRENTLY` |
| Add a foreign key | `ADD FOREIGN KEY` (validates under `SHARE ROW EXCLUSIVE` on **both** tables) | `ADD ... NOT VALID`, then `VALIDATE CONSTRAINT` in a later transaction |
| Add a CHECK | `ADD CHECK` (scan under `ACCESS EXCLUSIVE`) | `ADD ... NOT VALID`, then `VALIDATE CONSTRAINT` later |
| Make a column NOT NULL | `SET NOT NULL` (scan under `ACCESS EXCLUSIVE`) | PG 18: `ADD CONSTRAINT x NOT NULL col NOT VALID`, then `VALIDATE`. PG 12-17: validated `CHECK (col IS NOT NULL)` first |
| Add UNIQUE or PRIMARY KEY | `ADD UNIQUE (col)` (builds the index under `ACCESS EXCLUSIVE`) | `CREATE UNIQUE INDEX CONCURRENTLY`, then `ADD CONSTRAINT ... UNIQUE USING INDEX` |
| Add a column with generated values | `ADD COLUMN tracking_code uuid DEFAULT gen_random_uuid()` (volatile default: full rewrite) | add with no default, `SET DEFAULT` separately, batched backfill |
| Add a column with a constant default | (nothing wrong) | `ADD COLUMN c text NOT NULL DEFAULT 'x'` is catalog-only since PG 11; `now()` counts as constant |
| Change a column type | `ALTER TYPE` that rewrites (`int`→`bigint`, numeric scale, shrinking varchar) | expand/contract: new column, dual write, backfill, swap |
| Rename a column or table | `RENAME` (instant, but running code breaks) | expand/contract, or a compatibility view |
| Backfill existing rows | one `UPDATE` over the table (row locks on every row until commit) | keyset batches, `COMMIT` after each |

Full SQL for each row is in [references/recipes.md](references/recipes.md).

## Transactions and the migration runner

Most bugs in "safe" migrations come from the runner, not the SQL.

- **NOT VALID and VALIDATE must be in different transactions.** In one transaction, the `ADD` keeps
  its strong lock while `VALIDATE` scans, which is exactly the validated `ADD` you were avoiding.
  Separate files are only separate transactions if the runner commits between files. drizzle-orm's
  migrator (0.45.x) runs every pending migration in one transaction. node-pg-migrate's CLI
  defaults to `--single-transaction`.
- **`CREATE INDEX CONCURRENTLY`, `DROP INDEX CONCURRENTLY`, `REINDEX CONCURRENTLY` and `VACUUM`
  cannot run in a transaction block.** That includes the implicit block of a multi-statement simple
  query. `SET ...; CREATE INDEX CONCURRENTLY ...` sent as one string fails, so send one statement per
  call. graphile-migrate's no-transaction files must contain exactly one statement for this reason.
- **Opting out of the transaction**, per tool:
  - node-pg-migrate: `pgm.noTransaction()`.
  - dbmate: `-- migrate:up transaction:false`.
  - graphile-migrate: `--! no-transaction` at the top, one statement.
  - Django: `atomic = False` with `AddIndexConcurrently`, and `AddConstraintNotValid` plus
    `ValidateConstraint` in two separate migrations.
  - Rails: `disable_ddl_transaction!` with `algorithm: :concurrently`, and `validate: false` on
    `add_foreign_key` or `add_check_constraint`.
  - A custom runner: read it. Look for a per-file directive, and check whether it wraps one file or
    the whole batch.
  See [references/runners.md](references/runners.md).
- **A no-transaction file is not atomic.** If statement 3 of 4 fails, statements 1-2 stay applied and
  the file is not recorded, so the rerun repeats them. Make every statement idempotent:
  `IF NOT EXISTS`, `IF EXISTS`, and `DROP INDEX CONCURRENTLY IF EXISTS` before a concurrent build.
- **A failed concurrent build leaves an `INVALID` index** that costs write overhead and is never used.
  `CREATE INDEX CONCURRENTLY IF NOT EXISTS` then *skips* it and leaves it invalid (reproduced on
  18.6). Drop and rebuild instead.
- **Never edit an applied migration.** Production will not rerun it. Add a new file.

## Core recipes

**Index on a hot table** (non-transactional step):

```sql
DROP INDEX CONCURRENTLY IF EXISTS shipments_carrier_dispatched_idx;
CREATE INDEX CONCURRENTLY shipments_carrier_dispatched_idx
  ON shipments (carrier_id, dispatched_at DESC);
-- afterwards: SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;  -- expect no rows
```

Column order matters: equality columns first, then the `ORDER BY` column, so
`WHERE carrier_id = $1 ORDER BY dispatched_at DESC LIMIT 50` reads 50 index entries and stops. With
`(dispatched_at, carrier_id)` there's no sort either, but the scan walks most of the index.

**Foreign key or CHECK on existing rows:**

```sql
-- transaction 1: catalog-only, brief strong locks
SET LOCAL lock_timeout = '5s';
ALTER TABLE shipments ADD CONSTRAINT shipments_carrier_fk
  FOREIGN KEY (carrier_id) REFERENCES carriers (carrier_id) NOT VALID;
ALTER TABLE shipments ADD CONSTRAINT shipments_fee_minor_check CHECK (fee_minor >= 0) NOT VALID;

-- transaction 2, if existing rows need fixing: plain DML, ROW EXCLUSIVE only
UPDATE shipments SET carrier_id = $unknown_carrier
WHERE NOT EXISTS (SELECT 1 FROM carriers k WHERE k.carrier_id = shipments.carrier_id);

-- transaction 3: scans under SHARE UPDATE EXCLUSIVE (plus ROW SHARE on carriers): no blocking
ALTER TABLE shipments VALIDATE CONSTRAINT shipments_carrier_fk;
ALTER TABLE shipments VALIDATE CONSTRAINT shipments_fee_minor_check;
```

A `NOT VALID` constraint is enforced for new and updated rows immediately. Only existing rows are
unchecked until `VALIDATE`. Don't stop at `NOT VALID`: until it is validated, Postgres "will not
assume that the constraint holds for all rows", and neither should you.

**NOT NULL on an existing column:**

```sql
-- PostgreSQL 18+
-- tx 1
ALTER TABLE shipments ADD CONSTRAINT shipments_tracking_code_nn NOT NULL tracking_code NOT VALID;
-- tx 2
ALTER TABLE shipments VALIDATE CONSTRAINT shipments_tracking_code_nn;
-- attnotnull and information_schema already say NOT NULL while the constraint is NOT VALID (18.6);
-- only pg_constraint.convalidated tells you old rows were checked. Finish with VALIDATE, not with
-- SET NOT NULL: on a column with an invalid not-null constraint, SET NOT NULL validates it by
-- scanning under ACCESS EXCLUSIVE.

-- PostgreSQL 12-17
-- tx 1
ALTER TABLE shipments ADD CONSTRAINT shipments_tracking_code_present
  CHECK (tracking_code IS NOT NULL) NOT VALID;
-- tx 2
ALTER TABLE shipments VALIDATE CONSTRAINT shipments_tracking_code_present;
-- tx 3: SET NOT NULL skips its scan because the validated CHECK proves there are no NULLs
ALTER TABLE shipments ALTER COLUMN tracking_code SET NOT NULL;
ALTER TABLE shipments DROP CONSTRAINT shipments_tracking_code_present;
```

**Unique constraint:**

```sql
-- non-transactional step
CREATE UNIQUE INDEX CONCURRENTLY shipments_tracking_code_uniq ON shipments (tracking_code);
-- new transaction
SET LOCAL lock_timeout = '5s';
ALTER TABLE shipments ADD CONSTRAINT shipments_tracking_code_uniq
  UNIQUE USING INDEX shipments_tracking_code_uniq;
```

`USING INDEX` needs a plain btree, non-partial, non-expression unique index. For a partial or
expression rule (`lower(username)`), the unique index itself is the enforcement; skip the constraint.
A concurrent unique build fails, and leaves an invalid index, if duplicates exist. Find them first.

**New column filled for every row** (for example an external tracking code):

```sql
-- tx 1: catalog-only
SET LOCAL lock_timeout = '5s';
ALTER TABLE shipments ADD COLUMN tracking_code uuid;  -- no default here
-- new rows only, no rewrite
ALTER TABLE shipments ALTER COLUMN tracking_code SET DEFAULT gen_random_uuid();
-- then: batched backfill (below), CREATE UNIQUE INDEX CONCURRENTLY, NOT NULL via NOT VALID + VALIDATE
```

`gen_random_uuid()`, `uuidv7()` (PG 18), `clock_timestamp()`, `random()`, `serial`/`bigserial`,
identity columns and `STORED` generated columns all rewrite the table when added with existing rows
(measured). `now()`, literals and virtual generated columns (the PG 18 default) do not.

**Batched backfill that runs from a migration** (outside a transaction block; `COMMIT` inside `DO`
or a procedure is allowed only there):

```sql
DO $$
DECLARE
  chunk constant bigint := 5000;
  lower_key bigint := 0;
  upper_bound bigint;
BEGIN
  SELECT coalesce(max(shipment_id), 0) INTO upper_bound FROM shipments;
  WHILE lower_key <= upper_bound LOOP
    UPDATE shipments SET tracking_code = gen_random_uuid()
    WHERE shipment_id >= lower_key AND shipment_id < lower_key + chunk AND tracking_code IS NULL;
    lower_key := lower_key + chunk;
    COMMIT;            -- releases this chunk's row locks; each chunk is its own transaction
  END LOOP;
END
$$;
```

- Walk the primary key in ranges (keyset). `WHERE col IS NULL LIMIT n` without an index rescans
  from the start every batch.
- Set the column default **before** the backfill, so rows inserted during it are already filled.
- Keep batches small enough that each commits in well under a second on production hardware. On
  very large tables, run the backfill as a throttled background job, outside the deploy, and watch
  replication lag.
- Run inside a transaction block, `COMMIT` fails with `invalid transaction termination`. That's how
  you find out the runner wrapped your file.

## Check a migration empirically before shipping

Run each statement of the migration against a copy with realistic data, inside `BEGIN ... ROLLBACK`,
and look at what it actually did:

```sql
BEGIN;
SELECT relfilenode, pg_stat_get_xact_tuples_returned(oid) + pg_stat_get_xact_tuples_fetched(oid)
FROM pg_class WHERE oid = 'shipments'::regclass;                         -- note both values
-- <the DDL under test>
SELECT relfilenode, pg_stat_get_xact_tuples_returned(oid) + pg_stat_get_xact_tuples_fetched(oid)
FROM pg_class WHERE oid = 'shipments'::regclass;   -- new relfilenode => rewritten; difference => rows read
SELECT mode FROM pg_locks
WHERE relation = 'shipments'::regclass AND pid = pg_backend_pid() AND granted;  -- locks this tx now holds
ROLLBACK;
```

Use the difference: the `xact` counters can still include unflushed counts from earlier
transactions in the same session. A large difference together with `ShareLock`,
`ShareRowExclusiveLock` or `AccessExclusiveLock` means the statement blocks writes for as long as
that scan takes in production. Statements that refuse to run in a transaction (`CONCURRENTLY`) can't
be checked this way. Know their locks from the table above.

## Review checklist

- [ ] For each statement: lock mode, tables, and whether it scans, rewrites or builds.
- [ ] No scan, rewrite or index build under `SHARE` or stronger on a table with live traffic.
- [ ] Indexes are built and dropped `CONCURRENTLY`, one statement per call, outside any transaction,
      with invalid leftovers dropped before a rebuild.
- [ ] Foreign keys and CHECKs are added `NOT VALID` and validated in a **later transaction**. Verify
      the runner really commits in between.
- [ ] NOT NULL goes through a NOT VALID constraint (PG 18) or a validated CHECK (PG 12-17), never a
      bare `SET NOT NULL`.
- [ ] No volatile default in `ADD COLUMN`, and no type change that rewrites a big table.
- [ ] Backfills are batched and each batch commits. The default is in place before the backfill.
- [ ] `lock_timeout` is set for strong-lock DDL (`SET LOCAL`, or `RESET` after a session-level
      `SET`), and the deploy can retry.
- [ ] Code and schema order: expand, deploy the code that uses both shapes, backfill, contract.
- [ ] Applied migrations are untouched. The whole history still applies to an empty database.

## Anti-patterns

- `ALTER TABLE t ADD COLUMN c uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE` → rewrites `t` and
  builds the index under `ACCESS EXCLUSIVE`. Split it: add the column, set the default, backfill,
  build the index concurrently, add NOT NULL as NOT VALID and validate.
- `ADD CONSTRAINT ... NOT VALID; VALIDATE CONSTRAINT ...;` in one file of a transactional runner →
  same as a validated ADD. Move `VALIDATE` to a later, separately committed step.
- `CREATE INDEX CONCURRENTLY` in a normal migration → it errors inside the transaction. A plain
  `CREATE INDEX` "fixes" the error by blocking writes. Use the runner's no-transaction mode instead.
- `UPDATE big_table SET ...` in the same transaction as the `ALTER TABLE` that added the column →
  `ACCESS EXCLUSIVE` held for the whole backfill. Separate transactions, batched.
- `ALTER COLUMN event_id TYPE bigint` on a large table → full rewrite. Add a `bigint` column, keep it in
  sync with a trigger, backfill, build indexes concurrently, then swap in a short transaction.
- `RENAME COLUMN` while old code still runs → old pods error out. Expand/contract over two deploys.
- `SET lock_timeout` in a no-transaction file without `RESET` → silently applies to later migrations
  in the same session.
- A short `lock_timeout` on `CREATE INDEX CONCURRENTLY` → an `INVALID` index on timeout, and an
  `IF NOT EXISTS` retry keeps it.

## More

- [references/lock-matrix.md](references/lock-matrix.md): lock, scan and rewrite behaviour per
  statement, measured on 18.6.
- [references/recipes.md](references/recipes.md): full recipes, including type changes, renames,
  partitioned-table indexes and dropping columns.
- [references/runners.md](references/runners.md): how common migration tools handle transactions.
- [references/sources.md](references/sources.md): the documentation and experiments behind every claim.
