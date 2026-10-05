---
name: implement
description: Execute a specs/ plan end to end, one step at a time, then hand off to finalize. Trigger on:- implement, code this, follow the plan, build this, write tests.
disable-model-invocation: true
argument-hint: "plan path or target-project/module"
model: claude-sonnet-5
---

# Implement a plan

Executes a plan already authored by `plan-doc` at `specs/NNN-<slug>/plan.md`, then hands
the finished work to `finalize` to close out. Follows the plan exactly; flags ambiguity
instead of guessing.

## When to use this

- A `specs/NNN-<slug>/plan.md` exists with `status: authored`.
- Skip if no plan exists yet — run `plan-doc` first.

## Procedure

1. **Read `.specify/memory/constitution.md`**, then the plan in full. Identify every
   deliverable. If the user named a plan, read it directly; otherwise take the one with
   `status: authored` from `specs/README.md` and confirm which to build.

2. **Work the plan's Steps via the constitution's Item-execution loop** — in order, Do
   then Verify, one at a time. On an ambiguous or conflicting step, park a gate
   (`specs/NNN-<slug>/gates/NNN-<what>.md`) rather than guessing; you are long-running,
   so parking is fine.

3. **Write tests alongside each unit**, matching the style already in the codebase (look
   at one existing test file first). Run them as part of that step's Verify.

4. **Close out via `/finalize`** — done-checks, changelog, version, plan-index flip to
   `implemented`, commit on confirm. Don't duplicate any of that here. (A setup with its
   own ledger contract runs its overlay — e.g. `/land-feature` — instead.)

## What not to do

- Don't invent scope beyond the plan's Steps — new ideas go back to `plan-doc`.
- Don't make architectural decisions mid-build — park a gate (step 2).
- Don't skip a step's Verify because it "obviously works".
- Don't assert a function's return shape from memory — read it first. When the test is
  about *absence*, assert shape-independently (serialize the payload and search it).
