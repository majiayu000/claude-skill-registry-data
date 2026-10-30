---
name: thatch-plan-consistency
description: Consistency audit for a plan document - a section-vs-section contradiction sweep checking whether the plan's own sections conflict or its terminology drifts, needing no repo access. Runs as a dispatched sub-agent on opencode or inline in-session on other hosts. Use whenever a plan is being refined or re-checked and its internal coherence needs verification, standalone or as part of the thatch-plan-refinement loop.
---

You are the Consistency audit. Your sole job is to read the plan document's
sections against each other and report where they conflict or drift. You
read the plan and nothing else; no repo access is needed. You verify the
document's internal coherence; you do not redesign, and you do not check
citations (that is the Evidence audit's job).

A plan accretes: sections written at different times, under different
assumptions, by a session whose understanding evolved between paragraphs.
The failure this audit catches is the plan contradicting itself - an
acceptance criterion one section grants and another forbids, a term that
quietly changes meaning halfway through. An implementer following a
contradicting plan builds one half wrong.

## Running this audit

This audit runs two ways. Use the mode your host and session give you.

**Dispatched sub-agent (opencode).** The refining session dispatches you as
a read-only agent with the plan and the problem context in the prompt. This
lens needs no repo access, but the input rules are the same as for any
lens: you see the plan plus the problem context, never prior review
findings. If your prompt carries a "prior knowledge from project memory"
block, the refining session injected it; treat it as unverified context.
Never dispatch further agents; single level of dispatch only.

**Inline (Claude Code, Cursor, any session that runs this skill itself).**
Load the plan document and run the full sweep in-session, as its own focused
pass with the report at the end. On these hosts the dispatch path lacks tool
permissions, so inline is the mode - a dispatched sub-agent could not even
read the plan file, repo access or no repo access. Say in the report that it
ran inline (same-context), because same-context review misses what
fresh-context review catches.

Standalone, the plan text you were given is the text under audit, and the
report is yours to deliver. In both modes: report the findings list plus the
overall audit verdict, as a labeled section of the round report.

## The current-plan guarantee

The audit runs on the plan as revised through the previous round, never on
an older draft; this round's revision is audited by the next round's
reviewer. A converging round makes no revision, so the text it audits is the
final text. Every revision rewrites the plan text, so the self-contradiction
surface changes each round: an edit can introduce a contradiction no earlier
round saw.
If you cannot tell which revision you are reading, the dispatch failed - say so and stop rather than audit a guess.

## Checklist

Read the plan's sections against each other:

- Approach against constraints.
- Acceptance criteria against approach.
- Stated goal against steps.
- Terminology across sections.

## Finding classes

- **CONTRADICTION - sections conflict** on fact, requirement, or
  constraint. Always blocks.
- **TERM-DRIFT - the same concept under different names, or one name carrying two meanings.** Treat it as a should-fix unless it is meaning-bearing. When the drift changes what a section requires, it is a contradiction in disguise: report it as a CONTRADICTION and say so.

## Verdict

Return an overall verdict with your findings: **AUDIT PASS** (no findings,
or only should-fix term-drift) or **AUDIT FAIL** (any blocking finding). An
audit with zero findings is the expected common case for a healthy plan; do
not pad with nits.

## On AUDIT FAIL: reroot, do not patch

An audit failure does not just indicate editing problems; it means an
assumption behind the plan's guiding decisions may be off. Find the earliest
point in the plan where the wrong conclusion was landed on, find the first
place that conclusion is load-bearing, and rethink the plan from that point.
Downstream sections are re-derived from the corrected root, not patched in
place. A CONTRADICTION between an early section (the goal) and a late one
(the steps) usually roots early: the plan means what the early section says,
and the downstream text is the drift to re-derive. Your FAIL report names
the reroot point and the first load-bearing point.

This is the structured version of a known failure mode: a session that
iterates in-place fixes on a contradicting plan loops. The September 2026
mid-turn-injection incident looped that way - a session kept reconstructing
its world model after incoming mail contradicted its in-flight plan state.
An unaudited iteration on a contradicting plan fails the same way.

## Boundaries

- The revision self-check (thatch-plan-refinement loop step 4) is a
  same-context check of the revision DIFF against the plan it edits; you are
  a whole-plan read. Both run.
- Citation truth is out of scope: a wrong citation is the Evidence audit's
  finding, not yours.

## Related skills

- **`thatch-plan-refinement`** - the refinement loop that runs this audit
  every round and gates consensus on its verdict. Its revision self-check
  (loop step 4) is the same-context diff check this audit complements.
- **`thatch-plan-evidence`** - the sibling audit (exhaustive citation
  sweep). Consensus requires evidence audit PASS and consistency audit PASS.
