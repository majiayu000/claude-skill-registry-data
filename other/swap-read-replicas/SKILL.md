---
name: swap-read-replicas
description: Send read queries to Postgres read replicas. Use when the user decides the primary needs relief from reads, or asks about read replicas or splitting reads and writes. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Add read replicas

- **Interface:** `Database` (`read`, `write`, `disconnect`) in `packages/db/src/client.ts`.
- **Today:** `createDatabase` returns the same primary client for `read` and `write`.
  Repositories already choose per query: `read` for lists and dashboards that tolerate
  lag, `write` for changes and any read that must see them.
- **Provided by** `DatabaseModule.forRoot` (`packages/nest-common/src/database.ts`),
  called in each service's `src/app.module.ts` (api, worker, notifications, webhooks).
- **Env:** `<SERVICE>_DATABASE_URL` and `<SERVICE>_DATABASE_POOL_MAX` from `databaseEnv`
  in `packages/nest-common/src/env.ts`.

## Swap

1. In `createDatabase`, build `read` from a replica URL when one is given (a second
   `createDb`, or Prisma's read-replicas extension on the primary), and disconnect both.
   Row-level security works the same: policies and grants replicate.
2. Add an optional `<SERVICE>_DATABASE_REPLICA_URL` to `databaseEnv`, pass it through
   `DatabaseModule.forRoot` in each service that wants it, and document it in
   `.env.example` and `docs/environment.md`. Unset keeps today's behaviour.
3. Deployed: the replica's URL per role in the `db-<role>` secrets (the data chart,
   `deploy/charts/data`) and its pooler.
4. Audit reads that follow a write in the same request: they must use `write`
   (`database.write` or inside the `tenantTx`), or the user sees stale data.

The Python service (`apps/ai/app/db/session.py`) has one engine; it's separate.

## Tests

`packages/db/test/security.test.ts` (row-level security and privileges). Integration
suites run with `read` equal to `write`; add a test that points `read` at a separate
client and checks a repository's read-after-write paths use `write`.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
