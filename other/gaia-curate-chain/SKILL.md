---
name: gaia-curate-chain
description: >-
  Use for explicitly requested fixed-topology, discovery-only Gaia curation; for one source page use gaia-curate. Atomically
  checkpoints each candidate transition, retries only the failed field, and
  stops at human L4 review.
version: 3.0.0
argument-hint: "<source-or-small-batch>"
---

# Gaia Curate Chain

Read `../gaia-curate/CURATION-CORE.md`; it owns the lifecycle and packet. Use this extension when recoverability matters more than throughput.

## Checkpoint contract

Persist a run ledger under `generated-output/curate-discovery/<run-id>/run.json` containing the core contract digest, generic snapshot digest, source cursor, active candidate ID, completed candidate IDs, deferred rows, and next instruction. Write to a temporary file, validate it, then atomically rename it; never leave a partially written checkpoint.

Process exactly one candidate at a time. Validate its `discovery-packet-v2` after every transition and persist each final review packet to Core's `registry-for-review/discovery-packets/` path. V1 remains readable only for compatibility. Advance only when the current transition validates and its input digest matches the checkpoint. On resume, revalidate contract and generic snapshot digests; preserve raw source records but move stale mappings to `DEFER`.

Keep current-state `blockers` and `sourceRevisions` separate from historical events.
Each blocker records `checkId`, `status` (`open` or `resolved`), `summary`, and
`resolutionEvidence` when resolved. On resume, read
`gaia_cli.curationCheckpoint.compactCheckpoint(ledger, freshFailingChecks)` first;
only checks actually rerun during this resume, with fresh failure evidence, belong in
`freshFailingChecks`. Resolved blockers with evidence stay resolved; unproven
resolutions and open blockers remain active. Never promote old failure history into
a fresh check. Persist new failures as open blockers before the next checkpoint.
The CLI's `.gaia/curation/runs/<run-id>/state.json` stores the same fields under
`checkpoint`; `gaia curate --resume <run-id> [--status]` reports that compact state
and pauses on active blockers. Neither ledger format grants L4 approval.

## Bounded repair

Route only the failing candidate and field back to its worker. Allow at most two retries for transient fetch failure and one Luna High/equivalent repair for invalid structured output. A deterministic schema, hash, or generic-reference failure is not blindly retried.

If retries are exhausted or output remains invalid/ambiguous, emit `DEFER` with the stable core reason code and exact resume instruction: candidate ID, failed field, validator code, source cursor, and required operator action. Never synthesize or infer a decision.

The chain ends at L4 human review. Shared reconciliation accounts for every expected candidate exactly once (review-ready, deferred, rejected or proven duplicate), including failures. Review-ready is not human-approved. It does not collect evidence, calculate trust, mutate the registry, regenerate docs, create intake batches, commit, push, or open a PR.

## Explicit downstream handoff

After an L4 decision, write a handoff record; do not silently end the caller:

- New external discoveries: after independently verified L4 human approval bound to the exact reconciled inventory and manifest, ratify the packet via `gaia dev ratify` with a trusted authorization envelope. Local metadata is not authority; the descriptive flags remain (`--assessment`, `--reviewed-by`, `--approval-ref`, `--reason`, `--acknowledge-human-review`), which attaches the schema-defined `l4Resolution`, then run `gaia push --from-file <packet.json>`. Do not manually translate packets to `skills.yml` or fabricate resolutions; the adapter owns that deterministic translation and refuses unresolved identity or non-blob provenance.
- Rows that already came from `/gaia-draft-curate`: preserve `batchId` and issue/PR links, return them as `needs-evidence` to `/ev-pipeline`, then hand verified rows to a maintainer on `review/meta/*` for the CLI-only meta-shift in `CONTRIBUTING.md` §1C. Do not submit the same intake twice.

Record the route, artifact path, remaining gate, and exact next command. This compatibility handoff is data only; the chain remains discovery-only.
