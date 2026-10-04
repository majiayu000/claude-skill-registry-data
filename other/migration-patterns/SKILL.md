---
name: migration-patterns
description: Safe schema-migration patterns for systems under live traffic — expand/contract, backfill, double-write, shadow-read, online DDL. Use when authoring, reviewing, or sequencing a migration that can't take a maintenance window.
---

# Migration patterns

Assume: the service is running, writes are arriving, you cannot take a maintenance window. Most production migrations live here.

## The universal rule

**Never couple a schema change to a code change in the same deploy.** They fail independently, and you need each to be reversible independently.

## Expand → Migrate → Contract

The safe three-phase dance for any non-trivial change:

1. **Expand** — add the new shape alongside the old. No caller depends on it yet.
2. **Migrate** — move data to the new shape. Switch readers. Switch writers. Backfill anything left.
3. **Contract** — drop the old shape once nothing reads or writes it for a cooling-off period.

Each phase is a separate deploy. Each is independently revertable.

## Common change patterns

### Add a column
- **Safe**: `ALTER TABLE ... ADD COLUMN ... NULL`. No lock (or brief, depending on engine).
- **Danger**: `NOT NULL` with no default on a large table — full-table rewrite, long lock. Use a default (cheap if metadata-only in your engine) or expand/migrate/contract: add nullable → backfill → add NOT NULL constraint.

### Drop a column
- Ship code that stops reading it. Deploy. Wait a release.
- Ship code that stops writing it. Deploy. Wait a release.
- Drop the column.
- Never reverse this order.

### Rename a column
- Effectively: add new → dual-write → backfill → switch reads → stop writing old → drop old.
- Never `ALTER TABLE ... RENAME COLUMN` while code is live. Callers break.

### Change column type
- Add a new column with the target type.
- Dual-write (writers write both).
- Backfill the new column.
- Switch readers to the new column.
- Stop writing the old.
- Drop the old.

### Add an index on a large table
- **Postgres**: `CREATE INDEX CONCURRENTLY` — no table lock. Monitor for failure.
- **MySQL**: online DDL since 5.6 for most index adds. Check `ALGORITHM=INPLACE, LOCK=NONE`.
- Never just `CREATE INDEX` on a hot table without `CONCURRENTLY` / online algorithm.

### Add a foreign key
- Add the column first, without the constraint.
- Backfill valid values.
- Add the constraint `NOT VALID` (Postgres) so new rows are checked.
- `VALIDATE CONSTRAINT` later during low traffic.

### Partitioning
- Create the new partitioned table alongside.
- Shadow-write to both.
- Backfill.
- Switch reads.
- Drop the old.

## Backfill patterns

- **Batch in chunks** by primary key range. Size the chunk so a single chunk finishes in ~1s.
- **Sleep** between chunks. Leave room for user traffic and replication lag.
- **Checkpoint** progress in a table or file; a restart should resume, not re-scan.
- **Track replica lag** on Postgres/MySQL. If lag climbs, slow down.
- Avoid `UPDATE ... WHERE condition` on the whole table in one shot. It will bite.

Sketch:

```sql
-- in a loop, with checkpointing and sleep
UPDATE users
SET email_lower = LOWER(email)
WHERE id > $last_id
  AND id <= $last_id + 10000
  AND email_lower IS NULL;
```

## Dual-write safely

When writers must update both old and new:

- Apply the write to both inside the same transaction if they're in the same DB.
- If cross-store, use an outbox table — write to outbox in the transaction, publish async.
- Reject writes where the dual-write fails, unless the business accepts loss on the new path during rollout.

## Shadow-read for confidence

Before switching reads:

- Run both queries (old and new), compare results, log mismatches.
- Fix mismatches in the backfill, not in the read path.
- Only cut over when mismatch rate ≈ 0 for a sustained window.

## Reversibility

Every migration has a reverse. Write both up and down migrations. For destructive ops (drops, renames), the reverse might be "restore from backup" — state that explicitly, and get a snapshot before you run it.

## Checklist before you run it

- [ ] Ran on a restored copy of prod-sized data? Measured duration.
- [ ] Identified locking behavior on this engine, for this size.
- [ ] Backup / snapshot present and verified.
- [ ] Rollback path documented.
- [ ] Oncall notified. Deploy freeze if needed.
- [ ] Feature flag / flagged query gate, so readers/writers can switch without redeploy.

## Anti-patterns

- Migrations mixed into feature PRs. Can't revert independently.
- `DELETE FROM ... WHERE ...` to "clean up" at scale — use batched archival instead.
- `CREATE INDEX` without `CONCURRENTLY` on a live Postgres table — locks writes.
- `SELECT *` in backfill queries — read only what you need.
- Running a migration in the ORM's auto-migrate mode in production. Use explicit migration files, versioned and reviewed.
