---
name: vibe-e2e
description: >
  Generates and runs full end-to-end UI tests using Playwright against a live
  URL. Auto-installs Playwright and Chromium if not present — isolated in e2e/
  folder, never pollutes app dependencies. Reads SPEC.md and FEATURES.md to
  automatically generate test flows covering every critical user journey.
  Runs tests with video recording on failure and HTML report. Two-device flows
  (poster + joiner, sender + receiver) use parallel browser contexts. OAuth
  flows are skipped with clear warnings. Generates a cleanup script that
  deletes all test data after the suite runs. e2e: regenerate rewrites all
  tests from current SPEC.md. Triggers: "e2e: https://url" to run against
  a live URL, "e2e: regenerate" to rewrite tests from spec.
---

# Vibe E2E Skill

Generates Playwright E2E tests from your SPEC.md and FEATURES.md.
Runs them against a live URL. Records video on failure.
Cleans up test data after every run.

---

## Triggers

| Trigger | What it does |
|---|---|
| `e2e: https://url` | Generate tests (if none exist) + run against URL |
| `e2e: run https://url` | Run existing tests against URL without regenerating |
| `e2e: regenerate` | Rewrite all test files from current SPEC.md + FEATURES.md |
| `e2e: cleanup https://url` | Run cleanup script only — delete test data |

---

## Step 0 — Install Playwright if missing

Before anything else, check if Playwright is available and install if not.
Install into an isolated `e2e/` folder — never touch the app's `package.json`.

```bash
# Check if e2e folder exists with Playwright already installed
ls e2e/node_modules/@playwright/test 2>/dev/null && echo "INSTALLED" || echo "NOT_INSTALLED"
```

**If not installed:**

```bash
# Create e2e folder if it doesn't exist
mkdir -p e2e

# Detect project package manager
ls yarn.lock 2>/dev/null && echo "yarn" || ls pnpm-lock.yaml 2>/dev/null && echo "pnpm" || echo "npm"

# Install Playwright into e2e/ only
cd e2e

# If npm:
npm init -y
npm install -D @playwright/test

# If yarn:
yarn init -y
yarn add -D @playwright/test

# If pnpm:
pnpm init
pnpm add -D @playwright/test

# Install Chromium browser only (sufficient for QA, smallest download)
npx playwright install chromium --with-deps
```

**If project is Python-only (no package.json anywhere):**

```bash
pip install playwright
playwright install chromium
```

Tell the user: "Installing Playwright into e2e/ — this takes ~30 seconds for the first install."

---

## Step 1 — Read project context

```bash
cat vibe/SPEC.md 2>/dev/null
cat vibe/FEATURES.md 2>/dev/null || cat FEATURES.md 2>/dev/null
cat vibe/ARCHITECTURE.md 2>/dev/null
cat BRIEF.md 2>/dev/null
```

**Extract from these files:**
- Every user-facing feature
- Acceptance criteria (from SPEC.md) — these become assertions
- Auth method — email/password, OAuth providers, phone OTP
- Multi-user flows — any flow requiring two users simultaneously
- Admin-gated features
- Time-sensitive behaviour (e.g. "ride appears within 10 seconds")
- API endpoints used by the frontend (for cleanup script)

---

## Step 2 — Generate flow list

Before writing any test code, show the user the flows Claude has identified.
Group by domain. Number sequentially.
Flag multi-device flows and OAuth flows explicitly.

```
Flows detected from SPEC.md + FEATURES.md:

  AUTH
  01 · Register → complete profile → land on home          [single device]
  02 · Login with email and password                        [single device]
  03 · Login with Google OAuth                              [⚠️ SKIP — OAuth]
  04 · Login with Apple OAuth                               [⚠️ SKIP — OAuth]
  05 · Forgot password flow                                 [single device]

  CORE
  06 · Post a ride → appears in discover feed within 10s    [single device]
  07 · Discover → filter by vibe tag → request to join      [single device]
  08 · Poster approves join → joiner sees approval          [TWO DEVICES]
  09 · Approved joiner opens group chat → messages appear   [TWO DEVICES]

  TRIBE
  10 · Send tribe invite → other user accepts               [TWO DEVICES]
  11 · Direct message between tribe members                 [TWO DEVICES]

  ROUTES
  12 · Browse routes → filter → tap route → Plan a Ride    [single device]
  13 · Submit a route → appears in feed                     [single device]

  ADMIN
  14 · Admin: paste URL → Gemini extracts → publish route   [single device]

  PROFILE
  15 · Edit profile → change vibe tags → verify saved       [single device]
  16 · Post-ride rating → poster profile shows rating       [TWO DEVICES]

  ──────────────────────────────────────────────
  Total: 16 flows · 4 skipped (OAuth) · 6 two-device · 6 single-device

Generating Playwright tests for 12 active flows...
```

Wait briefly (2-3 seconds) then proceed with generation — no need for user confirmation unless the flow list looks wrong.

---

## Step 3 — Generate file structure

```
e2e/
├── package.json
├── playwright.config.ts
├── tests/
│   ├── 01-auth.spec.ts
│   ├── 02-core-flow.spec.ts
│   ├── 03-tribe.spec.ts
│   ├── 04-routes.spec.ts
│   ├── 05-admin.spec.ts
│   ├── 06-profile.spec.ts
│   └── helpers/
│       ├── auth.ts          ← login/register helpers
│       ├── fixtures.ts      ← test data with timestamps
│       ├── selectors.ts     ← centralised UI selectors
│       └── cleanup.ts       ← delete all test data via API
├── cleanup.ts               ← standalone cleanup script
├── .gitignore
└── test-results/            ← generated on run, gitignored
```

---

## Step 4 — Generate each file

### `e2e/package.json`
```json
{
  "name": "[project]-e2e",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "test": "playwright test",
    "test:headed": "playwright test --headed",
    "report": "playwright show-report e2e/report",
    "cleanup": "npx ts-node cleanup.ts"
  },
  "devDependencies": {
    "@playwright/test": "^1.44.0",
    "ts-node": "^10.9.2",
    "typescript": "^5.4.0"
  }
}
```

### `e2e/playwright.config.ts`
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  timeout: 45000,
  expect: { timeout: 10000 },
  retries: process.env.CI ? 2 : 1,
  workers: process.env.CI ? 1 : 2,
  fullyParallel: false,

  use: {
    baseURL: process.env.BASE_URL,
    headless: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
    actionTimeout: 15000,
    navigationTimeout: 30000,
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],

  reporter: [
    ['list'],
    ['html', { outputFolder: 'report', open: 'never' }],
    ['json', { outputFile: 'report/results.json' }],
  ],

  outputDir: 'test-results',
})
```

### `e2e/tests/helpers/fixtures.ts`
Generate timestamps so every test run creates unique data and never conflicts:
```typescript
const RUN_ID = Date.now()

export const USER_A = {
  email: `qa-a-${RUN_ID}@e2e-test.invalid`,
  password: 'E2eTest123!',
  name: `QA Rider A ${RUN_ID}`,
  bike: 'Royal Enfield Classic 350',
  city: 'Pune',
}

export const USER_B = {
  email: `qa-b-${RUN_ID}@e2e-test.invalid`,
  password: 'E2eTest123!',
  name: `QA Rider B ${RUN_ID}`,
  bike: 'KTM Duke 390',
  city: 'Pune',
}

export const TEST_RIDE = {
  destination: `E2E Test Ride ${RUN_ID}`,
  date: (() => {
    const d = new Date()
    d.setDate(d.getDate() + 1)
    return d.toISOString().split('T')[0]
  })(),
  maxRiders: 3,
}

export const TEST_ROUTE = {
  name: `E2E Test Route ${RUN_ID}`,
  distance: '45km',
  duration: '2h',
  startLocation: 'Pune',
}

// Track created entity IDs for cleanup
export const CREATED: {
  userIds: string[]
  rideIds: string[]
  routeIds: string[]
} = {
  userIds: [],
  rideIds: [],
  routeIds: [],
}
```

### `e2e/tests/helpers/auth.ts`
```typescript
import { Page } from '@playwright/test'
import { USER_A, USER_B, CREATED } from './fixtures'

export async function register(page: Page, user = USER_A) {
  await page.goto('/register')

  // Step 1 — email + password
  await page.getByLabel(/email/i).fill(user.email)
  await page.getByLabel(/password/i).first().fill(user.password)
  await page.getByRole('button', { name: /continue|next|sign up/i }).click()

  // Step 2 — profile setup (adjust selectors to match actual UI)
  await page.getByLabel(/display name|name/i).fill(user.name)

  // Bike field
  const bikeField = page.getByLabel(/bike/i)
  if (await bikeField.isVisible()) await bikeField.fill(user.bike)

  // City field
  const cityField = page.getByLabel(/city/i)
  if (await cityField.isVisible()) await cityField.fill(user.city)

  await page.getByRole('button', { name: /create|finish|done/i }).click()
  await page.waitForURL(/discover|home|dashboard/, { timeout: 15000 })

  // Extract and store user ID for cleanup
  const cookies = await page.context().cookies()
  const token = cookies.find(c => c.name === 'auth-token' || c.name === 'token')
  if (token) {
    // Decode JWT to get user ID (base64 middle segment)
    try {
      const payload = JSON.parse(atob(token.value.split('.')[1]))
      if (payload.sub || payload.user_id || payload.id) {
        CREATED.userIds.push(payload.sub || payload.user_id || payload.id)
      }
    } catch {}
  }
}

export async function login(page: Page, user = USER_A) {
  await page.goto('/login')
  await page.getByLabel(/email/i).fill(user.email)
  await page.getByLabel(/password/i).fill(user.password)
  await page.getByRole('button', { name: /log in|sign in|continue/i }).click()
  await page.waitForURL(/discover|home|dashboard/, { timeout: 15000 })
}

export async function registerAndLogin(page: Page, user = USER_A) {
  await register(page, user)
}
```

### `e2e/tests/helpers/cleanup.ts`
```typescript
import { APIRequestContext } from '@playwright/test'
import { CREATED } from './fixtures'

export async function cleanupTestData(request: APIRequestContext, baseURL: string, adminToken?: string) {
  const headers = adminToken
    ? { Authorization: `Bearer ${adminToken}` }
    : {}

  console.log(`\nCleaning up test data...`)

  // Delete test rides
  for (const rideId of CREATED.rideIds) {
    try {
      await request.delete(`${baseURL}/api/rides/${rideId}`, { headers })
      console.log(`  ✓ Deleted ride ${rideId}`)
    } catch (e) {
      console.log(`  ⚠ Could not delete ride ${rideId}: ${e}`)
    }
  }

  // Delete test routes
  for (const routeId of CREATED.routeIds) {
    try {
      await request.delete(`${baseURL}/api/routes/${routeId}`, { headers })
      console.log(`  ✓ Deleted route ${routeId}`)
    } catch (e) {
      console.log(`  ⚠ Could not delete route ${routeId}: ${e}`)
    }
  }

  // Delete test users (last — after rides/routes are gone)
  for (const userId of CREATED.userIds) {
    try {
      await request.delete(`${baseURL}/api/users/${userId}`, { headers })
      console.log(`  ✓ Deleted user ${userId}`)
    } catch (e) {
      console.log(`  ⚠ Could not delete user ${userId}: ${e}`)
    }
  }

  console.log(`Cleanup complete.\n`)
}
```

### `e2e/cleanup.ts` (standalone script)
```typescript
import { chromium } from '@playwright/test'
import { CREATED } from './tests/helpers/fixtures'
import { cleanupTestData } from './tests/helpers/cleanup'

const BASE_URL = process.env.BASE_URL
if (!BASE_URL) {
  console.error('ERROR: BASE_URL environment variable required')
  console.error('Usage: BASE_URL=https://your-app.railway.app npm run cleanup')
  process.exit(1)
}

;(async () => {
  const browser = await chromium.launch()
  const context = await browser.newContext()
  const request = context.request

  await cleanupTestData(request, BASE_URL)
  await browser.close()
})()
```

### Test specs — one per domain

Generate each spec fully from the actual flow list detected in Step 2.
Every assertion comes directly from acceptance criteria in SPEC.md.

**Pattern for single-device tests:**

```typescript
// 01-auth.spec.ts
import { test, expect, request } from '@playwright/test'
import { register, login } from './helpers/auth'
import { USER_A, USER_B } from './fixtures'
import { cleanupTestData } from './helpers/cleanup'

const BASE_URL = process.env.BASE_URL!

test.afterAll(async () => {
  const ctx = await request.newContext()
  await cleanupTestData(ctx, BASE_URL)
})

test.describe('Authentication', () => {

  test('01 · register → complete profile → land on discover', async ({ page }) => {
    await register(page, USER_A)
    await expect(page).toHaveURL(/discover/)
    await expect(page.getByText(/upcoming rides|discover/i)).toBeVisible()
  })

  test('02 · login with email and password', async ({ page }) => {
    // Register first if not done
    await register(page, USER_B)
    await page.goto('/logout')
    await login(page, USER_B)
    await expect(page).toHaveURL(/discover/)
  })

  // OAuth tests — skipped with explanation
  test.skip('03 · login with Google OAuth — skipped: requires real OAuth credentials', async ({ page }) => {
    // To enable: set E2E_GOOGLE_EMAIL and E2E_GOOGLE_PASSWORD env vars
    // and implement OAuth flow using those credentials
  })

  test.skip('04 · login with Apple OAuth — skipped: requires real Apple credentials', async ({ page }) => {
    // Apple OAuth cannot be automated without a real Apple Developer account
    // Test manually: Sign in with Apple button → Apple ID login → redirects to app
  })

})
```

**Pattern for two-device flows (parallel browser contexts):**

```typescript
// 02-core-flow.spec.ts — excerpt showing two-device pattern
test('08 · poster approves join → joiner sees approval notification', async ({ browser }) => {
  // Create two independent browser contexts — simulates two real devices
  const posterCtx  = await browser.newContext()
  const joinerCtx  = await browser.newContext()
  const posterPage = await posterCtx.newPage()
  const joinerPage = await joinerCtx.newPage()

  try {
    // Register both users
    await register(posterPage, USER_A)
    await register(joinerPage, USER_B)

    // USER_A posts a ride
    await posterPage.goto('/post-ride')
    await posterPage.getByLabel(/destination/i).fill(TEST_RIDE.destination)
    // ... fill other fields
    await posterPage.getByRole('button', { name: /post|create/i }).click()
    await expect(posterPage.getByText(TEST_RIDE.destination)).toBeVisible()

    // USER_B discovers the ride and requests to join
    await joinerPage.goto('/discover')
    await joinerPage.getByText(TEST_RIDE.destination).click()
    await joinerPage.getByRole('button', { name: /request to join/i }).click()
    await expect(joinerPage.getByText(/request sent|pending/i)).toBeVisible()

    // USER_A approves the join request
    await posterPage.goto('/my-rides')
    await posterPage.getByText(/pending request|join request/i).first().click()
    await posterPage.getByRole('button', { name: /approve|accept/i }).click()

    // USER_B should see approval
    await joinerPage.reload()
    await expect(joinerPage.getByText(/approved|open chat/i)).toBeVisible({ timeout: 15000 })

  } finally {
    await posterCtx.close()
    await joinerCtx.close()
  }
})
```

**Pattern for time-sensitive assertions (from SPEC acceptance criteria):**

```typescript
test('06 · post a ride → appears in discover feed within 10 seconds', async ({ page }) => {
  await login(page, USER_A)

  await page.goto('/post-ride')
  await page.getByLabel(/destination/i).fill(TEST_RIDE.destination)
  await page.getByLabel(/date/i).fill(TEST_RIDE.date)
  await page.getByRole('button', { name: /post|create/i }).click()

  // SPEC says: ride appears within 10 seconds
  await page.goto('/discover')
  await expect(
    page.getByText(TEST_RIDE.destination)
  ).toBeVisible({ timeout: 10000 })  // exact timeout from acceptance criteria
})
```

### `e2e/.gitignore`
```
node_modules/
test-results/
report/
*.webm
*.zip
playwright-report/
```

---

## Step 5 — Run the suite

```bash
cd e2e && BASE_URL=[url] npx playwright test --project=chromium 2>&1
```

Stream output to terminal in real time as tests run.
After run completes, automatically run cleanup:

```bash
cd e2e && BASE_URL=[url] npx ts-node cleanup.ts
```

**A passing assertion is not a clean run — observe the page, don't just probe it.**
A flow can satisfy every locator while the console throws and the screen renders
half-broken. Verification means *observing* what the software actually does, so each
spec must also watch the things a green checkmark hides:

- **Fail the flow on uncaught page errors / console errors.** Attach a listener in
  the shared fixture and assert it stayed empty for the flow:
  ```ts
  const errors: string[] = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  // …run the flow…
  expect(errors, `console/page errors during flow:\n${errors.join('\n')}`).toEqual([]);
  ```
  A red console during a "passing" flow is a real defect — surface it, don't ignore it.
- **Capture a screenshot at each flow's key state** as evidence (Playwright already
  keeps video + trace on failure; add `await page.screenshot(...)` at the asserted
  moment so the report shows what actually rendered, not just that a selector matched).
- **A blank or error screen is a failure even when no assertion tripped** — if the
  main content region is empty where content was expected, fail with that as the symptom.

---

## Step 6 — Report results

Present a clean summary after every run:

```
E2E REPORT — [Project Name]
URL: [url]
Run: [timestamp]
──────────────────────────────────────────────
01 auth    · Register → profile → discover      ✅  4.2s
02 auth    · Login email/password               ✅  1.8s
03 auth    · Google OAuth                       ⚠️   SKIPPED
04 auth    · Apple OAuth                        ⚠️   SKIPPED
05 core    · Post ride → discover in 10s        ✅  7.1s
06 core    · Discover → filter → join request   ✅  5.4s
07 core    · Approve join → notification        ❌  FAILED  8.2s
08 core    · Group chat send/receive            ⏭   SKIPPED (depends on 07)
09 tribe   · Send invite → accept               ✅  6.8s
10 tribe   · Direct message                     ✅  9.3s
11 routes  · Browse → filter → plan ride        ✅  3.9s
12 routes  · Submit route → appears in feed     ✅  4.1s
13 admin   · URL → Gemini → publish             ✅  11.2s
14 profile · Edit profile → verify saved        ✅  2.3s
──────────────────────────────────────────────
12 passed · 1 failed · 2 skipped (OAuth) · 1 skipped (dependency)

FAILURES
  07 · core · Approve join → joiner notification
       Step: joiner reloads page → expected "approved" text
       Got:  "pending" still showing
       Likely cause: real-time update not propagating — WebSocket or polling issue
       Video:  e2e/test-results/07-core-approve/video.webm
       Trace:  e2e/test-results/07-core-approve/trace.zip
       Open trace: npx playwright show-trace e2e/test-results/07-core-approve/trace.zip

OAUTH WARNINGS (manual testing required)
  03 · Google OAuth — test manually: tap "Sign in with Google" → complete flow → verify redirect
  04 · Apple OAuth  — test manually: tap "Sign in with Apple" → complete flow → verify redirect

CLEANUP
  ✓ Deleted 2 test rides
  ✓ Deleted 2 test users
  Cleanup complete.

VERDICT: ❌ 1 failure — fix before deploy
HTML report: e2e/report/index.html
```

---

## Step 7 — `e2e: regenerate`

Rewrites all spec files from current SPEC.md + FEATURES.md.
Preserves `helpers/` (auth, fixtures, cleanup, selectors) — only rewrites spec files.

Show new flow list first:
```
Regenerating from SPEC.md + FEATURES.md...

New flows detected (current SPEC):
  [updated flow list]

Changes from previous run:
  + Flow 17 added: Weather badge on discover
  ~ Flow 06 updated: ride now appears in 5s (was 10s per updated SPEC)
  - Flow 14 removed: Admin scraper UI (moved to separate admin suite)

Rewriting spec files... (helpers preserved)
✅ 6 spec files rewritten
```

---

## Step 8 — Update vibe docs

After a successful run, log to TASKS.md:

```
✅ E2E suite passed — [date]
   URL: [url]
   Flows: [N] passed · [N] failed · [N] skipped
   Report: e2e/report/index.html
```

If failures:
```
⚠️  E2E suite — [N] failures — [date]
   URL: [url]
   Failed: [flow names]
   Videos: e2e/test-results/
```

---

## Absolute rules

**OAuth flows are always skipped — never attempt to automate them.**
Google and Apple OAuth involve third-party login screens that actively
block automation. Mark them as `test.skip()` with a manual testing note.
Never try to interact with Google or Apple login screens.

**Test data uses `.invalid` domain emails.**
The `.invalid` TLD is reserved and guaranteed to never deliver email.
Use `qa-[role]-[timestamp]@[project]-test.invalid` — never a real domain.

**Cleanup always runs after the suite.**
Even if tests fail. Wrap cleanup in `afterAll` hooks AND run the
standalone cleanup script. Failing tests still create data on the server.

**Two-device tests always use `browser.newContext()`.**
Never share auth state between USER_A and USER_B in the same test.
Each context is a fresh, independent browser — simulates two real devices.
Always close both contexts in a `finally` block.

**Selectors prefer accessible roles over CSS.**
Use `getByRole`, `getByLabel`, `getByText` before `locator('.class')`.
This makes tests more resilient to UI changes and works across frameworks.

**Time-sensitive assertions use exact timeouts from SPEC.**
If SPEC says "within 10 seconds" — `toBeVisible({ timeout: 10000 })`.
Don't use arbitrary timeouts — they hide real performance regressions.

**Never hardcode the base URL.**
Always read from `process.env.BASE_URL`.
Never fallback to localhost in production test runs.

**Video and trace only on failure.**
`video: 'retain-on-failure'` — don't record passing tests.
Videos and traces are large. Only keep them when they're needed.
