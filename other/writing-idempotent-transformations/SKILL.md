---
name: writing-idempotent-transformations
description: Write data transformations and loads that produce the same result no matter how many times they run — using MERGE/upsert, deterministic partition overwrites, deduplication, and stable keys. Use when a retry could duplicate data, a job is not safe to re-run, a pipeline needs exactly-once effects, or loads must be backfill-safe.
---

# Writing Idempotent Transformations

## When to use

- A task may be retried (orchestrator retries, manual re-runs, replays).
- A backfill must not change already-correct numbers or create duplicates.
- You are writing an incremental load, upsert, or partition refresh.
- Do NOT use for one-off exploratory queries with no persisted side effects.

## Why it matters

Failures are normal. Retries, backfills, and replays run the same logic again.
If a job is idempotent, running it once or five times yields the same final
state — so recovery is safe and boring. If not, retries duplicate rows and
backfills silently change history. This is the single most reported source of
data incidents.

## Workflow

```
- [ ] Define the unit of work and its natural key
- [ ] Make writes overwrite-by-key or overwrite-by-partition (never blind append)
- [ ] Remove dependence on wall-clock time / autoincrement / random order
- [ ] Verify: running twice == running once (row counts and checksums match)
```

1. **Pick a deterministic key** for each output row (business key, or a hash of
   the identifying columns).
2. **Replace `INSERT`-append with `MERGE`/upsert** keyed on that key, or with a
   full **partition overwrite** for the window being processed.
3. **Remove non-determinism**: don't key on `now()`, sequence values, or
   unordered `row_number()`; derive timestamps from the data/event, not the run.
4. **Test it**: run the transform twice on the same input and assert identical
   output (count + checksum).

## Patterns

**Delete-insert by partition** — the simplest idempotent load for a time window:
delete the target partition, then insert its freshly computed rows in one
transaction. Re-running reprocesses only that window and cannot duplicate.

```sql
BEGIN;
DELETE FROM fct_orders WHERE order_date = DATE '2026-01-15';
INSERT INTO fct_orders
SELECT ... FROM staging WHERE order_date = DATE '2026-01-15';
COMMIT;
```

**MERGE/upsert by key** — when rows update in place:

```sql
MERGE INTO fct_orders t
USING staging s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET amount = s.amount, status = s.status
WHEN NOT MATCHED THEN INSERT (order_id, amount, status)
VALUES (s.order_id, s.amount, s.status);
```

**Deduplicate deterministically** — keep the latest version per key with a stable
tiebreaker, so the result never depends on scan order:

```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY order_id ORDER BY updated_at DESC, source_file DESC
  ) AS rn
  FROM staging
) WHERE rn = 1;
```

**dbt incremental** — use a `unique_key` and `merge` strategy so re-runs upsert
rather than append; use `insert_overwrite` on partitioned warehouses.

## Common pitfalls

- **Blind `INSERT ... SELECT`** in a retried task — the classic duplicate source.
- **Keying on `current_timestamp`/`uuid()`** — makes every run produce new rows.
- **`ROW_NUMBER()` without a tiebreaker** — nondeterministic when timestamps tie.
- **Appending to a partition instead of overwriting it** — backfills accumulate.
- **Non-transactional delete+insert** — a mid-run failure leaves the target empty;
  wrap both in one transaction or use atomic overwrite.

## References

- [Backfill-safe checklist and anti-patterns](references/CHECKLIST.md)
