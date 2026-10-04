---
name: e2e-playwright
description: End-to-end testing with Playwright in Next.js applications — user flow coverage, component testing, and CI integration. Use when writing E2E tests, debugging flaky tests, or setting up test infrastructure.
trigger: 需要编写端到端测试
input: 测试需求
output: E2E 测试代码
next: 无
dependencies: 无
---

# E2E Testing with Playwright

End-to-end testing strategy for Next.js applications using Playwright.

## Setup

```bash
npm init playwright@latest
# Choose: TypeScript, tests/e2e/, add GitHub Actions
```

Recommended config (`playwright.config.ts`):

```ts
import { defineConfig } from '@playwright/test'
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
})
```

## What to Test

### Critical User Journeys

Test the paths users actually take, not every component:

```
✓ User can sign up → verify email → login → see dashboard
✓ User can create/edit/delete content
✓ User can complete checkout flow
✓ Error states: 404, 500, network failure
✓ Responsive breakpoints (mobile, tablet, desktop)
```

### What NOT to Test with E2E

- Unit-verifiable logic (test in Vitest/Jest)
- Individual component states (test in Storybook/Component tests)
- Visual snapshots of static content

## Patterns

### Page Object Pattern

```ts
// tests/e2e/pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() { await this.page.goto('/login') }
  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email)
    await this.page.fill('[name="password"]', password)
    await this.page.click('button[type="submit"]')
  }
  async waitForDashboard() {
    await expect(this.page).toHaveURL(/\/dashboard/)
  }
}
```

### Data Seeding

```ts
// tests/e2e/global-setup.ts — seed DB before test run
import { seedTestData } from './helpers/seed'

export default async () => {
  await seedTestData({
    user: { email: 'test@example.com' },
    posts: 3,
  })
}
```

### Mocking API/Network

```ts
// Block external requests, mock specific responses
await page.route('**/api/analytics', route => route.abort())
await page.route('**/api/posts/**', async route => {
  await route.fulfill({ json: { title: 'Mock post' } })
})
```

## CI Integration

```yaml
# .github/workflows/e2e.yml
name: E2E
on: [deployment_status]
jobs:
  test:
    if: github.event_name == 'deployment_status' && github.event.state == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install
      - run: npx playwright test
```

## Debugging Flaky Tests

1. **Check trace** (`trace: 'on-first-retry'`) — Playwright captures full DOM + network + console
2. **Add `await page.waitForLoadState('networkidle')`** after navigation
3. **Use `toHaveURL` / `toHaveText`** instead of arbitrary timeouts
4. **Isolate tests** — each test should be self-contained, no shared state

## Checklist

- [ ] Can every critical user journey be tested end-to-end?
- [ ] Are Page Objects used for reusable page interactions?
- [ ] Is test data seeded before the run and cleaned up after?
- [ ] Is CI configured (Vercel deployment status trigger)?
- [ ] Are traces/screenshots captured on failure?
- [ ] No `await page.waitForTimeout(N)` — always wait for actual conditions
- [ ] Responsive testing at mobile (375px) and desktop (1280px+) breakpoints