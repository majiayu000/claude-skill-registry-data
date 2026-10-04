---
name: convert-meeting-notes
description: Convert a meeting transcript (Zoom, Teams, or Meet .vtt, or pasted text) into an Obsidian-ready note with decisions, owned action items, and open questions. Use after a recorded meeting or to turn Zoom notes into notes. For research interviews, use analyze-user-interview.
---

# Convert Meeting Notes

Turn a recorded meeting into a note people actually use: what was decided, who does what by when, and what is still open, with each item traceable to the transcript.

## Reasoning Framework

A transcript with headings is not notes. A useful note answers three questions: what did we decide, who owns what by when, and what is still unresolved. A script compacts the raw transcript (about a third to half smaller, speakers merged); the model extracts commitments and cites a timestamp for each, so nothing is invented and anything can be checked.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| Meeting note | Markdown with YAML frontmatter, Obsidian-compatible (`- [ ]` tasks, optional `[[wikilinks]]`) | User's notes folder or vault |
| Follow-up draft (optional) | Plain text recap for the user to send | User |

## When to Use

- After a recorded meeting with a transcript file (Zoom and Teams export `.vtt`)
- When the user pastes meeting text and wants decisions and actions pulled out
- When building a searchable meeting archive in Obsidian

## When NOT to Use

- User research interviews: use `analyze-user-interview` (research synthesis, not action items)
- A meeting that hasn't happened yet: use `prompts/claude/meeting-prep-brief.xml`

## Inputs

1. **Transcript**: path to a `.vtt` (preferred) or `.txt`/`.md` file, or pasted text.
2. **Meeting title and date**: from the filename or calendar; ask if unclear.
3. **Attendees and roles** (optional): helps resolve speaker labels.
4. **Your own notes** (optional): merged in; they often capture decisions the transcript misses.
5. **Output folder**: Obsidian vault path, default `~/Desktop`. Ask whether to use `[[wikilinks]]` for people.

## Steps

1. **Find the transcript.** If an email or calendar connector (Outlook, Microsoft 365, Google) is available in this session, you may use it read-only to find the recording notice, transcript, and meeting metadata. Otherwise ask for the file path. Never send messages or accept invites.
2. **Compact it (script)** for `.vtt` files:
   ```bash
   python3 scripts/vtt_to_transcript.py <meeting.vtt> -o <tmp>/transcript.md
   ```
   Read the printed summary first. If a label looks like a room or device ("Conference Room 4B", "iPhone"), ask who was there, then rerun with `--rename "Conference Room 4B=Dana Lee"`. For plain text, read it directly.
3. **Read** the compact transcript plus any user notes.
4. **Extract**, citing `[hh:mm:ss]` for each item:
   - **Decisions**: what was decided and by whom.
   - **Action items**: owner, task, due date. Use a date only if one was stated or clearly agreed; otherwise write "no date".
   - **Open questions**: and who can answer them.
   - **Discussion**: 3–7 bullets, each stating an outcome or position, not a topic ("Agreed export is the Q4 priority", not "Discussed export").
   - **Risks and blockers**, and **follow-ups** (next meeting, documents to share).
5. **Don't guess.** An unclear owner or date goes in "Needs confirmation", not into the task.
6. **Write the note** with the template below. Filename: `YYYY-MM-DD Title.md`. If the file exists, add a suffix instead of overwriting.
7. **Optional recap.** Draft a short follow-up (decisions plus action items) for the user to send themselves.

## Note Template

```markdown
---
type: meeting
date: 2026-09-22
title: Q4 roadmap sync
attendees: [Dana Lee, Priya Shah, Sam Ortiz]
source: 2026-09-22-roadmap-sync.vtt
tags: [meeting]
---

# Q4 roadmap sync (2026-09-22)

**Attendees:** Dana Lee (PM), Priya Shah (Eng), Sam Ortiz (Design) · **Length:** 00:52

## TL;DR
Two or three sentences: the most important decision and the most important next step.

## Decisions
- Export performance is the Q4 priority; bulk edit moves to Q1. Decided by Dana. [00:14:05]

## Action items
- [ ] Priya: estimate the export rewrite (due 2026-09-26) [00:20:11]
- [ ] Sam: share the bulk-edit flows with support (no date) [00:31:40]

## Open questions
- Do enterprise contracts promise bulk edit this year? Dana to check with sales. [00:36:02]

## Discussion
- ...

## Risks and follow-ups
- ...

## Needs confirmation
- Owner for the migration dry run was not named. [00:44:18]
```

For the Obsidian Tasks plugin, write due dates as `📅 2026-09-26`. Use `[[Dana Lee]]` wikilinks only if the user opted in.

## Examples

- "Turn this Zoom VTT into notes for my vault at ~/Notes/Meetings." Compact, resolve a room label, extract, and save `2026-09-22 Q4 roadmap sync.md` there.
- "Here's the transcript text from Teams." Read the pasted text directly and produce the same note.

## Guardrails

- No invented owners, dates, or decisions. Every item carries a timestamp or comes from the user's notes.
- Quote only verbatim text inside quotation marks.
- HR, compensation, legal, or other sensitive content: ask before writing it to a synced vault.
- Keep transcripts and notes local. Never commit them to this public repo.
- Never send email or messages. Drafts are for the user to send.

## Related Skills

- `analyze-user-interview`: research-grade synthesis of an interview
- `decision-brief`: when the meeting surfaced a decision that still needs making
- `prompts/claude/teams-meeting-summarizer.xml`: copy-paste version for chat tools
- `library/lenny-podcast/lenny-running-effective-meetings/SKILL.md`: making the meeting itself better
