---
name: tianzheng-batch-polyline-dimension
description: Automate native Tianzheng/AutoCAD dimensions for selected or runtime-discovered polylines, including ARC included-angle and LINE dimensions, ordinary exterior-band layout, exceptional collapsed-angle rescue, text-anchor restoration, machine audits, timing, and readable screenshots. Use when developing, testing, packaging, or running the project's batch polyline dimension command; do not use for unrelated CAD review or unvalidated production claims.
---

# Tianzheng Batch Polyline Dimension

Use this Skill as the entry for `自动批量多段线尺寸`. Its `runtime/` directory contains the existing business implementation and native-control source. Reuse that code instead of recreating the geometry algorithm from prose. Package version: 1.1.1; publication does not promote the complete command's validation maturity.

## Start from authority

1. Read [migration.md](references/migration.md). Use bundled `runtime/` as the source root unless the receiver explicitly selects an equivalent local checkout; do not look for the author's private computer or task IDs.
2. Read the receiver's current instructions and the runtime's source/build/input documentation. Local software, owner, document, scope and permission must be bound to the receiver's real environment.
3. Run `scripts/inspect_capability.ps1` to verify the packaged source manifest. This read-only check never starts CAD and does not authorize execution.
4. Runtime owner, selection ledger, scope, task handoff and return records are new local inputs, not author data to copy. If using the original governed controller, provide its same-schema inputs or equivalent host adapters while preserving scope/hash/owner checks.
5. Read `references/project-contract.md` before changing formulas or claiming acceptance. Default to offline preparation; native mutations require an authorized isolated drawing and a fresh exact session binding.

## Reuse the two-layer implementation

- Business layer: runtime geometry discovery, native ARC/LINE dimension generation, source mapping, first-pass exterior layout, and the narrow exceptional rescue pass.
- Observer layer: identity, ACK/COMPLETE, timings, semantic and endpoint audits, native-grip inventory, readable screenshot, and return delivery.

Keep the business path short. Do not insert heavyweight probes into already-fast stages. Enable targeted diagnostics only at a failed boundary or for a known difficult candidate.

## Preserve dimension semantics

- ARC objects must remain native included-angle dimensions expressed in degrees. Arc length is a semantic failure even if the picture looks plausible.
- LINE objects must remain native linear dimensions and must not receive a degree marker.
- Require runtime source mapping and endpoint association. A visible object without a valid mapping is not a successful dimension.
- Ordinary objects use the shared exterior-band formula first. Do not move every object merely because one exceptional corner needs rescue.

## Handle the exceptional collapsed-angle case

Apply the rescue chain only when runtime measurements identify the anomaly. Never match a fixed handle, coordinate, segment number, bounding box, or object count.

1. Establish or replace an endpoint-valid native angle candidate.
2. Accept the curve side and posture before moving text.
3. Apply the runtime outer-band formula.
4. If the text anchor still lies on or crowds the dimension curve, move grip 4 only.
5. Derive the grip-4 WCS delta from a same-source, shared-endpoint, rank-2 degree peer normalized by measured text height `H`.
6. Pass planner `DX/DY` through unchanged. The controller must not recalculate the vector.
7. Re-inventory the complete native set and produce a readable screenshot.

## Execute through the governed lane

Separate planning/inspection from the one owner that actually drives Tianzheng; task titles do not confer permission. The receiver may use its own equivalent coordination rather than copying the author's project task system.

For a real CAD mutation:

1. Verify no active CAD lease conflict.
2. Bind a fresh immutable handoff to the actual target, permitted actions, file hashes and save policy. When using the original controller schema, satisfy its real input contract; do not delete assertions or fabricate READY/PASS.
3. Dispatch only to the receiver's exact execution owner, never an author task ID.
4. Permit only the actions named by the handoff. Default test policy is `save=false` and `retry=0`.
5. The bounded executor stops at its contract boundary. The source task retains its active outcome and uses the host's existing wait/return mechanism to review the immutable result; do not replay the run or imply automatic continuation without an actual wake-up path.

An explicit current contract may allow saving a unique checkpoint through its accepted save-copy chain. This never authorizes overwriting the source, reusing a closed historical owner or silently retrying a terminal run. Without that authority keep `save=false`; a saved checkpoint is not formal delivery acceptance.

## Judge completion precisely

- A static test, DLL load, ACK, screenshot, or partial survivor set alone is not full success.
- Report generation coverage, semantic correctness, endpoint association, layout targets, protected-grip drift, source drift, screenshot result, business time, observer time, failures, and next legal gate.
- The special text peer-normal component has a current-board 3-of-3 stability record. This does not establish three complete blank-to-final runs and does not establish cross-structure DWG generality.
- Keep the whole command package at its registry maturity until its own promotion gates pass.

Read [current-scope reuse and acceptance](references/current-scope-practices.md) when reusing the common-band chain, diagnosing coarse collision flags, or interpreting sample acceptance and saved/reopened evidence. The historical special-text result above is not a complete current-state report.

## Keep the package clean

- Keep current run directories, drawings, screenshots, identities and credentials outside the distributed source. Bundled source dependencies may include a versioned helper required by the selected call chain; that does not make every optional action a default route.
- Do not revive routes listed as forbidden or rejected by the project.
- Fix repeatable workflow faults in the shared layer and add a regression; do not accumulate one-run workarounds.
- Follow the current handoff's explicit save/checkpoint authority; otherwise preserve test drafts unsaved. A checkpoint is not a formal accepted deliverable.
