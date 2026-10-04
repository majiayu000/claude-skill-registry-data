---
name: deployment-plan
description: Plan application deployments across hosting environments and release targets. Use when Codex is asked to deploy an app, design a deployment runbook, choose deployment steps, define rollout order, or prepare a deployment plan without directly changing production.
license: MIT
---

# Deployment Plan

## Core Workflow

1. Identify artifact, target environment, hosting model, dependencies, release
   owner, users affected, and approval requirements.
2. Document pre-deploy checks: build, tests, migrations, config, secrets,
   capacity, observability, and support readiness.
3. Define deployment steps, rollout order, smoke tests, monitoring, and
   communication points.
4. Include rollback or fallback triggers before deployment begins.
5. Separate dry-run, staging, canary, and production steps.
6. Record owners, timing, risks, and go/no-go criteria.

## Safety Rules

- Do not deploy, change production config, run migrations, or restart services
  without explicit approval.
- Do not claim a deployment is safe without validation evidence.
- Escalate deployments involving customer data, auth, billing, migrations,
  high traffic, regulated workloads, or broad availability.

## Deliverable Shape

For deployment plans, provide:

- Target artifact and environment
- Preconditions
- Deployment steps
- Smoke tests and monitoring
- Rollout and communication plan
- Rollback triggers
- Owners and approvals
- Go/no-go criteria

## References

- Read `references/deployment-plan-checklist.md` when preparing deployment
  plans or runbooks.
