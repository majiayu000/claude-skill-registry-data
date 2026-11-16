---
name: verify-before-done
description: "Use before claiming any task is complete, fixed, passing, or ready. Triggers on: 'done', 'fixed', 'tests pass', 'should work now', 'looks good', 'complete', 'finished', 'ready to merge', or any expression of satisfaction before showing evidence."
---

# Verify Before Done Skill

A claim without evidence is a guess. This skill enforces evidence before assertion.

This is the skill-layer complement to the Truth Gate hook (`core/hooks/truth-gate-guard.sh`).
The hook warns on claim verbs in output. This skill runs the actual verification.

## The Rule

```
NO COMPLETION CLAIM WITHOUT FRESH VERIFICATION OUTPUT IN THIS SAME RESPONSE.
```

If the verification command was not run in this message, you cannot claim it passes.

## When to use this skill

ALWAYS before any of these:
- Saying "done", "fixed", "complete", "finished", "ready"
- Expressing satisfaction: "looks good", "should work", "that should do it"
- Committing or pushing
- Moving to the next task
- Telling the user the bug is resolved

## Verification checklist

Run the relevant checks and show their output:

### Tests
```bash
# Run and show full output — do not truncate
bash core/tests/hooks/run-hook-tests.sh 2>&1
```
Claim "tests pass" only if output shows `0 failed`.

### Hook syntax
```bash
bash -n core/hooks/*.sh 2>&1 && echo "syntax OK"
```
Claim "syntax clean" only if output shows "syntax OK".

### Git state
```bash
git diff --stat
git status --short
```
Show actual output. "No uncommitted changes" requires empty output.

### For bug fixes — reproduce before claiming fixed
```bash
# Run the specific command/test that was failing
# Show it passes now
# If possible, show it would have failed before (git stash → run → git stash pop)
```

## Output format

After running checks, report like this:

```
Verification:
- tests: [N/N pass | FAIL: list failures]
- syntax: [OK | errors: list]
- git: [clean | N files changed: list]
- bug: [reproduced and resolved | not verified]

Status: DONE ✓   (or)   NOT DONE — [what's still failing]
```

## Red flags — stop and verify before continuing

- You are about to type "done", "fixed", "complete"
- You feel satisfied with the result
- The last thing you did was edit a file
- You're about to switch to a new task
- You're about to run `git commit`

**Any of the above = run this skill first.**

## Common rationalisations — ignore them

| What you're thinking | What to do instead |
|---------------------|-------------------|
| "I just changed one line, clearly it works" | Run the test |
| "The test passed before, it still passes" | Run it fresh |
| "Agent said success" | Verify independently |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
