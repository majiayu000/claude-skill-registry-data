---
name: testing
description: TDD patterns and test quality guidelines. Use when writing tests, setting up test infrastructure, TDD workflow, integration tests, unit tests, test strategy, mocking, test fixtures, test helpers, assertion patterns, test coverage, red-green-refactor cycle, failing tests, test quality review, or test anti-patterns.
user-invocable: false
---

## Philosophy
Write tests first. Tests encode requirements, not implementation details.
Coverage means behavior covered end-to-end, not test count — a green suite full of
isolated unit tests can coexist with a completely broken product.

## Integration Tests (Preferred)
Test real flows end-to-end. Prefer integration tests that exercise the actual
application stack over isolated unit tests.

## Unit Tests (Justify Every One)
Default to zero unit tests. Write one only when it catches something an
integration test cannot reasonably catch — and be able to state, in one line,
what that something is. Logic that typically clears this bar:

- State machines
- Calculations
- Validation rules
- Parsing logic

Belonging to this list is not the justification by itself — the justification is
the concrete failure the unit test catches that the integration suite would miss
(e.g. an edge-case input matrix too expensive to drive through the full stack).
A unit test that cannot be justified this way is a removal candidate, not coverage.

## UI Component Testing (Frontend Stacks)

When the project includes a frontend framework, classify each component before choosing test types.

### Classification Heuristic

| Category | Detection Signals | Test Types |
|---|---|---|
| **Presentational** | Props/inputs only, no services, no HTTP, no state store | Skip standalone tests — covered by parent integration tests. Exception: 3+ conditional branches warrant a focused test. |
| **Smart/Container** | Injects services, uses state management, makes HTTP calls, lifecycle logic | Integration tests (Component Harness / Testing Library) + unit tests for complex service interactions |
| **Form-heavy** | Reactive/template forms, custom validators, multi-step flows | Integration tests for form submission flows. Unit tests only for custom validators with complex rules. |
| **Critical User Journey** | Auth, checkout, payment, data deletion, onboarding | E2E tests (Playwright Test) + integration tests for individual screens |
| **Visual/Layout** | Pure styling, responsive layout, theme switching, design-token-driven | Visual regression tests (Playwright Test `toHaveScreenshot`). Playwright CLI for interactive spot-checks during dev only. |
| **Data Display** | Tables, lists, charts with transformations | Integration tests verifying data binding and transformation |

### Quality-First Rule
When a component spans multiple categories, apply ALL applicable test types.

### Test Type Definitions

| Test Type | What It Tests | Tools |
|---|---|---|
| Unit | Isolated logic (services, validators, pipes) | Framework test runner |
| Integration / Component | Component + real DOM + dependencies | Component Harness (Angular), Testing Library (React/Vue) |
| E2E | Full user journey across pages | Playwright Test (`npx playwright test`) |
| Visual | Layout, styling, responsive behavior | Playwright Test (`toHaveScreenshot`) for regression; Playwright CLI (`playwright-cli`) for ad-hoc dev verification |

## Browser Testing Tools

Two-tier model — **Playwright Test** for CI, **Playwright CLI** for interactive dev work:

| Purpose | Tool | Requires |
|---|---|---|
| Interactive browser automation | Playwright CLI (`playwright-cli`) | `npm i -g @playwright/cli` |
| Visual regression / E2E (CI) | Playwright Test (`toHaveScreenshot`, `npx playwright test`) | `@playwright/test` |

**Rules**:
1. **Playwright Test for anything repeatable** — tests live in the repo, run in CI
2. **Playwright CLI for interactive browser work** — navigation, screenshots, snapshots, form filling, network inspection during development
3. **Prefer the project's established browser tooling** — use Playwright CLI for
   interactive checks when it is installed; do not introduce another browser driver
   solely for an ad-hoc check
4. **Interactive tools are NOT a substitute for tests** — if it matters enough to verify, write a Playwright Test

## Anti-Patterns — NEVER DO THESE
- Hardcode magic values just to make tests pass
- Assert implementation details (call counts, internal method names)
- Copy expected values from implementation — tests should encode requirements, not mirror code
- Mock-heavy unit tests that re-verify wiring — mocking every collaborator and asserting the mocks were called proves the test agrees with the implementation, not that the product works
- Unit tests that would stay green while the product is broken — if the real flow can fail without this test failing, the test is false confidence, not coverage

## Good Assertions
Assert behavior and business rules:
- Status codes and response shapes
- Business state transitions
- Data presence/absence based on requirements
- Error conditions that requirements specify

Stack-specific test patterns are in the stack pack skills (e.g., stack-dotnet, stack-angular).
