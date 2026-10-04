---
name: fleet-devops-iac
description: How DevOps works — IaC principles, everything scriptable, phase-appropriate infrastructure, deployment manifests
user-invocable: false
---

# DevOps IaC Workflow

## The Principle

**Everything scriptable. Everything reproducible. Everything idempotent.**
No manual steps after checkout. A fresh machine runs setup.sh and gets a
running fleet. Zero drift between what's scripted and what's deployed.

This is Fleet Principle #4 — IaC only.

## Infrastructure Tiers by Delivery Phase

Don't overengineer POC. Don't underengineer production.

| Phase | Infrastructure Level |
|-------|---------------------|
| poc | Docker compose. Manual steps documented in README. Local only. |
| mvp | Automated CI (lint, test, build). Docker images tagged. Env vars for config. Basic health checks. |
| staging | Full CI/CD pipeline. Staging mirrors production. Health checks. Basic monitoring. Secrets managed. Blue-green or rolling deploy. |
| production | Production pipeline. Blue-green/canary. Full monitoring + alerting. Auto-scaling. Runbook. Rollback procedure tested. |

## Script Patterns

### Every script must:
1. **set -euo pipefail** — fail hard on errors
2. **Be idempotent** — running twice produces the same result
3. **Check dependencies** — install or error if missing
4. **Use color output** — GREEN for success, YELLOW for skip, RED for error
5. **Accept arguments** — `./script.sh [specific-target]` or all by default
6. **Source .env** — `source "$FLEET_DIR/.env" 2>/dev/null || true`

### Fleet script structure:
```bash
#!/usr/bin/env bash
set -euo pipefail

FLEET_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$FLEET_DIR/.env" 2>/dev/null || true

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ... idempotent operations ...
```

### Resolve vs hardcode:
- **Never** hardcode paths — use `$FLEET_DIR`, `$VENV`
- **Never** hardcode agent names — read from config YAML
- **Never** hardcode URLs — read from .env
- **Always** use `{{placeholders}}` in templates, resolve at deploy time

## Fleet Infrastructure Map

| Service | What | Script | Config |
|---------|------|--------|--------|
| MC Backend | Docker, API on :8000 | setup-mc.sh | docker-compose |
| MC Frontend | Web UI on :3000 | setup-mc.sh | docker-compose |
| Gateway | Agent sessions on :18789 | start-fleet.sh | gateway config |
| IRC | miniircd on :6667 | setup-irc.sh | 10 channels |
| The Lounge | Web IRC on :9000 | setup-lounge.sh | fleet/fleet |
| ntfy | Notifications on :8080 | (external) | 3 topics |
| Orchestrator | 30s cycle daemon | daemon.py | fleet.yaml |
| Sync daemon | 60s interval | daemon.py | fleet.yaml |
| Monitor daemon | 300s interval | daemon.py | fleet.yaml |
| Auth daemon | 120s interval | daemon.py | fleet.yaml |

## Contribution: deployment_manifest

When another agent's task needs infrastructure input:

1. Call `devops_deployment_contribution(task_id)` — gathers phase context
2. Produce a manifest covering:
   - **Environment:** services, ports, resources
   - **Configuration:** env vars, secrets, feature flags
   - **Deploy strategy:** rolling/blue-green/canary
   - **Monitoring:** what to monitor, alert thresholds
   - **Rollback:** how to roll back safely, tested procedure
3. Deliver: `fleet_contribute(task_id, "deployment_manifest", manifest)`

## Group Calls

| Call | When |
|------|------|
| `devops_infrastructure_health()` | Heartbeat — check MC, gateway, agents |
| `devops_deployment_contribution(task_id)` | Contribution task — produce manifest |
| `devops_cicd_review(task_id)` | Review — check CI/CD changes |
| `devops_phase_infrastructure(task_id)` | Assessment — gap between current and phase requirements |

## Vendor Patches

Fleet patches are in `patches/` and applied by `scripts/apply-patches.sh`.
Patches survive `git clone` of the vendor repo. When the vendor updates,
check if patches are still needed.

Current patches:
- 0001: skills marketplace category/risk upsert fix
- 0002: TOOLS.md parser handles markdown format
- 0003: last_seen_at set on provision complete
