---
name: Google Workspace
description: >
  Access Gmail, Calendar, Drive, Contacts, Sheets, Docs, Tasks, and other Google
  services via the `gog` CLI. Use whenever the user mentions email, calendar,
  schedule, drive, documents, spreadsheets, contacts, tasks, or anything Google
  Workspace-related. Triggers on: "check my email," "what's on my calendar,"
  "search my gmail," "send an email," "find a doc," "look up a contact,"
  "my schedule," "upcoming events," "unread mail," "create an event,"
  "what did I get from [person]," "search drive," "check my tasks,"
  "school email," "Brown email," or any request involving Google data.
  Also use when composing, replying to, or drafting emails.
---

# Google Workspace via gog CLI

`gog` is installed locally at `/opt/homebrew/bin/gog`. Run commands directly via Bash — no SSH or MCP needed.

## Accounts

| Account | Flag | Services |
|---------|------|----------|
| kosta963@gmail.com | `-a kosta963@gmail.com` | Gmail, Calendar, Drive, Contacts, Docs, Sheets, Chat, Classroom, Tasks, People, Forms, Slides, AppScript |
| kosta_milovanovic@brown.edu | `-a kosta_milovanovic@brown.edu` | Gmail, Calendar, Drive, Contacts, Docs, Sheets |

When the user says "my email" or "my calendar" without specifying, use the personal account. Use the Brown account when the user mentions "school," "Brown," "university," or "edu."

## Base Pattern

```bash
gog <service> <command> [flags] -a ACCOUNT --json --no-input
```

- `--json` for structured output (preferred for processing)
- `--plain` for TSV output (compact, grep-friendly)
- `--results-only` strips envelope metadata (cleaner JSON)
- `--no-input` prevents interactive prompts
- `--max N` limits result count

## Gmail

```bash
# Search threads (default: last 10)
gog gmail search 'newer_than:7d' -a EMAIL --json --no-input

# Search individual messages (bypasses thread grouping)
gog gmail messages search 'in:inbox from:example.com' --max 20 -a EMAIL --json --no-input

# Read a specific thread
gog gmail read THREAD_ID -a EMAIL --json --no-input

# Send plain text
gog gmail send --to recipient@example.com --subject 'Subject' --body 'Body text' -a EMAIL --no-input

# Send multi-line (heredoc)
gog gmail send --to recipient@example.com --subject 'Subject' --body-file - -a EMAIL --no-input <<'EOF'
Paragraph one.

Paragraph two.
EOF

# Send HTML
gog gmail send --to recipient@example.com --subject 'Subject' --body-html '<p>Hello</p>' -a EMAIL --no-input

# Reply to a thread
gog gmail send --to recipient@example.com --subject 'Re: Original' --body 'Reply' --reply-to-message-id MSG_ID -a EMAIL --no-input

# Create draft
gog gmail drafts create --to recipient@example.com --subject 'Subject' --body-file ./message.txt -a EMAIL --no-input

# Send existing draft
gog gmail drafts send DRAFT_ID -a EMAIL --no-input
```

Gmail search uses the same query syntax as the Gmail web UI: `from:`, `to:`, `subject:`, `newer_than:`, `older_than:`, `is:unread`, `has:attachment`, `label:`, etc.

`gog gmail search` returns one row per thread. Use `gog gmail messages search` when every individual message is needed.

## Calendar

```bash
# List events for a date range
gog calendar events primary --from 2026-02-26 --to 2026-02-27 -a EMAIL --json --no-input

# Create an event
gog calendar create primary --summary 'Meeting' --from 2026-02-26T10:00:00 --to 2026-02-26T11:00:00 -a EMAIL --no-input

# Update an event
gog calendar update primary EVENT_ID --summary 'New Title' -a EMAIL --no-input

# Show available event colors
gog calendar colors
```

Event color IDs (1-11): use `--event-color <id>` when creating/updating.

## Drive

```bash
# List recent files
gog drive ls -a EMAIL --json --no-input

# Search files
gog drive search 'name contains "report"' --max 10 -a EMAIL --json --no-input

# Download a file
gog drive download FILE_ID -a EMAIL --no-input

# Upload a file
gog drive upload ./local-file.pdf -a EMAIL --no-input
```

## Sheets

```bash
# Read a range
gog sheets get SHEET_ID 'Sheet1!A1:D10' -a EMAIL --json --no-input

# Write a range
gog sheets update SHEET_ID 'Sheet1!A1:B2' --values-json '[["Name","Score"],["Alice","95"]]' --input USER_ENTERED -a EMAIL --no-input

# Append rows
gog sheets append SHEET_ID 'Sheet1!A:C' --values-json '[["x","y","z"]]' --insert INSERT_ROWS -a EMAIL --no-input

# Get sheet metadata (tab names, dimensions)
gog sheets metadata SHEET_ID -a EMAIL --json --no-input

# Clear a range
gog sheets clear SHEET_ID 'Sheet1!A2:Z' -a EMAIL --no-input
```

## Docs

```bash
# Read a doc as text
gog docs cat DOC_ID -a EMAIL --no-input

# Export to file
gog docs export DOC_ID --format txt --out /tmp/doc.txt -a EMAIL --no-input
```

## Contacts

```bash
gog contacts list --max 20 -a EMAIL --json --no-input
```

## Tasks

```bash
gog tasks list -a EMAIL --json --no-input
```

## Guidelines

- Confirm with the user before sending emails or creating/modifying calendar events, because these actions are visible to others.
- Read operations (search, list, read) are safe to run without confirmation.
- Use `--dry-run` when the user wants to preview a write action before committing.
- When displaying email results, summarize the key fields (date, from, subject) rather than dumping raw JSON.
- When displaying calendar events, format them as a readable schedule with times in the user's timezone (America/New_York).
- For large result sets, use `--max` to limit output and paginate with `--page` when needed.
- The `--select` flag picks specific JSON fields: `--select id,subject,from` reduces output size.
