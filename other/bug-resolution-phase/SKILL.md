---
name: bug-resolution-phase
description: >-
  Resolves selected ClawPatch findings through classification, bounded fixes,
  triage, docs/debt routing, and revalidation. Use when the user selects a
  ClawPatch finding, asks for ClawPatch-backed bug resolution, or gives a
  tightly bounded finding batch.
disable-model-invocation: true
---

# Bug Resolution Phase

Selected-finding resolution. ClawPatch is the ledger and context source, not
runtime proof and not the default patching engine.

Load [REFERENCE.md](REFERENCE.md) before classifying or patching.

## Contract

- Default to one selected finding; accept a batch only when explicitly bounded.
- Default scope is PR changes, highlighted diffs, supplied code portions, or
  certain paths/domains around the selected finding. Full-codebase scan only
  when no PR is open and no certain scope exists, or when the user explicitly
  asks.
- Pass that bounded scope to every ClawPatch command or explicit patch attempt
  that accepts scope, path, or diff guidance.
- Patch through normal Harness/Codex edits unless the user explicitly requests
  ClawPatch patch attempts.
- Exit resolved/revalidated, routed to debugging, recorded as debt, triaged
  false positive, or blocked with evidence.

## Steps

1. Read the selected finding with `clawpatch show` and recover report/state
   context when useful.
2. Capture finding ID, report/state path, evidence, affected files, claimed
   behavior, current status, bounded scope, and provider/model default or
   explicit override when ClawPatch commands need it.
3. Classify as `resolve-now`, `needs-runtime-debugging`, `tech-debt`,
   `false-positive`, or `blocked`.
4. Execute that route within scope.
5. Run focused verification, then `clawpatch revalidate` or a clear
   triage/status update.
6. Keep final status decisions centralized for batches.

## Output

Return mode, finding IDs, report/state paths, classification, route, changes,
ClawPatch commands/state including provider/model default or override,
verification, artifacts, caveats, and next action.
