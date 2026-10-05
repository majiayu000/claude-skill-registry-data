---
name: debugging
description: Apply when diagnosing a bug, reproducing a failure, or performing root cause analysis. Covers systematic isolation, binary search, logging strategy, and hypothesis-driven investigation.
license: MIT
version: 1.0.0
tokens_target: 2000
triggers:
  - debugging
  - troubleshooting
  - root cause analysis
  - isolating bugs
loads_after: []
supersedes: []
---

# Sub-Skill: Debugging

**Purpose:** Systematic techniques for reproducing failures, isolating variables, and finding root causes without guessing. Complements `skills/tdd/SKILL.md` — a failing test is the best reproduction case.

---

## Rules

### Reproduction

1. **Reproduce before fixing.** Before changing any code, confirm you can trigger the failure on demand. A fix applied to an unreproduced bug is a guess, not a solution. Reference: ERR-2026-018
2. **Capture the minimal reproduction.** Reduce the failing scenario to the smallest input, fewest dependencies, and shortest code path that still exhibits the symptom. Smaller reproductions expose the cause faster and prevent regression.
3. **Write the reproduction as a test.** Encode the reproduction case as an automated test before touching production code. This locks in the failure signal and prevents silent regression. See `skills/tdd/SKILL.md`.

### Isolation

4. **Change one variable at a time.** Never modify multiple suspects simultaneously. Each change must be independently observable so you know which variable caused the change in behaviour.
5. **Use binary search on the call stack.** When the failure source is unknown, bisect: confirm the bug is present at the midpoint of the execution path, then recurse into the half that contains it. Avoid reading every line top-to-bottom.
6. **Prefer structured logging over print-debugging.** Add log statements at decision boundaries with structured key-value pairs (not free-form strings). Structured output is grep-able, diffable, and removable without side effects.

### Hypothesis and Root Cause

7. **State a falsifiable hypothesis before each experiment.** Write down: "I believe X causes Y because Z. If I change X, Y should disappear." Run the experiment. If the hypothesis is wrong, update your model before the next experiment.
8. **Distinguish symptom from cause.** The error message or stack trace is the symptom. The root cause is the incorrect assumption, missing guard, or wrong state that produced it. Never stop at the symptom — trace back to the decision that allowed the bad state to exist.
9. **Do not fix symptoms in isolation.** Patching the symptom without addressing the root cause produces a second bug that hides the first. Ensure the fix makes the root cause impossible, not just the observed symptom unlikely.

### Verification

10. **Verify the fix with the reproduction test.** After applying the fix, confirm the reproduction test now passes and no previously passing tests regressed. A fix that breaks other tests has introduced a new bug.
11. **Ensure the fix is observable.** After merging, confirm the symptom is gone in the target environment using the same signal (log line, metric, test) that first revealed the bug. Never declare a bug fixed without an observable confirmation.

---

## See also

- `skills/tdd/SKILL.md` — write the reproduction as a failing test first
- `skills/code-quality/SKILL.md` — narrow exception catches to avoid masking bugs (ERR-2026-016)
- `skills/error-log/SKILL.md` — errors that motivated rules in this skill

---

## Notes

- **Binary search applies to time too.** Use `git bisect` to find the commit that introduced a regression; do not read the full diff manually.
- **Logging is temporary.** Remove or gate debug log statements behind a flag before merging. Permanent debug noise degrades signal quality for the next investigation.
