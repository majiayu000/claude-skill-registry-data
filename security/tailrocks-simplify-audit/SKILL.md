---
name: tailrocks-simplify-audit
description: >-
  Audits one pull request, branch, or diff read-only for measured code
  removals whose observable behavior can be preserved. Use this skill
  only when the user explicitly requests it. Returns findings only.
  Never edits, tests in, or applies them.
argument-hint: "<PR, branch, or diff>"
disable-model-invocation: true
disableModelInvocation: true
license: Apache-2.0
user-invocable: true
when_to_use: >-
  User asks what code a change can remove without changing
  behavior.
---

# Simplify audit

## Use this skill

This skill finds what one bound change can lose while preserving
all observable behavior. It returns one report. It never writes a
characterization test, edits production code, applies a
candidate, or infers approval.

Use this skill when the user asks for removable code in a pull
request, branch, or diff. Do not use this skill to apply
removals. Approved removals belong to `tailrocks-simplify`.

## Before you start

Use this skill only when the user explicitly requests it. A model
must not select it from task similarity.

Obey the active user request first. If the request conflicts with a
safety rule in this skill, stop. Report the conflict.

Before any audit action, read `references/runtime-trust.md`. Resolve
each relative link against the directory that holds this SKILL.md
file.

This skill is read-only. It changes no repository byte.

The skill accepts one pull request, branch, or diff. Scope is
only changed lines plus code that the change made dead.
Untouched cleanup is excluded.

## Procedure

1. **Bind the target.** Record each item below:

   - The canonical repository
   - The HEAD
   - The exact merge base, range, or worktree snapshot
   - The dirty state
   - Touched files and hunks
   - Git-visible hashes.

2. **Mark protected constructs.** Apply
   `references/simplification-ladder.md`. Mark each item
   below before searching:

   - Trust-boundary validation
   - Authentication and authorization
   - Errors and failure paths
   - Transactions, retries, and idempotency
   - Ordering and cleanup
   - Concurrency and cancellation
   - Accessibility
   - Timeouts
   - Security limits.

   Keep an unexplained guard.

3. **Walk the ladder.** Walk the ladder per hunk. Stop at
   the first supported removal. Cite a reuse claim with an
   existing repository path or an exact API in the pinned
   runtime. A new dependency, rename, extraction,
   reorganization, two-site abstraction, and clever
   equivalent are not simplification.

4. **Count the delta.** Count lines, branches, names,
   parameters, nesting depth, configuration keys, and direct
   dependencies before and after. Reject a candidate with no
   positive counted delta. Never use line count as the only
   measure.

5. **Argue preservation.** Re-read each candidate. Argue
   identical behavior for every accepted input class. Cover
   each item below:

   - Return and error types
   - Side-effect order and count
   - Timing
   - Cleanup
   - Wire and persisted forms
   - Logs with consumers
   - Rendering semantics, focus, and accessibility.

   Looks equivalent is never evidence.

6. **Inspect the oracle.** Inspect existing tests and prove
   whether they enter the removed path. Run a command only
   with explicit authority and every control below:

   - An enforceably read-only tree
   - Frozen inputs
   - Scrubbed secrets
   - Disabled network
   - Owner-only external cache and output
   - Bounded time, retries, output, and process tree
   - TERM-then-KILL cleanup
   - Before and after hashes.

   Otherwise mark the oracle `NOT_RUN`.

7. **Report.** Return one report with the range, protected
   constructs, rejected candidates, behavior changes routed
   elsewhere, and findings. Shape each finding with each
   item below:

   - ID
   - Location
   - Removal
   - Ladder rung
   - Preservation argument and level
   - Required pre-edit test
   - Measured delta
   - Exact allowed paths
   - Risks.

## Result

The terminal shows one report. Every hunk has a verdict.
Every finding removes a counted measure and carries re-read
preservation evidence. No candidate is approved or applied.
No guard of unknown purpose is called redundant. No secret
value enters output.

## Completion checks

Before the report is complete, make sure that each item below is
true:

- No repository byte changed.
- Every hunk has a verdict.
- Every finding carries a counted delta.
- Every finding carries re-read preservation evidence.
- No behavior change is reported as a removal.

## References

Read these references at the stated times:

- Read `references/runtime-trust.md` before any action for the
  trust rules.
- Read `references/simplification-ladder.md` in steps 2
  through 5 for protected constructs, ladder rungs, and
  measures.
