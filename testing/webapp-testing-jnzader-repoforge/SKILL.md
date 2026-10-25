---
name: webapp-testing
description: >
  Browser-based UI verification using Playwright. Page Object Model, selector
  best practices, visual regression, network interception, and MCP integration.
  Trigger: When writing E2E tests, verifying UI changes, or setting up Playwright.
license: MIT
metadata:
  author: JNZader
  version: "1.0"
  tags: [playwright, e2e, testing, ui, browser]
  category: testing
  source: anthropics/skills
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

## Purpose

Patterns for browser-based UI verification using Playwright. Reliable, maintainable, fast E2E tests.

---

## Selector Priority

| Priority | Selector | Example | Why |
|----------|----------|---------|-----|
| 1 | Role | `getByRole('button', { name: 'Submit' })` | Accessible, semantic |
| 2 | Label | `getByLabel('Email')` | Accessible, user-facing |
| 3 | Test ID | `getByTestId('submit-btn')` | Stable, explicit |
| 4 | Text | `getByText('Sign in')` | Readable but fragile |
| 5 | CSS | `page.locator('.btn-primary')` | Last resort |

NEVER: XPath, auto-generated IDs, DOM structure selectors.

---

## Page Object Model

```typescript
export class LoginPage {
  constructor(private page: Page) {}
  get emailInput() { return this.page.getByLabel('Email'); }
  get passwordInput() { return this.page.getByLabel('Password'); }
  get submitButton() { return this.page.getByRole('button', { name: 'Sign in' }); }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

---

## Visual Regression

```typescript
test('dashboard renders correctly', async ({ page }) => {
  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');
  await expect(page).toHaveScreenshot('dashboard.png', { maxDiffPixelRatio: 0.01 });
});
```

---

## Network Interception

```typescript
test('handles API errors', async ({ page }) => {
  await page.route('**/api/users', route =>
    route.fulfill({ status: 500, body: 'Server Error' })
  );
  await page.goto('/users');
  await expect(page.getByText('Something went wrong')).toBeVisible();
});
```

---

## Anti-Flakiness

1. Wait for state, not time — never `page.waitForTimeout()`
2. Isolate tests — fresh context per test
3. Web-first assertions — `expect(locator).toBeVisible()` auto-retries
4. Mock external APIs
5. CI retries: `retries: 2` in config

---

## Critical Rules

1. NEVER use `page.waitForTimeout()` — wait for specific conditions
2. ALWAYS use Page Object Model for pages with 3+ interactions
3. Selectors MUST follow priority: role > label > testid > text > CSS
4. Visual regression MUST set `maxDiffPixelRatio`
5. E2E tests MUST NOT depend on seed data
6. ALWAYS use `--trace on-first-retry` in CI
