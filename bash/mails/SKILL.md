---
name: mails
description: Email infrastructure for AI agents - send/receive emails via Mails.dev
version: 1.0.0
author: Harmes House
tags: [Email, AI-Agent, Mails.dev]
---

# Mails.dev Email CLI

Email infrastructure for AI agents. Send and receive emails from `imclaw@mails.dev`.

## Configuration

Already configured:
- Mailbox: `imclaw@mails.dev`
- API key: stored in `~/.mailsrc` (configured via `mails config set api_key`)

Requires `bun` runtime. Path: `~/.bun/bin/bun`

## Common Operations

### Send Email

```bash
export BUN_INSTALL="$HOME/.bun" && export PATH="$BUN_INSTALL/bin:$PATH"
mails send --to <recipient> --subject "<subject>" --body "<message>"
```

Example:
```bash
mails send --to user@example.com --subject "Hello" --body "Test message"
```

With HTML:
```bash
mails send --to user@example.com --subject "Report" --html "<h1>Report</h1><p>Data...</p>"
```

### Check Inbox

```bash
mails inbox                           # List recent emails
mails inbox --mailbox imclaw@mails.dev  # List for specific mailbox
mails inbox --query "keyword"         # Search emails
mails inbox <id>                      # Read specific email
mails inbox <id> --save               # Save attachments
```

### Verify Email (for confirmation codes)

```bash
mails code --to imclaw@mails.dev --timeout 60
```

## Workflows

### Automated Report Sending

```bash
#!/bin/bash
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

REPORT_DATE=$(date +%Y-%m-%d)
mails send \
  --to recipient@example.com \
  --subject "Daily Report - $REPORT_DATE" \
  --body "See attached report for $REPORT_DATE"
```

### Email Alert Integration

```bash
# In cron or automation script
mails send --to imclaw@mails.dev --subject "[Alert] System Issue" --body "Description of issue"
```

## Notes

- Rate limit: 100 emails/month on free tier
- Email IDs are shown as short prefixes (e.g., `a6d18a3c`)
- Full ID can be shown with `mails inbox --full-id`
- Attachments saved with `--save` flag