---
name: weekly
description: Use when the user says "/weekly", "weekly review", "weekly", "review my week", "what shipped this week", "Sunday review", or "what slipped"
---

# /weekly: the Sunday review

Read in parallel, then stop reading once you have what you need:
1. `daily/<date>.md` for the last 7 dates, today included, skipping any file that does not exist
2. `.remember/hot.md` for deadlines and active projects

Only open a tracker (`*_tracker.md`) if hot.md lacks the detail. Never read big trackers by default.

## Output (exactly this, no intro)

**WEEKLY: <start date> to <end date>**

### Shipped
One line per thing finished this week, taken from the daily notes. If none: "Nothing logged as shipped".

### Slipped
One line per item that was planned in the daily notes or due this week and is not done. Name the file it came from.

### Next week's deadlines
Date | What | Status, from hot.md for the next 7 days. If none: "None this week".

### One thing to drop
One item from the slipped list or active projects that is worth stopping, with a one-line reason.

**What do you want to start with next week?**

## Rules
- Never invent a status or deadline. If it isn't in the files, say "unknown, check <file>".
- If fewer than 7 daily notes exist, say how many were found.
- If hot.md was last updated more than 2 days ago, say so.
- At the end of the review, remind the user to run /tldr.
