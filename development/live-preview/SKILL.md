---
name: live-preview
description: Opens browser, ensures dev server health, signs in, and maintains live preview during builds. Auto-fires when building features or fixing code. Navigates to pages being built and screenshots for verification.
user-invocable: true
---

# Live Preview (Auto-Fire During Builds)

This skill ensures the developer is always watching the website in real-time during builds. It fires automatically when feature work, bug fixes, or UI changes begin. It also handles server health, login, page navigation, and screenshot verification.

**Trigger conditions (auto-fire):**

- Feature development starts (before first Edit/Write of a build session)
- `/live-preview` invoked manually
- Builder agent begins execution
- Any UI/page work detected

## Phase 1: Server Health Check

### 1a. Check if dev server is running and responsive

```
curl -s -o /dev/null -w "%{http_code} %{time_total}s" --max-time 10 http://localhost:3100
```

**If HTTP 200/307 in under 10s:** Server healthy. Proceed to Phase 2.

**If no response or timeout:** Server is dead or zombie. Fix it:

1. Check what's on port 3100: `netstat -ano | grep ":3100.*LISTEN"`
2. If a process exists, check its memory: `tasklist | grep <PID>`
3. If memory > 8GB or unresponsive to curl for 30s: it's a zombie. Kill it: `taskkill //PID <PID> //F //T`
4. Wait for port to clear, then start fresh: `npm run dev` (background)
5. Wait for startup, re-test with curl

**Performance red flags:**

- Memory > 8GB = zombie, kill and restart
- Response time > 30s = stuck compilation, kill and restart
- EADDRINUSE = find and kill the holder, then start

### 1b. Note on Turbopack

Turbopack (`--turbo`) is NOT compatible with this codebase. The middleware imports `postgres` which needs Node.js `crypto` module. Turbopack runs middleware as edge runtime which lacks `crypto`. Do NOT attempt `--turbo`. Use standard webpack dev server.

## Phase 2: Browser Session

### 2a. Open browser if not already open

Use Playwright MCP tools to navigate to `http://localhost:3100/auth/signin`.

### 2b. Sign in

**Auth route:** `/auth/signin` (NOT `/sign-in`)

1. Read `.auth/agent.json` for credentials (agent account is the default test account)
2. If developer requests their own account, read `.auth/developer.json`
3. Use `browser_snapshot` to get element refs
4. Use `browser_fill_form` with email and password fields
5. Click "Sign In" button
6. Wait for redirect to `/dashboard`
7. Screenshot to confirm login success

**If "Invalid email or password":** Try agent account. If both fail, check database connectivity.

### 2c. Verify dashboard loads

Screenshot the dashboard. Confirm:

- Navigation sidebar visible
- Data cards populated (not $0.00 or empty)
- No build errors overlay
- No "Page Not Found" or 404

## Phase 3: Live Navigation During Builds

**This is the key behavior.** As code is written, navigate the browser to the pages being built so the developer watches in real-time.

### Rules:

1. **After editing a page file** (`app/**/page.tsx`): Navigate browser to that route
   - `app/(chef)/dashboard/page.tsx` -> navigate to `/dashboard`
   - `app/(chef)/recipes/[id]/page.tsx` -> navigate to `/recipes` (list page) or a known ID
   - `app/(chef)/menus/[id]/page.tsx` -> navigate to `/menus`
   - `app/(client)/my-events/[id]/page.tsx` -> navigate to a known event

2. **After editing a component** used on a specific page: Navigate to a page that uses it

3. **After fixing a build error**: Refresh the current page to verify the fix

4. **After any server action change**: Navigate to a page that exercises that action

### Navigation pattern:

```
# After each significant edit:
1. Wait 2-3 seconds for hot reload
2. browser_navigate to the relevant page
3. browser_take_screenshot
4. Read the screenshot to verify visually
5. If build error overlay: read error, fix it, repeat
6. If page loads clean: continue building
```

## Phase 4: Verification Screenshots

**Before declaring any build task complete:**

1. Navigate to every page that was modified
2. Take a screenshot of each
3. Read each screenshot and verify:
   - No build errors
   - No 404s
   - Data renders (not blank/zero)
   - UI looks correct
4. Report findings with screenshot evidence

**Never say "it's working" without a screenshot proving it.**

## Quick Reference

| Item             | Value                                                          |
| ---------------- | -------------------------------------------------------------- |
| Dev server port  | 3100                                                           |
| Auth route       | `/auth/signin`                                                 |
| Agent creds      | `.auth/agent.json`                                             |
| Developer creds  | `.auth/developer.json`                                         |
| Health check     | `curl -s -o /dev/null -w "%{http_code}" http://localhost:3100` |
| Turbopack        | NOT compatible (crypto/middleware issue)                       |
| Zombie threshold | >8GB memory or >30s response                                   |
