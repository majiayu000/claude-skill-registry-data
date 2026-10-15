---
name: meeting-minutes
description: "Turn meeting notes or a transcript into minutes with action items. Do NOT use for agendas (use meeting-agenda)."
---

# meeting-minutes

Converts raw meeting notes or transcript into structured minutes: attendees, key decisions, discussion summary, and action items with owners and due dates.

## Input

```json
{
  "meeting_type": "plc",
  "raw_notes": "Discussed reading data. [Teacher A] shared that 5 students below benchmark. Coach suggested switching to repeated reading for Tier 2 group. Team agreed to try for 4 weeks. [Teacher B] will pull small group during independent work time. Next meeting: review data.",
  "attendees": ["[Teacher A]", "[Teacher B]", "[Reading Coach]", "[AP]"]
}
```

## Output

```json
{
  "tool": "meeting-minutes",
  "minutes": {
    "meeting_type": "PLC",
    "date": "[Date]",
    "attendees": ["[Teacher A]", "[Teacher B]", "[Reading Coach]", "[AP]"],
    "key_decisions": [
      "Switch Tier 2 reading group to repeated reading intervention for 4-week trial"
    ],
    "discussion_summary": "Team reviewed reading benchmark data. Five students identified as below benchmark. Reading coach recommended repeated reading as a replacement intervention.",
    "action_items": [
      {"action": "Begin repeated reading intervention with Tier 2 group", "owner": "[Teacher B]", "due": "Next week"},
      {"action": "Review 4-week data at follow-up PLC", "owner": "Team", "due": "4 weeks"}
    ]
  },
  "human_review_required": true
}
```

## Do NOT use this atom for
- Creating agendas (use meeting-agenda)
- Recording meetings (this summarizes existing notes)
- IEP meeting minutes with legal requirements (use district templates)

## Pipeline note
Follows `references/method.md` at the Generation step (minutes composition). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — meeting participants should verify accuracy of decisions and action items.
