---
name: secure-supabase-rls
description: Use when adding or changing a Supabase table, view, function or storage bucket exposed through the Data API, or auditing one — enables RLS, writes per-operation role-scoped policies, indexes them, keeps definer functions private, and proves allow and deny with pgTAP.
---

# Secure Supabase RLS

RLS is the authorization boundary: the publishable key is public, so every row is reachable by anyone who holds a grant, and only a policy narrows it. The app's route guards are UX.

## 1. Audit current state

Read `.claude/stack-profile.md` (`database.host: supabase`, `backend.track`). Exposed schemas are `[api] schemas` in `supabase/config.toml` (default `public`, `graphql_public`). Run against the local stack (`--linked` for a remote):

```bash
pnpm supabase db advisors --local --type security            # the Security Advisor, same checks as the Dashboard
pnpm supabase db query --local "select n.nspname, c.relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where c.relkind in ('r','p') and n.nspname='public' and not c.relrowsecurity"
pnpm supabase db query --local "select schemaname, tablename, policyname, roles from pg_policies where roles = '{public}'"      # policies without a TO clause
pnpm supabase db query --local "select tablename, policyname from pg_policies where qual ~* 'user_metadata|raw_user_meta' or with_check ~* 'user_metadata|raw_user_meta'"
ls supabase/tests/*rls* 2>/dev/null
```

More queries (views, definer functions, grants, storage, unwrapped `auth.uid()`): [rls-patterns.md](./rls-patterns.md), "Audit queries". Each hit is a finding; report them before changing anything.

## 2. Decide what to do

- Table without RLS, or with RLS and no policy for an operation the app uses → steps 4–6.
- Policy without `to`, with `user_metadata`, or with a bare `auth.uid()` → fix in place (step 5), new migration.
- View without `security_invoker`, definer function in an exposed schema → step 5.
- No `supabase/tests/<table>_rls.test.sql` → step 6 even if the policies look right.
- All present and `supabase test db` green → "already in place".

## 3. Detect what the table is

Ask of each table, not of the codebase: who may read it, who may write it, and which column ties a row to its owner or tenant.

| Shape | Policy basis |
|---|---|
| Owner rows (`user_id`) | `(select auth.uid()) = user_id` |
| Tenant rows (`team_id`) | membership through a private definer function ([rls-patterns.md](./rls-patterns.md)) |
| Public read, server write | `select` grant and policy for `anon, authenticated`; no write grant |
| Server-only (jobs, audit log) | no grant to `anon`/`authenticated` at all; RLS on as a backstop |

## 4. Install only what's missing

Nothing to install: pgTAP ships with the local stack (`supabase test new`, `supabase test db`). For tenant tables, `supabase-test-helpers` is optional; plain `set local role` works without it ([rls-test-patterns.md](./rls-test-patterns.md)). Make sure the baseline privileges migration from [set-up-supabase](../set-up-supabase/SKILL.md) exists, so a new table does not start with every grant.

## 5. Write the migration — grants, RLS, policies, indexes in one file

```bash
pnpm supabase migration new secure_notes
```

```sql
create table public.notes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users (id) on delete cascade,
  body text not null,
  created_at timestamptz not null default now()
);

alter table public.notes enable row level security;
revoke all on table public.notes from anon, authenticated;
grant select, insert, update, delete on table public.notes to authenticated;

create policy "notes: owner reads" on public.notes for select
  to authenticated using ((select auth.uid()) = user_id);

create policy "notes: owner inserts" on public.notes for insert
  to authenticated with check ((select auth.uid()) = user_id);

create policy "notes: owner updates" on public.notes for update
  to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

create policy "notes: owner deletes" on public.notes for delete
  to authenticated using ((select auth.uid()) = user_id);

create index notes_user_id_idx on public.notes (user_id);
```

Rules in force (reasons in [rls-patterns.md](./rls-patterns.md)):

- One policy per operation, each `to authenticated` (or `anon, authenticated` for deliberate public reads).
- `(select auth.uid())`, never bare `auth.uid()`: the `select` makes Postgres evaluate it once per statement.
- An index on every column a policy filters, with that column first in the index.
- Authorization data comes from `app_metadata` or a table, never `user_metadata` (users can edit it).
- Views: `create view … with (security_invoker = true) as …`. A definer view hands out the rows the table policies withhold.
- Definer functions live in a schema that is not exposed (`private`), with `set search_path = ''`, schema-qualified names, and `revoke execute … from public` plus an explicit grant.
- Storage: policies on `storage.objects`, scoped by `bucket_id` and the owner folder; `anon` listing needs `storage.allow_any_operation`. See [rls-patterns.md](./rls-patterns.md), "Storage".
- The admin client (`SUPABASE_SECRET_KEY`) bypasses all of this: it must filter by the caller's id itself.

## 6. Test allow and deny with pgTAP

```bash
pnpm supabase test new notes_rls.test        # creates supabase/tests/notes_rls.test.sql
```

Cover `select`, `insert`, `update`, `delete` for `anon`, the owner and a stranger; pair every denied write with a check that the row is intact. A denied `using` filters silently (zero rows, no error), so assert emptiness, not an error; a missing grant or a failed `with check` raises `42501`. Template and the assertion table: [rls-test-patterns.md](./rls-test-patterns.md).

## 7. Wire into CI

`supabase test db` and `supabase db advisors --local --fail-on error` run in the PR job from [set-up-supabase](../set-up-supabase/SKILL.md). A new table without a test file fails review, not CI: add the audit query for tables lacking RLS to the PR checklist.

## 8. Verify

```bash
pnpm supabase db reset && pnpm supabase test db     # Result: PASS
pnpm supabase db advisors --local --type security --level warn   # no ERROR; warnings explained or fixed
curl -s "$SUPABASE_URL/rest/v1/notes?select=*" -H "apikey: $SUPABASE_PUBLISHABLE_KEY"   # anon: 401/permission denied or [], never rows
```

Run the curl against the local stack. Expected: no rows for `anon`, and the test run lists a denial for every operation.

## References
- [rls-patterns.md](./rls-patterns.md) — rules, anti-examples of common leaks, audit queries, storage.
- [rls-test-patterns.md](./rls-test-patterns.md) — pgTAP structure for owner and tenant tables.
- [../set-up-supabase/SKILL.md](../set-up-supabase/SKILL.md) — baseline privileges, CI.
- [../../core/_shared/security-baseline.md](../../core/_shared/security-baseline.md) — rule 3, authorization at the data boundary.
