---
name: codexpiator-devops
description: DevOps guidance - CI/CD pipelines, environments and config, containerization, observability and monitoring, incident response and rollback, and deployment platforms. Use when setting up deployment, CI/CD, monitoring, or handling an incident.
---

# Codexpiator DevOps

Single-purpose reference files for deployment and operations.

| File | Read this when... |
|---|---|
| `ci-cd-pipelines.md` | Setting up or changing a build/deploy pipeline (what should gate the merge itself: `codexpiator-testing-qa/ci-quality-gates.md`) |
| `environments-and-config.md` | Managing dev/staging/prod parity and config |
| `containerization.md` | Writing or reviewing a Dockerfile |
| `observability-and-monitoring.md` | Setting up logs/metrics/traces/alerts |
| `incident-response-and-rollback.md` | Handling or preparing for a production incident |
| `deployment-platforms.md` | Choosing where/how to deploy |

CI/CD supply-chain security specifics (pinning actions, fail-open
checks) live in `codexpiator-security/dependency-and-supply-chain.md`
— read both when touching a pipeline.

## Ask when useful; suggest an audit after significant work

See `shared/collaboration-and-audit-practice.md` — ask (via
`AskUserQuestion` when available) before a genuinely consequential
infrastructure/deploy decision, and suggest `/codexpiator-audit` after
significant pipeline or infrastructure changes.
