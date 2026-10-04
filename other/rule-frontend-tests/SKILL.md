---
name: rule-frontend-tests
description: MANDATORY when editing files matching ["frontend/tests/**/*", "frontend/src/**/*.test.*"]. When writing frontend tests (Jest, RTL, Playwright)
---

# Frontend Tests Rules

## Jest + React Testing Library Stack
ALWAYS use Jest as the test runner and `@testing-library/react` for component rendering. NEVER introduce alternative frameworks (Vitest, Enzyme).

## Accessibility Test Per Component
ALWAYS include a `jest-axe` accessibility scan in every component test suite. MUST use the standard `toHaveNoViolations()` pattern.

Example from codebase:
```tsx
// From frontend/tests/components/manageUsers/InviteLegacyUsersButton.test.tsx
import { axe } from "jest-axe";

it("should not have accessibility violations", async () => {
  const { container } = render(
    <InviteLegacyUsersButton organizationId="org-123" />,
  );
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Selective Snapshot Tests for Complex UI
ALWAYS consider snapshot tests for complex UI (tables, modals). NEVER use snapshots as the only test. ALWAYS pair with behavioral tests.

Example from codebase:
```tsx
// From frontend/tests/components/search/SearchResultsTable.test.tsx
it("matches snapshot", async () => {
  const component = await SearchResultsTable({
    searchResults: [mockOpportunity],
  });
  const { container } = render(component);
  expect(container).toMatchSnapshot();
});
```

## Mock next-intl via Shared intlMocks
ALWAYS mock `next-intl` using `useTranslationsMock()` from `src/utils/testing/intlMocks.ts`. NEVER define custom inline translation mocks.

Example from codebase:
```tsx
// From frontend/tests/components/search/SearchFilters.test.tsx
import { useTranslationsMock } from "src/utils/testing/intlMocks";

jest.mock("next-intl", () => ({
  useTranslations: () => useTranslationsMock(),
}));

// For server components:
jest.mock("next-intl/server", () => ({
  getTranslations: jest.fn(() => useTranslationsMock()),
}));
```

## Mock next/navigation with requireActual
ALWAYS use `jest.requireActual` spread when mocking `next/navigation` to preserve unmocked exports.

Example from codebase:
```tsx
// From frontend/tests/components/search/SearchPagination.test.tsx
jest.mock("next/navigation", () => ({
  ...jest.requireActual<typeof import("next/navigation")>("next/navigation"),
  useRouter: () => ({ push: () => {} }),
  usePathname: () => usePathnameMock() as string,
  useSearchParams: () => new URLSearchParams(),
}));
```

## Mock Auth Session with getSession Pattern
ALWAYS mock `src/services/auth/session` using a `jest.fn()` reference. NEVER import real session logic in unit tests.

Example from codebase:
```tsx
// From frontend/tests/api/organization-invitations/handler.test.ts
const getSessionMock = jest.fn();

jest.mock("src/services/auth/session", () => ({
  getSession: (): unknown => getSessionMock(),
}));

getSessionMock.mockReturnValue({ token: "a token", user_id: "1" });
```

## Type Hacks Accepted in Test Mocks
ALWAYS feel free to use `as unknown` casts and loose typing in `jest.mock` factory functions. NEVER spend excessive time solving complex type issues in test mocks.

Example from codebase:
```tsx
// From frontend/tests/api/organization-invitations/handler.test.ts
jest.mock("src/services/fetch/fetchers/fetchers", () => ({
  fetchUserWithMethod: () => (opts: unknown) =>
    mockUpdateOrganizationInvitation(opts) as unknown,
}));
```

## Mock New Third-Party Libraries
ALWAYS add `jest.mock()` for new third-party dependencies in all affected test files. NEVER leave tests broken by new library imports.

Example from codebase:
```tsx
// From frontend/tests/components/application/ApplyForm.test.tsx
jest.mock("next-navigation-guard", () => ({
  useNavigationGuard: () => jest.fn(),
}));
```

## No Duplicate jest.mock Blocks
NEVER include duplicate `jest.mock()` calls for the same module in a single test file. ALWAYS check for existing mocks before adding new ones.

## Direct Invocation for Async Server Components
ALWAYS test async server components by calling the function directly and passing the result to `render()`. NEVER use JSX syntax for async server components.

Example from codebase:
```tsx
// From frontend/tests/components/manageUsers/InviteLegacyUsersButton.test.tsx
it("confirm the URL is correct", async () => {
  const component = await InviteLegacyUsersButton({ organizationId: "org-123" });
  render(component);
  const link = await screen.findByRole("link");
  expect(link).toHaveAttribute("href", "/organization/org-123/manage-users/legacy");
});
```

## Shared Test Fixtures in fixtures.ts
ALWAYS define reusable mock data in `src/utils/testing/fixtures.ts`. NEVER duplicate large mock objects inline across test files.

Example from codebase:
```tsx
// From frontend/tests/components/search/AgencyFilterAccordion.test.tsx
import { fakeSearchAPIResponse } from "src/utils/testing/fixtures";

const component = await AgencyFilterAccordion({
  agencyOptionsPromise: Promise.resolve([fakeOptions, fakeSearchAPIResponse]),
  query: new Set(),
});
```

## Prefer Role-Based Queries
ALWAYS prefer `screen.getByRole()` / `screen.findByRole()`. Use `screen.getByText()` only when role-based queries are impractical. Use `screen.queryByRole()` for negative assertions.

Example from codebase:
```tsx
// From frontend/tests/components/search/SearchResultsTable.test.tsx
expect(
  screen.getByRole("heading", { name: "title" }),
).toBeInTheDocument();

expect(
  screen.queryByRole("link", { name: "a link" }),
).not.toBeInTheDocument();
```

## Use waitFor for Async State Assertions
ALWAYS use `waitFor` when asserting on state that updates asynchronously. NEVER rely on synchronous assertions for async state.

Example from codebase:
```tsx
// From frontend/tests/components/search/SavedSearchSelect.test.tsx
import { waitFor } from "@testing-library/react";

await waitFor(() => {
  const selectedOption = screen.getByRole("option", { selected: true });
  return expect(selectedOption).toHaveTextContent(fakeSavedSearchRecord.name);
});
```

## Ternary Over && for Conditional Rendering
ALWAYS use ternary operators over `&&` when the condition evaluates to a number (e.g., `.length`).

Example from codebase:
```tsx
// From frontend/src/components/workspace/WorkspacePage.tsx
{userInvitations?.length ? (
  <OrganizationInvitationReplies userInvitations={userInvitations} />
) : (
  <></>
)}
```

## Delete Tests with Components
ALWAYS delete a component's test file in the same PR that deletes the component. NEVER leave orphaned test files.

## Jest Environment Directive for Server Tests
ALWAYS add `@jest-environment node` at the top of test files for API route handlers or server-only code.

Example from codebase:
```typescript
// From frontend/tests/api/organization-invitations/handler.test.ts
/**
 * @jest-environment node
 */
import { updateOrganizationInvitation } from "src/app/api/.../handler";
```

## Always Reset Mocks
ALWAYS include `afterEach(() => jest.resetAllMocks())` in test suites.

## Playwright E2E Tests
ALWAYS use Playwright across Chromium, Firefox, WebKit, and Mobile Chrome. NEVER use Cypress. ALWAYS extract reusable interactions into shared utility files (`searchSpecUtil.ts`, `playwrightUtils.ts`). ALWAYS prefer `data-testid` attributes over CSS class selectors. ALWAYS use `pressSequentially` instead of `fill` for WebKit compatibility. NEVER leave flaky tests running -- use `test.skip()` with a comment and un-skip after fixing. ALWAYS use the Page Object Model pattern for complex form E2E tests.

Example from codebase:
```typescript
// From frontend/e2e/search/search-filters.spec.ts
const subAgencyItems = page.locator('[data-testid="sub-agency-item"]');
```

---

## Context Enrichment

When generating significant frontend test code (new test suite, complex mocking), enrich your context:
- Call `get_rules_for_file("[component being tested]")` from the `simpler-grants-context` MCP server to understand conventions the component should follow
- Call `get_rule_detail("frontend-components")` for component patterns being tested
- Consult **Compound Knowledge** for indexed documentation on test patterns, mock conventions, and fixture usage

## Related Rules

When writing frontend tests, also consult these related rules:
- **`frontend-components.mdc`** — component conventions being tested (RSC default, USWDS, context patterns)
- **`frontend-hooks.mdc`** — hook patterns for hook tests (`useClientFetch`, `useSearchParamUpdater`)
- **`frontend-i18n.mdc`** — i18n patterns for testing translations
- **`frontend-e2e-tests.mdc`** — Playwright E2E test patterns, tagging system, sharding, page object utilities
- **`accessibility.mdc`** — WCAG 2.1 AA / Section 508 compliance, jest-axe test requirements
- **`api-tests.mdc`** — shared testing philosophy (factory patterns, test structure)
- **`cross-domain.mdc`** — accessibility testing requirement (`jest-axe`)

**Debugging:** Invoke the debugging agent (or use `/debug`) to diagnose failing tests — it will trace through the code under test and identify root causes.

## Specialist Validation

When generating or significantly modifying frontend tests:

**For simple changes (adding a single test to existing suite):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new test suite, new mock patterns):**
Invoke `codebase-conventions-reviewer` to validate against frontend test conventions.

**For complex changes (new E2E test flows, Page Object Model, complex async testing):**
Invoke the following specialists (run in parallel where possible):
- `performance-oracle` — validate test efficiency (mock setup cost, unnecessary renders)
- `codebase-conventions-reviewer` — validate mock patterns and test structure
- `kieran-typescript-reviewer` — TypeScript-specific quality review for test code

<!-- Hook enforcement: test-pattern-checker validates testing conventions -->
