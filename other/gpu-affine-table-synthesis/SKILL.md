---
name: gpu-affine-table-synthesis
description: Use when an ecdsa.fail or reversible-circuit lane holds meaningful Toffoli share in dirty-table predicates (4/5/6-input truth functions under external controls), when a rival lands an affine/ESOP-class move, or when one hand-optimized table suggests the class pays — covers harvest, GPU/CPU candidate search, per-site winner rule, and exact re-verification.
---

# Tabällechnächt (gpu-affine-table-synthesis)

## Overview

For every dirty-table truth function f on n input wires, search coordinate transforms that make its reversible implementation cheaper: invertible linear CX frame G plus X-polarity p (exact ANF `a(y)=f(G⁻¹(y⊕p))` via bitwise Möbius), shear-ESOP/Davio cube plans, plain polarity ANF, and dirty-echo factoring. The emitter applies the frame, toggles the target by the winning monomials/cubes under the ORIGINAL external controls, and reverses the frame. Exact, no extra qubits, ordinary X/CX/CCX, no relative phases.

One manual table win (e.g. 226→178 T on a 9-bit chart) is the signal that the whole class pays. A GPU harvest of all tables at once is the step change (−115.6M T demonstrated on the 792-tree family, c602909 lineage).

## When to Use

- A circuit family keeps >3% of structural T in 4/5/6-input dirty-table predicates (harvest first — measure, never guess).
- A rival posts an affine/ESOP-class cut: the class transfers to YOUR tree within days; move first.
- One hand-built affine table already landed: the rest of the tree's tables are unharvested money.
- NOT for: nonce-lottery lanes (this class is exact, no island), relative-phase tricks (illegal in reversed gathers), or tables already at the emitter's cost floor (offer-loop keeps incumbents).

## Pipeline

1. **Harvest.** Diagnostic-only regeneration dumps every in-scope function: id, width, truth vector, external-control signature, current Toffoli cost, call count, site frames. Default build must stay bit-identical with the hook unset (A/B whole-count). One choke-point wrapper beats per-site patches (e.g. wrap the tree's `swap_terms`-equivalent).
2. **Score candidates per function**, with the TREE's OWN emitter cost model, never a ported one:
   - GPU frame bank: all invertible G for n=4 (20,160) and n=5 (~10M) feasible; n=6 needs a declared seeded subset (shear compositions + seeded random invertible frames — exhaustive is ~1.6e10). SoA storage, 256-work-item groups; CPU reference must match GPU exactly.
   - Shear-ESOP (n(n−1) single shears) and Davio/Shannon plans for larger tables — CPU is fine.
   - Polarity-only ANF (may already be harvested by the tree's existing synthesizer) and dirty-echo.
3. **Per-site winner rule.** Keep a rewrite only if ALL hold: Toffoli strictly smaller by ACTUAL emitted count (not the analytic proposal), operation count not increased, qubit allocation unchanged, interfaces disjoint, dirty-lender capacity sufficient. Cache key `(truth, extra)` — extras differ per site (rank-echo 0, truth_swap 1, T10 |base|+6).
4. **Re-verify everything.** Every baked table exhaustively (all 2^n assignments, plus active/disabled external controls, arbitrary target/dirty patterns, exact phase and literal inverse). Native checker tied to the final binary. No statistical acceptance.
5. **Gates.** Kill-switch flag (OFF must be bit-identical), candidate_configuration/audit constants re-frozen, per-block census, whole-default-count A/B, then the trusted 9,024-shot replay before any submit. Recheck the live record before every build — the board moves daily.

## Common Mistakes

| Mistake | Reality |
|---|---|
| Port the rival's winning transform class wholesale | Cost models differ per tree: shear-ESOP beat Möbius-after-G 22 vs 34 on one rank table. Offer-loop per site; never bet the tree on one class. |
| Trust the GPU's analytic score | The GPU only proposes. The emitter compares actual old/new op sequences and declines regressions. |
| Assume additivity across passes | Post-op passes (NCT-frame class) eat complementary cubes. Re-count STACKED, not baseline-summed. |
| Double-count already-optimized sites | Polarity search, rank-echo factorization, manual affine charts may already harvest part of the class. Inventory them first. |
| Nonce/seed confusion | The structural seed for frame candidates is unrelated to benchmark Fiat-Shamir seeds; no nonce is searched. |
| Ops-wall blindness | Winner rule includes ops-not-up; the official eval has time/payload limits. |

## Quick Reference

- Harvest: env-gated diagnostic mode wrapping the table choke point; JSONL per function (id, width, truth, external signature, unit T, calls, site frames).
- Verify: exhaustive scalar reconstruction per function + native forward/reverse checker with phase.
- Accept: strictly-smaller T, ops-not-up, qubit-neutral, disjoint interfaces, dirty capacity OK.
- Ship: kill-switch + re-frozen audit constants + census + whole-count + trusted replay + live-record recheck, then official submit with lineage attribution.

## Real-World Impact (2026-09-12 campaign)

- Manual instance (mod8 exit chart, 226→178 T/call): 793 × 817,508,135 official.
- Rival GPU instance (111 fns / 278 configs, 2× Intel Arc B50): 792 × 1,074,160,050 official, −115.6M T in one move.
