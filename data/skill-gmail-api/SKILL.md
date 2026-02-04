---
name: skill-gmail-api
description: |
  Gmail API skill for email operations via CLI. Supports reading, drafting, sending, archiving, labeling, and batch operations.
  Use when user needs to: read emails, create/send drafts, reply to messages, archive/trash messages, manage labels, or perform bulk email operations.
allowed-tools:
  - Execute
---

# Gmail API Skill

## Quick Reference

```bash
# Read
scripts/gmail.py read --limit 10
scripts/gmail.py read --query "is:unread" --full
scripts/gmail.py get --id MSG_ID

# Draft & Send  
scripts/gmail.py draft --to "x@y.com" --subject "Hi" --body "Hello"
scripts/gmail.py draft --reply-to MSG_ID --body "Thanks!"
scripts/gmail.py send --draft-id DRAFT_ID
scripts/gmail.py send --to "x@y.com" --subject "Hi" --body "Hello"

# Manage
scripts/gmail.py archive --id MSG_ID
scripts/gmail.py trash --id MSG_ID
scripts/gmail.py star --id MSG_ID
scripts/gmail.py mark-read --id MSG_ID

# Batch
scripts/gmail.py batch-archive --query "from:newsletters@"
scripts/gmail.py batch-mark-read --query "is:unread from:notifications@"
```

Run `scripts/gmail.py --help` or `scripts/gmail.py COMMAND --help` for options.

**Full command reference**: See [references/commands.md](references/commands.md)

## Setup

1. Create OAuth credentials at [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Copy `credentials.example.json` to `credentials.json` and add your client_id/secret
3. First run opens browser for OAuth consent
