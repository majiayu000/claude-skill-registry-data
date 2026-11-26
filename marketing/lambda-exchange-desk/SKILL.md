---
name: lambda-exchange-desk
description: >-
  Price statistical trades in an approximate-circuit campaign as an explicit exchange
  market: fix a Toffoli-per-lambda rate, measure every trade paired against its parent
  with a standard error, charge conservative floors, scan for buybacks priced below
  the rate, and guard census-fitted tables against in-sample overfitting. Use whenever
  an ecdsa.fail-style circuit trades executed Toffoli for failure rate before a nonce
  grind, or any scored artifact trades score for a statistical defect rate.
whenToUse: Approving, pricing, or reverting an approximate (statistical) circuit edit; fitting per-block parameter tables from shot censuses; deciding whether a lambda buyback is worth its Toffoli cost
---

# Wächselstube (lambda-exchange-desk)

Distilled from haotang1995's two record submissions (2026-10-29), where a stack of
approximate trades was run as a priced market: rate **500 T per unit lambda**, every
trade measured, some trades *reverted* when the market moved.

## Fix the rate first

- Declare the exchange rate (T per unit λ) before evaluating any approximate edit.
  Derive it from nonce economics: at failure rate λ per shot set, one clean island
  costs ~e^λ trials; λ is expensive in GPU-hours, not just in score.
- Trades are approved on **effective dT**: measured dT minus rate × max(dλ + SE, floor).
  Their floor: a minimum three-event charge against the Toffoli delta.

## Measure paired, or not at all

- Every trade reports dT, dλ, and the paired SE **against its own parent**, same
  shots, same seeds. Unpaired comparisons against a distant leader are marketing.
- Verifier-level SE (e.g. ±0.31 λ at 1M shots) cannot resolve small trades; the
  *worker* must run 4M–16M-shot paired runs to resolve its own layer.
- Interactions between layers are measured only through whole-circuit runs — never
  assume additivity.

## Run the buyback scan

- Prices move. Their choice-window pass sold λ at ~500 T/λ on ticks 1–119, then a
  later census showed ticks 81–112 had overpaid: reverting them bought λ back at
  **~325 T/λ** (+96 T, −0.295 λ) — below rate, so the revert is pure profit.
- After every accepted stack, re-price every open position in both directions.
  A revert that buys λ below the rate, or a new sell well above it, is a trade.

## Census-fitted tables: out-of-sample or reject

- Their per-block width table v1 looked +368 T effective in sample and only +212
  out of sample — a 42% overfit. v2 used more shots, a conservative estimator, and
  content-keyed rows.
- Rules: fit on a training census (e.g. 8M shots), validate on disjoint shots,
  key every row by content hash (FNV-1a), fail closed on any mismatch, and keep the
  uniform default for unlisted blocks.
- Selection rules need floors: their repair census required ≥5 repaired failures,
  **zero** added failures, and zero ancilla failures per admitted repair.

## Discovery-model quarantine

A classical/ideal model may guide discovery but is never evidence: it does not model
quantum phases or width-envelope failures. Their calibration: walk-model predictions
overestimated realized circuit gains **1.5–2×**. Price from paired shots, not from
the model.

## Measured case: a reserve can be priced out, not just exhausted (our own, 2026-10-31)

On the 5ba2d2d4 record tree, a structural census of the choice_narrow compare-narrowing table found room in
EVERY row (all 476 rows ≥3 chain units free; 416 ≥8): the naive read says "-476 T per +1 deepening sweep".
The sweep measured -367.0 T executed (dropped units execute ~77%) but the official eval FAILED with 20
classical + 17 phase-garbage failures on the fresh 9,024-shot set — dλ ≈ +2,216 ppm for -367 T ≈ 0.17 T/ppm,
~3,000x below the 500 T/ppm rate. Tie-model calibration gave q = P(overflow|tie) ≈ 0.0042, and even the
cheapest decile projects ~95 T/ppm. The reserve was real and unprofitable: the team stopped there because
their census already priced it, not because they ran out of rows. Lessons:
- Structural room is not a prize; only a paired price is. Run the room census AND one decisive sweep before
  claiming a reserve.
- λ units in this economy are ppm of failure probability; the 19.5 limit and the 500 T/ppm rate both come
  from island re-grind economics (a submission/stream with true rate λ fails its 9,024-shot eval with
  probability ~1-e^{-λ·9024} and re-grinds cost e^{λ·9024} retries). Sub-ppm trades are invisible to one
  official eval — 4M-16M-shot paired censuses are the resolution, and a coarse 9,024-shot sweep still bounds
  aggregate λ when failures actually occur (failures/9024).
- A fresh Fiat-Shamir shot set means any stream-changing sweep is an unpaired measurement; fine for
  coarse gates, never for desk-grade pricing.
- Bisect before concluding: a d<=2-only subset sweep (448 rows) still failed 18/9024 for -335.1 T — the
  λ was broad-based, not a hot tail. The uniform tie-probability model (2^{-(L-d)}) underestimated the
  realized rate ~1,000x: walk registers are strongly correlated, ties are common, and ~every tie breaks
  downstream (q ~ 1 on this tree). Depth-prior ranking would have predicted a cheap core that does not exist.
