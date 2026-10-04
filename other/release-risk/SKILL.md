---
name: release-risk
description: Assess engineering release risk and readiness. Use when Codex is asked for a go/no-go recommendation, rollout risk, release checklist, deployment readiness, rollback plan, monitoring plan, migration risk, or production change review.
license: MIT
---

# Release Risk

## Core Workflow

1. Define release scope, affected users, changed systems, dependencies,
   deployment path, and timing constraints.
2. Identify risk areas: data, auth, billing, migrations, integrations,
   performance, compatibility, flags, observability, support, and rollback.
3. Check readiness evidence: tests, reviews, docs, monitoring, alerts, support
   notes, owners, and approvals.
4. Define rollout plan, hold points, rollback or mitigation plan, and decision
   owner.
5. State go/no-go recommendation with confidence and residual risk.
6. Keep customer, support, and stakeholder communication separate from internal
   risk notes.

## Safety Rules

- Do not deploy, merge, release, or change production systems without explicit
  approval.
- Do not mark a release ready when tests, rollback, monitoring, or ownership are
  unknown.
- Escalate when the release affects money, access, customer data, security,
  compliance, migrations, or broad availability.

## Deliverable Shape

For release risk work, provide:

- Scope and affected users
- Risk assessment
- Required gates and evidence
- Rollout plan
- Rollback or mitigation plan
- Monitoring and support needs
- Go/no-go recommendation
- Residual risk and owner approvals

## References

- Read `references/release-risk-checklist.md` when assessing deployment,
  rollout, release candidate, or production change risk.
