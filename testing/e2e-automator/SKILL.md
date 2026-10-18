---
name: e2e-automator
description: "Build robust end-to-end test suites with Playwright or Cypress. Covers page objects, fixtures, visual testing, and CI integration."
category: testing
tags: [e2e, playwright, cypress, browser-automation, testing]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# E2E Test Automator

## Purpose
Create reliable, maintainable end-to-end test suites that simulate real user behavior across the full application stack.

## Playwright Setup (Recommended)

### 1️⃣ Page Object Model
```typescript
// tests/pages/LoginPage.ts
import { Page, Locator } from "@playwright/test";

export class LoginPage {
  private readonly emailInput: Locator;
  private readonly passwordInput: Locator;
  private readonly submitButton: Locator;
  private readonly errorMessage: Locator;

  constructor(private page: Page) {
    this.emailInput    = page.getByLabel("Email");
    this.passwordInput = page.getByLabel("Password");
    this.submitButton  = page.getByRole("button", { name: "Sign in" });
    this.errorMessage  = page.getByRole("alert");
  }

  async navigate(): Promise<void> {
    await this.page.goto("/login");
  }

  async login(email: string, password: string): Promise<void> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage(): Promise<string> {
    return await this.errorMessage.textContent() ?? "";
  }
}
```

### 2️⃣ Test Structure with Fixtures
```typescript
// tests/fixtures.ts
import { test as base } from "@playwright/test";
import { LoginPage } from "./pages/LoginPage";
import { DashboardPage } from "./pages/DashboardPage";

type TestFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: Page;
};

export const test = base.extend<TestFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  authenticatedPage: async ({ page }, use) => {
    // Login once via API for speed
    const response = await page.request.post("/api/auth/login", {
      data: { email: "test@example.com", password: "password123" },
    });
    const { token } = await response.json();
    await page.context().addCookies([{ name: "auth-token", value: token, url: "http://localhost:3000" }]);
    await use(page);
  },
});

export { expect } from "@playwright/test";
```

### 3️⃣ Tests
```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from "../fixtures";

test.describe("Authentication", () => {
  test("user can login with valid credentials", async ({ loginPage, page }) => {
    await loginPage.navigate();
    await loginPage.login("user@example.com", "password123");
    
    await expect(page).toHaveURL("/dashboard");
    await expect(page.getByText("Welcome back")).toBeVisible();
  });

  test("shows error with invalid credentials", async ({ loginPage }) => {
    await loginPage.navigate();
    await loginPage.login("wrong@example.com", "wrongpassword");
    
    const error = await loginPage.getErrorMessage();
    expect(error).toContain("Invalid credentials");
  });
});
```

### 4️⃣ Playwright Config for CI
```typescript
// playwright.config.ts
export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["html"], ["junit", { outputFile: "results.xml" }]],
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "mobile", use: { ...devices["iPhone 15 Pro"] } },
  ],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

## Outputs
1. Page Object Models for all major pages
2. Test fixtures and helper utilities
3. Test suite for critical user journeys
4. Visual regression test setup
5. CI/CD integration configuration
6. Test reporting setup
