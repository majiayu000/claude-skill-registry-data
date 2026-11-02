---
name: check-invariants
description: Run mechanically checkable invariants from the project overlay and report pass or fail.
disable-model-invocation: true
---

# Check Invariants

Read `.repo-context/invariants.md` and run each listed check.

## Rules

- Only run invariants with explicit commands.
- Report pass or fail per invariant.
- If an invariant is aspirational rather than mechanically checkable, say so and skip it.
- Use repo-relative paths only when presenting results.
