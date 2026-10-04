---
name: devops-and-operations
description: Operational guidance for CI/CD, deployments, runtime configuration, environment parity, and observability-aware system delivery.
compatibility: opencode
metadata:
  audience: devops
  purpose: operations-guidance
---
## Core approach

- Prefer simple, repeatable operational workflows.
- Treat pipeline and deployment changes as production-affecting work.
- Minimize environment drift and hidden runtime assumptions.
- Keep secret handling, rollout behavior, and observability in view.

## Practical guidance

- Review CI jobs, deployment automation, environment variables, secrets management, health checks, and monitoring hooks together.
- Call out brittle manual steps, missing rollback support, and poor environment parity.
