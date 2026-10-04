---
name: playwright-tester
description: Full-lifecycle Web E2E Testing, QA/QC analysis, and Playwright test automation. Generates business test matrices (happy path, negative, boundary, RBAC, API/network failure simulation), implements resilient Page Object Model tests, and produces structured QA bug reports.
mcp: codebase-memory-mcp
---

# /supergraph:playwright-tester

Complete Web QA/QC & Playwright E2E testing framework. From business requirement analysis to resilient test automation and defect reporting.

Announce: "🎭 /supergraph:playwright-tester — designing QA matrix & automating Playwright E2E tests..."

---

## When to Use

- Writing comprehensive E2E tests for web applications (Next.js, Vite, React, Vue, Angular, SSR/SPA)
- Testing complete business flows (happy path, validation failures, boundary states)
- Simulating system failures: API down (500), network timeout, offline mode, rate limit (429)
- Testing Authentication & Authorization (RBAC, unauthenticated redirects, expired token)
- Creating Page Object Model (POM) test architecture from scratch
- Performing formal QA/QC regression testing and generating defect reports

---

## The 4-Phase QA/QC Workflow

```
[Phase 1: QA Analyst]        [Phase 2: SDET]           [Phase 3: Runner]        [Phase 4: QC Lead]
Business Test Matrix  ───>  Playwright Automation ───>  Execution & Tracing ───> Defect Report & Gate
(Happy/Sad/Boundary/        (POM, Resilient Selectors,  (Trace, Screenshots,    (Blocker/Major,
 Network Failure/RBAC)       page.route API mocks)       Console & Network Logs) Steps to Reproduce)
```

---

## Phase 1: Business Test Matrix (QA Analyst)

Before writing any automation code, map out the test matrix using **Given-When-Then** format across 5 core test dimensions:

### 1. Happy Path (Primary Business Flow)
- Complete user journey from start to desired outcome with valid inputs.
- Verification of UI state changes, persistence, and navigation.

### 2. Negative Path (Sad Path & Validation)
- Missing required fields, invalid email/phone, password rules.
- Invalid business logic: expired coupon, insufficient balance, duplicate registration.
- Verify exact user-facing error messages, field highlight, and form submission prevention.

### 3. Boundary & Edge Cases
- Min/Max input limits (0, 1, max chars, special unicode/HTML characters).
- Rapid duplicate clicks (double-submit prevention on payment or submission buttons).
- Empty states (empty shopping cart, no search results, initial empty dashboard).

### 4. Authentication & RBAC (Role-Based Access Control)
- Unauthenticated user hitting protected routes → redirect to `/login` with `returnUrl`.
- Role isolation: User trying to access `/admin` → 403 Forbidden or redirected.
- Session expiration during an active workflow.

### 5. Network & System Resilience (Fault Injection)
- Backend failure: Mock `500 Internal Server Error` on critical API calls → verify graceful toast/banner error, no white screen.
- Slow network / Latency: Mock 3000ms delay → verify loading skeletons/spinners and disabled submit buttons.
- Offline behavior: Disconnect network → verify offline indicators.

---

## Phase 2: Playwright Automation Engine (SDET)

### Rule 1: Resilient User-Centric Selectors (Strict Priority)

Never use fragile CSS classes (`.btn-primary.mt-4`) or positional XPath (`//div[2]/button[1]`).

| Priority | Selector Method | Example |
|---|---|---|
| **1 (Best)** | `page.getByRole()` | `page.getByRole('button', { name: 'Submit Order' })` |
| **2** | `page.getByLabel()` | `page.getByLabel('Email address')` |
| **3** | `page.getByPlaceholder()` | `page.getByPlaceholder('Enter your password')` |
| **4** | `page.getByText()` | `page.getByText('Order completed successfully')` |
| **5** | `page.getByTestId()` | `page.getByTestId('order-summary-card')` |

### Rule 2: Page Object Model (POM) Structure

Encapsulate page locators and user interactions into reusable page classes:

```typescript
// tests/pages/checkout.page.ts
import { type Page, type Locator, expect } from '@playwright/test';

export class CheckoutPage {
  readonly page: Page;
  readonly cardInput: Locator;
  readonly payButton: Locator;
  readonly errorAlert: Locator;

  constructor(page: Page) {
    this.page = page;
    this.cardInput = page.getByLabel('Card Number');
    this.payButton = page.getByRole('button', { name: 'Pay Now' });
    this.errorAlert = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/checkout');
    await expect(this.payButton).toBeVisible();
  }

  async submitPayment(cardNumber: string) {
    await this.cardInput.fill(cardNumber);
    await this.payButton.click();
  }
}
```

### Rule 3: Session & Auth Optimization (`storageState`)

Never log in through the UI on every test. Authenticate once in a setup project and save state:

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'e2e-authenticated',
      dependencies: ['setup'],
      use: { storageState: 'playwright/.auth/user.json' },
    },
    {
      name: 'e2e-anonymous',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

### Rule 4: Network Interception & Failure Injection (`page.route`)

Simulate backend failures deterministically without touching test DB:

```typescript
// Simulating API 500 Error
test('displays error notification when order submission fails', async ({ page }) => {
  await page.route('**/api/v1/orders', async route => {
    await route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ message: 'Database connection failed' }),
    });
  });

  const checkoutPage = new CheckoutPage(page);
  await checkoutPage.goto();
  await checkoutPage.submitPayment('4242424242424242');

  await expect(checkoutPage.errorAlert).toBeVisible();
  await expect(checkoutPage.errorAlert).toContainText('Database connection failed');
});
```

### Rule 5: Auto-Waiting Assertions (Zero Arbitrary Sleeps)

- **FORBIDDEN**: `await page.waitForTimeout(3000)` (causes flakiness or slow tests).
- **MANDATORY**: Web-first auto-retrying assertions:
  - `await expect(locator).toBeVisible()`
  - `await expect(locator).toHaveText('...')`
  - `await expect(locator).toBeEnabled()`
  - `await expect(page).toHaveURL(/.*checkout/)`

---

## Phase 3: Execution, Flakiness Guard & Artifacts

Run test execution with tracing enabled for failure post-mortem:

```bash
# Run all tests
npx playwright test

# Run single file with UI / trace
npx playwright test tests/e2e/checkout.spec.ts --trace on

# Run headed for visual debugging
npx playwright test --headed
```

Configuration essentials in `playwright.config.ts`:
- `trace: 'retain-on-failure'`
- `screenshot: 'only-on-failure'`
- `video: 'retain-on-failure'`
- `webServer`: auto-start dev server if not already running.

---

## Phase 4: QC Defect & Quality Gate Report

When any test fails during execution, format the defect report immediately:

```markdown
### 🐛 QA Defect Report

- **Defect ID**: BUG-001
- **Severity**: Blocker | Critical | Major | Minor
- **Affected Flow**: [e.g. Checkout → Payment Submission]
- **Environment**: Chromium / Mobile Safari / Desktop

#### 1. Steps to Reproduce
1. Navigate to `/checkout` with 1 item in cart
2. Enter invalid card number `1234`
3. Click "Pay Now"

#### 2. Expected Result
- Button disabled or error message "Invalid card number" appears below input.
- No network request sent with invalid card format.

#### 3. Actual Result
- Error message missing. Unhandled promise rejection in browser console.
- Blank white screen rendered.

#### 4. Evidence & Artifacts
- Screenshot: `test-results/checkout-failure.png`
- Trace Viewer: `npx playwright show-trace test-results/trace.zip`
- Console Error: `TypeError: Cannot read properties of undefined (reading 'status')`

#### 5. Root Cause Hypothesis
- `useCheckout.ts:84` does not handle rejected promise from `api.submit()`.
```

---

## Execution Checklist

- [ ] Business test matrix defined (Happy, Sad, Boundary, RBAC, Network Failure)
- [ ] Selectors follow role/label/testId priority (no raw CSS/XPath)
- [ ] POM pattern applied for multi-step or shared pages
- [ ] Backend error states simulated via `page.route`
- [ ] Auto-waiting assertions used exclusively (no `waitForTimeout`)
- [ ] Artifacts captured (Trace, screenshots, video on failure)
- [ ] Quality gate report produced with clear PASS/FAIL verdict
