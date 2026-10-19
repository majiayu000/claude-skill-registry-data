---
name: playwright-e2e-tests
description: Use when writing, fixing or stabilizing end-to-end or UI tests with Playwright, automating a browser user flow, replacing Cypress or Selenium tests, or setting up Playwright in a web project.
---

# Playwright E2E Tests

## Overview

End-to-end tests prove that real user journeys work in a real browser. Write few of them, make each one reliable, and locate elements the way users find them.

## Method

1. **Setup** (if missing): `npm init playwright@latest`. Configure `baseURL`, `webServer` to start the app, `trace: "on-first-retry"`, and the browsers you support in `playwright.config.ts`.
2. **Pick journeys** by risk: sign up / log in, the core purchase or create flow, payments, permissions. One spec file per journey.
3. **Set up state through the API or storage state**, not through the UI, except in the test that covers that UI (log in once in a setup project and reuse `storageState`).
4. **Write steps with user-facing locators** and web-first assertions (table below).
5. **Run** `npx playwright test`, then `npx playwright test --repeat-each=5` on new tests to catch flakiness. Use `npx playwright show-trace` on failures.

## Locators and assertions

| Prefer | Avoid |
|---|---|
| `page.getByRole("button", { name: "Pay now" })` | `page.locator(".btn-primary:nth-child(2)")` |
| `getByLabel("Email")`, `getByPlaceholder`, `getByText` | XPath, deep CSS chains |
| `getByTestId("cart-total")` when no accessible name exists | IDs generated at runtime |
| `await expect(locator).toHaveText("₹900")` (auto-waits) | `expect(await locator.textContent()).toBe(...)` |
| `await expect(page).toHaveURL(/\/orders\/\d+/)` | `page.waitForTimeout(3000)` |

## Example

```ts
import { test, expect } from "@playwright/test";

test("user applies a coupon at checkout", async ({ page }) => {
  await page.goto("/cart");
  await page.getByLabel("Coupon code").fill("SAVE10");
  await page.getByRole("button", { name: "Apply" }).click();
  await expect(page.getByText("Coupon applied")).toBeVisible();
  await expect(page.getByTestId("cart-total")).toHaveText("₹900");
});
```

## Rules

- Each test is independent: its own data, no order dependence, runs in parallel.
- No fixed sleeps. Wait on a visible condition or a network response (`page.waitForResponse`).
- Mock only third parties you do not control (`page.route`); keep your own backend real.
- Use the Page Object pattern only when the same page is used in many specs.
- Visual comparisons (`toHaveScreenshot`) only for stable, important screens, with masks for dynamic content.

## Common mistakes

- Testing every edge case end to end; push those down to unit and API tests.
- Logging in through the UI in every test.
- Selectors tied to styling classes that change with design updates.
- Shared test accounts mutated by parallel tests.
- Retrying flaky tests instead of fixing the wait condition.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
