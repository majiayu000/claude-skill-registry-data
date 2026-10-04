---
name: testing:e2e-tests
description: |
  Create end-to-end tests using Playwright for user workflows.
  Use when testing user interactions, authentication flows, or full feature testing.
disable-model-invocation: false
allowed-tools: Read Write Edit Bash Grep Glob
---

# E2E Test Creation

Create Playwright E2E tests for user workflows.

## Usage

- `/testing:e2e-tests [feature]` - Create E2E tests for feature
- `/testing:e2e-tests status` - Check E2E coverage status

## Test Structure

```typescript
import { expect, test } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    test.setTimeout(120000);
    // Setup: login, navigate, etc.
  });

  test('should perform action', async ({ page }) => {
    // Arrange
    await page.goto('/feature');

    // Act
    await page.click('[data-testid="button"]');

    // Assert
    await expect(page.locator('.result')).toBeVisible();
  });
});
```

## Test Categories

```
tests/e2e/
├── smoke/      # Critical health checks
├── auth/       # Authentication flows
├── core/       # Core feature workflows
└── utils/      # Helper utilities
```

## Server Management

```bash
# Start server
nohup <dev-command> > dev.log 2>&1 &

# Verify ready
curl -s http://localhost:<port> | head -1

# Run tests
<playwright-runner> tests/e2e/[category]/[test]

# CRITICAL: Stop server after
pkill -f "<dev-process>"
```

## Priority Tags

- `@critical` - Must pass for release
- `@high` - Important functionality
- `@medium` - Secondary features
- `@low` - Nice to have

## Best Practices

- E2E tests should only cover what unit tests cannot: full user journeys, real API integration, auth flows, navigation
- Use structural assertions over content assertions to prevent flaky tests
- Use `storageState` for auth tests (login once, reuse) instead of per-test UI login
- Keep timeouts reasonable but generous for CI
