---
name: google-workspace
description: Manage Google Calendar and Gmail through Python code execution. Trigger keywords include calendar, gmail, meeting, email, schedule, event.
---

# Google Workspace Skill

Manage Google Calendar and Gmail using Python code execution.

## Purpose

This skill provides procedural knowledge for working with Google Calendar and Gmail APIs. Write Python code that executes in a sandbox, processes data locally, and returns only summaries.

**Key principle**: Data processing happens in the sandbox, not in context.

## When to Use

Use this skill when users need to:
- Query, create, or manage calendar events
- Send, search, or process emails
- Perform batch operations on calendars or mailboxes
- Generate reports combining calendar and email data

## Execution Workflow (Automatic)

When user requests Calendar/Gmail operation:

1. **Auto-check environment** → If venv missing, create it (30s)
2. **Auto-check token** → If missing/expired, run `scripts/unified_auth.py` (user clicks browser)
3. **Execute operation** → Run code in sandbox, return summary only

User only interacts once: clicking "Allow" in browser during first OAuth. Everything else is automatic.

## Environment Setup (Auto-detect and Fix)

Before executing any Calendar/Gmail operation, check and auto-fix environment:

**1. Check venv exists**:
```bash
if [ ! -d ~/.google-workspace/venv ]; then
    echo "⚙️  First setup: Creating Python virtual environment..."
    mkdir -p ~/.google-workspace
    python3 -m venv ~/.google-workspace/venv
    source ~/.google-workspace/venv/bin/activate
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    echo "✅ Environment setup complete"
fi
```

**2. Check token exists**:
```bash
if [ ! -f ~/.google-workspace/token.json ]; then
    echo "❌ Token not found, OAuth authentication required"
    cd ~/.claude/skills/google-workspace
    source ~/.google-workspace/venv/bin/activate
    python3 scripts/unified_auth.py
    # Script will open browser automatically, user clicks "Allow"
fi
```

**3. Try operation, auto-refresh if expired**:
- First attempt the API call
- If get 401 error, token auto-refreshes (handled by google-auth)
- If refresh fails, re-run `scripts/unified_auth.py`

## Code Execution Pattern

Always use this template for Calendar/Gmail operations:

```bash
source ~/.google-workspace/venv/bin/activate && python3 << 'EOF'
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

# Auto-discover token
token_path = os.path.expanduser('~/.google-workspace/token.json')
creds = Credentials.from_authorized_user_file(token_path)

# Build service
calendar = build('calendar', 'v3', credentials=creds)
# OR: gmail = build('gmail', 'v1', credentials=creds)

# Your operation here
# ... process data in sandbox ...

# Return only summary
print("Summary: ...")
EOF
```

## Supported Operations

### Calendar

**List operations**: list-calendars, list-events, search-events, get-event
**Modification**: create-event, update-event, delete-event
**Utilities**: get-freebusy, list-colors, get-current-time

**Key parameters**:
- Time ranges: `timeMin`, `timeMax` (ISO 8601)
- Filtering: `singleEvents=True`, `orderBy='startTime'`
- Calendar selection: Query all calendars by default

### Gmail

**Email operations**: send_email, search_emails, read_email
**Batch operations**: batch_modify_emails, batch_delete_emails
**Labels**: list_labels, create_label, update_label, delete_label, add_labels, remove_labels
**Drafts**: get_draft, create_draft, delete_draft

**Query syntax**: Use Gmail search operators in `q` parameter
**Batch size**: Limit to 50 items per batch for API compliance

Full API references available in `references/calendar-api.md` and `references/gmail-api.md`.

## Code Execution Pattern

### Core Strategy

```python
# 1. Call API
events = calendar.events().list(
    calendarId='primary',
    timeMin='2025-11-13T00:00:00Z',
    maxResults=100
).execute()['items']

# 2. Process in sandbox (data never enters context)
meetings = [e for e in events if len(e.get('attendees', [])) > 1]
by_date = {}
for m in meetings:
    date = m['start']['dateTime'][:10]
    by_date.setdefault(date, []).append(m['summary'])

# 3. Return only summary
print(f"Found {len(meetings)} meetings across {len(by_date)} days")
for date, titles in sorted(by_date.items()):
    print(f"{date}: {len(titles)} meetings")
```

### Optimization Rules

**DO**:
- Filter data in sandbox using list comprehensions
- Use API-native filtering (`timeMin`, `q` parameter)
- Batch operations together in single execution
- Return counts, summaries, or top-N results

**DON'T**:
- Return full JSON objects to context
- Make multiple small API calls when batch is possible
- Process data in context instead of sandbox
- Output more than necessary for user's request

### Common Patterns

**Multi-calendar query** (ALWAYS use this, user has multiple calendars):
```python
# 1. Get all calendars
calendars = calendar.calendarList().list().execute()['items']

# 2. Query events from ALL calendars
all_events = []
for cal in calendars:
    try:
        events = calendar.events().list(
            calendarId=cal['id'],
            timeMin='2025-11-13T00:00:00Z',
            maxResults=100,
            singleEvents=True
        ).execute().get('items', [])

        # Tag with calendar info
        for e in events:
            e['_calendar_name'] = cal['summary']
            e['_calendar_id'] = cal['id']

        all_events.extend(events)
    except Exception as e:
        # Skip inaccessible calendars
        continue

# 3. Process all_events in sandbox
# ... sort, filter, group by date, etc.
print(f"Found {len(all_events)} events across {len(calendars)} calendars")
```

**IMPORTANT**: Never use `calendarId='primary'` alone. Always query ALL calendars unless user specifically asks for one.

**Email search with metadata only**:
```python
results = gmail.users().messages().list(userId='me', q='is:unread').execute()
for msg in results.get('messages', []):
    detail = gmail.users().messages().get(
        userId='me',
        id=msg['id'],
        format='metadata',  # Only headers, not full body
        metadataHeaders=['From', 'Subject', 'Date']
    ).execute()
    # Extract headers in sandbox
```

**Batch label modification**:
```python
for i in range(0, len(message_ids), 50):
    batch = message_ids[i:i+50]
    gmail.users().messages().batchModify(
        userId='me',
        body={'ids': batch, 'removeLabelIds': ['UNREAD']}
    ).execute()
```

## Error Handling

```python
from googleapiclient.errors import HttpError

try:
    result = calendar.events().list(...).execute()
except HttpError as e:
    if e.resp.status == 401:
        print("Authentication expired. User needs to re-authorize.")
    else:
        print(f"API error: {e}")
```
