---
name: google-calendar
description: Google Calendar API — list events, create/update/delete appointments, check availability. Direct OAuth via service account, no third-party proxy.
metadata:
  {
    "nyxclaw":
      {
        "emoji": "📅",
        "requires":
          { "bins": ["node"], "env": ["GOOGLE_SERVICE_ACCOUNT_JSON", "GOOGLE_CALENDAR_ID"] },
        "primaryEnv": "GOOGLE_SERVICE_ACCOUNT_JSON",
      },
  }
---

# Google Calendar

Manage Google Calendar events directly via Google Calendar API. All scripts output JSON.

## Setup

### 1. Create a Google Cloud project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the **Google Calendar API**:
   - Go to **APIs & Services > Library**
   - Search "Google Calendar API" and click **Enable**

### 2. Create a service account

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > Service account**
3. Name it (e.g. `nyxclaw-calendar`) and click **Create**
4. Skip the optional permissions steps, click **Done**
5. Click on the created service account
6. Go to **Keys > Add Key > Create new key > JSON**
7. Download the JSON file — this is your credential

### 3. Share your calendar with the service account

1. Open [Google Calendar](https://calendar.google.com/)
2. Click the three dots next to your calendar > **Settings and sharing**
3. Under **Share with specific people**, click **Add people**
4. Paste the service account email (from the JSON file, field `client_email` — looks like `name@project.iam.gserviceaccount.com`)
5. Set permission to **Make changes to events**
6. Click **Send**

### 4. Configure in NyxClaw

Tell Nyx:

> "set env GOOGLE_SERVICE_ACCOUNT_JSON to (paste the entire JSON content)"
> "set env GOOGLE_CALENDAR_ID to (your calendar ID from step 3)"

The `GOOGLE_CALENDAR_ID` is the default calendar for all operations. Find it in Google Calendar > Settings > Integrate calendar. Format: `abc123...@group.calendar.google.com` (for custom calendars) or your email (for personal calendar).

If you already use `GOOGLE_SERVICE_ACCOUNT_JSON` for GSC Analytics, the same service account works — just share the calendar with it.

### 5. (Optional) Domain-wide delegation

For Google Workspace accounts, you can impersonate users:

1. Go to **Admin console > Security > API Controls > Domain-wide delegation**
2. Add the service account client ID with scope `https://www.googleapis.com/auth/calendar`
3. Set `GOOGLE_CALENDAR_USER` env var to the email to impersonate

## List Events

```bash
node {baseDir}/scripts/events.mjs list
node {baseDir}/scripts/events.mjs list --days 14 --limit 50
node {baseDir}/scripts/events.mjs list --calendar "other@gmail.com" --days 30
```

Options:

- `--days <n>`: Look-ahead window in days (default: 7)
- `--limit <n>`: Max events to return (default: 25)
- `--calendar <id>`: Calendar ID — must be the full ID, not the display name (default: primary, which is the service account's own calendar). Use `calendars.mjs` to discover IDs

## Get Event

```bash
node {baseDir}/scripts/events.mjs get <eventId>
```

## Create Event

```bash
node {baseDir}/scripts/events.mjs create "Dental Appointment" "2026-03-10T09:00:00" "2026-03-10T10:00:00"
node {baseDir}/scripts/events.mjs create "Team Sync" "2026-03-10T15:00:00" "2026-03-10T16:00:00" --description "Weekly sync" --attendees "john@example.com,jane@example.com"
node {baseDir}/scripts/events.mjs create "Holiday" "2026-03-15" "2026-03-16"
```

Options:

- `--timezone <tz>`: Timezone (default: Europe/Madrid)
- `--description <text>`: Event description
- `--attendees <emails>`: Comma-separated list of attendee emails

## Quick Add (natural language)

```bash
node {baseDir}/scripts/events.mjs quickadd "Meeting with John tomorrow at 3pm"
```

## Update Event

```bash
node {baseDir}/scripts/events.mjs update <eventId> '{"summary":"New Title"}'
node {baseDir}/scripts/events.mjs update <eventId> '{"start":{"dateTime":"2026-03-10T10:00:00","timeZone":"Europe/Madrid"}}'
```

## Delete Event

```bash
node {baseDir}/scripts/events.mjs delete <eventId>
```

## List Calendars

```bash
node {baseDir}/scripts/calendars.mjs
```

## Check Availability (Free/Busy)

```bash
node {baseDir}/scripts/freebusy.mjs
node {baseDir}/scripts/freebusy.mjs --days 14
node {baseDir}/scripts/freebusy.mjs --calendar "other@gmail.com"
```

## Notes

- **Environment variables are auto-injected** — `GOOGLE_SERVICE_ACCOUNT_JSON`, `GOOGLE_CALENDAR_ID` and all `env.vars` from nyxclaw.json are available as `process.env.*` when scripts run. Do NOT verify them manually via CLI — just run the scripts directly.
- The default calendar is `GOOGLE_CALENDAR_ID` env var. Override per-command with `--calendar <id>`.
- The service account must be shared on the target calendar with "Make changes to events" permission.
- All scripts authenticate automatically via `auth.mjs`.
- Times in RFC3339 format (e.g. `2026-03-10T09:00:00`) or date-only for all-day events (`2026-03-10`).
- If you already have `GOOGLE_SERVICE_ACCOUNT_JSON` configured for gsc-analytics, the same key works — just share the calendar.
- **Calendar ID vs display name:** The `--calendar` flag requires the full calendar ID (e.g. `abc123...@group.calendar.google.com`), not the display name. Run `calendars.mjs` first to discover IDs.
