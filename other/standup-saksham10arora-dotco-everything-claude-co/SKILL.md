---
name: standup
description: Use when the user says "/standup", "standup", "stand-up", "daily standup", "what did I do yesterday", "what am I doing today", "what are my blockers", or wants a quick standup summary
---

# /standup: the 60-second standup briefing

Read in parallel:
1. `daily/<yesterday>.md`: what was done yesterday
2. `daily/<today>.md`: what is planned for today
3. `.remember/hot.md`: active projects, tracks, hard rules (blockers live here)

Date arithmetic: yesterday = today - 1 calendar day. Use ISO format `YYYY-MM-DD` for filenames.

## Output (exactly this, no intro)

**STANDUP: <date>**

### Yesterday
One bullet per item found in yesterday's daily note. If the file is missing: "No note for <date>."

### Today
One bullet per item found in today's daily note. If the file is missing: "No note for <date>."

### Blockers
One bullet per blocker found across today's daily note and `.remember/hot.md`. If none appear: "None."

## Rules
- Never invent items. Every bullet must trace directly to text in one of the three files.
- Do not summarise, paraphrase beyond light clean-up, or merge items from different files.
- If a file does not exist, say so in one line and move on. Do not error.
- Keep each bullet to one line; drop markdown formatting noise (extra `#`, `---` dividers).
- Do not add commentary, greetings, or follow-up questions after the three sections.

