---
name: meeting-notes
description: Convert a transcript into structured meeting notes + action items
argument-hint: '[FILE=<path>] [TITLE="<title>"] [DATE=YYYY-MM-DD] [ATTENDEES="<names>"]'
disable-model-invocation: true
---

Turn a raw meeting transcript into concise, neutral notes. Distill the discussion; never reproduce the transcript.

## Get the transcript and overrides

- Read the transcript from the path supplied as `FILE=...`. If no file is supplied, use transcript text pasted in the chat.
- If neither is available, ask the user to provide the transcript and stop.
- Use supplied `TITLE=...`, `DATE=...`, and `ATTENDEES=...` values verbatim. If absent, infer them from the transcript where possible.

## Extract the meeting record

Identify the meeting's purpose, major topics, key discussion and rationale, explicit decisions, unresolved questions, and next actions. Remove fillers, chit-chat, and repeated points; retain the clearest version of each idea.

For action items, capture commitments and requests, including phrases such as “I can,” “I’ll,” and “Can you,” as well as follow-ups, drafts, reviews, updates, tests, schedules, and other concrete work. Name an owner only when the transcript does; otherwise use `TBD`. Preserve relative due dates as spoken (for example, “by next week” or “before launch”); use `TBD` when no due date is given.

Treat proposals as decisions only when the speakers indicate agreement or a choice, for example “let’s,” “we agreed,” or “we’ll go with.” Put contested topics without a final choice under open questions. If the transcript does not state a decision, say so explicitly.

Use speaker names from the transcript. When names are absent, use the available generic speaker label (such as “Engineering,” “PM,” or “Caller 2”); never invent a person. Infer the facilitator or primary speaker only when supported by the discussion.

If details are missing or speech is unclear, mark that uncertainty instead of guessing. Strip obvious email addresses, tokens, and API keys; replace credential-like strings with `[redacted sensitive string]`.

For transcripts shorter than 10 lines, keep the same format and include Summary, Decisions, and Action Items, even when some sections have no entries.

## Output

Return only the Markdown meeting notes below. Use `Unknown` for an uninferable date, `Untitled` for an uninferable title, and `Not specified` for attendees not supplied or named. Use `TBD` for missing action owners or due dates. In the source/confidence section, identify unclear transcript segments and any assumptions made.

```markdown
# Meeting Notes
**Title:** <supplied title, inferred title, or Untitled>
**Date:** <supplied date, inferred date, or Unknown>
**Attendees:** <supplied attendees, names in transcript, or Not specified>
**Facilitator/Primary speaker:** <supported speaker or Not specified>

## 1. Summary
- <3–6 concise bullets>

## 2. Agenda / Topics Covered
1. <Topic> — <short description>

## 3. Discussion Details
### <Topic>
- Key points:
  - <point>
- Rationale / context:
  - <context, when present>

## 4. Decisions
- Decision: <choice> (why: <reason, when stated>)

## 5. Action Items
| # | Action | Owner | Due | Notes / Source |
|---|--------|-------|-----|----------------|
| 1 | <action> | <owner or TBD> | <date or TBD> | <speaker and topic, when available> |

## 6. Open Questions / Parking Lot
- <unresolved question or topic>

## 7. Source / Confidence
- Transcript segments that were unclear: <segments or None>
- Assumptions made: <assumptions or None>
```

When no explicit decisions were captured, write: `No explicit decisions captured.` Keep empty sections present so the record has a consistent shape.
