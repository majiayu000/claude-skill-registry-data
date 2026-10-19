---
name: debugging-workflow
description: >
  Systematically reproduce, isolate, diagnose, and resolve software bugs using
  hypothesis-driven debugging. Use when diagnosing failing test suites, tracing
  unhandled exceptions, isolating regressions with git bisect, performing root
  cause analysis (RCA), or writing regression tests to prevent recurrence.
compatibility: >
  Agent Skills-compatible coding agents diagnosing software defects across languages.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "debugging, rca, git-bisect, troubleshooting, regression-testing, testing"
  topics: "software-development, testing, devtools"
---

# Hypothesis-Driven Debugging Workflow

Debugging is not a trial-and-error guessing game. It is a scientific, evidence-based process of observation, hypothesis formation, experimental isolation, root-cause identification, and regression verification. Never modify code blindly hoping that an issue disappears.

## Core Rules

1. **Reproduce the bug reliably first**: Do not write fixes for an issue you cannot reproduce. Create a minimal reproduction script or failing unit test.
2. **Formulate a falsifiable hypothesis**: Before modifying any code, explicitly state: *"I hypothesize the crash occurs because function X receives `null` when input Y is empty."*
3. **Change one variable at a time**: If a test fails to confirm the hypothesis, immediately revert the change before trying another.
4. **Isolate regressions with `git bisect`**: If something worked yesterday but is broken today, use binary search across git commits to locate the exact breaking commit.
5. **Always write a regression test before fixing**: The fix is only complete when the new test fails without the fix and passes with it.
6. **Understand the root cause, not just the symptom**: Don't just slap an `if (x != null)` bandage over a symptom if the real bug is that an upstream factory generated an invalid object.

---

## 1. The 6-Step Systematic Debugging Cycle

```
1. Reproduce: Build a minimal, reliable reproduction script or unit test.
      │
      ▼
2. Isolate: Narrow the search space (git bisect, stack traces, binary search in code).
      │
      ▼
3. Hypothesize: State a specific, testable explanation for the observed failure.
      │
      ▼
4. Experiment: Add focused assertion, log statement, or debugger breakpoint.
      │
      ├──> [Hypothesis Disproven] ──> Revert test change, form new hypothesis.
      │
      ▼ [Hypothesis Confirmed]
5. Fix Root Cause: Implement minimal, clean fix addressing root mechanism.
      │
      ▼
6. Verify & Prevent: Run regression test; verify full test suite passes.
```

---

## 2. Isolating Regressions with `git bisect`

When a known regression occurred between two points in Git history:

```bash
# 1. Start bisect
git bisect start

# 2. Mark current broken commit
git bisect bad

# 3. Mark last known good commit or tag
git bisect good v1.2.0

# 4. Git automatically checks out midpoint commits.
# Test the build/reproduction command:
pytest tests/test_parser.py
# If test fails:
git bisect bad
# If test passes:
git bisect good

# 5. Git announces the culprit:
# "[sha] commit message is the first bad commit"

# 6. End bisect and return to original branch
git bisect reset
```

Automating with `git bisect run`:
```bash
git bisect start HEAD v1.2.0
git bisect run pytest tests/test_parser.py
# Runs automatically in seconds until finding the guilty commit!
```

---

## 3. Creating a Minimal Reproduction Case

Strip away unrelated modules, database fixtures, and external network dependencies until you have the smallest possible script that triggers the failure:

```python
# reproduction.py
from my_app.core import parse_query

# Demonstrates crash: unescaped quotes in filter parameter
def test_reproduce_crash():
    raw_query = 'filter="name=O\'Connor"'
    result = parse_query(raw_query)  # Crashes with QuerySyntaxError
    assert result is not None

if __name__ == "__main__":
    test_reproduce_crash()
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| "Shotgun Debugging" (changing multiple files at once) | Creates new bugs and masks the true root cause | Change one variable, test, revert if inconclusive |
| Symptom patching (`if x is None: return`) | Propagates invalid state deeper into application | Fix where the invalid data was created |
| Fixing without a regression test | Bug re-emerges in the next release cycle | Write failing test first, then apply fix |
| Discarding reproduction scripts | Future maintainers cannot verify the fix | Commit the reproduction as a permanent unit test |
| Guessing instead of reading stack traces | Wastes hours looking at the wrong subsystem | Read full stack trace from bottom to top |

---

## 5. Verification Checklist

- [ ] Bug is captured in an automated, failing regression test.
- [ ] Root cause mechanism is understood and documented in commit message.
- [ ] Applied fix makes the regression test pass.
- [ ] Full existing test suite continues to pass (no unintended side effects).
- [ ] Temporary debug prints, logs, or breakpoints have been removed.
