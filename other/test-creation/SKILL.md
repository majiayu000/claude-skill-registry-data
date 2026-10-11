---
name: test-creation
description: Add meaningful tests for frontend, backend, APIs, utilities, database behavior, business logic, auth, authorization, forms, state management, regressions, and risky changes. Use when Codex needs to inspect an existing test setup, choose the right test type, create unit tests, component tests, API tests, integration tests, end-to-end tests, regression tests, security/permission tests, migration tests, fixtures, mocks, factories, edge-case coverage, validation tests, ownership/scope tests, error-state tests, loading/empty-state tests, and run or report relevant test commands before production, client handover, deployment, review, refactor, or bug-fix completion.
---

# Test Creation

Use this skill when a task needs regression protection or confidence that behavior actually works.

## Core Rule

Write tests for observable behavior, business rules, access control, edge cases, and regressions. Do not add shallow tests that pass without proving anything meaningful.

## Workflow

1. Understand what needs testing:
   - feature/module, user role, main success behavior, failure behavior, edge cases, business rules, security rules, API contract behavior, database behavior, UI state behavior, and bug regression behavior
2. Inspect existing test setup:
   - folders, naming conventions, unit/integration/API/component/e2e tests, utilities, mocks, fixtures, factories, test database setup, env vars, package scripts, and CI commands
3. Choose the correct test type:
   - unit, component, API, integration, end-to-end, regression, security/permission, or migration test
4. Prioritize high-value cases:
   - main success path, validation failures, permission/ownership boundaries, error handling, edge cases, business calculations, status transitions, auth behavior, payments/financial logic, and critical API contracts
5. Define test cases before or during implementation.
6. Prepare test data safely:
   - use existing fixtures, factories, mocks, fake users, fake tokens, sample payloads, and test database helpers
7. Test success paths.
8. Test validation failures and invalid input where applicable.
9. Test permission, ownership, tenant, shop, role, user, and scope rules where applicable.
10. Test error handling, loading states, empty states, and frontend submit states where applicable.
11. Add regression tests for bugs:
   - the test should fail before the fix and pass after the fix when practical
12. Avoid over-mocking:
   - mock external services, payment gateways, email/SMS, file storage, time/date, randomness, and network calls only when needed
13. Keep tests deterministic:
   - avoid uncontrolled current time, randomness, real network calls, external services, order dependence, and shared mutable state
14. Write clear behavior-focused test names.
15. Run relevant test commands:
   - targeted tests first, broader checks when practical and appropriate
16. Report results honestly:
   - commands run, pass/fail result, failure reason, whether failures relate to the change, and what remains unverified
17. Update CI or test documentation when introducing new test types, commands, environment setup, mocks, or fixtures.
18. Summarize tests added, behavior covered, edge cases, files changed, commands run, result, untested areas, risks, and follow-up recommendations.

Read `references/test-creation-checklist.md` for test-type selection, high-value case planning, fixture guidance, anti-patterns, command reporting, and the final report format.

## Non-Negotiable Rules

- Do not write tests before understanding expected behavior.
- Do not ignore existing test conventions.
- Do not add shallow tests that prove little.
- Do not rely only on snapshot tests for important behavior.
- Do not skip permission tests for protected actions.
- Do not skip validation tests for user input.
- Do not skip regression tests when fixing bugs unless impossible or clearly explained.
- Do not over-mock internal behavior.
- Do not use real external services in normal automated tests.
- Do not create flaky tests that depend on uncontrolled time, randomness, test order, or network.
- Do not claim tests passed if they were not run.
- Do not hide failing tests.
- Do not introduce new test frameworks unless necessary and approved.
- Keep tests focused, readable, deterministic, and maintainable.

## Output Contract

When using this skill, provide:

1. Feature or behavior tested.
2. Existing test setup discovered.
3. Test cases added.
4. Test type chosen.
5. Important paths covered: success, validation, permissions, errors, edge cases, regressions.
6. Files changed.
7. Commands run and real result.
8. Remaining untested areas.
9. Risks and follow-up recommendations.
