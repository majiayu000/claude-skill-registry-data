---
name: check
description: Run focused or complete validation for IronCrew. Use when the user asks to check, validate, lint, test, audit, or verify the repository state.
argument-hint: [focus|complete]
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash
---

# Check

Choose the smallest focused tests while iterating, but finish every Rust task
with the repository's complete all-target Rust gate.

## Repository policy

Run the module policy for production Rust changes and the repository validators
for every changed non-Rust policy surface:

- `python3 -B scripts/check_module_size.py`
- `python3 -B -m unittest discover -s scripts/tests -p 'test_*.py'`
- `bun run scripts/validate_skills.ts`
- `bun run scripts/issues_registry.ts check`
- `bun test scripts/tests/*.test.ts`
- `actionlint .github/workflows/*.yml` after workflow changes, when available
- `bun run scripts/check_worktree.ts`
- `git status --short`, with explicit review of all tracked and untracked
  source, policy, and documentation changes

## Required Rust gate

Run in order and stop on the first failure:

1. `cargo fmt --all -- --check`
2. `cargo clippy --all-targets -- -D warnings`
3. `cargo test --all-targets`
4. `cargo test --doc` after public Rust documentation changes

Run `cargo audit --deny warnings` after dependency or security-sensitive changes.

Add `./scripts/check-lua-examples.sh` for Lua/docs/example changes. Add the
crew-effectiveness or replica-soak Python unit/contract checks for evaluation
changes. For storage, idempotency, leases, HITL, journals, or replica behavior,
run the serial PostgreSQL 15 integration targets with a disposable database and
`IRONCREW_TEST_PG_URL`; a skipped test is not evidence.

Never use shared/production storage or print `.env` values. Report commands as
pass, fail, skipped, or not applicable and distinguish local, PostgreSQL,
process-level, soak, live-provider, Railway, and OpenShift evidence. Do not
modify failures unless the user also asked for fixes.
