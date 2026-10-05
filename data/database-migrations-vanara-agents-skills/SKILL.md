---
name: database-migrations
description: How to write safe, reversible, zero-downtime database schema migrations — additive-first changes, the expand/migrate/contract pattern, batched backfills, concurrent index builds, safe NOT NULL, rollbacks, and the locking pitfalls that cause outages. A deep reference with runnable checks.
type: skill
version: 2.0.0
updated: 2026-06-29
---
# Database Migrations

A migration runs against **live data while old code may still be serving traffic**. The dangerous moment
is never the steady state before or after — it's the in-between, when the schema has changed but not every
app instance has. Design every change to be correct *during* that window. Heavy detail lives in
`references/`; copy-paste material in `examples/`; a runnable safety check in `scripts/`.

## Mental model

Two things deploy on different clocks: your **schema** (one atomic change) and your **code** (rolled out
instance-by-instance over minutes). A migration is safe only if **both the old and new code work against
both the old and new schema** for the overlap window. That single rule explains almost every practice
below.

| Concern | Safe answer |
|---|---|
| What changed | the smallest possible step |
| When old code sees it | it must still work (backward-compatible) |
| Locks held | none long enough to block traffic |
| If it goes wrong | a tested, reversible path back |
| Big rename/retype | expand → migrate → contract, across deploys |

## 1. Additive-first

Prefer **additive, backward-compatible** changes. Adding a nullable column, adding a table, or adding an
index never breaks code that doesn't know about it. Destructive changes (drop/rename column, change type,
add `NOT NULL`) break the old code still running mid-deploy, so they must be sequenced — see §3.

```sql
-- SAFE: old code ignores the new column; new code can start using it.
ALTER TABLE users ADD COLUMN email_verified_at timestamptz NULL;

-- UNSAFE in one step: old code still INSERTs rows without this column.
ALTER TABLE users ADD COLUMN email_verified_at timestamptz NOT NULL;
```

## 2. Never hold a long lock

Most outages from migrations are **lock waits**, not data loss. A statement that rewrites a table or takes
an `ACCESS EXCLUSIVE` lock blocks every read/write behind it, and that queue backs up into your connection
pool within seconds.

- Add columns as **nullable** (or with a constant default — on modern Postgres a constant default is
  metadata-only and does not rewrite the table; a *volatile* default does).
- Build indexes with `CREATE INDEX CONCURRENTLY` (no table rewrite, no write lock — but it can't run
  inside a transaction).
- **Backfill in batches** with short transactions, not one giant `UPDATE` that locks every row.
- Set a `lock_timeout` so a migration that *can't* get its lock fails fast instead of stalling traffic.

```sql
SET lock_timeout = '3s';            -- fail fast rather than queue behind traffic
CREATE INDEX CONCURRENTLY idx_orders_status ON orders (status);
```

Full catalogue of which operations rewrite/lock and the safe alternative: `references/zero-downtime-changes.md`.

## 3. Expand / migrate / contract

The core pattern for any breaking change (rename, retype, split, add `NOT NULL`) without downtime. It
spreads one logical change across **multiple deploys** so old and new code always overlap safely:

1. **Expand** — add the new shape (nullable column / new table / new index). Backward-compatible.
2. **Migrate** — deploy code that **dual-writes** old+new, then **backfill** existing rows in batches,
   then switch **reads** to the new shape and verify.
3. **Contract** — once nothing reads or writes the old shape, drop it in a *later* deploy.

Each step is independently deployable and independently reversible. The full worked walkthrough
(including a column rename and a non-null-ification) is in `references/expand-contract.md`.

## 4. Reversibility & safety

Every migration should declare how to undo it. Some operations are **irreversible** in practice
(`DROP COLUMN`, `DROP TABLE`, `TRUNCATE` destroy data; a down-migration can recreate the *structure* but
not the *data*). Treat those specially:

- Provide a real `down` for reversible ops; for irreversible ones, document that recovery is **restore from
  backup**, and take a verified backup/snapshot immediately before.
- Separate the destructive `contract` step into its own migration so you can ship the safe parts and pause.
- Dry-run on a production-like copy and **time it** — a 30-minute backfill on staging may be hours in prod.

Reversible-vs-irreversible rules, backup checklists, and dry-run guidance: `references/rollback-and-safety.md`.
Validate a `.sql` file with `scripts/check-migration-reversible.mjs` before shipping.

## 5. Operational discipline

- **One concern per migration.** Mixing a schema change and a data backfill in one file makes rollback
  ambiguous and the transaction huge.
- **Forward-only in production.** Prefer rolling *forward* with a fix over rolling back a migration that
  already ran against live data; keep `down` for local/staging and emergencies.
- **Idempotent where possible** (`IF NOT EXISTS`, `IF EXISTS`) so a retried run after a partial failure
  doesn't error.
- **Backfills run outside the schema transaction**, in batches with a sleep, so they don't hold locks or
  bloat WAL/replication lag.

## Common pitfalls (failure modes)

- **`NOT NULL` in one shot** — adds a column the still-running old code inserts NULLs into, *or* triggers a
  full validating scan. Add nullable, backfill, then `SET NOT NULL` (validate via a `CHECK ... NOT VALID`
  then `VALIDATE`). See the zero-downtime reference.
- **Plain `CREATE INDEX`** on a hot table — takes a write lock for the whole build. Use `CONCURRENTLY`.
- **One giant `UPDATE` backfill** — locks millions of rows, blocks writes, balloons WAL. Batch it.
- **Rename a column in one deploy** — old code references the old name and 500s during the rollout window.
  Use expand/contract.
- **Volatile/changing default on add-column** — forces a full table rewrite under an exclusive lock.
- **No `lock_timeout`** — the migration silently queues behind a long transaction and takes the app down.
- **Destructive `down` that "reverses" a drop** — it recreates an empty column; the data is gone. Mark it
  irreversible and rely on backups.

## When NOT to use / trade-offs

- **Tiny project, maintenance window available.** If you can take 5 minutes of downtime at 3am and the
  table is small, a single blocking `ALTER` is simpler and cheaper than a three-deploy expand/contract.
  Zero-downtime machinery is overhead you only need at scale or with strict SLAs.
- **Throwaway / pre-launch schemas** with no real data — just recreate the schema; migrations add ceremony
  you don't need yet.
- **NoSQL / schemaless stores** shift the work to the application (versioned documents, read-time
  migration) rather than DDL — the expand/contract *idea* still applies, the SQL specifics don't.
- **Data migrations vs schema migrations** are different beasts; heavy data reshaping often belongs in a
  background job, not a migration runner that blocks deploys.

## Files in this package

- `references/expand-contract.md` — the expand/migrate/contract pattern, worked end-to-end
- `references/zero-downtime-changes.md` — per-operation safe recipes (add column, backfill, index, NOT NULL)
- `references/rollback-and-safety.md` — reversible vs irreversible ops, backups, dry-runs
- `examples/add-column-safe.sql` — a safe, batched, reversible migration
- `examples/migration-config.example.json` — a migration runner config with safety guardrails
- `scripts/check-migration-reversible.mjs` — Node check that flags irreversible SQL + missing down-migrations

Pairs with the `database-scaling` skill, the `data-modeling` skill, and the `database-reviewer` agent.
