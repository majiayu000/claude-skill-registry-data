---
name: calendar-setup
description: "Step-by-step setup and troubleshooting for connecting an owner's Google Calendar to an OpenClaw agent with read and write access. Use when: setting up calendar access for the first time, fixing read-only access, re-authenticating a broken Google connection, explaining the difference between the owner's Google account and the agent's Google account, how an OpenClaw agent accesses Gmail or Google Workspace, where credentials are stored, how to use the agent inbox, how to give the agent write access to the owner's calendar, or guiding another agent or user through the email or calendar setup model."
---

# Calendar Setup

Use this skill when calendar access needs to be established or repaired.

## Core model

Treat these as separate identities:
- **Owner account**: the human's Google account and calendar
- **Agent account**: the PA's own Google account

The agent does not get calendar access automatically. The owner must share access, and the agent must authenticate the relevant Google account in `gog`.

## Standard setup

### 1. Owner shares the calendar

The owner should do this in Google Calendar:
1. Open `calendar.google.com`
2. Open the primary calendar's **Settings and sharing**
3. Under **Share with specific people**, add the agent email
4. Grant **Make changes to events**

If external sharing is blocked, the owner's Google Workspace admin has to allow it.

### 2. Authenticate with `gog`

```bash
gog auth add owner@company.com --services gmail,calendar,drive,contacts
gog auth list
```

Use the actual owner email. If a stale auth entry exists:

```bash
gog auth remove owner@company.com
gog auth add owner@company.com --services gmail,calendar,drive,contacts
```

### 3. Verify write access

```bash
START=$(date -u -d '+1 hour' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v+1H +%Y-%m-%dT%H:%M:%SZ)
END=$(date -u -d '+2 hours' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v+2H +%Y-%m-%dT%H:%M:%SZ)

GOG_ACCOUNT=owner@company.com gog calendar create primary \
  --summary "PA setup test, delete me" \
  --start "$START" \
  --end "$END"
```

Then confirm the event appears in the owner's calendar and delete it.

## Troubleshooting order

Work in this order:
1. Confirm whether the problem is about the owner account or the agent account.
2. Run `gog auth list` and confirm the needed account exists.
3. Confirm the shared calendar permission is **Make changes to events**.
4. Use `GOG_ACCOUNT=owner@company.com` explicitly in commands.
5. Retry after `gog auth remove` + `gog auth add` if auth is stale.

## Common failures

### Dashboard says connected, but writes fail
The dashboard may reflect the agent's own Google connection, not the owner's calendar permission. Re-check sharing and `GOG_ACCOUNT`.

### Insufficient permissions
The calendar was shared read-only. Re-share with **Make changes to events**.

### No browser or interactive auth is unavailable
Use an already-provisioned `gog` account if one exists. If no valid Google auth is available on the host, stop and report that manual re-authentication is required.

### Multiple calendars
Authenticate each account separately and use the specific calendar ID from:

```bash
GOG_ACCOUNT=owner@company.com gog calendar list
```

## Verification checklist

- [ ] Owner shared the correct calendar with the agent email
- [ ] Permission is `Make changes to events`
- [ ] `gog auth list` shows the required account
- [ ] Commands use explicit `GOG_ACCOUNT=...`
- [ ] A test event can be created and deleted

## Notes

- Do not print OAuth secrets or credential file contents in chat.
- Prefer the shortest path that restores working read/write calendar access.
- If the issue is really about Gmail or Drive access, switch to the `gog` skill after clarifying the exact service.

---

## Email Model Appendix

*(Absorbed from `openclaw-email-orientation` on 2026-05-09.)*

### Minimum Model
Any model. This appendix is explanation and troubleshooting only — no complex reasoning needed.

### The Core Concept

There are two separate accounts:

| | Account |
|---|---|
| **Owner** | The human's Google account (e.g. `owner@company.com`) |
| **Agent** | The PA's own Google account (e.g. `agent@agentdomain.com`) |

These are separate. Having an agent email does NOT automatically give access to the owner's email or calendar. To access the owner's email/calendar: (1) owner must share access with the agent email, and (2) agent must authenticate using `gog`.

### Key Paths and Files

| File | Purpose |
|---|---|
| `~/.openclaw/.gog/credentials.json` | gog OAuth client credentials |
| `~/.openclaw/agents/main/agent/auth-profiles.json` | OpenClaw auth profiles |
| `~/.openclaw/workspace/skills/gog/SKILL.md` | gog usage reference |

**Security rule:** Never show the contents of these files in chat. Mentioning the path is fine; printing the content is not.

### Common gog Commands

```bash
# One-time setup: load OAuth credentials
gog auth credentials /path/to/client_secret.json

# Add an account (opens browser for OAuth flow)
gog auth add owner@company.com --services gmail,calendar,drive,contacts,sheets,docs

# Verify the account was added
gog auth list

# Use the account in commands (always include GOG_ACCOUNT=...)
GOG_ACCOUNT=owner@company.com gog gmail search 'is:unread' --max 10

# Search email
GOG_ACCOUNT=owner@company.com gog gmail search 'newer_than:7d' --max 10

# Send email
GOG_ACCOUNT=owner@company.com gog gmail send \
  --to "recipient@example.com" \
  --subject "Hello" \
  --body "Message text"

# List calendar events in a time window
GOG_ACCOUNT=owner@company.com gog calendar events primary \
  --from "2026-04-01T09:00:00Z" \
  --to "2026-04-01T18:00:00Z"

# Create a calendar event
GOG_ACCOUNT=owner@company.com gog calendar create primary \
  --summary "Meeting" \
  --start "2026-04-02T10:00:00+00:00" \
  --end "2026-04-02T11:00:00+00:00"
```

### Additional Troubleshooting

**If "Token expired" error:**
```bash
# Remove the expired account
gog auth remove owner@company.com

# Re-add it (will open browser for re-auth)
gog auth add owner@company.com --services gmail,calendar,drive,contacts
```

### Response Style

- Lead with the **owner vs. agent** distinction — this resolves most confusion.
- Give commands first, explanation second.
- When asked "where is X stored?" → give the path, do not print the file contents.
- When asked for step-by-step → follow the Calendar Write Access section above.

### Heleni-Specific: Direct API Workaround (when gog CLI auth fails on server)

`gog auth login` requires a browser — doesn't work on a headless server. Use the pre-existing credentials instead:

- Credentials file: `/path/to/openclaw/.gog/credentials.json`
- Accounts: `agent` (<agent-email>), `owner` (<owner-email>)
- `~/.config/gws/credentials.json` (gog default) has a stale/broken token — ignore it

```bash
# Step 1: Refresh access token using owner credentials from .gog file
curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=<client_id_from_file>" \
  -d "client_secret=<client_secret_from_file>" \
  -d "refresh_token=<refresh_token_from_file>" \
  -d "grant_type=refresh_token"

# Step 2: Use access_token for direct API calls
# List events:
curl -s "https://www.googleapis.com/calendar/v3/calendars/netanelab%40monday.com/events?timeMin=<ISO>&timeMax=<ISO>&singleEvents=true&orderBy=startTime" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# List all calendars:
curl -s "https://www.googleapis.com/calendar/v3/users/me/calendarList" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Cost Tips

- **Very cheap:** This appendix is explanation only — minimal LLM tokens needed.
- **Small model OK:** Any model can explain these concepts and provide commands.
- **Avoid:** Do not re-explain the full orientation every time. Ask what specifically is confusing, then address only that.
