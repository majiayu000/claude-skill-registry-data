---
name: debug-systematically
description: Use when a bug resists the first fix — reproduce it, bisect to the introducing change, test one hypothesis at a time, fix the root cause, and add a regression test.
---

# Debug Systematically

Replaces the "try things until it works" loop with a falsifiable process (The Pragmatic Programmer).
Pairs with [write-clean-tests](../write-clean-tests/SKILL.md) — the regression test is the proof the bug
cannot return.

## 1. Reproduce

A bug you cannot reproduce you cannot fix or verify. Capture the exact input, environment and steps that
trigger it; if it is intermittent, add logging or run the loop until it fails. State the symptom in one
sentence, not the suspected cause.

## 2. Bisect to the introducing change

```bash
git log --oneline -20
git bisect start 2>/dev/null   # only if you have a known-good and known-bad commit
```

Narrow the search by halves: the commit that introduced it, the one input field that matters, the one
boundary value that flips it. The change that introduced the bug is the most reliable clue to its cause.

## 3. Test one hypothesis at a time

- Form a falsifiable prediction ("if X is the cause, then changing Y fixes it and nothing else does").
- Change one thing, observe, record. Never change several at once — you will not know which one worked.
- Prefer the simplest explanation that fits all the evidence; resist the theory you already believe.

## 4. Fix the root cause

Fix the *why*, not the symptom. Patching the output where it shows up leaves the cause to resurface
elsewhere. If the fix feels like a workaround, the cause is one level deeper.

## 5. Add a regression test

Write the test that fails on the old code and passes on the fix. That test is the proof the bug cannot
return, and the reviewer's evidence the fix is real.

## Verify

The symptom is gone under the exact reproduction, the bisect points to one change, and the regression
test fails on the reverted fix and passes on it. State the root cause and the fix in the note.

## When to deviate

- An incident in production: stop the bleeding first (roll back, feature flag off), then debug the cause
  off the hot path.
- A bug that reproduces only under a dependency's bug: fix or pin the dependency, do not build a shim.
