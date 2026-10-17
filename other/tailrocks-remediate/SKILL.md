---
name: tailrocks-remediate
description: >-
  Applies one explicitly approved root-cause correction while preserving
  every unapproved behavior and proving instance and defect-class
  prevention. Use this skill only when the user explicitly requests it.
  Requires a current diagnosis contract. Never diagnoses, chooses, or
  approves the design.
argument-hint: "fix <approved root-cause report and target>"
disable-model-invocation: true
disableModelInvocation: true
license: Apache-2.0
user-invocable: true
when_to_use: >-
  User asks to apply an approved root-cause correction from a current
  diagnosis report.
---

# Remediate

## Use this skill

This skill executes one exact correction already diagnosed by
`tailrocks-root-cause` and explicitly approved by the user. It
preserves every unapproved behavior. It proves instance and
defect-class prevention.

Use this skill when the user passes explicit `fix` with the exact
current approved contract. Do not use this skill to diagnose, to
derive a design, or to expand the defect class. Do not treat a
diagnosis report as mutation authority. Reject omitted,
`analyze`, `rebuild`, mixed, and unknown selectors unchanged.

## Before you start

Use this skill only when the user explicitly requests it. A model
must not select it from task similarity.

Obey the active user request first. If the request conflicts with a
safety rule in this skill, stop. Report the conflict.

Before any action, read `references/runtime-trust.md`. Resolve
each relative link against the directory that holds this SKILL.md
file.

Run commands only with explicit execution authority and every
control below:

- Frozen dependencies and inputs
- Scrubbed secrets
- Disabled network, unless the approved operation needs one
  exact endpoint
- Owner-only external cache and output
- Bounded time, retries, output, and process tree
- TERM-then-KILL cleanup
- Repository hashes before and after every proof run.

## Procedure

1. **Bind the contract.** Record each item below:

   - The canonical repository
   - The current HEAD
   - The merge base and range
   - The dirty-state digest
   - The diagnosis ID and hashes
   - The approval text
   - Exact allowed paths and breaks
   - Expected preimages
   - The prevention claim
   - Migration slices
   - Expiry
   - Every irreversible and external step.

   Reject stale, ambiguous, symlinked, escaping, broadened,
   and self-approved contracts. Route re-diagnosis, redesign,
   and approval changes back to `tailrocks-root-cause` and the
   user.

2. **Revalidate the diagnosis.** Revalidate the reported
   contradiction, causal boundary, affected consumers,
   persisted and wire forms, compatibility promises, and
   capability set. A mismatch blocks. Never repair the contract
   in place. Preserve all behavior not named in the approved
   break inventory.

3. **Require proof oracles.** Require regression evidence for
   the reported instance and a boundary or property oracle for
   the defect class. A regression test that fails because of
   the defect is permitted before the correction: it proves the
   instance. Add an approved characterization test before
   production mutation when needed. Prove it against unchanged
   production bytes. A vacuous, unavailable, or mutation-prone
   baseline blocks application.

4. **Execute one approved slice at a time.** Publish every
   changed path sequentially by expected-preimage-to-owned-postimage
   compare-and-swap with a per-path receipt. Never claim
   multi-path atomicity. Examine the slice invariant and the
   focused oracle before continuing. Temporary bridges carry
   their approved removal condition. They are never the
   destination.

5. **Require fresh approval for outward actions.** Before
   each destructive, irreversible, persisted-data,
   published-contract, and outward action, require fresh
   action-specific user approval. Bind it to the exact target
   and current state. A data migration is resumable and
   idempotent. It verifies backup and checksum. It obeys
   expand-migrate-contract. It names the forward-recovery
   path. Never promise rollback of an irreversible effect. If
   active harm needs approved containment, apply only the
   named reversible measure. Report `CONTAINED`, never
   `CORRECTED`, until cause removal.

6. **Restore carefully on failure.** After current bytes
   prove that they still match the owned postimage of this
   invocation, restore a preimage only by compare-and-swap.
   Preserve concurrent replacements. If any mutation
   survives, stop. Name every changed path, partial
   migration, and recovery artifact as `RECOVERY_REQUIRED`.

7. **Prove the correction.** Run focused and full repository
   gates under the same bounded contract. Prove each item
   below:

   - The reported instance
   - The approved bounded class
   - Every migration invariant
   - The final break inventory
   - The exact changed-path allowlist
   - The structural measure
   - Removal of every temporary bridge due in this slice.

## Result

The terminal shows exactly one of `CORRECTED`, `CONTAINED`,
`BLOCKED`, `REFUSED`, or `RECOVERY_REQUIRED`, bound to
repository and HEAD identity and diagnosis and approval
identity. The result holds pre and post hashes, per-path
compare-and-swap receipts, commands and units, and instance
and class-prevention evidence. It holds approved breaks,
residual exposure, partial mutations, and recovery artifacts.
`CORRECTED` needs the full approved cause removal. `RECOVERY_REQUIRED` means at
least one mutation survives. No unapproved edit, behavior
change, scope expansion, commit, push, merge, issue, comment,
dependency install, credential use, network call, or external
action occurred.

## Completion checks

Before the result is complete, make sure that each item below is
true:

- The contract was current, exact, and user-approved.
- Every unapproved behavior is preserved.
- Instance and class prevention both have oracle evidence.
- Every changed path has a receipt.
- Partial mutations and recovery artifacts are reported
  exactly.

## References

Read this reference at the stated time:

- Read `references/runtime-trust.md` before any action for the
  trust rules.
