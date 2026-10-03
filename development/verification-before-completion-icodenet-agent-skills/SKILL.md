---
name: verification-before-completion
description: >-
  Gate every completion claim behind executed evidence. Use before saying
  "done", "fixed", "works", "passing", "delivered", or "merge-ready" — for any
  code change, bug fix, refactor, or configuration change. Requires running the
  relevant command and observing the output in this session; code inspection
  alone never counts as verification.
---

# Verification Before Completion

"The code looks right" is not a result. A completion claim is a claim about **behavior**, and behavior is only known by executing something and reading the output.

## The rule

Before any completion claim:

1. **Name the claim precisely.** "Fixed the timeout bug" / "feature X delivered" / "refactor is behavior-preserving" — a vague claim can't be verified.
2. **Run the verifying command in this session.** The relevant test suite, the failing repro, the build, the endpoint call, the UI flow. Prefer the project's own package scripts. Stale results from earlier in the session don't count if the code changed since.
3. **Read the output, don't pattern-match it.** Exit code 0 with skipped tests is not a pass. A green suite that doesn't exercise the changed behavior is not evidence for the claim.
4. **Match evidence to claim.** Bug fix → the original repro no longer fails *and* a regression test passes. Feature → the user-visible behavior was exercised, not just unit internals. Refactor → the pre-existing suite passes unchanged.
5. **Report command + outcome verbatim.** State exactly what ran and what it showed. If something was skipped, say so.

## When verification cannot run

Environment broken, credentials missing, suite requires services that are down:

- Say the claim is **unverified** and why.
- State the exact command someone must run to complete verification.
- Do not soften to "should work" — the status is *unverified*, not *probably fine*.

## Common self-deceptions (reject all of these)

| Deception | Reality |
|---|---|
| "The change is simple, no need to run it" | Simple changes break builds daily |
| "Tests passed before my last small edit" | The last edit is the one that breaks |
| "The type checker is happy" | Types don't verify behavior |
| "I ran the unit tests" (for a user-visible bug) | The user's flow was never exercised |
| "Lint + build succeeded" | Neither executes the changed code path |
| "The logs look like it worked" | Find the assertion, not the vibe |

## Verification

- [ ] Claim stated precisely
- [ ] Verifying command executed after the final code change
- [ ] Output actually read; skips/warnings accounted for
- [ ] Evidence type matches claim type (repro for bugs, behavior for features, suite for refactors)
- [ ] Report includes command + observed result, or an explicit UNVERIFIED status
