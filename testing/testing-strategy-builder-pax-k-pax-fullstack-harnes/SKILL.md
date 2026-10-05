---
name: testing-strategy-builder
description: Create a practical test strategy that coding agents can extend consistently. Use when a repo needs unit/integration/e2e conventions, fixtures, test command wrappers, examples, or a bug-fix rule that starts with a failing reproduction test.
---

# Testing Strategy Builder

## Purpose

Make tests easy for agents to add correctly by defining taxonomy, commands, fixtures, naming, and examples.

Use `tdd-playwright-workflow` for strict red-green-refactor execution, failing bug reproductions, or Playwright browser workflows.

## Inspect First

- existing tests, fixtures, and test runners
- package scripts or framework commands
- CI test behavior
- source modules with high behavioral risk
- previous bug reports when available

## Procedure

1. Classify tests.
   - Unit: isolated domain or utility behavior.
   - Integration: database, API, service, or module collaboration.
   - E2E: full user or API workflow.
   - Contract: public API or schema compatibility when relevant.
   - For web apps, prefer at least one browser e2e flow covering create/edit/delete or the closest product lifecycle.

2. Normalize commands.
   - Add `scripts/test`.
   - Add `scripts/test-unit`, `scripts/test-integration`, and `scripts/test-e2e` only when the repo can support them.
   - For Bun projects with Playwright, make `scripts/test` target unit/integration paths explicitly so it does not discover Playwright specs; keep Playwright behind `scripts/test-e2e`.
   - Include tests in `scripts/validate`.

3. Document conventions.
   - File naming and placement.
   - Fixture ownership.
   - When to use each test type.
   - How to run narrow tests.
   - How to write a bug reproduction test.

4. Add examples.
   - Prefer one small realistic example per test layer that exists.
   - Do not add fake tests that assert implementation details or pass trivially.
   - Use `assets/templates/playwright-e2e.spec.ts.tmpl` only when Playwright is already present or the task explicitly accepts adding browser e2e tooling.
   - Browser tests should locate icon-only controls by accessible name; UI code should provide `aria-label` or an equivalent component prop.

5. Align CI.
   - Ensure CI runs the same command interface.
   - Keep slow e2e tests separated if needed.
   - Use `tdd-playwright-workflow` when a change must prove behavior through unit and Playwright tests before implementation.
   - Use `termination-gatekeeper` to require e2e evidence when changed files cross UI, API, runtime, or data boundaries.

## Required Rule

When fixing a bug, add a failing reproduction test first unless impossible. If impossible, document why in the final response or PR validation notes.

## Validation

- Run the narrowest test command for any added tests.
- Run `./scripts/test`.
- Confirm docs match actual runner names and paths.
- For web e2e additions, run the browser flow or document the exact missing runtime dependency.

## Completion Criteria

- Agents know which test type to write for a change.
- Test commands are stable and documented.
- Fixtures and examples are easy to copy without creating brittle tests.
