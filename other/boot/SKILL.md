---
name: boot
description: Use when the user says "/boot", "start session", "boot up", "what's the situation", or starts a session wanting a full briefing
---

# /boot: the 30-second session briefing

Read in parallel, then stop reading once you have what you need:
1. `.remember/hot.md`: deadlines, active projects, tracks, hard rules
2. `daily/<today>.md` if it exists

Only open a tracker (`*_tracker.md`) if hot.md lacks the detail. Never read big trackers by default.

## Output (exactly this, no intro)

**BOOT: <date>**

### Kill list (hard deadlines in the next 7 days)
Date | What | Status. If none: "None this week".

### Active projects
One line each: name, status, what's left.

### Tracks
One line per track from hot.md: where you are, what's next.

### Today
Daily note headline, or "No daily note. Create one?"

**What are we doing?**

## Rules
- Load the "Hard rules" section of hot.md into working memory and never break them.
- Never invent a status or deadline. If it isn't in the files, say "unknown, check <file>".
- If hot.md was last updated more than 2 days ago, say so.
- At the end of the session, remind the user to run /tldr.
