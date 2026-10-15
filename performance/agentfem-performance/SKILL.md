---
name: agentfem-performance
description: Optimize and package reproducible AgentFEM simulations using phase timing, accepted-state replay, rollback checks and full-run evidence. Use for AgentFEM runtime bottlenecks and reproducible case delivery, not general website performance or claims based solely on short microbenchmarks.
license: Apache-2.0
---

# AgentFEM performance and reproducible cases

<!-- SPDX-FileCopyrightText: 2026 Haoming Luo and AgentFEM contributors -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

This is optional development guidance, not a solver or runtime dependency.
A delivered project must execute its declared model and installed providers
without an agent generating code, repairing inputs or making scientific
choices during the run. Skills help prepare and review it; they do not supply
missing executable behavior or prove that its results are valid.

Read the target repository's AGENTS.md and focused architecture/performance
documents. Inspect running numerical jobs before launching another. Preserve
private meshes and user laws outside the public library.

When promoting a private fast path into core, or diagnosing a regression after
that migration, read [Migration parity](references/migration-parity.md).
This is an evolving engineering playbook, not a fixed optimization recipe.
Past worker counts, test lengths and architecture choices are observations,
not defaults for the next problem. Reusable execution and export correctness
belong in the library, not in agent-written case workarounds.

## Choose work by expected whole-run benefit

Start with the user's outcome: runtime, memory, case simplicity or release
readiness. Use existing trustworthy evidence before collecting more. Separate
total increments, cost per accepted increment, rejected work, and one-off I/O;
a fast kernel does not address an excessive increment count. Inspect the actual
execution route, concurrency and data movement before tuning arithmetic.

Pick the largest plausible bottleneck, estimate its ceiling on total savings,
and state what measurement would change the decision. Consider algorithmic
work reduction, conservative search/certificate reuse, batching, fused passes,
ownership and memory layout—not just small kernel substitutions. Such changes
still need their relevant invalidation, failure and accuracy checks. Change
scientific inputs only as an explicitly scoped, sensitivity-tested experiment.

Use risk-proportionate gates:

- Exploration: one focused correctness check and a representative timing can
  reject a bad idea; they cannot establish a release or whole-run speed claim.
- Candidate: test the changed boundary and relevant failure paths; compare
  stages that exercise it. Increase repetitions only when uncertainty could
  change the decision. Do not cycle indefinitely around noisy small wins.
- Delivery: freeze the selected installed candidate, run the relevant release
  gates, and measure a complete run if full-run performance is being claimed.
  Do not repeat that expensive gate after every local edit or unrelated fix.

Set a bounded investigation budget appropriate to the requested sprint. Stop
or reprioritize when measured cost is too small, savings are not repeatable,
or complexity outweighs expected benefit. Preserve a compact finding so the
same failed experiment is not repeatedly rediscovered.

## Identify the expensive boundary

Measure preparation, kinematics, material update, force assembly, contact,
state transactions, reporting, checkpoint and export separately. Repeated
copy/validation of large state arrays and rewriting an expanding JSON history
can dominate a fast material kernel. Follow data ownership, not only FLOPs.
Prefer one immutable accepted owner with explicit publication boundaries;
never leave callbacks observing stale fields. An optimization requiring
exclusive ownership must declare and test that restriction.
This is a preferred implementation, not a ban on a better transaction design.
The invariant is that readers see valid accepted state and failed trials do
not corrupt it. Repeated validation may be fused or removed when a checked,
immutable owner proves the same invariant across consumers. A pointer/address
cache or an unchecked writable alias is not that proof.

Guarded native fast paths may reject individual points and repair them with the
unchanged reference algorithm before publishing a batch. Do not fall back the
entire batch unnecessarily; do not accept half-repaired trial state. Preserve
validation coverage, requested cutbacks and source-law diagnostics, not every
historical scan, copy or call boundary.
Native callbacks and function pointers are trusted code, not data assets.

## Evidence before speed claims

Choose the comparison before choosing the gate:

- Same discretization/algorithm: fix scientific inputs and compare equivalent
  accepted states. Bitwise equality is useful when arithmetic order is unchanged.
- New algorithm/discretization: compare time-to-solution at a declared accuracy
  target using common physical times, quantities and admissible field mappings.
  Different step counts, meshes and reduction order are allowed; justify error,
  convergence, path history and event handling instead of requiring byte equality.
- New hardware/backend: reselect operational budgets from capabilities and
  representative work. Keep scientific inputs separate from execution evidence;
  a missing optional accelerator need not invalidate the physical Model.

Freeze the selected candidate for its comparison, not the product forever.
For a same-algorithm comparison fix mesh, inertia, time grid, contact and output
cadence. For a method study name every intentionally varied choice and preserve
the reference. Do not require replay from the same checkpoint when the methods
have incompatible states; use a common initial problem and physical stations.
Do not patch a running reference or replace its loaded runtime. If unrelated
builds or tests overlap it, record that interference in the timing report.
Choose stages that exercise the change; damage/contact changes usually need
early, nonlinear and late evidence. A 5% short-run change may be noise, but no
fixed percentage makes a repeatable, cheap improvement worthless. Check the
affected scientific quantities and lifecycle, not just final force or checksum.
Bitwise parity is strong evidence for unchanged arithmetic, not a universal
requirement for a different valid algorithm. Predeclare appropriate tolerances
and sensitivity checks; do not loosen them after a failure to admit a speedup.
State explicitly when numerical replay is verified but independent physical
validation is missing. Internal work is not automatically stored energy.

Test worker budgets on the actual machine; more threads or dynamic scheduling
can regress. Avoid BLAS/OpenMP oversubscription using process-local settings,
not global shell changes. Keep comparative timing isolated from competing
numerical jobs. An active frozen run does not prohibit independent source
review, design or lightweight work; record material resource interference.
Do not change mass scaling, contact scope, penalty or horizon merely to meet a
runtime target. Any scientific change needs separate sensitivity evidence.

## Deliver a stable project

Keep case.py as modeling truth, private material implementation as a separate
provider, and operational settings separate from physics. Pin/hash the runtime,
source law and mesh. Use an installed package, not development-tree path
insertion. Verify the project from outside its directory before a full run.
Hash scientific inputs and executables separately from generated timings and
audit reports; running a diagnostic must not invalidate the model identity.
Preserve accepted checkpoints and unambiguous output status on interruption.
Append-only reporting can reduce growing-history write cost; its journal is
not a checkpoint. Preserve the final digest tip externally if suffix loss must
be detectable.

Separate reproducibility of one frozen run from portability of the software.
Thread counts, timing thresholds, hardware names, case-specific final counters
and experimental comparison tolerances are not scientific defaults. Check
whether implementation caps or operational fields unnecessarily enter restart
identity. Propose versioned, tested compatibility for operational changes;
never obtain portability by deleting identity checks from an existing archive.
An autotuning cache should be optional, capability/workload-scoped and fall
back when stale. It must not tune mass, material, penalty or accuracy silently.

Use the supported result writer and declared cell-order/field-layout contracts,
not hand-written connectivity or inferred nodal ordering. For visualization
delivery or writer changes, check with an independent reader: volume topology, complete
displacement, field association, and Warp coordinates. Keep unwarped coordinates
as the source geometry; presentation repair must not alter scientific arrays.

Report measured end-to-end time only after a complete run, including startup
and final export. Until then report the current accepted station and label all
whole-run estimates. Compare the completed run against the earlier frozen
reference and retain limitations. Never infer a transferable default thread
count, time increment or mass scaling from one successful project.

Maintain this skill when experience contradicts it: distinguish a scientific
invariant from a local convention, remove redundant ritual, and record only
decision-changing lessons. The skill itself is not evidence that a run passed.
