---
name: meetings
description: |-
  Schedule meetings, parse meeting notes, extract action items. Three distinct intents covered.
  Invoke when user mentions a specific meeting (past or future) by name or context.
  NOT for general calendar checks (use direct calendar.py), NOT for time-zone math.
  Triggers: "schedule with X", "minutes of the X meeting", "action items from yesterday's meeting",
  "prep me for meeting with X".
---

# Meetings Skill

## Minimum Model
Any model. For timezone reasoning or complex scheduling constraints, use a medium model.

## Trigger Phrases
- "schedule a meeting" / "set up a meeting with X" / "book a call with Y"
- "summarize meeting notes" / "take notes" / "action items from meeting" / "extract tasks from this transcript"

> ⚠️ CALENDAR AUTH: Do NOT use `gog` CLI — it's broken on this server. Use direct Google Calendar API with credentials from `/path/to/openclaw/.gog/credentials.json`. See calendar-setup skill for full auth pattern.

---

## Section 1 — Schedule a Meeting

End-to-end meeting coordination: find availability, contact the other PA, book the calendar invite.

### Step 1 — Understand the Request

Before acting, build a lightweight meeting contract:
- **Goal** — why this meeting should happen
- **Decision needed** — what should be clearer by the end
- **Constraints** — duration, timeframe, format, key attendees
- **Acceptance criteria** — what makes the scheduling/prep successful

Then confirm:
- **Who** to meet with
- **Duration** (default: 30 min if not specified)
- **Timeframe** ("this week", "next week", "mornings only", etc.)
- **Meeting type** (video, in-person, phone)

If the request is vague (e.g. "set up a call with Jane") → ask one clarifying question before proceeding.

---

### Step 2 — Find the Other PA

Check `data/pa-directory.json`:

```bash
python3 -c "
import json, sys
try:
    with open('data/pa-directory.json') as f:
        d = json.load(f)
except FileNotFoundError:
    print('ERROR: data/pa-directory.json not found')
    sys.exit(1)

name = 'PERSON_NAME'  # replace with actual name
matches = [p for p in d.get('pas', []) if name.lower() in p['owner'].lower()]

if not matches:
    print('No PA found for:', name)
else:
    for p in matches:
        print('PA:', p['name'], '| Phone:', p['phone'])
"
```

If no PA found → skip to Step 4 and contact the person directly by email.

---

### Step 3 — Check Owner's Availability

```bash
#!/bin/bash
TODAY=$(date -u +%Y-%m-%dT%H:%M:%SZ)
NEXT_WEEK=$(date -u -d '+7 days' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
  || date -u -v+7d +%Y-%m-%dT%H:%M:%SZ)

# BROKEN: replace with direct API call — see calendar-setup skill
# ACCESS_TOKEN: use refresh_token flow from /path/to/openclaw/.gog/credentials.json
GOG_ACCOUNT=owner@company.com gog calendar events primary \
  --from "$TODAY" \
  --to "$NEXT_WEEK" \
  2>/dev/null \
  | python3 -c "
import sys, json
try:
    events = json.load(sys.stdin)
except:
    events = []

print('Upcoming events:')
for e in sorted(events, key=lambda x: x.get('start', {}).get('dateTime', '')):
    start = e.get('start', {}).get('dateTime', '')[:16].replace('T', ' ')
    print(' ', start, '—', e.get('summary', 'Untitled'))
"
```

**Find free slots automatically:**

```python
#!/usr/bin/env python3
import subprocess, json, sys
from datetime import datetime, timedelta, timezone

OWNER_EMAIL = "owner@company.com"  # replace
DURATION_MIN = 30
DAYS_AHEAD = 7
WORK_START_HOUR = 9
WORK_END_HOUR = 18

try:
    # BROKEN: replace with direct API call — see calendar-setup skill
    # ACCESS_TOKEN: use refresh_token flow from /path/to/openclaw/.gog/credentials.json
    result = subprocess.run(
        ['gog', 'calendar', 'events', 'primary',
         '--from', datetime.now(timezone.utc).isoformat(),
         '--to', (datetime.now(timezone.utc) + timedelta(days=DAYS_AHEAD)).isoformat()],
        env={'GOG_ACCOUNT': OWNER_EMAIL, 'PATH': '/usr/bin:/usr/local/bin:/bin'},
        capture_output=True, text=True, timeout=30
    )
    events = json.loads(result.stdout) if result.stdout.strip() else []
except Exception as e:
    print("Could not fetch calendar:", e)
    sys.exit(1)

busy = []
for e in events:
    start = e.get('start', {}).get('dateTime')
    end = e.get('end', {}).get('dateTime')
    if start and end:
        busy.append((start, end))

suggestions = []
for day_offset in range(1, DAYS_AHEAD + 1):
    day = datetime.now(timezone.utc) + timedelta(days=day_offset)
    if day.weekday() >= 5:
        continue
    for hour in range(WORK_START_HOUR, WORK_END_HOUR):
        slot_start = day.replace(hour=hour, minute=0, second=0, microsecond=0)
        slot_end = slot_start + timedelta(minutes=DURATION_MIN)
        if slot_end.hour > WORK_END_HOUR:
            continue
        conflict = any(
            slot_start.isoformat() < b[1] and slot_end.isoformat() > b[0]
            for b in busy
        )
        if not conflict:
            suggestions.append(slot_start)
        if len(suggestions) >= 5:
            break
    if len(suggestions) >= 5:
        break

if not suggestions:
    print("No slots found in the next 7 days during working hours.")
else:
    print(f"Available {DURATION_MIN}-min slots:")
    for s in suggestions:
        print(" •", s.strftime('%A %b %d'), "at", s.strftime('%H:%M'), "UTC")
```

---

### Step 4 — Contact the Other PA

Propose 3–5 specific slots:

```
"Hey [PA Name], [your owner] would like to meet [their owner] for [duration].
Slots that work:
• [Day Date] at [HH:MM TZ]
• [Day Date] at [HH:MM TZ]
• [Day Date] at [HH:MM TZ]
Do any work? Or what times work best?"
```

If no response within 2 hours on a business day → follow up once.
If still no response after 4 hours → tell owner and suggest direct contact.

---

### Step 5 — Book the Meeting

Once both sides agree:

```bash
# BROKEN: gog calendar create is unavailable — use the Python alternative below
GOG_ACCOUNT=owner@company.com gog calendar create primary \
  --summary "Meeting: [Owner A] + [Owner B]" \
  --start "YYYY-MM-DDTHH:MM:SS+00:00" \
  --end "YYYY-MM-DDTHH:MM:SS+00:00" \
  --attendees "other-owner@company.com" \
  --description "Scheduled via PA coordination"
```

For video calls, add:
```bash
  --description "Video call: https://meet.google.com/xxx-xxxx-xxx"
```

**✅ Working alternative — Create calendar event via direct API:**

```python
# Create calendar event via direct API
import json, requests
from datetime import datetime, timezone

# Get access token (see auth pattern in calendar-setup skill)
with open('/path/to/openclaw/.gog/credentials.json') as f:
    creds = json.load(f)
owner = next(a for a in creds['accounts'] if a['type'] == 'owner')
resp = requests.post('https://oauth2.googleapis.com/token', data={
    'client_id': owner['client_id'],
    'client_secret': owner['client_secret'],
    'refresh_token': owner['refresh_token'],
    'grant_type': 'refresh_token'
})
access_token = resp.json()['access_token']

event = {
    "summary": MEETING_TITLE,
    "start": {"dateTime": START_ISO, "timeZone": "Asia/Jerusalem"},
    "end": {"dateTime": END_ISO, "timeZone": "Asia/Jerusalem"},
    "attendees": [{"email": ATTENDEE_EMAIL}],
    "description": DESCRIPTION
}

resp = requests.post(
    f"https://www.googleapis.com/calendar/v3/calendars/netanelab%40monday.com/events",
    headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
    json=event
)
event_id = resp.json().get('id')
print(f"Event created: {event_id}")
```

---

### Step 6 — Confirm Both Sides

```
To your owner:
"✅ Done — [Date] at [Time] with [Person]. Calendar invite sent."

To the other PA:
"✅ Invite sent to [Their Owner] for [Date] [Time]. Let me know if anything changes."
```

### Quick Templates

| Situation | Template |
|---|---|
| Initial request | "Hey [PA], [Owner A] wants to connect with [Owner B] for ~30 min [this/next] week. What works?" |
| Propose slots | "Here are 3 options: [A], [B], [C]. Any work?" |
| Confirm | "✅ Booked for [time]. Invite sent to [email]." |
| Reschedule | "[Owner] can't make [time]. Can we try [alternative]?" |
| Cancel | "[Owner] needs to cancel [time]. Apologies." |

### Rescheduling

```bash
# BROKEN: replace with direct API call — see calendar-setup skill
# ACCESS_TOKEN: use refresh_token flow from /path/to/openclaw/.gog/credentials.json

# Find the event
GOG_ACCOUNT=owner@company.com gog calendar events primary \
  --from "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --to "$(date -u -d '+14 days' +%Y-%m-%dT%H:%M:%SZ)"

# BROKEN: replace with direct API call — see calendar-setup skill
# ACCESS_TOKEN: use refresh_token flow from /path/to/openclaw/.gog/credentials.json
# Delete old event: DELETE https://www.googleapis.com/calendar/v3/calendars/netanelab%40monday.com/events/{EVENT_ID}
GOG_ACCOUNT=owner@company.com gog calendar delete primary EVENT_ID

# Re-coordinate and create new event
```

---

## Section 2 — Meeting Notes & Action Items

Paste any meeting notes, transcript, or text → get a clean summary with action items, owners, and deadlines.

### Response Format (MANDATORY — One Message Only)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 [MEETING TITLE] — [YYYY-MM-DD]
Duration: [X min] | Attendees: [Names]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY
[2-3 sentence overview]

⚡ ACTION ITEMS ([X] of [Total])
1. [ ] @Owner: Task — Deadline
2. [ ] @Owner: Task — Deadline
3. [ ] @Owner: Task — Deadline

✅ KEY DECISIONS
• Decision 1
• Decision 2

📎 Saved: meeting-notes/YYYY-MM-DD_topic-name.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Add to your to-do list?
• "all" — Add all [X] items
• "1,2,4" — Add specific items
• "none" — Skip
```

**Rules:**
- ONE message only — never split into multiple
- Filename format: `YYYY-MM-DD_topic.md` (date first, always)
- Always show numbered action items
- Always include the to-do prompt if action items exist

### What to Extract

| Section | Description |
|---------|-------------|
| **Summary** | 2-3 sentence overview |
| **Action Items** | `- [ ] @Owner: Task — Deadline` |
| **Decisions** | What was agreed upon |
| **Open Questions** | Unresolved items |
| **Next Steps** | What happens after this meeting |

### File Storage

Save all meeting notes to `meeting-notes/YYYY-MM-DD_topic.md`:

```markdown
---
date: YYYY-MM-DD
title: Meeting Title
attendees: [Name1, Name2]
source: pasted notes | transcript | email
---

# Meeting Title

## Summary
[2-3 sentences]

## Action Items
- [ ] **@Owner**: Task description — *Deadline*

## Decisions
- Decision 1

## Open Questions
- Question 1

<details>
<summary>📝 Raw Notes</summary>
[Original input preserved]
</details>
```

### To-Do List Integration

After extracting action items:
- "all" → Add all items to `todo.md`
- "1,3,5" → Add specific items
- "none" → Skip

File: `todo.md` in workspace root. Organized by: Overdue → Due Today → This Week → No Deadline → Completed.

### Referencing Previous Meetings

Ask things like:
- "What did we decide about the budget?" → search `meeting-notes/` Decisions sections
- "What action items does @Sarah have?" → search for `@Sarah` across all files
- "Show me last week's meetings" → list files from date range

### Edge Cases

| Situation | Action |
|---|---|
| Very short notes | Still extract what's there |
| No clear topic | Ask: "What should I call this meeting?" |
| Multiple meetings in one paste | Ask if they should be separated into files |
| Not meeting notes | Still extract actionable items; adjust filename |

---

## Cost Tips

- **Scheduling:** Cheap — any small model works for slot-finding and coordination.
- **Notes extraction:** Medium model recommended for complex transcripts with many action items.
- **Batch:** Propose 3–5 slots at once instead of one at a time.
- **Don't re-fetch calendar repeatedly** — fetch once, extract 5 slots, propose them all.
