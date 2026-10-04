---
name: tdd
description: Practice test-driven development for new features and bug fixes.
---

# TDD

## Invocation

This skill is performed in the `Developer` persona. If you are not already running as `Developer` (for example, the user invoked `/tdd` directly), read `subagents/developer.md` and adopt its role guidance for the rest of this task. Stay in the current chat—do not delegate to a subagent.

## Objective

Use a red -> green -> refactor workflow for changes that should be test-first.

Use `/code` instead when the work is implementation-heavy but not centered on new automated test coverage, such as tooling, config, or linting work.

## Instructions

1. Determine whether the task is a bug fix or a new feature.
2. For new features, read the relevant spec or acceptance criteria before writing tests.
3. For bug fixes, capture the expected behavior, actual behavior, and reproduction path before writing tests.
4. Identify the most appropriate unit-level test location based on nearby repo patterns.
5. Write the failing test first.
6. Verify the red phase by running the relevant test suite.
7. Implement the smallest change needed to make the new test pass.
8. Re-run tests, then run the applicable verification checks (linting, type checking, etc.).
9. If the change also requires browser-flow validation, call out that E2E tests are relevant and why.
10. End with the test paths, the observed red failure, the passing result, and any follow-up work.

## Guardrails

- Do not create or modify E2E tests unless the user explicitly asks for E2E coverage.
- Keep TDD changes scoped to the behavior under test.
- Refactor only after the tests demonstrate the intended behavior.
