---
name: knex-pro
description: Knex.js query-builder guidance — migrations, seeds, transactions, query patterns, and production config.
category: development
---

## Overview

Knex is a SQL query builder for Node.js — not an ORM. It gives you composable, parameterized queries across Postgres, MySQL, SQLite, and MSSQL without hiding the SQL. Teams that want full control over their queries, or that find ORMs too magical, use Knex as the sane middle ground between raw SQL strings and a full object mapper.

With that control comes responsibility: there's no model layer to lean on, so schema knowledge lives in your migrations and your discipline. This skill covers Knex migrations, transaction patterns, query composition, and production configuration.

## When to use

- Building a Node.js data layer with explicit SQL control.
- Writing and organizing Knex migrations and seeds.
- Composing dynamic queries (filters, sorting, pagination).
- Managing transactions correctly in Knex.
- Choosing between Knex, an ORM, and raw SQL.
- Using Knex with Objection.js as a model layer on top.
- Tuning connection pools for production.

## Core concepts

- **Query builder, not ORM.** `knex("orders").where({status: "paid"}).select("id")` builds parameterized SQL. You own the mapping between rows and objects — which means no magic and no magic failures.
- **Migrations.** Timestamped files with `up`/`down` (`knex migrate:make add_orders`); `knex migrate:latest` applies. Migrations are plain code — use the schema builder or raw SQL, and always write `down`.
- **Seeds.** `knex seed:make` + `knex seed:run` for dev/test data; keep seeds idempotent and environment-gated.
- **Transactions.** `knex.transaction(async (trx) => {...})` — use `trx` for every query inside. Like Sequelize, forgetting `trx` silently escapes the transaction.
- **Connection pooling.** Knex manages the pool (`pool: { min, max }`); size per environment, set `acquireConnectionTimeout` to fail fast when saturated.
- **Composability.** Builders are immutable-ish chainables — write helper functions that take a builder and add clauses conditionally. This is how you build dynamic filters cleanly.
- **Raw with bindings.** `knex.raw("... WHERE status = ?", [status])` for what the builder can't express; bindings keep it injection-safe.
- **No model layer.** Row → object mapping is yours. Many teams pair Knex with Objection.js (built on Knex) for models; others keep it lean with plain functions.
- **Dialect awareness.** The builder abstracts common SQL but each dialect has specifics (returning clauses, upsert syntax, DDL differences) — test against the real database.
- **Streaming.** `.stream()` for processing large result sets without loading them into memory — essential for exports and batch jobs.
- **Batch inserts.** `knex.batchInsert` (or multi-row `insert`) for bulk loads; chunk large batches to avoid parameter limits.
- **Migrations in CI/CD.** Run `migrate:latest` as a deploy step; never concurrently from multiple app instances — use a release phase or advisory lock.
- **Query events.** Knex emits query events — hook them for logging, timing, and slow-query detection in development.
- **Types via TS.** Knex has TypeScript support with table-type declarations; define row types once and get typed results.

## Practical workflow

1. **Set up knexfile.** Per-environment configs (client, connection, pool, migrations directory); connection strings from env vars, never hardcoded.
   ```js
   // knexfile.js
   module.exports = {
     production: {
       client: "pg",
       connection: process.env.DATABASE_URL,
       pool: { min: 2, max: 20, acquireTimeoutMillis: 10000 },
       migrations: { directory: "./migrations" },
     },
   };
   ```
2. **Write migrations.** `knex migrate:make add_orders`; schema builder for DDL; always implement `down`; review generated SQL for large tables (concurrent index creation).
   ```js
   exports.up = (knex) => knex.schema.createTable("orders", (t) => {
     t.uuid("id").primary().defaultTo(knex.raw("gen_random_uuid()"));
     t.string("status").notNullable().defaultTo("pending");
     t.decimal("total", 10, 2).notNullable();
     t.timestamps(true, true);
     t.index(["status", "created_at"]);
   });
   exports.down = (knex) => knex.schema.dropTable("orders");
   ```
3. **Compose queries with helpers.** Builder functions for filters/sorting/pagination shared across endpoints.
   ```js
   function paginate(qb, { cursor, limit = 20 }) {
     if (cursor) qb.where("id", "<", cursor);
     return qb.orderBy("id", "desc").limit(limit + 1);
   }
   ```
4. **Transact multi-write operations.** `trx` everywhere inside; short and ordered; retry serialization failures.
   ```js
   await knex.transaction(async (trx) => {
     const [order] = await trx("orders").insert({...}).returning("id");
     await trx("inventory").where({...}).increment("reserved", 1);
   });
   ```
5. **Stream large results.** `.stream()` for exports and batch processing; never `select *` a million rows into memory.
6. **Use raw safely.** `knex.raw` with `?` bindings for CTEs, window functions, and dialect-specific SQL — never template-literal interpolation.
7. **Monitor queries.** Log query text + duration in dev; track slow queries in prod via the database's own tooling (pg_stat_statements).
8. **Deploy migrations safely.** Separate release step; back up before migrating; expand-contract for zero-downtime changes on hot tables.

## Common pitfalls

- **Forgetting `trx`** — queries silently escaping the transaction; pass it to every query inside.
- **String-interpolated raw SQL** — injection; always use bindings.
- **No `down` migration** — rollbacks impossible; write both directions.
- **Concurrent migrates** — multiple instances racing `migrate:latest`; run once per deploy.
- **Unbounded selects** — `knex("orders")` without limit on a huge table; always paginate or stream.
- **Pool misconfiguration** — defaults under load; size min/max and set acquire timeouts.
- **N+1 in application code** — loops of queries instead of joins; the builder makes joins easy, use them.
- **Loading everything into memory** — exports via `select` instead of `.stream()`; OOM on large tables.
- **Dialect-specific SQL in shared code** — breaking other environments; isolate dialect specifics.
- **Ignoring query logs** — slow queries invisible; log and review in development.
- **Seeds in production** — destructive seed runs; gate by environment and keep idempotent.
- **Huge batch inserts** — parameter limits exceeded; chunk batches (e.g., 1000 rows).
