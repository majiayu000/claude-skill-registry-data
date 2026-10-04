---
name: rls-enforcement
description: |
  Operating Row-Level Security at RUNTIME: the two-pool service-context model
  (DATABASE_SERVICE_URL bypass vs the app pool), the non-owner runtime role (nextspark_app)
  and cutover, MIGRATE_DATABASE_URL, fail-closed LIST/READ enforcement, and ownershipFilter.
  Use this WHENEVER a DB call mysteriously returns 0 rows (or too many) for some users, a
  query/insert started failing after switching DATABASE_URL, a webhook / scheduled-action /
  login path hits a Postgres permission error, you're choosing between the app pool and the
  service (bypass) pool, or composing a transaction that mixes user-scoped and system writes —
  even if the words "RLS" or "cutover" never appear. Also for forcing the service pool
  (team/subscription bootstrap), doing/debugging the cutover, and extending core RLS policies
  from a theme. For policy SQL see database-migrations; for queryWithRLS usage see
  service-layer; for can_bypass_rls/superadmin see api-bypass-layers.
allowed-tools: Read, Glob, Grep
version: 1.1.0
---

# RLS Enforcement Layer Skill

**Canonical reference (read for SQL + cutover runbook):**
`packages/core/docs/10-backend/03-rls-policies.md` → "Enforcement Layer (beta.167+)".
This skill is the agent-facing companion: the operational rules and gotchas, not a
re-paste of the SQL.

## When to use this skill

- Adding/auditing a DB call and deciding **app pool (RLS) vs service pool (bypass)**.
- Anything that writes the **first** team membership/subscription (bootstrap).
- Doing or debugging the **RLS cutover** (`nextspark_app`, `DATABASE_SERVICE_URL`, `MIGRATE_DATABASE_URL`).
- A theme that needs to **override a core RLS policy** (e.g. widen a tier on `users`/`subscriptions`).
- Touching `generic-handler.ts` permission checks or `ownershipFilter`.

## 1. Two pools, routed by presence of `userId` (`src/lib/db.ts`)

| Helper | With `userId` | Without `userId` |
|---|---|---|
| `queryWithRLS` / `queryOneWithRLS` / `mutateWithRLS` / `getTransactionClient` | **app pool** (`SET LOCAL app.user_id`, RLS evaluated) | **service pool** (bypass) |

- **`query` / `queryOne` / `queryRows` ALWAYS go to the service pool (bypass).** They are
  system operations by definition. **Never** use them for a user-scoped read that must be
  RLS-filtered — use `queryWithRLS(sql, params, userId)`.
- **Force service even with a `userId`:** `mutateWithRLS(sql, params, userId, { service: true })`
  or `getServiceTransactionClient()`.
- `DATABASE_SERVICE_URL` falls back to `DATABASE_URL` when unset → pre-cutover behavior is
  unchanged (the app still connects as owner; nothing breaks).
- **A transaction is bound to ONE pool + ONE GUC at acquisition.** `getTransactionClient(userId)`
  / `getServiceTransactionClient()` acquire a single client up front; every `tx.query/.mutate`
  runs on that pool. You **cannot** do a user-scoped RLS read and a service-pool bootstrap write
  in the *same* `tx`. If a flow needs both, run the bootstrap as a service transaction and do
  the RLS reads/writes as separate `queryWithRLS(..., userId)` calls (or sequence them: commit
  the membership first, then the user-scoped write can satisfy RLS).
- **Atomicity:** `mutateWithRLS` wraps **each call** in its own BEGIN/COMMIT — N calls = N
  transactions. For "insert order + 3 items atomically", use `getTransactionClient(userId)`
  (one GUC, one commit/rollback), not N `mutateWithRLS` calls.

## 2. When you MUST force the service pool

Bootstrap writes that create the **first** membership/subscription of a team can't pass the
membership-based RLS insert policies under the new member's own GUC (they aren't a member
yet). These run on the **service pool**, authorized at the API/action layer (not RLS):

- `TeamService.create`, `teams/actions.ts:createTeam`, `addUserToGlobalTeam`,
  `TeamMemberService.add` (via `{ service: true }`).

If you add a new "first-membership" writer, route it the same way or it will break under RLS.

**Other legitimate service-pool actors** (no request user → service pool by routing, since they
call with no `userId`): Better Auth login/verification, the **scheduled-actions processor**,
**payment-provider webhooks**, the superadmin/developer bypass check. Inside such a system path,
any *user-scoped* sub-operation must re-introduce the resolved userId via
`queryWithRLS(..., userId)` so RLS applies for that slice.

> ⚠️ **The inverse is a security hole.** Force the service pool **only** for work that
> *structurally* cannot satisfy RLS (first-membership/subscription, pre-login auth, webhooks/
> scheduler with no user). **Never** add `{ service: true }` to a normal user-scoped read/write
> to "fix" a 0-rows or permission-denied bug — that silently disables tenant isolation and leaks
> cross-tenant data. A 0-rows bug means a missing policy / missing `userId` / missing
> `entity.list` permission — fix *that*, don't bypass RLS.

## 3. Runtime role + cutover gotcha

- Migration `022_rls_runtime_roles.sql` creates `nextspark_app` (non-owner, member of
  `authenticated`, **no** `BYPASSRLS`) + grants + `anon` lockdown.
- **Migrations run as the OWNER** via `MIGRATE_DATABASE_URL` (falls back to `DATABASE_URL`);
  the runtime runs as `nextspark_app`.
- **GOTCHA:** post-cutover `DATABASE_URL` is a **non-owner** role — any op that assumed owner
  (raw DDL, seeds, `query()` expecting full access) behaves differently. Keep owner work on
  the migrate/service connection.
- Cutover is **opt-in**: leave `DATABASE_SERVICE_URL` unset and nothing changes.

## 4. Fail-closed permission enforcement (`generic-handler.ts`)

- LIST and READ now check the session entity permission (was create/update/delete only).
  A member without `entity.list`/`entity.read` → **403**. Admin-bypass and api-key (scope)
  paths are skipped.
- A **thrown error** in the permission check returns **`500 PERMISSION_CHECK_FAILED`**
  (fail-closed) — never "allow". Themes must declare `list`/`read` per entity
  (`default`/`starter` already do).
- **api-key vs session — two different layers, two different behaviors:**
  - The **entity-permission** check is session-only (api-key uses scopes), so it's *skipped* for api-key.
  - But **DB RLS still applies to api-key** requests — api-key auth carries a `userId`, so reads
    route to the app pool and policies evaluate (team isolation holds).
  - **`ownershipFilter` (role-based row scoping) is OFF for api-key and admin-bypass**
    (`resolveOwnershipFilter` returns `{applies:false}` for those). So an api-key caller is *not*
    narrowed to "their own" rows by `ownershipFilter`; they see everything their team-RLS policy
    allows. To restrict api-key callers, scope the key narrowly or enforce it in a DB RLS policy
    (which fires for any app-pool request), not via `ownershipFilter`.

## 5. `ownershipFilter` (entity `access` config, `entities/types.ts`)

- `linkedBy` is **optional** → omit for **direct-field** ownership (entity row carries the
  owner id; filtered against the current user).
- `linkedBy.softDelete` makes the `deletedAt IS NULL` clause conditional — set `false` for
  tables without a `deletedAt` column (avoids a 42703 undefined-column error).

## Debugging & validating

**"Returned 0 rows after the cutover" (worked before, member gets `[]`, superadmin still sees all).**
RLS is now live. Triage in order:
1. **403 vs `[]`?** A `403` = fail-closed permission (member lacks `entity.list`/`read`, or theme
   didn't declare it). An empty `[]` (200) = permission passed but RLS filtered all rows. They
   are different bugs.
2. **Is a `userId` actually passed?** A missing `userId` routes to the service pool → would
   *over*-return, not under-return. So `[]` means a `userId` *is* present and RLS is filtering.
3. **Is `DATABASE_SERVICE_URL` set to a real bypass/owner role?** If unset, the "service" pool is
   *also* `nextspark_app` (no bypass) → even system reads get filtered. Most common cutover
   mistake. Set it.
4. **Does a policy exist?** RLS-enabled **with no policy** blocks ALL rows. Confirm a policy
   `TO authenticated` exists and `nextspark_app` is a member of `authenticated` (it is, per 022).
5. **Reproduce as the runtime role** (below). If empty there too, it's the policy / membership /
   `ownershipFilter`, not the app wiring.

**Validate/test RLS as the real runtime role (not the owner — owner bypasses RLS, proving nothing).**
`nextspark_app` is NOLOGIN, but `022` runs `GRANT nextspark_app TO current_user`, so the
test/migrate user can assume it:
```sql
BEGIN;
SET LOCAL ROLE nextspark_app;
SET LOCAL app.user_id = '<teamA_member_id>';
SELECT count(*) FROM "invoices" WHERE "teamId" = '<teamB_id>';  -- expect 0 (cross-tenant denied)
COMMIT;
```
Always include a positive control (same query as a team-B member → > 0), or a `0` is meaningless.
Seed fixtures via the service pool / owner (first-membership inserts can't satisfy RLS).

## Non-obvious rules (do not relearn the hard way)

- **RLS primitives live in migration `001`** (`can_bypass_rls`, `auth_user_can_see_user`,
  `is_superadmin`) — because the hardened policies in `002` use them, and `002` runs before
  the tables/functions a later migration would define. A policy with a forward dependency on
  a later table fails at `CREATE POLICY` time; wrap such logic in a `SECURITY DEFINER` helper
  defined in `001` (table refs resolve at call time). Cite `001`, not the stale `002:102`
  comment that still says "010".
- **`team_role` is `TEXT`** (not an ENUM). Themes add roles via config
  (`availableTeamRoles` + `permissions.config.ts`) — **never** `ALTER TYPE team_role`.
- **Theme override of a core RLS policy** runs in **phase 2** (after core). It must `DROP`
  the core policy by name and recreate its own — dropping **both** the legacy AND the current
  core policy names, or the policies **coexist** (RLS combines them with OR, loosening the
  restriction). See campus `9035/9036` for the pattern.
- **Don't break the metadata self-read policy** (`003_user_metas`): login reads the user's own
  flags under RLS via `MetaService.getEntityMetas(..., userId)`.
- **`anon` is not the app's public-read path.** Public reads enter with `userId=null` →
  service pool (bypass), filtered in SQL by the handler. `TO anon` policies + the `022`
  `anon` revoke are defense for the **Supabase Data API / PostgREST**, not app traffic.

## Anti-patterns

- ❌ Using bare `query()`/`queryOne()` for a user-scoped read that must be RLS-filtered (it
  bypasses RLS via the service pool).
- ❌ Adding a hardened policy that references `team_members`/`can_bypass_rls` to an **early**
  migration (e.g. 002) without a helper in 001 → forward-dependency failure.
- ❌ `ALTER TYPE team_role ADD VALUE ...` in a theme → the type no longer exists.
- ❌ A theme override that drops only the legacy core policy names → coexisting policies.
- ❌ Returning "allow" when a permission check throws → must be fail-closed.

## Checklist (the cross-cutting ones the body's rules don't already make obvious)

- [ ] DB call routing chosen deliberately: user-scoped → `queryWithRLS(..., userId)`; system → `query*`/no-userId; bootstrap-only → `{ service: true }`. **Not** `{ service: true }` to silence a 0-rows bug.
- [ ] No transaction tries to mix a user-scoped (app-pool) op and a service-pool (bootstrap) op on the same `tx`.
- [ ] Multi-row atomic write uses `getTransactionClient(userId)`, not N `mutateWithRLS` calls.
- [ ] New core-table policy: primitive deps already defined in `001` before the migration that uses them.
- [ ] New entity exposes `list`/`read` permissions (else 403 under enforcement); api-key callers restricted by scope or a DB policy (not `ownershipFilter`).
- [ ] Theme RLS override drops legacy AND current core policy names.

## Related skills

- `database-migrations` — RLS policy SQL patterns, migration structure.
- `service-layer` — `queryWithRLS`/`mutateWithRLS` usage and service classes.
- `api-bypass-layers` — `can_bypass_rls()`, superadmin/developer bypass.
- `permissions-system` — team roles, tiers, permission checks.
- `scheduled-actions` — background/webhook handlers (service-pool actors with no request user).
