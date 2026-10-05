---
name: designit
description: Iteratively drill a feature, idea or requirement into a locked spec, then hand it to /plan-doc. Trigger on:- designit, design this, brainstorm, design doc, architecture for, how should we build, what's the approach.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-opus-4-8
---

# Designit

Starts from a single high-level plan and progressively zooms in, one round at a time,
until the details are locked. **No coding** — the output is a decision, not an
implementation.

## When to use this

- Before building anything whose shape isn't already obvious.
- Skip for a change you could describe fully in one sentence — go straight to the edit,
  or to `/plan-doc` if it still deserves a record.

## Procedure

1. **Read `.specify/memory/constitution.md`.**

2. **State your assumptions upfront**, and ask clarifying questions rather than guessing
   at anything that would change the design. Read the codebase to ground them — do not
   guess the tech stack.

3. **Draft the design at one level of detail**, then present it and stop. This is a
   human gate (interactive — answered in-session per the constitution's gate protocol).
   The user decides: **redo** / **confirm and continue** (zoom in one level) / **confirm
   and finalize**.

4. **Repeat** until every Critical/Major decision is settled or the user says "confirm
   and finalize". Each round adds real resolution — structure, boundaries, libraries,
   the decisions and their reasons — never a restatement of the last.

5. **On finalize, write the spec** to `specs/NNN-<slug>/spec.md` from
   `.specify/templates/spec-template.md`, `status: accepted`. Take `NNN` from the
   `specs/` index. Then hand off: `/plan-doc` reads this spec and writes the plan.

## The spec must carry

Produce it in the template's shape so the write is a copy, not a rewrite:

- **Problem** — why the work exists, what is currently true, the constraint that forced
  the design.
- **Considered Approaches** and the **Decision** with its reason — the choices that were
  actually contested.
- **Design** — enough detail to plan against without re-deriving it.
- **Non-Goals** — what was deliberately left out, so it isn't re-litigated mid-build.

## What not to do

- Don't write code, and don't edit the target files "to check" — read only.
- Don't advance a round without the user's explicit word; "looks good" on one level
  isn't approval of the next.
- Don't leave a decision whose consequences you haven't drilled into.
