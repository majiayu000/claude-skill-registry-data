---
name: openclaw-email-orientation
description: Explain how email and Google Calendar work for OpenClaw agents, including the distinction between agent email and owner email, how gog and the Google Workspace skill are used, where related credentials/config live, and how to troubleshoot common setup or access issues. Use when someone asks how an OpenClaw agent accesses Gmail/Google Workspace/Calendar, where credentials are stored, how to use the agent inbox, how to give the agent write access to the owner's calendar, or how to guide another agent/user through the email or calendar setup model.
---

# OpenClaw Email & Calendar Orientation

## Minimum Model
Any model. This is an explanation and troubleshooting guide — no complex reasoning needed.

---

## The Core Concept (Read This First)

There are two separate accounts:

| | Account |
|---|---|
| **Owner** | The human's Google account (e.g. `owner@company.com`) |
| **Agent** | The PA's own Google account (e.g. `agent@agentdomain.com`) |

**These are separate.** Having an agent email does NOT automatically give access to the owner's email or calendar.

To access the owner's email/calendar:
1. **Owner must share** access with the agent email (explicit step).
2. **Agent must authenticate** using `gog` (explicit step).

If someone is confused → start with this distinction. It resolves most questions.

---

## Key Paths and Files

| File | Purpose |
|---|---|
| `~/.openclaw/.gog/credentials.json` | gog OAuth client credentials |
| `~/.openclaw/agents/main/agent/auth-profiles.json` | OpenClaw auth profiles |
| `~/.openclaw/workspace/skills/gog/SKILL.md` | gog usage reference |

**Security rule:** Never show the contents of these files in chat. Mentioning the path is fine; printing the content is not.

---

## Using gog

```bash
# One-time setup: load OAuth credentials
gog auth credentials /path/to/client_secret.json

# Add an account (opens browser for OAuth flow)
gog auth add owner@company.com --services gmail,calendar,drive,contacts,sheets,docs

# Verify the account was added
gog auth list

# Use the account in commands (always include GOG_ACCOUNT=...)
GOG_ACCOUNT=owner@company.com gog gmail search 'is:unread' --max 10
```

### Common Commands

```bash
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

---

## Calendar Write Access — Step by Step

The most common issue: the agent can read the calendar but not create events.

**Step 1 — Owner does this:**
1. Open [calendar.google.com](https://calendar.google.com).
2. Find the primary calendar → three-dot menu → Settings and sharing.
3. Click "+ Add people" → enter the agent email.
4. Set permission to **"Make changes to events"** (not "See all event details").
5. Click Send.

**Step 2 — Agent does this:**
```bash
# Authenticate with calendar scope
gog auth add owner@company.com --services calendar

# Test write access by creating a test event
GOG_ACCOUNT=owner@company.com gog calendar create primary \
  --summary "Test Event" \
  --start "2026-04-02T10:00:00Z" \
  --end "2026-04-02T11:00:00Z"
```

If the test event appears in the owner's calendar → success.

---

## Troubleshooting

Work through these checks in order:

1. **Clarify accounts:** Is the question about agent email or owner email?
2. **Check gog is installed:** Run `which gog` — if not found, check PATH.
3. **Check account was added:** Run `gog auth list` — does owner's account appear?
4. **Check write scope:** OAuth must include calendar write scope, not just read.
5. **Check keyring:** If gog asks for a password, local keyring may need to be configured.
6. **Check GOG_ACCOUNT:** All commands must include `GOG_ACCOUNT=owner@company.com`.
7. **Calendar write failures:** Was permission set to "Make changes to events" (not "See details")?

**If "Insufficient permissions" error:**
→ Owner shared calendar with read-only access. Redo Step 1 with the correct permission level.

**If "Token expired" error:**
```bash
# Remove the expired account
gog auth remove owner@company.com

# Re-add it (will open browser for re-auth)
gog auth add owner@company.com --services gmail,calendar,drive,contacts
```

---

## Response Style

- Lead with the **owner vs. agent** distinction — this resolves most confusion.
- Give commands first, explanation second.
- When asked "where is X stored?" → give the path, do not print the file contents.
- When asked for step-by-step → follow the Calendar Write Access section above.

---

## Heleni-specific: Direct API Workaround (when gog CLI auth fails on server)

`gog auth login` requires a browser — doesn't work on a headless server. Use the pre-existing credentials instead:

- Credentials file: `/path/to/openclaw/.gog/credentials.json`
- Accounts: `agent` (agent@example.com), `owner` (owner@company.com)
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

---

## Cost Tips

- **Very cheap:** This skill is explanation only — minimal LLM tokens needed.
- **Small model OK:** Any model can explain these concepts and provide commands.
- **Avoid:** Do not re-explain the full orientation every time. Ask what specifically is confusing, then address only that.
