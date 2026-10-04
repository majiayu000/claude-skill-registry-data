---
name: today
description: Daily planning - morning (fill journal, plan focus) or evening (close-out, prep tomorrow)
argument-hint: "[morning | evening]"
---

# Plan Today

You help the user run a morning ritual (plan focus items) or an evening ritual (close-out and prep tomorrow). Both modes write to the daily journal and to `Dashboard/tasks.md`.

## Mode selection

Check `$ARGUMENTS`:
- `morning` (or no argument before 4 PM local time): morning mode
- `evening` (or no argument after 4 PM local time): evening mode

If unclear, ask the user once: "Morning planning or evening close-out?"

---

## Morning mode

### Phase 1: Parallel data gather (no user interaction)

Do ALL of these before asking anything:

- Check if `journals/YYYY/MM-Month/DD-MM-YYYY.md` exists (month folder format: `02-February`).
- Read yesterday's journal: mood, energy, activities, "Tomorrow I start with" (if filled).
- If today's journal doesn't exist, create it from `templates/daily-note.md`.
- Read `Dashboard/tasks.md` - extract the "This week" section.
- Read `Dashboard/Weekly P-Tasks.md` - extract the current week's P-tasks.

### Phase 2: Personal questions (one AskUserQuestion, 3-4 questions)

Use yesterday's values as hints.

1. **Mood** (1-10) - hint with yesterday's mood.
   Options: "3-4 (rough)", "5-6 (okay)", "7-8 (good)", "9-10 (great)"
2. **Energy** (1-10) - hint with yesterday's energy.
   Options: "3-4 (low)", "5-6 (medium)", "7-8 (high)", "9-10 (full power)"
3. **Self-care**: "What did you do for yourself before work?"
   Options: "Exercise / run", "Walk", "Nothing special"
4. **Yesterday evening**: "How was yesterday after work?"
   Options: "Relaxing, no stress", "Active (workout / outing)", "Stressful / tough"

Update the journal's frontmatter `mood` and `energy`, and fill yesterday + today personal sections.

If mood < 6 or energy < 6: set `low_energy = true`.

### Phase 3: Calendar + focus planning (one round)

Ask the user to paste their calendar for the day (screenshot or text list).

After receiving the calendar:
- Extract meetings, calculate meeting time, calculate focus time, flag if >50% of the day is in meetings.
- Synthesize a daily plan from `Dashboard/tasks.md` "This week", current P-tasks, and calendar deadlines.

**Suggest max 3 focus items** for "My focus today (max 3)":
- If yesterday's "Tomorrow I start with" was filled, use it as the first focus item.
- Prioritize: hard deadlines > P1 tasks > meetings needing prep > overdue items.
- Focus items should be outcome-oriented (what you'll FINISH, not just work on).

**Capacity rules:**
- `low_energy`: max 2 focus items.
- >50% meetings: reduce focus count.
- Both: 1 focus item.

Present the plan and ask: "Anything to change? If OK, I'll update your journal and mark tasks as today's focus."

### Phase 4: Apply (no interaction)

- Fill "My focus today (max 3)" in the journal.
- For each focus item, if it corresponds to an entry in `Dashboard/tasks.md`, add ` 🎯` to the end of that line (marker meaning "today's focus"). Skills and the user can read this marker to spot today's work at a glance.
- Ensure frontmatter `mood` and `energy` are set.

### Phase 5: Morning summary

Write a short conversational summary, **not** a code-fenced template card. Two or three sentences max. Cover: day/date + mood/energy, the focus item(s) in plain prose, how many tasks got the 🎯 marker, a backtick-wrapped path to the updated journal, and a one-line nudge to run `/today evening` later.

Example tone (do not copy verbatim):

> Planning done for Tuesday, 21 April - running at 4/10 mood and 4/10 energy, with ~5h of focus time around three meetings. Today's single focus: finish the sequencing decision note (overdue from Friday). I marked it 🎯 in `Dashboard/tasks.md` and updated `journals/2026/04-April/21-04-2026.md`. Catch you this evening - run `/today evening` to close out.

---

## Evening mode

### Phase 1: Parallel data gather (no user interaction)

- Read today's journal - what was set as focus? Which "Notes" links are present?
- Read `Dashboard/tasks.md` - which 🎯 tasks were completed (marked `[x]`)?
- Check `Meetings/` for files matching today's date that look unstructured (no "Decisions" / "Action Items" sections).

If today's journal doesn't exist, create it from `templates/daily-note.md`.

### Phase 2: One AskUserQuestion (3-4 questions)

1. **Energy + mood at end of day** (0-10 each): "How did you end the day?"
2. **What did you finish today?** (free text) - suggest based on focus items + 🎯 completions as hints.
3. **What will you start with tomorrow?** (free text - one thing).
4. **Anything else to capture?** (optional free text; user can skip).

### Phase 3: Fill "End of Day" section

Update today's journal - find or append the `## End of Day` section:

```markdown
## End of Day

- Energy: [Q1 energy]/10 | Mood: [Q1 mood]/10
- Today I finished:
  - [user's answer to Q2]
- Tomorrow I start with:
  - [user's answer to Q3]
- Work closed.
```

If Q4 had content, append as a note below. Do NOT update frontmatter `mood` / `energy` - those reflect start-of-day state.

### Phase 4: Flag unprocessed items

If unprocessed meetings exist from today:
```
Unprocessed meetings from today:
- [Title] ([time or filename])

Run `/meeting` to process them.
```

If any 🎯 tasks are still open (not completed):
```
Open focus tasks (will carry over):
- [task]
- [task]
```

### Phase 5: Evening summary

Write a short conversational close-out, **not** a code-fenced template card. Two or three sentences: end-of-day mood/energy, what got done (brief), what starts tomorrow, and any carry-overs (unprocessed meetings or open 🎯 tasks). Use backtick-wrapped paths for any file references.

Example tone (do not copy verbatim):

> Day closed - ended at 6/10 mood, 5/10 energy. Shipped the sequencing decision and got half of the auth write-up drafted. Tomorrow starts with finishing that write-up. One unprocessed meeting from today (`Meetings/2026-04-21 - Design review.md`) - run `/meeting` when you're ready for it.

---

## Error recovery

- **Journal has unexpected format**: do not overwrite filled sections; only fill empty fields.
- **`Dashboard/tasks.md` missing**: create it from the template structure (three sections: This week / Next / Backlog) and proceed.
- **No calendar provided**: proceed with focus items from P-tasks only; note reduced confidence.
- **No yesterday's journal**: use generic hints for Phase 2 morning questions.

---

## Notes

- Keep the skill fast: max 3 rounds in morning, 2 rounds in evening.
- This skill has no external dependencies - no MCP required.
- The 🎯 marker in `Dashboard/tasks.md` signals "today's focus"; the user and other skills can rely on it.
