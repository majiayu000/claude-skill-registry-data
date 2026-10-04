---
name: conventions
description: Per-language coding conventions for this project. The implementer writes code that satisfies them; the reviewer checks against them and classifies each violation by its severity tag.
---

# Conventions

The reference for the task's language is included below. It lists the conventions this
project has settled. Treat this as the operational contract, do not invent conventions
beyond the list.

## If you are implementing or fixing

Write code that satisfies every convention in the language reference. These are settled
choices, not suggestions.

## If you are reviewing

For each convention, judge whether the change violates it, and assign severity from the
convention's tag:

- A convention tagged **correctness** is a real defect the mechanical gate (format, lint,
  types) cannot catch. Raise a violation as a **Major** finding: it must be fixed before
  shipping.
- A convention tagged **advisory** is a subjective preference. Note a violation as **Minor**:
  it never blocks the ship and is not auto-fixed.

Do not raise findings for anything outside this list or the mechanical gate. Formatting,
lint, and type errors are the gate's job, not yours.
