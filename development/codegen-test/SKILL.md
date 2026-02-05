---
name: codegen-test
description: A skill for writing Go tests in a TDD workflow. Follow README/Issue requirements and existing test conventions, add a balanced set of table-driven cases across behavior/boundaries/branches, and produce maintainable tests without excessive mocking or coverage-chasing.
---

# Codegen Test Skill

## Purpose
- Lock down the spec (expected behavior) based on README.md / Issue and run **Red → Green → Refactor**.
- Write idiomatic, readable, maintainable Go tests (table-driven, subtests, small helpers).
- Avoid focusing only on branch coverage; also add **boundary**, **black-box (behavior)**, and **regression** perspectives.
- Do not make coverage the “goal.” Do not write tests that reduce maintainability.
- Avoid mocks as much as possible; implement in a more classicist style.

## When to use
- When you want to write tests first for a feature, bug fix, or refactor.
- When existing behavior is unclear and you want to build consensus (freeze the spec) via tests.
- When you want to add regression tests to prevent recurrence.

## Deliverables (expected output)
- Tests that transition from failing → passing (Red → Green is observable)
- Test code aligned with the project’s existing test style
- Commands executed (go test / race / optionally bench) and brief result notes

---

## Execution steps (follow this order)

### 0) Safety measures before changes
- Tests become the spec (contract). Do not contradict README/Issue.
- If existing tests act as the de-facto spec, prioritize and do not break them.
- Start with the minimum necessary tests, then incrementally add perspectives as needed.

### 1) Understand the spec (README.md / Issue)
- From README.md / docs / comments / Issue, finalize acceptance criteria (expected behavior) as bullet points.
- Break them down (ideally usable as test case names):
  - Representative happy-path cases
  - Error cases (invalid input, broken preconditions, dependency failures)
  - Boundary values (empty, 0, min/max, off-by-one)
  - Concurrency (simultaneous execution, ordering, shared state)
  - Compatibility (preserve past behavior, regression prevention)

### 2) Follow existing test conventions (highest priority)
- Do not introduce additional external modules.
- Search existing `_test.go` files and match the following:
  - Package style (`package x` vs `package x_test`)
  - Assertion approach (stdlib `testing` vs an existing assertion library already used)
  - Table-driven style (`tests` / `tt`, field naming patterns)
  - Helper locations, naming, fixture patterns
  - Test data layout (whether `testdata/` exists)

*This skill is not about imposing new rules; it prioritizes matching the existing conventions.*

### 3) Test design principles
- Prefer black-box testing (behavior of the public API).
- Do not directly test implementation details (private functions/internal state).
  - Exception: Only when “hard to observe from the outside” requirements matter (e.g., performance or race-safety), and only with minimal supplemental tests.
- Do not write trivial tests (e.g., “assert the type”).

### 4) Use table-driven tests as the default shape
- If multiple conditions exercise the same logic, use a table-driven test.
- Recommended structure:
  - `tests := []struct{ name string; input ...; want ... }{ ... }`
  - `for _, tt := range tests { t.Run(tt.name, func(t *testing.T) { ... }) }`
- Prefer `input` / `want` prefixes for field names.
- Do not stuff functions or complex branching (e.g., `shouldX`, `setupMocks func...`) into the table.
  - If it becomes complex, split the table or split the test function.

### 5) Balance branch coverage (white-box) with behavior/boundaries (black-box)
- Branch coverage: ensure each if/switch branch is exercised at least once.
- Boundaries: add empty/min/max and just-before/just-after cases (off-by-one).
- Behavior: include “what must be guaranteed” in the test name so it’s understandable to readers.

### 6) Avoid mocks as much as possible (classicist)
- Principle: use something “close to real.”
  - Examples: in-memory implementations, `bytes.Buffer`, `httptest`, `t.TempDir()`, `net.Pipe()`
- Do not over-introduce interfaces (often harms design and maintainability).
- If external dependencies must be cut, swap them at the smallest boundary.
  - If large mock setups are required, prefer splitting the unit under test into smaller components.

### 7) Concurrency tests (only when needed, carefully)
- Make race-prone areas verifiable with `-race`.
- If using `t.Parallel()`, always rebind loop variables:
  - Do `tt := tt` immediately before `t.Run` to avoid capture bugs.
- For concurrent cases, explicitly state what is being guaranteed (no races, ordering, idempotency, etc.).

### 8) Run and verify (required)
- Run package-level (or full) tests including race checks:
  - `task go:test`
- If performance is a key concern, add/run benchmarks (only when necessary):
  - `task go:bench`
---

## Prohibited (do not do)
- Tests that are hard to read/brittle written only to raise coverage
- Complex branching inside table-driven tests or excessive flags (hurts maintainability)
- Tests tightly coupled to implementation details (not refactor-friendly)
- Unnecessary interfaces or heavy reliance on mocks

---

## Final report about test code and approach (keep it short)
- Output as a Markdown report:
  - Filename: `<issue_number>_<datetime>_test_report.md`
- Include:
  - Spec summary (acceptance criteria from README/Issue)
  - Added test perspectives (branches/boundaries/behavior/regression/concurrency)
  - Commands executed (test / race / bench)
  - Reasons for tests intentionally not written (e.g., avoiding excessive mocks), if needed