---
name: postgresql
description: Use when using PostgreSQL for application data or personal tooling — running a user-level instance without root (initdb and pg_ctl on a private port, listening on localhost only), schema migrations, constraints and indexes, EXPLAIN ANALYZE, safe upserts, backups with pg_dump, and connecting from scripts. Also use when a query is slow, a tool must start its own database on demand, or data integrity relies on application code alone.
---

# PostgreSQL

Default: a current major version, schema changes as ordered SQL migrations in git, constraints in the database (not only in code), connections over a local socket or `localhost`, `pg_dump` backups on a schedule.

## A user-level instance (no root)

When a tool needs its own database on a workstation:

```bash
initdb -D "$DATA" --auth=scram-sha-256 --pwfile=<(printf '%s' "$PGPASS_INIT") -U app
pg_ctl -D "$DATA" -o "-p 55432 -c listen_addresses=localhost" -l "$DATA/server.log" start
createdb -p 55432 -U app appdb
```

- Pick an unusual port to avoid clashing with a system instance.
- Listen on `localhost` only; nothing on the network should reach it.
- Let the tool start the server if it is not running (check with `pg_isready -p 55432`), so users never manage it by hand.
- Binaries can be unpacked from distribution packages into a user directory when installing system-wide is not possible.

## Schema

- Primary keys (`bigint generated always as identity` or UUIDs), `NOT NULL` by default, `CHECK` constraints for valid ranges, foreign keys with deliberate `ON DELETE` behaviour, `UNIQUE` for natural keys.
- `timestamptz` for times; `numeric` or integer minor units for money; `text` over `varchar(n)` unless a limit is a rule.
- Migrations are forward-only files (`0001_init.sql`, `0002_add_index.sql`) applied in a transaction and recorded in a table.

## Queries

- Upsert with `INSERT ... ON CONFLICT (key) DO UPDATE SET ...` — atomic, no read-then-write race.
- Always use parameters (`$1`, driver placeholders); never format SQL strings with user input.
- `EXPLAIN (ANALYZE, BUFFERS)` before adding indexes; index the columns in `WHERE`, `JOIN` and `ORDER BY` of frequent queries; check that the plan uses them.
- Large deletes and updates in batches to avoid long locks.

## Backups

- `pg_dump -Fc appdb > backup.dump` regularly; test restores with `pg_restore` into a scratch database — an untested backup is a hope.

## Verification loop

1. Apply all migrations to an empty database; the app's tests pass against it.
2. Constraint tests: inserting invalid rows fails.
3. `EXPLAIN ANALYZE` of the top queries shows index use and acceptable times.
4. Restore the latest backup successfully.

## Pitfalls

- **`timestamp` without time zone** stores wall-clock times that drift across zones; use `timestamptz`.
- **Connection storms** from short-lived processes; reuse connections or add a pooler.
- **Long transactions** block vacuum and hold locks; keep them short.
- **Implicit casts** (comparing `text` to numbers) prevent index use.
- **Major upgrades** need `pg_upgrade` or dump/restore; the data directory is not forward-compatible.
