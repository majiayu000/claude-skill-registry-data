---
name: playwright-testing
description: Enhanced testing infrastructure with TestContext and Page Objects for Playwright. Covers E2E testing patterns, accessibility testing, API testing, and best practices for maintainable test organization.
---

# Playwright Testing

## MCP Tools Available

- `mcp__microsoft-playwright-mcp__browser_*` - Browser automation and interaction
- `mcp__microsoft-playwright-mcp__browser_navigate` - Navigate to URLs
- `mcp__microsoft-playwright-mcp__browser_click` - Click elements on page
- `mcp__microsoft-playwright-mcp__browser_type` - Type text into fields
- `mcp__microsoft-playwright-mcp__browser_snapshot` - Capture accessibility snapshots
- `mcp__microsoft-playwright-mcp__browser_take_screenshot` - Take screenshots
- `mcp__microsoft-playwright-mcp__browser_evaluate` - Execute JavaScript
- `mcp__microsoft-playwright-mcp__browser_console_messages` - Get console messages

## Testing Infrastructure Overview

This project uses an enhanced Playwright testing infrastructure with:

### Core Abstractions

- **TestContext** - Centralized test resource management with automatic cleanup
- **ApiClient** - Fluent API client with typed responses and assertion chaining
- **BasePage** - Rich base class with common UI patterns and accessibility support
- **Page Objects** - Specialized page classes extending BasePage

### Test Organization

```
tests/
├── e2e/           # End-to-end browser tests
├── api/           # API endpoint tests
├── integration/   # Service integration tests
├── unit/          # Unit tests with Vitest
├── pages/         # Page Object Models
├── helpers/       # Test utilities and infrastructure
└── fixtures/      # Test data and mocks
```

## TestContext Pattern

TestContext provides centralized resource management for tests, handling user creation, cleanup, and database operations.

```typescript
import { TestContext } from '../helpers';

let ctx: TestContext;

test.beforeAll(async () => {
  ctx = new TestContext({ autoCleanup: true });
});

test.afterAll(async () => {
  await ctx.cleanup();
});

test('creates user with subscription', async () => {
  const user = await ctx.createUser({
    subscription: 'active',
    tier: 'pro',
    credits: 500,
  });

  // Test with user...
  // Cleanup handled automatically
});

test('creates multiple users for collaboration scenario', async () => {
  const [owner, collaborator] = await ctx.createUsers(2, {
    subscription: 'active',
    tier: 'pro',
  });

  // Test multi-user scenario...
});
```

### TestContext Features

- **User Management**: Create users with different subscription tiers
- **Automatic Cleanup**: Automatic resource cleanup after tests
- **Database Access**: Direct Supabase admin client access
- **Resource Tracking**: Track and clean up all created resources
- **Mock User Support**: Fallback to mock users in test environment

## ApiClient with Fluent Assertions

ApiClient provides a fluent interface for API testing with built-in response validation.

```typescript
import { ApiClient } from '../helpers';

test('API endpoint with authentication', async ({ request }) => {
  const api = new ApiClient(request).withAuth(user.token);

  const response = await api.post('/api/checkout', { priceId: 'price_123' });

  // Fluent assertions
  response.expectStatus(200).expectSuccess();
  await response.expectData({ url: expect.any(String) });
});

test('API error handling', async ({ request }) => {
  const api = new ApiClient(request);

  const response = await api.post('/api/protected', {});

  response.expectStatus(401).expectError();
  await response.expectErrorCode('UNAUTHORIZED');
});
```

### ApiClient Features

- **Typed Responses**: Generic type support for response data
- **Fluent Assertions**: Chainable assertion methods
- **Authentication**: Built-in bearer token support
- **Error Handling**: Structured error response validation
- **Headers/Params**: Easy header and parameter management

## Enhanced Page Objects

Page Objects extend BasePage to get common UI patterns and accessibility support.

```typescript
import { LoginPage } from '../pages/LoginPage';

test('login flow with enhanced page object', async ({ page }) => {
  const loginPage = new LoginPage(page);

  await loginPage.goto('/');
  await loginPage.openLoginModal();
  await loginPage.assertModalVisible();

  // Enhanced base methods available
  await loginPage.checkBasicAccessibility();
  await loginPage.waitForLoadingComplete();
  await loginPage.fillFieldByLabel('Email', 'test@example.com');
  await loginPage.fillFieldByLabel('Password', 'password123');
  await loginPage.clickButton('Sign In');
});
```

### BasePage Features

#### Navigation & Page Management

```typescript
const page = new BasePage(pageInstance);

await page.goto('/dashboard'); // Navigate with network idle wait
await page.waitForURL('/dashboard'); // Wait for URL pattern
await page.reload(); // Reload and wait for stability
await page.waitForPageLoad(); // Wait for full page load
```

#### Modal Handling

```typescript
await page.waitForModal(); // Wait for modal to appear
await page.clickModalButton('Submit'); // Click button in modal
await page.closeModal(); // Close modal (escape/backdrop)
await page.isModalVisible(); // Check modal visibility
```

#### Toast/Notification Management

```typescript
await page.waitForToast('Success'); // Wait for specific toast
await page.dismissToast(); // Dismiss any toast
await page.isToastVisible('Error'); // Check toast visibility
```

#### Form Interactions

```typescript
await page.fillField('Email', 'user@example.com');
await page.fillFieldByLabel('Password', 'secret');
await page.clickButton('Submit');
await page.selectOption('Country', 'United States');
await page.checkCheckbox('Remember me');
```

#### Loading States

```typescript
await page.waitForLoadingComplete(); // Wait for spinners to disappear
await page.waitForAuthLoadingComplete(); // Wait for auth loading
await page.waitForNetworkIdle(); // Wait for network idle
```

#### Network Request Handling

```typescript
const response = await page.waitForApiResponse('/api/user');
await page.waitForApiRequest('/api/log');
const responses = await page.waitForMultipleApiResponses(['/api/user', '/api/credits']);
```

#### Accessibility Testing

```typescript
await page.checkBasicAccessibility(); // Basic a11y checks
await page.checkAriaLabels(); // ARIA label validation
```

## E2E Test Patterns

### Critical User Journey Testing

```typescript
test('complete upscaler workflow', async ({ page }) => {
  const ctx = new TestContext();
  const user = await ctx.createUser({ subscription: 'active', credits: 100 });
  const upscalerPage = new UpscalerPage(page);

  await upscalerPage.goto('/');
  await upscalerPage.signIn(user.token);
  await upscalerPage.uploadImage('./test-assets/image.jpg');
  await upscalerPage.selectModel('realistic');
  await upscalerPage.startUpscaling();
  await upscalerPage.waitForCompletion();
  await upscalerPage.downloadResult();

  await ctx.cleanup();
});
```

### Mobile/Responsive Testing

```typescript
test('mobile upscaller experience', async ({ page }) => {
  // Configure mobile viewport
  await page.setViewportSize({ width: 375, height: 667 });

  const upscalerPage = new UpscalerPage(page);
  await upscalerPage.goto('/');

  // Test mobile-specific interactions
  await upscalerPage.openMobileMenu();
  await upscalerPage.uploadImageMobile('./test-assets/image.jpg');
  await upscalerPage.verifyMobileUI();
});
```

### Accessibility Testing Integration

```typescript
test('upscaler accessibility compliance', async ({ page }) => {
  const upscalerPage = new UpscalerPage(page);

  await upscalerPage.goto('/');
  await upscalerPage.checkBasicAccessibility();

  // Navigate through flow checking a11y at each step
  await upscalerPage.uploadImage('./test-assets/image.jpg');
  await upscalerPage.checkAriaLabels();
  await upscalerPage.selectModel('realistic');
  await upscalerPage.checkKeyboardNavigation();
});
```

## API Testing Patterns

### Authentication Testing

```typescript
test('protected endpoints require authentication', async ({ request }) => {
  const api = new ApiClient(request);

  // Test without auth
  await api
    .get('/api/user')
    .then(response => response.expectStatus(401).expectErrorCode('UNAUTHORIZED'));

  // Test with valid auth
  const authenticatedApi = api.withAuth(user.token);
  await authenticatedApi
    .get('/api/user')
    .then(response => response.expectStatus(200).expectSuccess());
});
```

### Webhook Testing

```typescript
import { WebhookClient } from '../helpers';

test('stripe webhook processing', async ({ request }) => {
  const webhookClient = new WebhookClient(request);

  const event = webhookClient.createStripeEvent('invoice.payment_succeeded', {
    customer: 'cus_123',
    amount_paid: 2000,
  });

  const response = await webhookClient.send('/api/webhooks/stripe', event);

  response.expectStatus(200);
  await response.expectWebhookResponse({ received: true });
});
```

### Error Scenario Testing

```typescript
test('API error responses are properly formatted', async ({ request }) => {
  const api = new ApiClient(request).withAuth(user.token);

  // Test validation errors
  await api.post('/api/checkout', { invalidData: true }).then(response =>
    response
      .expectStatus(400)
      .expectError()
      .expectErrorCode('VALIDATION_ERROR')
      .expectErrorMessage(/required/)
  );

  // Test rate limiting
  await api
    .get('/api/rate-limited')
    .then(response =>
      response
        .expectStatus(429)
        .expectErrorCode('RATE_LIMITED')
        .expectHeaders({ 'retry-after': '60' })
    );
});
```

## Integration Testing Patterns

### Database Integration

```typescript
test('user credit deduction workflow', async () => {
  const ctx = new TestContext();
  const user = await ctx.createUser({ credits: 100 });

  // Perform action that should deduct credits
  const result = await deductCredits(user.id, 50);

  // Verify database state
  const updatedUser = await ctx.supabaseAdmin
    .from('user_credits')
    .select('credits')
    .eq('user_id', user.id)
    .single();

  expect(updatedUser.data.credits).toBe(50);

  await ctx.cleanup();
});
```

### Service Integration

```typescript
test('stripe subscription integration', async () => {
  const ctx = new TestContext();
  const user = await ctx.createUser({ subscription: 'active' });

  // Test subscription change
  const result = await changeSubscription(user.id, 'pro');

  // Verify both local database and Stripe
  const localSubscription = await ctx.data.getUserSubscription(user.id);
  expect(localSubscription.tier).toBe('pro');

  const stripeCustomer = await getStripeCustomer(user.id);
  expect(stripeCustomer.subscription?.tier).toBe('pro');

  await ctx.cleanup();
});
```

## Best Practices

### Test Organization

1. **Use TestContext** for all user lifecycle management
2. **Extend BasePage** for all page objects to get common patterns
3. **Group related tests** in describe blocks with clear descriptions
4. **Use descriptive test names** that explain the behavior being tested

### Test Data Management

```typescript
// Good: Use TestContext for user management
let ctx: TestContext;
beforeAll(async () => {
  ctx = new TestContext();
});
afterAll(async () => {
  await ctx.cleanup();
});

// Good: Use UserFactory for complex setups
const user = await UserFactory.create()
  .withSubscription('active', 'pro')
  .withCredits(1000)
  .withProfile({ name: 'Test User' })
  .build();

// Avoid: Hardcoded test data
const userId = '123e4567-e89b-12d3-a456-426614174000';
```

### Assertion Patterns

```typescript
// Good: Fluent assertions with ApiClient
await api
  .post('/api/endpoint', data)
  .expectStatus(200)
  .expectSuccess()
  .expectData({ id: expect.any(String) });

// Good: Page object assertions
await upscalerPage.assertUploadSuccess();
await upscalerPage.assertCreditsDeducted(50);

// Avoid: Manual JSON parsing and assertions
const response = await api.post('/api/endpoint', data);
const data = await response.json();
expect(response.status()).toBe(200);
expect(data.success).toBe(true);
expect(data.data.id).toBeDefined();
```

### Error Handling

```typescript
// Good: Test both success and error scenarios
test('successful request', async () => {
  const response = await api.post('/api/valid', validData);
  response.expectStatus(200).expectSuccess();
});

test('invalid request handling', async () => {
  const response = await api.post('/api/valid', invalidData);
  response.expectStatus(400).expectErrorCode('VALIDATION_ERROR');
});

// Good: Test rate limiting behavior
test('rate limiting', async () => {
  // Make rapid requests
  const responses = await Promise.all([
    api.get('/api/rate-limited'),
    api.get('/api/rate-limited'),
    api.get('/api/rate-limited'),
  ]);

  // At least one should be rate limited
  expect(responses.some(r => r.status === 429)).toBe(true);
});
```

### Accessibility Testing

```typescript
// Good: Include accessibility checks in E2E tests
test('user journey with accessibility', async ({ page }) => {
  const loginPage = new LoginPage(page);

  await loginPage.goto('/');
  await loginPage.checkBasicAccessibility();

  await loginPage.signIn(user);
  await loginPage.checkAriaLabels();

  // Continue with flow...
});

// Good: Test keyboard navigation
test('keyboard navigation support', async ({ page }) => {
  await page.keyboard.press('Tab'); // Navigate to next element
  await page.keyboard.press('Enter'); // Activate focused element
  await page.keyboard.press('Escape'); // Close modal/dropdown
});
```

## Running Tests

### Individual Test Types

```bash
# E2E tests (Chrome desktop)
yarn test:e2e

# Mobile/tablet tests
yarn test:mobile

# API tests
yarn test:api

# Integration tests
yarn test:integration

# Unit tests
yarn test:unit
```

### Specific Test Files

```bash
# Run specific test file
yarn playwright tests/e2e/upscaler.e2e.spec.ts

# Run with specific reporter
yarn playwright --reporter=html tests/e2e/upscaler.e2e.spec.ts

# Run in debug mode
yarn playwright --debug tests/e2e/upscaler.e2e.spec.ts
```

### Test Configuration

The project uses a sophisticated Playwright configuration with:

- **Dynamic Ports**: Random test ports to avoid conflicts
- **Device Simulation**: Mobile, tablet, and desktop testing
- **Parallel Execution**: Optimized worker counts for CI/local
- **Automatic Server**: Built-in test server management
- **Trace Retention**: Debug traces on failure only

### Environment Variables

```bash
# Test environment (loaded from .env.test)
TEST_PORT=3101                    # Dynamic test server port
TEST_WRANGLER_PORT=8801          # Workers preview port
ENV=test                         # Test environment flag

# Supabase test configuration
SUPABASE_URL_TEST=               # Test Supabase instance
SUPABASE_SERVICE_KEY_TEST=       # Test service key
```

## Debugging Tests

### Screenshots and Traces

```typescript
// Manual screenshot
await page.screenshot('test-scenario', { fullPage: true });

// Automatic screenshot on failure (configured in playwright.config.ts)
// Screenshots saved to test-results/screenshots/

// Trace files for debugging
// Access via HTML report: test-results/index.html
```

### Console Messages

```typescript
// Check for JavaScript errors
const errors = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('div.error')).map(el => el.textContent);
});

// Browser console logs
const consoleMessages = await page.evaluate(() => {
  return window.consoleMessages || [];
});
```

### Network Debugging

```typescript
// Wait for specific API call
const response = await page.waitForApiResponse('/api/upscale');
console.log('API Response:', await response.json());

// Monitor all network requests
page.on('request', request => {
  console.log('Request:', request.url());
});

page.on('response', response => {
  console.log('Response:', response.status(), response.url());
});
```

## Advanced Patterns

### Custom Matchers

```typescript
// Extend expect with custom matchers
expect.extend({
  async toHaveAccessibleLabel(page, expectedLabel) {
    const element = page.locator(`[aria-label="${expectedLabel}"]`);
    const isVisible = await element.isVisible();
    return {
      pass: isVisible,
      message: () => `Expected element with label "${expectedLabel}" to be visible`,
    };
  },
});

// Use custom matcher
await expect(page).toHaveAccessibleLabel('Upload image');
```

### Test Utilities

```typescript
// Create reusable test utilities
class TestUtils {
  static async createAuthenticatedUser(ctx: TestContext) {
    const user = await ctx.createUser({ subscription: 'active' });
    return { user, apiClient: new ApiClient(request).withAuth(user.token) };
  }

  static async simulateFileUpload(page, fileName: string) {
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(fileName);
  }
}
```

### Performance Testing

```typescript
test('page load performance', async ({ page }) => {
  const startTime = Date.now();

  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');

  const loadTime = Date.now() - startTime;
  expect(loadTime).toBeLessThan(3000); // 3 second threshold
});
```

This enhanced testing infrastructure provides a solid foundation for maintaining high-quality, reliable tests while minimizing test maintenance overhead through reusable patterns and abstractions.
