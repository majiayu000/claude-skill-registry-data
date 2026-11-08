---
name: security-gate
description: Run authorization, privacy and prompt-injection test review for PromiseTwin Forge changes. Use before deployment or when touching tenant data, permissions, AI or approvals.
---
# security-gate

Follow docs/04-SECURITY.md. Inspect current diff for tenant data separation, authZ on each resolver, asApp vs asUser, trust in request fields, untrusted prompt data, secrets, egress, overbroad OAuth scopes and auditable mutations. Execute targeted tests. Run official forge-security-review if available. Fail release if critical/high risks remain.

Do not auto-deploy, publish, create public links or change external permissions. Return concise evidence and next action.
