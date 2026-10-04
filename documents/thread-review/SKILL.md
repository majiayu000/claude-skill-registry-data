---
name: thread-review
description: Cross-session review — what recurs, what has moved, what has gone quiet, and whether the frame of the issue still fits. Use when the user asks "what keeps coming back", monthly-ish, or before a therapist brief.
---

# thread-review

The one thing a workspace can do that a conversation can't: look across time.

## Threads

A thread is something that recurs. `threads/<id>.md`:

```markdown
---
type: thread
id: <id>
opened: 2026-07-14
status: open        # open | quiet | resolved | archived
sessions: [260714-first, 260801-phone-call]
---

# <the recurring thing, in their words if possible>

## Instances
- 2026-07-14 — <what happened, one line> (sessions/260714-first)
- 2026-08-01 — ...

## What it looks like
The shape, as currently understood. Rewritten when understanding changes;
previous version moved to the History section below.

## What's changed
Movement over time — in the events, or in how they read them.

## History
- 2026-08-01 — description revised: <what changed and why>
```

## Procedure

1. Read all of `threads/`, then every session file since the last review (frontmatter `threads:`
   tells you which sessions belong where).
2. For each thread: has it had new instances? Has its shape changed? Has it gone quiet — no
   instance in a month or more?
3. Look for threads that should merge (two names for one thing) and threads that should split
   (one file carrying two unrelated patterns). Propose; don't execute unilaterally.
4. Check the frame: does `context/issue.md` still describe what these threads are actually
   about? Frames drift, and an unexamined frame is the most common reason a workspace stops
   being useful.
5. Write `artefacts/review-YYMMDD.md` and update `threads/INDEX.md`.

## The review artefact

```markdown
# Review — 2026-08-14

Covering sessions <first> to <last> (<n> sessions over <period>).

## Open threads
One line each: what it is, how many instances, whether it's moved.

## What's changed since the last review
Concrete differences, not encouragement.

## What's gone quiet
Threads with no instances recently. Say so neutrally — quiet can mean resolved,
avoided, or simply not now.

## What hasn't moved
The honest section. If something has been open for six months and looks the
same, say so plainly and without judgement.

## Frame check
Does context/issue.md still fit? Proposed edits, if any.

## For the next appointment
Anything here worth taking to a professional. Feeds therapist-brief.
```

## Rules

- **Report movement, don't manufacture it.** "You've made real progress" when nothing has changed
  is flattery, and it makes every subsequent review worthless.
- **"Hasn't moved" is not a criticism.** Write it as an observation and leave it alone.
- **Quantify where you can.** "Mentioned in six of the last eight sessions" beats "comes up a
  lot" — it's checkable, and they can disagree with it.
- **Don't invent themes to fill the section.** Three real threads is a good review.
- Never merge or archive a thread without asking. Archived threads go to `archive/` with a line
  saying why and when.
