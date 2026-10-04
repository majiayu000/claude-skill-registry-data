---
name: fleet-deployment-strategy
description: How DevOps selects deployment strategy per delivery phase — rolling, blue-green, canary. Maps to devops_deployment_contribution and devops_phase_infrastructure.
---

# Deployment Strategy — Phase-Appropriate Infrastructure

Every delivery phase has different infrastructure needs. A POC doesn't need blue-green deployment. Production doesn't tolerate "docker compose up." Your job is to match the deployment strategy to the phase — and to contribute this knowledge to engineer tasks via `devops_deployment_contribution`.

## The Phase-Infrastructure Matrix

| Phase | Deploy Strategy | CI/CD | Monitoring | Secrets | Rollback |
|-------|---------------|-------|------------|---------|----------|
| poc | Manual docker-compose. Steps documented in README. | None (manual build) | Console logs only | .env file (gitignored) | docker compose down + up |
| mvp | Automated CI (lint + test + build). Docker images tagged per commit. | GitHub Actions: lint → test → build | Basic health endpoint. Console + file logs. | Environment variables | Rebuild from last passing tag |
| staging | Full CI/CD pipeline. Staging env mirrors production structure. | GA: lint → test → build → deploy-staging | Health checks + basic alerting. Structured logging. | Managed secrets (not env vars) | Automated rollback on health check fail |
| production | Zero-downtime deployment. Canary or blue-green. | GA: lint → test → build → staging → canary → production | Full monitoring suite. Dashboards. PagerDuty-style alerts. | Secrets manager. Rotation policy. | Automated canary rollback. DB migration rollback plan. |

## Deployment Strategy Selection

### Rolling Update
**What:** Update instances one at a time. Old serves while new deploys.
**When:** Stateless services. Phase: staging+.
**Pros:** Simple, resource efficient.
**Cons:** Mixed versions during deploy. Rollback = full redeploy.

### Blue-Green
**What:** Two identical environments. Green (live), Blue (new). Switch traffic atomically.
**When:** Stateful services or when mixed versions are dangerous. Phase: production.
**Pros:** Instant rollback (switch back to green). No mixed versions.
**Cons:** Double infrastructure cost during deployment.

### Canary
**What:** Route small % of traffic to new version. Monitor. Gradually increase.
**When:** High-traffic services where gradual confidence is needed. Phase: production.
**Pros:** Minimal blast radius. Real production traffic testing.
**Cons:** Complex routing. Need metrics to judge success. Longer deploy.

### For the Fleet
The fleet itself (MC, gateway, agents) uses a simpler model:
- **Gateway:** Stop → update → start (agents reconnect automatically)
- **MC:** Docker rebuild → restart (tasks persist in SQLite/Postgres)
- **Agents:** No deployment — they read files from `agents/` directory. Push new files = new behavior on next heartbeat.

## The Deployment Manifest (Contribution)

When you call `devops_deployment_contribution(task_id)`, you produce a `deployment_manifest` for the target task. The manifest covers:

1. **Environment** — what services, ports, resources does this feature need?
2. **Configuration** — what env vars, secrets, feature flags?
3. **Deploy strategy** — which strategy fits this phase + this change?
4. **Monitoring** — what to watch, what alert thresholds?
5. **Rollback** — how to undo safely (especially DB migrations)?

The engineer receives this as a contribution and follows it — they don't decide deployment strategy, you do.

## Phase Infrastructure Assessment

When you call `devops_phase_infrastructure(task_id)`, you assess whether the current infrastructure meets the phase's requirements. The tool returns the phase + requirements + all phase definitions.

Your assessment should identify:
- **What's in place** — existing CI, monitoring, secrets management
- **What's missing** — gaps between current state and phase requirements
- **What to build** — specific tasks to close the gaps

If the assessment finds gaps, create tasks for yourself: `fleet_task_create(agent_name="devops", title="Add health check endpoint for staging", task_type="task")`.

## IaC Principle

Everything in deployment MUST be scripted. No manual steps after checkout. This means:
- CI/CD pipeline defined in `.github/workflows/` (not configured in GitHub UI)
- Docker config in `Dockerfile` + `docker-compose.yaml`
- Infrastructure in `scripts/` (the fleet's IaC pattern)
- Secrets in documented config (not hardcoded, not manual)

If you can't script it, it can't be reproduced. If it can't be reproduced, it's not infrastructure — it's a liability.
