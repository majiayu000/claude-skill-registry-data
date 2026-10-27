---
name: test-driven-development
description: Use when the user asks for TDD, test-first, or red-green-refactor, or repository instructions require that cycle. Ordinary requests for tests use when-to-write-tests; a new contract or helper alone does not trigger TDD.
---

# Test-Driven Development

Use a few behavior tests through the public interface. This skill is opt-in
when the user asks for TDD/test-first, or repository instructions require
that cycle. Follow [codebase-design](../codebase-design/SKILL.md) for shared readability
rules and [when-to-write-tests](../when-to-write-tests/SKILL.md) for test scope.

## When to use

- The user asked for TDD, test-first, or red-green-refactor
- Repository instructions require a failing-test-first cycle for the change

## When not to use

- Ordinary implementation or refactors without a TDD request or requirement
- Private helper moves, comment edits, or docs edits alone
- A request for a contract test without a request or requirement for TDD; use
  [when-to-write-tests](../when-to-write-tests/SKILL.md) to choose that test
- "Every new function/method"
- Edges an advisory invented that are not the contract
- Existing tests already cover the public behavior

Default is no new test. Smoke the changed path. See `when-to-write-tests`.

## What to write

One (or a few) tests that walk the real path: input at the public boundary → through the system → observable result.

Good: seed the old inbound tables, apply the migration, list events, assert facts and metadata survived.

Bad: a test per helper, encoder, or bind-list rewrite.

Prefer real collaborators over mocks. Exercise the route/store/UI path for
those contracts; test a public pure function through its inputs and outputs. Supporting notes: [tests.md](tests.md), [mocking.md](mocking.md).

## Where tests live

Next to the source: `foo.test.ts` beside `foo.ts`. Do not create a separate top-level `test/` or `tests/` directory in a package for these.

Exception: an end-to-end test that spawns the real server or CLI, or spans packages, lives in the repo-root `tests/` (for example `tests/smoke.test.ts`).

## Cycle (only when this skill applies)

1. Name one observable behavior in a sentence.
2. Write one failing test through its public interface.
3. Write the simplest complete implementation that makes it pass.
4. Refactor only when it improves understanding; keep related logic together.
5. Repeat for the next required behavior. Do not add tests for each new helper.

Include failure, completion, and cleanup behavior when the contract requires it;
a public pure function does not need an application-wide E2E harness.

Do not delete working code to restart TDD. Outside a requested or required TDD
cycle, use the repository's proportional validation policy.

## Conflicts

User instructions and repository requirements take precedence. Use
`when-to-write-tests` to avoid redundant tests, not to waive required public
behavior or lifecycle coverage.
