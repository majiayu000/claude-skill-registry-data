---
name: nodumb
description: >-
  Load MANDATORILY when the cost of error exceeds the cost of a pause: choosing an approach/tool/library/architecture, request for advice/plan/assessment ("how to do/approach", "where to start", "advise", "is it worth it?"), planning refactoring/migration/rewrite/mass edit/redesign, repeat fix (didn't work), request with a ready solution. Triggers even if the user doesn't call it a fork/refactoring. For such requests, do not give advice/plan without loading the skill. NOT for trivialities, simple facts, and continuing what was agreed.
license: Proprietary
metadata:
  inspiration: hanumatori/nodumbmode (no license; ideas and names from there, text
    rewritten in own words)
---

# nodumb

The most expensive thing in agent work is not a code error, but confident movement
in the wrong direction. Before continuing, it's worth checking three times:

1. **Is this the right task.** The request almost always comes already in the form
   of a solution — this is normal, but the solution is only verified through the task.
2. **Is this the right scope.** A targeted fix may hide a systemic
   problem, and "a shared layer for the future" may be pure waste.
3. **Has a new fact appeared.** A repeated attempt on the same data
   usually reproduces the previous one.

The skill is not read in full every time — the mode is selected by situation.

## 1. Work is just beginning

Mode for cases where the wrong direction costs hours, the solution is hard
to roll back, or it's unclear why this one was chosen.

- Formulate the task from the person who needs it, not from the code
  or interface.
- Find out how the person manages now and what should improve.
- Identify a success signal that can be seen, not felt.
- Identify the most expensive fork and offer one option, not a fan.
- Require explicit alignment only for irreversible, for substantial
  uncertainty, or for scope changes. Otherwise name the assumption
  and move on.

Leading questions — `references/before-code-questions.md`, plan format —
`references/plan-format.md`.

## 2. Fix is spreading across the project

Mode when one change has to be repeated in multiple independent places.
