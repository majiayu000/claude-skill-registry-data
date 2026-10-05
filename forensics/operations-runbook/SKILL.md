---
name: operations-runbook
description: "Create or improve an operational runbook for recurring operations, incidents, maintenance, onboarding, or controlled recovery. Use for runbook, operational procedure, escalation guide, recovery steps, or on-call documentation. Turkish triggers: runbook hazırla, işletim adımları, olay müdahalesi ve geri alma, nöbet rehberi."
---

# Operations Runbook

Write a bounded procedure that a qualified operator can follow under pressure.

1. Define purpose, scope, prerequisites, permissions, owner, and stop conditions.
2. Use numbered steps with expected result and evidence after meaningful actions.
3. Include diagnostics before remediation, escalation triggers, rollback/recovery, and contact/ownership placeholders.
4. Label destructive, external, privileged, and irreversible actions explicitly.
5. Add a drill/review date and a lightweight change log.

Never hide commands that can delete data, change production, expose secrets, or bypass approvals. A runbook does not authorize its own execution.
