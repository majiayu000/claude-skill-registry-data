---
name: db-change
description: Change the database schema safely (new table or column, index, RLS policy, grants, backfill, drop). Use when a feature needs to store something new or change how it's stored, or when the user mentions migrations, Prisma schema or row-level security.
---

# Change the database

1. Edit the owning schema's file in `packages/db/prisma/schema/` (`app.prisma` for product
   data; `docs/database.md` lists the owners). Follow `base.prisma`: `uuidv7()` ids,
   `timestamptz(3)`, `@map`/`@@map` to snake_case, `@@schema` on every model. A tenant
   table has `orgId` with an `organization` relation `onDelete: Cascade` and an index on
   `[orgId, id(sort: Desc)]`, like `Todo` in `app.prisma`.
2. `bun run db:migrate`. Prisma asks for a name, writes
   `packages/db/prisma/migrations/<timestamp>_<name>/migration.sql` and applies it.
3. Prisma can't express policies, grants or functions: append them to that
   `migration.sql` by hand. A new tenant table needs, in the same migration:
   ```sql
   ALTER TABLE app.<table> ENABLE ROW LEVEL SECURITY;
   ALTER TABLE app.<table> FORCE ROW LEVEL SECURITY;
   CREATE POLICY tenant_isolation ON app.<table>
     USING (org_id = nullif(current_setting('app.org_id', true), '')::uuid)
     WITH CHECK (org_id = nullif(current_setting('app.org_id', true), '')::uuid);
   ```
   Tables in `app` and `auth` get `app_api`'s grants automatically (default privileges
   in the init migration); any other role or schema needs an explicit `GRANT`, as
   narrow as the service needs (see the `files` and `webhooks` migrations). Per-user tables use
   `user_id` and `app.user_id` (`withUser`/`userTx`).
   Editing a migration Prisma already applied makes the next `bun run db:migrate` ask to
   reset the local database, which deletes local data: ask the user first.
4. `bun run db:lint` (Squawk). Fix what it flags; a statement that is safe in context
   gets `-- squawk-ignore <rule>` above it with the reason.
5. `bun run gen` (Prisma client). For `ai` tables, also update `apps/ai/app/db/models.py`.
6. Tests: `bun run test:integration` connects as the service roles, so a missing grant
   or policy fails there. The Python models are checked by
   `apps/ai/tests/test_models_match_db.py`.

## Expand, then contract

Migrations run before the new code, and the old release keeps serving during the
rollout and after a rollback. Every migration must work with both:

1. Add the column or table (nullable, or with a default). Never rename or change a type
   in place.
2. Backfill in batches, with `SET lock_timeout`.
3. Ship the code that reads and writes the new shape.
4. Drop the old column in a later release, once nothing running uses it.

Never edit a migration that is on `master`; write a new one.

## Finish

1. The verify skill (it runs `db:lint`, the drift check and the integration tests for a
   migration).
2. The `migration-reviewer` agent on the migration, and fix what it reports. Then the
   `reviewer` agent on the code that uses the new shape.
