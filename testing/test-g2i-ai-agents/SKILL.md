---
name: test
description: Behavior-first test guidance.
---

# Test

## Invocation

This skill is performed in the `Developer` persona. If you are not already running as `Developer` (for example, the user invoked `/test` directly), read `subagents/developer.md` and adopt its role guidance for the rest of this task. Stay in the current chat—do not delegate to a subagent.

## Objective

Write or improve tests that defend real user-visible behavior without encoding broken behavior as correct.

## Core Rules

- Start from the expected user behavior or contract, not implementation details.
- Test names must describe observable behavior only.
- Never write a green test that asserts a known bug as correct behavior.
- If a test reveals a product bug, call that out explicitly instead of mutating the test to hide it.
- Prefer existing test helpers, fixtures, and patterns before creating new ones.

## Naming Guidance

- Good: `when a valid user signs in, they reach the dashboard`
- Good: `when repo access is removed, the preview no longer shows that collaborator`
- Bad: `useThing works correctly`
- Bad: `POST /api/foo returns 200`
- Bad: `someHelper handles edge cases`

## Repo Conventions

- Place unit tests close to the code they cover as `*.test.ts` or `*.test.tsx`.
- Run the relevant test suite for unit-level verification.
- Run E2E tests when the change requires browser-flow validation.
- If the repo does not provide a narrower script for the exact test slice you want, say so explicitly rather than inventing one.

## Bug Discovery Protocol

1. A failing test that exposes a real bug is a useful deliverable.
2. If the observed behavior looks wrong, ask whether it is intentional before turning it into the asserted contract.
3. Fix the application behavior when it is in scope.
4. If the bug is out of scope, document the gap clearly instead of pretending the behavior is correct.

## Review Checklist

- Does the test assert a real contract or user-visible behavior?
- Does it verify more than status-only success?
- Does it match existing repo test structure and helpers?
- Does it avoid broad mocks when the contract is integration-sensitive?
- Does it run under the right repo verification command?
