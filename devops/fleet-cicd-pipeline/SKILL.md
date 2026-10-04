---
name: fleet-cicd-pipeline
description: How DevOps designs and maintains CI/CD pipelines — build, test, deploy stages with fleet-appropriate automation, phase-gated deployments, and rollback strategy
user-invocable: false
---

# CI/CD Pipeline Design

## Fleet Context

The fleet operates across 4 projects (Fleet, AICP, DSPD, NNRT) with
different deployment targets and maturity levels. CI/CD must be:
- Project-aware (different pipelines per project)
- Phase-aware (POC deploys differently than production)
- Fleet-integrated (results feed back to Mission Control)

## Pipeline Stages

### 1. Build
```
Source → Lint → Type Check → Build Artifacts
```

| Check | Tool | Fail Action |
|-------|------|-------------|
| Lint | ruff check | Block merge |
| Format | ruff format --check | Block merge |
| Type check | pyright/mypy | Warn (POC), Block (MVP+) |
| Dependencies | pip audit | Warn (POC/MVP), Block (staging+) |

### 2. Test
```
Unit Tests → Integration Tests → Coverage Report
```

| Test Level | When | Timeout |
|-----------|------|---------|
| Unit | Every push | 5 min |
| Integration | Every PR | 15 min |
| End-to-end | Pre-deploy | 30 min |

Phase-dependent thresholds:
- POC: unit tests pass
- MVP: unit + integration, coverage > 60%
- Staging: all levels, coverage > 80%
- Production: all levels, coverage > 90%, regression suite

### 3. Security
```
Dependency Scan → Secret Scan → Static Analysis
```

| Scan | Tool | Frequency |
|------|------|-----------|
| Dependencies | pip audit / npm audit | Every build |
| Secrets | secret-detector sub-agent / gitleaks | Every PR |
| Static analysis | semgrep | Every PR |

### 4. Deploy
```
Build Image → Push Registry → Deploy Target → Smoke Test → Verify
```

Phase-gated deployment:
- POC: manual deploy (devops runs script)
- MVP: semi-automated (PR merge triggers deploy to dev)
- Staging: automated deploy to staging, manual promote to production
- Production: blue/green or canary, automated rollback on failure

### 5. Post-Deploy
```
Smoke Test → Health Check → Monitoring Alert Setup
```

- Smoke test: critical path verification (3-5 checks)
- Health check: service responds, dependencies connected
- Monitoring: alerts configured for the new deployment

## Fleet-Specific Pipeline Elements

### Results Feed to Mission Control
CI results should be posted to board memory:
```
fleet_chat(channel="#builds", message="CI: {project} {branch} — {status}")
```

### PR Integration
When CI completes on a PR:
- Status check on GitHub PR
- Comment with test summary
- Coverage diff in PR comment

### Agent Notifications
When a build fails on an agent's branch:
```
fleet_alert(channel="#builds", severity="warning",
  message="Build failed: {agent}/{branch} — {failure_reason}")
```

## Rollback Strategy

### Automated Rollback Triggers
- Health check fails within 5 minutes of deploy
- Error rate exceeds baseline by 3x
- Critical dependency unreachable

### Rollback Procedure
1. Revert to previous deployment (keep failed artifacts for analysis)
2. Notify: `fleet_alert(channel="#alerts", message="Rollback: {service}")`
3. Create bug task: `fleet_task_create(type="bug", title="Deploy failure: {details}")`
4. Post-mortem after stabilization

### What NOT to Rollback
- Database migrations (forward-only — fix forward)
- Configuration changes (may need manual intervention)

## IaC Principles

Every pipeline element must be:
1. **Scripted** — no manual steps after `git clone`
2. **Reproducible** — same input produces same output
3. **Versioned** — pipeline config is in the repo
4. **Documented** — what it does, why, how to debug

Pipeline config files:
- `.github/workflows/` — GitHub Actions
- `Makefile` — local development commands
- `scripts/` — deployment scripts
- `docker-compose*.yml` — service definitions
