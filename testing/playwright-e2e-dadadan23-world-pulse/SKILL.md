---
name: playwright-e2e
description: "World Pulse: When writing or modifying end-to-end tests for the web frontend (or Electron app) in the project's Playwright test suite."
---

# Playwright E2E Test

**When to use:** When writing or modifying end-to-end tests for the web frontend (or Electron app) in the project's Playwright test suite.

---

## Setup

Run E2E tests with:

```bash
npm run test:e2e
```

Playwright is configured in `playwright.config.ts` (root). Tests live alongside source or in a dedicated `e2e/` directory.

---

## Test Isolation

Each test must be fully independent — no shared state between tests:

```ts
import { test, expect } from '@playwright/test';

test('dashboard renders the globe', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('canvas')).toBeVisible();
});
```

Use `page.goto('/')` at the start of every test that needs a fresh page state.

---

## Selectors

Prefer accessible selectors in order:
1. `getByRole` — most resilient to DOM changes
2. `getByText` — for visible labels
3. `getByTestId` — add `data-testid` attributes sparingly and only for E2E use

Avoid CSS class selectors — Tailwind class names change.

---

## Async Patterns

Always `await` Playwright actions and assertions. Use `expect(locator).toBeVisible()` rather than manual wait loops:

```ts
// Good
await expect(page.getByText('CONNECTED')).toBeVisible({ timeout: 5000 });

// Bad — polling manually
while (!(await page.getByText('CONNECTED').isVisible())) { ... }
```

---

## Electron E2E

For Electron-specific tests, use the `electron` launch helper from `@playwright/test`:

```ts
import { _electron as electron } from 'playwright';

test('Electron window opens', async () => {
  const app = await electron.launch({ args: ['dist/main/main.js'] });
  const window = await app.firstWindow();
  expect(await window.title()).toBe('World Pulse');
  await app.close();
});
```

Build the app before running Electron E2E (`npm run build:electron`).

---

## CI Integration

E2E tests run separately from unit tests. In CI:
- Unit tests: `npm run test:coverage` (Vitest)
- E2E tests: `npm run test:e2e` (Playwright, requires a running server or `webServer` config)

Configure `webServer` in `playwright.config.ts` to start the dev server automatically:

```ts
export default defineConfig({
  webServer: {
    command: 'npm run dev:renderer',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## Anti-Patterns

- Do not use `page.waitForTimeout()` — use `expect(locator).toBeVisible()` with a timeout.
- Do not share browser state across tests via module-level variables.
- Do not write E2E tests for logic that unit tests can cover — E2E is for user-visible behavior.
- Do not hard-code ports — use environment variables or the `webServer` config.
