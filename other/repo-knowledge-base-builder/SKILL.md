---
name: repo-knowledge-base-builder
description: Build operational repo-local documentation for coding agents. Use when a repo needs docs that explain product intent, architecture, commands, testing, quality gates, observability, security, release, or specs in a way Codex can act on.
---

# Repo Knowledge Base Builder

## Purpose

Create a `docs/` knowledge base that works as project memory for agents. The docs must be operational: commands, paths, examples, invariants, failure modes, and update rules.

## Inspect First

- README and existing docs
- manifests, scripts, CI, env examples, routes, schemas, migrations, and test layout
- source directories and module boundaries
- user-provided product description or feature specs

## Procedure

1. Build the index first.
   - `docs/00-index.md` lists the docs, what each owns, and when to update it.

2. Split knowledge by ownership.
   - Product: goals, features, users, non-goals.
   - Architecture: layers, boundaries, data flow, key decisions.
   - Development: setup, commands, environment, CI.
   - Testing: taxonomy, fixtures, examples, bug reproduction rule.
   - Quality: style, dependencies, technical debt, golden patterns.
   - Observability: logging, diagnostics, metrics/tracing where applicable.
   - Security: baseline, secrets, auth/session, input validation.
   - Release: checklist, rollback, smoke tests.
   - Specs: feature-specific working decisions.

3. Convert decorative docs into operational docs.
   - Prefer concrete paths and commands over general advice.
   - Mark assumptions clearly.
   - Mark deprecated docs clearly and link replacements.

4. Keep docs synchronized.
   - Update docs when commands, env vars, routes, schemas, architecture, tests, or release behavior change.
   - Use `documentation-sync-enforcer` for drift detection and `scripts/check-docs`.
   - Use `prompt-to-spec-converter`, `task-planning-and-pr-protocol`, and `release-readiness-harness` for deeper specs, task protocol, and release docs.

## Required Docs

- `docs/00-index.md`
- `docs/product/vision.md`
- `docs/architecture/overview.md`
- `docs/architecture/boundaries.md`
- `docs/development/local-setup.md`
- `docs/development/commands.md`
- `docs/development/environment.md`
- `docs/testing/strategy.md`
- `docs/quality/code-style.md`
- `docs/quality/dependencies.md`
- `docs/quality/technical-debt.md`
- `docs/observability/debugging.md`
- `docs/security/baseline.md`
- `docs/release/checklist.md`

## Validation

- Every linked file exists.
- Commands in docs match wrappers or manifests.
- Environment variables mentioned in docs match `.env.example`.
- Docs identify their update triggers.

## Completion Criteria

- A new agent can use docs to understand what to build, where to put it, how to validate it, and what not to break.
- Docs are not just prose summaries; they contain actionable repo facts.
