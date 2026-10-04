---
name: grill-me
description: Prompt me with questions, one at a time, until we have a shared understanding. Use this skill when a decision, plan, or spec is too ambiguous to act on without guessing.
user-invocable: true
---
# Grill Me

Grill me with questions one at a time with options and recommendations until we have a shared common understanding.

## Rules

- Do not use the ask/question tool; **ask in thread**.
- Distinguish each option with a selectable letter.
- If executing on a goal or a plan, pause execution until you receive a response.
- If updating documentation, update the doc(s) after each answer.
- Be sure to include all relevant information in the question; vague questions or ones which lack the context to elicit informed decisions are unacceptable.

Note that the intent of refining is to get to promotion-grade understanding for specs, reqs, implementation, etc. Detail matters; don't skimp on documenting it.
