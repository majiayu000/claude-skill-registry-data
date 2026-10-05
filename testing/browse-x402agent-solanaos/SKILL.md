---
name: browse
description: "Playwright-powered browser automation and E2E testing for SolanaOS Hub. Covers test configuration, agent-driven test generation (planner/generator/healer), NanoHub route testing, Convex API validation, wallet flow testing, IPFS Hub verification, and CI/CD integration. Use when asked about E2E tests, browser automation, Playwright setup, NanoHub testing, visual regression, or Hub route verification."
version: 1.0.0
metadata: {"openclaw":{"emoji":"🎭","requires":{"bins":["node","npx","bun"]},"os":["darwin","linux","windows"]}}
---

# Browse — Playwright E2E Testing for SolanaOS Hub

Browser automation and end-to-end testing skill for the SolanaOS NanoHub, powered by Playwright.

## Quick Start

```bash
# Install Playwright browsers
npx playwright install chromium

# Run E2E tests
bun run test:e2e

# Run with UI mode
npx playwright test --ui

# Generate tests interactively
npx playwright codegen https://seeker.solanaos.net
```

## NanoHub Test Configuration

The NanoHub uses a dual config setup:

### Playwright Config (`playwright.config.ts`)

Browser-based E2E tests against the built frontend.

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  testMatch: /.*\.pw\.test\.ts/,
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4173',
    trace: 'retain-on-failure',
  },
  webServer: {
    command: 'bun run preview -- --host 127.0.0.1 --port 4173',
    url: 'http://127.0.0.1:4173',
    reuseExistingServer: !process.env.CI,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
})
```

### Vitest E2E Config (`vitest.e2e.config.ts`)

Node-based E2E tests for CLI and API validation (no browser needed).

```bash
bun vitest run -c vitest.e2e.config.ts
```

## NanoHub Routes to Test

| Route | Auth | What to verify |
|-------|------|----------------|
| `/` | No | Landing page renders, navigation works |
| `/launch` | No | Boot sequence animation, CTA links |
| `/mobile` | No | Seeker mobile walkthrough renders |
| `/skills` | No | Skill cards load from Convex |
| `/souls` | No | Soul cards load from Convex |
| `/ipfs` | No | IPFS Hub page renders, wallet input works |
| `/agents` | No | Agent directory loads public agents |
| `/dashboard` | Yes | Wallet connect, agent factory, pairing |
| `/upload` | Yes | Skill publish flow with file upload |
| `/settings` | Yes | User preferences, agent config |
| `/mining` | No | BitAxe fleet dashboard renders |
| `/strategy` | No | Strategy builder loads |
| `/create` | Yes | Skill creator wizard |
| `/auth/callback` | No | GitHub OAuth redirect handling |

## Writing Hub Tests

### Public Route Test

```typescript
import { test, expect } from '@playwright/test'

test('IPFS Hub page loads', async ({ page }) => {
  await page.goto('/ipfs')
  await expect(page.locator('h1')).toContainText('Private IPFS')
  await expect(page.locator('.gallery-stat-card')).toHaveCount(4)
})

test('agent directory shows cards', async ({ page }) => {
  await page.goto('/agents')
  await expect(page.locator('h1')).toContainText('Registered')
  // Wait for Convex query
  await page.waitForSelector('.agent-card', { timeout: 10_000 })
})

test('skill search works', async ({ page }) => {
  await page.goto('/skills')
  await page.locator('input[type="search"]').fill('solanaos')
  await page.waitForSelector('.skill-card')
  await expect(page.locator('.skill-card')).toHaveCount.greaterThan(0)
})
```

### Authenticated Route Test

```typescript
import { test, expect } from '@playwright/test'

// Use storage state from auth setup
test.use({ storageState: 'e2e/.auth/user.json' })

test('dashboard loads for authenticated user', async ({ page }) => {
  await page.goto('/dashboard')
  await expect(page.locator('.dashboard-section')).toBeVisible()
})
```

### Convex API Test (Vitest, no browser)

```typescript
import { describe, expect, it } from 'vitest'

const CONVEX_URL = process.env.CONVEX_URL || 'https://artful-frog-940.convex.cloud'

describe('Convex IPFS API', () => {
  it('GET /api/v1/ipfs/files returns array', async () => {
    const res = await fetch(
      `${CONVEX_URL}/api/v1/ipfs/files?wallet=test`,
      { headers: { Accept: 'application/json' } }
    )
    expect(res.ok).toBe(true)
    const data = await res.json()
    expect(data).toHaveProperty('files')
    expect(Array.isArray(data.files)).toBe(true)
  })

  it('GET /api/v1/ipfs/stats returns stats object', async () => {
    const res = await fetch(
      `${CONVEX_URL}/api/v1/ipfs/stats?wallet=test`,
      { headers: { Accept: 'application/json' } }
    )
    expect(res.ok).toBe(true)
    const data = await res.json()
    expect(data.stats).toHaveProperty('totalFiles')
  })
})
```

## Playwright Agents (AI-Driven Testing)

Playwright includes three built-in AI test agents.

### Setup

```bash
npx playwright init-agents --loop=vscode
```

### Planner

Explores the app and produces a Markdown test plan.

```
Input: "Generate a test plan for the IPFS Hub upload and recall flow"
Output: specs/ipfs-hub.md
```

The planner needs a **seed test** that sets up the environment:

```typescript
// tests/seed.spec.ts
import { test } from '@playwright/test'

test('seed', async ({ page }) => {
  await page.goto('/')
})
```

### Generator

Transforms Markdown plans into executable Playwright test files.

```
Input: specs/ipfs-hub.md
Output: tests/ipfs-hub/upload-file.spec.ts
```

### Healer

Automatically repairs failing tests by:
1. Replaying failing steps
2. Inspecting current UI for equivalent elements
3. Patching locators, waits, or data
4. Re-running until pass or skip

```
Input: "Heal tests/ipfs-hub/upload-file.spec.ts"
Output: Passing test (or skipped with reason)
```

## Configuration Reference

### Top-Level Options

| Option | Description |
|--------|-------------|
| `testDir` | Directory with test files |
| `testMatch` | Glob/regex for test file matching |
| `testIgnore` | Glob/regex for files to skip |
| `timeout` | Per-test timeout (default: 30s) |
| `retries` | Retry count for flaky tests |
| `workers` | Parallel worker count |
| `fullyParallel` | Run all tests in parallel |
| `forbidOnly` | Fail if `test.only` found (CI) |
| `reporter` | Output format: `list`, `html`, `json`, `dot` |
| `outputDir` | Artifacts directory (screenshots, videos, traces) |
| `globalSetup` | Path to setup script (runs before all tests) |
| `globalTeardown` | Path to teardown script (runs after all tests) |
| `webServer` | Auto-start dev server before tests |

### `use` Options

| Option | Description |
|--------|-------------|
| `baseURL` | Base URL for `page.goto('/')` |
| `storageState` | Pre-populated auth state |
| `trace` | Trace capture: `off`, `on`, `retain-on-failure`, `on-first-retry` |
| `screenshot` | Screenshot capture: `off`, `on`, `only-on-failure` |
| `video` | Video recording: `off`, `on`, `retain-on-failure` |
| `headless` | Run without browser UI (default: true) |
| `viewport` | Browser viewport size |
| `locale` | User locale emulation |
| `colorScheme` | `light` or `dark` mode |
| `geolocation` | GPS coordinate emulation |
| `permissions` | Browser permission grants |
| `offline` | Simulate offline mode |
| `proxy` | HTTP proxy settings |
| `extraHTTPHeaders` | Headers sent with every request |
| `actionTimeout` | Timeout per action (click, fill, etc.) |
| `testIdAttribute` | Custom test ID attribute |

### Annotations

```typescript
// Skip a test
test.skip('not ready', async ({ page }) => {})

// Mark as expected failure
test.fail('known bug', async ({ page }) => {})

// Mark as slow (3x timeout)
test.slow()

// Tag for filtering
test('login @smoke', async ({ page }) => {})
test('checkout', { tag: ['@e2e', '@slow'] }, async ({ page }) => {})

// Run tagged tests
// npx playwright test --grep @smoke
// npx playwright test --grep-invert @slow
```

## CLI Commands

```bash
# Run all tests
npx playwright test

# Run specific file
npx playwright test e2e/ipfs-hub.pw.test.ts

# Run by title match
npx playwright test -g "IPFS Hub"

# Run with browser visible
npx playwright test --headed

# Debug mode (inspector + slow)
npx playwright test --debug

# Interactive UI mode
npx playwright test --ui

# Generate test code interactively
npx playwright codegen https://seeker.solanaos.net

# View last test report
npx playwright show-report

# View trace file
npx playwright show-trace test-results/trace.zip

# Only re-run failures
npx playwright test --last-failed

# Shard across CI workers
npx playwright test --shard=1/3
```

## CI Integration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: npx playwright install --with-deps chromium
      - run: bun run build
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## NanoHub E2E Environment Variables

| Variable | Description |
|----------|-------------|
| `PLAYWRIGHT_BASE_URL` | Override base URL (skip local server) |
| `PLAYWRIGHT_PORT` | Override preview server port (default: 4173) |
| `CLAWHUB_E2E_TOKEN` | API token for authenticated CLI tests |
| `CLAWDHUB_E2E_TOKEN` | Alias for above |
| `CLAWHUB_REGISTRY` | Registry URL override |
| `CLAWHUB_SITE` | Site URL override |
| `CI` | Enables retries, single worker, forbidOnly |
