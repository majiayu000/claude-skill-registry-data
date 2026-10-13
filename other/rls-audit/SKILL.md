---
name: rls-audit
description: This skill should be used to audit Row-Level Security and database permissions on a Postgres backend exposed through an auto-generated API — Supabase, InsForge, or any Postgres + PostgREST setup. Trigger phrases (English) include "audit my RLS", "review my policies", "is my database exposed", "can users see each other's data", "check the anon key", "row level security", "someone could read my tables", "security definer", "is USING (true) a problem". Trigger phrases (Spanish) include "auditá mi RLS", "revisá las políticas", "¿se puede leer mi base con la anon key?", "¿un usuario puede ver datos de otro?", "seguridad a nivel de fila". It compares what each table is MEANT to expose against what the live database actually allows, and proves every finding from outside with the public key. Not for MySQL, MongoDB or Firebase.
---

# RLS Audit

On a BaaS, the database **is** the API. The public key ships inside your JavaScript bundle, so anyone can send any query your grants and policies allow. This skill finds the gap between what you meant to expose and what the database actually permits.

Analogy: RLS is the bouncer at each door of a building. This skill doesn't ask the bouncer whether they're doing a good job — it walks up to every door with a visitor badge and tries the handle.

## Why a scanner is not enough

A generic scanner greps for `USING (true)` and flags it. That is wrong in both directions: a public price list is *supposed* to be `USING (true)`, while a policy that looks strict (`customer_id = auth.uid()`) can be useless if the user is the one who writes `customer_id`. The scanner has no way to know what you intended. **Intent is the missing input, and you have to declare it.** That declaration is Step 1.

## Scope

Postgres reachable through PostgREST-style auto APIs: Supabase, InsForge, Neon + PostgREST. The role names below (`anon`, `authenticated`) are the common ones — confirm yours. It does not apply to MySQL, MongoDB or Firebase rules.

This is a focused review, not a penetration test. For an app holding money or sensitive data, it is the step before a professional audit, not a substitute for one.

## Step 1 — Declare intent (once, in writing)

Classify **every** table and view into exactly one bucket. Ask the developer; do not guess from names. Save it as `docs/rls-intent.md` so the next audit starts from it.

| Bucket | Meaning | What "correct" looks like |
| --- | --- | --- |
| **public-reference** | Anyone may read it, on purpose (catalog, plans, public directory) | `SELECT` open; no write from API roles |
| **owner-scoped** | A row belongs to one user | Every policy ties the row to the caller's id |
| **tenant-scoped** | A row belongs to an organization | Every policy ties the row to a tenant the caller is a member of |
| **server-only** | Only your backend touches it (billing, tokens, audit log) | RLS on, **no policies**, grants revoked from API roles |

For each table also list the **columns the user must never write** (role, tenant id, owner id, price, status, plan) and the **columns the user must never read** (cost, tokens, provider ids, internal notes). Steps 3c and 3d check these.

## Step 2 — Read the live database, not the migrations

Policies can exist that no migration created: the platform's dashboard, an assistant, or a default template may have added them. Audit what is running.

```sql
-- RLS switched on?
select c.relname, c.relrowsecurity as rls, c.relforcerowsecurity as forced
from pg_class c join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relkind = 'r';

-- Every policy, with its conditions
select tablename, policyname, roles, cmd, qual as using_expr, with_check
from pg_policies where schemaname = 'public' order by tablename;

-- What the API roles are granted (RLS only matters where a grant exists)
select grantee, table_name, string_agg(privilege_type, ', ') as privileges
from information_schema.role_table_grants
where table_schema = 'public' and grantee in ('anon', 'authenticated', 'PUBLIC')
group by 1, 2 order by 2, 1;

-- What FUTURE tables will be granted
select pg_get_userbyid(defaclrole) as owner, defaclobjtype, defaclacl
from pg_default_acl;

-- Views: who owns them and whether they run as the caller
select c.relname, c.reloptions, pg_get_userbyid(c.relowner) as owner, r.rolbypassrls
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
join pg_roles r on r.oid = c.relowner
where n.nspname = 'public' and c.relkind = 'v';

-- SECURITY DEFINER functions and who may execute them
-- (proacl NULL = the default, which is EXECUTE granted to PUBLIC)
select p.proname, p.proconfig, p.proacl
from pg_proc p join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public' and p.prosecdef;
```

Diff the policy list against the migrations folder. Anything live that is not in a migration is a finding by itself: nobody reviewed it.

## Step 3 — The eight checks

Run each against the intent table from Step 1.

**a. RLS on everywhere.** Every table has RLS enabled. RLS on with no policies means deny-all — correct for server-only, a bug for anything else.

**b. Grants match intent — today and by default.** RLS is the second lock; the grant is the first. Many platforms grant full privileges to `anon` on every new table through `ALTER DEFAULT PRIVILEGES`, so a table or view created tomorrow is born open. Revoke, then grant back only what the bucket needs, and fix the default:

```sql
revoke all on all tables in schema public from anon, authenticated;
alter default privileges in schema public revoke all on tables from anon, authenticated;
-- then: grant select on <public-reference tables> to anon; etc.
```

Default privileges belong to the role that set them: repeat the `alter default privileges` with `for role <owner>` for each owner the Step 2 query lists. Then verify by reading the ACL back — do not assume the statement did what you meant.

**c. A policy that compares a column the user writes protects nothing.** `WITH CHECK (customer_id = auth.uid())` stops a user from inserting under someone else's id — but says nothing about the other columns in that row. Check every write policy for the never-write list. Fixes, strongest first:
- Drop the `UPDATE` policy and route the change through a server function. Enumerating forbidden columns is the list that will be one item short next time.
- Column-level grants: `grant update (display_name, avatar_url) on profiles to authenticated;`
- A `BEFORE UPDATE` trigger that raises when a frozen column changes (exempt your trusted server role explicitly).

**d. RLS filters rows, never columns.** If the user can read the row, the user can read every column of it from the browser console — whatever the UI hides. For the never-read list: expose a view that selects only the safe columns, or use column-level `GRANT SELECT`. Note that with column grants, `select=*` starts failing with "permission denied", so client queries must name their columns.

**e. Views run as their owner unless told otherwise.** A view owned by a role with `BYPASSRLS` skips every policy underneath, and a simple view is auto-updatable — a write to the view lands on the base table. Set `security_invoker = true` (Postgres 15+) and grant only `SELECT`. Side effect to check: an aggregate view under `security_invoker` returns different totals to different viewers, because each one sums only the rows they can see.

**f. `SECURITY DEFINER` functions are open doors with a guard you have to write.** For each one:
- It checks **who is calling** inside the body. A parameter such as `p_user_id` or `p_org_id` must be compared to the caller's identity, never trusted.
- `revoke execute on function … from public, anon;` — the default grants it to everyone.
- It sets a fixed `search_path`.
- Its role comparisons survive `NULL`. `role <> 'admin'` is neither true nor false when role is null, so the guard does not fire for an anonymous caller. Use `is distinct from` or check `auth.uid() is not null` first.

**g. Service-key code re-implements the rule.** Edge functions and server routes that use the service key bypass RLS completely. Each must filter by the caller's tenant itself, taking the tenant from the verified session — never from the request body. Put the rule in one shared gate and call it everywhere; two gates drift apart.

**h. Delete the policies of deleted features.** Search for policies granting to `anon` and ask what needs each one. A policy opened "so our own server could get in" outlives the feature it served. The fix for that need is the service key in the server, not a public policy.

## Step 4 — Prove it from outside

A finding is real when the public key demonstrates it. A fix is real when the same request stops working. Write the checks as a script that runs with the public key and with two ordinary users (A and B).

Rules that keep these tests honest:

- **Compare the data before and after — not the response.** An `UPDATE` blocked by RLS returns success with zero rows. So does a typo in the table name.
- **Watch each test fail first.** Run it against the unfixed database and see it red. A test that was green before the fix proves nothing.
- **Confirm the login worked before measuring.** A failed sign-in makes every "forbidden" assertion pass.
- **Require your own rejection text.** "Function not found" also leaves the row unchanged.
- **Test both ends.** Denied for B is only meaningful next to allowed for A.

Minimum set: anonymous read of every non-public table; user B reading and writing user A's rows; a user changing each never-write column on their own row; a user calling each `SECURITY DEFINER` function with someone else's id.

## Output

Deliver: the intent table (`docs/rls-intent.md`), the intent-vs-actual matrix with every mismatch ranked by what it exposes, one migration that fixes them (revokes, policies, triggers, views), and the outside-in test script with its red-then-green output. State plainly what was not checked. Never claim the database is secure.

## Field notes

`references/field-notes.md` lists the failures this checklist came from — each one found in a production app that had RLS enabled and passing tests. Read it when a finding looks too unlikely to be worth checking.

## Reference

PostgreSQL docs (Row Security Policies, `CREATE VIEW … security_invoker`, `ALTER DEFAULT PRIVILEGES`, `GRANT` column privileges), Supabase "Row Level Security" and "Hardening the Data API" guides, PostgREST docs (schema cache: `NOTIFY pgrst, 'reload schema'`). Pairs with `data-modeling` (the schema), `auth` (the roles), `multi-tenancy` (the tenant rule) and `secure-coding`.
