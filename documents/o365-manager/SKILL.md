---
name: o365-manager
description: Expert in managing Office 365 professional emails and calendar. **Use this skill ONLY for professional emails when the user explicitly mentions 'mail professionnel', 'email professionnel', , 'professional email', 'Office 365', 'Outlook', or for calendar/meeting/events operations ('calendar', 'event', 'meeting', 'appointment', 'schedule', 'agenda', 'show my agenda', 'my agenda for', 'accept meeting', 'decline meeting', 'tentative', 'respond to meeting', 'create event', 'schedule meeting', 'check calendar', 'upcoming events').
---

# Office 365 Manager Skill

Expert in managing Office 365 emails and calendar using Microsoft Graph API with OAuth 2.1 PKCE authentication.

**Use this skill whenever the user mentions:**
- **Professional emails ONLY**: "mail professionnel", "email professionnel", "Office 365", "Outlook"
- **Calendar operations** (always professional): "calendar", "event", "meeting", "appointment", "schedule"
- **Agenda queries**: "show my agenda", "my agenda for", "what's on my calendar", "my schedule for"
- **Meeting responses**: "accept meeting", "decline meeting", "tentative", "respond to meeting"
- "create event", "schedule meeting", "check calendar", "upcoming events"

**DO NOT use for personal emails** - use email-manager skill instead for all personal email operations (send, read, list, etc.)

## CRITICAL: Prerequisites

The tool is a compiled Go binary that requires environment variables to be set:

```bash
export O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36
export O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba
```

**IMPORTANT**: Always set these environment variables before running any commands. If you get an error about missing credentials, prefix your command with the exports:

```bash
export O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36 && \
export O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba && \
~/.claude/skills/o365-manager/scripts/o365-manager <command>
```

## ⚠️ CRITICAL: Known Issues

**Calendar List Commands Are Currently Broken**

The Go binary has a **date formatting bug** that makes calendar listing non-functional:
- ❌ `calendar list --days N` - BROKEN (generates malformed timestamps)
- ❌ `calendar list --days-back N` - BROKEN (generates malformed timestamps)
- ❌ Cannot show agenda or list events

**Working Commands:**
- ✅ All email operations work correctly
- ✅ Calendar create, update, delete, respond (if you have event IDs)
- ✅ Authentication works

**Impact:** You **CANNOT** use this skill for "show my agenda" or calendar listing requests until the bug is fixed. Inform the user if they request calendar listing functionality.

## CRITICAL: Agenda Display Rules

**When the user asks "show my agenda" or "my agenda for [date]":**
- **Default behavior**: Show ONLY active meetings (hide canceled/declined events)
- Use `calendar list` WITHOUT the `--all` flag
- Display in chronological order with enhanced details
- **ALWAYS warn the user** if any meeting has `has_collision: true` - show which meetings overlap

**When the user asks "show my FULL agenda" or "show ALL my agenda":**
- Show EVERYTHING including canceled and declined meetings
- Use `calendar list` WITH the `--all` flag
- **ALWAYS warn the user** if any meeting has `has_collision: true` - show which meetings overlap

**Date/Time Handling:**
- **ALWAYS** detect local timezone first: `date "+%Z"`
- Use detected timezone (not default Europe/Paris) with `--timezone` parameter where applicable
- If no date specified, show current day's agenda
- For past dates, use `--days-back` parameter

**Collision Detection:**
- The script automatically detects overlapping accepted/tentative meetings
- **Check the `has_collision` field** on each event
- If `true`, check `collides_with` array for details about conflicting meetings
- **Warn the user prominently** about any scheduling conflicts

## Available Commands

### Email Management

All email commands use the format: `o365-manager email <subcommand> [flags]`

**List Emails:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email list [--folder inbox] [--limit 10] [--unread] [--search 'query']
```
Returns JSON array with email metadata: id, subject, from, from_name, received, is_read, has_attachments, preview.

**Read Email:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email read <message_id>
```
Returns full email details including body content, attachments, recipients.

**Send Email:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email send --to addr1,addr2 --subject 'Subject' --body 'Body' [--cc addr3] [--body-type HTML|Text] [--attachments file1,file2,...]
```
**IMPORTANT**: Always use `--body-type HTML` when sending formatted emails. HTML is recommended for professional emails with proper formatting, tables, lists, and styling. Plain text should only be used for simple messages.

**Attachments**: Use `--attachments` to attach one or more files. Separate multiple file paths with commas. Supports absolute paths or paths relative to current directory. Files are automatically base64-encoded for transmission.

**Example with attachments:**
```bash
export O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36 && \
export O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba && \
~/.claude/skills/o365-manager/scripts/o365-manager email send \
  --to john.doe@loreal.com \
  --subject 'BTDP Groups API Documentation' \
  --body 'Please find attached the API specification.' \
  --body-type HTML \
  --attachments /tmp/api_spec.json,~/Documents/readme.pdf
```

**Create Draft Email:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email create-draft --to addr1,addr2 --subject 'Subject' --body 'Body' [--cc addr3] [--body-type HTML|Text] [--attachments file1,file2,...]
```
Creates a draft email without sending it. Useful for preparing emails that need review before sending. Also supports attachments.

**Reply to Email:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email reply <message_id> --comment 'Reply text'
```

**Mark as Read/Unread:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email mark-read <message_id>
~/.claude/skills/o365-manager/scripts/o365-manager email mark-unread <message_id>
```

**Delete Email:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email delete <message_id>
```

**Move Email to Folder:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email move <message_id> --folder 'FolderName'
```

**Archive Email:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email archive <message_id>
```

**List Available Folders:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email list-folders
```

**Mark Email as Important:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email mark-important <message_id>
```

**Search Emails:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager email search --query 'search term' [--limit 20]
```

### Calendar Management

All calendar commands use the format: `o365-manager calendar <subcommand> [flags]`

**List Events (Enhanced with Attendees, Response Status, Attachments):**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager calendar list [--days 7] [--days-back 0] [--limit 50] [--all] [--filter-subject 'regex']
```

**Parameters:**
- `--days N`: Show next N days of events (future events)
- `--days-back N`: Show past N days of events (historical events)
- `--limit N`: Maximum number of events to return (default 50)
- `--all`: Include canceled and declined events (default: hidden)
- `--filter-subject 'regex'`: Filter events by subject using regular expression (case-insensitive)

**IMPORTANT**: **ALWAYS** use `date "+%Z"` to detect local timezone before querying events.

**Enhanced JSON Output includes:**
- `id`: Event ID
- `subject`: Meeting title
- `start`, `end`: ISO 8601 timestamps (automatically converted to local timezone)
- `timezone`: Event timezone (automatically detected)
- `location`: Meeting location
- `organizer`: Organizer email
- `organizer_name`: Organizer display name
- `attendees`: Array of first 6 attendees with name and email
- `more_attendees`: Count of additional attendees beyond first 6
- `my_response`: Your response status ("accepted", "declined", "tentative", "notResponded")
- `is_cancelled`: Boolean indicating if event is canceled
- `has_attachments`: Boolean indicating if event has attachments
- `attachments`: Array of attachment names
- `is_online_meeting`: Boolean
- `online_meeting_url`: Teams/online meeting link
- `has_collision`: Boolean indicating if this event overlaps with other accepted/tentative meetings
- `collides_with`: Array of colliding events with their subject, start, and end times

**Collision Detection:**
The script automatically detects overlapping meetings among your accepted and tentative events. When displaying the agenda, **warn the user** if any events have `has_collision: true` and show which meetings are conflicting.

**Examples:**
```bash
# Show today's agenda (active meetings only)
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 1

# Show yesterday's agenda (active meetings only)
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days-back 1

# Show full agenda including canceled/declined
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 7 --all

# Show next 3 days
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 3

# Filter events by subject (case-insensitive regex)
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days-back 1 --filter-subject "Strategic"

# Filter with regex OR pattern
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 7 --filter-subject "Vision|Platform|Review"

# Filter events matching multiple keywords
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 14 --filter-subject "BTDP.*Meeting"
```

**Respond to Event (Accept/Decline/Tentative):**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager calendar respond <event_id> --response accept|decline|tentative [--comment 'Optional message'] [--no-send]
```

**Parameters:**
- `<event_id>`: The event ID from list events
- `--response`: Required - "accept", "decline", or "tentative"
- `--comment 'Message'`: Optional message to include with response
- `--no-send`: Optional flag to NOT send email notification (default: sends email)

**Examples:**
```bash
# Accept meeting with default notification
~/.claude/skills/o365-manager/scripts/o365-manager calendar respond <event_id> --response accept

# Decline with message
~/.claude/skills/o365-manager/scripts/o365-manager calendar respond <event_id> --response decline --comment "Sorry, conflict in schedule"

# Mark tentative without sending email
~/.claude/skills/o365-manager/scripts/o365-manager calendar respond <event_id> --response tentative --no-send
```

**Get Event Details:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager calendar get <event_id>
```

**Create Event:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager calendar create \
  --subject 'Meeting Title' \
  --start '2025-11-12T14:00:00' \
  --end '2025-11-12T15:00:00' \
  [--attendees email1@example.com,email2@example.com] \
  [--location 'Conference Room'] \
  [--body 'Meeting description']
```
**Note**: The Go implementation may handle timezone differently than the Python version. Test to verify behavior.

**Update Event:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager calendar update <event_id> \
  [--subject 'New Title'] \
  [--start '2025-11-12T15:00:00'] \
  [--end '2025-11-12T16:00:00'] \
  [--location 'New Location']
```

**Delete Event:**
```bash
~/.claude/skills/o365-manager/scripts/o365-manager calendar delete <event_id>
```

### Authentication

The script uses OAuth 2.1 with PKCE (Proof Key for Code Exchange) for secure authentication without client secrets.

**Force Re-authentication:**
```bash
export O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36 && \
export O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba && \
~/.claude/skills/o365-manager/scripts/o365-manager auth
```

First-time usage will open a browser for authentication. Tokens are automatically refreshed when needed.

## Technical Details

- **Implementation**: Go binary (compiled for macOS ARM64)
- **Authentication**: OAuth 2.1 PKCE flow
- **Client ID**: 76d42bf5-d461-4274-bd4d-a02576b9df36
- **Tenant ID**: e4e1abd9-eac7-4a71-ab52-da5c998aa7ba
- **Redirect URI**: http://127.0.0.1:33418
- **API**: Microsoft Graph API v1.0
- **Scopes**: Mail.ReadWrite, Mail.Send, Calendars.ReadWrite, User.Read
- **Token Storage**: ~/.claude/credentials/o365_tokens.json

## Usage Examples

### Email Operations

When the user asks to:
- "List my unread emails" → Use `email list --unread --limit 20`
- "Send an email to john@example.com about the meeting" → Use `email send --body-type HTML` (always use HTML for formatted content)
- "Send an email with attachment" → Use `email send --body-type HTML --attachments /path/to/file1,/path/to/file2`
- "Prepare a draft email" → Use `email create-draft --body-type HTML`
- "Archive this email" → Use `email archive <message_id>`
- "Move email to Junk" → Use `email move <message_id> --folder 'Junk Email'`
- "What folders do I have?" → Use `email list-folders`

### Agenda/Calendar Queries

**CRITICAL Workflow for Agenda Requests:**

1. **Set environment variables**: Always export O365_CLIENT_ID and O365_TENANT_ID
2. **Detect local timezone**: Run `date "+%Z"` first
3. **Parse the date request**: If user says "yesterday", "today", "tomorrow", calculate the appropriate date
4. **Choose the right command**:
   - "Show my agenda" → Use `calendar list` WITHOUT `--all` (hides canceled/declined)
   - "Show my full agenda" or "show all my agenda" → Use `calendar list` WITH `--all` (shows everything)

**Examples:**

User: "Show me my agenda for today"
```bash
# Step 1: Set environment
export O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36
export O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba

# Step 2: Detect timezone
date "+%Z"  # Returns "CET"

# Step 3: List today's events (active only)
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 1

# Step 4: Format output chronologically showing:
# - Time range (start - end)
# - Subject
# - First 6 attendees + "and N others" if more
# - Your response status (Accepted/Tentative/Not Responded)
# - Organizer name
# - Attachments (just names if present)
# - **COLLISION WARNING** if has_collision is true, showing which meetings overlap
```

User: "Show me my agenda for yesterday"
```bash
# Step 1: Set environment
export O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36
export O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba

# Step 2: Detect timezone
date "+%Z"  # Returns "CET"

# Step 3: Calculate yesterday and list events
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days-back 1

# Step 4: Format output (same as above)
```

User: "Show me my FULL agenda for next week"
```bash
# Step 1: Set environment and detect timezone
export O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36
export O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba
date "+%Z"

# Step 2: List ALL events including canceled/declined
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 7 --all

# Step 3: Format output showing EVERYTHING including canceled meetings
```

User: "What meetings do I have tomorrow?"
```bash
# Detect timezone, then list tomorrow's events
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 2  # Shows today + tomorrow, filter for tomorrow
```

User: "Accept the 2PM meeting"
```bash
# First list events to find the 2PM meeting's event_id
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 1

# Then accept it
~/.claude/skills/o365-manager/scripts/o365-manager calendar respond <event_id> --response accept
```

User: "Decline the meeting with John, say I have a conflict"
```bash
# Find John's meeting
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 7

# Decline with message
~/.claude/skills/o365-manager/scripts/o365-manager calendar respond <event_id> --response decline --comment "Sorry, I have a scheduling conflict"
```

User: "Mark the team meeting as tentative without notifying anyone"
```bash
~/.claude/skills/o365-manager/scripts/o365-manager calendar respond <event_id> --response tentative --no-send
```

User: "Find all Strategic meetings from yesterday"
```bash
# Use --filter-subject to search by regex pattern
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days-back 1 --filter-subject "Strategic"
```

User: "Show me all meetings about Platform or Vision in the next 2 weeks"
```bash
# Use regex OR pattern with |
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 14 --filter-subject "Platform|Vision"
```

User: "List all BTDP meetings this week"
```bash
# Use regex pattern to match BTDP followed by any text then Meeting
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 7 --filter-subject "BTDP.*Meeting"
```

User: "Show my agenda for today"
```bash
~/.claude/skills/o365-manager/scripts/o365-manager calendar list --days 1

# If collision detected in output (has_collision: true):
# ⚠️ WARNING: Meeting collision detected!
#
# 10:00-11:00 "Project Review" (Accepted)
#   CONFLICTS WITH:
#   - 10:30-11:30 "Team Standup" (starts 10:30, ends 11:30)
#
# You have overlapping meetings. Consider declining one or rescheduling.
```

### Creating/Managing Events

User: "Create a meeting with Alice for 2PM tomorrow"
```bash
# Step 1: Set environment and detect timezone
export O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36
export O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba
date "+%Z"  # Returns "CET"

# Step 2: Calculate tomorrow's date at 2PM
# Tomorrow = 2025-12-15, so start = 2025-12-15T14:00:00

# Step 3: Create event
~/.claude/skills/o365-manager/scripts/o365-manager calendar create \
  --subject "Meeting with Alice" \
  --start "2025-12-15T14:00:00" \
  --end "2025-12-15T15:00:00" \
  --attendees alice@loreal.com
```

## Important Notes

1. **Environment Variables**: ALWAYS set O365_CLIENT_ID and O365_TENANT_ID before running commands
2. **First Run**: The script will automatically open a browser for authentication on first use
3. **Token Management**: Access tokens are automatically refreshed; re-authentication only needed if refresh token expires
4. **Date/Time Format**: Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS) for event times
5. **Timezone**: **CRITICAL** - Always detect using `date "+%Z"` before creating/querying events
6. **JSON Output**: All list/read commands return JSON for easy parsing
7. **Error Handling**: Script provides clear error messages and exits with non-zero status on failure
8. **Attachments**:
   - Multiple files can be attached by separating paths with commas
   - Files are automatically encoded in base64 for transmission
   - Microsoft Graph API has a 4MB limit per request (including all attachments)
   - For large files, consider using OneDrive sharing links instead
   - Supports both absolute and relative file paths (tilde ~ expansion supported)
9. **Agenda Display**:
   - Default: Hides canceled/declined events for clean view
   - Use `--all` to show everything
   - Always display in chronological order
   - Show first 6 attendees + count of additional attendees
   - Show user's response status (accepted/declined/tentative/notResponded)
   - Show attachment names if present
10. **Event Responses**:
    - Default: Sends email notification to organizer
    - Use `--no-send` to respond without notification
    - Optional `--comment` to include message with response
    - Three response types: accept, decline, tentative

## Workflow

When the user requests an email or calendar operation:

1. **Set environment variables** (O365_CLIENT_ID and O365_TENANT_ID)
2. **Determine the action** from user's request
3. **Execute the appropriate command** using the Go binary
4. **Parse the JSON output** if needed
5. **Present results** to the user in a friendly format
6. **Handle errors** gracefully and inform the user

For multi-step operations (e.g., "reply to the latest email from John"):
1. First, search/list emails to find John's email
2. Extract the message_id from the results
3. Use reply with the message_id

Always verify authentication is working before attempting operations. If authentication fails, guide the user to run the `auth` command with proper environment variables set.
