---
name: propose-answers
description: For each gap a drive's search could not close and only the person can confirm — who may decide, how we will know it works, how big it will get — draft our own proposed answer from what the drive's sources, memory and run already show, with its basis and the context the person needs to judge it, so the person confirms or corrects instead of answering a bare question. Closes as settled a gap the context already answers (an internal tool is not asked how it earns money). Used by the knowledge-builder agent in /build-knowledge.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Glob, Grep
---

# propose-answers

A person who gave a drive a prototype knows what it is for. A list of questions makes them do
the drive's work. This skill does that work: it drafts the answer we would put, from what we
already saw, and shows why — so the person only says yes or corrects.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `gaps` | yes | The search groups still `partly` or `open` that research cannot answer — each with its plain question, what is missing, and any partial answer |
| `sources` | yes | The drive's Source evidence (for a prototype: views, journeys, the page) |
| `run` | yes | What the drive made: the proposed intents, the domain, its capabilities (the product model's files for this run) |
| `out` | yes | Where to write the proposals (`<working>/proposals.json`) |

## Process

1. For each gap, ask first: **does the context already settle it?** A product the prototype shows
   as an internal tool has no revenue question; a tool the prototype shows one person using is
   not asked about teams of thousands. If so, close it `settled`, say what settles it, and name
   what that rests on (`basis`: the quote, screen or trace). A settled point is shown to the
   person in the brief; it is never dropped silently.
2. Otherwise draft **our proposed answer** — the answer we would put if no one corrected us:
   - start from what the source shows (one reviewer on every screen → "the person who asked
     decides"), what memory holds, and what the run made (a counter of what waits → "settled
     when nothing waits");
   - make it concrete and checkable (a number, a role, a rule), never "it depends";
   - mark a value the person must set (a target, a period) as our default, not a fact.
3. Write its **basis** — the quote, screen, memory trace or reasoning it rests on — and its
   **context** — the one or two facts the person needs to judge it without opening the
   prototype.
4. Never write a question as a proposal, and never answer from the model alone. If nothing in
   the source, memory or the run supports an answer, the gap stays open for research
   (`draft-knowledge-page`) — not a guess.

## Output

`proposals.json`: `{"proposals": [{"group", "closed_by": "proposal | settled", "answer",
"basis", "context", "why"}]}` — `answer`, `basis` and `context` for a proposal; `why` and
`basis` for settled.

## Rules

- No basis, no proposal: every proposed answer names what it rests on.
- Sample data is sample data: the shop inside a review tool's mockup tells you how the tool
  shows things, not facts about the tool's own users.
- Never decide for the person; a proposal is what they confirm or correct.
