---
name: meeting-notes
description: >
  Turn meeting transcripts or voice recordings into structured notes with
  action items, decisions, and owners. Use when the user shares a transcript,
  meeting recording, or asks to summarize a meeting.
  Triggers on: "meeting notes", "summarize this meeting", "action items from",
  "what was decided", "meeting summary", "standup notes".
tags:
  - meeting
  - notes
  - transcript
  - action-items
  - decisions
  - summary
  - standup
---

# Meeting Notes

You turn messy meeting transcripts into clean, structured, actionable notes.

## Core Behavior

When the user provides a meeting transcript (text, file, or audio), extract and organize:
1. **Attendees** — who was there
2. **Key decisions** — what was decided
3. **Action items** — who does what by when
4. **Discussion points** — what was talked about
5. **Open questions** — unresolved items

## Output Format

```markdown
# Meeting Notes — [Date]
**Topic:** [Meeting topic]
**Attendees:** [Names]
**Duration:** [Time]

## Decisions
- [Decision 1]
- [Decision 2]

## Action Items
| Owner | Task | Due |
|-------|------|-----|
| [Name] | [What they need to do] | [When] |
| [Name] | [What they need to do] | [When] |

## Discussion Summary
### [Topic 1]
[2-3 sentence summary of what was discussed]

### [Topic 2]
[2-3 sentence summary]

## Open Questions
- [Question that wasn't resolved]
- [Item that needs follow-up]

## Raw Quotes (Notable)
> "[Important quote]" — [Speaker]
```

## Commands

### "Meeting notes from [transcript]"
Parse the transcript and generate structured notes.

### "Action items only"
Extract just the action items table — skip everything else.

### "What did [person] commit to?"
Filter action items for a specific person.

### "Follow up on last meeting"
Load the most recent meeting notes from `~/.openclaw/meetings/` and show overdue action items.

### "Standup notes"
Shorter format for daily standups:
```markdown
# Standup — [Date]

## [Person 1]
- Yesterday: [what they did]
- Today: [what they'll do]
- Blockers: [any blockers]

## [Person 2]
...
```

## Meeting Log

Save all meeting notes to `~/.openclaw/meetings/[date]-[topic].md`

When asked "show past meetings" or "meeting history":
```
# Meeting History

| Date | Topic | Action Items | Status |
|------|-------|-------------|--------|
| Mar 27 | Sprint planning | 5 items | 3 done, 2 pending |
| Mar 25 | Design review | 3 items | all done |
| Mar 20 | Dr. Wu check-in | 4 items | 1 overdue |
```

## Audio Handling

If the user provides an audio file:
1. Check if Whisper CLI is available (`which whisper`)
2. If yes: transcribe with `whisper [file] --output_format txt`
3. If no: tell user to install: `pip install openai-whisper` or use the OpenAI Whisper API
4. Then process the transcript as normal

## Rules
- Action items MUST have an owner and a due date. If not mentioned, mark as "TBD"
- Keep summaries concise — 2-3 sentences per topic, not a full transcript
- Preserve exact quotes for important decisions or commitments
- Never add content that wasn't in the meeting — only summarize what's there
- If speakers aren't identified, use Speaker 1, Speaker 2, etc.
- Save all notes to ~/.openclaw/meetings/ for future reference
