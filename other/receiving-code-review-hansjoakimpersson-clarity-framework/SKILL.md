---
name: receiving-code-review
description: Use when code review feedback has come back on a change, before responding to or resolving any of it.
---

# Receiving Code Review

A review finding is a claim, not an order. Verify it before acting — but verifying is not the same
as dismissing it because a fix feels inconvenient.

## Guardrails

- Address or explicitly rebut every finding. Silence is not a decision anyone downstream can see;
  either fix it or state why no change is needed, in the same place the finding was raised.
- Do not mark a finding resolved without one of those two outcomes actually having happened. A
  status flip with no corresponding diff or explanation is the finding being hidden, not settled.
- When a finding conflicts with what the task or plan explicitly specified, that is a real
  disagreement to surface, not something to silently resolve in either direction. Say which side you
  are taking and why.
- Fix findings one at a time when they touch different concerns; batching an unrelated fix into a
  finding's diff makes the re-review harder than the original review.
- A finding that turns out to be right about a pattern beyond the current diff is worth a note for
  later, not scope creep into fixing everything it applies to right now.

## What this is not

Not a mandate to implement every suggestion verbatim. A reviewer can be wrong, out of context, or
proposing a preference rather than a defect — the obligation is to engage with the finding visibly,
not to comply with it unconditionally.

## Integration contract

When used by `plan-driven-build`, receive the review findings, task brief, and relevant diff. Return
one disposition per finding: `accepted`, `rejected`, or `needs-clarification`, with technical
evidence and the required fix or re-review scope. The orchestrator owns fix-round limits and human
gates; this skill owns the quality of each disposition.
