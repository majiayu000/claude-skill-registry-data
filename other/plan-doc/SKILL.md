---
name: plan-doc
description: Translate a spec into a numbered, deterministic implementation plan under specs/. Trigger on:- plan this, write a plan, implementation plan, plan-doc, plan from spec, step-by-step plan.
argument-hint: "Path to the spec, or a feature description if no spec exists"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-opus-5
---

# Plan doc

Turns a spec (or raw feature description) into a numbered plan detailed enough that a
junior model executes every step without re-deriving anything. Output is **deterministic**:
no vague verbs, no missing file paths, no Verify step without an expected result.

## When to use this

- After `/designit` finalizes, to put the agreed plan on disk.
- On its own before `ExitPlanMode`, for anything bigger than a single edit.
- Skip for a one-file change nobody needs to re-read in six months.

## Procedure

1. **Read `.specify/memory/constitution.md`**, then the spec if one exists
   (`specs/NNN-<slug>/spec.md` with `status: accepted`, or the argument path).

2. **Take the plan number from the `specs/` index (`specs/README.md`), not from `ls`** —
   an abandoned plan keeps its number. The plan is `specs/NNN-<slug>/plan.md`, written
   from `.specify/templates/plan-template.md`, `status: authored`.

3. **Read the source files the plan will touch** — entry points, interfaces, tests —
   before describing any change to them. Never write a change against a file you haven't
   read.

4. **Write the plan** in the template's Context → Decisions → Out of Scope → Steps shape.
   Each step:
   - **One concern.** Not "add the model + wire the route + write tests" in one step.
   - **Files are exact paths.** Read the codebase first.
   - **Do names the function, signature, types, exact behaviour**, any constants introduced.
   - **Verify is a runnable command with an expected result.** `pytest -q …` → `1 passed`,
     not "tests should pass".
   - **Dependencies explicit** — if step 3 needs step 2's output, say so.

5. **Review gate.** Present the full plan text (not a summary) and ask *"Does this look
   right? Reply yes to keep it, or describe what to change."* Interactive gate per the
   constitution — the plan is already on disk, so a revision is an edit. Don't proceed
   to index it until confirmed.

6. **Index it** in `specs/README.md` — a plan without an index row does not exist. Status
   vocabulary is in the constitution.

## What not to do

- Never flip a row to `implemented` — that's `finalize`'s job, so the status and the
  ledger entry land together.
- Never renumber, rename or delete a plan file to reflect a status change.
- Never write a Verify line that can't actually be run.
