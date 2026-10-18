---
name: verification-before-completion
description: Use when about to report a task, story, build, or Definition of Done condition as complete, or before checking off any item in a plan or checklist.
---

# Verification Before Completion

"Looks right" is not evidence. Before marking anything done, run the actual check — the test, the
build, the exact command a Definition of Done condition names — and read its output.

## Guardrails

- Never report a status from memory of writing the code. Report it from the last command's output.
- A check that cannot run (missing tool, no environment, out of scope for this session) is not the
  same as a passed check. Say which check did not run and why; do not round it up to "done".
- Partial success is not success. If three of four tests pass, the task is not complete — say which
  one failed.
- A Definition of Done condition that names a command is checked by running that command, not by
  reading the code it would exercise.
- If a condition checks an excluded boundary (a file, an area the plan marked out of scope), verify
  it by scanning the whole diff, not just the files the task touched — the boundary is exactly the
  place a stray change would hide.

## What this is not

Not a call for more testing than the task needs. A one-line change verified by reading its one line
and the test that already covers it is enough. The rule is about evidence, not volume: whatever
level of checking the task warrants, that checking has to have actually happened before the words
"done" or "complete" appear.

## Integration contract

When used by `plan-driven-build`, receive the Definition of Done and verification report as inputs.
Return one result per condition with the command, exit status, and evidence path. A failed or
unavailable check keeps the condition unverified and tells the orchestrator whether the next action
is debugging, another bounded verification attempt, or human intervention.
