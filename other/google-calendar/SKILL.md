---
name: google-calendar
description: Use when scheduling, rescheduling, or canceling appointments via Google Calendar ג€” Sales agent bookings, Customer Service reminders, availability lookups. Covers the Calendar MCP server.
---

# Google Calendar skill

## When to invoke

- Sales agent booking initial consultations
- Customer Service sending appointment reminders
- Rescheduling / canceling existing appointments
- Checking advisor availability before suggesting times

## Available MCP tools

`list_calendars`, `list_events`, `get_event`, `create_event`, `update_event`, `delete_event`, `respond_to_event`, `suggest_time`.

**Prefer `suggest_time`** for finding open slots ג€” do not roll your own availability logic.

## Hard rules

1. **Always confirm timezone** ג€” Israel is `Asia/Jerusalem` (handle DST automatically via IANA tz, never hardcode UTC offset)
2. **Default appointment length**: 45 min for new consultations, 30 min for follow-ups (override only if customer requested)
3. **Buffer**: 15 min between back-to-back meetings ג€” respect when suggesting times
4. **Working hours**: Sunג€“Thu 09:00ג€“18:00, Fri 09:00ג€“13:00. No appointments on Shabbat or Israeli holidays unless explicitly approved by advisor
5. **Customer-facing event title in Hebrew**; description may mix Hebrew/English
6. **Always include**: customer name, phone, meeting type (Zoom link or office address), advisor name

## Reminder cadence (Customer Service agent)

- T-24h: WhatsApp reminder
- T-2h: WhatsApp reminder + confirmation request
- T-15min: only if customer hasn't confirmed ג†’ final reminder

## Reschedule / cancel flow

1. `get_event` to confirm current state
2. `update_event` (reschedule) or `delete_event` (cancel)
3. Log change to CRM
4. Notify customer in Hebrew with new details

## Error handling

Calendar API failure during booking ג†’ do NOT confirm to customer ג†’ escalate immediately. A "phantom" appointment is worse than no booking.