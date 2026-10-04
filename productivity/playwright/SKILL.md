---
name: playwright
description: Use when testing or validating the client UI end-to-end - verifying a page renders, a form submits, navigation works, or checking visual/responsive behavior in a real browser. Use when the user asks to "test", "check", or "verify" something in the app that requires clicking through the UI, not just unit tests.
---

# Playwright Browser Automation

Write and run a small, purpose-built Playwright script for the task at hand rather than reaching for a generic pre-built test. Most browser-verification tasks in this repo are one-off: does this page render, does this form submit, does this flow redirect correctly.

## This Repo's Setup

- `client/` — Angular app, served via `npm start` (`ng serve --host 0.0.0.0 --port 4200`) → `http://localhost:4200`
- `agent/` — Express API the client talks to, via `npm run dev` → `http://localhost:3000`
- Neither package currently depends on Playwright. Install it once per machine as a devDependency before first use:
  ```bash
  npm install -D @playwright/test --prefix client
  npx --prefix client playwright install chromium
  ```
  (Or install globally in a scratch directory if you'd rather not touch `client/package.json` for an ad-hoc check.)

## Workflow

1. **Confirm the dev server is actually running** before writing a script — don't assume port 4200 (and 3000, if the flow touches the API) is up. Start it if it isn't (`npm start` in `client/`, `npm run dev` in `agent/`), or ask for the URL if testing something already deployed.
2. **Write the script to a scratch path** (this session's scratchpad directory, or `/tmp`), never into `client/` — these are throwaway verification scripts, not part of the app.
3. **Parameterize the URL** as a constant at the top of the script so it's obvious what's being tested.
4. **Run with a visible browser by default** (`headless: false`) when a human is watching / debugging; use `headless: true` for a quick unattended check or when running from a non-interactive context.
5. **Always wait on real signals** (`waitForSelector`, `waitForURL`, `waitForLoadState('networkidle')`), never a fixed `waitForTimeout` as the only guard — Angular's change detection and API round-trips make fixed sleeps flaky.

## Minimal Script Template

```javascript
// scratch/playwright-check.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:4200'; // parameterize, don't hardcode inline below

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    await page.goto(TARGET_URL, { waitUntil: 'networkidle' });
    console.log('Title:', await page.title());

    // ... actions specific to the task ...

    await page.screenshot({ path: 'scratch/screenshot.png', fullPage: true });
  } finally {
    await browser.close();
  }
})();
```

Run with: `node scratch/playwright-check.js`

## Common Patterns

**Fill and submit a form** (e.g. a job-request form in `client/`):
```javascript
await page.goto(`${TARGET_URL}/requests/new`);
await page.fill('input[formcontrolname="name"]', 'Test Job');
await page.selectOption('select[formcontrolname="type"]', 'http');
await page.click('button[type="submit"]');
await page.waitForSelector('.success-message, [role="alert"]');
```

**Check a list/status page renders data from the API:**
```javascript
await page.goto(`${TARGET_URL}/requests`);
await page.waitForLoadState('networkidle');
const rowCount = await page.locator('table tbody tr').count();
console.log('Rows rendered:', rowCount);
```

**Responsive check across viewports:**
```javascript
const viewports = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'mobile', width: 375, height: 667 },
];
for (const v of viewports) {
  await page.setViewportSize({ width: v.width, height: v.height });
  await page.goto(TARGET_URL, { waitUntil: 'networkidle' });
  await page.screenshot({ path: `scratch/${v.name}.png`, fullPage: true });
}
```

**Multi-tenant check** (this app is multi-tenant — verify tenant isolation when relevant):
```javascript
// Set whatever header/localStorage/cookie this app uses to select tenant context
await page.goto(TARGET_URL);
await page.evaluate((tenantId) => localStorage.setItem('tenantId', tenantId), 'tenant-a');
await page.reload();
```
Confirm the actual mechanism (header vs. localStorage vs. route param) by reading how `client/src` sets tenant context before assuming this pattern.

## Selectors

Prefer, in order: `role=` / accessible name, `text=`, a stable `data-testid` if present, Angular `formcontrolname`/component selectors, then CSS as a last resort. Avoid brittle nth-child selectors.

## Tips

- Use `slowMo: 100` when a human needs to actually watch the run happen
- Always wrap the page interaction in `try/finally` so `browser.close()` runs even on failure
- `console.log` progress as you go — output is the only feedback while headless
- Don't commit scratch scripts or screenshots to the repo

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `browserType.launch: Executable doesn't exist` | Run `npx playwright install chromium` |
| Element not found immediately after navigation | Angular hasn't finished rendering — add `waitForSelector` or `waitForLoadState('networkidle')` |
| Works locally, flaky in CI | Fixed timeouts instead of condition-based waits — replace `waitForTimeout` with a real wait condition |
