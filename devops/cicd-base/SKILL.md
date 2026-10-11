---
name: cicd-base
description: Shared CI/CD — stages, quality gates, secret management, rollback.
---

## Standard Pipeline Stages

Stages run in this order. Each stage must pass before the next begins.

| # | Stage | Purpose | Fails on |
|---|-------|---------|----------|
| 1 | `lint` | Code style and static analysis | Any lint error |
| 2 | `test` | Unit + integration tests with coverage report | Test failure or coverage below threshold |
| 3 | `security-scan` | SAST + dependency vulnerability check (OWASP) | HIGH or CRITICAL findings |
| 4 | `build` | Compile / bundle / containerize | Build error |
| 5 | `publish` | Push artifact/image to registry | Registry error — runs only on `main`/release branches |
| 6 | `deploy-staging` | Deploy to staging environment | Deploy failure — auto, after publish |
| 7 | `smoke-test` | Automated smoke tests against staging | Any smoke test failure |
| 8 | `deploy-prod` | Deploy to production | Manual gate, or auto on semver tag |

> Platform-specific skills (`cicd-github`, `cicd-gitlab`, `cicd-bitbucket`, `cicd-jenkins`) map these stages to their native primitives. This file defines the intent — the platform skill defines the syntax.

---

## Quality Gate Pattern

- All stages 1–4 must pass before any deploy stage (`publish`, `deploy-staging`, `deploy-prod`) runs
- **Coverage threshold**: default ≥ 80% line coverage; blocks on failure
- **Security threshold**: `HIGH` or `CRITICAL` severity findings block the pipeline; `MEDIUM`/`LOW` produce warnings only
- Never deploy from a branch that has failing checks

---

## Secret Management

- Never hardcode secrets in pipeline config files — treat the pipeline config as public
- Use the platform's native secret store:
  - GitHub Actions → Repository/Organization Secrets
  - GitLab CI → CI/CD Variables (masked + protected)
  - Bitbucket Pipelines → Repository/Deployment Variables
  - Jenkins → Credentials Store (with the Credentials Binding plugin)
- Rotate secrets on a defined schedule (quarterly minimum)
- Revoke secrets immediately on team member offboarding
- Reference secrets by name only in config; never echo or log their values

---

## Artifact Strategy

| Rule | Detail |
|------|--------|
| **Tagging** | Tag images with git SHA for every build; add semver tag when on a release branch |
| **Retention** | Keep last 10 builds; prune older artifacts automatically |
| **Immutability** | Never redeploy a mutable `latest` tag to production — always use a pinned SHA or semver |
| **Registry** | Push to a private registry; do not rely on Docker Hub for production images |

---

## Rollback

- Every `deploy-staging` and `deploy-prod` stage must have a documented rollback step
- Prefer **blue/green** or **canary** over in-place deploys for zero-downtime rollback capability
- Rollback triggers:
  - Smoke tests fail after staging deploy → auto-rollback to previous artifact
  - Manual trigger by on-call engineer for production
- Store the last successful artifact reference so rollback does not require a rebuild
