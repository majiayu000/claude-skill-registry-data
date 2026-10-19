---
name: user-feedback
description: Intake protocol for user feedback and reports — how to split, classify, investigate, dedupe, and file them in the issue tracker, and when to escalate. Use whenever the repo owner pastes user feedback, bug reports, complaints, or feature requests.
---

# Handling user feedback

Tracker-agnostic: "the tracker" below is whatever the project uses.

> **Current tracker: Linear** — project "Mathiz" (team Founder Ops), label
> `feedback`. If the tracker changes (e.g. to GitHub issues), update ONLY
> this block; the protocol below must not assume any specific tool.

## Principles

- **Never lose the verbatim quote.** Users report symptoms in their own
  words; paraphrasing destroys evidence. Quote first, interpretation
  clearly separate and below it.
- **Track problems, not solutions.** Titles state the user's problem
  ("parent couldn't find the join code"), never a premature fix ("make
  the button bigger").
- **Duplicates are the signal.** Repeat reports accumulate as dated
  comments on ONE issue — the comment trail IS the demand count. Never
  file a clone.
- **A feedback record is not a work item.** File what happened; derive
  actionable bug/feature issues only when there is something to act on.
  One paste can yield zero or several.

## Intake protocol (each time feedback is pasted)

1. **Split** the paste into discrete items — one message often carries
   several complaints plus noise.
2. **Classify** each: bug / UX friction / feature request / docs-or-copy
   gap / pure signal (praise, confusion worth recording).
3. **Investigate before filing.** For bugs and friction, read the code
   first and file with a root-cause hypothesis, affected files, and an
   effort estimate — never a bare symptom. (A "probably user error"
   report deserves the same look: several such reports here turned out to
   be real bugs, e.g. MCQ options never being shuffled.)
4. **Dedupe** against the tracker. Existing theme → add a dated comment
   with the verbatim quote and anything new (+1, not a new issue). New →
   create: problem-statement title, verbatim quote up top, source + date,
   triage analysis below, feedback label, priority.
5. **Severity gate.** Anything breaking a child's play session, money
   flows, or signup gets flagged to the repo owner IMMEDIATELY with a
   proposed hotfix — it does not wait in a backlog.
6. **Report back** a compact table: item → disposition (filed X / +1'd Y
   / hotfix proposed / noted, no action). Every sentence of the paste is
   accounted for.
7. **Intake is not fixing.** File and analyze; implement only when the
   owner says so. Exception: step 5 escalations still propose, not ship.

## Review rollup (on request, e.g. "review the feedback")

Rank themes by demand count (comment trails), cross-check against product
analytics where available (a complaint corroborated by a funnel drop-off
outranks a loud one-off), and propose the next fixes/features with the
evidence attached. The owner picks; nothing is auto-promoted.
