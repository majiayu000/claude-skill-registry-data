---
name: kpa-find-spec-mismatches
description: Find 3 mismatches between OpenSpec specifications and actual implementation, ranked by severity
context: fork
agent: Sonnet
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Find 3 mismatches between the OpenSpec specifications and the actual implementation, ranked by severity.

## Steps

1. List all spec files in `openspec/specs/*/spec.md`.
2. Find spec files which don't have a last verified date in the past week.
3. For each spec that hasn't been verified in the last week, read the spec file and identify the **requirements** and **scenarios** (GIVEN/WHEN/THEN).
4. For each requirement, find the corresponding implementation files in the codebase (components, API routes, lib functions, hooks, tests).
5. Compare the spec against the implementation. Check each scenario against what the code actually does.
6. Mark the specs you have verified successfully with the date verified (today's date).
7. Report mismatches found (see format below).

## What Counts as a Mismatch

### Behavioral mismatches (highest value)
- A scenario says THEN X happens, but the code does Y instead
- A scenario says WHEN condition, but the code doesn't handle that condition
- A scenario specifies exact text/labels, but the UI renders different text
- A scenario specifies a specific route, but the route doesn't exist or behaves differently
- A scenario specifies an ordering of elements, but the code renders them in a different order

### Missing implementations
- A requirement exists in the spec but has no corresponding code at all
- A scenario describes behavior that is entirely unimplemented

### Extra behavior not in spec
- The code does something significant that contradicts or goes beyond what the spec describes (only flag this if it seems like a bug, not just an undocumented enhancement)

### What does NOT count as a mismatch
- Minor wording differences that don't affect behavior
- Implementation details the spec intentionally leaves open
- Test coverage gaps (that's a separate concern)
- Code quality issues (that's a separate concern)

## Report Format

For each mismatch found, report:

- **Severity**: Critical / High / Medium / Low
  - Critical: Feature is broken or behaves opposite to spec
  - High: Significant behavior doesn't match spec
  - Medium: Minor behavioral difference or missing edge case
  - Low: Cosmetic difference (labels, ordering, styling)
- **Spec**: Which spec file and requirement/scenario
- **Expected** (from spec): What the spec says should happen (quote the relevant GIVEN/WHEN/THEN)
- **Actual** (from code): What the code actually does, with file path and line number(s)
- **Recommendation**: What would need to change to match the spec (brief)

## Strategy Tips

- Start with specs that have very specific, testable assertions (exact text, exact routes, exact ordering) — these are easiest to verify.
- Read the actual component/page code, not just tests — tests may also be wrong.
- Pay close attention to: label text, route paths, status codes, error messages, conditional logic, and UI element ordering.
- Don't just grep for keywords — read the code paths to understand the actual runtime behavior.
- Use parallel reads to check multiple specs efficiently.

## Notes

- Focus on real, verifiable mismatches — not style preferences or ambiguous interpretations.
- If a spec is vague enough that the implementation could reasonably satisfy it, it's not a mismatch.
- Do NOT fix the issues, only report them.
