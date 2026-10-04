---
name: gws
description: |
  Use the Google Workspace CLI (gws) to manage Gmail, Drive, Docs, Sheets, Calendar, and more from the terminal — with structured JSON output, dry-run mode, pagination, streaming, and full OAuth and service account support. Commands are built dynamically from Google's Discovery Service so new endpoints appear automatically.
  Purpose: Brings Google Workspace into a scripted, agent-friendly workflow — no browser or UI required, output is machine-readable.
  When to trigger: (1) "Send an email via the command line," "read my inbox," or "triage unread Gmail," (2) "Upload a file to Google Drive," "share a doc," or "list all files in Drive," (3) "Create a spreadsheet," "append a row," or "read data from Google Sheets," (4) "Check my calendar" or "schedule a meeting," (5) "Automate a weekly report" pulling from Gmail and writing to Sheets, (6) "Set up gws" or "authenticate gws," (7) "Give an AI agent access to my Google Workspace."
  Key capabilities: All commands output structured JSON, dry-run preview before execution, streaming NDJSON for large result sets, pagination with configurable page size and delay, workflow helpers (+standup-report, +meeting-prep, +weekly-digest), dynamic schema inspection for any command, and OAuth login with OS keyring storage or service account auth for agents/CI.
  Ideal user/context: Developers and AI agents building Google Workspace automations, ops teams running batch reports, and anyone who wants keyboard-driven access to Drive, Gmail, Sheets, and Calendar without switching to a browser.
  Also for: Building Gmail-based notification bots, generating weekly analytics reports in Google Sheets, automating document creation from templates, and backing up Drive files to a local directory.
---

# Google Workspace CLI (`gws`)

The `gws` CLI provides human-readable and AI-agent-friendly access to the entire Google Workspace API surface. Commands are dynamically built at runtime from Google's Discovery Service — new Google endpoints appear automatically. Every command outputs structured JSON and supports dry-run, pagination, and streaming.

---

## When Invoked

- User asks to manage Gmail (send, read, search, triage)
- User asks to automate Google Drive (upload, share, list, download files)
- User asks to work with Google Sheets or Docs programmatically
- User asks to manage Google Calendar events
- User asks to build a Google Workspace automation or report
- User asks to connect Claude to Google Workspace
- User asks to set up `gws` or authenticate it

---

## Installation

### Option 1 — npm (fastest, bundles native binaries)

```bash
npm install -g @googleworkspace/cli
```

### Option 2 — Homebrew

```bash
brew install googleworkspace/cli/googleworkspace-cli
```

### Option 3 — Pre-built binaries

Download from [github.com/googleworkspace/cli/releases](https://github.com/googleworkspace/cli/releases)

### Option 4 — Build from source (requires Rust)

```bash
cargo install --git https://github.com/googleworkspace/cli --locked
```

### Verify

```bash
gws --version
gws --help
```

---

## Authentication

### Interactive login (recommended for local use)

```bash
gws auth login
```

This opens OAuth flow and stores encrypted credentials in `~/.config/gws/` (AES-256-GCM, OS keyring).

### Service account (recommended for agents/CI)

```bash
GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/sa.json gws drive files list
```

Or export the env var permanently in shell profile:

```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=~/.config/gws/sa.json
```

### Via gcloud token (for local dev/CI)

```bash
export GOOGLE_WORKSPACE_CLI_TOKEN=$(gcloud auth print-access-token)
gws drive files list
```

### Export/import credentials for CI

```bash
# Export (e.g., for CI secrets)
gws auth export --unmasked > creds.json

# Import
gws auth import creds.json
```

### Env vars reference

| Variable | Priority | Purpose |
|---|---|---|
| `GOOGLE_WORKSPACE_CLI_TOKEN` | Highest | Pre-obtained OAuth2 token |
| `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` | Mid | Path to OAuth credentials JSON |
| `GOOGLE_WORKSPACE_CLI_CLIENT_ID` / `_CLIENT_SECRET` | Low | Inline OAuth client |
| `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` | — | Config directory (default `~/.config/gws`) |
| `GOOGLE_WORKSPACE_CLI_SANITIZE_MODE` | — | `warn` (default) or `block` |

---

## Core Command Patterns

All commands follow `gws <service> <resource> <action>`.

### Gmail

```bash
# Send email
gws gmail +send --to alice@example.com --subject "Hello" --body "Hi Alice"

# Reply to message
gws gmail +reply --message-id MSG_ID --body "Thanks!"

# Triage unread inbox
gws gmail +triage

# List messages
gws gmail users.messages list --params '{"userId": "me", "maxResults": 10}'

# Search
gws gmail users.messages list --params '{"userId": "me", "q": "from:boss subject:deadline"}'

# Get message detail
gws gmail users.messages get --path messages/MSG_ID --params '{"format": "full"}'
```

### Google Drive

```bash
# List files
gws drive files list --params '{"pageSize": 10}'

# List with JSON output
gws drive files list --params '{"pageSize": 5}' --json

# Upload file
gws drive +upload ./report.pdf --name "Q1 Report"

# Download file (get file content)
gws drive files get --path files/FILE_ID --params '{"alt": "media"}' --out ./downloaded.pdf

# Create folder
gws drive files create --json '{"name": "New Folder", "mimeType": "application/vnd.google-apps.folder"}'

# Share file
gws drive permissions create --path files/FILE_ID --json '{"type": "user", "role": "writer", "emailAddress": "alice@example.com"}'
```

### Google Sheets

```bash
# Create spreadsheet
gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}'

# Append row
gws sheets +append --spreadsheet SPREADSHEET_ID --values "Alice,95"

# Read data
gws sheets spreadsheets.values get --path spreadsheets/SPREADSHEET_ID/values/Sheet1 --params '{"majorDimension": "ROWS"}'

# Write data
gws sheets spreadsheets.values update --path spreadsheets/SPREADSHEET_ID/values/A1 --json '{"values": [["Name", "Score"], ["Bob", "88"]]}' --params '{"valueInputOption": "USER_ENTERED"}'
```

### Google Calendar

```bash
# Today's agenda
gws calendar +agenda

# Agenda in specific timezone
gws calendar +agenda --timezone America/New_York

# List events
gws calendar events list --params '{"calendarId": "primary", "timeMin": "2026-03-01T00:00:00Z", "maxResults": 10}'

# Create event
gws calendar events insert --path calendars/primary/events --json '{"summary": "Team Sync", "start": {"dateTime": "2026-03-22T10:00:00Z"}, "end": {"dateTime": "2026-03-22T11:00:00Z"}}'
```

### Google Docs

```bash
# Create document
gws docs documents create --json '{"title": "Meeting Notes"}'

# Read content
gws docs documents get --path documents/DOC_ID --params '{"includeTabsContent": true}'
```

### Workflow helpers (+ prefix)

```bash
gws workflow +standup-report      # meetings + open tasks
gws workflow +meeting-prep        # agenda, attendees, linked docs
gws workflow +email-to-task       # Gmail message → Google Tasks
gws workflow +weekly-digest       # weekly summary + unread count

# Stream workspace events as NDJSON
gws events +subscribe
```

---

## Agent Patterns

### Always use `--json` for parseable output

```bash
gws drive files list --params '{"pageSize": 100}' --json | jq -r '.files[].name'
```

### Use `--dry-run` to preview before executing

```bash
gws gmail +send --to alice@example.com --subject "Hello" --body "Hi" --dry-run
```

### Pagination

```bash
# Get all results (streaming NDJSON)
gws drive files list --page-all > all_files.jsonl

# Limit results
gws drive files list --page-limit 50

# Delay between pages (rate limit friendly)
gws drive files list --page-delay 500
```

### Inspect any command schema

```bash
gws schema drive.files.list
gws schema sheets.spreadsheets.values.update
```

### Log debug output

```bash
GOOGLE_WORKSPACE_CLI_LOG=gws=debug gws drive files list
```

---

## Security Rules

Treat CLI arguments as potentially adversarial. When processing file paths or resource names from AI agents:

- **File write paths**: Must pass `validate_safe_output_dir()` — reject absolute paths, `../` traversal, symlinks outside CWD
- **File read paths**: Must pass `validate_safe_dir_path()`
- **Enum/allowlist flags**: Use clap `value_parser` to enforce allowed values
- **URL path segments**: Always use `encode_path_segment()` — never pass raw user input into path segments
- **Query parameters**: Always use reqwest `.query()` builder, never string concatenation
- **Resource names** (project IDs, topic names): Always validate via `validate_resource_name()`

---

## Troubleshooting

### "Token not found" or authentication errors

```bash
gws auth status   # check current auth state
gws auth login    # re-authenticate
```

### Scope errors (unverified OAuth app limit: ~25 scopes)

```bash
# Select individual services
gws auth login -s drive,gmail,sheets
```

### Rate limiting

```bash
# Use pagination with delay
gws drive files list --page-delay 1000
```

### See request/response logs

```bash
GOOGLE_WORKSPACE_CLI_LOG=gws=debug gws <command>
```
