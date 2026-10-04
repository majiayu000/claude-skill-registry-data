---
name: playwright-auth-state
description: Playwright workflows for authenticated browser state reuse through storageState and setup projects.
---

# Playwright Auth State

## Overview

Use this skill when tests need to start in a known logged-in session or with a role-specific browser state instead of repeating the login UI in every spec. It keeps the browser state deterministic without making authentication the focus of the test.

Do not use this skill when the login form itself is the feature under test, or when the app is fully local and does not need shared browser state.

## When to Use

- When a test requires an already authenticated user.
- When a suite benefits from reusing browser state across many tests.
- When you need separate roles or permissions without redoing the UI login.

## When Not to Use

- When the login flow is the feature under test.
- When the app behavior is fully local and does not depend on stored session state.
- When you are diagnosing a flake that should be fixed first in `playwright-debugging`.

## Authenticated State

Create the authenticated state once in a setup project, then load it in the tests that need it.

```typescript
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: 'Sign in' }).click();

  await expect(page.getByRole('button', { name: 'Sign out' })).toBeVisible();
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});
```

Apply the saved state in configuration:

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'chromium',
      dependencies: ['setup'],
      use: {
        storageState: 'playwright/.auth/user.json',
      },
    },
  ],
});
```

If only some tests need the logged-in session, scope the state to a specific project rather than making it global. For multiple roles, keep one state file per role and give each project a clear name.

Treat the generated storage state as a build artifact, not source code. Keep it out of version control unless your project has a specific reason to commit it.

## Multiple Roles

When a suite needs more than one authenticated identity — an admin and a standard
user, for example — create one setup test and one storage state file per role, and
give each project a name that makes the role obvious at a glance.

```typescript
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('authenticate as admin', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('admin@example.com');
  await page.getByLabel('Password').fill('adminpass123');
  await page.getByRole('button', { name: 'Sign in' }).click();

  await expect(page.getByRole('heading', { name: 'Admin Dashboard' })).toBeVisible();
  await page.context().storageState({ path: 'playwright/.auth/admin.json' });
});

setup('authenticate as user', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: 'Sign in' }).click();

  await expect(page.getByRole('button', { name: 'Sign out' })).toBeVisible();
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});
```

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium-admin',
      dependencies: ['setup'],
      testMatch: /.*\.admin\.spec\.ts/,
      use: { storageState: 'playwright/.auth/admin.json' },
    },
    {
      name: 'chromium-user',
      dependencies: ['setup'],
      testMatch: /.*\.user\.spec\.ts/,
      use: { storageState: 'playwright/.auth/user.json' },
    },
  ],
});
```

Route each spec to the project whose role it needs through a file naming convention
such as `*.admin.spec.ts` and `*.user.spec.ts`. Keep the matchers explicit so a
project never becomes a catch-all for unrelated specs.

## Recommended Project Shape

Keep the setup file and the auth state file in a predictable location:

- `tests/auth.setup.ts`
- `playwright/.auth/user.json`
- `playwright.config.ts`

Keep the setup test focused on creating state, not on exercising the full product flow. The setup project should end as soon as the authenticated signal is visible and the storage state has been written.

## Verification

Verify the state file was created and loaded correctly.

Typical checks:

```bash
npx playwright test --project=setup
npx playwright test tests/dashboard.spec.ts
```

For debugging, use trace viewer or UI mode to confirm the login state is present in the resulting session.
