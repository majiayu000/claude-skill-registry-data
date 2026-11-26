---
name: exact-hold-pass
description: >-
  Exact final-pass Toffoli reduction for reversible/quantum op streams: replace
  repeated unconditional Toffolis with a CX copy from a held wire (product holds),
  and clear-then-rebuild idle live wires whose value another live wire duplicates
  (dup loans, Clifford-only). Uses affine symbolic value tracking with a random
  128-bit hash, a provable width cap, and fail-closed relocation. Use when a stream
  recomputes products or carries duplicated live values over idle intervals.
whenToUse: Looking for exact (zero-lambda) Toffoli cuts late in a circuit pipeline; building or auditing a hold/loan pass; checking that a value-reuse rewrite preserves the RNG/measurement schedule
---

# Pfandleihi (exact-hold-pass)

*Exact Hold Pass (product holds + dup loans)*

Distilled from haotang1995's `hold_pass` (ecdsa.fail record submission e5f4dddc,
2026-10-29): 17,919 dup loans + 53 product holds, −53 T **exact** (dλ 0.000,
identical failing shots), implemented as the last pass before the nonce tail.
Reusable on any reversible op stream with repeated products or idle live wires.

## The two primitives

- **Product hold.** If an unconditional `CCX(a,b -> t)` is recomputed later and the
  product still lives on a held copy, replace the repeat with a `CX` from the copy.
  Place a hold only if (live count + already-placed holds) ≤ width cap over the
  *whole* hold interval, and the copy sits on a wire provably |0⟩ at placement.
- **Dup loan.** If a live wire is idle over an interval and another live wire holds
  the same value (or its complement) at both interval ends, clear the wire with `CX`
  at the start and rebuild it with `CX` at the end. Clifford-only; frees width that
  product holds can spend.

## Why it is exact — the correctness machinery

- Track every wire's value **symbolically as an affine form** over atoms: inputs,
  measurement outcomes, and products of affine forms.
- Fingerprint forms with a **128-bit random linear hash**; equal hash ⇒ identical
  function up to collision probability ~2^-128. "Provably |0⟩" means form 0.
- **No measurement is added and no RNG draw changes** — the random-coin schedule
  stays aligned, so the nonce machinery upstream is untouched.
- **Fail closed**: if any relocation step cannot prove its precondition, the pass
  returns the stream unchanged, not a best-effort edit.

## Operating rules

- Run it **last**, after every statistical pass, before the nonce tail — earlier
  passes change the stream and invalidate the intervals.
- Verify with a paired exact evaluation against the parent: expected signature is
  dT < 0 with **dλ = 0.000 and byte-identical failing-shot sets**. Any λ movement
  means the symbolic model leaked; revert and autopsy.
- The exactness caveat is the hash, nothing else: exact up to ~2^-128. Say so in
  the note.

## Where to hunt for holds

- Repeated unconditional products emitted by template bodies (compute/inverse pairs
  that re-derive the same intermediate).
- Long idle intervals on live wires near the width peak — a dup loan there converts
  dead width into hold capacity exactly where holds need it.
- Do not confuse with measured-lifetime elimination at fixed width: their worker
  logged 38,665 such attempts with 0 committed. Loans and holds pay because they are
  *value-equality* driven, not liveness driven.
