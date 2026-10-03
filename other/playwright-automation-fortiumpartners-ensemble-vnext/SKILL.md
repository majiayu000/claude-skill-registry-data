---
name: playwright-automation
description: Drive a browser with Playwright for RPA, web scraping, and workflow automation — resilient selectors, session persistence, retries.
when_to_use: Reach for this when the goal is to operate a real site to GET WORK DONE (scrape data, fill/submit forms, automate a flow), not to test your own app. For writing E2E *test suites* of your app use writing-playwright-tests; for visual/pixel comparison against Figma use figma-pixel-perfect. Browser-automation/RPA skill.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "playwright.config.*"
  - "scripts/**/*.{ts,js}"
  - "automation/**"
---

# Playwright Automation Skill

Production browser automation with Playwright for RPA, web scraping, and workflow automation. Covers resilient selectors, session persistence, retry/recovery patterns, and Playwright 1.56 agents.

---

## When to Use

This skill is auto-detected when the user mentions:
- "automation", "browser automation", "RPA"
- "scraping", "web scraping", "data extraction"
- "workflow automation", "form filling", "bot"
- Production Playwright usage outside of test suites

**For E2E testing, use the `writing-playwright-tests` skill instead.** That skill covers test assertions, test structure, CI test runners, and `@playwright/test` patterns. This skill covers long-running production automation, resilience, and recovery.

---

## Distinction from E2E Testing

| Concern | E2E Testing | Production Automation |
|---------|-------------|----------------------|
| **Goal** | Verify app correctness | Complete a real-world task |
| **On failure** | Test fails, report generated | Retry, recover, continue |
| **State** | Ephemeral, reset per test | Persistent sessions, cookies saved |
| **Error handling** | `expect()` assertions | Try/catch with fallback actions |
| **Lifecycle** | CI pipeline, minutes | Long-running, hours/days |
| **Data** | Fixtures, mocks | Live production data |
| **Selectors** | `data-testid` (you control source) | ARIA roles + fallback chains (third-party sites) |
| **Concurrency** | Parallel test workers | Worker pool with job queue |
| **Browser context** | Fresh per test | Reused with saved auth state |

---

## Resilient Selector Strategy

### Priority Order

ARIA role-based locators are the PRIMARY recommendation. They survive redesigns, class name changes, and DOM restructuring because they bind to semantic meaning.

```typescript
// BEST: Role-based locators (survive redesigns)
page.getByRole('button', { name: 'Submit Order' });
page.getByRole('navigation').getByRole('link', { name: 'Dashboard' });
page.getByRole('textbox', { name: /email/i });

// GOOD: Test IDs (when you control the source)
page.getByTestId('checkout-submit');

// ACCEPTABLE: CSS selectors (third-party sites you cannot modify)
page.locator('#login-button');
page.locator('[data-action="submit"]');

// LAST RESORT: Structural selectors (fragile, document why)
page.locator('form.checkout >> button:last-child');
```

### Chaining and Filtering

```typescript
// Filter within a container to avoid ambiguity
const row = page.getByRole('row').filter({ hasText: 'Widget Pro' });
await row.getByRole('button', { name: 'Add to Cart' }).click();

// Chain locators for specificity
await page.getByRole('complementary').getByRole('link', { name: 'Settings' }).click();
```

### Fallback Selector Chains

On third-party sites, selectors break without warning. Use a fallback chain that tries multiple strategies in order.

```typescript
import { Page, Locator } from 'playwright';

async function resilientLocator(
  page: Page,
  strategies: Array<() => Locator>,
  timeout = 5000
): Promise<Locator> {
  for (const strategy of strategies) {
    const locator = strategy();
    try {
      await locator.waitFor({ state: 'visible', timeout });
      return locator;
    } catch {
      // Strategy did not match; try next
    }
  }
  throw new Error(`No strategy matched a visible element`);
}

// Usage: third-party login page
const submitBtn = await resilientLocator(page, [
  () => page.getByRole('button', { name: /sign in/i }),
  () => page.getByTestId('login-submit'),
  () => page.locator('button[type="submit"]'),
]);
await submitBtn.click();
```

---

## Session Persistence

### storageState for Cookies and localStorage

```typescript
const AUTH_STATE_PATH = './auth-state.json';

// Save after login
await page.context().storageState({ path: AUTH_STATE_PATH });

// Restore on next run
const context = await browser.newContext({ storageState: AUTH_STATE_PATH });
```

### CRITICAL: storageState Does NOT Persist sessionStorage

`storageState` only captures cookies and `localStorage`. If the target app stores auth tokens in `sessionStorage`, those values are silently lost between runs. This is a common source of "works once, fails on resume" bugs.

**Workaround: Manual sessionStorage Save and Restore**

```typescript
import * as fs from 'fs';

const SESSION_STORAGE_PATH = './session-storage.json';

async function saveSessionStorage(page): Promise<void> {
  const data = await page.evaluate(() => {
    const entries: Record<string, string> = {};
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i)!;
      entries[key] = sessionStorage.getItem(key)!;
    }
    return entries;
  });
  fs.writeFileSync(SESSION_STORAGE_PATH, JSON.stringify(data, null, 2));
}

async function restoreSessionStorage(context): Promise<void> {
  if (!fs.existsSync(SESSION_STORAGE_PATH)) return;
  const data = JSON.parse(fs.readFileSync(SESSION_STORAGE_PATH, 'utf-8'));
  // addInitScript runs before any page script on every new page
  await context.addInitScript((entries) => {
    for (const [key, value] of Object.entries(entries)) {
      sessionStorage.setItem(key, value as string);
    }
  }, data);
}
```

### Persistent Browser Contexts

For long-running automation (monitoring, periodic scraping), use a persistent context that writes all browser state to disk.

```typescript
// Preserves cookies, localStorage, IndexedDB, service workers, cache
const context = await chromium.launchPersistentContext(
  './browser-data/profile-1',
  { headless: true, viewport: { width: 1280, height: 720 } }
);
```

---

## Retry and Recovery Patterns

### withRetry Wrapper with Exponential Backoff

```typescript
interface RetryOptions {
  maxRetries?: number;
  baseDelayMs?: number;
  maxDelayMs?: number;
  onRetry?: (error: Error, attempt: number) => void;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const { maxRetries = 3, baseDelayMs = 1000, maxDelayMs = 30000, onRetry } = options;
  let lastError: Error;

  for (let attempt = 1; attempt <= maxRetries + 1; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
      if (attempt > maxRetries) break;
      const delay = Math.min(baseDelayMs * 2 ** (attempt - 1), maxDelayMs);
      onRetry?.(lastError, attempt);
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw lastError!;
}
```

### Page Crash Recovery

```typescript
async function withCrashRecovery(context, task: (page) => Promise<void>) {
  let page = await context.newPage();
  page.on('crash', async () => {
    console.error('Page crashed. Creating new page.');
    page = await context.newPage();
  });
  await withRetry(() => task(page), { maxRetries: 2 });
}
```

### Navigation Timeout and Stale Element Recovery

```typescript
// Safe navigation: accept partial load if URL is correct
async function safeGoto(page, url: string, timeout = 30000) {
  await withRetry(async () => {
    try { await page.goto(url, { timeout, waitUntil: 'domcontentloaded' }); }
    catch (e) {
      if (e.message?.includes('Timeout') && page.url().startsWith(url.split('?')[0])) return;
      throw e;
    }
  }, { maxRetries: 2, baseDelayMs: 3000 });
}

// Stale element: re-query the locator on each retry attempt
await withRetry(async () => {
  await page.getByRole('button', { name: 'Next Page' }).click();
}, { maxRetries: 3, baseDelayMs: 500 });
```

---

## Anti-Flake Techniques

### CRITICAL: Never Use waitForTimeout() in Production

`page.waitForTimeout()` is a hard sleep. It wastes time when the page is ready early and fails when the page is slow. Always wait for a concrete signal.

```typescript
// BAD: Hard sleep
await page.waitForTimeout(3000);

// GOOD: Wait for a specific network response
await page.waitForResponse(
  (resp) => resp.url().includes('/api/products') && resp.status() === 200
);

// GOOD: Wait for an element (web-first assertion)
await expect(page.getByRole('table')).toBeVisible();

// GOOD: Wait for network idle
await page.waitForLoadState('networkidle');
```

### Wait for API Response + Navigation

```typescript
async function navigateAndWaitForData(page, url: string, apiPattern: string) {
  const [response] = await Promise.all([
    page.waitForResponse((resp) => resp.url().includes(apiPattern) && resp.ok()),
    page.goto(url),
  ]);
  return response.json();
}
```

### Polling with expect().toPass()

For conditions that require repeated checks, `expect().toPass()` retries until success or timeout.

```typescript
await expect(async () => {
  const rowCount = await page.getByRole('row').count();
  expect(rowCount).toBeGreaterThanOrEqual(10);
}).toPass({ timeout: 15000, intervals: [500, 1000, 2000] });
```

---

## Error Capture

### On-Failure Diagnostic Bundle

On failure, capture a screenshot, DOM snapshot, and recent network activity for debugging.

```typescript
function createDiagnosticCollector(page) {
  const networkLog: Array<{ url: string; status: number; method: string }> = [];
  const consoleMessages: string[] = [];

  page.on('response', (resp) => {
    networkLog.push({ url: resp.url(), status: resp.status(), method: resp.request().method() });
    if (networkLog.length > 50) networkLog.shift();
  });
  page.on('console', (msg) => {
    consoleMessages.push(`[${msg.type()}] ${msg.text()}`);
    if (consoleMessages.length > 100) consoleMessages.shift();
  });
  page.on('pageerror', (error) => {
    consoleMessages.push(`[PAGE_ERROR] ${error.message}`);
  });

  return async () => ({
    screenshot: await page.screenshot({ fullPage: true }),
    html: await page.content(),
    url: page.url(),
    networkLog: [...networkLog],
    consoleMessages: [...consoleMessages],
    timestamp: new Date().toISOString(),
  });
}

// Usage
const capture = createDiagnosticCollector(page);
try {
  await automateCheckout(page);
} catch (error) {
  const diag = await capture();
  fs.writeFileSync(`./errors/${diag.timestamp}-screenshot.png`, diag.screenshot);
  fs.writeFileSync(`./errors/${diag.timestamp}-context.json`, JSON.stringify({
    error: error.message, url: diag.url, networkLog: diag.networkLog,
    consoleMessages: diag.consoleMessages,
  }, null, 2));
  throw error;
}
```

---

## Parallel Execution

### Worker Isolation

Each worker gets its own browser instance. Never share a `BrowserContext` across workers.

```typescript
async function createWorker(workerId: string) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  return {
    browser, context,
    cleanup: async () => { await context.close(); await browser.close(); },
  };
}
```

### Queue-Driven Pattern

```typescript
import PQueue from 'p-queue';

const queue = new PQueue({ concurrency: 4 });

async function processJobs(browser, jobs: Array<{ url: string; action: (page) => Promise<unknown> }>) {
  const results = await Promise.allSettled(
    jobs.map((job) => queue.add(async () => {
      const context = await browser.newContext();
      const page = await context.newPage();
      try {
        await page.goto(job.url);
        return await job.action(page);
      } finally {
        await context.close();
      }
    }))
  );
  return results;
}
```

### Resource Cleanup on Worker Exit

Always register cleanup handlers to prevent orphaned browser processes.

```typescript
let activeBrowsers: Browser[] = [];

async function cleanupAll() {
  await Promise.allSettled(activeBrowsers.map((b) => b.close()));
  activeBrowsers = [];
}

process.on('SIGINT', async () => { await cleanupAll(); process.exit(0); });
process.on('SIGTERM', async () => { await cleanupAll(); process.exit(0); });
```

> **See [REFERENCE.md](./REFERENCE.md)** for BullMQ integration, in-memory queue runner, and container-based scaling.

---

## Playwright Agents (v1.56)

Playwright 1.56 introduced Agents: AI-driven components that plan, generate, and heal automation flows. The Healer agent is directly useful in production automation for self-healing selectors.

### Agent Overview

| Agent | Purpose | Automation Use Case |
|-------|---------|---------------------|
| **Planner** | Explores app, produces structured test plans | Generating initial automation specs from a live site |
| **Generator** | Converts plans into executable code | Scaffolding automation scripts from descriptions |
| **Healer** | Detects and repairs broken selectors | Self-healing bots when target sites change markup |

### Initializing Agents

```bash
npx playwright init-agents --loop=claude
npx playwright init-agents --loop=vscode
```

Regenerate definitions after Playwright version upgrades to access new tools and instructions.

### Healer Agent for Production Automation

When a selector breaks because the target site redesigned, the Healer:

1. Replays the failing step
2. Inspects the current UI state
3. Proposes updated selectors
4. Re-runs the step to verify the fix

```bash
npx playwright test --heal my-automation.spec.ts
```

### Integrating Agents into Pipelines

Combine the Healer with your retry logic: on selector failure, invoke the Healer before retrying.

**Important limitations:**
- Agents require an LLM backend (Claude, VS Code Copilot, or OpenCode)
- Agent definitions must be regenerated on Playwright version upgrades
- The Healer works on `@playwright/test` spec files; for raw `playwright` scripts, wrap automation steps in spec format

---

## Quick Reference Card

```
SELECTORS (priority order):
  page.getByRole('button', { name: 'Submit' })     # BEST: ARIA role
  page.getByTestId('checkout-btn')                  # GOOD: test ID
  page.locator('#login-btn')                        # OK: CSS (third-party)
  page.locator('form >> button:last-child')         # LAST RESORT

SESSION PERSISTENCE:
  context.storageState({ path })                    # Save cookies + localStorage
  browser.newContext({ storageState: path })         # Restore
  page.evaluate(() => sessionStorage...)             # Manual (NOT auto-saved)
  chromium.launchPersistentContext(dir)              # Full profile on disk

WAITS (never use waitForTimeout in production):
  page.waitForResponse(resp => ...)                 # API response
  page.waitForLoadState('networkidle')              # Network idle
  page.waitForURL(pattern)                          # Navigation
  expect(locator).toBeVisible()                     # Element visible
  expect(async () => ...).toPass({ timeout })       # Polling

RETRY:
  withRetry(fn, { maxRetries: 3 })                  # Exponential backoff
  page.on('crash', handler)                         # Crash recovery
  resilientLocator(page, [s1, s2, s3])              # Fallback chain

DIAGNOSTICS:
  page.screenshot({ fullPage: true })               # Screenshot
  page.content()                                    # DOM snapshot
  page.on('console', handler)                       # Console capture
  page.on('pageerror', handler)                     # Error capture

PARALLEL:
  PQueue({ concurrency: N })                        # Job queue
  browser.newContext()                               # Isolated context
  process.on('SIGTERM', cleanupAll)                 # Graceful shutdown

AGENTS (v1.56):
  npx playwright init-agents --loop=claude          # Initialize
  npx playwright test --heal script.spec.ts         # Heal selectors
```

---

**See [REFERENCE.md](./REFERENCE.md) for**: Page Object Model for production automation, queue-driven execution architecture, browser profile management, network interception for stability, monitoring and alerting, and scaling with container-based workers.
