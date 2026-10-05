---
name: ci-cd-harness
description: Build PR validation, local CI reproduction, CI triage, and deployment gates. Use when a repo needs GitHub Actions beyond basic validation, coverage/artifact expectations, branch protection notes, CI failure triage docs, or release/deployment readiness gates.
---

# CI/CD Harness

## Purpose

Make CI reproducible, debuggable, and aligned with local validation instead of a separate source of truth.

## Inspect First

- existing workflows, package manager, scripts, test/build outputs, coverage config, deployment config, branch protection docs, and CI failures if available

## Procedure

1. Align local and remote validation.
   - CI should call `./scripts/validate` or documented wrappers.
   - Add `scripts/ci-local` when CI-only failures are likely.
   - Prefer a thin `scripts/ci-local` wrapper that runs lint, typecheck, unit tests, and build before adding slower release or deployment checks.

2. Improve PR checks.
   - Cache dependencies.
   - Upload useful artifacts or coverage only when project tooling produces them.
   - Separate slow or deployment checks from fast PR checks when needed.

3. Document triage.
   - Add `docs/development/ci.md`.
   - Include how to reproduce CI locally and how to inspect artifacts/logs.

4. Define deployment gates.
   - Coordinate with `release-readiness-harness`.
   - Document required validation before deploy.
   - Keep fast smoke checks separate from full `./scripts/validate`; CI-local may reproduce PR validation while smoke proves runtime/deployment health.
   - Use stack-specific smoke examples where possible: web URL, API health endpoint, DB readiness/migration status, or library import/build sanity.

## Validation

- Validate workflow syntax when tooling is available.
- Run `./scripts/ci-local` or `./scripts/validate`.
- Confirm CI docs match workflow names and commands.

## Completion Criteria

- CI uses the same stable command interface as local development.
- CI failures have a documented reproduction path.
