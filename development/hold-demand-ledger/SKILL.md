---
name: hold-demand-ledger
description: >-
  Measure hold/dup-loan demand and supply on an ecdsa.fail-style reversible op stream, and price Q-cut
  (width) moves correctly against hold capacity. Use when extending or auditing a hold_pass-type final pass,
  when pricing a qubit cut against the holds it enables or destroys, when a "shortfall histogram" or
  demand curve looks suspiciously clean, or before trusting internal consistency checks (sym asserts,
  relocate 0-failures) as evidence of correctness. Contains the four measured traps: tautological shortfall,
  uniform-shift vs peak-clip model confusion, pre-loan/with-loan numbering drift, and oracle-only rejection.
whenToUse: Working on hold/loan passes or width cuts on ecdsa.fail trees; pricing Q changes against hold capacity; writing measurement probes on op streams; auditing another lane's demand/supply claims.
---

# Milchbüechli (hold-demand-ledger)

*Hold Demand Ledger (measured on the 5ba2d2d4 record tree)*

How to measure the hold/dup-loan economy of an ecdsa.fail stream without fooling yourself. Distilled from
our own defense work (2026-10-31) on the 1234q × 739,480T record, including two errors an adversarial
reviewer (Claude Fable) caught and the oracle rejection that followed. The probe code lives in the lane's own
checkout of the record tree and is not bundled.

## The byte-exact replica recipe (the enabler)

The shipped `build()` = `clear_process_env()` (ALL env vars wiped — env knobs are dead on this path) +
a compiled-in zstd prefix (count+SHA3 pinned) + ~20 hash-bound passes. The structural generator
(`build_generated()`) is retained and **reproduces the shipped stream byte-identically** (verify:
sha256 of both outputs equal). Add a `GEN_PATH=1` switch to `build_circuit.rs` main that calls
`build_generated()` and writes a different filename; pin `HEO_PIN_TRACE_CCX_SITES=1` in source after the
recipe install (env is wiped, so source-pin it) to get `ccx_sites.tsv` (op_idx, kind, file, line, phase)
for the whole record circuit. One build+run ≈ 3.5 min. Always sha256-verify replica == shipped before
attributing anything.

## Trap 1 — the tautological shortfall histogram

If holds are placed greedily under `live+extra+1 <= cap`, then measuring skipped candidates' shortfall as
`max(live+extra_final)+1−cap` returns exactly 1 for every skip **on any stream** — by construction.
It carries zero information about needed width. We published `[1166,0,0,...]` as if it were a measurement;
it is a tautology. If your histogram is suspiciously degenerate, check whether the instrument can output
anything else at all.

## Trap 2 — uniform shift ≠ peak clip ≠ Q-cut (three different models)

Relaxing the cap by W in simulation (cap+W) is a **uniform live-shift** bound (optimistic). A real width
cut is a **peak clip** (`live' = min(live, cap−W)`), and a real Q-row cut is clip **plus** a lower cap.
Measured on the record stream (1,219 hold candidates, 53 placed at baseline):
- uniform cap+W: +1 → 160 holds, +2 → 264, +4 → 465, +8 → 802 (the optimistic curve)
- Q-cut model (clip + reduced cap): cap 1233 → **27** holds, 1232 → 17, 1230 → 2, 1226 → 0 — **holds collapse**,
  because holds stack 25–30 deep at live≈1205 positions and a lower cap destroys stacking room.
So a Q-cut carries a holds **penalty**, not a bonus. Correct door arithmetic for this tree (exact fractions,
S0=912,518,320, T0=739,479.769, measured qcut holds): C_max = S0/(1234−W) − T0 − (53−h(W)) gives
W=1 → 574.0, W=2 → 582.3, W=4 → 588.5, W=8 → 596.6 T/qubit — strictly below the naive T/Q = 600 at every
measured W. Run all three models before quoting a "door", and compute the door with exact fractions, not
mental math.

## Empirical cap-knob pricing (measured, 5ba2d2d4 generator replica)

The walk-cap pins form a hierarchy (last wins): skywalk recipe 1172 → leapfrog recipe 1234 → a2_recipe 1234;
the square phase has its own literal phase cap (`with_phase_cap(Some(1234))`), NOT the dead LF_SQUARE_CAP env
pin. Cutting ALL of them to 1233 does deliver a 1233-peak generated stream (verified per-phase) — at
C(1) = +726 expected T (divide +272, multiply +452, square +2), which EXCEEDS the 574 door: Q1233 by cap knobs
loses ~156k score. Lesson: the square cap cut is nearly free (+4 native CCX); the walks carry all the cost.
And any stream-changing edit hits the pinned-table rebind wall immediately (lane3_sigcut's length assert
panics first) — budget the rebind before celebrating a knob that moves.

## Trap 3 — pre-loan vs with-loan numbering drift

Dup loans insert 2–7 ops per loan end; 18,040 loans shifted positions by ~43k ops (~0.4%). A supply probe
that compares candidate windows (pre-loan numbering) against binding positions measured on the with-loan
stream is silently comparing two different coordinate systems. Either measure positions and candidates on
the SAME stream version, or track the insertion offset map. When in doubt, re-derive candidates on the
stream you actually measure (`dup_candidates(s1)` on the with-loan stream).

## Trap 4 — internal consistency is not evidence; only the shot oracle judges

A round-2 iterated-loans variant (re-derive candidates on the with-loan stream, place 4,641 more loans,
+2 holds) passed every internal check — symbolic-value asserts, clean condition-stack boundaries,
relocate 0-failures — and the official eval **failed it**: 20 classical mismatches + 13 phase-garbage
batches (one coordinate wrong on specific shots). Any loan/hold extension must be certified by the
official shot eval before any "gain" is claimed. Stream-hash parity with the baseline is the fast
negative check (restoration proof), not a correctness proof of a changed stream. Measured twice on
5ba2d2d4: naive round-2 (4,641 loans) failed with 20 classical mismatches + 13 phase-garbage batches;
then with every window spanning a measurement/reset op excluded (the obvious suspect), 4,613 loans still
failed with 18 classical + 6 phase — so the corruption is
structural to re-candidacy on an already-loaned stream (remaining suspect: condition-stack nesting of
round-1 pop/push artifacts), not any single op-kind interaction. Iterated loans need a candidacy rule
derived from the insertion mechanics, not filtered from the original one.

## Measured reference numbers (5ba2d2d4, certified 912,518,320 / 0-failures)

- Pipeline: 42,431 dup candidates → 18,040 placed (attrition = insert_loans source failures + bans, not
  the per-wire filter); 1,219 hold candidates → 53 placed; 2M-op window never binds; relocate 180/0.
- Supply at the four hottest hold-binding positions (with-loan ops 6.51M–6.80M): **zero** covering windows
  (correctly numbered). 7,661 residual candidates on the with-loan stream; 722 windows / 74 wires overlap
  the wider binding region; converting them corrupted the stream (Trap 4).
- Hold windows span the whole 1234 shelf (divide 0.48M–3.35M, square 4.3M–5.3M, multiply 6.4M–9.56M pre-loan);
  regional shaves leak: one 4096-op block → +1-2 holds; 360k-op binding region → +28 T (vs +107 global uniform).
- Rejection attribution after a regional shave: 71% raw-shelf positions (live ≥ 1234), 29% stacked/near-peak.
- The shelf = 1,740 maximal plateaus at exactly 1234 (332,602 positions; longest 15,958 ops) — tick-scale
  peaks; a whole-shelf shave is a width-schedule change covering every capped tick, not a local fix.

## What this implies for route choice

- Cheap hold_pass extensions on a heavily loan-optimized tree: measure supply at the binding instants FIRST
  (zero here); expect iteration rounds to need loan-artifact-aware candidacy and re-validation per round.
- Q-cuts: price with the Q-cut model (holds collapse), not the uniform curve. The door is ~574 T/qubit here.
- A rival's announced "v2" measured on THEIR tree does not transfer after your edits change the stream
  (our choice_narrow edits eliminated the dup supply his v2 presumably mined). Re-measure on YOUR tree.
