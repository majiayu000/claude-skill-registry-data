---
name: release-readiness-harness
description: Define and validate what ready-to-ship means beyond tests passing. Use when a repo needs release checklists, smoke tests, rollback plans, changelog/versioning guidance, deployment verification, or scripts/smoke-test.
---

# Release Readiness Harness

## Purpose

Prevent agents from treating a passing test suite as the whole release decision.

## Inspect First

- release docs, CI/CD workflows, deployment config, smoke tests, migrations, changelog, version files, rollback docs, and observability diagnostics

## Procedure

1. Define readiness.
   - Full validation evidence from `./scripts/validate` or documented equivalent.
   - Fast smoke tests that prove the release/runtime can start and answer a minimal health or user-flow check.
   - Migration status.
   - Rollback plan.
   - Monitoring or diagnostics.
   - Known risks.

2. Add release assets.
   - `docs/release/checklist.md`
   - `docs/release/rollback.md`
   - `scripts/smoke-test` where feasible; keep it fast and runtime/deployment-focused, not a default alias for full `./scripts/validate`.
   - Select a stack-aware smoke pattern when useful:
     - web app: request the base URL or one minimal browser smoke path.
     - API service: request `/health` or the configured health endpoint.
     - database-backed app: check database readiness plus migration status.
     - library/package: run a fast import/build sanity check.
   - `CHANGELOG.md` when the project uses changelogs or the user asks.

3. Wire checks.
   - Coordinate with `ci-cd-harness` for deployment gates.
   - Coordinate with `migration-and-schema-harness` for migration risk.
   - Coordinate with `termination-gatekeeper` so release readiness is not claimed before task completion evidence exists.

## Validation

- Run `./scripts/smoke-test` when present.
- Run or cite full `./scripts/validate` separately from smoke evidence.
- Confirm rollback steps are concrete.
- Confirm release docs cite validation commands.

## Completion Criteria

- A release has explicit readiness, smoke, rollback, and verification criteria.
