---
name: ls-backlog-and-reminders
description: "Record deferred ideas, to-dos, and reminders (with optional due date or 'whenever'); show due/overdue when user starts a session or asks. Use when user says 'add to backlog', 'remind me', 'I'll do this later', 'what's due?', 'show my backlog', 'start my session', or wants to capture ideas for later."
metadata:
  version: "1.1"
---

# Backlog and reminders

**Purpose:** Let users record things they want to do later (repo features, tasks, free-form reminders) with an optional due date or no date ("whenever"). Surfaces due and overdue items when they start a session or ask. AI condenses free-form input into clear, actionable backlog items.

## When to use this skill

- User wants to record an idea, to-do, or reminder for later (with or without a date).
- User says "add to backlog", "remind me", "I'll do this later", "save this for later", "don't have time now", "set a reminder", "what's on my backlog?", "what's due?", "show my backlog", "start my session", "what should I work on?".
- User gives free-form text that should become one or more concrete backlog items.

## When not to use

- User names a different skill or tool (for example, Todoist or Apple Reminders). Use what they asked for.
- Exact-time reminders require a scheduler that can deliver at the requested instant; this date-level backlog cannot provide timed delivery. Route the request to an appropriate scheduler. Convert it to a date-only backlog item only after the user explicitly approves losing the clock time.

## Backlog file location

- Canonical path: `.localsetup/backlog.md`.
- Legacy fallback: `BACKLOG.md` at the repo root, only when `.localsetup/backlog.md` does not exist.
- If both files exist, read and update `.localsetup/backlog.md`; mention that root `BACKLOG.md` is legacy and should be merged or removed when the user is ready.
- If neither file exists, create `.localsetup/backlog.md` with the structure below.
- Never create or update backlog/reminder state under `ls/`; that directory is framework-owned source.

## File format

Use Markdown with these sections. Preserve any extra sections or comments the user (or you) added.

```markdown
# Backlog

*Last updated: YYYY-MM-DD*

## Overdue
- [ ] Short title (due: YYYY-MM-DD) optional note
## Due soon (today through 6 days after today)
- [ ] Short title (due: YYYY-MM-DD) optional note
## Scheduled (7 or more days after today)
- [ ] Short title (due: YYYY-MM-DD) optional note
## No date (whenever)
- [ ] Short title - optional note
## Done
- [x] Short title (done: YYYY-MM-DD)
```

- **Overdue:** Incomplete dated items whose due date is before today.
- **Due soon:** Incomplete dated items due from today through six days after today.
- **Scheduled:** Incomplete dated items due seven or more days after today.
- **No date (whenever):** Items with no due date; do when convenient or when user asks "what should I work on?".
- **Done:** Completed items; move here when user marks done; optional to trim old entries periodically.

## Timezone and due-date rules

- Store due dates as date-only values in `YYYY-MM-DD` form. This package provides session-level reminders, not timed delivery.
- Resolve relative dates such as "today", "tomorrow", "next Friday", and "in two weeks" using one consistent timezone.
- Timezone precedence:
  1. Use the explicit timezone from the user's message or environment context when provided.
  2. Otherwise use `LOCALSETUP_TIMEZONE` if set.
  3. Otherwise use `TZ` if set.
  4. Otherwise use the host system local timezone.
  5. If none is available or the date would be ambiguous, ask once before writing the item.
- If a request includes a clock time, route it to an appropriate scheduler. If the user instead wants it retained here, state that timed delivery will be lost and obtain explicit confirmation before storing only the resolved date.
- Reclassify every incomplete dated item whenever the backlog is read or updated: `Scheduled` to `Due soon` as it enters the seven-day window, and any dated section to `Overdue` after its due date passes. Preserve item order within each destination section.
- Compute all date classifications from the same timezone used to resolve the due date.

## Adding items

1. **Parse user input:** Extract one or more distinct ideas, tasks, or reminders. If the user gives a long paragraph, condense into 1-3 clear items with short titles and optional notes.
2. **Due date:** Resolve date-only requests ("next Friday", "March 15", "in two weeks") to `YYYY-MM-DD` and place them in `Overdue`, `Due soon`, or `Scheduled`. Put undated items in `No date (whenever)`. Handle clock-time requests under the timed-delivery rule above before writing.
3. **Write:** Append (or insert) each new item in the correct section. Update "Last updated" at the top. Do not remove or reorder existing items unless the user asks (e.g. "remove X", "mark Y done").
4. **Confirm:** Reply briefly with what was added and, if applicable, the due date.

## Showing the backlog (session start or on demand)

When the user asks to "start my session", "what should I work on?", "what's due?", "show my backlog", or when they begin a session and you have a habit of surfacing backlog:

1. Read the backlog file (create empty structure if missing).
2. Summarize in this order:
   - **Overdue:** List items; say they are past due.
   - **Due soon:** List items and due dates.
   - **Scheduled:** Give the count and nearest due date; include full items when the user asks for the full backlog.
   - **No date:** Give the count and optionally 1-2 example titles; say they can ask to "show full backlog" or "work on something from backlog".
3. Before summarizing, move dated items into the section required by today's date and the configured timezone.
4. Suggest one next step (for example, pick an overdue item or "pick one from whenever").
5. Keep the summary short (bullet list plus one line of guidance).

If the file has no incomplete items in `Overdue`, `Due soon`, `Scheduled`, or `No date`, say the backlog is clear and offer to add something ("Want to add an item or a reminder?").

## Marking done / removing

- **Mark done:** When user says "mark X done", "completed X", "did X": move that item from its current section to "Done" and add `(done: YYYY-MM-DD)`. Confirm.
- **Remove:** When user says "remove X", "delete X from backlog": delete that line from the file. Confirm.

## Condensing free-form input

When the user dumps a long idea or list:

- Split into discrete items (one actionable unit per bullet).
- Give each a short title (few words); put detail in a note after the title or in parentheses.
- If they mention a date for part of it, attach that date to the relevant item only.
- If nothing has a date, put all in "No date (whenever)".

Example: "I want to add a dark mode toggle and also fix the login bug by next week, and someday refactor the API layer" -> three items: (1) "Add dark mode toggle" (whenever), (2) "Fix login bug" (due: next week), (3) "Refactor API layer" (whenever).

## References

- Backlog template and precedence notes: [references/backlog-template.md](references/backlog-template.md).
- Backlog file: `.localsetup/backlog.md`; root `BACKLOG.md` is a legacy fallback.
- No external services required; everything is file-based and git-friendly.
