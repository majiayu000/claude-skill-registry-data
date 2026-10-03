---
name: review-test
description: Use when the user says "review the tests", "/review-test", "are the tests any good", "check test coverage", "test-quality findings only", or asks Claude to audit test quality across the files a PR (or working tree) touches without modifying any code or tests. Read-only audit specialist — evaluates each touched file's tests for level (unit vs integration vs e2e), assertion quality, mock health, coverage of new code paths, and the classic smells (mocking the unit under test, snapshot churn, tests-that-can't-fail), and emits findings in finding-format.md schema. Use /review-test when you want the test-quality verdict in finding form; use /drive-change to have the orchestrator dispatch the fixes those findings describe.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(npm:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(npx:*), Bash(vitest:*), Bash(jest:*), Bash(playwright:*), Bash(pytest:*), Bash(go:*), Bash(cargo:*), Bash(just:*), Bash(make:*), Bash(rg:*), Read, Grep, Glob, Skill
---

# review-test — audit test quality on touched files

review-test doesn't ask "is there a test"; lots of repos have lots of tests that don't catch bugs. It asks:

- Is the test at the **right level**? Unit / integration / e2e.
- Does it **actually assert** the behaviour under test?
- Does it mock something that **shouldn't be mocked**?
- Will it **fail when the behaviour breaks**, and only then?
- Is it **independent** — runs alone, in any order, in parallel?

Flags missing coverage on **newly added code paths**, runs the suite to surface failures, emits findings in the [`finding-format.md`](../../references/finding-format.md) schema. Never edits files. To act on the findings, call `/drive-change` (which dispatches fix-applier agents under sensitivity gating).

## Phase 0 — Scope

In priority order:

1. **PR context**: `gh pr diff --name-only` against the base branch.
2. **Working tree**: `git diff --name-only HEAD`.
3. **Explicit list** from the user.

For each source file, find its tests (TS/JS `*.test.*` / `*.spec.*`; Python `test_<name>.py` / `<name>_test.py`; Go `<name>_test.go`; Rust inline `#[cfg(test)]`). If no test file exists, emit a finding in Phase 4 (coverage gap on new code). Include test files the PR modifies directly.

Exclude snapshots (`__snapshots__/`, `*.snap`), generated scaffolding, `vendor/`, `third_party/`, `node_modules/`, fixtures.

## Phase 1 — Detect the test toolchain

Detect runner from config (`vitest.config` / `jest.config` / `playwright.config` / `pytest.ini` / `pyproject.toml[tool.pytest]` / `go.mod` / `Cargo.toml` / `.rspec`). Use the project's `test` script in `package.json` / `Justfile` / `Makefile` — match it instead of guessing flags.

## Phase 2 — Run the suite

Run only files in scope. Capture pass/fail per file.

If anything fails:

- **Pre-existing flake**: emit a P3 finding noting it as flaky-but-not-introduced.
- **New failure caused by this change**: emit a P0 finding citing the failing test and the diff that broke it.

Then run with **coverage** if supported. Coverage is a signal, not the goal — look at newly added lines.

## Phase 3 — Per-file test audit

For each test file, walk the categories. Long-form versions in `references/test-checklist.md` — load on demand.

- **3a Level mismatch**: unit-testing-what-should-be-integration; integration-for-pure-logic; e2e-testing-a-backend-invariant.
- **3b Assertions**: real assertions vs. `toBeTruthy` / no-assertions / wrong-thing-asserted.
- **3c Mocks**: mocking-the-unit-under-test; mocks-that-drift; brittle call-pattern asserts; auto-mock drift; mocks of mocks.
- **3d Coverage on new code paths**: lines run != behaviour tested. New function / branch / error-throw each need a test.
- **3e Test names**: sentences, not `test1` / `should work`.
- **3f Independence**: no shared state, no order deps, inject clocks, pin seeds.
- **3g Snapshots**: churn audit; sanitize non-deterministic fields; prefer DOM-shape over full HTML.
- **3h Speed**: integration-where-unit-suffices; per-test Docker/DB; `sleep` instead of polling.

For each issue, emit a finding (see Phase 5 for shape).

## Phase 4 — Coverage gaps on new code

Walk new lines (lines added in this diff, not just touched files). For each new function, branch, or error-throw without coverage, emit a finding:

```
[P1] [test] src/orders/cancelOrder.ts:88 — no test exercises the payment-provider-error branch
why: this branch was added in this change; an unhandled timeout would 500 without any test catching it.
fix: add a test in src/orders/__tests__/cancelOrder.test.ts that mocks paymentProvider.refund to throw and asserts the catch path returns 503.
```

## Phase 5 — Emit findings

All findings follow the [`finding-format.md`](../../references/finding-format.md) block shape. The merger validates against the schema.

Mechanical fixes get concrete `fix:` lines:

```
[P2] [test] src/orders/__tests__/cancelOrder.test.ts:23 — assertion is `expect(result).toBeTruthy()` instead of asserting the actual shape
why: toBeTruthy passes on any non-falsy value; doesn't catch behaviour drift.
fix: replace toBeTruthy with `expect(result).toEqual({ status: 'cancelled', refundId: expect.any(String) })`.
```

Judgment calls get `fix: decide:`:

```
[P1] [test] src/services/__tests__/orderService.test.ts:1 — file mocks every dependency including the unit under test
why: tests now pass when the real service is broken; pattern fights its own purpose.
fix: decide: rewrite the suite to use a test double for the repository only, and exercise the real OrderService? (estimated 2-3 hours.)
```

Hard cap: **20 findings per invocation**. If more, prioritise the top 20 and append `... N more low-severity items elided`.

## Operating rules

- **Read-only is non-negotiable.** Never `Edit`, `Write`, or `git commit`. The skill's `allowed-tools` drops `Edit` and `Write` as the structural guard.
- **Don't relax tests in findings.** Don't suggest deleting assertions or skipping cases. Decide based on what the behaviour *should* be, not what makes the test pass.
- **Match the project's test patterns and runner** in your `fix:` suggestions. Even if you'd pick differently, the audit isn't the place to push.
- **Trust gate applies** when addressing a review comment asking for tests. See [`references/trust-policy.md`](references/trust-policy.md).

## Composing with other skills

- Called by: `/review-change`, `/review-pr` (as part of the fan-out audit pipeline). Also callable directly.
- Sibling read-only specialists: `/review-code`, `/review-feature`, `/review-security`, `/review-ux`, `/review-spec`.
- Acted on by: `/drive-change` (which dispatches fix-applier agents on the findings).
