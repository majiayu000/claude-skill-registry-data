---
name: managing-google-workspace
description: Manages Google Workspace services including Gmail, Drive, Docs, Sheets, Slides, Calendar, Forms, Tasks, and Chat. Use when the user wants to interact with Google services, manage emails, documents, spreadsheets, presentations, or calendar events.
---

# Google Workspace Tools

Tools for interacting with Google Workspace APIs.

## Authentication

All tools require OAuth2 authentication. Set environment variables:
- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`

## Quick Reference

| Service | Common Operations |
|---------|-------------------|
| Gmail | Send, search, read emails |
| Drive | List, upload, download, share files |
| Docs | Create, read, edit documents |
| Sheets | Read, write, query spreadsheets |
| Slides | Create presentations, add slides |
| Calendar | List, create, update events |
| Forms | Create forms, get responses |
| Tasks | Manage task lists and tasks |
| Chat | Send messages to spaces |

## Gmail

```python
# Search emails
result = await gmail_search_emails(query="from:user@example.com", max_results=10)

# Send email
result = await gmail_send_email(
    to="recipient@example.com",
    subject="Hello",
    body="Message content"
)

# Read email
result = await gmail_get_email(message_id="abc123")
```

## Drive

```python
# List files
result = await drive_list_files(query="name contains 'report'", max_results=25)

# Upload file
result = await drive_upload_file(file_path="/local/file.pdf", folder_id="folder123")

# Download file
result = await drive_download_file(file_id="abc123", destination="/local/path")

# Share file
result = await drive_share_file(file_id="abc123", email="user@example.com", role="reader")
```

## Docs

```python
# Create document
result = await docs_create_document(title="My Document")

# Read content
result = await docs_get_content(document_id="abc123")

# Append text
result = await docs_append_text(document_id="abc123", text="New paragraph")
```

## Sheets

```python
# Read values
result = await google_sheets_read_values(spreadsheet_id="abc123", range_notation="Sheet1!A1:D10")

# Write values
result = await google_sheets_write_values(
    spreadsheet_id="abc123",
    range_notation="Sheet1!A1",
    values=[["Header1", "Header2"], ["Data1", "Data2"]]
)

# Create spreadsheet
result = await google_sheets_create_spreadsheet(title="New Sheet", sheet_names=["Data", "Summary"])
```

## Slides

```python
# Create presentation
result = await google_slides_create_presentation(title="My Presentation")

# Add slide
result = await google_slides_add_slide(presentation_id="abc123", layout="TITLE_AND_BODY")

# Add text
result = await google_slides_add_text(
    presentation_id="abc123",
    slide_id="slide1",
    text="Hello World",
    x=100, y=100
)
```

## Calendar

```python
# List events
result = await calendar_list_events(max_results=10)

# Create event
result = await calendar_create_event(
    summary="Meeting",
    start_time="2024-01-15T10:00:00",
    end_time="2024-01-15T11:00:00"
)
```

## Forms

```python
# Create form
result = await forms_create_form(title="Survey")

# Add question
result = await forms_add_question(
    form_id="abc123",
    title="Your feedback?",
    question_type="TEXT"
)

# Get responses
result = await forms_get_responses(form_id="abc123")
```

## Tasks

```python
# List task lists
result = await tasks_list_tasklists()

# Create task
result = await tasks_create_task(tasklist_id="abc123", title="Complete report")

# Complete task
result = await tasks_complete_task(tasklist_id="abc123", task_id="task456")
```

## Chat

```python
# Send message
result = await chat_send_message(space_name="spaces/abc123", text="Hello team!")

# List spaces
result = await chat_list_spaces()
```

## Response Format

All tools return:
```json
{
  "success": true,
  "data": { ... }
}
```

On error:
```json
{
  "success": false,
  "error": "Error description"
}
```

## Additional Resources

See [README.md](README.md) for detailed setup instructions and OAuth configuration.
