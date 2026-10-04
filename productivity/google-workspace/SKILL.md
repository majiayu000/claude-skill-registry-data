---
name: google-workspace
description: Interact with Google Workspace — Gmail, Drive, Calendar, Sheets, Docs, Tasks, Chat, and cross-service workflows. Read emails, manage files, check schedule, send messages, and automate productivity tasks.
allowed-tools: Bash, Read, Write
---

# Google Workspace

Manage Gmail, Drive, Calendar, Sheets, Docs, Tasks, and Chat via the `gws` CLI.

## Prerequisites

The `gws` CLI must be authenticated. Check with:

```bash
gws auth status
```

If `auth_method` is `"none"`, the user needs to set up OAuth credentials first:

1. Create a Desktop OAuth client at https://console.cloud.google.com/apis/credentials
2. Save the JSON to `~/.config/gws/client_secret.json`
3. Run `gws auth login`

**Do not proceed with any commands until auth is confirmed.** If auth fails, tell the user what's missing.

## Quick Start

```bash
# Check today's schedule
gws calendar +agenda --today

# See unread emails
gws gmail +triage

# List recent Drive files
gws drive files list --params '{"pageSize": 10}'

# Today's standup (meetings + tasks)
gws workflow +standup-report
```

## Gmail

### Read & Triage

```bash
# Unread inbox summary (sender, subject, date)
gws gmail +triage
gws gmail +triage --max 10
gws gmail +triage --query 'from:someone@example.com'
gws gmail +triage --query 'subject:invoice is:unread'
gws gmail +triage --format table

# Read a specific message (get ID from +triage output)
gws gmail +read --id MESSAGE_ID
gws gmail +read --id MESSAGE_ID --headers
gws gmail +read --id MESSAGE_ID --format json
```

### Send & Reply

```bash
# Send email
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi Alice!'
gws gmail +send --to alice@example.com --subject 'Report' --body 'See attached' -a report.pdf
gws gmail +send --to team@example.com --subject 'Update' --body '<b>Bold</b> update' --html

# Save as draft instead of sending
gws gmail +send --to alice@example.com --subject 'Draft' --body 'WIP' --draft

# Reply (auto-threads)
gws gmail +reply --message-id MSG_ID --body 'Thanks, got it!'
gws gmail +reply --message-id MSG_ID --body 'Adding Carol' --cc carol@example.com

# Reply all
gws gmail +reply-all --message-id MSG_ID --body 'Sounds good to me'

# Forward
gws gmail +forward --message-id MSG_ID --to dave@example.com
gws gmail +forward --message-id MSG_ID --to dave@example.com --body 'FYI see below'
```

### Search (Advanced)

```bash
# Gmail search queries via +triage --query
gws gmail +triage --query 'has:attachment larger:5M'
gws gmail +triage --query 'after:2026/03/01 before:2026/04/01'
gws gmail +triage --query 'label:important is:unread'

# Raw API for more control
gws gmail users messages list --params '{"userId":"me","q":"from:ceo@company.com","maxResults":5}'
```

### Watch for New Emails

```bash
# Stream new emails as NDJSON (requires GCP project with Pub/Sub)
gws gmail +watch --project PROJECT_ID --label-ids INBOX --poll-interval 10
gws gmail +watch --project PROJECT_ID --once  # single pull
```

## Calendar

```bash
# View schedule
gws calendar +agenda               # upcoming events
gws calendar +agenda --today        # today only
gws calendar +agenda --tomorrow     # tomorrow
gws calendar +agenda --week         # this week
gws calendar +agenda --days 3       # next 3 days
gws calendar +agenda --format table

# Create event
gws calendar +insert \
  --summary 'Team Sync' \
  --start '2026-04-01T10:00:00+02:00' \
  --end '2026-04-01T10:30:00+02:00' \
  --attendee alice@example.com \
  --attendee bob@example.com \
  --meet  # adds Google Meet link

# Check free/busy
gws calendar freebusy query --json '{
  "timeMin": "2026-04-01T00:00:00Z",
  "timeMax": "2026-04-02T00:00:00Z",
  "items": [{"id": "primary"}]
}'
```

## Drive

```bash
# List files
gws drive files list --params '{"pageSize": 10}'
gws drive files list --params '{"pageSize": 10, "q": "mimeType=\"application/pdf\""}'
gws drive files list --params '{"q": "name contains \"report\""}'
gws drive files list --params '{"q": "modifiedTime > \"2026-03-01T00:00:00\""}'

# Search in shared drives
gws drive files list --params '{"q": "name contains \"budget\"", "includeItemsFromAllDrives": true, "supportsAllDrives": true}'

# Get file metadata
gws drive files get --params '{"fileId": "FILE_ID"}'

# Download file
gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' --output ./downloaded-file.pdf

# Export Google Doc as PDF
gws drive files export --params '{"fileId": "DOC_ID", "mimeType": "application/pdf"}' --output ./doc.pdf

# Upload file
gws drive +upload ./report.pdf
gws drive +upload ./data.csv --parent FOLDER_ID --name 'Q1 Sales Data.csv'

# Create folder
gws drive files create --json '{"name": "Project Files", "mimeType": "application/vnd.google-apps.folder"}'

# Share file
gws drive permissions create --params '{"fileId": "FILE_ID"}' --json '{
  "role": "reader",
  "type": "user",
  "emailAddress": "alice@example.com"
}'
```

## Sheets

```bash
# Read spreadsheet data
gws sheets +read --spreadsheet SHEET_ID --range 'Sheet1!A1:D10'
gws sheets +read --spreadsheet SHEET_ID --range 'Sheet1'  # entire sheet

# Append rows
gws sheets +append --spreadsheet SHEET_ID --values 'Alice,100,true'
gws sheets +append --spreadsheet SHEET_ID --json-values '[["Alice",100],["Bob",200]]'

# Get spreadsheet metadata
gws sheets spreadsheets get --params '{"spreadsheetId": "SHEET_ID"}'
```

## Docs

```bash
# Read document
gws docs documents get --params '{"documentId": "DOC_ID"}'

# Append text
gws docs +write --document DOC_ID --text 'Meeting notes from today...'
```

## Tasks

```bash
# List task lists
gws tasks tasklists list

# List tasks in default list
gws tasks tasks list --params '{"tasklist": "@default"}'

# Create a task
gws tasks tasks insert --params '{"tasklist": "@default"}' --json '{
  "title": "Review Q1 report",
  "notes": "Check figures before Friday",
  "due": "2026-04-04T00:00:00Z"
}'

# Complete a task
gws tasks tasks patch --params '{"tasklist": "@default", "task": "TASK_ID"}' --json '{"status": "completed"}'
```

## Chat (Google Chat)

```bash
# List spaces
gws chat spaces list

# Send message to a space
gws chat +send --space spaces/SPACE_ID --text 'Hello team!'

# List messages in a space
gws chat spaces messages list --params '{"parent": "spaces/SPACE_ID"}'
```

## Cross-Service Workflows

```bash
# Morning standup: today's meetings + open tasks
gws workflow +standup-report

# Prepare for next meeting: agenda, attendees, linked docs
gws workflow +meeting-prep

# Weekly digest: this week's meetings + unread count
gws workflow +weekly-digest

# Convert email to task
gws workflow +email-to-task --message-id MSG_ID

# Announce a Drive file in Chat
gws workflow +file-announce --file-id FILE_ID --space spaces/SPACE_ID --message 'New report ready!'
```

## Output Formats

All commands support `--format`:

```bash
gws gmail +triage --format table   # human-readable table
gws gmail +triage --format json    # structured JSON (default)
gws gmail +triage --format csv     # CSV for spreadsheets
gws gmail +triage --format yaml    # YAML
```

**For programmatic use**, pipe JSON through `jq`:

```bash
gws gmail +triage --format json | jq '.[].subject'
gws drive files list --params '{"pageSize":5}' | jq '.files[].name'
gws calendar +agenda --today --format json | jq '.[].summary'
```

## Pagination

For large result sets:

```bash
# Auto-paginate (NDJSON, one JSON per page)
gws drive files list --params '{"pageSize": 100}' --page-all --page-limit 5

# With delay between pages (rate limiting)
gws gmail users messages list --params '{"userId":"me","maxResults":100}' --page-all --page-delay 200
```

## Schema Introspection

Discover API parameters for any endpoint:

```bash
gws schema drive.files.list
gws schema gmail.users.messages.get
gws schema calendar.events.insert --resolve-refs
```

## Important Notes

- **Read-only helpers** (+triage, +agenda, +read, +standup-report, +weekly-digest, +meeting-prep) never modify data
- **Write helpers** (+send, +reply, +forward, +insert, +append, +write, +email-to-task, +file-announce) create or modify data -- always confirm with user before executing
- **--dry-run** flag validates without sending -- use when uncertain
- **--draft** flag (Gmail) saves as draft instead of sending -- safer for review
- **userId is always "me"** for Gmail raw API calls
- **File IDs** can be extracted from Google URLs: `https://docs.google.com/document/d/{FILE_ID}/edit`
- All timestamps use **RFC 3339 / ISO 8601** format

## When to Use

- **Email management**: Triage inbox, read/reply/forward messages, draft responses
- **Schedule management**: Check agenda, create events, prep for meetings
- **File operations**: Search Drive, upload/download files, share with collaborators
- **Data entry**: Read/write spreadsheets, append to docs
- **Task management**: Create tasks from emails, track to-dos
- **Team communication**: Send Chat messages, announce files
- **Daily workflows**: Standup reports, weekly digests, meeting prep

## Troubleshooting

### Auth Error (exit code 2)
```bash
gws auth status  # check current state
gws auth login   # re-authenticate
```

### API Not Enabled
If you get a "API has not been enabled" error, enable it:
```bash
gcloud services enable gmail.googleapis.com --project=PROJECT_ID
gcloud services enable drive.googleapis.com --project=PROJECT_ID
gcloud services enable calendar-json.googleapis.com --project=PROJECT_ID
gcloud services enable sheets.googleapis.com --project=PROJECT_ID
gcloud services enable docs.googleapis.com --project=PROJECT_ID
gcloud services enable tasks.googleapis.com --project=PROJECT_ID
gcloud services enable chat.googleapis.com --project=PROJECT_ID
```

### Scope Issues
If commands fail with permission errors, re-login with broader scopes. The CLI requests scopes automatically based on the service used.

### Discovery Errors (exit code 4)
Transient -- retry the command. The CLI fetches API schemas from Google's Discovery Service on first use of each service.
