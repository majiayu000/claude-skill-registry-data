---
name: e2e-testing
description: Write and maintain Playwright end-to-end browser tests for this codebase using page objects, BasePage patterns, TestContext, fixtures, accessibility checks, mobile coverage, and user-flow assertions.
---

# E2E Testing Skill

When writing E2E/client tests for this codebase, follow the established patterns using Playwright and the BasePage pattern.

## Overview

- **Framework**: Playwright E2E tests (`tests/e2e/*.e2e.spec.ts`)
- **Pattern**: Enhanced Page Object Model with `BasePage` class
- **Test Context**: `TestContext` - centralized resource management
- **Fixtures**: Extended Playwright fixtures in `tests/test-fixtures.ts`

## Directory Structure

```
tests/
├── e2e/              # End-to-end browser tests (.e2e.spec.ts)
├── pages/            # Page object models
│   └── BasePage.ts   # Base class with common UI patterns
├── helpers/
│   └── TestContext.ts # User factory and cleanup
└── test-fixtures.ts  # Playwright fixture extensions
```

---

## BasePage Pattern

All page objects extend `BasePage` for common functionality:

```typescript
import { BasePage } from '@tests/pages/BasePage';

export class LoginPage extends BasePage {
  // Locators
  get googleSignInButton(): Locator {
    return this.page.getByRole('button', { name: 'Continue with Google' });
  }

  get emailInput(): Locator {
    return this.page.getByPlaceholder(/email/i);
  }

  // Actions
  async openLoginModal(): Promise<void> {
    await this.signInButton.click();
    await this.waitForModal();
  }

  async fillLoginForm(email: string, password: string): Promise<void> {
    await this.fillField(/email/i, email);
    await this.fillField(/password/i, password);
  }

  async submitForm(): Promise<void> {
    await this.clickButton('Sign In');
  }

  // Assertions
  async assertModalVisible(): Promise<void> {
    await expect(this.modal).toBeVisible();
  }
}
```

---

## BasePage Available Methods

### Navigation

```typescript
await page.goto('/'); // Navigate to path
await page.waitForURL('/dashboard'); // Wait for URL
```

### Modal Handling

```typescript
await this.waitForModal(); // Wait for modal to appear
await this.closeModal(); // Close active modal
await this.clickModalButton('Submit'); // Click button in modal
```

### Toast/Notifications

```typescript
await this.waitForToast('Success!'); // Wait for toast with text
await this.dismissToast(); // Dismiss active toast
```

### Loading States

```typescript
await this.waitForLoadingComplete(); // Wait for page load
await this.waitForAuthLoadingComplete(); // Wait for auth load
```

### Network Handling

```typescript
await this.waitForApiResponse('/api/user'); // Wait for API response
await this.waitForApiRequest('/api/upscale'); // Wait for API request
```

### Form Helpers

```typescript
await this.fillField(/email/i, 'test@example.com');
await this.selectOption(/country/i, 'United States');
```

### Accessibility

```typescript
await this.checkBasicAccessibility(); // Basic a11y checks
await this.checkAriaLabels(); // Verify ARIA labels
```

---

## Writing E2E Tests

### Basic Test Structure

```typescript
import { test, expect } from '@tests/e2e/fixtures';
import { LoginPage } from '@tests/pages/LoginPage';

test.describe('Authentication', () => {
  test('should show login form when clicking sign in', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto('/');
    await loginPage.openLoginModal();
    await loginPage.assertModalVisible();
  });
});
```

### TestContext Setup

```typescript
import { TestContext } from '@tests/helpers/TestContext';

let ctx: TestContext;

test.beforeAll(async () => {
  ctx = new TestContext();
});

test.afterAll(async () => {
  await ctx.cleanup();
});
```

### User Factory

```typescript
// Simple user
const user = await ctx.createUser();

// Fluent builder API
const user = await ctx.createUser().withSubscription('active', 'pro').withCredits(500).build();

// Preset configurations
const proUser = await ctx.userFactory.proUser(500);
const businessUser = await ctx.userFactory.businessUser(1000);
```

---

## Common E2E Test Patterns

### Form Submission

```typescript
test('should submit login form', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto('/');

  await loginPage.openLoginModal();
  await loginPage.fillLoginForm('user@example.com', 'password123');
  await loginPage.submitForm();

  await loginPage.waitForToast('Welcome back!');
});
```

### Navigation

```typescript
test('should navigate to dashboard', async ({ page }) => {
  const dashboardPage = new DashboardPage(page);
  await dashboardPage.goto('/');
  await dashboardPage.clickNavLink('Dashboard');
  await dashboardPage.waitForURL('/dashboard');
});
```

### Loading States

```typescript
test('should show loading state during upload', async ({ page }) => {
  const uploadPage = new UploadPage(page);
  await uploadPage.goto('/upload');

  await uploadPage.uploadImage(testImage);
  await uploadPage.waitForLoadingComplete();

  await expect(uploadPage.resultPreview).toBeVisible();
});
```

### Network Requests

```typescript
test('should handle API errors gracefully', async ({ page }) => {
  const uploadPage = new UploadPage(page);

  // Intercept and mock API response
  await page.route('**/api/upscale', route =>
    route.fulfill({ status: 500, body: '{"error":"Server error"}' })
  );

  await uploadPage.goto('/upload');
  await uploadPage.uploadImage(testImage);

  await uploadPage.waitForToast('Something went wrong');
});
```

### Keyboard Navigation

```typescript
test('should handle keyboard navigation properly', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto('/');
  await loginPage.openLoginModal();

  await page.keyboard.press('Tab');
  await expect(loginPage.emailInput).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(loginPage.passwordInput).toBeFocused();
});
```

---

## Accessibility Testing

Always include accessibility checks in E2E tests:

```typescript
test('should have proper accessibility attributes', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto('/');
  await loginPage.openLoginModal();

  // Check basic accessibility
  await loginPage.checkBasicAccessibility();

  // Check ARIA labels
  await loginPage.checkAriaLabels();
});
```

### Manual Accessibility Checks

```typescript
test('should be keyboard accessible', async ({ page }) => {
  const page = new BasePage(page);
  await page.goto('/');

  // Test Tab navigation
  await page.keyboard.press('Tab');
  // Verify focus indicator visible
});

test('should have proper ARIA labels', async ({ page }) => {
  await page.goto('/');

  const button = page.getByRole('button', { name: /submit/i });
  await expect(button).toHaveAttribute('aria-label', 'Submit form');
});
```

---

## Mobile Testing

The Playwright config includes mobile device projects. Tests automatically run on:

- **Desktop** (chromium)
- **Mobile iPhone** (iPhone 12)
- **Mobile Android** (Pixel 5)
- **Tablet** (iPad)

Write mobile-specific tests:

```typescript
test.describe('Mobile Navigation', () => {
  test('should show hamburger menu on mobile', async ({ page }) => {
    // This test runs on mobile devices
    const nav = new Navigation(page);
    await nav.goto('/');

    await expect(nav.hamburgerMenu).toBeVisible();
    await nav.openMobileMenu();
    await expect(nav.mobileMenuItems).toBeVisible();
  });
});
```

---

## Common Pitfalls to Avoid

### 1. Fragile Selectors

**Bad**: Text-based selectors break easily

```typescript
await page.click('Submit');
```

**Good**: Role-based selectors

```typescript
await page.getByRole('button', { name: 'Submit' }).click();
```

**Good**: Test IDs (most stable)

```typescript
await page.getByTestId('submit-button').click();
```

### 2. Hardcoded Waits

**Bad**: Fixed timeouts are flaky

```typescript
await page.waitForTimeout(2000);
```

**Good**: Wait for specific condition

```typescript
await page.waitForURL('/dashboard');
await expect(element).toBeVisible();
await this.waitForLoadingComplete();
```

### 3. Not Cleaning Up

Always clean up test data:

```typescript
let ctx: TestContext;

test.beforeAll(async () => {
  ctx = new TestContext();
});

test.afterAll(async () => {
  await ctx.cleanup(); // Don't forget this!
});
```

### 4. Skipping Accessibility

Don't skip accessibility checks:

```typescript
test('should work', async ({ page }) => {
  // Missing accessibility checks!
  await page.goto('/');
});

test('should work with accessibility', async ({ page }) => {
  await page.goto('/');
  await new BasePage(page).checkBasicAccessibility();
});
```

### 5. Ignoring Mobile

Don't only test desktop - tests run on all devices:

```typescript
// This runs on desktop AND mobile/tablet
test('should work on all devices', async ({ page }) => {
  await page.goto('/');
  // Test works on all screen sizes
});
```

---

## Best Practices

### Test Naming

- Use descriptive names: `"should show login form when clicking sign in"`
- Group by feature: `test.describe('Authentication')`
- Test user flows: `"should complete checkout flow"`

### Page Object Structure

```typescript
export class FeaturePage extends BasePage {
  // Locators (getters for lazy evaluation)
  get element(): Locator {
    return this.page.locator('...');
  }

  // Actions (async methods)
  async doSomething(): Promise<void> {}

  // Assertions (async methods with 'assert' prefix)
  async assertSomething(): Promise<void> {
    await expect(this.element).toBeVisible();
  }
}
```

### Selector Priority

1. **Test IDs** - Most stable: `getByTestId()`
2. **Role + Name** - Semantic: `getByRole('button', { name })`
3. **Labels/Placeholders** - Form inputs: `getByPlaceholder()`, `getByLabel()`
4. **Text** - Only when necessary: `getByText()`
5. **CSS** - Last resort: `locator()`

---

## Testing Commands

```bash
# Run all E2E tests
yarn test:e2e

# Run specific test file
yarn test:e2e tests/e2e/auth.e2e.spec.ts

# Playwright UI mode (interactive)
yarn test:e2e:ui

# Debug mode with inspector
yarn test:e2e:debug

# Run on specific device
yarn test:e2e --project=mobile-iphone

# Full verification suite
yarn verify
```

---

## Before Finishing

1. **Write tests** for your changes following the patterns above
2. **Run tests**: `yarn test:e2e`
3. **Check accessibility**: Include `checkBasicAccessibility()` in relevant tests
4. **Run verify**: `yarn verify` (required before completing any task)

## Key Files to Reference

- `tests/pages/BasePage.ts` - Base class with common UI patterns
- `tests/helpers/TestContext.ts` - User factory and cleanup
- `tests/test-fixtures.ts` - Playwright fixture extensions
- `tests/e2e/fixtures.ts` - Reusable test fixtures
- `playwright.config.ts` - Playwright configuration (devices, projects)
