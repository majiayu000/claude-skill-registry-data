---
name: reflect
description: End-of-day reflection — what worked, what surprised, message to tomorrow. Saves to running journal. Use when asked to "reflect", "end of day", "wrap up", "what did I do today".
---

# End-of-Day Reflection

Capture what matters before context fades. Takes 2 minutes. Builds a journal the morning kickoff and weekly retro can pull from.

## Process

1. **Show today's activity** — run `git log --since='12 hours ago' --oneline` to remind the user what they did
2. **Ask three questions** (one at a time, wait for each answer):

   > **What worked today?** (A decision, approach, or tool that paid off)

   > **What surprised you?** (Something unexpected — good or bad)

   > **What would you tell yourself tomorrow morning?** (Context you'll forget overnight)

3. **Save the reflection** — write to `docs/reflections/YYYY-MM-DD.md`:

```markdown
# Reflection — YYYY-MM-DD

**Commits today:** [count]
**Summary:** [2-3 sentence summary of git activity]

## What worked
[User's answer]

## What surprised me
[User's answer]

## Note to tomorrow
[User's answer]
```

4. **Create the directory** if `docs/reflections/` doesn't exist yet
5. **Close with one line** — "Saved. See you tomorrow." Don't over-narrate.

## Rules

- Ask questions ONE AT A TIME. Don't dump all 3 at once.
- Keep it conversational, not formal.
- If the user says "nothing" or gives short answers, that's fine. Save what they give.
- Don't add your own analysis or suggestions. This is their space.
- Don't commit the file — it's personal notes, not code.
