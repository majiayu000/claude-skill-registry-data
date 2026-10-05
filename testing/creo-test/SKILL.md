---
name: creo-test
description: >
  Testing orchestration that routes to unit test and E2E test subagents. Manages test
  plans, coverage tracking, and coordinates test execution across the full stack.
  Supports Vitest/Jest for unit tests and Playwright for E2E tests. Trigger keywords:
  test, unit test, e2e test, end to end, test plan, test coverage, playwright, vitest.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Test Orchestrator

Master coordinator for all testing workflows. Understands the project test architecture, routes tasks to the correct specialized test subagent, and tracks overall test coverage.

## Commands

| Command | Description |
|---------|-------------|
| `/creo test unit` | Write or run unit/integration tests |
| `/creo test e2e` | Write or run end-to-end Playwright tests |
| `/creo test plan` | Create a structured test plan for a feature |
| `/creo test coverage` | Analyze test coverage and identify gaps |

## Subagents

| Subagent | Purpose | When to Route |
|----------|---------|---------------|
| creo-unit-test | Unit and integration tests (Vitest/Jest + Testing Library) | Component, store, hook, service, utility tests |
| creo-e2e-test | End-to-end tests (Playwright) | Full user flow, cross-page navigation, auth flows, responsive testing |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `project_id`, `test_frameworks`, `dev_server_url`, coverage targets
3. Load project extension if it exists at `.claude/skills/creo-test/creo-test-{project_id}.md`. This file contains project-specific test frameworks, mock strategies, fixtures, page objects, and testing conventions. `{project_id}` comes from `project-config.md`. Always load it before doing work.
4. If no config exists, use defaults or ask user

### Routing Rules

Route to **creo-unit-test** when:
- "Write tests for this component"
- "Test this hook/store/utility"
- "Unit test the validation logic"
- "Integration test with providers"
- "Mock the API and test the component"

Route to **creo-e2e-test** when:
- "Test this user flow end to end"
- "E2E test for the wizard"
- "Test login and navigation"
- "Test responsive layout"
- "Automated browser test"

Handle yourself when:
- "Run all tests" -- Execute test commands
- "What is the test coverage?" -- Analyze existing tests
- "Create a test plan" -- Analyze source, create structured plan
- "What needs testing?" -- Read source, identify gaps

### Creating Test Plans

When asked to test a feature:

1. Read source code to understand what needs testing
2. Identify which test types are needed (unit, integration, E2E)
3. Create structured plan:

```markdown
## Test Plan: [Feature Name]

### Unit / Integration Tests (creo-unit-test)

| File | Tests | Priority |
|------|-------|----------|
| `__tests__/component.test.tsx` | Rendering, interaction, state | P0 |
| `__tests__/hook.test.ts` | Hook logic, edge cases | P1 |

### E2E Tests (creo-e2e-test)

| File | Tests | Priority |
|------|-------|----------|
| `e2e/feature/happy-path.spec.ts` | Complete user flow | P0 |
| `e2e/feature/edge-cases.spec.ts` | Error handling | P1 |
| `e2e/feature/responsive.spec.ts` | Mobile/tablet | P2 |

### Mock Requirements

| Module | Mock Strategy |
|--------|---------------|
| API hooks | vi.mock() with factory functions |
| Navigation | Mock useRouter, usePathname |
```

4. Ask for priority confirmation if the plan is large
5. Delegate to specialized subagents

### Unit Test Principles (creo-unit-test)

- **Test behavior, not implementation** -- test what the user sees
- **One assertion per behavior** -- each `it()` tests one thing
- **Arrange-Act-Assert** pattern
- **Factory functions** for test data (no inline literals)
- **Mock at the right level** -- mock API layer, test component logic
- **Frameworks**: Vitest, Jest, Testing Library

### E2E Test Principles (creo-e2e-test)

- **Semantic locators** -- `getByRole()`, `getByText()`, `getByLabel()` (accessibility-first)
- **Test user flows, not implementation** -- interact as a real user
- **Explicit assertions** -- no `waitForTimeout()`, use proper waits
- **Isolate tests** -- each test is independent
- **Auth state reuse** -- `storageState` for authenticated tests
- **Page Object Model** for complex flows
- **Responsive testing** -- `test.use({ viewport: { width, height } })`

### Running Tests

Typical patterns (check project config for specifics):

```bash
# Unit/Integration
pnpm test                              # Run all
pnpm test -- --reporter=verbose        # Detailed output
pnpm test -- --coverage                # With coverage

# E2E
npx playwright test                    # Run all E2E
npx playwright test --ui               # Interactive mode
npx playwright test --debug            # Debug mode
```

### Tracking Coverage

1. List existing test files
2. List source files that lack tests
3. Calculate rough coverage by file count
4. Prioritize gaps: critical paths > happy paths > edge cases > error handling

### Coordinating Cross-Agent Work

When a feature needs both unit and E2E tests:
1. Start with unit tests (faster feedback loop)
2. Then E2E tests (validates integration)
3. Verify no regressions across the stack

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/test-patterns.md` | Common testing patterns and examples |
| `references/mock-strategies.md` | Mocking guide for different frameworks |

## Quality Gates

### Unit Tests
- All tests pass
- No TypeScript errors
- Tests are independent (no shared mutable state)
- Factory functions used for test data
- Mocks reset in `beforeEach`
- Descriptive test names
- Edge cases covered (empty, null, error states)

### E2E Tests
- All tests pass locally
- Tests are independent (no order dependency)
- Semantic locators used
- No `waitForTimeout()` calls
- Auth state reused
- Responsive tests for mobile-critical features
- Screenshots on failure configured
