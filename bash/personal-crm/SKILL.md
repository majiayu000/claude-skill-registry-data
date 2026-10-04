---
name: personal-crm
description: "Personal CRM built on monday.com. Tracks contacts, last interactions, next meetings, and topics. Runs daily to update from Calendar + email. Delivers pre-meeting briefings as part of morning-briefing. Use when: someone asks about a contact, before a meeting, or during daily CRM sync."
---

## Load Local Context
```bash
CONTEXT_FILE="/path/to/workspace/skills/personal-crm/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Then use: $CRM_BOARD_ID, $OWNER_EMAIL, etc.
```

# Personal CRM Skill

CRM נבנה על monday.com — ללא integrations חדשות. מבוסס על Calendar API + gog Gmail.

---

## Board Structure

- *Board:* Personal CRM — the owner (ID in .context)
- *Columns:* Name | Email | Phone | Role | Last Contact | Next Meeting | Relationship | Notes | Last Topic
- *Groups:* Leadership | Team | External

---

## Daily CRM Sync (run as part of morning-briefing or standalone cron)

### Step 1 — Fetch today's calendar events
```bash
# Use Calendar API directly (gog CLI auth is broken — use credentials.json)
# See calendar-setup skill for full auth flow
ACCESS_TOKEN=$(...)  # refresh from /path/to/openclaw/.gog/credentials.json

TODAY=$(date -u +%Y-%m-%d)
TOMORROW=$(date -u -d '+1 day' +%Y-%m-%d 2>/dev/null || date -u -v+1d +%Y-%m-%d)

curl -s "https://www.googleapis.com/calendar/v3/calendars/netanelab%40monday.com/events?timeMin=${TODAY}T00:00:00Z&timeMax=${TOMORROW}T00:00:00Z&singleEvents=true&orderBy=startTime" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Step 2 — For each meeting attendee
1. Search CRM board by name/email
2. If found → update "Last Contact" to today, update "Last Topic" with meeting title
3. If not found → create new contact item
4. If meeting is upcoming (>now) → update "Next Meeting" date

### Step 3 — Update monday.com
```
Use change_item_column_values tool:
- date_mm242bkk = Last Contact date
- date_mm24fnmn = Next Meeting date  
- text_mm24jwh8 = Last Topic (meeting title / email subject)
```

---

## Pre-Meeting Briefing

Run before each meeting (integrate into morning-briefing skill):

For each meeting today with external attendees:
1. Fetch contact from CRM board
2. Pull: Last Contact, Last Topic, Notes, Role
3. Format briefing:

```
📋 Meeting Prep: [Meeting Title] at [TIME]

Attendees:
• [Name] — [Role]
  Last spoke: [Last Contact date] | Topic: [Last Topic]
  Notes: [Notes field]
  [No history] if first time
```

Send to the owner via WhatsApp before the meeting (30 min prior if possible).

---

## Manual Query

When the owner asks "מה אני יודע על X" or "מתי דיברתי עם X":
1. Search CRM board by name (use get_board_items_page with searchTerm)
2. Return: Role, Last Contact, Next Meeting, Last Topic, Notes
3. If not in CRM → say so, offer to add

---

## Adding a New Contact

When a new person appears in meetings or email:
1. Create item in board with: Name, Email/Phone (if known), Role
2. Set Last Contact = today
3. Set Last Topic = how they were encountered (meeting title or email subject)

---

## Cron Setup

Add to morning-briefing or as standalone:
```bash
openclaw cron add \
  --name "crm-daily-sync" \
  --every 24h \
  --session isolated \
  --message "Run personal-crm skill: sync today's calendar events to CRM board, update Last Contact and Next Meeting for all attendees. If new contacts found, add them. Silent if no changes." \
  --timeout-seconds 120
```

---

## .context File Template

```bash
# personal-crm/.context
CRM_BOARD_ID="18407279559"
OWNER_EMAIL="owner@company.com"
OWNER_PHONE="+1234567890"
GOG_CREDS="/path/to/openclaw/.gog/credentials.json"

# Column IDs
COL_EMAIL="email_mm24sjhq"
COL_PHONE="phone_mm244na6"
COL_ROLE="text_mm24dn6c"
COL_LAST_CONTACT="date_mm242bkk"
COL_RELATIONSHIP="color_mm24z8s8"
COL_NOTES="long_text_mm24yvyb"
COL_NEXT_MEETING="date_mm24fnmn"
COL_LAST_TOPIC="text_mm24jwh8"
```

---

## Cost Tips
- Cheap: reading from monday.com board
- Calendar sync: once per day max (not per heartbeat)
- Pre-meeting briefing: only if meeting has external attendees
- No LLM needed for sync — only for generating briefing text
