---
name: circuit-edit-integration-safety
description: "Debug a reversible-circuit primitive that is value-exact in isolation but leaves identical classical, phase and ancilla dirt on every Fiat-Shamir shot once wired into the full circuit. Run a three-step falsifier ladder first: stale stream-specific optimization indexes, free-pool qubit-ID aliasing, then the measurement-vent discharge target. Use before blaming the primitive's math."
license: MIT
---

# Bastelunfall (circuit-edit-integration-safety)

*Reversible-circuit edit-integration safety (the "isolation-clean, full-circuit-dirty" desync)*

Use when a circuit PRIMITIVE (a borrowed-ancilla adder, a measurement-vented uncompute, a new gate
or vent) tests VALUE-EXACT in isolation (0/0/0 on selftests) but the FULL circuit emits
**nonce-INDEPENDENT** dirt (classical / phase / ancilla identical across every Fiat-Shamir shot incl.
random) after you wire it in. This is the "integration desync". It is almost never the primitive's
math; it is a stream-edit / allocation interaction.

## Goal

Stop blaming the primitive. Diagnose and fix the two dominant integration-desync causes (**stale
stream-specific optimizations** and **free-pool ID-reuse aliasing**) with a 3-step falsifier ladder,
before any "deep math" investigation.

## The diagnostic signature (tells you this is the right skill)

After wiring in an edit, full-circuit eval gives `cls>0 AND pha>0 AND anc>0` that is **bit-for-bit
identical across ALL nonces including random** (nonce-INDEPENDENT). Nonce-independence = the failure is
structural/deterministic, not input-dependent → it is a construction/integration artifact, NOT a
correctness bug in the primitive's truth table. (If the dirt were input-dependent, you'd have a math bug.
It isn't, so you don't.) Bonus tell: a sub-count (e.g. `141 anc`) equals the number of new vents/allocs
you added → those allocs/vents are the leak source.

## The 3-step falsifier ladder (cheapest first)

1. **Stale stream-specific optimization (run with it DISABLED).** Any precomputed op-index optimization
   (dead-gate / CCX-CZ cancellation / template / drop-dead-robust `.idx`) was built for the BASELINE op
   stream. Your edit changed the stream (new gates/vents), so the baseline index now silently drops the
   WRONG ops → exactly nonce-independent dirt. Falsifier: re-run with the optimization DISABLED
   (e.g. `DROP_DEAD_ROBUST_DISABLE=1`), even 1-shot. Outcomes:
   - dirt CLEARS or changes → stale-index contamination. **Regenerate the index for the edited stream**
     before any further diagnosis. (Most common; cheapest fix.)
   - dirt IDENTICAL with optimization off → not the index; go to step 2.
   - (peak/ops too high with drops off is fine: diagnostic only.)
   Also state whether your reported op-count was PRE- or POST-optimization; if post-, rerun raw.

2. **Free-pool ID-reuse aliasing (transient allocs must avoid the free pool).** The full circuit recycles
   freed qubit IDs via a free pool. Your primitive's TRANSIENT allocations (dummy `|0>`, scratch,
   boundary carry-out) pulled from that pool can grab an ID that was just freed but is still LOGICALLY
   ENTANGLED with the in-flight computation → the transient aliases a live qubit → nonce-independent
   phase/ancilla leak at the vent/restore. Falsifier: allocate ALL transient borrowed ancilla at
   FRESH HIGH IDs (a dedicated range above the circuit's current max, never from the free pool). If the
   dirt clears → aliasing was the cause.

3. **Measurement-vent discharge target (palindrome violation).** A measurement-vent discharges
   `Z^{carry}` onto a target qubit. If that target is entangled with a control that is a LIVE carry-in
   read mid-vent (a control the restore is conditioned on), the discharge leaks. Fix: discharge onto a
   provably-unentangled fresh target, OR defer the vent until AFTER the conditioned control is restored,
   OR replace an assumed-`|0>` `zero_and_free` with an actual measurement-vent (`Hmr`) so phase can't leak.

If all three are ruled out, THEN emit the first-divergence shot + first mismatching output bit + first
nonzero ancilla bit to localize a genuine schedule/shift bug.

### Refined Gidney q1152 branch (2026-06-25)

In the 4cd1b2f production-adjacent Gidney tree, raw/no-drop did **not** restore
correctness but did reduce the failure to `12 cls / 12 pha / 0 anc` over 9024
shots. A schedule ledger then showed:

```text
final_g_diffs=0
headroom_diffs=0
phase_diffs=0
local_peak_diffs=214
```

So for this class, do not stop at "stale `.idx` confirmed" merely because
`anc` clears. If raw/no-drop leaves value/phase dirt and the schedule ledger is
identical, the next production branch is:

1. first-divergence probe at the first failing shot;
2. free-pool vs forced-fresh-high-ID A/B for the suspect transient family;
3. lifetime graph for any ID whose high-ID A/B changes the failure;
4. park as primitive/footprint divergence if high-ID does not change it.

Do not send such a build to scanner until this branch is clean.

## Output

For a wired-in primitive: a clean/disambiguated full-circuit result, plus which of the 3 causes applied
and the one-line fix. The durable rules to bake into any reversible-circuit build:
- **Regenerate every stream-specific optimization after any op-stream edit** (or gate it off for the
  diagnostic). Never apply a baseline dead-drop/peephole index to a modified stream.
- **Transient borrowed ancilla never come from the recycled free pool**: fresh high IDs, or
  measurement-vented.
- **Nonce-independent `anc>0 ∧ pha>0` after an edit = integration desync, not a math bug**: run the
  ladder before touching the primitive.

## Credit

Synthesized from the live ecdsa.fail secp256k1 Gidney-Fig-5 integration investigation (2026-06-25),
including Codex-Vector's stale-dead-drop falsifier and the free-pool-aliasing diagnosis. Related:
Gidney, "A Classical-Quantum Adder with Constant Workspace and Linear Gates," arXiv:2507.23079 (2025);
Khattar & Gidney, "Rise of conditionally clean ancillae," arXiv:2407.17966 (2025). Its companion cards from the June 2026 harness are in this repository's history at
commit `dd6a173`.

## Why this is a compiler bug, not a circuit-design problem

The blocker is fundamentally an ENGINEERING / compiler-correctness defect: no paper gives a new gate
that fixes it. Governing principle: **every pass that edits the op stream (dead-gate elimination,
template matching, peephole cancellation, adder substitution) must recompute its analyses from the
post-edit stream. A precomputed op-index is valid ONLY for the exact stream it was computed on; applying
it to a mutated stream is a stale-analysis bug, indistinguishable from use-after-free.** Nonce-independent
dirt is the fingerprint (rules out runtime/probabilistic/physics causes). "141 phase = 141 vents" is the
smoking gun: each aliased vent deposits a structurally-determined phase flip on the wrong register.

## Verified sources

- **Dead Gate Elimination**: Chen/Mendl/Seidl, ICCS 2025, arXiv:2504.12729 (demo github.com/i2-tum/demo-dead-gate-elimination). This IS the source of `DROP_DEAD_ROBUST`; its correctness is scoped to the CURRENT program's measurement structure, not a reusable index → applying a baseline index to a modified stream is outside the guarantee (step 1 of the ladder is the literal falsifier).
- **Qubit Recycling Revisited**: Jiang, PLDI 2024, doi:10.1145/3656428. Free-pool/ID-reuse correctness: qubit dependency graph (QDG), recycling valid iff `→∘↪` acyclic; a recycled ID aliases a live qubit iff a `discard[q]→alloc[q′]` reuse edge loops (q′ still live). Prior verified compilers "do not directly apply" to recycling → a bare free-pool allocator has no backstop (step 2). Localize: for each vent, is any alloc's recycled ID in the live-set of an active logical register at vent time?
- **Spooky Pebble Games and Irreversible Uncomputation**: Gidney, 2019, algassert.com/post/1905. Source of venting; a vented qubit must be Z-redundant (Z-basis function ONLY of values live at vent time). Else the `|−>` branch phase-flips whatever actually controls the bit-flips (the aliased register) → nonce-independent phase dirt. Explains 141=141.
- **Measurement-Based Uncomputation for Modular Arithmetic**: arXiv:2407.20167 (2024). Formal MBU correctness for our domain; re-derive the precondition on the INTEGRATED circuit, not the isolated adder.
- **Advantages of using relative-phase Toffoli gates**: Maslov, Phys. Rev. A 93, 022311 (2016), arXiv:1508.03273. Relative-phase gates correct ONLY in matched compute/uncompute pairs; integration breaks the pairing → 0/0/0 selftest vs phase dirt integrated.
- **Verified Compilation of Space-Efficient Reversible Circuits**: Amy/Roetteler/Svore, CAV 2017, doi:10.1007/978-3-319-63390-9_1. Space-efficient allocation REQUIRES verification; an unchecked free-pool is the defect class. (ECDLP literature documents no "nonce-independent integration dirt", which confirms it is a build-pipeline defect.)
