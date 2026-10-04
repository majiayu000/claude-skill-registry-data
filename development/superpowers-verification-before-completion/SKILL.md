---

name: superpowers-verification-before-completion
description: >
  Use before claiming any work is complete — requires fresh verification evidence before any
  assertion of success. Runs a 4-step verification gate: (1) identify the exact command proving
  the claim, (2) run it fully, (3) read complete output and exit code, (4) verify output supports
  the claim. Skipping steps is lying, not verifying. Also for: confirming linter-clean builds,
  validating regression tests with a red-green cycle, checking agent completion via VCS diff plus
  independent verification, and vetting any 'looks good' statements before committing or pushing.
  Also for: catching "should be fine" statements before merging, confirming agent work via
  independent verification, validating full red-green regression cycle, and checking builds
  are clean before declaring done.
---


# Verification Before Completion

**Core principle:** Evidence before claims — always. No exceptions.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

## Verification Gate (4 Steps)

1. **Identify** the command that proves the claim
2. **Run** it fully and freshly
3. **Read** the complete output and exit code
4. **Verify** — if output supports claim, state it with evidence; if not, report actual status with evidence

Skipping any step equals lying, not verifying.

## What Each Claim Requires

| Claim | Required |
|-------|----------|
| Tests pass | Test output: 0 failures |
| Linter clean | Linter output: 0 errors |
| Build succeeds | Build command: exit 0 |
| Bug fixed | Original symptom test: passes |
| Regression test works | Red-green cycle verified |
| Agent completed | VCS diff + independent verification |

## Stop Triggers

**Never express satisfaction before:**
- Running the exact verification command
- Reading the complete output
- Confirming against the claim

| Phrase That Means STOP | Why |
|------------------------|-----|
| "should" | Not verified |
| "probably" | Not verified |
| "seems to" | Not verified |
| "looks good" | Not verified |
| "I'm confident" | Not verified |
| "Just this once" | Not verified |

## Red-Green Pattern for Regression Tests

Write → run (pass) → revert fix → run (must fail) → restore → run (pass).

A test passing once without the fail step does not verify a regression test works.

## When to Apply

**Always before:**
- Any success or completion claim
- Any positive statement about work state
- Committing, pushing, or creating PRs
- Moving to next tasks
- Delegating to agents

## Bottom Line

> "Run the command. Read the output. THEN claim the result. This is non-negotiable."
