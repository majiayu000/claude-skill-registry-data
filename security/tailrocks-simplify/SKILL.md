---
name: tailrocks-simplify
description: >-
  Applies one explicitly approved set of measured code removals within a
  bound diff while preserving every observable behavior. Use this skill
  only when the user explicitly requests it. Requires a proven oracle.
  Never discovers removals or changes behavior.
argument-hint: "apply <approved removal set and PR, branch, or diff>"
disable-model-invocation: true
disableModelInvocation: true
license: Apache-2.0
user-invocable: true
when_to_use: >-
  User asks to apply an approved removal set from a current
  simplification audit.
---

# Simplify apply

## Use this skill

This skill applies one exact removal set already produced by
`tailrocks-simplify-audit` and explicitly approved by the user.
It keeps public behavior and necessary validation during each
removal. It discovers no candidate, broadens no scope, fixes no
defect, and changes no behavior. Naming an audit report grants
no mutation authority.

Use this skill when the user passes explicit `apply` with the
exact approved findings. Do not use this skill to audit. Refuse
mixed selectors. Never silently invoke the audit owner.

## Before you start

Use this skill only when the user explicitly requests it. A model
must not select it from task similarity.

Obey the active user request first. If the request conflicts with a
safety rule in this skill, stop. Report the conflict.

Before any action, read `references/runtime-trust.md` and
`references/behavior-preservation.md`. Resolve each relative link
against the directory that holds this SKILL.md file.

Run baseline and proof commands only with explicit execution
authority and every control below:

- Frozen existing dependencies and inputs
- Scrubbed secrets
- Disabled network
- Owner-only external cache and output
- Bounded time, retries, output, and process tree
- TERM-then-KILL cleanup
- Repository hashes before and after each read-only run.

A red, vacuous, unavailable, or mutation-prone baseline blocks
application.

## Procedure

1. **Bind the approval.** Record each item below:

   - The canonical repository
   - The HEAD
   - The merge base and range
   - The dirty state
   - Exact approved finding IDs
   - Touched and dead-code reach
   - Approved characterization-test paths
   - Expected counted deltas
   - Hashes of every writable file.

   Reject stale, ambiguous, symlinked, escaping,
   behavior-changing, and extra-scope work.

2. **Require a preservation oracle.** Require relevant
   existing tests that enter every removed path. Without
   them, require an explicitly approved characterization
   test that first passes against unchanged production
   bytes. Permit reasoned equivalence only for a locally
   obvious unreachable symbol with complete reference
   proof. Never permit it for errors, effects, ordering,
   timing, resources, interfaces, concurrency,
   authorization, validation, or security.

3. **Publish characterization tests first.** If approved,
   publish each characterization-test file sequentially by
   compare-and-swap. Record its receipt. Prove it against
   unchanged production bytes.

4. **Apply one removal at a time.** Apply exactly one
   approved removal. Publish every production file
   sequentially by expected-preimage-to-owned-postimage
   compare-and-swap. Record one receipt per path. Run its
   focused oracle. Continue one removal at a time. Never
   claim multi-file atomicity.

5. **Roll back rather than repair.** On any failed oracle,
   restore a preimage only by compare-and-swap. Restore
   only after current bytes prove that they still match the
   owned postimage. Never use broad Git restoration, repair
   behavior, or overwrite a concurrent replacement. When
   full rollback is impossible, retain and name every
   surviving changed path and recovery artifact.

6. **Prove the result.** Run focused and full repository
   gates under the same bounded command contract. Recount
   every promised measure. Compare the final changed-path
   allowlist, observable contracts, and repository state
   with the approved receipt.

## Result

The terminal shows `APPLIED`, `BLOCKED`, `ROLLED_BACK`, or
`RECOVERY_REQUIRED` with target identity, approved IDs, pre
and post hashes, and tests established before production
edits. It shows command and unit receipts, per-removal and
total measured deltas, exact changed paths, partial
mutations, and recovery artifacts. `ROLLED_BACK` means every
owned mutation was restored and no changed path survives. Any surviving mutation
is `RECOVERY_REQUIRED`. No unapproved edit, behavior change,
commit, push, merge, issue, comment, dependency install, or
external action occurred.

## Completion checks

Before the result is complete, make sure that each item below is
true:

- Every applied removal was approved exactly.
- Every observable behavior is preserved.
- Every promised measure was recounted.
- Every changed path has a receipt.
- Partial mutations and recovery artifacts are reported
  exactly.

## References

Read these references at the stated times:

- Read `references/runtime-trust.md` before any action for the
  trust rules.
- Read `references/behavior-preservation.md` before any
  action for observable behavior and proof levels.
