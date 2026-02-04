---
name: google-gmail-integration
description: Manages Gmail through the Gmail API. Search and read emails, send messages, manage labels and filters, handle attachments, and automate email workflows. Use when working with Gmail, reading/sending emails, searching inbox, managing email organization, or processing email data.
---

# Gmail Integration

Comprehensive Gmail integration enabling email search, message management, sending, label organization, attachment handling, and workflow automation through the Gmail API v1.

## Quick Start

When asked to work with Gmail:

1. **Authenticate**: Set up OAuth2 credentials (one-time setup)
2. **Search emails**: Find messages by sender, subject, date, or content
3. **Read messages**: Get email content and attachments
4. **Send emails**: Compose and send messages
5. **Organize**: Create labels, apply filters, archive messages
6. **Automate**: Process emails based on rules

## Prerequisites

### One-Time Setup

**1. Enable Gmail API:**
```bash
# Visit Google Cloud Console
# https://console.cloud.google.com/

# Enable Gmail API for your project
# APIs & Services > Enable APIs and Services > Gmail API
```

**2. Create OAuth2 Credentials:**
```bash
# In Google Cloud Console:
# APIs & Services > Credentials > Create Credentials > OAuth client ID
# Application type: Desktop app
# Download credentials as credentials.json
```

**3. Install Dependencies:**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client --break-system-packages
```

**4. Initial Authentication:**
```bash
python scripts/authenticate.py
# Opens browser for Google sign-in
# Saves token.json for future use
```

See [reference/setup-guide.md](reference/setup-guide.md) for detailed setup instructions.

## Core Operations

### Search Emails

**Basic search:**
```bash
# Search by keyword
python scripts/search_emails.py --query "project update"

# Search by sender
python scripts/search_emails.py --from "boss@company.com"

# Search by subject
python scripts/search_emails.py --subject "Weekly Report"

# Search unread
python scripts/search_emails.py --unread

# Search with label
python scripts/search_emails.py --label "Important"
```

**Advanced search queries:**
```python
# Combination search
query = "from:boss@company.com subject:urgent is:unread"

# Date ranges
query = "after:2025/01/01 before:2025/01/31"

# Has attachment
query = "has:attachment filename:pdf"

# Size filters
query = "larger:10M"

# Categories
query = "category:primary"
query = "category:social"
query = "category:promotions"

# Boolean operators
query = "(from:alice@company.com OR from:bob@company.com) subject:meeting"
```

See [reference/search-syntax.md](reference/search-syntax.md) for complete search reference.

### Read Messages

**Get message content:**
```bash
# Read email
python scripts/read_email.py --message-id MESSAGE_ID

# Get specific format
python scripts/read_email.py --message-id MESSAGE_ID --format full
python scripts/read_email.py --message-id MESSAGE_ID --format minimal
python scripts/read_email.py --message-id MESSAGE_ID --format raw
```

**Extract information:**
```bash
# Get headers
python scripts/get_headers.py --message-id MESSAGE_ID

# Get body text
python scripts/get_body.py --message-id MESSAGE_ID --format text
python scripts/get_body.py --message-id MESSAGE_ID --format html

# List attachments
python scripts/list_attachments.py --message-id MESSAGE_ID
```

**Download attachments:**
```bash
# Download all attachments
python scripts/download_attachments.py --message-id MESSAGE_ID --output ./downloads/

# Download specific attachment
python scripts/download_attachments.py --message-id MESSAGE_ID --filename "report.pdf"
```

### Send Emails

**Simple send:**
```bash
# Send plain text
python scripts/send_email.py \
  --to "recipient@example.com" \
  --subject "Hello" \
  --body "Email content here"

# Send to multiple recipients
python scripts/send_email.py \
  --to "user1@example.com,user2@example.com" \
  --cc "manager@example.com" \
  --subject "Team Update" \
  --body "Content here"
```

**Send with attachments:**
```bash
python scripts/send_email.py \
  --to "recipient@example.com" \
  --subject "Report" \
  --body "Please see attached" \
  --attachments "./report.pdf,./data.xlsx"
```

**Send HTML email:**
```bash
python scripts/send_email.py \
  --to "recipient@example.com" \
  --subject "Newsletter" \
  --html-body "./newsletter.html"
```

**Reply to message:**
```bash
python scripts/reply_email.py \
  --message-id MESSAGE_ID \
  --body "Thanks for your email..."
```

**Forward message:**
```bash
python scripts/forward_email.py \
  --message-id MESSAGE_ID \
  --to "colleague@example.com" \
  --body "FYI"
```

### Label Management

**Create labels:**
```bash
# Create label
python scripts/create_label.py --name "Project Alpha"

# Create nested label
python scripts/create_label.py --name "Projects/Alpha"

# Create with settings
python scripts/create_label.py \
  --name "Important" \
  --label-list-visibility show \
  --message-list-visibility show
```

**Apply labels:**
```bash
# Add label to message
python scripts/add_label.py --message-id MESSAGE_ID --label "Important"

# Add multiple labels
python scripts/add_label.py --message-id MESSAGE_ID --labels "Work,Urgent"

# Remove label
python scripts/remove_label.py --message-id MESSAGE_ID --label "Inbox"
```

**List labels:**
```bash
# Get all labels
python scripts/list_labels.py

# Get label ID
python scripts/get_label_id.py --name "Project Alpha"
```

### Message Management

**Mark as read/unread:**
```bash
# Mark as read
python scripts/mark_read.py --message-id MESSAGE_ID

# Mark as unread
python scripts/mark_unread.py --message-id MESSAGE_ID
```

**Archive/Trash:**
```bash
# Archive message (remove from Inbox)
python scripts/archive_email.py --message-id MESSAGE_ID

# Move to trash
python scripts/trash_email.py --message-id MESSAGE_ID

# Delete permanently
python scripts/delete_email.py --message-id MESSAGE_ID
```

**Batch operations:**
```bash
# Archive all read emails older than 30 days
python scripts/batch_archive.py --days 30 --read-only

# Delete all emails from sender
python scripts/batch_delete.py --from "spam@example.com"

# Mark all as read
python scripts/batch_mark_read.py --label "Inbox"
```

## Common Workflows

### Workflow 1: Process Unread Emails

**Scenario:** Read unread emails and categorize

```bash
# Get unread emails
python scripts/process_unread.py \
  --label-rules rules.json \
  --mark-read

# rules.json example:
{
  "rules": [
    {
      "condition": "from:boss@company.com",
      "action": "add_label",
      "label": "Important"
    },
    {
      "condition": "subject:invoice",
      "action": "add_label",
      "label": "Finance"
    }
  ]
}
```

### Workflow 2: Email to Task Conversion

**Scenario:** Convert emails into task format

```bash
# Extract tasks from emails
python scripts/email_to_tasks.py \
  --query "label:To-Do" \
  --output tasks.json \
  --mark-done
```

### Workflow 3: Automated Responses

**Scenario:** Send auto-replies based on conditions

```bash
# Auto-respond to specific emails
python scripts/auto_respond.py \
  --query "from:client@company.com subject:urgent" \
  --template response_template.txt \
  --label "Auto-Responded"
```

### Workflow 4: Email Backup

**Scenario:** Download emails for backup

```bash
# Backup all emails
python scripts/backup_emails.py \
  --output ./email_backup/ \
  --format mbox

# Backup specific label
python scripts/backup_emails.py \
  --label "Important" \
  --output ./important_backup/ \
  --include-attachments
```

### Workflow 5: Email Analytics

**Scenario:** Analyze email patterns

```bash
# Generate email statistics
python scripts/email_stats.py \
  --start-date 2025-01-01 \
  --end-date 2025-01-31 \
  --output stats.json

# Top senders
python scripts/top_senders.py --limit 10

# Email volume by day
python scripts/email_volume.py --days 30
```

## Search Query Syntax

### Operators

```python
# Sender/Recipient
"from:sender@example.com"
"to:recipient@example.com"
"cc:person@example.com"
"bcc:person@example.com"

# Subject
"subject:meeting"
"subject:(status report)"

# Date
"after:2025/01/01"
"before:2025/12/31"
"older_than:2d"  # days
"newer_than:7d"

# Status
"is:unread"
"is:read"
"is:starred"
"is:important"

# Has
"has:attachment"
"has:drive"
"has:document"
"has:spreadsheet"
"has:presentation"
"has:youtube"

# Size
"larger:10M"
"smaller:1M"
"size:5M"

# Category
"category:primary"
"category:social"
"category:promotions"
"category:updates"
"category:forums"

# Label
"label:important"
"label:work"
"-label:inbox"  # exclude inbox

# Filename
"filename:pdf"
"filename:report.xlsx"

# In
"in:inbox"
"in:trash"
"in:spam"
"in:anywhere"  # includes spam and trash

# Boolean
"OR"  # Must be uppercase
"AND"  # Implied, can be explicit
"-"   # NOT operator
"()"  # Grouping
```

### Example Queries

```python
# Unread emails from boss
"from:boss@company.com is:unread"

# Large emails with attachments
"has:attachment larger:5M"

# Recent important unread
"is:important is:unread newer_than:7d"

# Specific sender, subject, with PDF
"from:client@company.com subject:invoice has:attachment filename:pdf"

# Multiple senders
"(from:alice@company.com OR from:bob@company.com) subject:meeting"

# Date range with keyword
"after:2025/01/01 before:2025/01/31 project update"

# Exclude categories
"-category:promotions -category:social is:unread"
```

## Message Format Options

### Format Types

```python
# Minimal - IDs and labels only
format = 'minimal'

# Full - Complete message with body and headers
format = 'full'

# Raw - Raw MIME message (for forwarding)
format = 'raw'

# Metadata - Headers and labels without body
format = 'metadata'
```

### Accessing Message Parts

```python
# Get headers
headers = message['payload']['headers']
for header in headers:
    if header['name'] == 'Subject':
        subject = header['value']
    elif header['name'] == 'From':
        sender = header['value']

# Get body (plain text)
parts = message['payload'].get('parts', [])
for part in parts:
    if part['mimeType'] == 'text/plain':
        body = base64.urlsafe_b64decode(part['body']['data']).decode()

# Get attachments
for part in parts:
    if part.get('filename'):
        attachment_id = part['body']['attachmentId']
```

## Sending Email Formats

### Plain Text

```python
from email.mime.text import MIMEText
import base64

message = MIMEText('Email body')
message['to'] = 'recipient@example.com'
message['subject'] = 'Test Email'

raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
```

### HTML Email

```python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

message = MIMEMultipart('alternative')
message['to'] = 'recipient@example.com'
message['subject'] = 'HTML Email'

text = "Plain text version"
html = "<html><body><h1>HTML Version</h1></body></html>"

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

message.attach(part1)
message.attach(part2)
```

### With Attachments

```python
from email.mime.base import MIMEBase
from email import encoders
import os

message = MIMEMultipart()
message['to'] = 'recipient@example.com'
message['subject'] = 'With Attachment'

# Add body
body = MIMEText('Please see attached')
message.attach(body)

# Add attachment
with open('file.pdf', 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename={os.path.basename("file.pdf")}'
    )
    message.attach(part)
```

## Label Visibility

**Label list visibility:**
- `labelShow` - Show in label list
- `labelHide` - Hide from label list

**Message list visibility:**
- `show` - Show label in message list
- `hide` - Hide label in message list

## API Rate Limits

**Gmail API quotas:**
- **Queries per day:** 1,000,000,000
- **Queries per 100 seconds per user:** 250
- **Send message:** 100 per day per user (can request increase)

**Best practices:**
- Batch requests when possible
- Use partial responses to reduce data
- Implement exponential backoff
- Cache message IDs and metadata

## OAuth Scopes

```python
# Full access (read, send, delete)
'https://www.googleapis.com/auth/gmail.modify'

# Read-only
'https://www.googleapis.com/auth/gmail.readonly'

# Send only
'https://www.googleapis.com/auth/gmail.send'

# Labels only
'https://www.googleapis.com/auth/gmail.labels'

# Compose (draft and send)
'https://www.googleapis.com/auth/gmail.compose'

# Insert (add messages)
'https://www.googleapis.com/auth/gmail.insert'

# Metadata only
'https://www.googleapis.com/auth/gmail.metadata'
```

Choose the minimal scope needed for your use case.

## Scripts Reference

**Authentication:**
- `authenticate.py` - Initial OAuth setup
- `refresh_token.py` - Refresh token

**Search:**
- `search_emails.py` - Search with queries
- `find_by_sender.py` - Quick sender search
- `find_unread.py` - Get unread messages

**Read:**
- `read_email.py` - Read message content
- `get_headers.py` - Extract headers
- `get_body.py` - Get message body
- `list_attachments.py` - List attachments
- `download_attachments.py` - Download files

**Send:**
- `send_email.py` - Send new email
- `reply_email.py` - Reply to message
- `forward_email.py` - Forward message
- `send_bulk.py` - Send to multiple recipients

**Labels:**
- `create_label.py` - Create new label
- `list_labels.py` - Get all labels
- `add_label.py` - Apply label to message
- `remove_label.py` - Remove label

**Manage:**
- `mark_read.py` - Mark as read
- `mark_unread.py` - Mark as unread
- `archive_email.py` - Archive message
- `trash_email.py` - Move to trash
- `delete_email.py` - Permanent delete

**Batch:**
- `batch_archive.py` - Archive multiple
- `batch_delete.py` - Delete multiple
- `batch_mark_read.py` - Mark multiple read

**Automation:**
- `process_unread.py` - Process unread emails
- `auto_respond.py` - Automated responses
- `email_to_tasks.py` - Extract tasks
- `apply_filters.py` - Apply rule-based filters

**Analytics:**
- `email_stats.py` - Usage statistics
- `top_senders.py` - Most frequent senders
- `email_volume.py` - Volume over time

## Best Practices

1. **Use specific queries:** Narrow searches reduce processing time
2. **Batch operations:** Process multiple messages in single API call
3. **Cache data:** Store message IDs and metadata locally
4. **Handle pagination:** Use pageToken for large result sets
5. **Respect quotas:** Monitor API usage
6. **Error handling:** Implement retry logic with backoff
7. **Secure tokens:** Never commit token.json to version control
8. **Minimal scopes:** Request only needed permissions

## Integration Examples

See [examples/](examples/) for complete workflows:
- [examples/email-automation.md](examples/email-automation.md) - Automated email processing
- [examples/task-integration.md](examples/task-integration.md) - Email to task conversion
- [examples/reporting.md](examples/reporting.md) - Email analytics and reporting
- [examples/backup-strategy.md](examples/backup-strategy.md) - Email backup approaches

## Troubleshooting

**"Token expired"**
```bash
rm token.json
python scripts/authenticate.py
```

**"Insufficient permissions"**
- Check SCOPES in authenticate.py
- Delete token.json and re-auth with new scopes

**"Message not found"**
- Message may have been deleted
- Check if in trash or spam

**"Rate limit exceeded"**
- Implement delays between requests
- Use batch operations
- Request quota increase if needed

## Reference Documentation

- [reference/setup-guide.md](reference/setup-guide.md) - Setup instructions
- [reference/search-syntax.md](reference/search-syntax.md) - Complete search reference
- [reference/api-reference.md](reference/api-reference.md) - API documentation
- [reference/email-formats.md](reference/email-formats.md) - MIME and format reference
