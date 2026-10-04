---
name: fleet-phase-infrastructure-maturity
description: How DevOps assesses whether infrastructure meets delivery phase requirements — the gap analysis between current infra and what the phase demands. Maps to devops_phase_infrastructure group call.
---

# Phase Infrastructure Maturity — DevOps Gap Assessment

Each delivery phase demands different infrastructure. A POC on Docker Compose is fine. Production without monitoring is negligent. Your job is to assess the gap between current infrastructure and what the phase requires, then plan the work to close it.

## The Phase-Infrastructure Matrix

| Requirement | POC | MVP | Staging | Production |
|------------|-----|-----|---------|------------|
| Deployment | docker-compose, manual | Automated CI build | Full CI/CD pipeline | Zero-downtime deploy |
| Config | .env file | Env vars | Managed secrets | Secrets manager + rotation |
| Monitoring | Console logs | Health endpoint + file logs | Structured logging + basic alerts | Full suite + dashboards + on-call |
| Testing | Manual | CI runs unit tests | CI + integration tests | CI + integration + performance |
| Security | Basic scan | Auth + validation | Dep audit + pen-test mindset | Certified + compliance |
| Rollback | docker-compose down/up | Rebuild from tag | Automated on health fail | Blue-green / canary |
| Data | SQLite / local | Persistent volume | Backup + restore tested | Automated backup + DR plan |

## The Assessment Process

### Step 1: Identify Current Phase

Read the task's `delivery_phase` field. Call `devops_phase_infrastructure(task_id)` for the structured assessment context.

### Step 2: Inventory Current Infrastructure

For the fleet's own infrastructure:
```
Agent: container-inspector — check Docker health, configs
Agent: code-explorer — check CI/CD pipeline files, scripts
```

For project-specific:
- Check Dockerfile exists and follows best practices
- Check docker-compose.yaml for service definitions
- Check .github/workflows/ for CI pipeline
- Check scripts/ for deployment automation
- Check monitoring configuration

### Step 3: Gap Analysis

Compare current inventory against phase requirements:

```
## Phase Infrastructure Gap Analysis

Current phase: MVP
Target phase: staging (requested advancement)

### What's in place:
✓ Docker Compose with service definitions
✓ Automated CI (lint + test + build)
✓ Health endpoint on MC backend
✓ .env for configuration
✓ Basic unit tests in CI

### What's missing for staging:
✗ Full CI/CD pipeline (deploy step missing)
✗ Staging environment (no staging server)
✗ Structured logging (using print statements)
✗ Basic alerting (no alert rules configured)
✗ Managed secrets (still using .env, not secrets manager)
✗ Integration tests in CI
✗ Backup + restore procedures
✗ Dependency audit in CI

### Gap severity:
- BLOCKING: no staging environment, no CI deploy step
- IMPORTANT: no structured logging, no alerting
- RECOMMENDED: secrets manager, integration tests

### Work required:
1. Create staging environment (3 SP, devops task)
2. Add deploy step to CI pipeline (2 SP, devops task)
3. Implement structured logging (2 SP, devops task)
4. Configure basic alerting (2 SP, devops task)
Total: ~9 SP before phase advancement is safe
```

### Step 4: Contribute or Create Tasks

If this is a contribution to another agent's task:
```
fleet_contribute(task_id, "deployment_manifest", gap_analysis)
```

If standalone work:
```
fleet_task_create(title="Staging infrastructure: CI deploy step", agent_name="devops", ...)
fleet_task_create(title="Staging infrastructure: structured logging", agent_name="devops", ...)
```

## Phase Gate Connection

When PM calls `fleet_phase_advance(from_phase="mvp", to_phase="staging")`:
1. The tool checks phase standards from `config/phases.yaml`
2. Your gap analysis informs whether the infrastructure is ready
3. If gaps exist → phase advance is blocked with specific gaps listed
4. PO sees the gaps in the gate request and decides: advance anyway or fix first

Your assessment feeds the PO's decision. You don't block — you inform.

## The IaC Principle for Phase Maturity

Every infrastructure capability must be SCRIPTED:
- `scripts/setup.sh` produces the full environment
- Each phase's requirements have corresponding scripts
- No "configure the server manually" instructions
- If it can't be reproduced from scripts, it's not ready for the phase

Phase maturity isn't just "does the capability exist?" — it's "can it be reproduced from zero?"
