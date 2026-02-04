---
name: skill-google-gmail-tool
description: Access Google Gmail, Calendar, Tasks, Drive APIs
---

# When to use
- Access Gmail messages, send emails, export to Obsidian
- Manage Google Calendar events and export schedules
- Work with Google Tasks and to-do lists
- Search, upload, download Google Drive files

# Google Gmail Tool Skill

## Purpose

The `google-gmail-tool` is a professional CLI that provides comprehensive access to Google services including Gmail, Calendar, Tasks, and Drive. It enables agent-friendly JSON output, human-readable text formats, multi-level verbosity logging, and seamless Obsidian integration.

## When to Use This Skill

**Use this skill when:**
- Reading or sending Gmail messages programmatically
- Managing calendar events and schedules
- Working with Google Tasks and to-do lists
- Searching, uploading, or downloading files from Google Drive
- Exporting Google data to Obsidian markdown notes
- Automating Google service workflows

**Do NOT use this skill for:**
- Direct Google API programming (this is a CLI wrapper)
- Google Workspace admin tasks (requires different APIs)
- Real-time synchronization (uses polling-based access)

## CLI Tool: google-gmail-tool

A CLI that provides access to Google services with OAuth2 authentication, supporting Gmail, Calendar, Tasks, and Drive operations.

### Installation

```bash
# Clone repository
git clone https://github.com/dnvriend/google-gmail-tool.git
cd google-gmail-tool

# Install globally with uv
uv tool install .

# Verify installation
google-gmail-tool --version
```

### Prerequisites

- **Python**: 3.14 or higher
- **OAuth Credentials**: Google Cloud Console OAuth 2.0 Client ID (Desktop application)
- **Environment Variables**:
  - `GOOGLE_GMAIL_TOOL_CREDENTIALS`: Path to credentials JSON file
  - `GOOGLE_GMAIL_TOOL_CREDENTIALS_JSON`: Full OAuth2 credentials as JSON string
  - `OBSIDIAN_ROOT`: Path to Obsidian vault (for export commands)

### Quick Start

```bash
# 1. Get OAuth credentials from Google Cloud Console
# Visit: https://console.cloud.google.com/apis/credentials

# 2. Set credentials environment variable
export GOOGLE_GMAIL_TOOL_CREDENTIALS=~/.config/google-gmail-tool/credentials.json

# 3. Verify authentication
google-gmail-tool auth check

# 4. List Gmail threads
google-gmail-tool mail list --today

# 5. List calendar events
google-gmail-tool calendar list --this-week
```

## Progressive Disclosure

<details>
<summary><strong>📧 Gmail Commands (Click to expand)</strong></summary>

### mail list - List Gmail messages or threads

List Gmail messages or threads with optional filtering, supporting full Gmail search syntax.

**Usage:**
```bash
google-gmail-tool mail list [OPTIONS]
```

**Options:**
- `--query "TEXT"`: Gmail search query (supports full Gmail search syntax)
- `--today`: Filter emails from today only
- `--max-results N` / `-n N`: Maximum results (default: 50, max: 500)
- `--format FORMAT` / `-f FORMAT`: Output format (json, text)
- `--text`: Shorthand for `--format text`
- `--message-mode`: List individual messages instead of threads
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Gmail Search Operators:**
- `is:unread`, `is:read`, `is:starred` - Message status
- `has:attachment`, `filename:pdf` - Attachments
- `from:email@example.com` - Sender
- `to:email@example.com` - Recipient
- `subject:keyword` - Subject line
- `after:YYYY/MM/DD`, `before:YYYY/MM/DD` - Date range
- `older_than:2d`, `newer_than:1m` - Relative dates
- `label:important`, `in:inbox` - Labels

**Examples:**
```bash
# List 50 most recent threads
google-gmail-tool mail list

# Find unread emails from today
google-gmail-tool mail list --today --query "is:unread"

# Search for specific sender
google-gmail-tool mail list --query "from:team@company.com" -n 10

# Find emails with attachments
google-gmail-tool mail list --query "has:attachment" --text

# Complex query
google-gmail-tool mail list \
    --query "from:john@example.com subject:report after:2025/01/01" \
    --message-mode
```

**Output (JSON):**
```json
[
  {
    "id": "19a90f13e3c7af52",
    "threadId": "19a90f13e3c7af52",
    "snippet": "Meeting notes from...",
    "from": "sender@example.com",
    "to": "recipient@example.com",
    "subject": "Meeting Notes",
    "date": "2025-11-20T10:30:00Z"
  }
]
```

---

### mail send - Send email via Gmail

Send emails via Gmail API with support for HTML, CC, BCC, and attachments.

**Usage:**
```bash
google-gmail-tool mail send [OPTIONS]
```

**Options:**
- `--to EMAIL`: Recipient email (required)
- `--subject TEXT`: Email subject (required)
- `--body TEXT`: Email body (required)
- `--from EMAIL`: Sender email (optional, uses default)
- `--cc EMAIL`: CC recipients (comma-separated)
- `--bcc EMAIL`: BCC recipients (comma-separated)
- `--html`: Send as HTML instead of plain text
- `--dry-run`: Preview email without sending
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Send plain text email
google-gmail-tool mail send \
    --to "user@example.com" \
    --subject "Meeting Notes" \
    --body "Here are the notes from today's meeting..."

# Send HTML email with CC
google-gmail-tool mail send \
    --to "user@example.com" \
    --cc "team@example.com" \
    --subject "Weekly Report" \
    --body "<h1>Report</h1><p>Details...</p>" \
    --html

# Preview without sending
google-gmail-tool mail send \
    --to "user@example.com" \
    --subject "Test" \
    --body "Test email" \
    --dry-run
```

---

### mail get - Get email message details

Retrieve detailed information about a specific Gmail message.

**Usage:**
```bash
google-gmail-tool mail get MESSAGE_ID [OPTIONS]
```

**Options:**
- `MESSAGE_ID`: Gmail message ID (required)
- `--format FORMAT` / `-f FORMAT`: Output format (json, text)
- `--include-body`: Include full message body
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Get message metadata
google-gmail-tool mail get 19a90f13e3c7af52

# Get message with full body
google-gmail-tool mail get 19a90f13e3c7af52 --include-body

# Text format output
google-gmail-tool mail get 19a90f13e3c7af52 --include-body --format text
```

---

### mail export-obsidian - Export Gmail to Obsidian

Export Gmail threads to Obsidian markdown notes with attachments.

**Usage:**
```bash
google-gmail-tool mail export-obsidian [OPTIONS]
```

**Options:**
- `--query "TEXT"`: Gmail search query
- `--today`: Export emails from today only
- `--max-results N` / `-n N`: Maximum threads to export
- `--obsidian-root PATH`: Obsidian vault root path (or use `OBSIDIAN_ROOT` env var)
- `--download-attachments`: Download email attachments (default)
- `--no-download-attachments`: Skip downloading attachments
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Obsidian Structure:**
```
$OBSIDIAN_ROOT/emails/<timestamp>-<sender>-<subject>/
├── thread.md                 # Thread with all messages
└── attachments/              # Downloaded attachments
    ├── document.pdf
    └── image.png
```

**Examples:**
```bash
# Export today's emails
google-gmail-tool mail export-obsidian --today

# Export specific threads
google-gmail-tool mail export-obsidian --query "from:important@example.com"

# Export without attachments
google-gmail-tool mail export-obsidian \
    --query "subject:report" \
    --no-download-attachments
```

</details>

<details>
<summary><strong>📅 Calendar Commands (Click to expand)</strong></summary>

### calendar list - List calendar events

List calendar events with time range and query filtering.

**Usage:**
```bash
google-gmail-tool calendar list [OPTIONS]
```

**Options:**
- `--today`: Events for today
- `--tomorrow`: Events for tomorrow
- `--this-week`: Events this week (Monday-Sunday, default)
- `--next-week`: Events next week
- `--days N`: Events for next N days
- `--date YYYY-MM-DD`: Events for specific date
- `--range-start YYYY-MM-DD`: Start of custom range
- `--range-end YYYY-MM-DD`: End of custom range
- `--query "TEXT"`: Free-text search (title, description, location)
- `--max-results N` / `-n N`: Maximum results (default: 100)
- `--format FORMAT` / `-f FORMAT`: Output format (json, text)
- `--text`: Shorthand for `--format text`
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# List this week's events (default)
google-gmail-tool calendar list

# Today's events
google-gmail-tool calendar list --today

# Next 7 days
google-gmail-tool calendar list --days 7

# Search for meetings
google-gmail-tool calendar list --query "team meeting"

# Custom date range
google-gmail-tool calendar list \
    --range-start 2025-11-20 \
    --range-end 2025-11-27
```

**Output (JSON):**
```json
[
  {
    "id": "event123",
    "summary": "Team Meeting",
    "start": "2025-11-20T10:00:00Z",
    "end": "2025-11-20T11:00:00Z",
    "location": "Conference Room A",
    "attendees": ["user1@example.com", "user2@example.com"]
  }
]
```

---

### calendar create - Create calendar event

Create a new calendar event with optional attendees and Google Meet.

**Usage:**
```bash
google-gmail-tool calendar create [OPTIONS]
```

**Options:**
- `--title TEXT` / `-t TEXT`: Event title (required)
- `--start DATETIME`: Start datetime (YYYY-MM-DD HH:MM)
- `--end DATETIME`: End datetime (YYYY-MM-DD HH:MM)
- `--date YYYY-MM-DD`: Date for all-day event
- `--all-day`: Create all-day event (requires `--date`)
- `--location TEXT` / `-l TEXT`: Event location
- `--description TEXT` / `-d TEXT`: Event description
- `--attendees EMAILS` / `-a EMAILS`: Comma-separated attendee emails
- `--add-meet`: Add Google Meet video conferencing
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Create simple event
google-gmail-tool calendar create \
    --title "Team Meeting" \
    --start "2025-11-20 10:00" \
    --end "2025-11-20 11:00"

# Create event with Google Meet
google-gmail-tool calendar create \
    --title "Remote Standup" \
    --start "2025-11-21 09:00" \
    --end "2025-11-21 09:30" \
    --add-meet

# Create all-day event
google-gmail-tool calendar create \
    --title "Conference" \
    --date "2025-11-25" \
    --all-day

# Create event with attendees
google-gmail-tool calendar create \
    --title "Project Review" \
    --start "2025-11-22 14:00" \
    --end "2025-11-22 15:00" \
    --location "Room 301" \
    --attendees "user1@example.com,user2@example.com"
```

---

### calendar export-obsidian - Export calendar to Obsidian

Export calendar events to Obsidian daily notes as checklist items.

**Usage:**
```bash
google-gmail-tool calendar export-obsidian [OPTIONS]
```

**Options:**
- `--today`: Export today's events
- `--this-week`: Export this week's events (default)
- `--date YYYY-MM-DD`: Export specific date
- `--range-start YYYY-MM-DD`: Start of custom range
- `--range-end YYYY-MM-DD`: End of custom range
- `--query "TEXT"`: Filter events by search query
- `--obsidian-root PATH`: Obsidian vault root path
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Smart Merge Logic:**
- Preserves checked-off items
- Updates event times if changed
- Removes cancelled events
- Adds new events

**Examples:**
```bash
# Export today's schedule
google-gmail-tool calendar export-obsidian --today

# Export this week to daily notes
google-gmail-tool calendar export-obsidian --this-week

# Export filtered events
google-gmail-tool calendar export-obsidian --query "meeting"
```

</details>

<details>
<summary><strong>✅ Task Commands (Click to expand)</strong></summary>

### task list - List Google Tasks

List Google Tasks with status and date filtering.

**Usage:**
```bash
google-gmail-tool task list [OPTIONS]
```

**Options:**
- `--completed`: Show only completed tasks
- `--incomplete`: Show only incomplete tasks (default)
- `--show-all`: Show both completed and incomplete
- `--today`: Tasks due today
- `--overdue`: Tasks past due date
- `--max-results N` / `-n N`: Maximum results (default: 100)
- `--format FORMAT` / `-f FORMAT`: Output format (json, text)
- `--text`: Shorthand for `--format text`
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# List incomplete tasks (default)
google-gmail-tool task list

# Show all tasks including completed
google-gmail-tool task list --show-all

# Tasks due today
google-gmail-tool task list --today

# Overdue tasks
google-gmail-tool task list --overdue

# First 10 incomplete tasks
google-gmail-tool task list --incomplete -n 10
```

**Output (JSON):**
```json
[
  {
    "id": "task123",
    "title": "Review PR #456",
    "notes": "Check code quality and tests",
    "due": "2025-11-20",
    "status": "needsAction",
    "updated": "2025-11-19T15:30:00Z"
  }
]
```

---

### task create - Create new task

Create a new Google Task with optional notes and due date.

**Usage:**
```bash
google-gmail-tool task create [OPTIONS]
```

**Options:**
- `--title TEXT` / `-t TEXT`: Task title (required)
- `--notes TEXT` / `-n TEXT`: Task notes/description
- `--due YYYY-MM-DD` / `-d YYYY-MM-DD`: Due date
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Create minimal task
google-gmail-tool task create --title "Review PR #123"

# Create task with due date
google-gmail-tool task create \
    --title "Submit report" \
    --due "2025-11-25"

# Create task with notes
google-gmail-tool task create \
    --title "Team meeting prep" \
    --notes "Prepare slides and agenda" \
    --due "2025-11-20"
```

---

### task complete - Mark tasks as completed

Mark one or more tasks as completed.

**Usage:**
```bash
google-gmail-tool task complete TASK_ID [TASK_ID...] [OPTIONS]
```

**Options:**
- `TASK_ID`: One or more task IDs (space-separated)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Complete single task
google-gmail-tool task complete abc123xyz

# Complete multiple tasks
google-gmail-tool task complete abc123 def456 ghi789

# Pipeline with jq
TASK_ID=$(google-gmail-tool task list -n 1 | jq -r '.[0].id')
google-gmail-tool task complete "$TASK_ID"
```

---

### task export-obsidian - Export tasks to Obsidian

Export Google Tasks to Obsidian daily notes as checklist items.

**Usage:**
```bash
google-gmail-tool task export-obsidian [OPTIONS]
```

**Options:**
- `--today`: Export tasks due today
- `--this-week`: Export tasks due this week
- `--date YYYY-MM-DD`: Export tasks for specific date
- `--range-start YYYY-MM-DD`: Start of custom range
- `--range-end YYYY-MM-DD`: End of custom range
- `--obsidian-root PATH`: Obsidian vault root path
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Smart Merge Logic:**
- Preserves checked-off items
- Updates task details if changed
- Removes completed tasks (optional)
- Adds new tasks

**Examples:**
```bash
# Export today's tasks
google-gmail-tool task export-obsidian --today

# Export this week's tasks
google-gmail-tool task export-obsidian --this-week

# Export custom date range
google-gmail-tool task export-obsidian \
    --range-start 2025-11-20 \
    --range-end 2025-11-27
```

</details>

<details>
<summary><strong>📁 Drive Commands (Click to expand)</strong></summary>

### drive list - List Drive files

List files in Google Drive with filtering and sorting.

**Usage:**
```bash
google-gmail-tool drive list [OPTIONS]
```

**Options:**
- `--query "TEXT"`: Drive query string
- `--max-results N` / `-n N`: Maximum results (default: 50)
- `--folder FOLDER_ID`: List files in specific folder
- `--order-by FIELD`: Sort by field (name, createdTime, modifiedTime desc)
- `--format FORMAT` / `-f FORMAT`: Output format (json, text)
- `--text`: Shorthand for `--format text`
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# List 50 most recent files
google-gmail-tool drive list

# List files in folder
google-gmail-tool drive list --folder 0ALlMmd1yT2TNUk9PVA

# Sort by name
google-gmail-tool drive list --order-by name -n 20
```

**Output (JSON):**
```json
[
  {
    "id": "1abc...xyz",
    "name": "document.pdf",
    "mimeType": "application/pdf",
    "size": "1048576",
    "modifiedTime": "2025-11-20T10:30:00Z",
    "webViewLink": "https://drive.google.com/..."
  }
]
```

---

### drive search - Search Drive files

Search for files and folders with common filters.

**Usage:**
```bash
google-gmail-tool drive search [OPTIONS]
```

**Options:**
- `--name "TEXT"`: Search by file/folder name
- `--type TYPE`: Filter by type (document, spreadsheet, presentation, folder, pdf, image)
- `--owner OWNER`: Filter by owner (me, others, anyone)
- `--shared`: Show only shared files
- `--max-results N` / `-n N`: Maximum results (default: 50)
- `--format FORMAT` / `-f FORMAT`: Output format (json, text)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Search by name
google-gmail-tool drive search --name "report"

# Find PDFs I own
google-gmail-tool drive search --type pdf --owner me

# Find shared spreadsheets
google-gmail-tool drive search --type spreadsheet --shared

# Complex search
google-gmail-tool drive search \
    --name "2025" \
    --type document \
    --owner me \
    -n 100
```

---

### drive upload-file - Upload file to Drive

Upload a local file to Google Drive.

**Usage:**
```bash
google-gmail-tool drive upload-file LOCAL_PATH [PARENT_ID] [OPTIONS]
```

**Options:**
- `LOCAL_PATH`: Local file path (required)
- `PARENT_ID`: Parent folder ID (optional, defaults to My Drive root)
- `--name NAME`: Drive file name (defaults to local filename)
- `--description TEXT`: File description
- `--mime-type TYPE`: Override MIME type
- `--force` / `-f`: Skip duplicate check
- `--format FORMAT`: Output format (json, text)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Upload to My Drive root
google-gmail-tool drive upload-file document.pdf

# Upload to specific folder
google-gmail-tool drive upload-file report.pdf 0ALlMmd1yT2TNUk9PVA

# Upload with custom name
google-gmail-tool drive upload-file data.csv \
    --name "Sales Report 2025.csv"
```

---

### drive download - Download file from Drive

Download a file from Google Drive to local filesystem.

**Usage:**
```bash
google-gmail-tool drive download FILE_ID OUTPUT_PATH [OPTIONS]
```

**Options:**
- `FILE_ID`: Drive file ID (required)
- `OUTPUT_PATH`: Local output path (required)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Download file
google-gmail-tool drive download 1abc...xyz document.pdf

# Download to specific directory
google-gmail-tool drive download 1abc...xyz ~/Downloads/report.pdf
```

</details>

<details>
<summary><strong>🔐 Authentication Commands (Click to expand)</strong></summary>

### auth check - Verify credentials

Verify Google OAuth credentials and API access.

**Usage:**
```bash
google-gmail-tool auth check [-v|-vv|-vvv]
```

**Environment Variables:**
- `GOOGLE_GMAIL_TOOL_CREDENTIALS_JSON`: Full OAuth2 credentials as JSON string
- `GOOGLE_GMAIL_TOOL_CREDENTIALS`: Path to OAuth2 credentials JSON file

**Validates:**
- OAuth credential format and validity
- Access token refresh capability
- Gmail API access
- Calendar API access
- Tasks API access
- Drive API access

**Examples:**
```bash
# Check authentication
google-gmail-tool auth check

# Check with debug output
google-gmail-tool auth check -vv
```

**Output:**
```
🔐 Checking Google OAuth credentials...
✓ Credentials loaded successfully
✓ Gmail API access granted
✓ Calendar API access granted
✓ Tasks API access granted
✓ Drive API access granted
```

---

### auth login - Complete OAuth flow

Complete OAuth flow to generate authorized credentials.

**Usage:**
```bash
google-gmail-tool auth login [OPTIONS]
```

**Options:**
- `--client-id ID`: OAuth Client ID
- `--client-secret SECRET`: OAuth Client Secret
- `--json-file PATH`: Path to client secret JSON (alternative)
- `--output PATH` / `-o PATH`: Output file for credentials (default: `~/.config/google-gmail-tool/credentials.json`)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Login with client ID and secret
google-gmail-tool auth login \
    --client-id "123...apps.googleusercontent.com" \
    --client-secret "GOCSPX-..."

# Login with JSON file
google-gmail-tool auth login \
    --json-file ~/Downloads/client_secret.json

# Custom output location
google-gmail-tool auth login \
    --json-file ~/Downloads/client_secret.json \
    --output ~/.credentials/google.json
```

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

### Multi-Level Verbosity

Control logging detail with `-v/-vv/-vvv` flags:

- **No flag** (WARNING): Only critical issues
- **`-v`** (INFO): High-level operations, important events
- **`-vv`** (DEBUG): Detailed operations, API calls, validation steps
- **`-vvv`** (TRACE): Full request/response, library internals

**Examples:**
```bash
# Normal mode (warnings only)
google-gmail-tool mail list

# Info level
google-gmail-tool mail list -v

# Debug level
google-gmail-tool mail list -vv

# Trace level (includes Google API internals)
google-gmail-tool mail list -vvv
```

---

### Shell Completion

Install tab completion for bash, zsh, or fish:

**Bash:**
```bash
eval "$(google-gmail-tool completion bash)"
# Or add to ~/.bashrc
```

**Zsh:**
```bash
eval "$(google-gmail-tool completion zsh)"
# Or add to ~/.zshrc
```

**Fish:**
```bash
google-gmail-tool completion fish > ~/.config/fish/completions/google-gmail-tool.fish
```

---

### Output Formats

All commands support JSON and text output:

**JSON (default):**
```bash
google-gmail-tool mail list | jq '.[] | .subject'
```

**Text (human-readable):**
```bash
google-gmail-tool mail list --text
```

---

### Pipeline Integration

Designed for Unix pipeline integration:

**Examples:**
```bash
# Extract email subjects
google-gmail-tool mail list | jq -r '.[] | .subject'

# Count unread messages
google-gmail-tool mail list --query "is:unread" | jq 'length'

# Complete first incomplete task
TASK_ID=$(google-gmail-tool task list -n 1 | jq -r '.[0].id')
google-gmail-tool task complete "$TASK_ID"

# Search and download Drive file
FILE_ID=$(google-gmail-tool drive search --name "report" | jq -r '.[0].id')
google-gmail-tool drive download "$FILE_ID" report.pdf
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: "Credentials not found"**
```bash
# Error
[ERROR] Credentials not found
```

**Solution:**
1. Set credentials environment variable:
   ```bash
   export GOOGLE_GMAIL_TOOL_CREDENTIALS=~/.config/google-gmail-tool/credentials.json
   ```
2. Or use `auth login` to generate credentials:
   ```bash
   google-gmail-tool auth login --json-file ~/Downloads/client_secret.json
   ```

---

**Issue: "API access denied"**

**Solution:**
1. Check API is enabled in Google Cloud Console
2. Verify OAuth scopes include required permissions
3. Re-run auth check:
   ```bash
   google-gmail-tool auth check -vv
   ```

---

**Issue: "Token expired"**

**Solution:**
Credentials include refresh token, should auto-refresh. If not:
```bash
# Re-authenticate
google-gmail-tool auth login --json-file ~/Downloads/client_secret.json
```

---

**Issue: "Obsidian export fails"**

**Solution:**
1. Set `OBSIDIAN_ROOT` environment variable:
   ```bash
   export OBSIDIAN_ROOT=~/Documents/ObsidianVault
   ```
2. Or use `--obsidian-root` flag:
   ```bash
   google-gmail-tool mail export-obsidian --obsidian-root ~/Documents/ObsidianVault
   ```

### Getting Help

```bash
# Main help
google-gmail-tool --help

# Command group help
google-gmail-tool mail --help
google-gmail-tool calendar --help

# Specific command help
google-gmail-tool mail list --help
google-gmail-tool task create --help
```

</details>

## Exit Codes

- `0`: Success
- `1`: General error (authentication, API error, validation failure)
- `2`: Not found (message/event/task/file not found)

## Output Formats

**JSON (default):**
- Agent-friendly structured data
- Suitable for parsing with jq
- Consistent schema across commands

**Text (--text flag):**
- Human-readable format
- Tabular or list output
- Good for terminal viewing

## Best Practices

1. **Use Environment Variables**: Set `GOOGLE_GMAIL_TOOL_CREDENTIALS` and `OBSIDIAN_ROOT` for convenience
2. **Enable Verbosity for Debugging**: Use `-vv` or `-vvv` when troubleshooting
3. **JSON Output for Scripts**: Default JSON output is ideal for automation
4. **Obsidian Integration**: Use export commands to maintain synchronized notes
5. **Pipeline with jq**: Combine with jq for powerful data processing
6. **Shell Completion**: Install completion for better CLI experience

## Resources

- **GitHub**: https://github.com/dnvriend/google-gmail-tool
- **Google Cloud Console**: https://console.cloud.google.com/apis/credentials
- **Gmail Search Syntax**: https://support.google.com/mail/answer/7190
- **Obsidian**: https://obsidian.md
