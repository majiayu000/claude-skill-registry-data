---
name: verification-before-completion
description: Use before claiming work is complete, fixed, or passing, and before committing or opening a PR - run the actual verification command and read its output before making any success claim.
---

# Verification Before Completion

## Overview

**Core principle:** evidence before claims, always.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If the verification command hasn't been run in this turn, its result can't be claimed.

## The Gate

Before stating any status or expressing satisfaction with the result:

1. **Identify** what command actually proves the claim (`npm test`, `npm run lint`, `npm run build`, re-running the exact symptom that was reported as a bug)
2. **Run** the full command, fresh — not a cached memory of an earlier run
3. **Read** the full output: exit code, failure count, warnings
4. **Check** whether the output actually supports the claim
5. **Only then** state the claim, with the evidence attached

Skipping any step turns the claim into a guess wearing the words of a fact.

## Common Failures

| Claim | What it actually requires | Not sufficient |
|---|---|---|
| Tests pass | Fresh test run, 0 failures | "Ran it earlier", "should still pass" |
| Lint clean | Fresh linter run, 0 errors | Partial check, extrapolating from one file |
| Build succeeds | Fresh build, exit 0 | Linter passing (linter isn't the compiler) |
| Bug fixed | The original symptom re-tested and gone | "Code changed, should be fixed now" |
| A delegated task succeeded | Diff/output actually inspected | Trusting a subagent's self-reported "done" |

## Red Flags

- Reaching for "should", "probably", "seems to" in a completion claim
- Saying "Done!" / "Perfect!" before the command has been run this turn
- About to commit, push, or open a PR without a fresh check
- Trusting an agent's or tool's own success report without inspecting the actual diff/output
- "Just this once" — there's no once that's actually exempt

## Rationalization Table

| Excuse | Reality |
|---|---|
| "Should work now" | Run it and see |
| "I'm confident" | Confidence isn't evidence |
| "Linter passed" | Linter doesn't check compilation or test correctness |
| "The agent said it succeeded" | Verify independently — check the actual diff |
| "Partial check is close enough" | A partial check proves nothing about the untested part |

## Patterns

**Tests:** run → read `N/N pass` → *then* say "all tests pass". Never the reverse order.

**Regression test (red-green):** write the test → confirm it passes with the fix in place → temporarily revert the fix → confirm the test now fails → restore the fix → confirm it passes again. A regression test that was never seen failing hasn't proven anything.

**Build:** run the actual build command and check exit code — a clean linter run is not evidence the build compiles.

**Delegated work:** when a subagent or tool reports success, check the VCS diff or actual output yourself before repeating the claim upward.

## When to Apply

Always, before: any completion or success claim, any expression of satisfaction with the result, committing, opening a PR, moving on to the next task, or reporting a delegated task's outcome back to the user. Applies to paraphrases and implications of success just as much as the literal words "it works."
