---
name: e2e-user-journeys
description: Use when implementing critical user workflows that span multiple pages/components - tests complete journeys end-to-end using Page Object Model, user-centric selectors, and condition-based waiting; use sparingly (10-15% of tests)
---

# Frontend E2E User Journeys

## Overview

End-to-end (E2E) tests verify complete user workflows from start to finish, including multiple pages, API requests, and database state.

**When to use this skill:**
- Implementing critical user workflows (login, checkout, signup)
- Testing cross-page journeys (onboarding wizard)
- Verifying third-party integrations (OAuth, payments)
- Testing business-critical flows (cancel subscription, refund)

**When NOT to use:**
- Component-level behavior → Use component tests
- Edge cases → Use unit tests
- Variations of same flow → Use parameterized tests
- Rapid iteration → E2E tests too slow

## The Iron Law

```
E2E TESTS ONLY FOR CRITICAL USER JOURNEYS
```

**Rule of thumb**: If manual QA would test it end-to-end, automate it at E2E level. Otherwise, test at lower level.

**Target**: E2E tests should be 10-15% of total test suite (not more).

## When to Write E2E Tests

### Use E2E Tests For:

**Critical user workflows:**
- ✓ User signup → Email verification → First login
- ✓ Add to cart → Checkout → Payment → Order confirmation
- ✓ Login → Browse products → Add to wishlist
- ✓ Create account → Set preferences → Verify email → Login

**Cross-page workflows:**
- ✓ Multi-step wizards (onboarding, configuration)
- ✓ Shopping cart persistence across pages
- ✓ Authentication flow across entire app

**Third-party integrations:**
- ✓ OAuth login (Google, GitHub, etc.)
- ✓ Payment processing (Stripe, PayPal)
- ✓ Email verification flows

**Business-critical flows:**
- ✓ Cancel subscription
- ✓ Refund order
- ✓ Delete account

### DON'T Use E2E Tests For:

- ✗ Edge cases (test at unit level)
- ✗ Component behavior (test with component tests)
- ✗ Validation logic (test at unit level)
- ✗ Every permutation (test logic separately)
- ✗ Rapid development iteration (too slow)

**Decision Tree:**

```
Is this a complete user workflow?
├─ YES → Continue
│   ├─ Is it business-critical?
│   │   ├─ YES → E2E test appropriate
│   │   └─ NO → Could this be component test?
│   └─ NO → Use component or unit test
└─ NO → Use component or unit test
```

## Page Object Model Pattern

**Encapsulate page interactions in reusable classes:**

### Why Page Objects?

**Benefits:**
- Single source of truth for selectors
- Easy to update when UI changes
- Readable tests (domain language)
- Works with Playwright, Selenium, Puppeteer

**Pattern:**

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  // Locators (encapsulated)
  private get emailInput() {
    return this.page.locator('[name="email"]');
  }

  private get passwordInput() {
    return this.page.locator('[name="password"]');
  }

  private get submitButton() {
    return this.page.locator('button[type="submit"]');
  }

  // High-level actions (domain language)
  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage(): Promise<string | null> {
    const alert = this.page.locator('[role="alert"]');
    return await alert.textContent();
  }

  async isLoggedIn(): Promise<boolean> {
    return await this.page.locator('[data-testid="user-menu"]').isVisible();
  }
}
```

### Using Page Objects in Tests

```typescript
// tests/login.spec.ts
test('user can log in with valid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);

  await loginPage.goto();
  await loginPage.login('test@example.com', 'password123');

  expect(await loginPage.isLoggedIn()).toBe(true);
  await expect(page).toHaveURL('/dashboard');
});

test('shows error for invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);

  await loginPage.goto();
  await loginPage.login('test@example.com', 'wrongpassword');

  const error = await loginPage.getErrorMessage();
  expect(error).toContain('Invalid credentials');
});
```

**Benefits visible:**
- Test code is readable (domain language)
- Selectors encapsulated (change once, tests still work)
- Actions reusable (login used in multiple tests)

## User-Centric Selectors

**Select elements the way users find them:**

### Priority Order (Testing Library Guidance)

```typescript
// 1. BEST: Accessible selectors (what screen readers see)
page.getByRole('button', { name: 'Submit' });
page.getByRole('heading', { name: 'Welcome' });
page.getByLabel('Email address');

// 2. GOOD: Semantic selectors (visible text)
page.getByText('Click here to continue');
page.getByPlaceholder('Enter your name');
page.getByAltText('Company logo');

// 3. ACCEPTABLE: Test IDs (when no semantic option)
page.locator('[data-testid="checkout-form"]');

// 4. NEVER: Implementation details (brittle)
page.locator('.btn-primary-lg-v2');  // CSS classes
page.locator('div > div > button:nth-child(3)');  // Element hierarchy
page.locator('#component-instance-xyz');  // Internal IDs
```

### Why User-Centric Selectors Matter

**Resilience:**
- Tests survive refactoring
- CSS changes don't break tests
- Component restructuring doesn't break tests

**Accessibility verification:**
- If button has no accessible name, test fails
- Forces proper ARIA labels
- Ensures screen reader compatibility

**Readability:**
- "Click Submit button" not "Click .btn-xyz"
- Tests read like user instructions
- Easier to understand and maintain

### Examples

```typescript
// ❌ BAD: CSS selectors (brittle)
await page.click('.btn-primary.btn-lg');

// ✅ GOOD: Accessible selector (resilient)
await page.click('button[name="submit"]');

// ❌ BAD: Element hierarchy (brittle)
await page.fill('div.form > div:nth-child(2) > input');

// ✅ GOOD: Semantic selector (resilient)
await page.fill('input[name="email"]');
// OR
await page.getByLabel('Email address').fill('test@example.com');
```

## Condition-Based Waiting

**Always wait for conditions, not arbitrary times:**

### The Anti-Pattern

```typescript
// ❌ BAD: Guessing at timing
await page.click('button');
await page.waitForTimeout(500);  // Hope response in 500ms
const result = await page.textContent('.result');
```

**Problems:**
- Flaky tests (fails when slow)
- Slow tests (waits longer than needed)
- No guarantee condition met

### The Solution

```typescript
// ✅ GOOD: Wait for condition
await page.click('button');
await page.waitForSelector('.result');  // Wait until appears
const result = await page.textContent('.result');

// ✅ BETTER: Wait for specific state
await page.click('button');
await page.waitForResponse(resp => resp.url().includes('/api/submit'));
await page.waitForSelector('.result:has-text("Success")');
```

### Framework-Agnostic Waiting

**Playwright:**
```typescript
await page.waitForSelector('.element');
await page.waitForResponse(resp => resp.url().includes('/api'));
await page.waitForFunction(() => document.querySelector('.element'));
```

**Selenium:**
```typescript
import { until } from 'selenium-webdriver';
await driver.wait(until.elementLocated(By.css('.element')));
await driver.wait(until.elementIsVisible(element));
```

**Cypress:**
```typescript
cy.get('.element').should('be.visible');  // Built-in retry
cy.intercept('/api/data').as('getData');
cy.wait('@getData');
```

**See**: condition-based-waiting skill for comprehensive guidance.

## Test Data Management

### Use Factories or Fixtures

```typescript
// ✅ GOOD: Reusable test data factory
async function createTestUser(overrides = {}) {
  return await db.users.create({
    email: `test-${Date.now()}@example.com`,
    password: 'password123',
    name: 'Test User',
    ...overrides
  });
}

// Each test creates its own data
test('user can update profile', async ({ page }) => {
  const user = await createTestUser();

  // ... test using user
  await loginPage.login(user.email, user.password);

  // Cleanup
  await db.users.delete(user.id);
});
```

### Test Isolation

**Each test must be independent:**

```typescript
// ✅ GOOD: Each test sets up and tears down
test('test A', async () => {
  const user = await createTestUser();
  // ... test
  await cleanup(user);
});

test('test B', async () => {
  const user = await createTestUser();
  // ... test
  await cleanup(user);
});

// ❌ BAD: Tests share data (flaky)
const sharedUser = await createTestUser();

test('test A', async () => {
  // Uses sharedUser - what if test B modified it?
});
```

### Unique Test Data

```typescript
// ✅ GOOD: Unique data per test
email: `test-${Date.now()}-${Math.random()}@example.com`

// ✅ GOOD: Use UUIDs
import { randomUUID } from 'crypto';
email: `test-${randomUUID()}@example.com`
```

## Complete E2E Test Structure

### Pattern: Arrange-Act-Assert-Cleanup

```typescript
test('user can complete checkout', async ({ page }) => {
  // ARRANGE: Set up test data
  const user = await createTestUser();
  const product = await createTestProduct();

  // ACT: Perform user workflow
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login(user.email, user.password);

  const productPage = new ProductPage(page);
  await productPage.goto(product.id);
  await productPage.addToCart();

  const checkoutPage = new CheckoutPage(page);
  await checkoutPage.goto();
  await checkoutPage.fillShippingInfo({
    address: '123 Main St',
    city: 'Seattle',
    zip: '98101'
  });
  await checkoutPage.fillPaymentInfo({
    cardNumber: '4242424242424242',
    expiry: '12/25',
    cvc: '123'
  });
  await checkoutPage.submitOrder();

  // ASSERT: Verify outcome
  await expect(page.locator('[data-testid="order-confirmation"]'))
    .toContainText('Order placed successfully');

  // Verify database state
  const order = await db.orders.findByUserId(user.id);
  expect(order.status).toBe('confirmed');
  expect(order.total).toBe(product.price);

  // CLEANUP: Remove test data
  await db.orders.delete(order.id);
  await db.users.delete(user.id);
  await db.products.delete(product.id);
});
```

## API Mocking (When Needed)

**Mock external services, not your own API:**

```typescript
// ✅ GOOD: Mock external payment provider
test('handles payment failure', async ({ page }) => {
  await page.route('https://api.stripe.com/v1/charges', route => {
    route.fulfill({
      status: 400,
      body: JSON.stringify({
        error: { message: 'Card declined' }
      })
    });
  });

  // ... attempt checkout

  await expect(page.locator('[role="alert"]'))
    .toContainText('Payment failed: Card declined');
});

// ❌ BAD: Mocking your own API (defeats purpose)
test('shows user profile', async ({ page }) => {
  await page.route('/api/users/123', route => {
    route.fulfill({ body: JSON.stringify({ name: 'Alice' })});
  });
  // Not testing real API integration!
});
```

## Framework Examples

### Playwright (Recommended)

```typescript
import { test, expect } from '@playwright/test';

test('user signup flow', async ({ page }) => {
  await page.goto('/signup');

  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.fill('[name="confirmPassword"]', 'password123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/verify-email');
  await expect(page.locator('h1')).toContainText('Check your email');
});
```

### Selenium

```typescript
import { Builder, By, until } from 'selenium-webdriver';

test('user signup flow', async () => {

## References

For detailed information, see:

- `references/detailed-guide.md` - Complete workflow details, examples, and troubleshooting
