---
name: verification-before-completion
description: Requires running verification commands and reading their actual output before any claim that work is complete, fixed, or passing. Use when about to say done, tests pass, bug fixed, or build works; before committing, creating a PR, marking a task complete, or trusting a subagent's success report.
---

# Verification Before Completion

## Overview

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

**Announce at start:** "Using opm:verification-before-completion before claiming this is done."

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Claim -> Required Evidence

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Type check clean | Type checker output: 0 errors | Editor shows no squiggles |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test of original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Subagent completed | `git diff` / `git log` shows the changes | Agent reports "success" |
| Requirements met | Line-by-line checklist against spec/plan | Tests passing |
| Plan task complete | Task's own test steps run, output read | Implementer said DONE |
| No silent failures | Error paths exercised or reviewed (`silent-failure-hunter` subagent for large diffs) | "I handled errors" |
| Safe to ship | `security-reviewer` subagent or `/security-review` on the diff | "Nothing sensitive touched" |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit, push, or open a PR without verification
- Trusting a subagent's success report without checking the diff
- Relying on partial verification (one test file, one platform)
- Thinking "just this once"
- Tired and wanting the work to be over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification. |
| "I'm confident" | Confidence is not evidence. |
| "Just this once" | No exceptions. |
| "Linter passed" | Linter is not the compiler, and neither is the test suite. |
| "Agent said success" | Verify independently: read the diff, run the tests. |
| "I ran it earlier" | Earlier is before the last edit. Run it again. |
| "I'm tired" | Exhaustion is not an excuse. |
| "Partial check is enough" | Partial proves nothing about the rest. |
| "Different words so the rule doesn't apply" | Spirit over letter. |
| "The reviewer approved it" | Review is not execution. Run the command. |

## Key Patterns

**Tests:**
```
OK:  [Run test command] [See: 34/34 pass] "All tests pass"
BAD: "Should pass now" / "Looks correct"
```

**Regression tests (TDD red-green, see opm:tdd-workflow):**
```
OK:  Write -> Run (pass) -> Revert fix -> Run (MUST FAIL) -> Restore -> Run (pass)
BAD: "I've written a regression test" (without red-green verification)
```

**Build:**
```
OK:  [Run build] [See: exit 0] "Build passes"
BAD: "Linter passed" (linter does not check compilation)
```

**Requirements:**
```
OK:  Re-read plan/spec -> Create checklist -> Verify each item -> Report gaps or completion
BAD: "Tests pass, phase complete"
```

**Subagent delegation:**
```
OK:  Agent reports success -> Check git diff -> Run the task's tests -> Report actual state
BAD: Trust the agent's report
```

## When To Apply

**ALWAYS before:**
- ANY variation of a success or completion claim
- ANY expression of satisfaction
- ANY positive statement about the state of the work
- Committing, PR creation, task completion
- Moving to the next task in `opm:executing-plans`
- Delegating to, or accepting results from, subagents

**The rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion or correctness

## Reporting Format

When the evidence is in, report it, not just the conclusion:

```
Verification:
- `npm test` -> 112 passed, 0 failed (exit 0)
- `npm run lint` -> 0 errors, 0 warnings
- `npm run build` -> exit 0
- Spec checklist: 7/7 requirements have a passing test
```

If any line fails, the work is not done. Say so, with the failing output, and keep going.

<!-- Adapted from obra/superpowers (MIT) -->
