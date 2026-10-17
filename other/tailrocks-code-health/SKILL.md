---
name: tailrocks-code-health
description: >-
  Establishes or tightens one explicitly approved shrink-only
  code-health ratchet for architecture, lint, dependency, flake, defect,
  documentation, or verification debt. Use this skill only when the user
  explicitly requests it. Audit and measurement-only reporting belong to
  tailrocks-code-health-audit.
argument-hint: "<establish|tighten, approved debt class, metric, and paths>"
disable-model-invocation: true
disableModelInvocation: true
license: Apache-2.0
user-invocable: true
when_to_use: >-
  User asks to establish or tighten a shrink-only quality bound or
  ratchet.
---

# Code health ratchet

## Use this skill

This skill applies one approved monotonic mutation. It
establishes a bound from measured current debt, or it
tightens an existing bound to a proven lower measurement.
Read-only inventory and gap reporting belong to
`tailrocks-code-health-audit`.

Use this skill when the user asks to establish or tighten a
shrink-only bound. Do not use this skill to audit, to adopt
unrelated tools, or to absorb a regression.

## Before you start

Use this skill only when the user explicitly requests it. A model
must not select it from task similarity.

Obey the active user request first. If the request conflicts with a
safety rule in this skill, stop. Report the conflict.

Before any action, read `references/runtime-trust.md` and
`references/shared-version-policy.md`. Resolve each relative link
against the directory that holds this SKILL.md file.

The skill accepts `establish` or `tighten` with the approved debt
class, metric, and paths. Refuse an audit-shaped request,
unselected debt, and permission inferred from a finding.

Copy an absent baseline artifact from `assets/` instead of
reconstructing it:

| Template | Destination | Consumed by |
| --- | --- | --- |
| `ratchet.toml` | Project ratchet configuration | Selected bound |
| `flaky-tests.toml` | Flake quarantine | Flake evidence |
| `DEFECT_LEDGER.md` | Defect-to-gate ledger | Defect evidence |
| `renovate.json` | `renovate.json` | Version ratchet |

## Procedure

1. **Bind the exact approval.** Record each item below:

   - `establish` or `tighten`
   - The canonical root and revision
   - The selected debt class
   - The prevented failure class
   - The metric
   - The owner
   - Approved paths
   - Command and network authority
   - The rollback boundary.

2. **Prove the precondition.** Read only the applicable
   reference: `references/architecture-and-docs.md`,
   `references/ratchets-and-baselines.md`,
   `references/defects-flakes-and-reports.md`,
   `references/verification-lanes.md`, or
   `references/versions-and-dependencies.md`. Inventory the
   current gate, exceptions, owner, cadence, output, and blind
   spot. Measure deterministically before writing. For
   `establish`, record an exact current-debt snapshot. For
   `tighten`, prove that measured debt is below the committed
   bound. Run a measurement command only under the read-only
   controls of step 5. Otherwise do not run it.

3. **Select canonical bytes.** Copy an absent baseline artifact
   from `assets/`. Preserve stronger compatible local rules.
   Take the bound only from the measured state of this
   repository. Never import another project count.

4. **Apply one transactional slice.** Reject symlinked targets.
   Stage the selected config, provider, and gate changes.
   Re-check exact preimages. Publish the multi-file set only to
   approved paths. Keep every intermediate state runnable.
   Dependency and tool resolution needs separate authority, an
   immutable pinned and verified artifact, and network isolation
   from target execution. Roll back only still-owned bytes.
   Retain named recovery evidence on uncertainty.

5. **Enforce monotonic behavior.** Growth fails. A measurement
   below the bound also fails until `tighten` lowers it.
   Presence ratchets reject unlisted debt and stale resolved
   entries. Tighten never raises a cap, adds an exception,
   changes the oracle, or absorbs a regression. Retries expose
   flakes. They never forgive them. Keep one semantic violation
   model across human, JSON, and CI renderers.

6. **Place and prove the gate.** Assign PR, merge-readiness, or
   scheduled cadence from measured runtime and false-positive
   evidence. Run the narrow proof plus affected surrounding
   gates under every control below:

   - Frozen inputs
   - Scrubbed secrets
   - Disabled target network
   - A read-only published tree
   - Owner-only external cache and output
   - Bounded processes.

   Otherwise do not run them. Retain the recovery and
   blocker. For version debt, detect latest stable releases
   continuously and apply highest-fixed vulnerability updates
   immediately, under the recorded release-age policy.

7. **Report.** Name each item below:

   - The mode
   - Changed paths
   - Old and new bound
   - The measurement
   - The prevented failure
   - Commands and counts
   - Skips
   - Cadence
   - Recovery state
   - Remaining approved work.

## Result

The terminal shows one approved debt class with one monotonic
bound, an honest measured precondition, exact writes, and the
placed gate. No unrelated tool adoption occurred. Growth and
stale generosity both fail. No concurrent loss or unknown
recovery state remains.

## Completion checks

Before the result is complete, make sure that each item below is
true:

- Exactly one debt class and one bound changed.
- The precondition measurement is honest and current.
- No unrelated tool was adopted.
- Every write stayed on approved paths.
- The gate placement has measured runtime evidence.

## References

Read these references at the stated times:

- Read `references/runtime-trust.md` before any action for the
  trust rules.
- Read `references/shared-version-policy.md` before any action
  for version comparison rules.
- Read the one applicable provider reference in step 2 for class
  criteria.
