---
name: spa-fetch
description: "Fetch rendered content from JavaScript-driven or login-gated pages with Playwright, including internal sites behind SSO or bot checks, when WebFetch cannot. Skip static HTML (WebFetch first), API endpoints (curl or MCP), and official Anthropic docs."
argument-hint: "<url> [css-selector] [--html]"
allowed-tools: Bash, Read, AskUserQuestion
disable-model-invocation: false
---

Fetch rendered content from a JavaScript-heavy SPA site.

Arguments: $ARGUMENTS

## Script

`spa-fetch.js` in this skill's base directory (shown above as "Base directory for this skill: ...").

All bash commands below use `<base-dir>` as a placeholder — substitute the actual base directory path.

## Steps

### 1. Headless fetch

```bash
node <base-dir>/spa-fetch.js <url> [css-selector] [--html]; echo "EXIT:$?"
```

Use `dangerouslyDisableSandbox: true` and `timeout: 45000`.

Check the `EXIT:` line in stdout to determine the result:

- **EXIT:0**: success — go to step 3
- **EXIT:10**: login required — go to step 2
- **EXIT:11**: bot detection (Cloudflare/CAPTCHA) — go to step 2 (establish browser session first)
- **EXIT:1**: error — report to user

### 2. Login flow (only if exit code 10)

Run the login browser in background:

```bash
node <base-dir>/spa-fetch.js --open-login <url>
```

Use `dangerouslyDisableSandbox: true`, `timeout: 300000`, and `run_in_background: true`.

Then **immediately** prompt interactively:
> 로그인이 필요합니다. 브라우저가 열렸으니 5분 내 로그인해주세요 (timeout 300s — 초과 시 background process가 종료되어 인증이 저장되지 않습니다). 로그인 완료 후 자동으로 닫힙니다. 닫히면 알려주세요.

When user confirms, retry step 1. If step 1 still returns EXIT:10, the background process likely timed out before login completed — re-run step 2 and prompt the user again.

### 3. Output

Present the fetched content, or use it for the requested analysis.

### 4. Deep exploration (optional)

If the fetched content is a list/table and the user wants detail from individual items:

1. Write a custom Playwright script to `$TMPDIR`
2. Reuse the auth profile at `<base-dir>/.spa-auth/<domain>/`
3. Require Playwright from `<base-dir>/node_modules/playwright`
4. Use `chromium.launchPersistentContext(profileDir, { headless: true })` for session reuse

Boilerplate:

```js
const { chromium } = require('<base-dir>/node_modules/playwright');
const path = require('path');
const profileDir = path.join('<base-dir>', '.spa-auth', '<domain>');

(async () => {
  const ctx = await chromium.launchPersistentContext(profileDir, {
    headless: true,
    timeout: 30000,
    args: ['--disable-blink-features=AutomationControlled'],
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  });
  const page = ctx.pages()[0] || await ctx.newPage();
  // ... navigate, interact, extract
  await ctx.close();
})();
```

Use `dangerouslyDisableSandbox: true` and appropriate timeout.

## Rules

- Always use `dangerouslyDisableSandbox: true`
- Do NOT combine --open-login with fetch in a single call
- If script not found, run `cd <base-dir> && npm install`
