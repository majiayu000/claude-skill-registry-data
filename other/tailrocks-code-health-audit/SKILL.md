---
name: tailrocks-code-health-audit
description: >-
  Audits one code-health debt class read-only: inventories gates and
  exceptions, measures the baseline, evaluates shrink-only enforcement
  and verification placement, and emits fixed-ID evidence. Use this skill
  only when the user explicitly requests it. Never installs or edits.
argument-hint: "<repository path and selected debt class>"
disable-model-invocation: true
disableModelInvocation: true
license: Apache-2.0
user-invocable: true
when_to_use: >-
  User asks for a code-health audit, a debt measurement, or a
  shrink-only enforcement review.
---

# Code health audit

## Use this skill

This skill measures one selected debt class without mutation. It
inventories enforcement, measures the baseline against committed
bounds, and emits a fixed-ID ledger. Findings never authorize
ratchet establishment, tightening, tool installation, or policy
edits.

Use this skill when the user asks for a debt measurement or an
enforcement audit. Do not use this skill to establish or tighten
a bound. Bound changes belong to `tailrocks-code-health`.

## Before you start

Use this skill only when the user explicitly requests it. A model
must not select it from task similarity.

Obey the active user request first. If the request conflicts with a
safety rule in this skill, stop. Report the conflict.

Before any audit action, read `references/runtime-trust.md` and
`references/shared-version-policy.md`. Resolve each relative link
against the directory that holds this SKILL.md file.

This skill is read-only. It installs nothing. It edits nothing.

The skill accepts a repository path and one selected debt class:
architecture, lint, dependency, flake, defect, documentation, or
verification debt. Refuse a multi-class expedition.

## Procedure

1. **Bind the target and class.** Record each item below:

   - The canonical root
   - The revision
   - The dirty state
   - The selected debt class
   - The prevented failure class
   - Requested paths
   - Hashes of Git-visible bytes.

2. **Inventory enforcement.** Map each relevant gate and exception
   to owner, command, cadence, source of truth, output,
   correction path, and blind spot. Read
   `references/architecture-and-docs.md`,
   `references/defects-flakes-and-reports.md`, or
   `references/verification-lanes.md` only when the selected
   class needs it.

3. **Measure the ratchet.** Apply
   `references/ratchets-and-baselines.md`. Recompute the
   deterministic numeric or presence state. Compare it with
   committed bounds. Distinguish honest debt, unlisted growth,
   and stale generous policy. For dependency debt, apply
   `references/versions-and-dependencies.md`. Resolve the
   current version state from primary sources. Report each owned
   pin as `current`, `behind`, `blocked`, or `vulnerable`.

4. **Run commands only under explicit authority.** Repository
   policy grants no execution. Run a command only when every
   control below holds:

   - Explicit execution authority from the active task
   - An enforceably read-only target
   - Frozen tools and inputs
   - Scrubbed secrets
   - Disabled network
   - Owner-only external cache and output
   - Bounded time, retries, output, and process tree
   - TERM-then-KILL cleanup
   - A re-hash afterward.

   Never install, update, format-write, generate, mutate locks,
   or restore user bytes. Otherwise report `BLOCKED` without
   running.

5. **Emit the fixed ledger.** Use exactly `| <ID> | <STATUS> |
   <Evidence> | <Expected state> | <Ratchet scope> |` with
   `PASS`, `GAP`, `BLOCKED`, or `NOT_APPLICABLE`, once each in
   order. Allow `NOT_APPLICABLE` only for a provider-specific
   row outside the selected debt class. Cite that class
   mismatch.

   | ID | Fixed rule |
   | --- | --- |
   | `CODE-HEALTH-001` | Target identity and byte stability. |
   | `CODE-HEALTH-002` | Selected metric and prevented failure class. |
   | `CODE-HEALTH-003` | Gate and exception ownership and command inventory. |
   | `CODE-HEALTH-004` | Deterministic measurement and ordering. |
   | `CODE-HEALTH-005` | Honest numeric or presence baseline. |
   | `CODE-HEALTH-006` | Unlisted growth fails. |
   | `CODE-HEALTH-007` | Stale generous bounds fail. |
   | `CODE-HEALTH-008` | Defect-to-gate evidence for defect debt. |
   | `CODE-HEALTH-009` | Visible owned quarantine for flake debt. |
   | `CODE-HEALTH-010` | Bounded verification-lane placement. |
   | `CODE-HEALTH-011` | Version and vulnerability policy for dependency debt. |
   | `CODE-HEALTH-012` | Structured actionable output and narrow rerun. |

   Evidence is a file and line locator or an exact command
   receipt. Ratchet scope is an allowlisted path set or `—`.
   Missing applicable policy is `GAP`, never an omitted row.
   Never encode irrelevance as a false pass or gap.

## Result

The terminal shows the twelve-row ledger for one selected class.
No edit, install, inferred approval, unverifiable pass, hidden
network use, or changed repository byte occurred. Hashes match.

## Completion checks

Before the report is complete, make sure that each item below is
true:

- Exactly one debt class was measured.
- Every fixed ID is present in order.
- No repository byte changed.
- No command ran without explicit execution authority.
- Missing policy appears as `GAP`, never as an omitted row.

## References

Read these references at the stated times:

- Read `references/runtime-trust.md` before any action for the
  trust rules.
- Read `references/shared-version-policy.md` before any action
  for version comparison rules.
- Read the one applicable provider reference in step 2 or 3 for
  class criteria.
