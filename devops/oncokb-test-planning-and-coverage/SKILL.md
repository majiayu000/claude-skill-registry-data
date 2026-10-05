---
name: oncokb-test-planning-and-coverage
description: Decide when to add tests and how to design them; require user-provided test cases before implementing tests.
---

## Purpose

Use this skill to decide test scope and test type before writing tests.

## When to use this skill

- Use when adding, changing, or reviewing automated tests.
- Use when deciding whether code changes require unit tests, end-to-end tests, or both.
- Use when a request mentions coverage, regressions, or test strategy.

## Core policy

- Always ask the user which specific test cases must be added before implementing tests.
- Do not guess required test cases.
- You may recommend candidate test cases and test types, but wait for user confirmation of what to include.

## Test type rules

- Add unit tests for non-trivial logic.
- Treat business logic beyond basic CRUD as non-trivial unless the user states otherwise.
- Add end-to-end tests for user-facing I/O behavior, including API call flows and rendering output checks.
- If end-to-end tests are in scope, include performance testing as required coverage for those end-to-end flows.
- For UI rendering behavior, include screenshot-based assertions when the project already supports visual or snapshot-style rendering checks.
- If the codebase already supports database migration tests and the change affects schema or migration logic, add migration-focused tests.

## Required question before writing tests

Ask one grouped question that captures:

- The exact test cases the user wants added.
- The priority order of those test cases.
- Any required constraints (framework, fixtures, environments, CI limits, or snapshot policy).
- Any required constraints for migration tests when migration test infrastructure already exists.
- Any required constraints for end-to-end performance testing (budgets, thresholds, tooling, and environments) when end-to-end tests are present.

If the user has already provided explicit test cases, confirm them briefly and proceed.

## Workflow

1. Classify the changed behavior.
   - Separate non-trivial logic from CRUD-only behavior.
   - Identify user-facing I/O surfaces (API responses, page rendering, server rendering, client rendering).
   - Completion criterion: candidate unit-test and end-to-end-test targets are listed.

2. Propose test options and ask for required test cases.
   - Recommend specific unit and end-to-end test ideas.
   - Ask the required grouped question and wait for user selection.
   - Completion criterion: user-approved list of test cases exists.

3. Implement only approved test cases.
   - Map each approved case to the right test layer (unit or end to end), and include required performance checks for any approved end-to-end coverage.
   - Keep tests deterministic and focused on observable behavior.
   - Completion criterion: every approved case is implemented once at the correct layer.

4. Validate and report coverage mapping.
   - Run the relevant test commands.
   - Report pass/fail and map each implemented test back to the user-approved case list.
   - Completion criterion: user can verify that requested cases were implemented without guessing.

## What to avoid

- Adding tests the user did not request as required coverage.
- Treating trivial CRUD plumbing as needing deep unit test suites by default.
- Replacing end-to-end checks with unit mocks for user-facing I/O behavior.
- Silent assumptions about expected edge cases when the user has not confirmed them.
