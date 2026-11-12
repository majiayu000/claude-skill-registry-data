---
name: daily
description: Use when the user says "good morning", "start the day", "daily", "what is today", "morning briefing", "what should I focus on", "daily note", or "today's priorities"
---

# /daily: start the day

1. Open `daily/YYYY-MM-DD.md` for today, or create it.
2. List unsorted files in `inbox/` and flag them.
3. Scan `projects/` and every `*_tracker.md` for deadlines in the next 7 days or anything marked blocked.
4. Read `personal/tracker-staleness.md` (written nightly) and name trackers that went quiet.
5. Surface the top 3 priorities, then ask: "What are we working on today?"

## Automatic wiki upkeep (no need to ask)
- If `inbox/` has files, run /wiki to compile them.
- If `wiki/_index.md` shows no health check in 7+ days, run /wiki-health and include the report.
