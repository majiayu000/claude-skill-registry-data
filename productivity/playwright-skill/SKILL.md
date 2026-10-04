---
name: playwright-skill
description: Complete browser automation with Playwright. Auto-detects dev servers, writes clean test scripts to /tmp. Test pages, fill forms, take screenshots, check responsive design, validate UX, test login flows, check links, automate any browser task. Use when user wants to test websites, automate browser interactions, validate web functionality, or perform any browser-based testing.
---

**IMPORTANT - Path Resolution:**
Determine the skill directory from where this SKILL.md was loaded. Replace `$SKILL_DIR` with that path in all commands below.

Common installation paths:
- Plugin system: `~/.claude/plugins/marketplaces/playwright-skill/skills/playwright-skill`
- Manual global: `~/.claude/skills/playwright-skill`
- Project-specific: `<project>/.claude/skills/playwright-skill`

# Playwright Browser Automation

## CRITICAL WORKFLOW

Follow these steps in order for every request:

**1. Detect dev servers** (localhost testing — run this first, always):
```bash
cd $SKILL_DIR && node -e "require('./lib/helpers').detectDevServers().then(s => console.log(JSON.stringify(s)))"
```
- 1 server found → use it automatically, inform user
- Multiple found → ask user which one
- None found → ask for URL or offer to start dev server

**2. Write script to `/tmp`** — never write to skill directory or user's project:
```
/tmp/playwright-test-<task>.js
```

**3. Execute via run.js:**
```bash
cd $SKILL_DIR && node run.js /tmp/playwright-test-<task>.js
```

## Script Template

Every script must follow this structure:

```javascript
const { chromium } = require('playwright');
const TARGET_URL = 'http://localhost:3001'; // detected or user-provided

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  try {
    // automation here
  } catch (e) {
    console.error('Error:', e.message);
  } finally {
    await browser.close();
  }
})();
```

## Inline Execution

For quick one-off tasks, skip writing a file:
```bash
cd $SKILL_DIR && node run.js "
await page.goto('http://localhost:3001');
await page.screenshot({ path: '/tmp/shot.png', fullPage: true });
console.log('Done');
"
```

Use inline for: screenshots, element checks, page title.
Use files for: multi-step flows, responsive tests, anything user might re-run.

## Setup

```bash
cd $SKILL_DIR && npm run setup
```

Only needed once. Installs Playwright and Chromium.

## Available Helpers

```javascript
const helpers = require('./lib/helpers');

await helpers.detectDevServers()              // scan common ports — use FIRST
await helpers.safeClick(page, selector)       // click with retry
await helpers.safeType(page, sel, text)       // type with clear
await helpers.takeScreenshot(page, name)      // timestamped screenshot to /tmp
await helpers.handleCookieBanner(page)        // dismiss common accept banners
await helpers.extractTableData(page, sel)     // table → { headers, rows }
await helpers.createContext(browser)          // context with env headers merged
await helpers.authenticate(page, creds)       // fill + submit login form
await helpers.retryWithBackoff(fn)            // exponential backoff wrapper
await helpers.waitForPageReady(page)          // smart wait: networkidle + selector
```

## Custom Headers

Identify automated traffic or pass auth tokens globally:

```bash
# Single header
PW_HEADER_NAME=X-Automated-By PW_HEADER_VALUE=playwright-skill \
  cd $SKILL_DIR && node run.js /tmp/script.js

# Multiple headers (JSON)
PW_EXTRA_HEADERS='{"X-Automated-By":"playwright-skill","X-Debug":"true"}' \
  cd $SKILL_DIR && node run.js /tmp/script.js
```

Headers apply automatically when using `helpers.createContext(browser)`.
For raw Playwright API, use the injected `getContextOptionsWithHeaders(options)`.

## Rules

- **Visible browser** — always `headless: false` unless user explicitly says "headless" or "background"
- **Parameterize URLs** — put URL in `TARGET_URL` constant at top of every script
- **Wait strategies** — use `waitForURL`, `waitForSelector`, `waitForLoadState`, never fixed `waitForTimeout`
- **Error handling** — always wrap in try/catch, close browser in finally block

## Troubleshooting

```bash
# Playwright not installed
cd $SKILL_DIR && npm run setup

# Module not found — always run via run.js, never node directly on script
cd $SKILL_DIR && node run.js /tmp/script.js

# Element not found — add explicit wait
await page.waitForSelector('.target', { timeout: 10000 })

# Browser doesn't open — check headless: false and display availability
```

For advanced patterns (network interception, visual regression, auth sessions, CI/CD):
see [API_REFERENCE.md](API_REFERENCE.md)
