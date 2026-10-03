---
name: webapp-testing
description: Automated end-to-end web application testing using Playwright. Use when the user wants to write automated tests for a web app, test frontend functionality, verify UI behaviour programmatically, debug interactions in a browser, capture screenshots of a running app, check for console errors, or test a user flow from login to completion.
---

# Web App Testing (Playwright)

Manual testing finds bugs once. Automated tests find them every time. This skill writes Playwright scripts that test real browser behaviour — clicks, forms, navigation, network calls, and visual state — reliably and repeatably.

---

## Web App Testing Principles

- **Reconnaissance before action.** Never assume a selector exists. Navigate, wait for load, inspect the DOM, then act. Selectors that work in dev break in staging. Discover them at runtime.
- **Wait for real readiness.** `networkidle` is not always enough. Wait for the specific element you need, not just page load.
- **Test what the user experiences.** Test by role, text, and label — not by CSS class or XPath. Classes change; user-facing text is more stable.
- **One test, one user journey.** A test that does login + checkout + confirmation + email verification is four tests jammed together. Split them.
- **Tests must clean up after themselves.** A test that leaves state (created users, placed orders) that affects the next test is a flaky test waiting to happen.
- **Screenshot on failure.** Every test should capture a screenshot when it fails — this is the single fastest debugging tool available.

---

## Step 0: Choose the Right Approach

```
Is the app running?
├── NO → Start it first with with_server.py helper (if available)
│         or: npm run dev / python app.py in background
└── YES
    └── Is it static HTML (no JS framework)?
        ├── YES → Read HTML directly, write selectors from source
        └── NO (React, Vue, Svelte, etc.)
            → Reconnaissance first: navigate → networkidle → screenshot → inspect → act
```

---

## Project Setup

### Install Playwright
```bash
npm init -y
npm install -D @playwright/test
npx playwright install chromium  # or: install firefox, webkit too

# Python
pip install playwright
playwright install chromium
```

### Config (`playwright.config.ts`)
```typescript
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  timeout: 30_000,
  retries: process.env.CI ? 2 : 0,  // retry in CI, not locally
  use: {
    baseURL: process.env.BASE_URL ?? "http://localhost:3000",
    headless: true,
    screenshot: "only-on-failure",  // always capture on failure
    video: "retain-on-failure",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "npm run dev",
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## Reconnaissance Pattern (Always Do This First)

Before writing any selectors, discover the actual rendered DOM:

```typescript
import { test, expect } from "@playwright/test";

test("reconnaissance — inspect login page", async ({ page }) => {
  await page.goto("/login");
  await page.waitForLoadState("networkidle");

  // Take screenshot to see what's there
  await page.screenshot({ path: "screenshots/login.png", fullPage: true });

  // List all interactive elements
  const buttons = await page.locator("button").all();
  for (const btn of buttons) {
    console.log("Button:", await btn.textContent(), await btn.getAttribute("type"));
  }

  const inputs = await page.locator("input").all();
  for (const input of inputs) {
    console.log("Input:", await input.getAttribute("name"), await input.getAttribute("type"));
  }
});
```

Run this first. Read the output. Then write your real tests based on what actually exists.

---

## Writing Tests

### Preferred Selector Order (most stable → least stable)

```typescript
// 1. Role + name (most resilient — matches what users see)
page.getByRole("button", { name: "Sign in" })
page.getByRole("textbox", { name: "Email address" })
page.getByRole("link", { name: "Forgot password?" })

// 2. Label (for form fields)
page.getByLabel("Email address")
page.getByLabel("Password")

// 3. Test ID (when team adds them explicitly)
page.getByTestId("submit-button")

// 4. Text (for non-interactive elements)
page.getByText("Welcome back")

// 5. CSS selector (last resort — fragile, breaks on refactor)
page.locator(".login-form button[type='submit']")

// ❌ Never use XPath — brittle, unreadable
page.locator("//button[@class='btn-primary']")
```

### Complete Login Test
```typescript
import { test, expect } from "@playwright/test";

test.describe("Authentication", () => {
  test("user can log in with valid credentials", async ({ page }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");

    // Fill form
    await page.getByLabel("Email").fill("test@example.com");
    await page.getByLabel("Password").fill("password123");

    // Submit
    await page.getByRole("button", { name: "Sign in" }).click();

    // Verify redirect to dashboard
    await page.waitForURL("**/dashboard");
    await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
  });

  test("shows error on invalid credentials", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("Email").fill("wrong@example.com");
    await page.getByLabel("Password").fill("wrongpassword");
    await page.getByRole("button", { name: "Sign in" }).click();

    await expect(page.getByText("Invalid email or password")).toBeVisible();
    // Should NOT redirect
    await expect(page).toHaveURL(/.*login.*/);
  });
});
```

### Form Submission Test
```typescript
test("user can submit contact form", async ({ page }) => {
  await page.goto("/contact");
  await page.waitForLoadState("networkidle");

  await page.getByLabel("Name").fill("Jane Doe");
  await page.getByLabel("Email").fill("jane@example.com");
  await page.getByLabel("Message").fill("This is a test message with sufficient length.");

  // Intercept the API call to verify it's made
  const responsePromise = page.waitForResponse(
    response => response.url().includes("/api/contact") && response.status() === 200
  );

  await page.getByRole("button", { name: "Send message" }).click();

  await responsePromise;
  await expect(page.getByText("Message sent successfully")).toBeVisible();
});
```

### Navigation Test
```typescript
test("main navigation links work", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");

  const navItems = [
    { link: "Products", url: /.*products.*/ },
    { link: "Pricing",  url: /.*pricing.*/ },
    { link: "About",    url: /.*about.*/  },
  ];

  for (const { link, url } of navItems) {
    await page.getByRole("navigation").getByRole("link", { name: link }).click();
    await expect(page).toHaveURL(url);
    await page.goBack();
    await page.waitForLoadState("networkidle");
  }
});
```

### API Interception
```typescript
test("handles API failure gracefully", async ({ page }) => {
  // Mock the API to return an error
  await page.route("**/api/users", route => {
    route.fulfill({ status: 500, body: JSON.stringify({ error: "Server error" }) });
  });

  await page.goto("/users");
  await page.waitForLoadState("networkidle");

  // App should show error state, not crash
  await expect(page.getByText("Something went wrong")).toBeVisible();
  await expect(page.getByRole("button", { name: "Try again" })).toBeVisible();
});
```

---

## Visual Testing

### Screenshot comparison
```typescript
test("dashboard looks correct", async ({ page }) => {
  await page.goto("/dashboard");
  await page.waitForLoadState("networkidle");

  // Wait for data to load before snapping
  await page.waitForSelector("[data-testid='chart']");

  await expect(page).toHaveScreenshot("dashboard.png", {
    maxDiffPixelRatio: 0.02  // allow 2% pixel difference
  });
});
```

### Console error detection
```typescript
test("page has no console errors", async ({ page }) => {
  const errors: string[] = [];

  page.on("console", msg => {
    if (msg.type() === "error") errors.push(msg.text());
  });

  page.on("pageerror", err => errors.push(err.message));

  await page.goto("/");
  await page.waitForLoadState("networkidle");

  expect(errors).toHaveLength(0);
});
```

---

## Python Playwright

```python
import pytest
from playwright.sync_api import Page, expect

def test_login(page: Page):
    page.goto("/login")
    page.wait_for_load_state("networkidle")

    page.get_by_label("Email").fill("test@example.com")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Sign in").click()

    page.wait_for_url("**/dashboard")
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()

def test_shows_error_on_invalid_login(page: Page):
    page.goto("/login")
    page.get_by_label("Email").fill("wrong@example.com")
    page.get_by_label("Password").fill("wrong")
    page.get_by_role("button", name="Sign in").click()

    expect(page.get_by_text("Invalid email or password")).to_be_visible()
```

```bash
# Run
pytest tests/ -v

# With headed browser (see what's happening)
pytest tests/ --headed

# Generate HTML report
pytest tests/ --html=report.html
```

---

## Debugging Failures

```typescript
// Slow down execution to watch what's happening
test.use({ actionTimeout: 5000 });

// Pause and inspect in headed mode
await page.pause();  // opens Playwright Inspector

// Log every network request
page.on("request", req => console.log("→", req.method(), req.url()));
page.on("response", res => console.log("←", res.status(), res.url()));

// Dump current DOM
const html = await page.content();
console.log(html.slice(0, 2000));

// Check what Playwright sees
await page.screenshot({ path: "debug.png", fullPage: true });
```

---

## CI Integration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test
        env:
          BASE_URL: http://localhost:3000
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## Common Pitfalls

| Mistake | Why it fails | Fix |
|---|---|---|
| Not waiting for `networkidle` on dynamic apps | JS hasn't hydrated yet — selectors not found | `await page.waitForLoadState("networkidle")` |
| Hardcoding CSS classes as selectors | Classes change on refactor | Use `getByRole`, `getByLabel`, `getByText` |
| Not closing browser on error | Orphaned browser processes | Use `test.afterEach` cleanup or `using` |
| `page.click()` before element is visible | Race condition | `await page.getByRole(...).click()` waits automatically |
| Writing one giant test | Flaky, hard to debug, slow to isolate | One test per user journey |
| No screenshot on failure | Can't debug without knowing what was on screen | Set `screenshot: "only-on-failure"` in config |

---

## Definition of Done — Web App Testing

- [ ] Reconnaissance run first — selectors discovered from rendered DOM
- [ ] `getByRole`, `getByLabel`, or `getByText` used — no raw CSS selectors
- [ ] Each test covers exactly one user journey
- [ ] `waitForLoadState("networkidle")` called after navigation
- [ ] Screenshot on failure configured in `playwright.config.ts`
- [ ] Both happy path and error paths tested
- [ ] API mocking tested for failure states
- [ ] Tests are independent — no shared mutable state between tests
- [ ] Tests clean up after themselves (created data removed in `afterEach`)
- [ ] CI pipeline runs tests on every PR
- [ ] Failure artifacts (screenshots, traces) uploaded in CI
