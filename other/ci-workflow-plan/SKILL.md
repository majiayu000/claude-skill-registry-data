---
name: ci-workflow-plan
description: Design CI workflows and quality gates for builds, tests, linting, security checks, packaging, and release automation. Use when Codex is asked to plan or review CI/CD workflows across GitHub Actions, GitLab CI, Azure Pipelines, CircleCI, or other systems.
license: MIT
---

# CI Workflow Plan

## Core Workflow

1. Identify repository type, languages, build artifacts, test layers, release
   needs, and target CI host.
2. Define triggers, jobs, dependencies, caching, artifacts, environment
   variables, secrets, and permissions.
3. Add quality gates: lint, typecheck, unit, integration, E2E, security,
   package, and publish checks as appropriate.
4. Keep secrets scoped and write permissions minimal.
5. Define failure reporting, retry policy, required checks, and branch
   protection expectations.
6. Include migration notes when moving between CI hosts.

## Safety Rules

- Do not add broad write tokens, unreviewed secrets, or deploy-on-every-branch
  workflows without explicit approval.
- Do not claim CI commands pass without output.
- Verify host-specific syntax from current docs when implementing a real
  workflow file.

## Deliverable Shape

For CI workflow plans, provide:

- CI host and repository assumptions
- Trigger and job plan
- Quality gates
- Cache and artifact plan
- Secrets and permission model
- Required checks
- Failure and retry behavior
- Validation steps

## References

- Read `references/ci-workflow-plan-checklist.md` when planning or reviewing CI
  workflows.
