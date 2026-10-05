---
name: infrastructure-devops
description: Design and maintain deployment, runtime, CI/CD, containers, workers, scheduling, and operational infrastructure using platform-agnostic principles.
metadata:
  internal: true
---

# infrastructure-devops

Use this skill for deployment, CI/CD, containers, scheduling, workers, runtime configuration, health checks, and operational automation.

## Principles

Prefer reproducible and observable deployment processes.

Separate configuration from application source where appropriate.

Automated workflows should fail clearly and avoid silently publishing broken artifacts.

Consider:

- build reproducibility
- health checks
- restart behavior
- rollout strategy
- rollback strategy
- resource limits
- secret handling
- logs
- monitoring

Background and scheduled workloads should define:

- ownership
- retries
- duplicate execution behavior
- concurrency
- failure handling

Do not assume local development behavior represents production behavior.

## Adaptation

Use project evidence to determine the actual language, framework, runtime, and existing conventions.

When stack-specific implementation guidance is needed, prefer project evidence, native framework or language mechanisms, and relevant user-installed specialist skills. Technology-specific guidance must not redefine or weaken the core engineering requirement.