---
name: daily-admin-brief
description: "Turn a pasted calendar dump, inbox shortlist, and open todos into a one-page daily brief: top actions, schedule conflicts, draft reply stubs, FYI, dates to capture. Paste-first, no connectors. Triggers: 'daily admin brief', 'brief me on my day', 'бриф на день', 'разбери мой день'."
version: 1.0.0
---

# Daily Admin Brief

This skill turns three pasted raw dumps — the day's calendar, a shortlist of inbox items, and open todos — into one page the user can run their day from. It ranks what actually has to happen today, flags where the calendar is physically impossible, drafts reply stubs for the mail that needs a two-line answer, and catches dates buried in the text that never made it onto the calendar.

**Input:**
- Pasted text (or a local file path) with one to three blocks: calendar dump, inbox shortlist, open todos. No fixed schema — parse whatever arrives.

**Output:**
- One markdown page in the chat: Top Actions, Schedule Risk, Draft Replies, FYI, Needs Your Call, Dates to Capture.

**Hard scope — paste-first.** Work only on text the user pasted or a local file they named. Never assume, request, or simulate a Gmail, Outlook, Calendar, or task-manager connector. Never claim to have read a live mailbox, and never send anything.

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

All section headings and generated prose are rendered in the response language. Quoted fragments from the input stay verbatim in their original language.

---

## Instructions

### Step 1: Validate Input and Identify Streams

1. Check that day-material was actually provided.
   - Nothing pasted, or only a request with no data → stop. See **Negative Cases** (NEG1). Do not emit a template with placeholders.
   - Pasted material with no schedule, inbox, or todo signal (a spec, an article, a contract) → stop. See NEG3.

2. Segment the input into three streams:
   - **Calendar** — lines carrying times or durations (`10:00`, `10:00–11:00`, `2pm`, `1h`), often with a title after the time.
   - **Inbox** — lines carrying a sender plus a subject or snippet (`From: Ivan`, `Ivan — Budget sign-off`, `Anna: re: offer`).
   - **Todos** — imperative lines, checkboxes (`- [ ]`), or bare task phrases with no time and no sender.
   - If the user labelled the blocks (`## Calendar`, `Почта:`), trust the labels over the heuristic.
   - For ambiguous lines, see `references/stream-parsing.md`.

3. State which streams were found and which were not, in one line at the top of the output.
   - An absent stream is **not** an empty stream. Never generate content for a stream the user did not provide (EC1).
   - Name the consequence: `no inbox provided — Draft Replies skipped, Dates to Capture drawn from todos only`.

4. If the input contains credentials, tokens, or full card numbers, do not reproduce them anywhere in the output. Flag once that a secret appears in the pasted text, then continue with the rest (NEG4).

### Step 2: Establish the Target Day

1. Take the date from the calendar dump. If no date is stated anywhere, treat the material as "today" and say so.
2. If the material spans several days, use the **earliest** day covered as the target day and state that assumption in one line at the top (EC4).
3. Items belonging to later days do not go into Top Actions. Route their deadlines to **Dates to Capture** instead.

### Step 3: Analyse the Calendar for Schedule Risk

1. Detect and report:
   - **Overlaps** — two events whose stated intervals intersect.
   - **Back-to-back runs** — three or more consecutive events with no gap between them.
   - **Unbroken blocks** — more than three hours of continuous meetings.
   - **Meetings that need prep** — titles implying a decision or a performance (`review`, `interview`, `decision`, `presentation`, `board`, `1:1` with an unfamiliar name) that have no preparation block anywhere before them.

2. Only assert an **overlap** when both a start and an end (or a duration) are stated for both events.
   - Start time but no end/duration → do not assert a conflict. Report the pair as adjacent, mark `duration not stated`, and list it as unverified (EC3).

3. Do not silently normalise timezones.
   - Times with no timezone → compare them as given.
   - Entries in different stated timezones → flag `timezone mismatch — verify before trusting the conflict list` and show both as written (EC2).

4. Full detection rules and worked examples: `references/schedule-risk-rules.md`.

### Step 4: Rank Top Actions (3–5 items)

1. Rank only on evidence present in the input. The ordering criteria, highest first:
   1. An explicit deadline stated in the text that falls today
   2. A meeting today that needs preparation and has no prep block
   3. An inbox item that blocks someone else (`waiting on you`, `need it before`, `blocked`)
   4. A todo the user themselves marked urgent

2. Every action carries the source it came from: `*(from: inbox — Ivan, "Budget sign-off")*`.
   - Never emit an action that cannot be traced to a pasted line. Nothing is inferred from what a manager "usually" has to do.

3. Cap at five. If more than five items qualify, keep the top five and note how many were left out and where they went.
   - If fewer than three items qualify (thin input, or only one stream provided), list only the items with evidence. Never pad the list to reach three by inventing an action or lowering the evidence bar.

4. Do not apply a priority framework (Eisenhower, MoSCoW) and do not propose time blocks. Report what the material says and stop.

### Step 5: Draft Reply Stubs

1. Only for inbox items where the answer is genuinely short: acknowledge, confirm, decline, or ask one clarifying question.
   - An item needing a real decision, a document, or a long explanation does not get a stub — it goes to Top Actions instead.

2. Each stub is 2–4 lines, written in the **language of the message it answers**, matching its register (formal mail → formal stub).

3. Where the reply needs a fact the user has not pasted (a date, a number, a name), leave an explicit `[…]` gap. Never invent the fact to make the sentence read well.

4. Label the whole section as drafts to copy manually. The skill sends nothing (NEG2).

### Step 6: Sort the Remainder

1. **FYI** — items requiring no action today, awareness only. One line each, with source.
2. **Needs Your Call** — genuine ambiguity in the input, phrased as a question rather than resolved by guessing:
   - two items that may be the same commitment
   - an item with no owner
   - an unreadable or contradictory deadline
3. If the inbox shortlist runs to 20+ items, draft stubs only for those passing the short-answer test and list the rest under FYI by sender and subject with a count — never truncate silently (EC6).

### Step 7: Extract Dates to Capture

1. Scan the inbox and todo text for any date, deadline, or scheduling commitment that does **not** appear in the calendar dump.
2. Quote the fragment each date came from so the user can verify it before putting it in their calendar.
3. If no calendar was pasted, every date found is listed here, with a note that nothing could be cross-checked.

### Step 8: Assemble the Page

1. Emit sections in fixed order: Top Actions → Schedule Risk → Draft Replies → FYI → Needs Your Call → Dates to Capture.
2. Drop any section with no content and say so in a single line (`No schedule conflicts found.`).
3. Keep it to one page where the input allows. Structure and headings: `references/brief-template.md`.

---

## Negative Cases

- **NEG1 — nothing pasted.** Stop before generating anything. Ask for at least one of the three streams, naming all three (calendar, inbox shortlist, open todos), in the language of the user's message. Do not produce a placeholder brief.
- **NEG2 — asked to send the replies or connect to a service.** Decline in one sentence and state the paste-first scope: the skill works only on pasted text. Output the stub text for the user to copy manually. Never claim a message was sent; never pretend to have read a live mailbox or calendar.
- **NEG3 — pasted material has no day-signal.** Report that no calendar, inbox, or todo material was found, name what the skill needs, and stop. Do not force an unrelated document into the brief format.
- **NEG4 — credentials in the input.** Do not reproduce the secret in the output. Flag once that a credential appears in the pasted text and continue with the rest of the brief.

---

## Output Format

One markdown page in the chat. No files are written. Headings are translated to the response language; structure is identical in both.

```markdown
# Daily Admin Brief — {day, date}
Streams found: {list}. **{missing stream} not provided** — {consequence}.

## Top Actions
1. **{action}** — {why it is today}. *(from: {stream} — {source})*

## Schedule Risk
- **{time} overlaps {time}** — "{event A}" and "{event B}". One has to move.
- **{time} → {time} → {time} back-to-back**, no gap before {event}.
- **{time} "{event}"** — duration not stated; adjacency with {event} unverified.

## Draft Replies — copy manually, nothing is sent
**→ {sender}, "{subject}"**
> {2–4 line stub, with […] where a fact is missing}

## FYI
- {item} — no action today. *(from: {source})*

## Needs Your Call
- {ambiguity phrased as a question}

## Dates to Capture — not on the pasted calendar
- **{date}** — {commitment}. *(from: {source}, "{quoted fragment}")*
```

**Field rules:**
- **Top Actions:** 3–5 items, each with a source reference; ranked by the criteria in Step 4
- **Schedule Risk:** overlaps only when both intervals are fully stated; otherwise `duration not stated` + unverified
- **Draft Replies:** 2–4 lines, language of the original message, `[…]` for missing facts, labelled as drafts
- **FYI:** one line per item, no action implied
- **Needs Your Call:** phrased as a question, never resolved by guessing
- **Dates to Capture:** date + commitment + the quoted fragment it came from

---

## Key References

- **references/schedule-risk-rules.md**: full conflict-detection rules — overlap vs. adjacency, timezone handling, prep-needed title patterns, worked examples
- **references/stream-parsing.md**: how to classify ambiguous lines into calendar / inbox / todo, and what to do when a line fits two streams
- **references/brief-template.md**: the output page skeleton in EN and RU, with translated headings

Consult `stream-parsing.md` during Step 1, `schedule-risk-rules.md` during Step 3, and `brief-template.md` during Step 8.
