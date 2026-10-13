---
name: imap-smtp-email
version: 1.0.0
description: "IMAP/SMTP Email integration - Read, send, and manage emails using standard email protocols. Supports Gmail, Outlook, and custom email servers."
author: gzlicanyi
---

# IMAP/SMTP Email 📧

**By gzlicanyi**

A comprehensive email integration skill that allows you to read, send, and manage emails using standard IMAP and SMTP protocols.

## Overview

This skill enables OpenClaw to:
- **Read emails** from your inbox via IMAP
- **Send emails** via SMTP
- **Search** through email content
- **Manage** folders and labels
- **Process** attachments

## Prerequisites

### Required Information

To use this skill, you need your email provider's IMAP and SMTP settings:

**Gmail**:
- IMAP Server: `imap.gmail.com`
- IMAP Port: `993` (SSL)
- SMTP Server: `smtp.gmail.com`
- SMTP Port: `465` (SSL) or `587` (TLS)
- Authentication: Required (App Password recommended)

**Outlook/Office 365**:
- IMAP Server: `outlook.office365.com`
- IMAP Port: `993` (SSL)
- SMTP Server: `smtp.office365.com`
- SMTP Port: `587` (TLS)
- Authentication: Required

**Custom Server**:
- Use your provider's IMAP/SMTP settings

**Aliyun Enterprise Email (阿里云企业邮箱)**:
- IMAP Server: `imap.qiye.aliyun.com`
- IMAP Port: `993` (SSL)
- SMTP Server: `smtp.qiye.aliyun.com`
- SMTP Port: `465` (SSL)
- POP Server: `pop.qiye.aliyun.com`
- POP Port: `995` (SSL)
- Authentication: Required (邮箱地址 + 密码/Token)

### Security Notes

⚠️ **Important**: For Gmail and some providers, you may need to:
1. Enable 2-factor authentication
2. Generate an App Password (not your regular password)
3. Allow less secure apps (deprecated, use App Password instead)

## Configuration

### Step 1: Create Email Configuration

Create a configuration file at `/workspace/projects/.email-credentials.json`:

```json
{
  "imap": {
    "host": "imap.gmail.com",
    "port": 993,
    "secure": true,
    "user": "your-email@gmail.com",
    "password": "your-app-password"
  },
  "smtp": {
    "host": "smtp.gmail.com",
    "port": 465,
    "secure": true,
    "user": "your-email@gmail.com",
    "password": "your-app-password"
  }
}
```

### Step 2: Test Connection

```bash
# Test IMAP connection
openclaw email test --protocol imap

# Test SMTP connection
openclaw email test --protocol smtp
```

## Usage

### Reading Emails

```bash
# List recent emails (default: 10)
openclaw email list --limit 20

# Search emails by subject
openclaw email search --subject "project update"

# Read a specific email by ID
openclaw email read --id 12345

# List emails from a specific sender
openclaw email list --from "boss@company.com"

# List unread emails
openclaw email list --unread

# List emails with attachments
openclaw email list --attachments
```

### Sending Emails

```bash
# Send a simple email
openclaw email send \
  --to "recipient@example.com" \
  --subject "Meeting Update" \
  --body "Hi, here's the update..."

# Send email with CC and BCC
openclaw email send \
  --to "primary@example.com" \
  --cc "cc@example.com" \
  --bcc "bcc@example.com" \
  --subject "Newsletter" \
  --body "Content here..."

# Send email with attachment
openclaw email send \
  --to "recipient@example.com" \
  --subject "Report" \
  --body "Please find attached..." \
  --attach "/path/to/file.pdf"

# Send HTML email
openclaw email send \
  --to "recipient@example.com" \
  --subject "Invitation" \
  --body "<h1>Welcome!</h1><p>HTML content</p>" \
  --html
```

### Email Management

```bash
# Mark as read
openclaw email mark-read --id 12345

# Mark as unread
openclaw email mark-unread --id 12345

# Delete email
openclaw email delete --id 12345

# Move to folder
openclaw email move --id 12345 --folder "Important"

# Archive email
openclaw email archive --id 12345

# Star/unstar email
openclaw email star --id 12345
openclaw email unstar --id 12345
```

### Folder Management

```bash
# List folders
openclaw email folders

# Create folder
openclaw email create-folder --name "Project X"

# List emails in specific folder
openclaw email list --folder "Project X"
```

## Advanced Features

### Email Processing

```bash
# Process attachments
openclaw email attachments --id 12345

# Download attachment
openclaw email download-attachment \
  --email-id 12345 \
  --attachment-id 1 \
  --output "/path/to/save"
```

### Batch Operations

```bash
# Mark multiple as read
openclaw email batch-mark-read --ids "12345,12346,12347"

# Delete multiple emails
openclaw email batch-delete --ids "12345,12346,12347"

# Archive by date
openclaw email archive-before --date "2024-01-01"
```

## Integration with Other Skills

This skill works well with:
- **calendar skills** - Schedule meetings from email
- **file management** - Save attachments
- **summarization** - Summarize long email threads
- **proactive-agent** - Proactively check important emails

## Best Practices

### Security
- Never store passwords in plain text
- Use App Passwords when available
- Limit permissions to minimum required
- Regularly rotate credentials

### Performance
- Use filters to reduce email load
- Process emails in batches
- Archive old emails regularly

### Automation
```bash
# Daily digest of unread emails
openclaw email list --unread --limit 20

# Watch for important emails
openclaw email watch --folder "INBOX" --interval 300
```

## Troubleshooting

### Authentication Failed
- Check username and password
- For Gmail: Enable 2FA and use App Password
- For Outlook: Check if account is locked

### Connection Timeout
- Verify server settings
- Check firewall rules
- Ensure correct port (993 for IMAP SSL, 465/587 for SMTP)

### IMAP/SMTP Not Enabled
- Gmail: Settings → Forwarding and POP/IMAP
- Outlook: Settings → Mail → Sync email

### Attachment Download Failed
- Check file size limits
- Verify sufficient disk space
- Check permission settings

## Gmail Setup Guide

### Enable IMAP
1. Go to Gmail Settings
2. Click "Forwarding and POP/IMAP"
3. Enable IMAP
4. Save changes

### Generate App Password
1. Go to Google Account Settings
2. Security → 2-Step Verification
3. App Passwords → Generate
4. Use this password in config

## Outlook Setup Guide

### Enable IMAP
1. Go to Outlook Settings
2. Mail → Sync email
3. Enable IMAP
4. Save changes

### Use Modern Authentication
- OAuth 2.0 support recommended
- Use Exchange password if needed

## Example Workflows

### Workflow 1: Daily Email Summary
```bash
# Get unread emails from important senders
openclaw email list \
  --unread \
  --from "boss@company.com,hr@company.com" \
  --limit 10

# Summarize using AI
openclaw email summarize --folder "INBOX"
```

### Workflow 2: Meeting Coordination
```bash
# Find meeting requests
openclaw email search --subject "meeting"

# Extract date/time and propose times
openclaw email extract-meeting --id 12345

# Send confirmation
openclaw email send \
  --to "organizer@example.com" \
  --subject "Meeting Confirmation" \
  --body "Confirmed for 2pm tomorrow"
```

### Workflow 3: Newsletter Processing
```bash
# Find newsletters
openclaw email list --folder "Newsletter"

# Extract key points
openclaw email summarize --folder "Newsletter"

# Archive after reading
openclaw email archive-before --date "2024-01-01" \
  --folder "Newsletter"
```

## Limitations

- Large attachments (>25MB) may time out
- Batch operations limited to 50 emails at a time
- HTML rendering may vary
- Calendar invites require additional processing

## Metrics to Track

Monitor:
- Email processing time
- Success rate for sending/receiving
- Attachment download success
- API quota usage (if applicable)

---

**Note**: This skill requires manual configuration of email credentials. Never commit email credentials to version control.
