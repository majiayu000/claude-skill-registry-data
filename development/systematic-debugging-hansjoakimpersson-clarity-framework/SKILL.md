---
name: systematic-debugging
description: Use when investigating a bug, test failure, crash, or unexpected behavior, before proposing or applying a fix.
---

# Systematic Debugging

A fix proposed before the failure is reproduced and understood is a guess. Guesses that happen to
work hide the actual defect until it resurfaces somewhere else.

## Guardrails

- Reproduce the failure first. If it cannot be reproduced, say so and stop guessing at fixes — a fix
  for a failure you cannot trigger cannot be verified either.
- State the hypothesis before changing code: what you believe is wrong, and what evidence supports
  it. A hypothesis grounded in "the log line before the crash" is worth more than one grounded in
  "this looks suspicious".
- Trace to the root cause, not the first symptom. A crash caused by a missing check at the line it
  surfaced is a different defect from the same crash caused by bad state set two calls earlier — fix
  the second; the first check is still worth adding, but it is not the fix.
- Change one thing at a time. Several simultaneous speculative changes make it impossible to tell
  which one — if any — addressed the actual cause.
- After the change, re-run the exact reproduction that failed before. A fix that was never re-run
  against its own failing case is unverified — see the `verification-before-completion` skill.
- When a defect looks likely to recur across a family of similar units (sibling test classes,
  parallel endpoints, repeated migrations), check the whole family before declaring the fix
  complete — a fix that only covers the instance found first will resurface on the next sibling.

## When not to use

A one-line typo with an obvious cause does not need a hypothesis write-up. The discipline scales
with the uncertainty: a bug that took ten minutes to spot needs a sentence of reasoning, not a
report.

## Integration contract

When used by `plan-driven-build`, receive the bounded failure output, phase, and reproduction
command. Return the root cause, `failure_class`, `retryable` decision, evidence path, and one next
action. Do not change the retry loop or dispatch another agent; the orchestrator owns those choices.
