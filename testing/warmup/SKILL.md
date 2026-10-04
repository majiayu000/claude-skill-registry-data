---
name: warmup
description: Get a chef account warm and on standby - server up, authenticated, routes compiled, browser open. Usage - /warmup [account] where account is chef-bob (default), agent, or developer.
user-invocable: true
---

# Warmup - Get a Chef Account on Standby

Get an account warm and ready for real-time interaction. "Standby" means: server responding, session authenticated, key routes pre-compiled (no cold-start lag), browser open with live session.

## Arguments

- `account` (optional): Which `.auth/*.json` file to use. Default: `chef-bob`. Options: `chef-bob`, `agent`, `developer`.
- `port` (optional): Which port. Default: `3100`.

Parse from user input. Examples:

- `/warmup` -> chef-bob on 3100
- `/warmup agent` -> agent on 3100
- `/warmup developer 3000` -> developer on 3000
- `/warmup chef-bob 3100` -> chef-bob on 3100

## Procedure

Run the warmup script. It handles everything: server check/start, auth, route warming, browser launch.

```bash
bash scripts/warmup.sh <account> <port>
```

The script:

1. **Server check** - verifies port is responding. If not, kills stuck processes and starts `npm run dev`
2. **Auth** - hits `/api/e2e/auth` with credentials from `.auth/<account>.json`, captures session cookie
3. **Route warming** - curls 6 key routes with the session cookie so Next.js compiles them ahead of time
4. **Browser launch** - opens Playwright Chromium with injected session cookie, navigates to dashboard
5. **Screenshot** - saves `tmp-warmup/dashboard.png` as proof

## After Warmup

- Read the screenshot at `tmp-warmup/dashboard.png` and show it to the user
- Report which routes compiled successfully
- The browser stays open for the user to interact with in real time
- State file at `tmp-warmup/warmup-state.json` has session token for any follow-up requests

## If Something Fails

- **Server won't start**: Check if another process holds the port (`netstat -ano | grep :<port>`), kill it
- **Auth fails 403**: `E2E_ALLOW_TEST_AUTH=true` must be in `.env.local`
- **Auth fails 401**: Account may not exist in DB. Run `npx tsx scripts/setup-demo-accounts.ts`
- **Browser won't launch**: Playwright not installed. Run `npx playwright install chromium`

## Browser-Only Mode

If the server is already warm and you just need a browser with a saved session:

```bash
node scripts/warmup-browser.mjs tmp-warmup/warmup-state.json
```

This skips server check and route warming, just launches the browser with the last saved session token.

## Cleanup

Temp files created: `tmp-warmup/` directory. Not gitignored by default (add to .gitignore if desired). Cleaned up by `/close-session` or manually:

```bash
rm -rf tmp-warmup/
```
