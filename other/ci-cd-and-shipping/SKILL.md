---
name: ci-cd-and-shipping
description: >
  End-to-end pipeline from CI configuration through production deployment.
  Covers pipeline stages, test automation, deployment strategies, pre-launch
  checklists, rollback planning, and post-deploy verification.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "setting up CI/CD"
  - context: "deploying to production"
  - context: "launching a feature"
  - command: "/ship"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - test-driven-development@^1.0.0
  - security-and-hardening@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 1
---

## Overview

CI/CD pipelines automate the path from commit to deployment. This skill covers the full pipeline: fast CI checks, deployment strategies, pre-launch verification, rollback planning, and post-deploy monitoring.

## When to Use

- When setting up or modifying a CI/CD pipeline
- Before deploying to production
- When releasing a new version
- During `/ship` phase

## Process

### 1. CI Pipeline Stages

```yaml
stages:
  - lint        # Code style + static analysis (< 1 min)
  - test        # Full test suite (< 5 min target)
  - build       # Compile/bundle (< 2 min)
  - security    # Dependency audit + SAST (< 2 min)
```

**Key principles:** Fast feedback (< 10 min total), fail fast (cheapest checks first), deterministic (no flaky tests), branch protection (main requires passing CI).

### 2. Security in CI

```yaml
security:
  - npm audit --audit-level=high
  - npx secretlint "**/*"
```

### 3. Deployment Strategies

| Strategy | Risk | Rollback | Use When |
|---|---|---|---|
| **Blue-green** | Low | Instant | Production services |
| **Canary** | Low | Fast | High-traffic services |
| **Rolling** | Medium | Moderate | Stateless services |
| **All-at-once** | High | Slow | Dev/staging only |

### 4. Pre-Launch Checklist

- [ ] All tests pass on the release branch
- [ ] Build succeeds with no warnings
- [ ] Security audit clean (no critical/high)
- [ ] Code review approved
- [ ] Staging environment tested
- [ ] Rollback plan documented
- [ ] Monitoring/alerting configured

### 5. Rollback Plan

Before deploying, document:
1. How to detect a failed deployment (metrics, alerts)
2. How to rollback (command, process, timeline)
3. Who to notify if rollback is needed

### 6. Post-Deploy Verification (within 15 min)

- [ ] Health check endpoint returns 200
- [ ] Core user flows work
- [ ] Error rates and response times normal
- [ ] Logs clean (no unexpected errors)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "CI is too slow, I'll push directly" | Fix the slow pipeline, don't bypass it. |
| "It worked on staging, it'll work in production" | Staging ≠ production. Different data, load, and config. Verify after deploy. |
| "We don't need a rollback plan" | Murphy's Law. 5 minutes of planning saves hours of panic. |

## Red Flags

- No CI pipeline for multi-contributor projects
- Pipeline takes > 15 minutes
- Main branch unprotected
- Deploying without rollback plan
- Deploying on Friday afternoon
- No post-deploy verification

## Verification

- [ ] CI pipeline runs lint, test, build, and security stages
- [ ] Pipeline completes in < 10 minutes
- [ ] Pre-launch checklist complete
- [ ] Rollback plan documented
- [ ] Post-deploy verification passed

## See Also

- `codehands:git-workflow-and-versioning` — Git conventions for CI
- `codehands:finishing-a-development-branch` — Branch completion flow
- `codehands:security-and-hardening` — Security scanning details
