---
name: authz-boundary-review
description: "Reviews authorization, tenant isolation, roles, ownership, row access, admin boundaries, sharing, and privilege escalation."
---

# Authz Boundary Review

Review access-control boundaries as behavior, not style.

## Workflow

1. Identify actors, roles, tenants, objects, and privileged actions.
2. Trace request/input to authorization decision and data access.
3. Check object ownership, tenant scoping, bulk operations, admin bypasses,
   background jobs, and indirect object references.
4. Validate with tests or concrete code evidence.
5. Report exploit path and minimal fix.

## Output

- affected boundary
- attacker capability
- missing or weak control
- exploit path
- files and lines
- regression test suggestion

## Rule

Do not accept UI-only hiding as authorization. The enforcing control must exist
on the server or trusted boundary.
