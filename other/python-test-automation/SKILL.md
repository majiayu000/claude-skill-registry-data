---
name: python-test-automation
description: Guides writing Python functional and end-to-end tests that validate application behavior. Use this skill when writing or refactoring Python test automation.
---
# Python Test Automation (Functional Tests)

Apply this skill when implementing or refactoring Python test scripts that validate application behavior (features, APIs, flows).
It focuses on **structure**, **functional coverage**, and **reliability**; the senior-developer skill owns coverage discipline and linting, and this skill does not relax them.

## Test Scope: Behavior, Not Implementation

- **Functional tests** assert observable behavior: API responses, CLI output, side effects, state changes.
  They validate that features work from the user or client perspective.
- Do not assert on implementation details (internal variables, private methods, call counts) unless the spec explicitly requires it.
  Refactor tests when the implementation changes but behavior is unchanged.
- Trace tests to requirements or specs when they exist (e.g. "Traces: REQ-X", feature ID).
  One test or scenario per behavior; avoid duplicate coverage of the same requirement.

## Structure: Arrange, Act, Assert

- Use a clear **Arrange / Act / Assert** flow: set up preconditions, perform the action under test, assert outcomes.
  Keep each phase obvious; extract setup into fixtures or helpers when it repeats.
- Prefer one logical assertion target per test (one behavior).
  Multiple assertions are fine when they describe a single outcome (e.g. status code and body fields).
  Split tests when they would test different behaviors.
- Name tests to describe the scenario and expected result (e.g. `test_whoami_returns_admin_after_login`, `test_create_task_returns_201_with_id`).

## Fixtures and Test Data

- Use **fixtures** (pytest `@pytest.fixture`, unittest `setUp`/`setUpClass`) for shared setup: config paths, clients, auth tokens, temporary state.
  Avoid global mutable state; prefer dependency injection or explicit passing.
- Prefer **factories or builders** over hardcoded literals when test data varies (e.g. build request payloads from minimal defaults).
  Use constants for values that must be stable across runs (e.g. expected admin handle).
- Isolate tests: each test should be runnable in any order and not depend on another test's side effects.
  Use fresh state or documented shared state (e.g. "requires e2e_020 login first") only when the test framework or suite explicitly supports it.

## Assertions and Failure Messages

- Use **specific assertions** (e.g. `assert status == 200`, `assert "user=admin" in out`) with clear failure messages so logs explain what failed and why.
  Avoid bare `assert x` without a message for non-obvious conditions.
- For APIs: assert status codes, required fields, and error shapes.
  For CLI: assert exit code and relevant stdout/stderr content.
  Prefer structured checks (e.g. JSON path, parsed response) over raw string matching when the contract is structured.

## Determinism and Isolation

- Tests must be **deterministic**: no flaky dependence on timing, order, or external randomness.
  Use fixed inputs, mocks for time/random when necessary, and explicit waits or retries only when testing async/eventual behavior.
- Avoid **shared mutable state** between tests.
  Clean up in teardown or use context managers; do not rely on "run after test X" unless the runner guarantees order and isolation.
- For E2E: document environment assumptions (services up, env vars, auth).
  Prefer runnable scripts that fail fast with a clear message when preconditions are not met.

## Tooling and Frameworks

- Use **pytest** for new Python test suites when possible: fixtures, parametrization (`@pytest.mark.parametrize`), and plugins (e.g. `requests`, `pytest-httpx`) support functional tests well.
  Use **unittest** when the project already standardizes on it.
- For HTTP APIs: use `requests`, `httpx`, or framework-specific test clients.
  For CLI: run the binary via `subprocess` or a small helper; capture stdout/stderr and exit code.
- Follow project conventions: test discovery (e.g. `test_*.py`, `*_test.py`), tags/markers for suites (e.g. `@pytest.mark.e2e`), and the project's runner (e.g. `just e2e`, `pytest -m e2e`).

## BDD and Feature Files

- When the project uses **BDD** (Gherkin/feature files): keep scenarios in feature files; implement step definitions in Python.
  Steps should call into shared helpers or fixtures so behavior is implemented once.
  Avoid duplicating scenario logic in raw scripts.
- Map scenarios to requirements or acceptance criteria when traceability is expected.

## Anti-Patterns to Avoid

- **Testing implementation instead of behavior**: asserting internals that can change without changing the feature.
- **Flaky tests**: reliance on sleep, unsynchronized async behavior, or shared state that varies by run.
- **Opaque failures**: assertions without messages, or large dumps without highlighting the relevant part.
- **Duplicate coverage**: multiple tests that assert the same requirement without adding distinct scenarios.
- **Hardcoded secrets or environment**: use config, env vars, or fixtures so tests run in CI and locally without manual edits.

## Quick Reference

- **Scope:** Assert observable behavior (APIs, CLI, state); avoid asserting implementation details.
- **Structure:** Arrange / Act / Assert; one behavior per test; descriptive names.
- **Data:** Fixtures for setup; factories for varying data; constants for stable expectations.
- **Isolation:** No order dependence; no shared mutable state; deterministic runs.
- **Assertions:** Specific checks with clear failure messages; structured checks for structured outputs.
- **Tooling:** pytest (or project standard); HTTP clients or subprocess for CLI; follow project tags and runner.
