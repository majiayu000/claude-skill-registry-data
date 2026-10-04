---
name: rule-frontend-e2e-tests
description: MANDATORY when editing files matching ["frontend/tests/e2e/**/*"]. When working on Playwright E2E tests in frontend/tests/e2e/
---

# Frontend E2E Tests Rules

## Test Tagging — Execution Tags (Required)

EVERY test MUST have exactly ONE execution tag. These control when the test runs in CI:

- `@smoke` — Runs on every PR (local environment)
- `@core-regression` — Runs on merge to main (local + staging)
- `@full-regression` — Runs daily at 6-7am EST (local + staging)
- `@extended` — Runs weekly on Sundays (local + staging)

NEVER create a test without an execution tag. NEVER assign multiple execution tags to a single test.

Example from codebase:
```typescript
// From frontend/tests/e2e/search/search.spec.ts
test("@smoke @grantee @opportunity-search should display search results", async ({ page }) => {
  // Test implementation
});
```

## Test Tagging — Feature Tags (Optional)

Feature tags are optional and categorize tests by domain:
- `@grantor` — Grantor-facing functionality
- `@grantee` — Grantee-facing functionality
- `@opportunity-search` — Search and discovery
- `@apply` — Application submission
- `@static` — Static content pages
- `@auth` — Authentication flows
- `@user-management` — User/org management

ALWAYS define tags in `frontend/tests/e2e/tags.ts`. NEVER use ad-hoc tag strings — always reference the centralized enum.

## Test File Naming

ALWAYS use `happy-path-*.spec.ts` for positive/success path tests. ALWAYS use `failure-path-*.spec.ts` for negative/error path tests. NEVER mix happy and failure paths in the same spec file for complex features.

Example from codebase:
```
frontend/tests/e2e/apply/
  happy-path-submit-application.spec.ts
  failure-path-validation-errors.spec.ts
  application-submission-validation.spec.ts
```

## Directory Organization

ALWAYS organize tests by feature area in subdirectories. NEVER place all tests in the root e2e directory.

```
frontend/tests/e2e/
  tags.ts                          # Centralized tag definitions
  login.spec.ts                    # Auth tests
  search/                          # Search feature tests
    search.spec.ts
    search-results.spec.ts
    search-filters.spec.ts
    searchSpecUtil.ts              # Feature-specific utilities
  apply/                           # Application feature tests
    happy-path-*.spec.ts
    failure-path-*.spec.ts
    fixtures/                      # Test data fixtures
    utils/                         # Feature-specific helpers
  saved-opportunities/             # Saved opportunities tests
```

## Page Object Pattern — Utility Functions

ALWAYS use utility-based page object patterns (exported functions), NOT OOP class-based page objects. ALWAYS place shared utilities in a `utils/` subdirectory within the feature directory or in the root `utils/` directory.

Example from codebase:
```typescript
// From frontend/tests/e2e/utils/authenticate-e2e-user-utils.ts
export async function authenticateUser(page: Page, credentials: UserCredentials) {
  await page.goto("/login");
  await page.fill('[name="email"]', credentials.email);
  await page.fill('[name="password"]', credentials.password);
  await page.click('button[type="submit"]');
  await page.waitForURL("/dashboard");
}
```

## Shared Test Utilities

ALWAYS place cross-feature utilities in `frontend/tests/e2e/utils/`. ALWAYS place feature-specific utilities adjacent to their tests. NEVER duplicate utility logic across feature directories.

Key shared utilities:
- `authenticate-e2e-user-utils.ts` — Authentication helpers
- `create-application-utils.ts` — Application creation helpers
- `submit-application-utils.ts` — Submission flow helpers
- Feature-specific: `searchSpecUtil.ts`, `general-forms-filling.ts`, etc.

## Test Data and Fixtures

ALWAYS use dedicated fixture files for complex test data. ALWAYS place fixtures in a `fixtures/` subdirectory within the feature directory. NEVER hardcode large test data structures inline in spec files.

## Playwright Configuration Awareness

Be aware of environment-specific Playwright settings:
- **Timeouts:** 75s (local), 120s (staging/prod)
- **Parallelism:** `fullyParallel: true` (local), `false` (staging)
- **Workers:** 10 default, configurable via `PLAYWRIGHT_WORKERS`
- **Retries:** 0 (local), 3 (CI)
- **Sharding:** 4 shards via `TOTAL_SHARDS`/`CURRENT_SHARD`
- **Browsers:** Chrome + Firefox + Safari (local), Chrome + Mobile Chrome (staging)
- **Reporter:** HTML (local), blob (CI, for merged reports)

NEVER write tests that assume specific timeout values — use Playwright's built-in waiting mechanisms.

## BDD Feature Files

Tests MAY include BDD `.feature` files (Gherkin syntax) alongside `.spec.ts` files. When present, the spec file implements the scenarios defined in the feature file.

## Assertions

ALWAYS use Playwright's built-in assertions (`expect(locator).toBeVisible()`, etc.) over manual checks. NEVER use `page.waitForTimeout()` — use `page.waitForSelector()` or other event-driven waits.

---

## Context Enrichment

When generating significant E2E test code (new test suite, new page object utility, new feature tests), enrich your context:
- Call `get_architecture_section("frontend")` from the `simpler-grants-context` MCP server to understand frontend architecture
- Call `get_rule_detail("frontend-tests")` for Jest/RTL unit test patterns (complementary to E2E)
- Call `get_rule_detail("frontend-app-pages")` for page structure that tests exercise
- Consult **Compound Knowledge** for indexed documentation on E2E patterns

## Related Rules

When working on E2E tests, also consult these related rules:
- **`frontend-tests.mdc`** — Jest/RTL unit test patterns (complementary, not overlapping)
- **`frontend-app-pages.mdc`** — page structure and routes being tested
- **`frontend-components.mdc`** — component patterns and ARIA attributes used in selectors
- **`accessibility.mdc`** — accessibility requirements that E2E tests should verify
- **`ci-cd.mdc`** — CI workflow integration for E2E test execution and sharding

## Specialist Validation

When generating or significantly modifying E2E test code:

**For simple changes (< 20 lines, adding an assertion, updating a selector):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new spec file, new page object utility):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new feature test suite, test infrastructure changes):**
Invoke the following specialists (run in parallel where possible):
- `code-simplicity-reviewer` — check for unnecessary complexity in test utilities
- `kieran-typescript-reviewer` — TypeScript-specific quality review
