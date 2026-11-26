---
name: bounded-commuting-fold
description: >-
  Exact commuting-pair cancellation for very large reversible/quantum op streams:
  per-wire last-read/last-write dependency stamps, canonical-gate matching with
  classical conditions retained, stable-condition-block pair cancellation,
  in-place billion-op memory discipline, and the holds-then-fold rerun (slack fold
  again after the hold table: at most two rounds, stop early on a zero round). Distilled from
  nasqret's public ecdsa.fail notes and source (Q660 15df559e, 389f99c3, Nov 2026).
whenToUse: Building or auditing a stream-level peephole/cancellation pass on a large reversible circuit; deciding pass order relative to hold/dup-loan passes; making a billion-op fold run in bounded memory; pricing guarded vs unconditional gate savings
---

# Faltschachtle (bounded-commuting-fold)

A pass that deletes pairs of identical product-toggles separated by intervening work,
provably exact. The pair search is **block-local**: commuting_pairs runs once per lowered
16,384-op block inside slack_fold (`slack_fold.rs:79`), so pairs farther apart than a block
are never found. The billion-op in-place discipline belongs to slack_fold. nasqret's version and reports its
savings split into *charged* (unconditional) vs *guarded* (conditioned) — only the
trusted evaluator's executed count is evidence.

## The commuting rule (the exact core)

Two `CCX(a,b,t)` (toggle t by the product a·b) separated by other gates can cancel when
the intervening gates provably commute with them. The stamp rules below are a **sufficient**
condition, not a characterisation; they also block on a later read of the target t:

- Track **one stamp per wire**: most recent read position and most recent write position.
- For X / CX / CCX: a candidate is blocked if anything after the first gate **read t**
  or **wrote a or b**.
- For Z / CZ / CCZ (diagonal): check the **last write on every argument**; diagonal
  gates on overlapping wires commute with each other.
- Lookup key: sort the two CCX controls; for CZ/CCZ sort all quantum arguments; the
  key retains the explicit classical condition. A table hit is only a *candidate* —
  the deletion requires **exact comparison of the complete gate record** (a hash
  collision can suppress an opportunity, never allow one).
- A gate already consumed by an earlier deletion cannot be reused. Stale dependency
  stamps may be left in place after a deletion: they only make later matches harder
  to accept (the safe direction).

## Conditioned pairs

Two explicitly conditioned gates may cancel inside a stable condition block **iff the
conditions are identical** and all wire dependencies pass — they then act on exactly
the same shots, so the executed T saving equals the static one. Delimiters that end
the pair search: resets, measurements, swaps, register annotations, classical
mutations, any change to the captured-condition stack, and any wire index >= 2048
(`commuting_pairs.rs:4, 75-83`). A phase rule matters: a
phase gate depending on a toggle's target can distinguish two otherwise equal
sequences — treat phase writers as full dependencies.

## The holds-then-fold rerun (pass order is the mechanism)

Placing a hold (copying a product onto a free wire, restoring it later with CNOTs)
changes which wires are read/written near both endpoints — it can *expose* commuting
identities that forward and reverse fold sweeps already stopped on. So:

1. Run the hold/dup-loan table first (pinned to the exact stream).
2. **Reopen the local simplifier after it.** Loop at most two rounds; a round whose
   unconditional *and* guarded charged savings are both zero ends the loop.
3. Print a per-round removed-instruction summary; the official score comes only from
   the trusted evaluator on the full circuit.

## Billion-op in-place discipline

Bound the fold's extra live storage by `min(available capacity, ceil(input/256) slots,
4,194,304 slots)`. Per sweep, copy one block to a small buffer before writing the
transformed block back. Forward sweep: shift the input right by its allowance; reverse
sweep: read from the far end, write from the right of free storage, restoring native
order before the commuting test. Blocks may expand ≤ 1 slot per 32 records, with
headroom released in proportion to progress; if a block overflows its writable span,
re-lower that block with a tighter limit and re-check before copying. A vector whose
capacity exactly equals its length still works; later blocks reuse positions freed
earlier in the same sweep.

## Hazards found when stacking it (8 Nov 2026 forensics)

- **It deletes a positional nonce pair.** commuting_pairs cancels an identity nonce pair emitted before the post-passes. Nonce re-rolls then do nothing and fingerprint-bound hold tables panic. Fix: append the row's own nonce pair after every pass (our 9b0fcff2 / f5e8aeac). Alternatively, lift the trailer out before the passes and re-append it, as nasqret's 8e366dbc does (`mod.rs:177-190`).
- **The output depends on Vec capacity.** Headroom is `min(cap - len, ceil(n/256), 2^22)`, so the same input with a different allocation history can give a different stream. Generate tables from the builder's own dump; never rerun the fold in a side tool.
- **The rerun is two rounds, not a fixpoint.** 389f99c3 stops after 2 rounds, or early on a zero round. It paid ~110k at 660.

## Reporting discipline

- Savings are counted as *removed charged instructions*; executed savings come only
  from the official evaluator under real conditions (guarded ops are charged only on
  shots where the condition holds).
- Bound memory claims are part of the method's credibility: state the three limits.

## Source bindings

- nasqret `15df559e` (Q660, T 474,071,120): slack_fold.rs + commuting_pairs.rs (the passes themselves).
- nasqret `389f99c3` (Q660, T 472,530,838, 2026-11-08): fold-after-holds call site,
  commuting/storage rules, in-place limits.
- Parent-side hold tables referenced: haotang1995 / odinfree public implementations.
