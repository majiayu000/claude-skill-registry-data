---
name: supabase-rls-policy-audit
description: Review Supabase/Postgres row-level security policies for tenant isolation, role boundaries, query coverage, and safe privileged access.
---

# Supabase Rls Policy Audit

## Goal

Verify that database access rules prevent cross-user or cross-tenant reads and writes while preserving intended application flows.

## Inputs to inspect

Schema, RLS policies, grants, JWT claims, auth model, service-role usage, and representative queries from application code.

## Workflow

1. Inventory tables, views, functions, grants, enabled RLS status, and all policies. Identify tables that store user-owned or tenant-scoped data.
2. Define the identity and tenancy invariant for each operation: which authenticated role may select, insert, update, or delete which rows and under what ownership conditions.
3. Inspect policy expressions for missing tenant checks, unsafe `USING` versus `WITH CHECK` asymmetry, nullable ownership, broad `TO public` access, and assumptions about JWT claim presence.
4. Test with distinct users and tenants, anonymous sessions, stale/missing claims, and privileged service credentials. Attempt cross-tenant reads and writes using the real application query paths.
5. Review views, security-definer functions, background jobs, and service-role bypasses separately; verify that server-only credentials cannot leak to browser builds or logs.

## Validation checklist

- [ ] RLS is enabled on every table that requires user or tenant isolation.
- [ ] Policies are tested as the actual roles used by the app, not only by database owner/admin.
- [ ] Insert and update policies prevent moving a row into a different tenant or owner scope.
- [ ] Service-role bypass is confined to trusted server code and documented administrative paths.
- [ ] Negative tests demonstrate that a user cannot read or mutate another tenant's records.

## Required output

Produce a table-by-table access matrix, confirmed vulnerabilities, policy diffs, user/tenant test cases, and remaining exceptions requiring explicit approval.

## Boundaries and failure handling

Do not infer security from a policy's name; do not expose service-role keys or treat an administrator-session test as proof of RLS safety.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
