---
name: e2e-playwright
description: Use when writing end-to-end browser tests with Playwright. Covers resilient locators, auto-waiting, network interception, authentication reuse, parallelization, and eliminating flakiness.
metadata:
  category: testing
  version: 1.0.0
  tags: [playwright, e2e, browser, flakiness, automation]
---

# End-to-End Testing with Playwright

## Purpose

Write browser tests that fail only when the application is broken. An end-to-end suite that fails randomly is worse than no suite: it consumes attention and trains the team to ignore red.

## When to Use

- Testing a complete user journey through a real browser.
- Replacing a flaky Selenium or Cypress suite.
- Testing flows that cross pages, tabs, or authentication.
- Debugging an intermittent E2E failure.

## Capabilities

- Resilient locators based on user-visible attributes.
- Auto-waiting and web-first assertions.
- Network interception, mocking, and request assertion.
- Authentication state reuse across tests.
- Parallel execution and sharding.
- Trace, video, and screenshot capture on failure.

## Inputs

- The journeys that matter enough to test end to end (there are fewer than you think).
- The application, its authentication, and its test data strategy.

## Outputs

- Tests locating elements by role and accessible name.
- Zero explicit waits or sleeps.
- Traces on failure that make a CI-only failure diagnosable.

## Workflow

1. **Choose the journeys** — End-to-end tests are slow and expensive. Test the paths whose failure would be a serious incident: sign up, check out, pay. Not every form.
2. **Locate the way a user would** — `getByRole("button", { name: "Place order" })`. Not a CSS class, not an XPath. Class names change; the accessible name is the contract with the user.
3. **Never sleep** — Playwright's assertions auto-wait and retry. `waitForTimeout` is the single largest cause of both flakiness and slowness in an E2E suite.
4. **Reuse authentication** — Log in once in a setup project, save the storage state, and reuse it. Logging in before every test triples the suite runtime.
5. **Control the network where the test is not about the network** — Mock the third-party payment provider; do not depend on its sandbox being up.
6. **Capture traces on failure** — A CI failure with a trace is diagnosable in two minutes. Without one, it is a mystery.

## Best Practices

- Any `waitForTimeout` in a Playwright test is a bug. If you need to wait for something, assert on the thing you are waiting for — the assertion retries until it is true.
- Locating by CSS class couples the test to the styling. A CSS refactor should not break the test suite.
- Tests must be independent and able to run in any order, in parallel. A test that depends on a previous test's data will fail intermittently forever.
- Each test creates the data it needs, with a unique identifier. Shared fixture data plus parallel execution equals a race condition.
- Assert on the user-visible outcome, not on an implementation detail. "The order confirmation shows the order number" — not "the POST returned 201".
- Run the suite against a production-like build. E2E tests against a dev server with hot reloading are testing something you do not ship.

## Examples

**Resilient, independent, and free of sleeps:**

```typescript
import { test, expect } from "@playwright/test";

test.describe("checkout", () => {
  test("a customer can place an order and see it confirmed", async ({ page }) => {
    // Unique data per test: the suite can run in parallel without collisions.
    const email = `test-${crypto.randomUUID()}@example.com`;
    await seedCustomer({ email, cardOnFile: true });

    // The payment provider is a third party. The test is not about their uptime.
    await page.route("**/v1/payment_intents", (route) =>
      route.fulfill({ status: 200, json: { id: "pi_test", status: "succeeded" } }),
    );

    await page.goto("/checkout");

    // Located as a user perceives them, not by class name.
    await page.getByRole("textbox", { name: "Email" }).fill(email);
    await page.getByRole("button", { name: "Place order" }).click();

    // Web-first assertion: retries until it passes or times out. No sleep needed.
    await expect(page.getByRole("heading", { name: "Order confirmed" })).toBeVisible();
    await expect(page.getByTestId("order-number")).toHaveText(/^ord_[0-9A-Z]{10}$/);
  });
});
```

**Authentication reused, not repeated:**

```typescript
// auth.setup.ts — runs once, before everything.
setup("authenticate", async ({ page }) => {
  await page.goto("/login");
  await page.getByRole("textbox", { name: "Email" }).fill(process.env.TEST_USER!);
  await page.getByRole("textbox", { name: "Password" }).fill(process.env.TEST_PASS!);
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();

  await page.context().storageState({ path: ".auth/user.json" });
});

// playwright.config.ts
projects: [
  { name: "setup", testMatch: /auth\.setup\.ts/ },
  {
    name: "chromium",
    dependencies: ["setup"],
    use: { storageState: ".auth/user.json" },   // every test starts logged in
  },
],
```

## Notes

- `trace: "on-first-retry"` in the config gives you a full trace — DOM snapshots, network, console — for exactly the runs that failed, at negligible cost. It is the difference between debugging a CI flake in minutes and never diagnosing it.
- Playwright's auto-waiting covers actionability (visible, enabled, stable, receives events). It does not cover *your* application's asynchronous state — for that, assert on what the user would see.
- Component testing (Playwright, Vitest browser mode) covers far more ground per second than end-to-end testing. Push tests down the pyramid whenever the coverage is equivalent.
