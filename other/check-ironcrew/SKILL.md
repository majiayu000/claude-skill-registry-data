---
name: check-ironcrew
description: Run IronCrew's Rust, repository-policy, Lua-example, evaluation, security, PostgreSQL, replica, and release-build validation. Use when the user asks to check, validate, lint, test, verify, audit, or confirm that an IronCrew change is ready. Do not modify failures unless the user also asks for fixes.
---

# Check IronCrew

Run from the repository root. Treat `.github/workflows/ci.yml` as authoritative
if it diverges from this skill. Report drift during a validation-only request;
reconcile files only when the user also asks for changes.

## Select the gate

- Use focused tests while iterating, including negative, cancellation,
  concurrency, and boundary cases relevant to the change.
- Every Rust task finishes with `cargo fmt --all -- --check`,
  `cargo clippy --all-targets -- -D warnings`, and
  `cargo test --all-targets`.
- Add Lua validation when docs, examples, the Lua runtime, crew construction,
  tools, or public workflow behavior change.
- Add PostgreSQL validation when schemas, leases, idempotency, HITL, run events,
  reconciliation, or replica behavior change. Never use shared or production data.
- Use the complete gate before a requested commit/push, release preparation,
  branch integration, or when the user explicitly asks for every check.

## Pre-push admission

- Enable the repository-owned hook once per clone with `task hooks-install`.
  Confirm `git config --local --get core.hooksPath` returns `.githooks`.
- Before any requested push, list open pull requests targeting the destination
  branch and resolve relevant incoming dependency or workflow updates first.
- Before committing work intended for `develop`, run `task develop-refresh`.
  Review and commit any toolchain, manifest, lockfile, workflow, or policy
  changes produced by the latest-stable refresh before validation.
- Run `./scripts/pre-push-check.sh` directly before push even when the hook is
  enabled. It is the canonical locally reproducible CI gate. It requires a
  clean worktree, upgrades Bun before Bun-based tooling, refreshes managed
  dependencies, and fails closed when refresh changes need a commit or the
  Rust, cargo-audit, actionlint, or immutable GitHub Action pins do not match
  current latest-stable policy.
- The complete pre-push gate requires both `IRONCREW_TEST_PG_FLOOR_URL` for a
  disposable `postgres:17` database and `IRONCREW_TEST_PG_URL` for disposable
  `postgres:latest`. The shared runner checks both connections before any
  destructive tests and runs all five suites serially on each database.
  Missing URLs or incorrect versions fail the gate instead of skipping it.
  The earlier all-target Rust pass has the database URLs removed so destructive
  PostgreSQL fixtures cannot also run concurrently outside the serial gate.
- The hook does not replace GitHub's macOS, Windows, protected-environment, or
  other platform-only jobs. Require the exact pushed commit's CI before merge.

## Repository policy

Run these first because they are cheap and fail before Rust compilation:

1. `python3 -B scripts/check_module_size.py`
2. `python3 -B -m unittest discover -s scripts/tests -p 'test_*.py'`
3. `bun run scripts/validate_skills.ts`
4. `bun run scripts/issues_registry.ts check`
5. `bun test scripts/tests/*.test.ts`
6. `actionlint .github/workflows/*.yml` when available
7. `bun run scripts/check_worktree.ts`
8. `git status --short`, followed by explicit review of every tracked and
   untracked source, policy, and documentation change

Use Bun's native YAML parser for repository-owned YAML checks. Do not add a
Python YAML dependency merely to validate skills or the issue ledger.

## Default Rust gate

Run in this order:

1. `cargo fmt --all -- --check`
2. `cargo clippy --all-targets -- -D warnings`
3. `cargo test --all-targets`
4. `cargo test --doc`
5. `cargo audit --deny warnings` after dependency or security-sensitive changes

Stop after a failure and preserve the actionable output. Do not add an allow,
ignore, or exception merely to make a gate green.

## Lua and evaluation gates

- Run `./scripts/check-lua-examples.sh` for broad Lua, docs, or example changes.
- Run `python3 -m unittest discover -s evaluations/crew-effectiveness -p 'test_*.py'`
  after evaluator changes.
- Run contract mode with the current debug binary and a disposable report path;
  contract mode validates orchestration and scoring, not crew superiority.
- Run `python3 -m unittest discover -s evaluations/replica-soak -p 'test_*.py'`
  after soak-harness changes.

Never expose `.env` values in commands, logs, reports, or summaries. Live
provider evaluation requires explicit intent and must record model, dataset,
repetitions, cost/token, latency, revision, and dirty-worktree boundaries.

## PostgreSQL and replica gate

IronCrew 4.x keeps a PostgreSQL 17 floor for its lifetime; see
`docs/storage.md#postgresql-support-policy`. Pull both `postgres:17` and
`postgres:latest` immediately before creating disposable databases, record
each resolved server version/image digest, and use least-privilege test roles.
Never reuse an existing data volume for a new major version. Set
`IRONCREW_TEST_PG_FLOOR_URL` and `IRONCREW_TEST_PG_URL` only for the gate process.
The runner requires the exact floor major and a newer major for latest; it
does not discover the latest release or provision databases. Fresh image pulls
and version/digest receipts remain required to establish latest-stable coverage.
CI and pre-push use the same command. Automatic `.env` loading is disabled so
test URLs must be supplied explicitly to the process:

```bash
bun --no-env-file run scripts/check-postgres.ts
```

The runner validates both connections before launching the floor suite, then
runs `postgres_store_test`, `usage_storage_test`, `app_db_pg_test`,
`multi_replica_http_test`, and `two_process_replica_acceptance_test` with
`--locked --all-features -- --test-threads=1` against floor and latest in that
order. Any failure stops the gate. Use `--check-only` for read-only admission;
it is not integration-test evidence.

Run the short provider-free replica soak when replica lifecycle, routing,
leases, HITL, journals, or readiness changed. Record the database image/major,
process count, duration, workload, and whether evidence is local or deployed.
A skipped live test is not a pass.

## Report

Report every selected command as pass, fail, skipped, or not applicable.
Separate default Rust, PostgreSQL, process-level, soak, live-provider, Railway,
OpenShift, and platform-only CI evidence. “CI-equivalent” means every locally
reproducible gate; do not claim Windows or another unavailable runner was tested
locally. Do not claim a commit, push, release, or deployment that did not occur.
