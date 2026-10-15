---
name: meeting-agenda
description: "Create ONE meeting agenda from a purpose and attendee list. Do NOT use for minutes (use meeting-minutes)."
---

# meeting-agenda

Generates a structured meeting agenda with time allocations, discussion items, roles, and action-item placeholders. Adapts format to meeting type (PLC, IEP, faculty, parent conference, etc.).

## Input

```json
{
  "purpose": "Weekly PLC meeting — review student data and plan intervention adjustments",
  "meeting_type": "plc",
  "duration_minutes": 45,
  "attendees": ["3rd grade team (4 teachers)", "reading coach", "assistant principal"]
}
```

## Output

```json
{
  "tool": "meeting-agenda",
  "agenda": {
    "title": "3rd Grade PLC — Weekly Data Review",
    "date": "[Date]",
    "duration": "45 minutes",
    "items": [
      {"time": "5 min", "item": "Norms review and celebrations", "lead": "Team lead"},
      {"time": "15 min", "item": "Review running records and ORF data", "lead": "Reading coach"},
      {"time": "15 min", "item": "Identify students needing intervention adjustments", "lead": "All"},
      {"time": "5 min", "item": "Plan next steps and assign action items", "lead": "Team lead"},
      {"time": "5 min", "item": "Parking lot and adjournment", "lead": "Team lead"}
    ],
    "materials_needed": ["Student data reports", "Intervention tracking sheets"]
  },
  "human_review_required": true
}
```

## Do NOT use this atom for
- Meeting minutes or summaries (use meeting-minutes)
- Scheduling meetings (this creates the agenda, not the calendar event)
- IEP meeting agendas with legal timelines (those require district-specific templates)

## Pipeline note
Follows `references/method.md` at the Generation step (agenda creation). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — agenda items should be customized by the meeting facilitator.
