---
name: quality-gates-installer
description: Install executable quality gates for a repo and normalize validation behind stable scripts. Use when a project needs linting, formatting, type checking, tests, builds, doc checks, boundary checks, CI, or a single scripts/validate command for Codex.
---

# Quality Gates Installer

## Purpose

Turn repeated agent mistakes into executable checks. Prefer project-native tooling and normalize it behind stable wrappers.

## Inspect First

- manifests and package scripts
- existing linters, formatters, typecheckers, test runners, build commands, CI
- current `scripts/` directory
- docs describing commands or quality policy

## Procedure

1. Detect existing checks.
   - Reuse project-native commands first.
   - Do not add dependencies just to satisfy a generic harness shape.

2. Create stable wrappers.
   - `scripts/lint`
   - `scripts/typecheck`
   - `scripts/test`
   - `scripts/build`
   - `scripts/check-boundaries`
   - `scripts/check-docs`
   - `scripts/audit-entropy`
   - `scripts/validate`
   - Optional control-loop wrappers when useful: `scripts/check-feature-state`, `scripts/check-session-handoff`, `scripts/init-check`, `scripts/termination-check`, `scripts/check-sprint-contract`, and `scripts/check-instructions`.
   - Optional surface wrappers when current repo surfaces require them: `scripts/test-e2e`, `scripts/click-path-audit`, `scripts/check-research-evidence`, and `scripts/ci-local`.

3. Make `scripts/validate` canonical.
   - Run lint, typecheck, tests, build, boundaries, docs, and entropy audit in deterministic order.
   - Omit or no-op only when the repo truly lacks that concern, and document why.

4. Add CI.
   - For GitHub repos, add `.github/workflows/ci.yml` that runs the same validation interface.
   - Cache dependencies using the package manager's standard cache.
   - Keep CI reproducible locally through `scripts/ci-local` when helpful.
   - Use `ci-cd-harness` when deployment gates, artifacts, coverage, or CI failure triage are needed.

5. Update docs.
   - Update `docs/development/commands.md`.
   - Update `docs/quality/code-style.md`.
   - Update `AGENTS.md` command list if needed.
   - Use `security-baseline`, `dependency-governance`, and `documentation-sync-enforcer` for specialized security, dependency, and docs checks.
   - Use `termination-gatekeeper` when validation must prove task completion instead of baseline health.

## Wrapper Rules

- Use `#!/usr/bin/env bash` and `set -euo pipefail` for shell wrappers.
- Scripts should be executable.
- Prefer `rg` for text checks.
- Fail with clear messages.
- Avoid formatting commands that rewrite files unless the user explicitly asked for autofix behavior.
- In Bun repos with Playwright, keep `scripts/test` scoped to unit/integration tests and run Playwright only through `scripts/test-e2e`.
- Generated text checks should scan source files by extension, not docs or `AGENTS.md`, unless the check is explicitly a docs check.

## Validation

- Run each wrapper individually.
- Run `./scripts/validate`.
- Run CI syntax checks when feasible.
- Confirm docs and `AGENTS.md` list the same commands.

## Completion Criteria

- One command tells Codex whether the repo baseline is healthy.
- Missing tools are either installed intentionally or documented as not applicable.
- CI and local validation use the same stable interface.
