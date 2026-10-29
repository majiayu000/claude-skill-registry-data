---
name: meeting-note-summariser
description: "Use when someone asks to summarize meeting notes, recap a meeting, or format meeting minutes."
argument-hint: "[meeting topic or date]"
allowed-tools: Read, Write
---

## What This Skill Does

Takes raw or unstructured meeting notes and produces a clean, structured summary with attendees, key decisions, action items with owners and deadlines, and open questions.

## Steps

1. If notes weren't already given, ask via `AskUserQuestion` how to provide them: **Paste the raw meeting notes** / **Provide a file path**. Then request the actual content per their choice as free text -- the notes themselves have no finite menu.
2. If the content is clearly not meeting notes (e.g., an email thread, unrelated document), flag that instead of forcing it into the template.
3. Determine the meeting title:
   - If `$ARGUMENTS` is provided, use it as the title.
   - Otherwise, infer a reasonable title from the content of the notes.
4. Extract the following from the notes:
   - **Attendees** — Who was in the meeting
   - **Key decisions** — What was explicitly decided
   - **Action items** — Who owes what, with deadlines if mentioned; flag any that lack clear owners or deadlines as "TBD" rather than inventing them
   - **Open questions** — Anything unresolved or needing follow-up
5. If multiple distinct topics or sections appear in the notes, group or label decisions and action items by topic rather than merging them into one undifferentiated list.
6. Format the output using the template below.
7. Return the summary as text output in the conversation by default.
8. If the user explicitly asks to save it, write the file to `output/meeting-note-summariser/[title]-summary.md` using the Write tool.

## Output Template

```
# Meeting: [title]
**Date:** [date if mentioned, otherwise "Not specified"]
**Attendees:** [comma-separated list]

## Key Decisions
- [decision]
- [decision]

## Action Items
- [ ] [person/team]: [task] (due: [date or "TBD"])
- [ ] [person/team]: [task] (due: [date or "TBD"])

## Open Questions
- [question]
- [question]
```

## Notes

- Keep summaries concise. Don't add commentary, editorializing, or unsolicited suggestions.
- Never fabricate attendees, decisions, owners, deadlines, or action items that weren't in the notes.
- If notes are too vague to extract meaningful details, flag those items as "TBD" or "Unclear" rather than inventing them.
- If part of the notes doesn't map cleanly to one of the categories, flag it as "Unclassified" rather than omitting it.
- Preserve specific details (names, numbers, dates) even if it makes the summary slightly longer.
- Only write a file if explicitly asked by the user—keep output conversational by default.
- Clickable-question convention: the Step 1 intake-method choice uses `AskUserQuestion`. The meeting notes content itself stays free text -- genuine data, not a finite menu. No other user-facing questions exist; saving to file happens only if the user spontaneously asks, not via a skill-initiated prompt.
