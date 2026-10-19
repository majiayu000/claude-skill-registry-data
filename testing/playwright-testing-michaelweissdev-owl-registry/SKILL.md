---
name: playwright-testing
description: >
  Author, execute, and maintain end-to-end (E2E) web integration tests using Playwright.
  Use when designing Page Object Models (POM), authoring resilient user-visible locators
  (getByRole, getByText), configuring auto-waiting assertions, intercepting and mocking
  network traffic, persisting authenticated storageState, analyzing execution traces,
  or configuring cross-browser CI pipelines.
compatibility: >
  Agent Skills-compatible coding agents with access to Node.js/TypeScript or Python
  runtimes and Playwright test runners. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "playwright, testing, e2e, pom, locators, auto-waiting, fixtures, network-mocking, trace-viewer, browser"
  topics: "testing"
---

# Playwright End-to-End Testing Engineering

Playwright is a modern automation and end-to-end testing framework for web applications across Chromium, WebKit, and Firefox. Reliable test suites prioritize user-visible behaviors, isolate authentication sessions, and eliminate flakiness through built-in auto-waiting assertions and tracing artifacts.

## Purpose & Overview

Flaky end-to-end tests degrade engineering velocity, erode trust in deployment pipelines, and mask real regressions. Common causes of flakiness include arbitrary sleep timers, brittle CSS/XPath selectors, unisolated global browser state, and unhandled asynchronous network transitions.

This skill equips agents with standards and techniques to:
- Structure scalable test suites using the **Page Object Model (POM)** and custom test fixtures.
- Target elements using **user-visible semantic locators** (`getByRole`, `getByLabel`, `getByText`) rather than brittle DOM hierarchy.
- Rely on Playwright's **auto-waiting and web-first assertion retries** instead of manual sleep intervals.
- Mock external APIs, simulate error conditions, and modify network payloads using route interception (`page.route`).
- Manage test authentication efficiently by reusing **`storageState` session cookies and tokens** across suites.
- Diagnose and debug failures using the **Playwright Trace Viewer**, video recordings, and network HAR archives.
- Execute cross-browser and parallel test suites reliably in headless CI environments with test sharding.

---

## Core Principles & Rules

1. **Prioritize User-Visible Locators**: Locate elements the way users and assistive technology interact with them. Always prefer `getByRole`, `getByLabel`, `getByPlaceholder`, or `getByText` over brittle CSS classes (e.g., `.btn-primary.sc-1a2b3`) or implementation-dependent XPath.
2. **Never Use Arbitrary Delays (`page.waitForTimeout`)**: Manual sleeps guarantee slow test suites and eventual race condition failures. Always assert on state with auto-retrying web-first matchers (`await expect(locator).toBeVisible()`).
3. **Isolate State via Fixtures and `storageState`**: Never execute tests that depend on the state left behind by a previous test. Authenticate once via an authentication setup dependency or fixture, saving cookies and local storage into a `storageState` file.
4. **Enforce Single Responsibility in Page Objects**: Page objects should encapsulate element discovery and interaction logic. Page objects must return promises or locators; they should avoid hardcoding business assertions that belong in test specifications.
5. **Intercept, Don't Break, the Network**: When mocking third-party integrations (e.g., payment gateways, analytics), mock at the browser network boundary using `page.route()`, fulfilling realistic JSON schemas.
6. **Capture Diagnostic Traces on Failure**: Configure `trace: 'on-first-retry'` or `'retain-on-failure'` in production CI to inspect DOM snapshots, console logs, and network requests without adding overhead to successful runs.

---

## Standard Workflows & Procedures

### Workflow 1: Designing Page Object Models (POM)

1. **Define the Page Class**: Encapsulate locators as readonly properties and user actions as async methods.
   ```typescript
   // pages/LoginPage.ts
   import { type Locator, type Page } from '@playwright/test';

   export class LoginPage {
     readonly page: Page;
     readonly usernameInput: Locator;
     readonly passwordInput: Locator;
     readonly submitButton: Locator;
     readonly errorMessage: Locator;

     constructor(page: Page) {
       this.page = page;
       this.usernameInput = page.getByLabel('Username');
       this.passwordInput = page.getByLabel('Password');
       this.submitButton = page.getByRole('button', { name: 'Sign In' });
       this.errorMessage = page.getByRole('alert');
     }

     async goto() {
       await this.page.goto('/login');
     }

     async login(username: string, password: string) {
       await this.usernameInput.fill(username);
       await this.passwordInput.fill(password);
       await this.submitButton.click();
     }
   }
   ```
2. **Author the Test Specification**: Keep test specs declarative, focusing on user journeys and verification.
   ```typescript
   // tests/auth/login.spec.ts
   import { test, expect } from '@playwright/test';
   import { LoginPage } from '../../pages/LoginPage';

   test.describe('Authentication Flow', () => {
     test('rejects invalid credentials with an error alert', async ({ page }) => {
       const loginPage = new LoginPage(page);
       await loginPage.goto();
       await loginPage.login('invalid-user', 'wrong-pass');

       await expect(loginPage.errorMessage).toBeVisible();
       await expect(loginPage.errorMessage).toContainText('Invalid username or password');
     });
   });
   ```

### Workflow 2: Authenticated Session Re-use (`storageState`)

Instead of logging in through UI forms in every test (which drastically slows down execution), log in once in an authentication setup step and share the state file.

```
┌─────────────────────────────────┐
│ auth.setup.ts                   │
│ Logs in once & writes state     │
└───────────────┬─────────────────┘
                │
                ▼ writes .auth/user.json
┌───────────────────────────────────────────────┐
│ playwright.config.ts                          │
│ Projects depend on 'setup', load storageState │
└───────┬───────────────────────────────┬───────┘
        │                               │
        ▼                               ▼
┌──────────────────┐            ┌──────────────────┐
│ checkout.spec.ts │            │ settings.spec.ts │
│ (Pre-authenticated)           │ (Pre-authenticated)
└──────────────────┘            └──────────────────┘
```

1. **Configure Setup Project in `playwright.config.ts`**:
   ```typescript
   import { defineConfig, devices } from '@playwright/test';

   export default defineConfig({
     testDir: './tests',
     projects: [
       { name: 'setup', testMatch: /.*\.setup\.ts/ },
       {
         name: 'chromium',
         use: {
           ...devices['Desktop Chrome'],
           storageState: '.auth/user.json',
         },
         dependencies: ['setup'],
       },
     ],
   });
   ```

2. **Implement `tests/auth.setup.ts`**:
   ```typescript
   import { test as setup, expect } from '@playwright/test';

   const authFile = '.auth/user.json';

   setup('authenticate user session', async ({ page }) => {
     await page.goto('/login');
     await page.getByLabel('Username').fill(process.env.TEST_USER_EMAIL || 'test@example.com');
     await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD || 'secret');
     await page.getByRole('button', { name: 'Sign In' }).click();

     // Wait until redirect or authenticated element confirms successful login
     await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

     // Save session cookies and localStorage to disk
     await page.context().storageState({ path: authFile });
   });
   ```

### Workflow 3: Network Interception and Mocking

Use `page.route` to mock slow, unreliable, or paid third-party APIs without altering backend application code.

```typescript
test('displays fallback banner when inventory service returns 500', async ({ page }) => {
  // Intercept GET requests matching the inventory API route
  await page.route('**/api/v1/inventory/*', async (route) => {
    await route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'Service Unavailable' }),
    });
  });

  await page.goto('/products/widget-pro');
  
  const statusBanner = page.getByRole('status');
  await expect(statusBanner).toBeVisible();
  await expect(statusBanner).toHaveText('Inventory information currently unavailable.');
});
```

---

## Real-World Examples & Patterns

### Pattern 1: Custom Test Fixtures with Dependency Injection

Custom fixtures extend the base `test` runner, instantiating page objects and state automatically per test and tearing them down cleanly.

```typescript
// fixtures/baseFixture.ts
import { test as baseTest, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

type CustomFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
};

export const test = baseTest.extend<CustomFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },
  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },
});

export { expect };
```

Usage in test specifications:
```typescript
import { test, expect } from '../fixtures/baseFixture';

test('navigates to user profile from dashboard', async ({ dashboardPage, page }) => {
  await dashboardPage.goto();
  await dashboardPage.openProfileMenu();
  await expect(page).toHaveURL(/\/profile/);
});
```

### Pattern 2: Asserting Asynchronous UI Transitions and Lists

```typescript
test('filters and orders product items dynamically', async ({ page }) => {
  await page.goto('/shop');

  const filterSelect = page.getByLabel('Category Filter');
  await filterSelect.selectOption('Electronics');

  const productCards = page.getByTestId('product-card');

  // Web-first assertion automatically polls until count condition is fulfilled
  await expect(productCards).toHaveCount(4);

  // Assert on item text list values in deterministic order
  await expect(productCards.getByRole('heading')).toHaveText([
    'Wireless Headphones',
    'USB-C Microphone',
    'Mechanical Keyboard',
    '4K Display Monitor',
  ]);
});
```

### Pattern 3: Playwright CI Pipeline Configuration

A production GitHub Actions workflow executing Playwright with parallel sharding and trace retention:

```yaml
name: Playwright E2E Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 30
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright Browsers with OS dependencies
        run: npx playwright install --with-deps chromium
      - name: Run Playwright Tests with Sharding
        run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
      - name: Upload Playwright Report & Traces
        uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report-${{ matrix.shardIndex }}
          path: playwright-report/
          retention-days: 7
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Operational Hazard | Correct Engineering Approach |
|:---|:---|:---|
| **Using `page.waitForTimeout(5000)`** | Tests run needlessly slow and intermittently fail when network or CPU latency fluctuates. | Use web-first assertions like `await expect(locator).toBeVisible()` which auto-poll. |
| **Selecting via deep CSS or generated classes** | E.g. `div.css-1r8g4b > div:nth-child(3)` breaks whenever styling or DOM wrappers change. | Use semantic locators: `page.getByRole('button', { name: 'Submit' })`. |
| **Re-authenticating through UI in every test** | Wastes 5-15 seconds per test file, multiplying CI run times exponentially. | Authenticate once using setup dependencies and load serialized `storageState`. |
| **Asserting without `await`** | Writing `expect(locator.isVisible())` evaluates synchronously, causing unhandled promise rejections or false positives. | Always `await expect(locator).toBeVisible()`. |
| **Leaking state across parallel test workers** | Modifying shared database rows or global tenant settings without unique identifiers creates race conditions. | Isolate test datasets using unique identifiers (e.g. `test-${Date.now()}@example.com`). |
| **Uncaptured failure diagnostics** | CI jobs fail with opaque timeouts, giving no visibility into UI state. | Enable trace capture on failure (`trace: 'retain-on-failure'`) and inspect with `npx playwright show-trace`. |

---

## Verification Checklist

- [ ] All element selectors use semantic user-visible locators (`getByRole`, `getByText`, `getByLabel`, `getByTestId`).
- [ ] No occurrences of `page.waitForTimeout()` remain in the test codebase.
- [ ] Assertions use auto-retrying web-first matchers (`expect(locator).toBeVisible()`, `toHaveText()`, `toBeEnabled()`).
- [ ] Page Object Models cleanly encapsulate element definitions and actions without embedded assertions.
- [ ] Reusable authenticated sessions are managed via `storageState` rather than redundant UI logins.
- [ ] Network mocks (`page.route()`) unroute or isolate handlers per test to prevent cross-test leakage.
- [ ] `playwright.config.ts` is configured with `trace: 'on-first-retry'` or `'retain-on-failure'`.
- [ ] CI pipeline executes headless browsers with appropriate sharding and artifact uploading.

---

## Tooling & Reference Guides

- **Playwright Test Runner Documentation**: Canonical guide and API reference ([playwright.dev](https://playwright.dev)).
- **Playwright Trace Viewer**: Interactive post-mortem debugger for DOM snapshots, console logs, and network events (`npx playwright show-trace trace.zip`).
- **Playwright Codegen**: Interactive element locator and script generator (`npx playwright codegen http://localhost:3000`).
- **Aria Roles Reference**: Accessible Rich Internet Applications (W3C ARIA) role specifications used for `getByRole` selectors.
