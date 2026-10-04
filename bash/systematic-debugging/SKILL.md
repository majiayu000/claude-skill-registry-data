---
name: systematic-debugging
description: >
  4-phase root cause investigation methodology for bugs and unexpected
  behavior. Use when tests fail, errors occur, behavior is unexpected,
  or a fix attempt has failed. Prohibits guessing and symptom-fixing.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "debugging an error"
  - context: "test failure"
  - context: "unexpected behavior"
  - context: "a fix attempt failed"
  - command: "/debug"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - test-driven-development@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
    phase_phrasing: "Let's investigate this together. First, we need to find the root cause — not guess at a fix."
  gemini:
    enforcement_style: "structured-checklist"
    phase_phrasing: "PHASE GATE: ☐ Root cause identified ☐ Evidence collected ☐ Hypothesis formed ☐ Fix verified"
  gpt:
    enforcement_style: "directive-imperative"
    phase_phrasing: "You MUST complete root cause investigation before proposing any fix. Do NOT skip phases."
author: codehands-core
signed: true
tier: 1
---

## Overview

Systematic debugging prevents the #1 agent anti-pattern: guessing at fixes. Instead of trying random changes and hoping something works, this skill enforces a scientific method — observe, hypothesize, test, confirm — that finds the actual root cause before any code changes.

## When to Use

- When a test fails and the cause isn't immediately obvious
- When behavior differs from specification
- When a previous fix attempt made things worse
- When the same bug keeps reappearing after "fixing"
- When an error message doesn't clearly indicate the problem
- NOT for typos, syntax errors, or obvious one-line fixes

## Process

### Phase 1: Root Cause Investigation

> **STOP. Do not write any fix code until you complete this phase.**

1. **Reproduce the bug deterministically.** Run the failing test or trigger the error. Save the exact output.
2. **Gather evidence.** Read the error message, stack trace, logs, and relevant source code. Do NOT skim — read carefully.
3. **Trace the execution path.** Starting from the error, trace backward through the call stack:
   - What function failed?
   - What called that function?
   - What data was passed?
   - Where did the data come from?
4. **Identify the divergence point.** Where does actual behavior diverge from expected behavior? This is the root cause location — NOT necessarily where the error is thrown.

### Phase 2: Pattern Analysis

5. **Check for related symptoms.** Does this bug manifest in other places? Search for:
   - Similar code patterns in the codebase
   - The same function called from other locations
   - Similar error types in recent history
6. **Check recent changes.** Did anything change recently that could have introduced this?
   ```bash
   git log --oneline -20
   git diff HEAD~5 -- <affected-files>
   ```
7. **Check assumptions.** Which assumptions in the failing code are actually verified? Common false assumptions:
   - "This input will never be null/undefined"
   - "This API always returns the expected format"
   - "This function is pure / has no side effects"
   - "The order of operations is guaranteed"

### Phase 3: Hypothesis & Testing

8. **Form a hypothesis.** State clearly: "The bug occurs because X causes Y when Z."
9. **Design a verification test.** How can you confirm the hypothesis WITHOUT changing production code?
   - Add a reproduction test
   - Add logging/print statements to confirm the path
   - Inspect state at the divergence point
10. **Verify the hypothesis.** Run the verification. Does the evidence support your hypothesis?
    - If YES → proceed to Phase 4
    - If NO → return to Phase 1 with new evidence

### Phase 4: Implementation

11. **Write a reproduction test.** This test MUST fail with the bug present and pass after the fix (Prove-It Pattern from `codehands:test-driven-development`).
12. **Implement the minimal fix.** Change the fewest lines possible to address the root cause.
13. **Run the reproduction test.** It MUST pass.
14. **Run the full test suite.** Nothing else should break.
15. **Add defense-in-depth.** After fixing the immediate cause, add guardrails:
    - Input validation at the boundary where invalid data entered
    - Type checking or assertions that would catch this class of bug earlier
    - Error messages that would have made this easier to diagnose

### Escalation Rule

> **If you've attempted 3+ fixes and the bug persists, STOP fixing. Question the architecture.**
>
> Three failed fixes is evidence that the problem is structural, not local. Escalate to the human with:
> - What you've tried
> - What evidence you've gathered
> - Why you believe the architecture may need reconsidering

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I think I already know what the fix is" | If you know the fix, you should have no trouble proving it via the 4-phase process. Skip the process only if you want to risk wasting hours on a wrong guess. |
| "Let me just try this quick change" | "Quick changes" are the #1 source of regression bugs. One quick change leads to another, and soon you're 5 commits deep with no clear understanding of what you fixed or why. |
| "The stack trace points directly to the issue" | The stack trace points to where the error MANIFESTS, not where it ORIGINATES. The root cause is often 2-3 layers up. |
| "I'll add logging everywhere to find it" | Scattershot logging is Phase 1 avoidance. First trace the execution path mentally, THEN add targeted logging to verify your hypothesis. |
| "It's probably a race condition / timing issue" | "Probably" is not evidence. Can you demonstrate the race condition? Can you trigger it reliably? If not, you haven't identified the root cause yet. |
| "The error is in a library / not our code" | Libraries are invoked with YOUR inputs. The root cause is usually how you call the library, not the library itself. Check your inputs first. |
| "I need to refactor before I can fix this" | No. Fix the bug first with a targeted change. Then refactor with a green test suite. Refactoring while debugging creates two problems simultaneously. |

## Red Flags

- Changing code without first understanding why the current code fails
- Multiple "fix attempts" without a clear hypothesis for each
- "Shotgun debugging" — changing many things at once hoping something works
- Fixing the symptom (error suppression, try/catch) instead of the cause
- Not running the full test suite after a fix
- Declaring the bug fixed based on manual testing only
- Commit messages like "fix bug" or "try fix" without explaining the root cause

## Verification

- [ ] Root cause has been identified and can be stated in one sentence
- [ ] A reproduction test exists that fails without the fix and passes with it
- [ ] The fix addresses the root cause, not just the symptom
- [ ] The full test suite passes after the fix
- [ ] Defense-in-depth guardrails have been added
- [ ] The fix has been explained clearly (in commit message or PR description)
- [ ] If 3+ fix attempts were made, risk of architectural issue has been assessed

## See Also

- `codehands:test-driven-development` — Prove-It Pattern for bug fixes
- `codehands:verification-before-completion` — Confirm the fix actually works
- `codehands:code-review-and-quality` — Review the fix for quality
