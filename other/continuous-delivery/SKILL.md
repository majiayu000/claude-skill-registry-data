---
name: continuous-delivery
description: CI/CD pipeline health check, branch strategy, and deploy readiness assessment
triggers: [ci/cd, pipeline, deploy, continuous delivery, continuous integration, release, branch strategy]
audience: engineer
---

# Continuous Delivery

## Context
Continuous Delivery is the practice of keeping software in a releasable state at all times. This skill helps you assess pipeline health, validate deploy readiness, improve branch strategies, and remove bottlenecks to fast, safe delivery.

Works in monoliths (single pipeline) and distributed systems (service-level pipelines with coordination).

Use this skill when:
- Setting up or reviewing a CI/CD pipeline
- Diagnosing a slow or flaky pipeline
- Preparing a release or checking deploy readiness
- Evaluating your team's branching strategy

## Instructions

### Deploy Readiness Checklist
Before deploying, verify:
- [ ] All tests pass (unit, integration, contract)
- [ ] No known failing checks in CI
- [ ] Feature flags in place for any incomplete or risky features
- [ ] Database migrations are backward-compatible (old app version can run against new schema)
- [ ] Rollback procedure is defined and tested
- [ ] Observability is in place: new code emits logs/metrics/traces
- [ ] No hardcoded secrets or environment-specific values in the diff
- [ ] Dependent services (APIs, queues, DBs) are compatible with this version

### Pipeline Health Assessment
Evaluate the pipeline against these benchmarks:
| Stage | Target | Warning | Critical |
|-------|--------|---------|----------|
| Unit tests | < 5 min | 5–15 min | > 15 min |
| Integration tests | < 15 min | 15–30 min | > 30 min |
| Full pipeline | < 30 min | 30–60 min | > 60 min |
| Deploy frequency | Daily+ | Weekly | Monthly or less |

If pipeline is slow:
1. Parallelize test stages
2. Identify and fix or quarantine flaky tests
3. Cache dependencies aggressively
4. Split large test suites by type (fast unit vs. slow integration)

### Branching Strategy Guidance
- **Trunk-based development** (recommended): Small, short-lived branches merged to main daily. Feature flags gate incomplete work. Enables true CD.
- **Gitflow** (acceptable for release-train teams): Use when regulatory or batch release constraints exist.
- **Long-lived feature branches**: Avoid. They accumulate merge debt and make CD impossible.

### Monolith-Specific Guidance
- Use a single pipeline with clearly separated stages
- Ensure the build produces one deployable artifact
- Gate on a single test suite that covers the whole system
- Use blue-green or canary deployments to reduce risk

### Distributed/Microservices-Specific Guidance
- Each service owns its pipeline
- Use contract tests (consumer-driven) to detect cross-service breakage early
- Deploy services independently — never require coordinated multi-service deploys
- Use a deployment manifest or GitOps approach for environment state tracking

## Principles
- Source: [Continuous Delivery — Martin Fowler](https://martinfowler.com/delivery.html)
- Source: [Trunk-Based Development — trunkbaseddevelopment.com](https://trunkbaseddevelopment.com)
- Key idea: *"The key test of Continuous Delivery is: can you deploy to production on demand? If the answer is 'it depends on whether the planets are aligned', you don't have CD."*

## Output Format
When applying this skill, the agent should:
- Run through the deploy readiness checklist and flag any gaps
- Identify the slowest pipeline stages if diagnosing speed issues
- Recommend specific changes to branching strategy if suboptimal
- Produce a prioritized list of improvements with estimated impact
