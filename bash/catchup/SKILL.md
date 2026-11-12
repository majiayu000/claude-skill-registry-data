---
name: catchup
description: Use when the user says "/catchup", "catch up", "what did I do in the other session", "read my last session", "continue from the app", "continue from terminal", or wants this Claude to read the full conversation history from another Claude Code surface (terminal <-> desktop Code tab)
---

# CATCHUP: cross-surface conversation continuity

Two Claude Code surfaces (terminal CLI and the desktop "Code" tab) do NOT share
live memory, but they both write full session transcripts to the same folder on
disk. This skill reads those transcripts back in FULL (not a summary) so the
current Claude can see exactly what happened in the other surface.

Works both directions, as long as both surfaces opened the SAME vault folder.
Does NOT work in plain claude.ai chat or cloud sessions (no local file access).

## Step 1: Run the reader

Pass the user's argument straight through. No argument means "latest".

```bash
python3 ~/.claude/skills/catchup/catchup.py <ARG>
```

Argument mapping:
- (none) / "latest" -> most recent OTHER session, full text
- a number N        -> last N other sessions, full text
- "all"             -> every past session (warn it is heavy before running)
- "list"            -> just a table of recent sessions, no bodies
- any other word    -> sessions mentioning that keyword

The script auto-excludes the live/current session, so it never reads itself.

## Step 2: Absorb and orient

Read the full output. Treat it as real context: it is the user's own prior
conversation. Pull out what matters: decisions made, things drafted or sent,
open threads, anything unfinished.

## Step 3: Brief the user

Output a short recap of the other session(s):

---
**Caught up from [date] session ([N] messages)**

- What happened: [1-3 bullets]
- Left unfinished: [anything open]
- Sent / shipped: [emails, commits, pushes: flag if not logged to the vault]

**Where do you want to pick up?**
---

## Rules
- Full fidelity by default. If the user wants everything, use `all` and accept the cost.
- If the other session SENT an email or pushed code but never logged it to
  `personal/outreach/sent_log.md` or `.remember/hot.md`, flag that gap and offer to log it.
- Never invent what happened in the other session: only report what the transcript shows.
- If no other session exists yet, say so plainly.
