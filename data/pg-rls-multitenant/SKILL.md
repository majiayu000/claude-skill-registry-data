---
name: pg-rls-multitenant
description: "Enforces Postgres row-level security for multi-tenant Ottili workloads: tenant-key-first design, FORCE RLS, expand/contract migrations, and automated leak tests that fail on policy gaps. Use when adding a tenant-isolated table or view, reviewing company_id/organization_id/namespace columns for missing RLS, or investigating 'user X saw user Y's data' incidents."
license: MIT-compat
compatibility: "PostgreSQL 15+ (verified 18); framework-agnostic"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# PG RLS Multitenant Skill — Quick Reference (body <500 lines; full procedure in references/pg-rls-procedure.md)

## When to use this skill (trigger)
Any of these fires it:
- Adding a new tenant-isolated table or view to an Ottili schema.
- A code review mentions `company_id`, `organization_id`, or `namespace` columns without RLS.
- A migration adds a column that becomes the tenant discriminator.
- An incident report says "user X saw user Y's data".
- Reviewing Supabase, Hasura, Prisma, or direct SQL for missing RLS.

## Disambiguation
- Fires: new tenant-isolated table/view, company_id/organization_id/namespace columns without RLS, a column becoming the tenant discriminator, 'user X saw user Y data', reviewing Supabase/Hasura/Prisma for missing RLS.
- Does NOT fire for: a single-user app with no tenants, or event delivery idempotency (use outbox-idempotency).

## When NOT to use this skill
- Single-tenant databases (no tenant discriminator needed).
- Read-only analytics replicas where RLS is enforced upstream.
- Tables that intentionally share rows across tenants (e.g., global config) — mark them `bypassrls` explicitly instead of omitting policies.
- A database that is only ever used by one tenant — the skill still applies (the discriminator is still required), but the policy is trivially `true`.
- A view that is only ever queried by an owner account — that is the exact bypass the skill forbids; `security_invoker = true` is the fix, not an exception.
- "We encrypt the column instead of using RLS" — encryption is not access control; the skill fires when encryption is proposed as a substitute for tenant isolation.

## Decision table — expand/contract migration
| Step | Action | Threshold / pitfall |
|------|--------|---------------------|
| 1. Add column | `ALTER TABLE t ADD COLUMN company_id uuid` | Start `NULL` if the table is non-empty; adding NOT NULL on a non-empty table without a default blocks |
| 2. Backfill | `UPDATE t SET company_id = <owner> WHERE company_id IS NULL` | Must run in batches on large tables; record the batch size |
| 3. Constrain | `ALTER TABLE t ALTER COLUMN company_id SET NOT NULL` + `CHECK` | CHECK must match the app tenant format (UUID v4) |
| 4. Policy | `CREATE POLICY ... USING (company_id = current_setting(...))` | Policy must exist before the app depends on isolation |
| 5. Leak test | Run `scripts/check_rls_migration.py` + Docker harness | All 7 cases must PASS; any FAIL blocks merge |
| 6. Contract | Separate `V<n>__<desc>__contract_*.sql` migration dropping the old column | N = 4 weeks minimum after expand lands in production; record the date in the migration comment; rollback SQL in a `-- ROLLBACK` block |

## Decision table — leak-test outcome
| Test case | Expected | If it fails |
|-----------|----------|-------------|
| Same-tenant read | tenant A sees only its rows | Policy expression is wrong — fix the `USING` clause |
| Cross-tenant read | tenant A sees ZERO of tenant B's rows | RLS not enabled, or view bypasses it — add FORCE / `security_invoker = true` |
| INSERT wrong tenant | rejected by `WITH CHECK` | `WITH CHECK` missing or wrong — add it |
| UPDATE company_id | rejected when a RESTRICTIVE policy is present | RESTRICTIVE policy missing — add it |
| View bypass | `security_invoker=false` view exposes cross-tenant rows → FAIL | Set `security_invoker = true` on the view, or exclude it from RLS scope |
| Owner bypass | table without FORCE exposes all rows → FAIL | Add `FORCE ROW LEVEL SECURITY` |
| service_role bypass | `service_role` sees everything by design | Never use `service_role` client-side; restrict it in the auth layer |

## Worked examples
Good (permissive policy + FORCE + scoped grant):
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
CREATE POLICY orders_tenant_select ON orders
  FOR SELECT
  TO web_app
  USING (company_id = current_setting('app.company_id', true));
GRANT SELECT ON orders TO web_app;
```
Bad (owner bypass — table created by migration role, no FORCE):
```sql
CREATE TABLE notes (id uuid, company_id uuid, body text);
-- migration role can read every tenant's notes until FORCE is added
```
Bad (view bypass):
```sql
CREATE VIEW active_orders AS SELECT * FROM orders;
-- runs as view owner; RLS on orders is skipped
```
Bad (expand without backfill — old rows silently excluded):
```sql
ALTER TABLE orders ADD COLUMN company_id uuid NOT NULL;
-- fails: cannot add NOT NULL without a default; and if it succeeds, old rows are NULL
-- and match no policy — a silent data-loss trap, not a leak
```

## Pitfalls from research (real incidents)
- Owner bypasses RLS unless FORCE is set — a table created by a migration role silently exposes
  rows to that role's sessions.
- Views are security-definer by default and bypass RLS unless `security_invoker = true`.
- Missing GRANT before policy → error 42501 before any policy runs.
- `service_role` key bypasses all RLS — never use it client-side.
- Sub-select race condition between policy evaluation and INSERT can leak rows under concurrent load.

## Near-miss triggers (act before the incident)
- A table is created by a migration role and has no FORCE RLS → that role's sessions see all tenants' rows.
- A view is created without `security_invoker = true` → it runs as the view owner and bypasses RLS.
- `GRANT ALL` appears on a protected table → silently overrides the policy grant.
- `service_role` is used in client-side code → bypasses every RLS policy by design.
- A policy uses a sub-select on the same table → the check-then-insert race leaks rows under concurrent load.
- A migration adds the tenant column AFTER data exists, with no backfill → old rows have NULL company_id and match no policy (silent exclusion, not a leak, but a data-loss trap).
- "The leak test passed once, so the policy is fine" — re-run it after every policy change; RLS is not monotonic.

## Verification checklist (all must pass before merge)
- [ ] Every row table has at least one policy matching its tenant column
- [ ] FORCE ROW LEVEL SECURITY is set on all non-dev tables
- [ ] No GRANT ALL on protected tables
- [ ] Leak test harness runs green against Docker Postgres
- [ ] Migration includes rollback SQL
- [ ] Views use security_invoker = true or are excluded from RLS scope


## Verification
- Run the offline gate: `python3 scripts/check_rls_migration.py <migration.sql>` — must exit 0.
- Run the Docker harness: `scripts/pg-rls-leak-test.sh <migration.sql> [table]` — must print PASS.
- Run the standard validator: `python3 scripts/validate_skills.py` — must report OK.
- Full procedure, version table, worked examples, and pitfalls: `references/pg-rls-procedure.md`.
- Eval prompts with expected behaviour and failure signs: `references/EVALS.md`.
- Primary sources with URLs and retrieval dates: `references/SOURCES.md`.

## Related skills
- [acceptance-harness](../acceptance-harness/SKILL.md) — a tenant-leak scenario is an acceptance scenario with PASS evidence.
- [honest-status](../honest-status/SKILL.md) — the RLS migration is a status item; mark it VERIFIED only after the leak test ran green.
- [long-test-discipline](../long-test-discipline/SKILL.md) — the leak test is a long test that runs in the foreground.
- [module-contract-first](../module-contract-first/SKILL.md) — an RLS policy is a contract: enumerate it, version it, block merge on drift.
- [problem-json-contracts](../problem-json-contracts/SKILL.md) — a leak is reported as a problem detail, not a silent row.
- [outbox-idempotency](../outbox-idempotency/SKILL.md) — the outbox row is tenant-scoped and must survive RLS; the leak test and the outbox leak test share the same tenant-isolation contract.
- [shared-tree-git](../shared-tree-git/SKILL.md) — the migration and the leak-test evidence are committed with a task-id prefix.
