---
name: purify
description: Katara bends the impurities out of the water and leaves it clear. Use for deslop, /deslop, "remove AI slop", "clean up this diff", or before every commit. Checks the branch diff against main and removes AI-generated code slop, such as needless comments, abnormal defensive checks, casts to any, and deep nesting, without changing behavior.
---

# Katara purifies the water

A waterbender can pull silt, salt, and poison out of water and leave the water itself untouched. Purify does that to a diff. It draws out what an agent added that does not belong, and keeps every drop of behavior.

## Scope

Check the diff against the base branch (default `main`, including the working tree) and remove the AI-generated slop the branch introduced. Touch only lines the branch changed.

## What to draw out

- Extra comments that are unnecessary or inconsistent with the file's local style. For a full comment pass, run `clear-water`.
- Defensive checks or `try`/`catch` blocks that are abnormal for a trusted code path. Guards belong at system boundaries (Boundary Discipline, Earth in `four-elements`).
- Casts to `any` used only to get past a type error. Fix the type instead (see `typescript-forms`).
- Deeply nested code that early returns would flatten.
- Any other pattern inconsistent with the file and the code around it.

## Rules

- Keep behavior unchanged unless you are fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- Run the nearby tests after the pass. Purify that breaks a test has poisoned the water.

## Reply

One to three sentences on what you removed.
