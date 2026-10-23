---
name: rls-reference
description: "Pure-reference catalog of row-level security for tenant isolation, Postgres-first. Covers enabling RLS (ALTER TABLE ... ENABLE ROW LEVEL SECURITY, default-deny semantics), CREATE POLICY syntax (USING vs WITH CHECK clauses, FOR SELECT/INSERT/UPDATE/DELETE/ALL, permissive vs restrictive, TO role_name), bypassing RLS (superuser / BYPASSRLS / table owner / FORCE ROW LEVEL SECURITY), tenant context patterns (current_user, current_setting, JWT claims via Supabase auth.uid() / auth.jwt()), and performance discipline (wrapping auth functions in SELECT, index on policy-referenced columns). Row/tenant isolation on the non-Postgres engines - MySQL / MariaDB invoker views, CockroachDB native RLS, Vitess vindex sharding, SQL Server security policies - lives in references/other-engines.md. Use as the RLS-pattern reference for tenant isolation on any of these engines. Consumed by cross-tenant-data-leak-tests."
---

# rls-reference

## Overview

Postgres Row-Level Security (RLS) lets the database itself enforce per-tenant
row visibility, independent of the application code. It is the canonical
defence-in-depth layer for pool / horizontally-partitioned tenancy models - even
if the application forgets to add a `WHERE tenant_id = ?` filter, the database
refuses to return another tenant's rows.

Per [postgresql.org/docs/current/ddl-rowsecurity.html](https://www.postgresql.org/docs/current/ddl-rowsecurity.html),
RLS "restricts which rows users can access based on per-user policies." Unlike
standard SQL `GRANT` / `REVOKE` privileges which act on whole tables, RLS
controls **row visibility and modification** per role.

This skill is a **pure reference** consumed by the tenant-leak test authors and
reviewers. Postgres is the primary engine; MySQL / MariaDB, CockroachDB, Vitess,
and SQL Server are covered in
[references/other-engines.md](references/other-engines.md). For the broader
model context see the isolation-models reference in
`cross-tenant-data-leak-tests`.

## When to use

- Designing tenant isolation on a Postgres-backed pool / bridge model (for
  MySQL / MariaDB, CockroachDB, Vitess, or SQL Server see
  [references/other-engines.md](references/other-engines.md)).
- Auditing existing RLS policies for correctness.
- Writing tests that verify RLS denies cross-tenant access (per
  `cross-tenant-data-leak-tests`).
- Onboarding a new table to the tenant_id discriminator pattern.

## How to use

1. Enable AND force RLS on every tenant-bearing table (`ENABLE` then `FORCE ROW
   LEVEL SECURITY`) so the table owner obeys policies too.
2. Pick a tenant context source from
   [references/tenant-context-patterns.md](references/tenant-context-patterns.md)
   and confirm the app sets it per transaction (`SET LOCAL`) from an
   authenticated session, never from request input.
3. Write the tenant policy using
   [references/create-policy-syntax.md](references/create-policy-syntax.md) and a
   shape from
   [references/policy-and-bypass-patterns.md](references/policy-and-bypass-patterns.md) -
   scope `USING` + `WITH CHECK` to the tenant discriminator.
4. Confirm the app connection role is not a superuser, lacks `BYPASSRLS`, and
   either does not own the table or runs with `FORCE ROW LEVEL SECURITY`.
5. Apply the performance discipline below: wrap auth functions in `SELECT` and
   index every policy-referenced column.
6. Run the statement-level and application-level tests as a non-privileged role;
   assert cross-tenant reads and writes fail.
7. Cross-check the policy against the Anti-patterns table before sign-off.

## Enabling RLS

```sql
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
```

Per Postgres docs: "Once enabled, a default-deny policy applies - no rows are
visible or modifiable unless explicitly allowed by a policy."

To disable:

```sql
ALTER TABLE accounts DISABLE ROW LEVEL SECURITY;
```

### Force RLS on table owner

By default, the **table owner bypasses RLS**. For tenant isolation this is
dangerous - the application's connecting role is often the table owner. Force
the owner to obey policies too:

```sql
ALTER TABLE accounts FORCE ROW LEVEL SECURITY;
```

Per Postgres docs, this is the production-safe default for multi-tenant tables.

## CREATE POLICY syntax

The full grammar plus `USING` vs `WITH CHECK`, per-command policies, permissive
vs restrictive combination, and `TO role_name` scoping:
[references/create-policy-syntax.md](references/create-policy-syntax.md).

## Tenant context patterns

The policy needs a source of truth for the current tenant. Four canonical
patterns - `current_setting()` with `SET LOCAL`, `current_user` / `session_user`,
Supabase `auth.uid()` / `auth.jwt()`, and in-policy JWT claim parsing:
[references/tenant-context-patterns.md](references/tenant-context-patterns.md).

## Policy patterns and bypass

The three tenant-isolation policy shapes (strict discriminator, tenant + per-row
ACL, admin override), the three RLS bypass categories (superuser / BYPASSRLS /
table owner), and the operations that always bypass RLS (FK, unique, TRUNCATE,
REFERENCES):
[references/policy-and-bypass-patterns.md](references/policy-and-bypass-patterns.md).

## Performance discipline

Per Supabase RLS performance docs:

| Practice | Effect |
|---|---|
| Wrap auth function calls in `SELECT` | Postgres optimiser caches result per statement (initPlan); 94%+ improvement on large tables |
| Specify `TO role_name` | Avoids policy evaluation for unrelated roles |
| Index on policy-referenced columns | 99%+ improvement for tenant_id-filtered queries |
| Include explicit filter in query | Helps query planner even when RLS adds implicit filter |

Bad:

```sql
USING ( auth.uid() = user_id )
```

Good (initPlan-cached):

```sql
USING ( (SELECT auth.uid()) = user_id )
```

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| RLS enabled but no policy | Default-deny means no rows return - broken silently | Always create at least one policy after enabling |
| Policy on table without `FORCE ROW LEVEL SECURITY` | Table owner bypasses; app role often is the owner | Add FORCE ROW LEVEL SECURITY |
| `current_user` for tenant_id without per-tenant roles | Tenants share a role; no isolation | Use SET LOCAL or JWT claim |
| `tenant_id` from request header -> SET LOCAL | Spoofable; never derive from request input | Derive from authenticated session/JWT only |
| `auth.uid()` not wrapped in SELECT | Per-row evaluation - major perf hit at scale | `(SELECT auth.uid())` for initPlan caching |
| No index on tenant_id | Sequential scan after policy filter | btree index on tenant_id always |
| Permissive policy + missing TO clause | Applies to all roles including superusers | Always specify TO app_user |
| Tests use superuser to verify policies | Bypasses RLS - test passes but prod leaks | Tests must connect as a non-superuser without BYPASSRLS |
| Trusting raw_user_meta_data in Supabase policies | User-modifiable per Supabase docs | Use raw_app_meta_data (server-set) |
| Single policy mixing tenant + per-row ACL with OR | Permissive OR widens access; one bad clause leaks tenant | Split into permissive (tenant) + restrictive (ACL) |

## Testing RLS policies

Two levels:

### Statement-level

```sql
-- Connect as app_user (no BYPASSRLS, not table owner)
SET LOCAL app.tenant_id = '11111111-1111-1111-1111-111111111111';
SELECT count(*) FROM documents;  -- should match tenant 1's count only

SET LOCAL app.tenant_id = '22222222-2222-2222-2222-222222222222';
SELECT count(*) FROM documents;  -- should match tenant 2's count

-- Attempt cross-tenant
SET LOCAL app.tenant_id = '11111111-1111-1111-1111-111111111111';
INSERT INTO documents (tenant_id, body)
VALUES ('22222222-2222-2222-2222-222222222222', 'leak');
-- Must fail with: new row violates row-level security policy
```

### Application-level

Run the existing test suite under a non-superuser, non-BYPASSRLS,
non-table-owner role. If passing tests rely on RLS bypass, the suite is silently
invalid for production. Per `cross-tenant-data-leak-tests` the gate test must use
a tenant-A session to attempt access to tenant-B-owned rows and assert 0 rows
returned.

## Worked example

Onboard a `documents` table to the strict tenant_id discriminator (Pattern 1).
Enable and force RLS, then create the policy scoped to `app_user`:

```sql
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON documents
    AS PERMISSIVE FOR ALL TO app_user
    USING (tenant_id = current_setting('app.tenant_id')::uuid)
    WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
```

The application runs `SET LOCAL app.tenant_id = '<uuid>'` from the authenticated
session at the start of every transaction. Connected as `app_user` (no
BYPASSRLS, not the table owner), the tester sets tenant 1 and runs
`SELECT count(*) FROM documents` - it returns tenant 1's rows only. Setting
tenant 1 and attempting `INSERT INTO documents (tenant_id, body) VALUES
('<tenant-2-uuid>', 'leak')` fails with `new row violates row-level security
policy`, because `WITH CHECK` rejects the foreign tenant_id. The table is isolated
for both reads and writes.

## Limitations

- **Constraint side channels.** FK and UNIQUE checks bypass RLS; this creates
  timing/error-message side channels.
- **RLS does not protect logs.** A query that filters to 0 rows still appears in
  `pg_stat_statements` and slow-query logs with the same SQL text. Log
  sanitisation is a separate concern.
- **No RLS on views by default.** A view that does `SELECT * FROM tenants`
  doesn't inherit RLS unless `WITH (security_invoker = true)` is set on the view
  (Postgres 15+).
- **Replication.** Logical replication does not respect RLS by default; the
  subscriber sees all rows. Per-publication filters needed.
- **Schema migrations.** ALTER TABLE for new columns runs as table owner - review
  whether new columns need to be added to policies.

## References

- Postgres Row-Level Security:
  [postgresql.org/docs/current/ddl-rowsecurity.html](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).
- `CREATE POLICY` syntax:
  [postgresql.org/docs/current/sql-createpolicy.html](https://www.postgresql.org/docs/current/sql-createpolicy.html).
- Supabase RLS guide:
  [supabase.com/docs/guides/database/postgres/row-level-security](https://supabase.com/docs/guides/database/postgres/row-level-security).
- [references/create-policy-syntax.md](references/create-policy-syntax.md) -
  full CREATE POLICY grammar and clause semantics.
- [references/tenant-context-patterns.md](references/tenant-context-patterns.md) -
  four tenant context source patterns.
- [references/policy-and-bypass-patterns.md](references/policy-and-bypass-patterns.md) -
  tenant policy shapes and RLS bypass rules.
- [references/other-engines.md](references/other-engines.md) -
  row/tenant isolation on MySQL / MariaDB, CockroachDB, Vitess, and SQL Server
  (per-engine detail in mysql-mariadb.md, cockroachdb.md, vitess.md,
  sqlserver.md).
- Tenant isolation context: the isolation-models reference in
  `cross-tenant-data-leak-tests`.
- Consumed by: `cross-tenant-data-leak-tests` (planning section + runtime gate).
