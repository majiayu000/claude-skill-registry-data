---
name: playwright-network-mocking
description: Playwright workflows for deterministic third-party responses using page.route().
---

# Playwright Network Mocking

## Overview

Use this skill when a test depends on a slow, unreliable, or external service and you need deterministic responses without hitting the real provider. It lets you isolate the boundary that matters while keeping the rest of the application real.

Do not use this skill when the real third-party integration is the feature under test, or when the app is already local and deterministic without request interception.

## When to Use

- When a test depends on an unreliable or slow external API.
- When you need deterministic responses for billing, email, auth, analytics, or similar services.
- When you want to mock the minimum necessary surface area and leave the rest of the app untouched.

## When Not to Use

- When the test must validate a real provider integration end to end.
- When the login UI is the feature under test.
- When you are diagnosing a flaky test and should start with `playwright-debugging` instead.

## Network Interception

Use `page.route()` to replace external responses with deterministic data before the page makes the request.

```typescript
import { test, expect } from '@playwright/test';

test('shows premium dashboard when billing is active', async ({ page }) => {
  await page.route('**/api/v1/billing/status', async route => {
    await route.fulfill({
      status: 200,
      json: {
        subscription: 'active',
        plan: 'premium',
      },
    });
  });

  await page.goto('/dashboard');

  await expect(page.getByRole('heading', { name: 'Welcome to Premium' })).toBeVisible();
});
```

Intercept only the unstable boundary and leave the rest of the application real. If the code under test makes several external calls, mock the minimum necessary surface area.

Prefer `page.route()` when the response is part of the behavior under test and must be controlled from the browser context. If you need broader, suite-wide control, consider a fixture or a backend test double instead of scattering route handlers through individual tests.

## Verification

Verify the intercepted request produces the expected UI and that the real service is not required for the test to pass.

Typical checks:

```bash
npx playwright test tests/dashboard.spec.ts
```

Use trace viewer or UI mode to confirm the mocked response is the one the app consumed.