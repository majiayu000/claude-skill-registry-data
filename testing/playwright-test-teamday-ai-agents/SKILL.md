---
name: playwright-test
description: Run end-to-end browser tests using the Playwright Test CLI. Create test configs, write spec files with expect assertions, execute tests with npx playwright test, and analyze results. Pre-installed with Chromium in the computer image — no setup needed. Use for E2E testing, regression testing, smoke tests, visual comparisons, and automated QA workflows.
category: code
tags:
  - testing
  - e2e
  - browser
  - playwright
  - qa
allowed-tools: Bash, Read, Write, Edit
---

# Playwright Test CLI

Run end-to-end browser tests using the Playwright Test framework. `@playwright/test` and Chromium are **pre-installed globally** — no setup required.

## Quick Start

**1. Create a config file** in the project root (or working directory):

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    screenshot: 'only-on-failure',
  },
  reporter: [['list'], ['html', { open: 'never' }]],
  retries: 1,
  timeout: 30000,
});
```

**2. Write a test file:**

```typescript
// tests/example.spec.ts
import { test, expect } from '@playwright/test';

test('homepage loads and has title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/My App/);
});

test('navigation works', async ({ page }) => {
  await page.goto('/');
  await page.click('a[href="/about"]');
  await expect(page).toHaveURL(/about/);
});
```

**3. Run tests:**

```bash
npx playwright test
```

## CLI Reference

### Running Tests

```bash
# Run all tests
npx playwright test

# Run a specific test file
npx playwright test tests/login.spec.ts

# Run tests matching a name/regex
npx playwright test -g "login flow"

# Run tests in a specific directory
npx playwright test tests/smoke/

# Run with a specific config
npx playwright test --config=playwright.ci.config.ts
```

### Filtering & Debugging

```bash
# Run only tests tagged with @smoke
npx playwright test --grep @smoke

# Exclude tests tagged @slow
npx playwright test --grep-invert @slow

# Run a specific test by line number
npx playwright test tests/auth.spec.ts:15

# Run in debug mode (step through tests)
npx playwright test --debug

# Run with verbose output
npx playwright test --reporter=list
```

### Execution Control

```bash
# Run tests in parallel (default)
npx playwright test --workers=4

# Run tests serially (useful for debugging)
npx playwright test --workers=1

# Retry failed tests
npx playwright test --retries=2

# Set timeout per test (ms)
npx playwright test --timeout=60000

# Stop on first failure
npx playwright test --max-failures=1
```

### Reporters & Output

```bash
# List reporter (real-time output, good for CI)
npx playwright test --reporter=list

# Line reporter (minimal, one line per test)
npx playwright test --reporter=line

# JSON reporter (machine-readable)
npx playwright test --reporter=json

# HTML report (generates browsable report)
npx playwright test --reporter=html

# Multiple reporters
npx playwright test --reporter=list,html

# JUnit XML (for CI integration)
npx playwright test --reporter=junit
```

### Updating Snapshots

```bash
# Update visual comparison screenshots
npx playwright test --update-snapshots
```

## Test Patterns

### Page Object Model

```typescript
// tests/pages/login.page.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(private page: Page) {
    this.emailInput = page.locator('input[name="email"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/login.page';

test('successful login redirects to dashboard', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto('/login');
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL(/dashboard/);
});
```

### API Testing

```typescript
import { test, expect } from '@playwright/test';

test('API returns valid response', async ({ request }) => {
  const response = await request.get('/api/users');
  expect(response.ok()).toBeTruthy();

  const data = await response.json();
  expect(data.users).toBeInstanceOf(Array);
  expect(data.users.length).toBeGreaterThan(0);
});
```

### Visual Regression

```typescript
test('homepage matches screenshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.01,
  });
});
```

### Test Tags

```typescript
// Tag tests for selective execution
test('login works @smoke', async ({ page }) => { /* ... */ });
test('complex workflow @slow', async ({ page }) => { /* ... */ });

// Run: npx playwright test --grep @smoke
```

### Fixtures

```typescript
import { test as base, expect } from '@playwright/test';

// Extend test with custom fixtures
const test = base.extend<{ authenticatedPage: Page }>({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL(/dashboard/);
    await use(page);
  },
});

test('dashboard shows user name', async ({ authenticatedPage }) => {
  await expect(authenticatedPage.locator('.username')).toContainText('Test User');
});
```

## Config Options

Common `playwright.config.ts` settings:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'list',

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    headless: true,
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
    video: 'retain-on-failure',
  },

  // Multiple browser projects
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['Pixel 5'] } },
  ],

  // Auto-start dev server before tests
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    timeout: 30000,
  },
});
```

## Workflow

When asked to write or run Playwright tests:

1. **Check for existing config** — look for `playwright.config.ts` in the working directory
2. **Create config if missing** — use the Quick Start template, adjust `baseURL` to match the user's app
3. **Create test directory** — `mkdir -p tests`
4. **Write test files** — use `.spec.ts` extension, import from `@playwright/test`
5. **Run tests** — `npx playwright test` with appropriate flags
6. **Report results** — parse output, highlight failures, suggest fixes

## Tips

- **Always use headless mode** — the computer image has no display; `headless: true` is the default
- **Use `baseURL`** — set it in config so tests use relative paths (`page.goto('/')` instead of full URLs)
- **Prefer locators over selectors** — `page.getByRole()`, `page.getByText()`, `page.getByTestId()` are more resilient
- **Use `expect` auto-waiting** — Playwright assertions auto-retry, so `await expect(locator).toBeVisible()` waits automatically
- **Capture traces on failure** — set `trace: 'on-first-retry'` in config for debugging failed tests
- **Only Chromium is available** — don't configure Firefox or WebKit projects; only `chromium` is installed
