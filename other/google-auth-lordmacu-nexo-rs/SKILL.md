---
name: Google OAuth
description: Authenticate against the user's own Google account (Gmail, Drive, Calendar, Sheets, etc.) via the installed-application OAuth 2.0 flow and make authenticated HTTP calls.
requires:
  bins: []
  env: []
---

# Google OAuth

Drives the agent's access to the user's Google services — Gmail,
Drive, Calendar, Sheets, Photos, YouTube Data, Tasks, and every other
`*.googleapis.com` endpoint. Backed by 4 tools (`google_auth_start`,
`google_auth_status`, `google_call`, `google_auth_revoke`) that wrap a
real OAuth 2.0 installed-application flow with a loopback callback and
persistent refresh tokens.

## Use when

- "Read my last 10 Gmail emails"
- "Create a Calendar event for tomorrow at 3pm"
- "Find the 'Q4 budget' document in my Drive"
- "Add a row to my expenses Sheet"
- "Delete the videos I uploaded to YouTube this month"

## Do not use when

- **Google apps that do not belong to this user** (an admin's Drive,
  someone else's Gmail) — each agent can only access the account that
  granted consent.
- **Free actions that do not require account auth** (public search,
  no-account maps, etc.) — use dedicated tools (`ext_wikipedia_search`,
  etc.) that do not consume Google API quota.
- **Gemini / AI Studio** — that path does not use OAuth; it uses
  direct API-key auth (`GEMINI_API_KEY`).

## Canonical workflow

First turn where the user asks for a Google action:

```
1. google_auth_status()
   → { authenticated: false, reason: "no tokens on file" }

2. google_auth_start()
   → { ok: true, url: "https://accounts.google.com/o/oauth2/v2/auth?...",
       redirect_uri: "http://127.0.0.1:8765/callback",
       instructions: "Open this URL..." }

3. Send this to the user in chat:
   "To let me read your Gmail, open this link and approve permissions:
    <url>. If you're connected through a remote server, use an SSH
    tunnel: `ssh -L 8765:127.0.0.1:8765 <host>`. Tell me when you're done."

4. Wait for the user's next message. DO NOT retry tools meanwhile.

5. When the user replies "done" (or similar):
   google_auth_status()
   → { authenticated: true, expires_in_secs: 3589, has_refresh: true,
       scopes: [...] }

6. Now run `google_call(...)` for the user's requested task.
```

All following calls (including future sessions days later) only need
direct **`google_call`**. The persisted refresh token automatically
renews access tokens — the user does not see consent again unless they
revoke access.

## Tool reference

| Tool | When to call |
|---|---|
| `google_auth_status` | Before the first Google operation in each session. Fast diagnostic — no network calls. |
| `google_auth_start` | Only if `status.authenticated == false`. Requires human action (click + browser consent). No retries/polling by the LLM — wait for the next user message. |
| `google_call` | The workhorse. 99% of your calls. |
| `google_auth_revoke` | Only if the user explicitly asks to disconnect Google. Invalidates the token in Google. |

## `google_call` — API examples

### Gmail

```json
{ "method": "GET",
  "url": "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=10" }

{ "method": "GET",
  "url": "https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}?format=full" }

{ "method": "POST",
  "url": "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
  "body": { "raw": "<base64-encoded RFC 2822 message>" } }
```

Required scope: `gmail.readonly` (read) or `gmail.modify` (send/trash).

### Calendar

```json
{ "method": "GET",
  "url": "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=2026-04-24T00:00:00Z" }

{ "method": "POST",
  "url": "https://www.googleapis.com/calendar/v3/calendars/primary/events",
  "body": {
    "summary": "Dentist",
    "start": {"dateTime": "2026-04-25T15:00:00-05:00"},
    "end":   {"dateTime": "2026-04-25T16:00:00-05:00"}
  } }
```

Scope: `calendar.readonly` or `calendar.events`.

### Drive

```json
{ "method": "GET",
  "url": "https://www.googleapis.com/drive/v3/files?pageSize=50&q=name contains 'budget'" }

{ "method": "GET",
  "url": "https://www.googleapis.com/drive/v3/files/{fileId}?fields=*" }
```

Scope: `drive.readonly` or `drive`.

### Sheets

```json
{ "method": "GET",
  "url": "https://sheets.googleapis.com/v4/spreadsheets/{id}/values/Sheet1!A1:D100" }

{ "method": "POST",
  "url": "https://sheets.googleapis.com/v4/spreadsheets/{id}/values/Sheet1!A1:append?valueInputOption=USER_ENTERED",
  "body": { "values": [["2026-04-24", "coffee", 5.50, "food"]] } }
```

Scope: `spreadsheets.readonly` or `spreadsheets`.

## Scopes commonly requested

Configure these in `agents.yaml` → `google_auth.scopes`:

| Short name | Canonical URL | Scope |
|---|---|---|
| `userinfo.email` | `https://www.googleapis.com/auth/userinfo.email` | user's email |
| `userinfo.profile` | `https://www.googleapis.com/auth/userinfo.profile` | profile name + picture |
| `gmail.readonly` | `/auth/gmail.readonly` | read-only email (no label changes, no send) |
| `gmail.send` | `/auth/gmail.send` | send only, no read |
| `gmail.modify` | `/auth/gmail.modify` | everything except permanent delete |
| `calendar.readonly` | `/auth/calendar.readonly` | read calendar |
| `calendar.events` | `/auth/calendar.events` | create/edit events |
| `drive.readonly` | `/auth/drive.readonly` | read Drive |
| `drive.file` | `/auth/drive.file` | only files created by this app |
| `drive` | `/auth/drive` | full access (high risk) |
| `spreadsheets.readonly` | `/auth/spreadsheets.readonly` | read Sheets |
| `spreadsheets` | `/auth/spreadsheets` | read + write |
| `youtube.readonly` | `/auth/youtube.readonly` | read your channel data |

## Failure modes

- `401 Unauthorized` -> token expired. Run `google_auth_status`; if
  `authenticated: false`, call `google_auth_start` and request re-consent.
- `403 Forbidden` -> missing scope grant. Update
  `google_auth.scopes` in config, run `google_auth_revoke`, then run
  `google_auth_start` again (Google does not merge old and new scopes).
- `refresh_token` "invalid_grant" -> user revoked access, or the app is
  in "Testing" and 7 days passed. Run `google_auth_start` to refresh.
- Port 8765 is busy -> set `google_auth.redirect_port` to another free
  port in `agents.yaml`, and also update "Authorized redirect URI" in
  Google Cloud Console.

## Gotchas

- **Do not share refresh tokens across agents.** Each agent has its
  own profile and token file.
- **Scopes are fixed at consent time.** If you add scopes later, revoke
  and re-consent. Google does not expand scopes on an existing token.
- **Testing-mode apps**: refresh tokens may expire after 7 days. For
  production, publish the app in Google Cloud Console.
- **Rate limits are project-scoped, not user-scoped**: if multiple
  agents share one `client_id`, they share quota.
