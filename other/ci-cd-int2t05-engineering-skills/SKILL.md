---
name: ci-cd
description: Build a reproducible pipeline for the actual repository and release platform. Triggers on "CI pipeline", "流水线".
---

# CI/CD and Automation

## When to use

- Build a reproducible pipeline for the actual repository and release platform.

**Not for:** shipping for release execution; linting for static fixes.

## Steps

1. Identify actual commands, environments, credential boundaries and release target.

2. Configure applicable checks and builds; verify triggers and generated-file drift paths against the real tree.

3. Specify artifact provenance, environment separation, deployment authority and platform recovery.

4. Validate configuration and equivalent local checks; use authorized remote runs and explicitly report unexecuted stages.

## Verify

- Commands and path filters match the repository; unrun remote pipelines are not reported as passed.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/ci-templates.md](references/ci-templates.md) — Dependabot config, caching/parallelism split jobs, preview deployment, rollback workflow_dispatch
