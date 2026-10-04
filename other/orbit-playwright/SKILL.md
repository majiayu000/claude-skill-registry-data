---
name: orbit-playwright
description: Playwright (browser automation) end-to-end suite for a WordPress plugin — first-time setup, write specs, run, watch (UI / headed / debug / trace viewer), HTML reporter. Covers admin pages, frontend output, block editor, login flow, settings forms. Use when the user says "Playwright", "E2E", "browser test", "headless", "trace viewer", "debug flaky test", or any first-time setup of E2E for their plugin.
---

# 🪐 orbit-playwright — Browser automation E2E

The browser-test skill. Setup, write, run, debug — every Playwright workflow Orbit uses.

---

## First-time setup (one command)

```bash
# Already done if you ran /orbit-install. Otherwise:
cd ~/Claude/orbit
npm install
npx playwright install chromium firefox webkit

# Save admin cookies (one time per Docker site)
WP_TEST_URL=http://localhost:8881 \
  npx playwright test tests/playwright/auth.setup.js --project=setup
```

`auth.setup.js` logs in as admin, saves the session to `.auth/admin.json`. Every other test reuses these cookies.

---

## Run tests — 5 ways

### 1. Headless (CI mode — default)
```bash
WP_TEST_URL=http://localhost:8881 npx playwright test
```
Fast, no browser window. Used in CI.

### 2. UI Mode (best for development)
```bash
npx playwright test --ui
```
Opens the test runner GUI: time-travel debugger, DOM snapshots at every step, network/console/source tabs, watch mode (re-runs on file save). **Use this 90% of the time.**

### 3. Headed (watch the browser)
```bash
npx playwright test --headed --slowMo=500
```
Real Chromium window, 500ms delay between actions. Good for verifying a flow visually.

### 4. Debug (step through)
```bash
npx playwright test --debug
```
Playwright Inspector — set breakpoints, step over, pick locators by hovering.

### 5. Trace Viewer (post-mortem on a failure)
```bash
npx playwright show-trace test-results/.../trace.zip
```
Full forensic replay — DOM, network, console, screenshots. Traces auto-save on first retry (configured in `playwright.config.js`).

---

## HTML report after any run

```bash
npx playwright show-report reports/playwright-html
```

Pass/fail per test, screenshots of failures, traces, diffs. Auto-opens in browser.

---

## Project structure

```
tests/playwright/
├── playwright.config.js     # 7 projects: setup, chromium, firefox, mobile, tablet, a11y, visual
├── auth.setup.js            # Admin login → saves cookies
├── helpers.js               # assertPageReady, gotoAdmin, snapPair, attachConsoleErrorGuard
├── templates/               # Copy these to start
│   ├── generic-plugin/
│   ├── elementor-addon/
│   ├── gutenberg-block/
│   ├── seo-plugin/
│   ├── woocommerce/
│   └── theme/
└── flows/                   # Custom UAT flow specs (per plugin)
```

---

## Writing a new spec

Copy a template, replace selectors:

```bash
cp tests/playwright/templates/generic-plugin/core.spec.js \
   tests/playwright/my-plugin/core.spec.js
```

Edit the new spec:

```js
const { test, expect } = require('@playwright/test');
const { gotoAdmin, assertPageReady, attachConsoleErrorGuard } = require('../helpers');

test.describe('My Plugin — admin', () => {
  test.beforeEach(async ({ page }) => attachConsoleErrorGuard(page));

  test('Settings page loads cleanly', async ({ page }) => {
    await gotoAdmin(page, '/wp-admin/admin.php?page=my-plugin');
    await assertPageReady(page);

    await expect(page.getByRole('heading', { name: 'My Plugin Settings' })).toBeVisible();
    await expect(page).toHaveScreenshot('settings-default.png', { maxDiffPixelRatio: 0.02 });
  });

  test('Save settings persists', async ({ page }) => {
    await gotoAdmin(page, '/wp-admin/admin.php?page=my-plugin');
    await page.getByLabel('API Key').fill('test-key');
    await page.getByRole('button', { name: 'Save Settings' }).click();
    await expect(page.getByText('Settings saved')).toBeVisible();

    // Verify persisted
    await page.reload();
    await expect(page.getByLabel('API Key')).toHaveValue('test-key');
  });
});
```

---

## Helper conventions (use these — don't reinvent)

| Helper | Purpose |
|---|---|
| `gotoAdmin(page, url)` | Navigate to WP-Admin with auth + waits for page-ready |
| `assertPageReady(page)` | Asserts no PHP fatal, no JS console error, page < 4s, all images loaded |
| `attachConsoleErrorGuard(page)` | Fails any test that produces a JS console error from the plugin |
| `snapPair(page, n, slug, side, dir)` | Side-by-side screenshot helper for `/orbit-uat-compare` |
| `discoverNavLinks(page)` | Print all nav links — used when writing first spec for an unknown plugin |

Source: `tests/playwright/helpers.js`.

---

## Debug a flaky test

```bash
# Run that one test with full trace + retry
npx playwright test flows/my-test.spec.js --project=chromium --trace on --retries 0

# Show the trace
npx playwright show-trace test-results/.../trace.zip
```

Common causes + fixes:
- **Parallelism collision** → add `test.describe.configure({ mode: 'serial' })` for state-mutating tests
- **Timing** → use Playwright's auto-waiting (`page.locator(...).waitFor()`) — never `waitForTimeout`
- **Network** → mock with `page.route('**/api/**', route => route.fulfill({...}))`
- **Animation** → set `animations: 'disabled'` in screenshot options
- **Auth expired** → re-run `auth.setup.js`

---

## Multi-browser / multi-viewport

`playwright.config.js` has 7 projects:

```bash
# Just mobile
npx playwright test --project=mobile-chrome

# All viewports
npx playwright test --project=mobile-chrome --project=tablet --project=chromium

# Just one project + one file
npx playwright test --project=chromium tests/playwright/my-plugin/core.spec.js
```

---

## Configure for your plugin

`qa.config.json` drives everything:

```json
{
  "plugin": {
    "adminSlug": "/wp-admin/admin.php?page=my-plugin"
  },
  "visualUrls": [
    "/wp-admin/admin.php?page=my-plugin",
    "/wp-admin/admin.php?page=my-plugin-settings"
  ],
  "wpEnv": { "port": 8881 }
}
```

Playwright reads this via `tests/playwright/playwright.config.js`. Edit the config once → every spec inherits.

---

## CI / GitHub Actions

```yaml
- run: npx playwright install --with-deps chromium
- run: WP_TEST_URL=http://localhost:8881 npx playwright test
- if: always()
  uses: actions/upload-artifact@v4
  with:
    name: playwright-report
    path: reports/playwright-html/
```

Runs identically to local — no environment-specific config.

---

## Common errors

| Error | Fix |
|---|---|
| `Error: net::ERR_CONNECTION_REFUSED at http://localhost:8881` | wp-env not running → `/orbit-docker-site` |
| `Test timeout of 30000ms exceeded` | Slow page or slow assertion → either fix the perf bug or bump `timeout: 60000` for that test |
| `expect(locator).toBeVisible() received hidden` | Selector is right but element is `display:none` — use `.toHaveCount(1)` instead, or fix the visibility |
| `Could not find admin.json` | Auth setup not run → re-run `auth.setup.js` |
| `Strict mode violation: locator resolved to N elements` | Selector matches multiple — narrow with `.first()` or use a more specific role/label |

---

## Pair with related skills

- Visual regression baseline updates → `/orbit-visual-regression`
- User journey + click depth → `/orbit-user-flow`
- Plugin-vs-plugin compatibility → `/orbit-conflict-matrix`
- Performance timing → `/orbit-editor-perf`

This skill is the foundation; the others are specialised use-cases on top.
