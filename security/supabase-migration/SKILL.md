---
name: supabase-migration
description: Use when changing kasane's Supabase schema — adding or altering a table, column, index, policy or grant, regenerating `src/types/supabase.ts`, or when asked about RLS, row-level security, or whether user data is exposed.
---

# Supabase Migration

kasane ships its Supabase **publishable** key in the client bundle (`src/api/supabase.ts`). That is correct and intended: it is anon-scoped. It also means **RLS is the entire security boundary.** A table created without policies is either invisible or wide open, and there is no server tier to catch the mistake.

## The two data classes

| Class                           | Tables                                                                | Rule                                                                                                                                        |
| ------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Catalog** (public, read-only) | `series`, `arc_mappings`, `movies`, `search_aliases`, `genre_filters` | `for select using (true)`; `grant select ... to anon, authenticated`. No client writes, ever.                                               |
| **User data** (owner-scoped)    | `user_progress`, `user_preferences`                                   | `for all using (auth.uid() = user_id) with check (auth.uid() = user_id)`; `grant select, insert, update, delete ... to authenticated` only. |

A new table joins one of these classes. If it fits neither, that is the design question to resolve before writing SQL.

## Every migration

1. **Look first.** `list_tables`, and read `supabase/migrations/20260715000000_kasane_catalog_and_user_data.sql` for the established shape.
2. **Write the file** as `supabase/migrations/<YYYYMMDDHHMMSS>_<slug>.sql`. Keep the existing style: lower-case SQL, a comment block per section, `bigint generated always as identity` primary keys, `timestamptz not null default now()` for `created_at`/`updated_at`.
3. **Every new table needs four things.** Omitting any one is the bug:
   ```sql
   alter table public.<t> enable row level security;
   create policy "<t> are readable by everyone" on public.<t> for select using (true);
   grant select on public.<t> to anon, authenticated;
   create index <t>_<col>_idx on public.<t> (<fk or filtered column>);
   ```
   `enable row level security` **without** a policy denies everyone, including the app. A policy **without** `enable row level security` does nothing at all. Both failure modes are silent at migration time.
4. **`with check` on anything writable.** `using` gates which rows are read and updated; `with check` gates what a row may become. A user-writable policy with only `using` lets a user reassign a row to another `user_id`.
5. **Apply** via `apply_migration` (service role, bypasses RLS), never the app's publishable key.
6. **Regenerate types**, which the data layer reads directly:
   ```bash
   # via Supabase MCP generate_typescript_types, or:
   bunx supabase gen types typescript --project-id obtgldkascmxbtpnvscn > src/types/supabase.ts
   bun run typecheck
   ```
7. **Run the advisors.** `get_advisors` with the security lint catches missing RLS, exposed views, and mutable search paths. Treat its output as part of the migration, not optional.
8. **Verify as an anonymous client**, not as the service role:
   ```sql
   set local role anon;
   select * from public.<t> limit 1;          -- catalog: rows. user data: none.
   insert into public.<t> ...;                -- catalog: must fail.
   ```

## Consumers to update

A catalog column change ripples: `src/types/supabase.ts` → the row-to-domain converters in `src/data/catalog.ts` (`toArc`, `toMovie`, `rowToMapping`) → the `SeriesMapping` types in `src/types/index.ts` → `scripts/audit-mappings.ts`. Grep for the column name before assuming the migration is done.

The catalog is fetched once and cached for 7 days, so a removed column keeps arriving from stale client caches. Prefer adding a nullable column over renaming one.

## Common mistakes

| Mistake                                                 | Consequence                                                                            |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `enable row level security` with no policy              | The app silently reads zero rows.                                                      |
| A policy with no `enable row level security`            | The table is fully open to anon.                                                       |
| Writable policy with `using` but no `with check`        | A user can reassign a row to someone else's `user_id`.                                 |
| Granting `insert` on a catalog table to `authenticated` | Any signed-up user can rewrite the mappings every client trusts.                       |
| Editing the existing migration file                     | It has already run. Add a new timestamped file.                                        |
| Forgetting `generate_typescript_types`                  | `src/types/supabase.ts` drifts and typecheck passes on a schema that no longer exists. |
| Dropping or renaming a column in one step               | Clients hold a 7-day cached catalog and break. Add nullable, migrate, remove later.    |
