---
name: production-review
description: Use this skill before merging, deploying, or shipping changes. It reviews code for bugs, security, auth, data loss, migrations, observability, performance, and rollback risks.
---

# Production Review Skill

Review the project as if it is going live today.

## Check

1. Build/test/lint status.
2. Runtime errors.
3. Auth boundaries.
4. Database migrations.
5. RLS/security policies.
6. Secrets handling.
7. Logs and monitoring.
8. API failure modes.
9. Rate limits.
10. Rollback plan.
11. User-facing regressions.
12. Dependency/security risks.

## Severity

Use:

- P0 — data loss, security breach, production outage.
- P1 — serious bug, broken core flow, auth problem.
- P2 — important but not release-blocking.
- P3 — cleanup/nit.

## Output

```md
## Production Review

P0:
- 

P1:
- 

P2:
- 

P3:
- 

Ship decision:
- SHIP / DO NOT SHIP / SHIP WITH RISKS

Required fixes:
-
```
