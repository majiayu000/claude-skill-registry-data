---
name: ci-cd-pipeline
description: "CI/CD pipeline architecture, matrix builds, automated security gates, deployment rollbacks, and pipeline caching."
---

# CI/CD Pipeline Architecture Protocol

Build fast, deterministic, and secure deployment pipelines.

---

## 1. Fast Feedback & Pipeline Stages

Structure CI workflows into ordered stages:
1. **Lint & Formatting**: Fast static syntax verification (< 1 min).
2. **Type Check & Unit Tests**: Parallelized test execution with dependency caching.
3. **Security Audit**: Dependency vulnerability scan and secret detection.
4. **Build & Package**: Containerization or artifact bundling.
5. **E2E Smoke Tests**: Verification on staging/preview deployment before production rollout.

---

## 2. Secrets & Branch Protection

1. Require mandatory pull request reviews and passing CI checks before merging to main.
2. Restrict production deployment credentials exclusively to protected branches or tagged releases.
3. Store secrets in designated platform vaults, never in pipeline definitions.
