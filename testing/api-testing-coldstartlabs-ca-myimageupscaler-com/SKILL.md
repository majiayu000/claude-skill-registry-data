---
name: api-testing
description: Write and maintain Playwright API and integration tests for this codebase using ApiClient, TestContext, TestDataManager, authentication helpers, and fluent request/response assertions.
---

# API Testing Skill

When writing API tests for this codebase, follow the established patterns using the ApiClient helper and supertest-style assertions.

## Overview

- **Framework**: Playwright API tests (`tests/api/*.api.spec.ts`)
- **Helper**: `ApiClient` - fluent, type-safe API client with chainable assertions
- **Test Context**: `TestContext` - centralized resource management with automatic cleanup
- **Data Manager**: `TestDataManager` - direct Supabase operations for test data

## Directory Structure

```
tests/
├── api/              # API route tests (.api.spec.ts)
├── integration/      # Integration tests (.integration.spec.ts)
├── unit/api/         # API-related unit tests (.unit.spec.ts)
├── helpers/
│   ├── ApiClient.ts  # Fluent API testing client
│   ├── TestContext.ts # Centralized resource management
│   └── TestDataManager.ts # Direct database operations
```

---

## ApiClient: Basic Usage

### Simple Request

```typescript
import { test, expect } from '@tests/e2e/fixtures';
import { ApiClient } from '@tests/helpers/ApiClient';

test.describe('API: Health Check', () => {
  test('should return 200 OK with status', async ({ request }) => {
    const api = new ApiClient(request);
    const response = await api.get('/api/health');

    response.expectStatus(200);
    response.expectData({ status: 'ok' });
  });
});
```

### Fluent Assertions

```typescript
const response = await api.post('/api/upscale', payload);

// Chain multiple expectations
response
  .expectStatus(200)
  .expectSuccess()
  .expectData({ url: expect.any(String) })
  .expectHeader('content-type', /json/);

// Check error codes
response.expectErrorCode('INSUFFICIENT_CREDITS');

// Async data checks
await response.expectData(async data => {
  expect(data.url).toMatch(/^https:\/\//);
});
```

### All HTTP Methods

```typescript
await api.get('/api/users');
await api.post('/api/users', { name: 'John' });
await api.put('/api/users/123', { name: 'Jane' });
await api.patch('/api/users/123', { name: 'Jane' });
await api.delete('/api/users/123');
```

---

## Authentication Patterns

### Unauthenticated Request

```typescript
test('should reject access without authentication', async ({ request }) => {
  const api = new ApiClient(request);
  const response = await api.post('/api/upscale', testData);
  response.expectStatus(401);
});
```

### Authenticated Request

```typescript
test('should allow access with valid authentication', async ({ request }) => {
  const user = await ctx.createUser();
  const api = new ApiClient(request).withAuth(user.token);
  const response = await api.post('/api/upscale', testData);
  expect([401, 403]).not.toContain(response.status);
});
```

### Reusing Authenticated Client

```typescript
let api: ApiClient;

test.beforeAll(async () => {
  const user = await ctx.createUser();
  api = new ApiClient(request).withAuth(user.token);
});

test('should work with authenticated request', async () => {
  const response = await api.get('/api/user/profile');
  response.expectStatus(200);
});
```

---

## TestContext for Resource Management

### Basic Setup

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

### User Factory Patterns

```typescript
// Simple user
const user = await ctx.createUser();

// Fluent builder API
const user = await ctx
  .createUser()
  .withSubscription('active', 'pro')
  .withCredits(500)
  .withEmail('test@example.com')
  .build();

// Preset configurations
const proUser = await ctx.userFactory.proUser(500);
const businessUser = await ctx.userFactory.businessUser(1000);
const trialingUser = await ctx.userFactory.trialingUser('business');

// Multiple users
const users = await ctx.userFactory.createMany('pro', 5);
```

### Direct Supabase Access

```typescript
// TestContext provides admin Supabase client
const { data: profile } = await ctx.supabase.from('profiles').select('*').eq('id', userId).single();
```

---

## TestDataManager for Database Operations

```typescript
import { TestDataManager } from '@tests/helpers/TestDataManager';

const dataManager = new TestDataManager();

// Create users
const user = await dataManager.createTestUser();
const userWithPass = await dataManager.createTestUser({ email, password });

// Manage subscriptions
await dataManager.setSubscriptionStatus(userId, 'active', 'pro');

// Credit management
await dataManager.addCredits(userId, 100, 'bonus');
await dataManager.deductCredits(userId, 50, 'processing');

// Cleanup
await dataManager.cleanupUser(userId);
await dataManager.cleanupAllUsers();
```

---

## Common API Test Patterns

### Rate Limiting Tests

```typescript
test('should apply rate limiting to protected routes', async ({ request }) => {
  const user = await ctx.createUser();
  const api = new ApiClient(request).withAuth(user.token);

  const responses = [];
  for (let i = 0; i < 15; i++) {
    const response = await api.post('/api/upscale', testData);
    responses.push(response);
  }

  const rateLimitedCount = responses.filter(r => r.status === 429).length;
  if (rateLimitedCount > 0) {
    expect(responses.find(r => r.status === 429)?.raw.headers()['retry-after']).toBeDefined();
  }
});
```

### Validation Tests

```typescript
test('should reject invalid input', async ({ request }) => {
  const user = await ctx.createUser();
  const api = new ApiClient(request).withAuth(user.token);

  const response = await api.post('/api/upscale', {
    imageData: 'invalid',
    mimeType: 'not-a-mime-type',
  });

  response.expectStatus(400);
  response.expectErrorCode('VALIDATION_ERROR');
});
```

### Error Code Tests

```typescript
test('should return insufficient credits error', async ({ request }) => {
  const user = await ctx.createUser({ credits: 0 });
  const api = new ApiClient(request).withAuth(user.token);

  const response = await api.post('/api/upscale', testData);
  response.expectStatus(402);
  response.expectErrorCode('INSUFFICIENT_CREDITS');
});
```

### Integration Workflow Tests

```typescript
test.describe('Authentication Flow Integration', () => {
  test('should handle login with valid credentials', async ({ request }) => {
    const api = new ApiClient(request);
    const testUser = await ctx.createUser();

    const loginResponse = await api.post('/api/auth/login', {
      email: testUser.email,
      password: 'test-password-123',
    });

    expect(loginResponse.ok).toBeTruthy();
    const { session } = await loginResponse.json();

    // Test token usage
    const authenticatedApi = api.withAuth(session.access_token);
    const protectedResponse = await authenticatedApi.get('/api/protected/example');
    expect(protectedResponse.ok).toBeTruthy();
  });
});
```

---

## Unit Testing API Handlers

```typescript
import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';

describe('Stripe Webhook Handler', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test('should handle invoice.payment_succeeded', async () => {
    // Mock dependencies
    vi.mock('@server/stripe', () => ({
      stripe: {
        webhooks: {
          constructEventAsync: vi.fn(),
        },
      },
    }));

    // Use dynamic import for fresh module
    const { handleInvoicePaymentSucceeded } = await import('./handler');

    const result = await handleInvoicePaymentSucceeded(mockEvent);

    expect(result.success).toBeTruthy();
  });
});
```

---

## Common Pitfalls to Avoid

### 1. Hardcoded Configuration Values

**Bad**: Tests fail when config changes

```typescript
const response = await api.post('/api/subscription', {
  priceId: 'price_123abc', // Hardcoded - will break when config changes
});
```

**Good**: Import actual config values

```typescript
import { stripeConfig } from '@server/config/stripe';

const response = await api.post('/api/subscription', {
  priceId: stripeConfig.prices.pro.monthly,
});
```

### 2. Outdated Payload Schemas

APIs evolve - keep test payloads in sync with current validation:

```typescript
// Old format
const payload = { quality: 'high', scale: 2 };

// New format (check actual API schema!)
const payload = { qualityTier: 'premium', scale: 2 };
```

### 3. Missing Cleanup

Always clean up test resources to avoid flaky tests:

```typescript
let ctx: TestContext;

test.beforeAll(async () => {
  ctx = new TestContext();
});

test.afterAll(async () => {
  await ctx.cleanup(); // Don't forget this!
});
```

### 4. Not Testing Error Paths

Don't only test happy paths - test error scenarios:

```typescript
test('should handle errors properly', async ({ request }) => {
  const api = new ApiClient(request);
  const response = await api.post('/api/endpoint', invalidData);
  response.expectStatus(400);
  response.expectErrorCode('VALIDATION_ERROR');
});
```

---

## Best Practices

### Test Naming

- Use descriptive names: `"should return 200 OK with status"`
- Group by feature: `test.describe('API: Health Check')`
- Cover error scenarios: `"should reject invalid credentials"`

### Test Structure

```typescript
test.describe('Feature Name', () => {
  let ctx: TestContext;

  test.beforeAll(async () => {
    ctx = new TestContext();
  });

  test.afterAll(async () => {
    await ctx.cleanup();
  });

  test.describe('Sub-feature', () => {
    test('specific behavior', async ({ request }) => {
      const api = new ApiClient(request);
      // Test implementation
    });
  });
});
```

### Code Quality Standards

- **80%+ coverage target**
- **Mock all external dependencies** in unit tests
- **Comprehensive error testing**
- **Test both success and failure paths**

---

## Testing Commands

```bash
# Run all API tests
yarn test:api

# Run specific test file
yarn test tests/api/upscale.api.spec.ts

# Run integration tests
yarn test:integration

# Run with coverage
yarn test:coverage

# Full verification suite
yarn verify
```

---

## Before Finishing

1. **Write tests** for your changes following the patterns above
2. **Run tests** on affected areas: `yarn test:api` or `yarn test:integration`
3. **Run verify**: `yarn verify` (required before completing any task)

## Key Files to Reference

- `tests/helpers/ApiClient.ts` - Fluent API testing client
- `tests/helpers/TestContext.ts` - Centralized test resource management
- `tests/helpers/TestDataManager.ts` - Direct database operations
- `playwright.config.ts` - Playwright configuration (api, integration projects)
