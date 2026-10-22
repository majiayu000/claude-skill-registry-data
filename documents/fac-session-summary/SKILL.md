---
name: fac-session-summary
description: Turns a session's capture into the record of the day, with a five-line headline against the brief, decisions and owners in the words used, and themes shown with the items under them. Use for "run fac-session-summary", "workshop summary", "write up the workshop", "session notes and decisions", "what did the workshop decide", "workshop output report", "the session was yesterday and I need to send something today", "summary of the offsite", part of the Claude for Trainers and Facilitators Pack by Polar Bear.
---

# Session Summary and Decisions

## When To Use
The session was yesterday and you need to send something today, before it un-happens. Decisions blur, owners forget, and the wall has been wiped. Use this within two days to write the record of what the room produced against what the brief asked for.

## When Not To Use
If the material is still photos and loose notes, run Wall and Board Capture first: a summary written straight from memory interprets before anything is on the page. For a pure training session where nothing was produced or decided, the first message of the Post-Session Follow-Up Sequence is enough.

## Inputs
- The capture: transcribed walls and boards, vote counts, the parking lot, the close in the words used
- The brief, or one sentence on what the session was meant to produce, the date it ran, and who will read the summary
If you have none of this, I start from your memory of the close and the brief, and mark the output as a first draft written from memory.

## Approach
This is synthesis with the interpretation left visible, a practice standard among facilitators with no single originator. The brief is the yardstick, so the summary is ordered by what the session was for, not by the clock. Wherever it clusters or names a theme, the items sit underneath so a reader can tell what the room said from what the summary made of it. The failure it prevents: three enthusiastic notes become "the group agreed", and a month later someone is held to a decision nobody took. It works in a plain chat, or as a document in Claude Docs (beta).

## Workflow
1. Ask three questions: what did the brief ask the session to produce, when was the session, and who reads this summary?
2. If more than two days have passed, say so at the top and mark every line that rests on your memory instead of the capture. It is still worth writing, only with more of it open to correction.
3. Write the headline in five lines against the brief, with one honest verdict: reached, partly reached with the path to finish, or something more important surfaced. An uncomfortable headline is written plainly with the way forward.
4. Record decisions and owners in the exact words from the close, with dates and where each sits in the capture. A decision you remember that is not in the capture is listed as "remembered, not in the capture" for you to confirm, never written as decided.
5. Build the themes per thing the brief asked for. List the underlying items under every theme, and give votes as counts. "The room chose X" needs the vote or the stated agreement; three notes are three notes.
6. Carry over the parking lot and the open questions as they were written. They are raw material for the next session, not leftovers.
7. Run the "before it is sent" sweep: anything readers were not cleared to see, internal shorthand, and any name attached to something that was not a decision or commitment made openly.

## Output Format
```markdown
# Session Summary and Decisions
Session: [name] | Held: [date] | Written: [date] | Based on: [capture / notes / memory, stated]
## Headline
[Five lines: what the brief asked for, what the room produced, and the verdict: reached / partly reached, with the path to finish / something more important surfaced.]
## Decisions and owners
| Decision or commitment, in the words used | Owner | By when | Where it is in the capture |
|---|---|---|---|
| [exact words] | [name, only if taken openly] | [date] | [block, board or note] |
## What the room built
| What the brief asked | Theme (named by this summary) | Items from the capture under it | Votes (count) |
|---|---|---|---|
| [ask] | [theme] | [item]; [item]; [item] | [count, or "no vote"] |
## Parking lot
- [item, as written]
## Open questions
- [question] | [who can answer it]
## Checks before it is sent
- [ ] Remembered but not in the capture, to confirm: [items]. Removed or cleared for these readers: [items]
## Decision
[Trainer name] corrects and approves this record by [date, within two days of the session]; [sponsor or owner name] confirms the next step and its date by [date].
```

## Done When
- A reader who was not in the room can say whether the session got what it came for
- Every theme shows the items it was built from
- Every decision carries an owner, a date and its place in the capture, or is marked as not yet confirmed
- No sentence claims agreement without a vote or a stated agreement behind it, and the sweep is done

## Quality Bar
- Ordered by what the brief asked for, never as a diary of the day
- The room's own words for decisions; the summary's words only for theme names
- Anonymous material stays anonymous, and a summary that flatters the session sets up a worse next one
- The summary records what was produced and decided, never who resisted or dominated, and names a person only for a decision or commitment they made openly.

## Next
Run fac-follow-up-sequence (Post-Session Follow-Up Sequence) to get the summary to the room with a next step attached.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).