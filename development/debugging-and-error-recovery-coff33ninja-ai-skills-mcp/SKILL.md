---
name: debugging-and-error-recovery
description: Enforces structured debugging workflow — reproduce, localize, reduce, fix, guard. No fix until root cause is identified with file:line evidence. One-change-at-a-time hypothesis testing. Prevents surface-level fixes and random guessing.
---

# Debugging & Error Recovery

## Problem it solves

Debugging without structure wastes time and introduces regressions. Common failure modes:
- Applying surface-level fixes without identifying root cause
- Random guessing ("maybe it's this, let's try it")
- Making multiple changes at once and not knowing which fixed it
- Fixing the symptom but not the underlying cause
- Introducing new bugs from incomplete fixes
- Wasting tokens on ineffective debugging loops

## Protocol

### 1. The Iron Law: no fix without root cause

Before any code change, identify the root cause with:
- **File**: which file contains the bug
- **Line**: the specific line or range
- **Evidence**: why this line causes the failure (trace the data/call flow two levels deep)

If you cannot point to a file:line with evidence, you have not found the root cause. Keep investigating.

### 2. Reproduce first

Before fixing, reproduce the bug:
- What exact input/action triggers it?
- What is the expected behavior?
- What is the actual behavior?
- Can you reproduce it consistently?

If you cannot reproduce it, you cannot verify the fix works.

### 3. Localize

Isolate the bug to the smallest possible scope:
- Which component/module?
- Which function?
- Which line?
- What are the relevant input values at failure point?

Use tools strategically:
- Read error messages completely (not just the first line)
- Check logs, stack traces, and return codes
- Add targeted debug output (print/trace) — remove after fix
- Check recent changes (git diff, git log) that may have introduced the bug

### 4. Reduce

Create the minimal reproduction:
- Strip away unrelated code until only the failing case remains
- Verify the stripped version still fails (confirms you've isolated the right cause)
- If you can't reduce it, you may not understand the bug well enough

### 5. Fix one change at a time

- Make exactly one change
- Test immediately — does it fix the issue?
- If no, revert and try the next hypothesis
- If yes, verify the fix doesn't break related functionality

Do NOT batch multiple attempted fixes. One change, one test, repeat.

### 6. Guard against regression

After the fix:
- Add a test that reproduces the original bug (it should now pass)
- Run existing tests to verify nothing broke
- Check for similar patterns elsewhere in the codebase
- Document the root cause and fix (commit message should explain why, not just what)

### 7. When stuck

If the root cause isn't found within 3-5 attempts:
- Take a step back — what assumptions might be wrong?
- Explain the problem out loud (rubber duck)
- Check if the bug is in a dependency, not your code
- Check environment differences (dev vs prod, OS versions, config)
- Ask for help with specific: "I expected X but got Y when I did Z"

## Detection triggers

Activate when:
- User reports a bug or unexpected behavior
- Tests are failing unexpectedly
- Error messages appear in output
- Code produces wrong results
- User says "debug", "fix this", "something is broken", "why is this happening"

## When NOT to use

- Adding a new feature (use spec-driven-development + test-driven-development)
- Code review (use code-review)
- User explicitly says "just patch it, don't investigate"
- Known issues with documented workarounds

## Cross-references

- **spec-driven-development** — Write a spec for the fix before debugging. Defines what "fixed" looks like.

- **test-driven-development** — After finding root cause, write a failing test that reproduces it, then fix (RED-GREEN pattern for bugs).

- **code-review** — After fixing, submit for review. Review checks root cause analysis and test coverage.

- **verify-and-cite** — Verify claims about root cause with evidence. Don't guess.

- **anti-premature-termination** — Do not declare a bug fixed until root cause is identified, fix is verified, and regression tests pass.

- **follow-existing-patterns** — Debug output should match the project's existing logging/tracing patterns. Remove debug code before committing.

- **anti-sycophancy** — If the user suggests a fix, do not agree without verifying. Test the hypothesis first.
