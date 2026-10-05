---
name: e2e-testing-automation
description: End-to-end testing automation with Playwright, Cypress, and Selenium including page objects, visual regression, and CI integration. Use when implementing.
---

# E2E Testing Automation

Comprehensive guidance for implementing end-to-end browser testing using modern frameworks. Covers framework selection, page object patterns, waiting strategies, visual regression, API mocking, authentication fixtures, parallel execution, CI/CD integration, flaky test management, and accessibility testing.

## When to Use This Skill

Use this skill for:

- Choosing between Playwright, Cypress, and Selenium for a project
- Implementing the page object model for maintainable test suites
- Writing reliable selectors using data-testid and ARIA roles
- Configuring auto-wait and explicit wait strategies to eliminate flakiness
- Setting up visual regression testing with screenshot comparison
- Mocking or intercepting API responses in browser tests
- Handling authentication in E2E tests without repeated login flows
- Running tests in parallel across multiple browsers
- Integrating E2E tests into CI/CD pipelines (GitHub Actions, GitLab CI)
- Diagnosing and fixing flaky tests
- Adding accessibility checks to existing E2E suites

**Trigger phrases**: "E2E testing", "end-to-end test", "Playwright", "Cypress", "Selenium", "page object", "visual regression", "flaky test", "browser testing", "test automation", "data-testid", "accessibility testing"

## What This Skill Does

Provides production-ready E2E testing patterns including:

- **Framework Selection**: Decision matrix for Playwright vs Cypress vs Selenium
- **Architecture**: Page object model, test fixtures, configuration management
- **Selectors**: Priority hierarchy (ARIA roles, data-testid, CSS, XPath)
- **Reliability**: Auto-wait, retry strategies, network idle detection
- **Visual Testing**: Screenshot comparison, threshold tuning, baseline management
- **CI Integration**: Pipeline configs, parallelization, artifact collection
- **Debugging**: Trace viewers, video recording, flaky test quarantine

## Instructions

### Step 1: Select the Right Framework

**Framework Decision Matrix**:

| Feature | Playwright | Cypress | Selenium |
|---------|-----------|---------|----------|
| Language support | JS/TS, Python, Java, C# | JS/TS only | All major languages |
| Browser support | Chromium, Firefox, WebKit | Chromium, Firefox, WebKit | All browsers |
| Auto-wait | Built-in | Built-in | Manual |
| Network interception | Native | Native | Requires proxy |
| Multi-tab/window | Yes | Limited | Yes |
| iframes | Easy | Difficult | Moderate |
| Parallel execution | Built-in | Via CI parallelization | Grid/Selenoid |
| Mobile emulation | Device profiles | Viewport only | Appium integration |
| Speed | Fast | Fast | Moderate |
| Debugging | Trace viewer, codegen | Time-travel debugger | Logs only |

**Recommendation**: Use Playwright for new projects. It provides the best combination of speed, reliability, cross-browser support, and developer experience.

### Step 2: Set Up Playwright Project

**Installation and Configuration**:

```bash
# Initialize Playwright project
npm init playwright@latest

# Project structure after setup:
# tests/
#   example.spec.ts
# playwright.config.ts
# package.json
```

**Playwright Configuration** (`playwright.config.ts`):

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  outputDir: './test-results',

  /* Fail the build on CI if test.only is left in source */
  forbidOnly: !!process.env.CI,

  /* Retry flaky tests in CI only */
  retries: process.env.CI ? 2 : 0,

  /* Parallel workers */
  workers: process.env.CI ? 4 : undefined,

  /* Shared settings for all projects */
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',       // Capture trace on failure
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10_000,
    navigationTimeout: 30_000,
  },

  /* Reporter configuration */
  reporter: process.env.CI
    ? [['html', { open: 'never' }], ['junit', { outputFile: 'results.xml' }]]
    : [['html', { open: 'on-failure' }]],

  /* Browser projects */
  projects: [
    // Desktop browsers
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },

    // Mobile viewports
    { name: 'mobile-chrome', use: { ...devices['Pixel 7'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 14'] } },
  ],

  /* Local dev server */
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
```

### Step 3: Implement the Page Object Model

Page objects encapsulate page-specific selectors and actions, making tests resilient to UI changes.

**Base Page Object**:

```typescript
// tests/pages/base.page.ts
import { Page, Locator } from '@playwright/test';

export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  /* Navigation helpers */
  async goto(path: string): Promise<void> {
    await this.page.goto(path);
  }

  async waitForPageLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }

  /* Common element interactions */
  async clickAndWait(locator: Locator): Promise<void> {
    await locator.click();
    await this.page.waitForLoadState('domcontentloaded');
  }

  /* Toast / notification helpers */
  async getToastMessage(): Promise<string> {
    const toast = this.page.getByRole('alert');
    await toast.waitFor({ state: 'visible' });
    return toast.textContent() ?? '';
  }
}
```

**Login Page Object**:

```typescript
// tests/pages/login.page.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './base.page';

export class LoginPage extends BasePage {
  /* Selectors: prefer role-based and data-testid locators */
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByTestId('login-error');
    this.forgotPasswordLink = page.getByRole('link', { name: 'Forgot password' });
  }

  async navigate(): Promise<void> {
    await this.goto('/login');
  }

  async login(email: string, password: string): Promise<void> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectErrorVisible(message: string): Promise<void> {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toContainText(message);
  }
}
```

**Dashboard Page Object**:

```typescript
// tests/pages/dashboard.page.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './base.page';

export class DashboardPage extends BasePage {
  readonly heading: Locator;
  readonly orderTable: Locator;
  readonly searchInput: Locator;
  readonly filterDropdown: Locator;
  readonly exportButton: Locator;

  constructor(page: Page) {
    super(page);
    this.heading = page.getByRole('heading', { name: 'Dashboard' });
    this.orderTable = page.getByRole('table', { name: 'Orders' });
    this.searchInput = page.getByPlaceholder('Search orders...');
    this.filterDropdown = page.getByTestId('status-filter');
    this.exportButton = page.getByRole('button', { name: 'Export' });
  }

  async navigate(): Promise<void> {
    await this.goto('/dashboard');
  }

  async searchOrders(query: string): Promise<void> {
    await this.searchInput.fill(query);
    // Wait for debounced search to trigger and table to update
    await this.page.waitForResponse(resp =>
      resp.url().includes('/api/orders') && resp.status() === 200
    );
  }

  async getOrderCount(): Promise<number> {
    const rows = this.orderTable.getByRole('row');
    // Subtract 1 for the header row
    return (await rows.count()) - 1;
  }

  async filterByStatus(status: string): Promise<void> {
    await this.filterDropdown.selectOption(status);
    await this.page.waitForLoadState('networkidle');
  }
}
```

### Step 4: Write Reliable Selectors

**Selector Priority Hierarchy** (most resilient to least):

```typescript
// 1. ARIA roles (best: tied to accessibility semantics)
page.getByRole('button', { name: 'Submit' });
page.getByRole('heading', { name: 'Dashboard', level: 1 });
page.getByRole('link', { name: 'Sign out' });
page.getByRole('textbox', { name: 'Email' });

// 2. Accessible labels
page.getByLabel('Email address');
page.getByPlaceholder('Search...');
page.getByAltText('Company logo');
page.getByTitle('Close dialog');

// 3. data-testid (stable, decoupled from UI text)
page.getByTestId('order-total');
page.getByTestId('submit-payment');

// 4. Text content (fragile if text changes frequently)
page.getByText('Welcome back');
page.getByText(/total: \$[\d.]+/i);

// 5. CSS selectors (last resort)
page.locator('.order-card >> nth=0');
page.locator('#main-content');

// AVOID: XPath (brittle, hard to read)
// page.locator('xpath=//div[@class="card"]/span[2]');
```

### Step 5: Handle Waiting Strategies

**Playwright Auto-Wait** (built-in, handles most cases):

```typescript
// Playwright automatically waits for elements to be:
// - Attached to DOM
// - Visible
// - Stable (not animating)
// - Enabled
// - Receiving events
await page.getByRole('button', { name: 'Submit' }).click();
// No explicit wait needed; Playwright retries until actionable
```

**Explicit Waits for Complex Scenarios**:

```typescript
// Wait for a specific API response
const responsePromise = page.waitForResponse(
  resp => resp.url().includes('/api/orders') && resp.status() === 200
);
await page.getByRole('button', { name: 'Load orders' }).click();
const response = await responsePromise;
const data = await response.json();

// Wait for element state
await page.getByTestId('loading-spinner').waitFor({ state: 'hidden' });

// Wait for a specific number of elements
await expect(page.getByTestId('order-row')).toHaveCount(10);

// Wait for navigation
await Promise.all([
  page.waitForURL('**/dashboard'),
  page.getByRole('button', { name: 'Sign in' }).click(),
]);
```

### Step 6: Implement Visual Regression Testing

**Playwright Visual Comparisons**:

```typescript
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('dashboard renders correctly', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');

    // Full-page screenshot comparison
    await expect(page).toHaveScreenshot('dashboard-full.png', {
      fullPage: true,
      maxDiffPixelRatio: 0.01,  // Allow 1% pixel difference
    });
  });

  test('order card component renders correctly', async ({ page }) => {
    await page.goto('/dashboard');

    // Component-level screenshot
    const orderCard = page.getByTestId('order-card').first();
    await expect(orderCard).toHaveScreenshot('order-card.png', {
      maxDiffPixels: 50,  // Allow up to 50 pixels difference
    });
  });

  test('responsive layout at mobile width', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/dashboard');

    await expect(page).toHaveScreenshot('dashboard-mobile.png', {
      fullPage: true,
    });
  });
});
```

**Updating Baselines**:

```bash
# Update all visual snapshots after intentional UI changes
npx playwright test --update-snapshots

# Update snapshots for a specific test file
npx playwright test tests/visual.spec.ts --update-snapshots
```

### Step 7: Mock and Intercept API Calls

```typescript
import { test, expect } from '@playwright/test';

test.describe('API Mocking', () => {
  test('displays orders from mocked API', async ({ page }) => {
    // Intercept the API call and return mock data
    await page.route('**/api/orders*', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          orders: [
            { id: '1', total: 99.99, status: 'pending' },
            { id: '2', total: 149.50, status: 'shipped' },
          ],
          total: 2,
        }),
      });
    });

    await page.goto('/dashboard');
    await expect(page.getByTestId('order-row')).toHaveCount(2);
  });

  test('handles API error gracefully', async ({ page }) => {
    await page.route('**/api/orders*', (route) =>
      route.fulfill({ status: 500, body: 'Internal Server Error' })
    );

    await page.goto('/dashboard');
    await expect(page.getByText('Failed to load orders')).toBeVisible();
  });

  test('modifies real API response', async ({ page }) => {
    await page.route('**/api/orders*', async (route) => {
      const response = await route.fetch();  // Forward to real server
      const json = await response.json();
      json.orders[0].status = 'cancelled';   // Modify one field
      await route.fulfill({ response, json });
    });

    await page.goto('/dashboard');
    await expect(page.getByText('cancelled')).toBeVisible();
  });
});
```

### Step 8: Handle Authentication Efficiently

**Storage State Pattern** (login once, reuse across tests):

```typescript
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const AUTH_FILE = 'tests/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('securepassword');
  await page.getByRole('button', { name: 'Sign in' }).click();

  // Wait for redirect to dashboard after login
  await page.waitForURL('**/dashboard');
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

  // Save authentication state (cookies, localStorage)
  await page.context().storageState({ path: AUTH_FILE });
});
```

**Use Saved Auth in Tests**:

```typescript
// playwright.config.ts (add setup project and dependency)
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'tests/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

**API-Based Authentication** (faster, no browser login):

```typescript
// tests/fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';

type AuthFixture = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixture>({
  authenticatedPage: async ({ page, request }, use) => {
    // Get auth token via API (no browser login flow)
    const response = await request.post('/api/auth/login', {
      data: { email: 'test@example.com', password: 'securepassword' },
    });
    const { token } = await response.json();

    // Inject token into browser context
    await page.goto('/');
    await page.evaluate((t) => {
      localStorage.setItem('auth_token', t);
    }, token);

    await use(page);
  },
});
```

### Step 9: Integrate into CI/CD

**GitHub Actions Pipeline**:

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium firefox

      - name: Build application
        run: npm run build

      - name: Run E2E tests
        run: npx playwright test --shard=${{ matrix.shard }}/${{ strategy.job-total }}
        env:
          BASE_URL: http://localhost:3000
          CI: true

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report-${{ matrix.shard }}
          path: |
            playwright-report/
            test-results/
          retention-days: 14

      - name: Upload test results to PR
        if: always() && github.event_name == 'pull_request'
        uses: daun/playwright-report-summary@v3
        with:
          report-file: results.xml

    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
```

### Step 10: Manage Flaky Tests

**Flaky Test Identification and Quarantine**:

```typescript
// Tag known flaky tests for separate tracking
test.describe('Flaky Test Quarantine', () => {
  // Mark as flaky: will retry up to 3 times before failing
  test('intermittent WebSocket connection', {
    tag: '@flaky',
    retries: 3,
  }, async ({ page }) => {
    // Test implementation
  });
});

// Run only non-flaky tests in the main pipeline
// npx playwright test --grep-invert @flaky

// Run flaky tests separately for monitoring
// npx playwright test --grep @flaky
```

**Common Flaky Test Causes and Fixes**:

| Cause | Symptom | Fix |
|-------|---------|-----|
| Race condition | Passes locally, fails in CI | Add explicit waits for API responses |
| Animation timing | Element not clickable | Wait for animation end or disable animations |
| Shared test state | Order-dependent failures | Reset state in beforeEach, use isolated contexts |
| Network latency in CI | Timeout errors | Increase timeouts, mock slow endpoints |
| Time-dependent logic | Fails at month/year boundaries | Mock `Date.now()` or use fixed test dates |

### Step 11: Add Accessibility Testing

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('dashboard has no WCAG violations', async ({ page }) => {
    await page.goto('/dashboard');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .exclude('.third-party-widget')  // Exclude elements you cannot control
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('login form is keyboard navigable', async ({ page }) => {
    await page.goto('/login');

    // Tab through form elements
    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Email')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Password')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Sign in' })).toBeFocused();

    // Submit with Enter
    await page.keyboard.press('Enter');
  });
});
```

## Best Practices

- **Prefer role-based selectors**: `getByRole` ties tests to accessibility semantics, improving both test resilience and a11y
- **One assertion per logical check**: Keep tests focused on a single user flow or behavior
- **Never use hard-coded waits**: Replace `page.waitForTimeout(3000)` with event-based waits
- **Use page objects for all pages**: Centralizes selector maintenance when UI changes
- **Mock external services**: Do not depend on third-party APIs in E2E tests
- **Run in CI on every PR**: Catch regressions before merge, not after
- **Record traces on failure**: Playwright traces provide full replay for debugging
- **Parallelize with sharding**: Split tests across CI workers for faster feedback
- **Quarantine flaky tests**: Do not let flaky tests block the main pipeline
- **Test critical paths first**: Login, checkout, and core CRUD flows before edge cases

## Quality Checklist

- [ ] Framework selected with documented rationale
- [ ] Page object model implemented for all tested pages
- [ ] Selectors use ARIA roles or data-testid (no fragile CSS/XPath)
- [ ] Authentication handled via storage state or API fixtures
- [ ] Visual regression baselines established and reviewed
- [ ] API mocking covers error states and edge cases
- [ ] Tests run in CI on every pull request
- [ ] Parallel execution configured (sharding or multiple workers)
- [ ] Test artifacts (traces, screenshots, video) uploaded on failure
- [ ] Flaky tests identified, tagged, and tracked separately
- [ ] Accessibility checks (axe-core) included in the test suite
- [ ] All tests pass consistently across Chromium, Firefox, and WebKit

## Related Skills

- `unit-tests` - Unit testing for individual functions and components
- `test-cases` - Integration and API testing patterns
- `cicd-architect` - CI/CD pipeline design for test automation
- `code-coverage` - Measuring and improving test coverage
- `performance-testing` - Load testing and performance benchmarking

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
