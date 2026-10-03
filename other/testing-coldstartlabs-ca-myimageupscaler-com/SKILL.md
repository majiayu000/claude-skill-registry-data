---
name: testing
description: Use the codebase testing strategy across Vitest unit tests and Playwright API, integration, and E2E tests, including when to choose each test type and related local testing patterns.
---

# Testing Overview

This codebase uses a multi-layered testing strategy with Vitest for unit tests and Playwright for integration, API, and E2E tests.

## Quick Reference

| Test Type   | File Pattern            | Framework  | Command                 | Skill                                |
| ----------- | ----------------------- | ---------- | ----------------------- | ------------------------------------ |
| Unit        | `*.unit.spec.ts`        | Vitest     | `yarn test:unit`        | [unit-testing.md](./unit-testing.md) |
| API         | `*.api.spec.ts`         | Playwright | `yarn test:api`         | [api-testing.md](./api-testing.md)   |
| E2E         | `*.e2e.spec.ts`         | Playwright | `yarn test:e2e`         | [e2e-testing.md](./e2e-testing.md)   |
| Integration | `*.integration.spec.ts` | Playwright | `yarn test:integration` | [api-testing.md](./api-testing.md)   |

---

## When to Use Each Skill

### Unit Testing (`unit-testing.md`)

Use when:

- Testing individual functions, services, utilities
- Testing React components with React Testing Library
- Testing API handlers in isolation
- Need to mock external dependencies (Stripe, Supabase, etc.)

**Key patterns**: Dynamic imports, vi.mock, module caching avoidance

### API Testing (`api-testing.md`)

Use when:

- Testing API routes and endpoints
- Testing authentication/authorization
- Testing rate limiting and validation
- Testing complete request/response cycles

**Key patterns**: ApiClient fluent assertions, TestContext user factory

### E2E Testing (`e2e-testing.md`)

Use when:

- Testing user flows across multiple pages
- Testing UI interactions and navigation
- Testing accessibility
- Testing mobile/responsive behavior

**Key patterns**: BasePage pattern, Playwright fixtures, accessibility checks

---

## Directory Structure

```
tests/
├── unit/             # Unit tests (.unit.spec.ts)
├── api/              # API route tests (.api.spec.ts)
├── e2e/              # End-to-end tests (.e2e.spec.ts)
├── integration/      # Integration tests (.integration.spec.ts)
├── pages/            # Page object models
├── helpers/          # Test utilities
│   ├── ApiClient.ts
│   ├── TestContext.ts
│   └── TestDataManager.ts
├── fixtures/         # Test data
├── test-fixtures.ts  # Playwright extensions
└── vitest.setup.tsx  # RTL setup
```

---

## Common Testing Concepts

### TestContext

Centralized resource management used across API and E2E tests:

```typescript
let ctx: TestContext;

test.beforeAll(async () => {
  ctx = new TestContext();
});

test.afterAll(async () => {
  await ctx.cleanup();
});
```

### User Factory

Create test users with specific configurations:

```typescript
// Simple
const user = await ctx.createUser();

// Fluent
const user = await ctx.createUser().withSubscription('active', 'pro').withCredits(500).build();

// Presets
const proUser = await ctx.userFactory.proUser(500);
```

---

## Testing Commands

```bash
# All tests
yarn test

# By type
yarn test:unit          # Vitest unit tests
yarn test:api           # Playwright API tests
yarn test:e2e           # Playwright E2E tests
yarn test:integration   # Playwright integration tests

# Development
yarn test:watch         # Vitest watch mode
yarn test:e2e:ui        # Playwright UI mode
yarn test:e2e:debug     # Playwright debug mode
yarn test:coverage      # Coverage report

# Verification (run before committing)
yarn verify
```

---

## Configuration Files

- `vitest.config.ts` - Vitest configuration (jsdom, path aliases)
- `playwright.config.ts` - Playwright projects (chromium, mobile, api, integration)
- `vitest.setup.tsx` - React Testing Library setup

---

## Coverage Targets

- **Unit tests**: Pure functions, services, utilities, components
- **API tests**: All endpoints, auth, rate limiting, validation
- **E2E tests**: Critical user flows, accessibility, mobile
- **Integration tests**: Complete workflows across systems

Target: **80%+ overall coverage**

---

## Before Finishing Any Task

1. **Write tests** for your changes using the appropriate skill
2. **Run tests** on affected areas
3. **Run verify**: `yarn verify` (required before completing)

---

## Related Skills

- **[unit-testing.md](./unit-testing.md)** - Unit testing with Vitest
- **[api-testing.md](./api-testing.md)** - API testing with ApiClient
- **[e2e-testing.md](./e2e-testing.md)** - E2E testing with Playwright
- **[test-fixing.md](./test-fixing.md)** - Fixing failing tests (debugging methodology)
