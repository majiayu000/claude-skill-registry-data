---
name: production-readiness
description: "Audit a .NET release for functional evidence, security, reliability, migrations, rollbacks, alerts and operational ownership."
---

# Release readiness gate
- Evaluate `templates/RELEASE_CHECKLIST.md` for all impacted services, UI clients and MAUI app store targets.
- Confirm acceptance/test evidence, code review, dependency scan, API and schema compatibility, security, idempotency, performance target.
- Confirm SLO, telemetry, alert ownership, runbooks, backups, deployment window, feature flags, rollout/rollback and smoke plan.
- Mark each item **verified / blocked / unverified / not applicable** with link or command output.
- Do not mark GREEN without evidence. Escalate data loss, privileged access or rollback blockers.
