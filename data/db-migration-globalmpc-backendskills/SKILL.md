---
name: db-migration
description: Rules for database schema changes. Use for any new table, column, index, constraint, enum or trigger, any data backfill, and any migration file.
---

# Schema change

Examples are Postgres. Assume the table is large and the app is live: deploys are rolling, so the previous
version of the app keeps running against the new schema for a few minutes.

## 1. Expand, then contract: never rename or drop in the same deploy

Why: the version still running during the deploy queries the old name and fails until the deploy finishes.

```sql
-- Bad: the running version breaks the moment this migration lands
alter table customers rename column name to full_name;

-- Good, deploy 1: add the new column and fill it. Keep it in sync until every server runs the new code
-- (write both in the app, or use a trigger).
alter table customers add column full_name text;
update customers set full_name = name where full_name is null;  -- batch it on big tables (rule 4)
-- Deploy 2, once nothing reads the old column: drop name.
```

The same applies to dropping a table or column, and to narrowing a type. Adding is safe. Removing waits
for a later deploy.

## 2. Indexes on big tables are built concurrently

Why: a plain `create index` blocks every write to the table until it finishes, which can take minutes.

```sql
-- Bad
create index invoices_customer_id_idx on invoices (customer_id);

-- Good: its own migration file, nothing else in it
create index concurrently invoices_customer_id_idx on invoices (customer_id);
```

`concurrently` can't run inside a transaction. Many runners wrap each migration, or a multi-statement
file, in one transaction, so keep the statement alone in its file (or use the runner's no-transaction
option). The same goes for `drop index concurrently`.

If the build fails (a deadlock, a duplicate in a unique index), Postgres keeps a broken INVALID index
under that name. Don't add `if not exists`: the retry would skip it and leave it broken. Drop it with
`drop index concurrently` and build again. Find leftovers with
`select indexrelid::regclass from pg_index where not indisvalid`.

## 3. Don't hold a lock while waiting for one

Why: `alter table` waits behind a long-running query, and every other query on the table queues behind
the `alter table`. A one-millisecond change takes the API down.

```sql
-- Good: give up quickly and retry the deploy rather than block the table
set local lock_timeout = '5s';  -- "local": only until this migration's transaction ends
alter table invoices add column note text;
```

A plain `set` stays on the connection after the migration, so the next query that reuses it gives up
after 5 seconds too. If your runner doesn't run the migration in a transaction, `set local` does nothing:
use `set`, then `reset lock_timeout` at the end.

- New column that is nullable, or has a constant default (Postgres 11+; older versions rewrite the whole
  table for a default): fine. NOT NULL without a default on a table with rows: fails.
- New foreign key or CHECK on a big table: add it `not valid`, then `validate constraint` in a later
  migration. Validation doesn't block writes.

## 4. Backfill in batches

Why: one `update` over millions of rows holds row locks for its whole run and bloats the table.

```sql
-- Bad: one statement, every row locked until it ends
update customers set full_name = name;

-- Good: walk the table by id in small batches (a script or job, outside the schema migration).
-- $1 starts at 0, then is the highest id the previous batch returned. Stop when a batch returns no rows.
update customers set full_name = name
where id in (select id from customers where id > $1 order by id limit 5000)
returning id;
```

Move forward by id, not by "rows still empty". A row whose source is NULL stays empty after the update,
so `where full_name is null` picks it again forever.

## 5. Rules live in the database

Why: app validation gives nice error messages, but only the database guarantees them. That covers
another service, a script, or a race between two requests.

Use NOT NULL, foreign keys, UNIQUE (this is what stops duplicate rows when two requests arrive at once), and
CHECK for ranges and allowed values (`check (seats between 1 and 10)`, `check (balance_cents >= 0)`).

Rows that must never change once written (audit logs, ledgers, history) get a trigger that rejects
UPDATE, DELETE and TRUNCATE:

```sql
create function audit_log_append_only() returns trigger language plpgsql as $$
begin
  raise exception 'audit_log is append-only';
end $$;
-- "for each statement": TRUNCATE never fires row triggers
create trigger audit_log_append_only before update or delete or truncate on audit_log
  for each statement execute function audit_log_append_only();
```

## 6. Every migration can be undone, and is checked

Why: a migration that can't be rolled back turns a bad deploy into an outage.

- Write the reverse next to it, undoing exactly what the migration did: drop what you created (tables,
  columns, indexes, constraints, triggers, functions, types) in reverse order.
- A down migration can't bring back data: after a contract step drops a column or table, the down
  recreates it empty. That's why the drop waits for its own later deploy (rule 1). Copy or back up
  the data first if you might need it.
- Never edit a migration that has been merged: other databases already ran it. Write a new one.
- Before calling it done, run the round trip: migrate up, run the down, migrate up again.

## Make it yours

Your team's choices. A line that says "not set" means: follow what the repo already does.

- **Where the down migration goes:** not set. Tools with `up()`/`down()` (TypeORM, Knex, …): write `down()`.
  Plain SQL files: put it where the repo keeps its down migrations, or ask.
- **Running migrations:** not set; use the repo's script.
- **Big table threshold:** treat any table that can grow past ~100k rows as big.
