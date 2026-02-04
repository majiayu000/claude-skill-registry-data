---
name: office:calendar-management
description: Manage calendar events, check conflicts, handle scheduling from emails. Use when adding events or coordinating meetings to ensure proper timezone handling and conflict detection.
---

# Calendar Management with Office Admin

## When to Use This Skill

Use this skill when:
- Adding events from emails
- Checking for scheduling conflicts
- Creating calendar holds for tentative events
- Converting timezones for international contacts
- Managing working hours and availability
- Blocking focus time or recurring events

## User Calendar Preferences

Load preferences from `~/.claude/office-admin-config.json`:

```json
{
  "personal": {
    "timezone": "America/Chicago",
    "workingHours": {
      "start": "09:30",
      "end": "16:30",
      "lunchStart": "12:00",
      "lunchEnd": "13:30"
    }
  },
  "calendar": {
    "defaultDuration": 30,
    "bufferMinutes": 15,
    "schedulingLink": "https://user.cal.com/schedule",
    "autoAddFromEmail": true,
    "eventNaming": {
      "includeLocation": true,
      "includeAttendees": false
    }
  }
}
```

## Core Principles

1. **Always check conflicts first** - Before committing to an event
2. **Respect working hours** - Use user's configured schedule
3. **Handle timezones carefully** - Convert accurately, show both zones
4. **Be proactive** - Auto-add events from emails when configured
5. **Use descriptive titles** - Include location/context per user preference

## Adding Events from Emails

### Step 1: Extract Event Details

Look for in the email:
- **Date and time** (or phrases like "tomorrow", "next Tuesday", "in two weeks")
- **Duration** (or use defaultDuration from config)
- **Location** (physical address, restaurant name, virtual link)
- **Event type** (meeting, lunch, coffee, party, etc.)
- **Attendees** (who else is invited)
- **Special notes** (dress code, what to bring, etc.)

### Step 2: Parse Relative Dates

Handle conversational dates:
- "tomorrow" → current date + 1 day
- "next Monday" → next occurrence of Monday
- "in two weeks" → current date + 14 days
- "Dec 5" → December 5 of current year (or next if passed)

### Step 3: Check Calendar for Conflicts

BEFORE creating the event:

```bash
# Get user's calendar for that date
mcp__pd__google_calendar-list-events(
  instruction="Get all events for [date], between [start_time - bufferMinutes] and [end_time + bufferMinutes]"
)
```

Look for:
- Direct conflicts (overlapping times)
- Buffer violations (< bufferMinutes between events)
- Lunch conflicts (check workingHours.lunch* from config)
- End-of-day violations (past workingHours.end)

### Step 4: Report Availability

Tell the user:

**If free:**
```
You're free at [time] on [date].
```

**If conflict exists:**
```
That conflicts with:
- [event name] from [start] to [end]

Your schedule that day:
9:30am - 10:30am: Team standup
10:30am - 12:00pm: FREE
12:00pm - 1:30pm: Lunch
1:30pm - 3:00pm: [Proposed event would go here]
3:00pm - 4:00pm: Client call
```

### Step 5: Create the Event

If user confirms or no conflict exists:

```bash
mcp__pd__google_calendar-create-event(
  instruction="Create event with:
  - Title: [descriptive title with location if includeLocation=true]
  - Date: [YYYY-MM-DD]
  - Start time: [HH:MM] [timezone]
  - End time: [HH:MM] [timezone]
  - Location: [physical address or link]
  - Description: [context about who invited, what it's about]
  - Attendees: [email addresses]
  "
)
```

**Title format examples:**
- If `includeLocation: true`: "Lunch with Mike at Soho House"
- If `includeLocation: false`: "Lunch with Mike"
- If `includeAttendees: true`: "Meeting with Mike, Sarah, John"

**Timezone:** Always use user's timezone from config unless explicitly scheduling with someone in another timezone.

### Step 6: Confirm Addition

Provide:
- Event summary
- Calendar link for verification
- Note any adjustments made (e.g., moved 15min earlier to respect buffer)

## Handling Tentative Events

For events pending confirmation:

1. **Create with "HOLD:" prefix**
   ```
   Title: "HOLD: Call with Jean (pending confirmation)"
   ```

2. **Add note in description**
   ```
   Description: "(pending confirmation) Call with Jean Labuschagne about consulting opportunity"
   ```

3. **Update when confirmed**
   - Remove "HOLD:" prefix
   - Update description to remove "pending" note

4. **Delete if falls through**
   - Remove the calendar event
   - Log in CRM why it didn't happen (if tracking deals)

## Timezone Handling

### For Same-Timezone Contacts

Use user's timezone from config:
```
Time: 2:00 PM America/Chicago
```

### For Different-Timezone Contacts

When scheduling with someone in another timezone:

1. **Specify both timezones in email:**
   ```
   "How about 9am Chicago time (4pm Zurich)?"
   ```

2. **Double-check conversion:**
   - Look up their timezone
   - Calculate offset from user's timezone
   - Verify conversion is correct
   - Account for DST differences

3. **Common international contacts:**
   Keep a mental note of frequent timezone conversions:
   - US East Coast: +1 hour from Chicago (America/New_York)
   - UK: +6 hours from Chicago (Europe/London)
   - Central Europe: +7 hours from Chicago (Europe/Zurich)
   - Tokyo: +15 hours from Chicago (Asia/Tokyo)

4. **Create event in user's timezone:**
   ```
   Title: "Call with Jean in Zurich"
   Time: 9:00 AM America/Chicago
   Description: "9am Chicago / 4pm Zurich - Call with Jean Labuschagne"
   ```

## Working Hours Awareness

### Checking Availability

When someone asks "when are you free?":

1. Check user's workingHours from config
2. Look for gaps between existing events
3. Respect bufferMinutes between meetings
4. Avoid scheduling during lunch hours
5. Prefer morning or afternoon blocks

### Typical Day Structure

Based on config defaults:
```
9:30am - Start of working day
    ↓
[Morning block for meetings/work]
    ↓
12:00pm - 1:30pm - Lunch (avoid scheduling)
    ↓
[Afternoon block for meetings/work]
    ↓
4:30pm - End of working day
```

### Buffer Management

Apply bufferMinutes (default: 15) between events:
```
10:00am - 11:00am: Meeting A
[15 min buffer]
11:15am - 12:00pm: Meeting B
```

Don't schedule back-to-back unless user explicitly requests.

## Recurring Events

For recurring events (weekly standups, monthly check-ins):

```bash
mcp__pd__google_calendar-create-event(
  instruction="Create recurring event:
  - Title: [name]
  - Frequency: [daily/weekly/monthly]
  - Day: [Monday, Tuesday, etc. for weekly]
  - Time: [HH:MM]
  - Duration: [minutes]
  - Until: [end date or 'indefinitely']
  "
)
```

## Focus Time / Blocking

For work blocks or focus time:

```bash
mcp__pd__google_calendar-create-event(
  instruction="Create focus time block:
  - Title: 'Focus Time' or 'Deep Work'
  - Mark as: Busy
  - Visibility: Private (optional)
  - Duration: [typically 2-4 hours]
  - Recurring: [if regular pattern]
  "
)
```

## Integration with Email Skill

When email-management skill sees scheduling language:

1. **Extract event details**
2. **Call this skill to check conflicts**
3. **Report back to email skill**
4. **Email skill includes availability in draft response**
5. **This skill creates event once confirmed**

Seamless handoff between skills.

## Common Scenarios

### Scenario 1: Lunch Invitation
```
Email: "Want to grab lunch next Tuesday?"

1. Check calendar for next Tuesday
2. Check lunch hours (12:00-1:30pm from config)
3. Look for conflicts in that window
4. Report: "You're free for lunch on Tuesday Dec 5"
5. Create tentative hold
6. Once confirmed, create proper event with restaurant location
```

### Scenario 2: Meeting Request with Multiple Options
```
Email: "Can we meet Monday or Tuesday afternoon?"

1. Check both Monday and Tuesday afternoons
2. Identify all free slots after lunch
3. Report: "You're free:
   - Monday 2:00pm-4:30pm
   - Tuesday 1:30pm-3:00pm, 4:00pm-4:30pm"
4. Let user choose
5. Create event for chosen slot
```

### Scenario 3: International Call
```
Email from Switzerland: "9am your time?"

1. Confirm user's timezone (America/Chicago)
2. Calculate Switzerland time (4pm CET)
3. Check 9am Chicago for conflicts
4. Report availability
5. Create event with both timezones in description
```

## Common Mistakes to Avoid

### ❌ Not Checking Conflicts
**Problem:** Double-booking user
**Solution:** ALWAYS check calendar before confirming availability

### ❌ Wrong Timezone
**Problem:** Event created in wrong timezone, user misses meeting
**Solution:** Use timezone from config, verify conversions carefully

### ❌ Ignoring Buffers
**Problem:** Back-to-back meetings with no break
**Solution:** Apply bufferMinutes between events

### ❌ Scheduling During Lunch
**Problem:** Booking meetings during lunch hours
**Solution:** Check workingHours.lunchStart/End from config

### ❌ Vague Event Titles
**Problem:** "Meeting" with no context
**Solution:** Include who, what, where based on eventNaming preferences

### ❌ Forgetting to Create Holds
**Problem:** User verbally commits but event not tracked
**Solution:** Always create HOLD events for tentative commitments

## Integration Checklist

Before completing a calendar task:

- [ ] Loaded user's calendar preferences from config
- [ ] Checked for conflicts with sufficient buffer
- [ ] Verified timezone is correct
- [ ] Respected working hours and lunch time
- [ ] Used descriptive event title per preferences
- [ ] Added location if includeLocation enabled
- [ ] Included relevant attendees
- [ ] Added context in description
- [ ] Confirmed event was created successfully
- [ ] Provided calendar link to user

## Success Criteria

You're managing calendar well when:
- No double-bookings occur
- User has appropriate buffers between meetings
- Timezone conversions are accurate
- Event titles are clear and helpful
- Working hours are respected
- Conflicts are caught before committing
- Integration with email is seamless

## Remember

Calendar management is about protecting user's time and making scheduling effortless. Be proactive, be accurate, and always check conflicts first.
