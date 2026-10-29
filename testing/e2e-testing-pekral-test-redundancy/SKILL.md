---
name: e2e-testing
description: "Use when writing or stabilizing Playwright end-to-end browser tests against a Laravel app — but only when the project already has Playwright; otherwise defer to manual testing or Pest/Dusk."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/code-testing/general.md` for the deterministic-test contract: tests must be reliable, isolated, and free of arbitrary sleeps.
- GATED skill: proceed only when the consuming project already ships Playwright. Never install Playwright unprompted.
- Stable selectors over brittle ones: prefer role and `data-testid` over CSS/structure.
- No arbitrary `waitForTimeout`. Rely on auto-waiting locators and explicit conditions.
- Every completed E2E scenario must leave a repeatable artifact that identifies the scenario and outcome: keep the configured trace, screenshot/video, JUnit result, or an equivalent generated report.

## Use when
- Writing Playwright E2E browser tests for a Laravel app.
- Stabilizing flaky Playwright tests.
- Wiring Playwright into CI against the app under test.

## Preconditions (run first, do not skip)
Check whether Playwright is actually present:

```bash
ls playwright.config.* 2>/dev/null
grep -q '@playwright/test' package.json 2>/dev/null && echo "playwright present"
```

- If neither a `playwright.config.*` file nor `@playwright/test` in `package.json` exists, STOP. Do not install Playwright. Defer to manual, scenario-based testing, or Pest feature tests / Laravel Dusk for browser coverage inside the PHP stack.
- Only when Playwright IS present, continue with the patterns below.

## File organization
```
tests/
  e2e/
    auth/login.spec.ts
    features/search.spec.ts
  pages/
    ItemsPage.ts
  fixtures/
    auth.ts
playwright.config.ts
```

## Page Object Model
Encapsulate page structure so specs read as behavior, not selectors.

```typescript
import { Page, Locator } from '@playwright/test'

export class ItemsPage {
  readonly page: Page
  readonly searchInput: Locator
  readonly itemCards: Locator
  readonly createButton: Locator

  constructor(page: Page) {
    this.page = page
    // Prefer role/test-id selectors. data-testid is stable across restyles.
    this.searchInput = page.getByTestId('search-input')
    this.itemCards = page.getByTestId('item-card')
    this.createButton = page.getByRole('button', { name: 'Create' })
  }

  async goto() {
    await this.page.goto('/items')
  }

  async search(query: string) {
    await this.searchInput.fill(query)
    // Wait for the real response, not a fixed delay.
    await this.page.waitForResponse(r => r.url().includes('/items') && r.ok())
  }

  itemCount() {
    return this.itemCards.count()
  }
}
```

## Stable selectors
Order of preference:
1. `getByRole(...)` with an accessible name.
2. `getByTestId(...)` — add `data-testid` to the relevant Blade/Livewire markup.
3. `getByLabel` / `getByText` for forms and copy.
4. Raw CSS only as a last resort; it breaks on Tailwind restyles.

## Test structure
```typescript
import { test, expect } from '@playwright/test'
import { ItemsPage } from '../pages/ItemsPage'

test.describe('Item search', () => {
  let items: ItemsPage

  test.beforeEach(async ({ page }) => {
    items = new ItemsPage(page)
    await items.goto()
  })

  test('searches by keyword', async () => {
    await items.search('test')
    expect(await items.itemCount()).toBeGreaterThan(0)
    await expect(items.itemCards.first()).toContainText(/test/i)
  })

  test('shows empty state with no results', async ({ page }) => {
    await items.search('zzz-nonexistent')
    await expect(page.getByTestId('no-results')).toBeVisible()
    expect(await items.itemCount()).toBe(0)
  })
})
```

## Running against the Laravel app
Point Playwright at the running app and let it boot `php artisan serve` (or use an already-running instance / CI app URL).

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: [['html', { outputFolder: 'playwright-report' }], ['junit', { outputFile: 'playwright-results.xml' }]],
  use: {
    baseURL: process.env.APP_URL ?? 'http://127.0.0.1:8000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
  ],
  webServer: {
    command: 'php artisan serve --port=8000',
    url: 'http://127.0.0.1:8000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
})
```

Use a dedicated testing database/env (`.env.testing`) so E2E runs never touch development data, and migrate/seed it before the suite.

## Auth and network state reuse
Log in once, save storage state, and reuse it so specs skip the login flow.

```typescript
// global-setup.ts — sign in once, persist cookies/session
import { chromium } from '@playwright/test'

export default async () => {
  const browser = await chromium.launch()
  const page = await browser.newPage()
  await page.goto(`${process.env.APP_URL ?? 'http://127.0.0.1:8000'}/login`)
  await page.getByLabel('Email').fill(process.env.E2E_EMAIL!)
  await page.getByLabel('Password').fill(process.env.E2E_PASSWORD!)
  await page.getByRole('button', { name: 'Log in' }).click()
  await page.waitForURL('**/dashboard')
  await page.context().storageState({ path: 'tests/e2e/.auth/user.json' })
  await browser.close()
}
```

Wire it via `globalSetup` and `use: { storageState: 'tests/e2e/.auth/user.json' }`. Keep `.auth/` out of version control. Seed the `E2E_EMAIL` account in the E2E database, or use a test account the project documents; never use a real user's credentials. For a manual walkthrough, `@skills/interactive-testing/SKILL.md` *Sign-in and test accounts* owns the sign-in order. You can also stub backend responses with `page.route(...)` to isolate the frontend from flaky external services.

## CI wiring
```yaml
name: E2E
on: [push, pull_request]
jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with: { php-version: '8.4' }   # match composer.json require.php
      - run: composer install --no-interaction --prefer-dist
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run build
      - run: php artisan migrate --seed --env=testing
      - run: npx playwright test
        env:
          APP_URL: http://127.0.0.1:8000
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: playwright-report, path: playwright-report/, retention-days: 30 }
```

## Flaky-test avoidance
Per `@rules/code-testing/general.md`, tests must be deterministic.

- Use auto-waiting locators (`locator.click()`), never `page.click(selector)` on a maybe-not-ready node.
- Replace `await page.waitForTimeout(...)` with `waitForResponse`, `waitForURL`, or `expect(locator).toBeVisible()`.
- Wait for the element state before acting on animated UI: `await locator.waitFor({ state: 'visible' })`.
- Never quarantine a flaky test with `test.fixme` or a skip: `@rules/git/general.md` forbids a skipped test left to be enabled later. Fix its cause — a missing wait, shared state — and keep the test. When the cause cannot be established, report it instead of parking the test. A flaky test outside the diff and unrelated to the assignment is left unchanged, per `@skills/resolve-issue/references/quality-gates.md` *A flaky test outside the diff and the assignment is left alone*.
- Reproduce flakiness with `npx playwright test path.spec.ts --repeat-each=10`.

## Done when
- Preconditions confirmed Playwright is present (otherwise deferred to manual/Pest/Dusk).
- Specs use POM and role/test-id selectors.
- The suite runs against the Laravel app on a dedicated testing env/database.
- Auth/network state is reused where it speeds the suite.
- No arbitrary sleeps; all waits are condition-based.
- CI runs the suite and uploads the report.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
