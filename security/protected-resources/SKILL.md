---
name: protected-resources
description: "Super-Admin-only lock-down pattern. Use before touching admin.admins, admin.admin_audit_log, is_super_admin() / requireSuperAdmin() / selectIsSuperAdmin, app/api/admin/admins/**, app/(admin)/administration/users/admins/**, the admin RPCs (admin_promote, admin_update, admin_revoke, admin_list, admin_list_audit, admin_find_user_by_email), createAdminClient(), a new RLS policy, SECURITY DEFINER RPC, or admin-gated route, or when locking a sensitive table to Super Admin."
---

# Protected Resources — Single Path of Resistance

> 🚨 **Never remove, narrow, supersede or suppress `platform_admin_read`** — it is our own admin database access (the admin dashboard reads every row through it). Check before and after any policy change: `../common-docs/policies/our-own-admin-database-access.md` (the query must return 0).

This skill is the canonical pattern for protecting tables/operations from contributors who have the codebase but should NOT be able to modify the data. It assumes the threat model: **regular admins have commit access, can read .env files, can deploy from branches, and can call the API with their own session token**.

**Rule of thumb:** if the wrong person controlling the codebase could cause real damage, the protection has to be in the **database**, not in TypeScript.

---

## Threat model — what you're defending against

A `developer` or `senior_admin` admin who has the codebase can:
- Edit `requireSuperAdmin()` to remove the check, push to a branch, deploy from their machine.
- Call any API route directly via curl with their own auth token, skipping the UI.
- Read `.env.local` for any leaked keys.
- Use `createAdminClient()` (service role) if that key is reachable from their environment.

The naive answers — "guard the route", "check the selector", "hide the button" — all fail. The codebase is hostile territory.

---

## The five-layer defense (load-bearing → soft)

| # | Layer | Where it lives | Bypassable by a regular admin? |
|---|---|---|---|
| 1 | **Service-role key isolation** | Only in Vercel production env. Never in any committed `.env*`. Never in dev tooling. | Only if leaked. **This is the foundation; without it, layers 2–3 fold.** |
| 2 | **RLS deny-writes** on the protected table | Postgres policy: `FOR ALL USING (false) WITH CHECK (false)` for `authenticated`. Lets `service_role` through (Supabase default). | **No — DB-enforced.** |
| 3 | **`SECURITY DEFINER` RPCs gated by `is_super_admin()`** | Postgres function. Begins with `IF NOT public.is_super_admin() THEN RAISE EXCEPTION ...`. The ONLY supported write path. | **No — DB-enforced.** |
| 4 | **`requireSuperAdmin()` in the API route** | Server-side TS check before calling the RPC. Better error messages, same effect. | Yes — but DB still rejects. Belt-and-suspenders. |
| 5 | **`selectIsSuperAdmin` UI gate** | Hides the page/button. UX, not security. | Yes — anyone can curl. Layers 1–3 are what stop them. |

**Layers 1–3 are what actually keep the data safe. Layers 4–5 are good UX and clean error paths.**

---

## The "single path of resistance" rule

Every mutation to a protected table goes through ONE choke point: a `SECURITY DEFINER` RPC. There is no other way in. Audit logging hangs off that one path so you only have to monitor one thing.

```
                  ┌──── direct .schema('admin').from('admins').insert(...)  ❌ blocked by RLS
                  │
                  ├──── direct API route writing the table  ❌ blocked by RLS
   any caller ───┤
                  ├──── service-role client                 ⚠️ bypasses RLS — service-role-only paths must be tightly held
                  │
                  └──── RPC admin_promote()  ✅ checks is_super_admin() + writes audit row
                              │
                              ▼
                        admin.admins (RLS denies direct writes)
                              │
                              ▼
                        audit trigger → admin.admin_audit_log
```

**Never add a second mutation path.** If you find yourself calling `createAdminClient().from('admins').update(...)` from a route, stop — wrap it in an RPC instead. Two paths means two things to audit and two things to keep in sync. The whole point of this pattern is that there is exactly ONE place to look when investigating.

---

## Current protected resources (Matrx Main)

| Resource | RLS | Mutation RPCs | Audit |
|---|---|---|---|
| `admin.admins` | self-select + super-admin-select; deny all writes | `admin_promote`, `admin_update`, `admin_revoke` | `admin_audit_log` (trigger captures every INSERT/UPDATE/DELETE) |
| `admin.admin_audit_log` | super-admin-only select; deny all writes | (only the trigger writes) | self-evident; immutable by design |

Read RPCs:
- `admin_list()` — all admins + email/last-sign-in
- `admin_list_audit(limit, offset)` — audit log with actor + target emails
- `admin_find_user_by_email(email)` — for the promote-by-email flow
- `is_super_admin()` — boolean, used inside other RPCs and as the RLS condition
- `get_admin_status()` — `(is_admin, admin_level)` for the current `auth.uid()`, used by SSR boot

API routes (all check `requireSuperAdmin()` first, then call the RPC):
- `app/api/admin/admins/route.ts` — GET (list) / POST (promote)
- `app/api/admin/admins/[userId]/route.ts` — PATCH (update level / permissions / metadata) / DELETE (revoke)
- `app/api/admin/admins/audit/route.ts` — GET (audit log)
- `app/api/admin/admins/lookup/route.ts` — GET (find user by email)

UI: `app/(admin)/administration/users/admins/page.tsx` (list views on the canonical MatrxDataTable)

Bricking guards inside the RPCs (worth knowing — they raise `42501`):
- Cannot demote yourself out of `super_admin`.
- Cannot revoke yourself.
- Cannot demote/revoke the **last** Super Admin.

---

## Recipe: locking down a new table

When the user says "I don't want regular admins touching X" (billing, feature flags, secrets, audit data, anything sensitive), do exactly this — in order. Skipping a step breaks the model.

### 1. Secret-key isolation (one-time, project-wide)

The admin/secret key is **`SUPABASE_SECRET_KEY`** (`sb_secret_*`). The legacy JWT-based `SUPABASE_SERVICE_ROLE_KEY` is **deprecated and BANNED in this repo** — ESLint blocks reintroduction. See [Supabase API keys docs](https://supabase.com/docs/guides/getting-started/api-keys).

If either key (or any `sb_secret_*` value) appears in a committed `.env*` file, that's the first thing to fix. Production env vars only. If it's already isolated, skip.

### 2. Migration: RLS + RPCs + audit

Use [`migrations/admin_management_rls_and_rpcs.sql`](../../../migrations/admin_management_rls_and_rpcs.sql) as the template. Substitute your table name and adjust the gate (`is_super_admin()` is fine for most cases; if you want a different bar, define it once and reuse).

Mandatory pieces:
1. `ALTER TABLE public.X ENABLE ROW LEVEL SECURITY;`
2. `CREATE POLICY ... FOR ALL USING (false) WITH CHECK (false);` for writes.
3. A SELECT policy that's as restrictive as the data deserves (super-admin-only is a fine default).
4. One `SECURITY DEFINER` RPC per legitimate write operation. **Each RPC starts with:**
   ```sql
   IF NOT public.is_super_admin() THEN
     RAISE EXCEPTION 'Forbidden: Super Admin required' USING ERRCODE = '42501';
   END IF;
   ```
5. A `public.X_audit_log` table with the same shape as `admin_audit_log` (or extend `admin_audit_log` if it makes sense).
6. An `AFTER INSERT OR UPDATE OR DELETE` trigger that writes audit rows. The trigger is `SECURITY DEFINER` so it works regardless of caller. **The trigger must supply `organization_id` on every audit INSERT** — it is NOT NULL with no default (the DDL guard refuses a default), so omitting it makes every write to the audited table die on `23502`; a row that belongs to no customer carries the platform tenant, read from `iam.system_orgs` where `key = 'system'`, never hardcoded.
7. `GRANT EXECUTE ON FUNCTION ... TO authenticated;` for each RPC.

### 3. API routes

Mirror [`app/api/admin/admins/`](../../../app/api/admin/admins/):
- `requireSuperAdmin()` first — clean 401/403.
- Then `supabase.rpc('your_rpc', { ... })` — the user's own JWT carries `auth.uid()` into the RPC, which is what `is_super_admin()` reads.
- Map RPC error codes: `42501` → 403, `23503` → 404, else 400.

**Do not** use `createAdminClient()` here. The whole point is that the user's JWT must reach the DB so `auth.uid()` can be checked. Service role bypasses RLS — fine for system jobs, wrong for user-initiated writes.

### 4. UI

Place under `app/(admin)/administration/<resource>/`. The `(admin)` layout requires an admin (`checkIsUserAdmin`) — it does NOT require Super Admin. For Super-only surfaces the real gate is the API route (`requireSuperAdmin()`) + the RPC (`is_super_admin()`); optionally hide the page/nav with `selectIsSuperAdmin` for UX.

For per-action confirmation, use the imperative `confirm()` from `@/components/dialogs/confirm/ConfirmDialogHost` (or `<ConfirmDialog />` inline). **Never** `window.confirm` — see CLAUDE.md.

### 5. Register in `categories.tsx` and `navigation-links.tsx`

Add an entry to:
- [`app/(admin)/administration/categories.tsx`](../../../app/(admin)/administration/categories.tsx) — appears on the admin landing page.
- [`constants/navigation-links.tsx`](../../../constants/navigation-links.tsx) — appears in the admin sidebar.

### 6. Verify

After running the migration:
1. Hit the API as a non-admin → must 401/403.
2. Hit it as a super-admin → must succeed.
3. Try a destructive op via direct `.from('X').delete()` with a regular admin's JWT → must be blocked by RLS.
4. Confirm the audit log has rows after a successful change.

---

## DO

- ✅ Put the gate in the RPC (`is_super_admin()`), not just the API route.
- ✅ Treat the audit log as the SINGLE place to look when investigating "who changed what".
- ✅ Use `requireSuperAdmin()` in the API route too — fast 401/403, doesn't depend on a network round-trip to the DB to know it's forbidden.
- ✅ Reuse the existing `is_super_admin()` helper across RPCs. Don't redefine the check.
- ✅ Use `SECURITY DEFINER SET search_path = public` on every RPC and trigger. Without `SET search_path`, you've opened a search-path injection foothold.
- ✅ When you add a new mutation RPC for an existing protected table, add a matching audit-trigger case (or extend the existing trigger). Don't let a write path skip the audit log.

## DON'T

- ❌ Add a `.from('protected_table').insert/update/delete(...)` anywhere (for the `admin` schema tables, that's `.schema('admin').from('admins'/'admin_audit_log')`). There should be ZERO such call sites in the codebase. RLS will block them anyway, but the call site is a maintenance hazard — it implies the model is "RLS plus app-level checks" when it should be "RLS plus RPCs."
- ❌ Use `createAdminClient()` for user-initiated writes to a protected table. Service role bypasses RLS — that's the point — but it also bypasses `auth.uid()`, so `is_super_admin()` returns false (correctly: there is no current user). Use the user's normal client + RPC.
- ❌ Add a second mutation path "for convenience". Convenience is the enemy of monitoring. One choke point, one audit log, one thing to read.
- ❌ Disable RLS "temporarily" on a protected table. There is no temporarily.
- ❌ Set `SECURITY INVOKER` on the management RPCs. They have to be DEFINER so they can read/write past RLS — the gate inside the function is what makes it safe.
- ❌ Skip the bricking guards (last super admin, self-demote, self-revoke). The user can lock themselves out and there's no clean recovery without service-role access.
- ❌ Log secrets, tokens, or full row contents from the audit trigger if the table has sensitive columns. Audit `before` / `after` JSONB fields ARE persisted forever — sanitize at the trigger level if needed.

---

## Monitoring (the "ensure admins never take advantage" part)

The audit log is the single source. Two ways to read it:

1. **UI:** [/administration/users/admins](../../../app/(admin)/administration/users/admins) — bottom of the page, last 50 entries.
2. **SQL:** `SELECT * FROM public.admin_list_audit(p_limit := 500);` (or query `admin_audit_log` directly with super-admin SQL access).

Things to look for periodically:
- `actor_user_id IS NULL` rows — those are service-role / system writes (e.g. a migration). Should be rare and explainable.
- `update` rows where `before.level = 'super_admin'` — privilege grants. Confirm each one was intentional.
- Rapid bursts (many rows in a short window) — could be automation gone wrong.
- `revoke` of an active user — confirm with the actor.

If a regular admin manages to bypass all five layers, the audit row is still written by the DB trigger (the trigger runs as DEFINER regardless of who triggered it). Tampering would require modifying the trigger function itself, which requires service-role / SQL editor access — the same key/access boundary as layer 1.

---

## When the gate isn't `is_super_admin()`

For surfaces that should be open to "any admin level" (not Super-only), use:
- TS: `requireAdmin()` / `selectIsAdmin` / `state.userAuth.isAdmin`
- SQL: `EXISTS (SELECT 1 FROM admin.admins WHERE user_id = auth.uid())` — there's no shipped helper for this since the default IS super-only.

For surfaces that need a specific tier (e.g. "developer or above"), gate on `state.userAuth.adminLevel` directly — read `selectAdminLevel` and check the values you want. Don't invent new boolean selectors per tier; the level enum is the source of truth.

This skill, the `is_super_admin()` helper, and `admins.level` cover everything. If you find yourself adding a new gate primitive, stop and re-read this file — odds are the existing primitives compose into what you need.
