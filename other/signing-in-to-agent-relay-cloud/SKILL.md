---
name: signing-in-to-agent-relay-cloud
description: Sign a person in to Agent Relay Cloud from a running agent session through the OAuth device flow, with no API key or dashboard wizard - start the device grant, let the human approve it, poll for tokens, refresh them, read the account and workspace from whoami, and hand the session to the official CLI without printing a token. Use when an agent needs a Cloud access token or the person's user and workspace ids, including as the first step of an Agent Relay agent-driven signup.
---

# Sign In to Agent Relay Cloud

Use the existing OAuth device flow. No API key, invitation, dashboard wizard,
or pre-existing Agent Relay account is required. Only the human approves the
sign-in; never approve access on their behalf, ask for their password, or
operate the approval page yourself.

Paths below are relative to the Cloud API base, `https://agentrelay.com/cloud`,
including its `/cloud` prefix. When a guide names a different Cloud base (for
example a local development stack), use that exact base throughout and never
fall back to production.

## HTTP client

Use `curl` or `fetch`. Avoid Python's `urllib` or `requests` with their
default User-Agent: the device-token endpoint answers them with HTTP 403 and no
JSON body (tracked in AgentWorkforce/cloud#4254). Never print a raw auth
response while debugging; on success it contains tokens. Send JSON request
bodies with `Content-Type: application/json`, set a 30-second request timeout,
and check every response status before proceeding.

## 1. Start the device grant

`POST /api/v1/auth/device/start` with:

```json
{"client_name":"My agent setup"}
```

An agent-driven signup guide also passes its product as `signup_source`
(`"teams"` or `"flows"`); keep the value the guide names. Omit it otherwise.

Expect HTTP 201 with `device_code`, `user_code`, `verification_uri_complete`,
`verification_uri`, `interval` (seconds), and `expires_in` (seconds). Keep
`device_code` private. Open `verification_uri_complete` in the person's
browser with the OS URL opener (for example macOS `open`, with the URL passed as
a separate argument, never interpolated into shell code), or give them the link
if no opener is available. Show the `user_code` so they can compare it. The page
lets them sign in with Google, review the requesting device, and Approve or
Deny. A signup marker in the returned URL creates the right account type;
preserve it through sign-in. Do not call `/auth/device/approve` yourself.

For a fresh signup, you can open `/api/auth/google/start?next=<encoded-return-path>`
on the same Cloud base first (in production,
`https://agentrelay.com/cloud/api/auth/google/start?next=<encoded-return-path>`), where `encoded-return-path` is the URL-encoded pathname plus query of
`verification_uri_complete`. This opens Google immediately and returns to the
same device approval with its code and signup marker intact. Never open the
production URL for a non-production base: that would sign the human in to
production instead.

## 2. Poll for tokens

While the browser is open, wait `interval` seconds between POSTs to
`/api/v1/auth/device/token` with this JSON (substitute the private
`device_code`):

```json
{"grant_type":"urn:ietf:params:oauth:grant-type:device_code","device_code":"<device_code>"}
```

- `authorization_pending`: keep waiting; respect a returned interval.
- `slow_down`: increase the interval by at least 5 seconds.
- HTTP 429: respect `Retry-After` and increase the interval.
- HTTP 5xx or request timeout: retry with backoff, bounded by `expires_in`.
- `access_denied`: stop. `expired_token` or `invalid_grant`: explain and start
  a new grant only if the person still wants to continue. Never poll past
  expiry.

HTTP 200 returns `access_token`, `refresh_token`, `access_token_expires_at`,
`refresh_token_expires_at`, `api_url` and `token_type`. Keep credentials in
memory or a private file (directory 0700, file 0600) outside repositories.
Never echo tokens, put them in chat or URLs, or dump full authentication
responses. Use `Authorization: Bearer <access_token>` for subsequent Cloud
requests. Reject an `api_url` pointing at another origin; keep using the Cloud
base above.

## 3. Refresh before expiry

Before expiry, `POST /api/v1/auth/token/refresh` with
`{"refreshToken":"<refresh_token>"}`. The response uses camelCase:
`accessToken`, `refreshToken`, `accessTokenExpiresAt`, `refreshTokenExpiresAt`,
`apiUrl`. Replace both stored tokens atomically. Serialize refreshes: the
refresh token rotates and must not be shared between machines. An
invalid/expired refresh requires a new device login, not an endless retry.

## 4. Read the account and workspace

`GET /api/v1/auth/whoami`. Require `authenticated: true` and read `user.id`,
`user.email`, `currentWorkspace.id`, and `currentOrganization.id`. New signups
create a workspace automatically. Reuse it; do not create duplicate
accounts/workspaces. If `currentWorkspace` is missing, or an existing account
is in the wrong workspace, resolve that with the person before connecting or
activating anything. Never silently replace an existing connection to another
account.

## 5. Hand the session to the official CLI

When running a child process, pass these through its environment from your
private session object (never interpolate their values into logged commands):

```text
CLOUD_API_URL=<the Cloud base above; https://agentrelay.com/cloud in production>
CLOUD_API_ACCESS_TOKEN=<access_token>
CLOUD_API_REFRESH_TOKEN=<refresh_token>
CLOUD_API_ACCESS_TOKEN_EXPIRES_AT=<access_token_expires_at>
CLOUD_API_REFRESH_TOKEN_EXPIRES_AT=<refresh_token_expires_at>
```

The official CLI consumes this session. Refresh the parent session before
starting a long command; do not concurrently refresh it from parent and child
processes. Do not overwrite an existing CLI auth file or copy a session to
another machine. Delete temporary authentication files after the work is
complete.
