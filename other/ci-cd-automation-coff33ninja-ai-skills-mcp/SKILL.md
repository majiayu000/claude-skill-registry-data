---
name: ci-cd-automation
description: Pipeline setup/maintenance standards, CI best practices, Shift Left principle. Broader than toolchain-fallback (toolchain detection); this covers the full CI/CD automation pipeline. Write pipelines before merging, test in CI, fail fast.
---

# CI/CD Automation

## Problem it solves

Without structured CI/CD practices, pipelines become unreliable and slow:
- Tests pass locally but fail in CI (environment drift)
- Pipeline configs drift from project requirements
- Long feedback cycles — developers wait too long for CI results
- Flaky tests ignored or disabled instead of fixed
- Security checks added as afterthoughts
- No automated deployment process — manual steps that cause errors

## Protocol

### 1. Shift Left — test early, test often

Run quality checks as early as possible in the pipeline:
- **Pre-commit**: Lint, format, type-check (fast, <1 min)
- **Pre-push**: Unit tests, security scan (medium, <5 min)
- **CI**: Integration tests, e2e tests, performance benchmarks (longer)
- **CD**: Deploy to staging, smoke tests, deploy to production

A bug found at pre-commit costs seconds. Same bug found in production costs hours.

### 2. Pipeline structure

Every project should have a CI pipeline that runs on every push:

```yaml
# Minimum CI pipeline
jobs:
  lint:        # linting and formatting
  typecheck:   # type checking
  test:        # unit + integration tests
  build:       # verify it builds
```

Optional but recommended:
```yaml
  security:    # dependency audit, SAST
  benchmark:   # performance regression check
  e2e:         # end-to-end tests
```

### 3. Pipeline reliability

- **Deterministic**: Same code → same result every time
- **Idempotent**: Running twice produces the same result
- **Fast**: Keep under 10 minutes. If longer, split into parallel jobs.
- **Isolated**: Each job runs in a clean environment
- **Reproducible**: Pin dependency versions, use lockfiles, use CI cache

### 4. Fail fast

- If lint fails, don't run tests
- If unit tests fail, don't run e2e
- If staging smoke tests fail, don't deploy to production
- Each step should gate the next

### 5. CI/CD is code

- Pipeline configs belong in version control
- Review pipeline changes like code changes
- Test pipeline changes in a branch before merging to main
- Document pipeline structure and what each job does

### 6. Secret management

- Never hardcode secrets in pipeline configs
- Use CI/CD platform secret store (GitHub Secrets, GitLab CI variables, etc.)
- Rotate secrets regularly
- Audit who has access to secrets

## Detection triggers

Activate when:
- Setting up a new project
- Adding or modifying CI/CD configuration
- Pipeline is failing or flaky
- User says "setup CI", "add pipeline", "configure deployment"
- User reports tests passing locally but failing in CI

## When NOT to use

- Prototyping or throwaway projects
- User explicitly says "no CI needed"

## Cross-references

- **toolchain-fallback** — Use together to detect available toolchains before writing pipeline configs. toolchain-fallback detects tools; this skill wires them into pipelines.

- **release-changelog** — CI/CD pipelines should trigger release workflows (version bump, tag, publish). release-changelog defines the release process; CI/CD automates it.

- **git-workflow-conventional-commits** — CI should enforce conventional commit format and branch naming conventions.

- **test-driven-development** — CI runs the tests. TDD ensures tests exist for CI to run.

- **code-review** — CI checks should pass before review. Review should check CI config changes.

- **project-scripts** — Use to discover existing build/test/deploy scripts before writing the pipeline.

- **security-best-practices** — Integrate security scanning into the pipeline (dependency audit, SAST, secrets scan).

- **anti-premature-termination** — CI passing is a completion criterion. Do not declare done until pipeline is green.
