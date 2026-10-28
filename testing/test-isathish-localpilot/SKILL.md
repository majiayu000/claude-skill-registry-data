---
name: test
description: Add or improve automated tests and make them pass — detect the test framework, write focused unit/integration/e2e tests with edge cases, run them, and fix real failures. USE WHEN the user asks for tests, coverage, "write tests for", "TDD", "make sure this works", "add a regression test", or after implementing a non-trivial change.
---

# Test

Goal: tests that fail for the right reason, pass reliably, and read like documentation of the behaviour.

## 1. Detect the setup
- Find the framework and runner: look in the package manifest / config files (`jest.config*`, `vitest.config*`, `pytest.ini`, `pyproject.toml [tool.pytest]`, `go.mod` + `_test.go`, `Cargo.toml`, `*.csproj` + xunit/nunit, `phpunit.xml`, `.mocharc*`, `playwright.config*`, `cypress.config*`).
- Find where tests live and how they are named (`file_search` for `**/*.test.*`, `**/*_test.*`, `**/tests/**`, `**/__tests__/**`). Read one existing test near the code under test and copy its style: imports, fixtures, mocking approach, assertion library.
- Find the command: manifest scripts (`test`, `test:unit`), Makefile targets, CI workflow steps. Learn how to run a single file/test (e.g. `npx vitest run path`, `pytest path::test_name -q`, `go test ./pkg -run Name`).
- No framework yet? Pick the ecosystem default (vitest/jest for JS/TS, pytest for Python, built-in `testing` for Go, `cargo test` for Rust, xunit for .NET) and add the minimal config + script. Ask with `ask_user` only if the choice is contentious for the project.

## 2. Decide what to test
Read the code under test in full. For each public behaviour list:
- the happy path(s)
- boundaries (empty, one, many, max, zero, negative, unicode, very long)
- error paths (invalid input, missing file, network failure, timeout, permission denied) — assert the message/type the caller relies on
- state/order dependencies and concurrency where relevant
- regression: if fixing a bug, first write a test that reproduces it and watch it fail.
Prioritise: behaviour over implementation details; the riskiest logic first; one assertion focus per test.

## 3. Write
- Arrange / Act / Assert, descriptive names ("returns empty list when file is missing"), no logic in tests, deterministic (no real time/network/random — inject or mock at the boundary the codebase already uses).
- Use the project's fixtures/factories; create small helpers only when three or more tests need them.
- Prefer real objects over mocks for pure code; mock only I/O and external services.
- Keep test data minimal and meaningful; avoid snapshot tests for logic.

## 4. Run and fix
- Run the new test file alone first (`run_command`), then the full suite.
- A failing test means either the test is wrong or the code is. Read the assertion diff carefully; fix the real cause. Never make a test pass by loosening it, skipping it, or special-casing the code for the test.
- Flaky? Find the nondeterminism (time, order, shared state, async leak) and remove it.
- Run `get_diagnostics` on test files too — type errors in tests count.

## 5. Report
- Summarise: tests added (file → cases), command used, result (N passed), and any behaviour you discovered is untested or suspicious. Suggest the next most valuable test if coverage is thin.
