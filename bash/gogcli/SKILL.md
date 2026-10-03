---
name: gogcli
description: Use `gog` CLI for Gmail and Google Calendar operations. Trigger when user asks to send/search/read email, manage Gmail labels/drafts/filters, create/update/list calendar events, check availability, or interact with Google Workspace email and scheduling. Also covers auth setup, account management, and output formatting.
---

# gogcli — Gmail & Calendar CLI

`gog` is a fast, script-friendly CLI for Google Workspace. This skill covers Gmail and Calendar — the two most common services.

Install: `brew install gogcli`

## Quick reference

### Auth setup

```bash
gog auth credentials ~/Downloads/client_secret_....json
gog auth add you@gmail.com
export GOG_ACCOUNT=you@gmail.com
```

Verify: `gog auth list --check`

### Gmail essentials

```bash
# Search
gog gmail search 'newer_than:7d' --max 10
gog gmail search 'from:boss@example.com is:unread'

# Read
gog gmail thread get <threadId>
gog gmail get <messageId>

# Send
gog gmail send --to a@b.com --subject "Hi" --body "Hello"
gog gmail send --to a@b.com --subject "Hi" --body-file ./message.txt
gog gmail send --to a@b.com --subject "Report" --body "See attached" --body-html "<p>See attached</p>"

# Reply (threaded, with quoted original)
gog gmail send --reply-to-message-id <messageId> --quote --to a@b.com --subject "Re: Hi" --body "My reply"

# Drafts
gog gmail drafts create --to a@b.com --subject "Draft" --body "Body"
gog gmail drafts list
gog gmail drafts send <draftId>

# Labels
gog gmail labels list
gog gmail thread modify <threadId> --add STARRED --remove INBOX

# Download attachments
gog gmail thread get <threadId> --download --out-dir ./attachments
```

### Calendar essentials

```bash
# List events
gog calendar events primary --today
gog calendar events primary --tomorrow
gog calendar events primary --week
gog calendar events primary --days 3
gog calendar events primary --from 2025-01-15 --to 2025-01-20

# All calendars
gog calendar events --all --today

# Search
gog calendar search "standup" --today
gog calendar search "meeting" --days 30

# Create event
gog calendar create primary \
  --summary "Team Sync" \
  --from 2025-01-15T14:00:00Z \
  --to 2025-01-15T15:00:00Z \
  --attendees "alice@example.com,bob@example.com" \
  --location "Zoom"

# Update event
gog calendar update primary <eventId> \
  --summary "Updated Meeting" \
  --from 2025-01-15T11:00:00Z \
  --to 2025-01-15T12:00:00Z

# Delete event
gog calendar delete primary <eventId>

# RSVP
gog calendar respond primary <eventId> --status accepted
gog calendar respond primary <eventId> --status declined

# Check availability
gog calendar freebusy --calendars "primary,work@example.com" \
  --from 2025-01-15T00:00:00Z --to 2025-01-16T00:00:00Z

# Conflicts
gog calendar conflicts --all --today

# Calendars list
gog calendar calendars
```

## Key patterns

### Output formats

- Default: human-readable tables
- `--json`: machine-readable JSON (stdout), errors on stderr
- `--plain`: stable TSV for piping

Always use `--json` when chaining commands or parsing output programmatically.

### Account selection

```bash
# Flag
gog gmail search 'is:unread' --account work@company.com

# Alias
gog auth alias set work work@company.com
gog gmail search 'is:unread' --account work

# Environment (preferred for sessions)
export GOG_ACCOUNT=you@gmail.com
```

### Confirmation behavior

`gog` prompts before destructive actions (sending mail, creating events). Use `--force` to skip, `--no-input` for CI/scripting.

### Send notifications for calendar changes

Pass `--send-updates all` (or `externalOnly`) on create/update/delete to notify attendees. Default: no notifications sent.

## Extended reference

For complete command reference including filters, batch operations, vacation settings, delegation, recurring events, special event types (focus-time, out-of-office, working-location), and advanced patterns, see [references/commands.md](references/commands.md).
