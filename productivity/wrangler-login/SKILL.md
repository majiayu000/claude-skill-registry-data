---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: wrangler-login
description: >
  Non-interactive wrangler OAuth login using playwriter to automate the
  Cloudflare consent flow in the user's browser. Use when wrangler auth
  is expired ("Failed to fetch auth token: 400 Bad Request") or when
  `wrangler whoami` fails. Delegate to a subagent Task to save context.
---

# wrangler-login

Automate `wrangler login` when the OAuth token is expired and the agent
cannot run interactive commands. Uses playwriter to click through the
Cloudflare consent page in the user's existing Chrome session.

## Prerequisites

The user **must already be logged in to Cloudflare** in their browser before
you attempt this flow. The Cloudflare OAuth consent page is protected by a
Turnstile captcha that agents cannot bypass. If the user is not logged in,
Cloudflare will show a login page with Turnstile, and the automation will
fail.

**If Cloudflare is not already logged in:** stop immediately and ask the
user to log in to `https://dash.cloudflare.com` in their browser first,
then retry.

## When to use

- `wrangler whoami` fails or returns an auth error
- Deploy commands fail with "Failed to fetch auth token: 400 Bad Request"
- Any wrangler command says "set a CLOUDFLARE_API_TOKEN environment variable"

## How to run

Delegate to a **general** subagent Task so the playwriter back-and-forth
doesn't eat your main context. Pass this as the prompt:

```
Automate wrangler login via playwriter. Follow these steps exactly:

IMPORTANT: This only works if the user is already logged in to Cloudflare
in their browser. The consent page has a Turnstile captcha that agents
cannot solve. If at any point you see a Turnstile challenge, a login form,
or a CAPTCHA, STOP and tell the user to log in to https://dash.cloudflare.com
in their browser first, then retry.

1. Start wrangler login in a tuistory background session:
   bunx tuistory launch "pnpm exec wrangler login" -s wrangler-login
   bunx tuistory -s wrangler-login wait "/https:\/\/dash\.cloudflare\.com/i" --timeout 15000
   bunx tuistory read -s wrangler-login

2. Copy the full OAuth URL from tuistory output.

3. Load the playwriter skill (run `playwriter skill`), then open a
   playwriter session and navigate to that URL:
   playwriter session new
   playwriter -s <id> -e '
   state.page = await context.newPage();
   await state.page.goto("<OAUTH_URL>", { waitUntil: "domcontentloaded" });
   await waitForPageLoad({ page: state.page, timeout: 8000 });
   console.log("URL:", state.page.url());
   await snapshot({ page: state.page, showDiffSinceLastCall: false }).then(console.log);
   '

4. The consent page shows "Wrangler wants to access your account".
   Click through in order:
   a. Select the account button (e.g. "Beats.by.morse@gmail.com's Account")
   b. Click "Review permissions"
   c. Wait 2s for permissions list to load
   d. Click the Authorize button: [data-test-id="oauth-consent-form-allow-button"]

5. After authorize, the page redirects to
   https://welcome.developers.workers.dev/wrangler-oauth-consent-granted
   and wrangler prints "Successfully logged in."

6. Verify: pnpm exec wrangler whoami

7. Clean up:
   bunx tuistory -s wrangler-login close
   playwriter -s <id> -e 'await state.page.close()'

Return the wrangler whoami output to confirm success.
```

## Gotchas

- `wrangler login` must be running **before** you navigate to the OAuth
  URL. It starts a local HTTP server on port 8976 that receives the
  callback. If you navigate first, the redirect to localhost will fail.

- The consent page requires selecting an account before "Review permissions"
  becomes clickable. If you click Review without selecting, it shows
  "Select at least one account".

- The Authorize button uses `data-test-id`, not `role`. Use
  `state.page.locator('[data-test-id="oauth-consent-form-allow-button"]')`
  instead of `getByRole`.

- If the user has multiple Cloudflare accounts, the consent page shows
  multiple account buttons. Pick the one that owns the Workers/D1
  resources.

- The OAuth URL contains a `code_challenge` that is unique per
  `wrangler login` invocation. Never reuse a URL from a previous run.
