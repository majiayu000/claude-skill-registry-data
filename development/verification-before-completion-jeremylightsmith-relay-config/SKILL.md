---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, or to express satisfaction, or before committing/pushing/opening a PR or moving to the next task.
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

    NO COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

Before claiming any status or expressing satisfaction:

1. **IDENTIFY** the command that proves the claim.
2. **RUN** it fresh and in full (for this project, the gate is `mix precommit` — compile
   warnings-as-errors, format, credo --strict, sobelow, deps.audit, full test suite).
3. **READ** the full output; check the exit status; count failures.
4. **VERIFY** the output actually confirms the claim.
5. **ONLY THEN** make the claim — and state it *with* the evidence.

Skip any step = lying, not verifying.

## Common Failures

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | Test output: 0 failures | A previous run, "should pass" |
| Precommit clean | `mix precommit` exit 0 | "the focused test passed" |
| Bug fixed | Test the original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red → green cycle verified | Test passes once |
| Subagent completed | `git diff` shows the changes | Subagent reports "success" |
| Requirements met | Line-by-line checklist vs the plan | Tests passing |

## Red Flags — STOP

Using "should," "probably," "seems to" · expressing satisfaction before verifying ("Great!",
"Perfect!", "Done!") · about to commit/push/PR without running the gate · trusting a subagent's
success report · relying on a partial check · "just this once" · tired and wanting it over ·
**any wording that implies success without having run the verification.**

## Rationalizations

| Excuse | Reality |
|---|---|
| "Should work now" | Run the verification. |
| "I'm confident" | Confidence ≠ evidence. |
| "Credo passed" | A linter isn't the compiler or the test suite. |
| "The subagent said success" | Verify independently — check `git diff`. |
| "I'm tired" | Exhaustion ≠ excuse. |
| "Partial check is enough" | Partial proves nothing. |
| "Different words, so the rule doesn't apply" | Spirit over letter. |

## Key Patterns

**Tests / precommit:** `[run mix precommit] [read: 0 failures, exit 0]` → "precommit passes."
Not: "should pass now."

**Regression test (Red-Green):** write → run (pass) → revert the fix → run (MUST fail) →
restore → run (pass). Not: "I wrote a regression test" without the red-green proof.

**Requirements:** re-read the plan → make a checklist → verify each item → report gaps or
completion. Not: "tests pass, so it's done."

**Subagent delegation:** subagent reports success → check `git diff` → verify the changes →
report the actual state. Not: trust the report.

## The Bottom Line

Run the command. Read the output. THEN claim the result. This is non-negotiable.
