---
name: sidenote
description: "Park a passing thought as a later-task without derailing the current one — logged, not acted on. Use when the user says \"sidenote\", \"park this\", \"note that for later\", or drops an aside mid-task that should be recorded rather than acted on. Also use with no thought supplied to flush and list the open sidenotes."
---

# Sidenote

Park the thought the user just dropped as a sidenote. A sidenote is a *later-task*, not a *now-task*. Your job is to record it and keep going, nothing more.

**The contract — hold it exactly:**

- **Do not act on it.** Don't investigate it, don't open the files it mentions, don't add it to your current plan, don't answer the question it poses. It is parked, not pending.
- **Do not let it touch the current task.** Its scope, plan, priorities, and *pace* stay exactly as they were. In particular: **do not speed up or cut corners to "get to" the note.** The whole point of parking it is that it costs the current work nothing.
- **Urgency doesn't override the contract.** If the note reads as urgent ("prod is down", "this is broken"), that's the wrong channel — a real emergency is a normal interruption, not a sidenote. Still just log it and resume; the human will escalate directly if they meant to.

**Persist it so it survives this session** (context gets compacted; memory doesn't count as "logged"):

1. Append one entry to `.claude/sidenotes.md` at the project root — create the file (and `.claude/`) if missing. This is deliberately the same file every other agent on this machine parks to, so notes are visible no matter which tool you were in when the thought landed.
2. Format — an open checkbox, the verbatim thought, then a one-line **anchor** so the note still makes sense when another session or agent reads it cold (the verbatim thought alone is full of "this / here / it" that dangles without the moment that produced it):

   ```
   - [ ] [<today's date, YYYY-MM-DD>] <the thought, captured verbatim>
     ↳ <task you were mid-way through> · <file/area the note points at, if "this"/"here" resolves to one> · <branch>@<short-sha>
   ```

   - **Thought — verbatim.** Don't paraphrase or "improve" it; capture what was said.
   - **Anchor — coordinates you already hold, not a research task.** Fill it only from what's already in front of you: the task in progress, the file/area currently in focus, the current branch and short SHA (already in your session's git context). **Do not open files, grep, or investigate the note's subject to complete it** — that would break the park contract. Any field you don't already know, omit. The anchor records where you were standing; it never sends you looking.

Then: **one-line acknowledgement** (e.g. `Parked in .claude/sidenotes.md — continuing.`) and **resume exactly where you left off**, as if the note had never arrived.

**If no thought was supplied** (the user just asked for a sidenote with nothing to park), there's nothing to record — treat it as a *flush*: read `.claude/sidenotes.md` and list the **open** entries back to the user so they can decide what to pick up. Open means *not checked off* — every entry except the ones marked done (`- [x]`), so older bullets without a checkbox still count. Change nothing, act on nothing, then resume. (Checking an item off to `- [x]` happens when it's actually handled — not part of parking or flushing.)
