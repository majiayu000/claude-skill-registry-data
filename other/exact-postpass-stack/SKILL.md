---
name: exact-postpass-stack
description: "Port or stack exact stream-level post-passes on a finished reversible/quantum op stream: NCT pair folds and sandwiches, multi-round folds, symbolic control-product proofs, reverse and slack folds, commuting-pair cancellation. Use when a rival row carries a post-pass chain your tree lacks, when deciding whether a fold family will pay on a stream, or when a stacked pass breaks a table, a nonce tail, memory or the CI time envelope."
---

# Nachputzete (exact-postpass-stack)

nasqret's ecdsa.fail 660 chain (7-8 Nov 2026) took a frogdrop stream from 486,601,558 to 474,071,120 at constant width: -12.53M T, -2.58%, value-exact. It used seven passes shipped across six rows: slack_fold and commuting_pairs went in together in 15df559e. The later rerun after our holds (389f99c3, ~110k) is outside that figure. This skill is the port recipe. The per-pass catalogue behind it (file:line citations into his public row sources, plus our own rebuild measurements) is a campaign record and is not bundled; fetch the rows with `ecdsafail reset <id>` to read the passes.

## 1. Decide whether it pays

Exact local NCT folds pay on streams that are **ancilla-starved, Toffoli-dense, uncompute by replaying Toffolis, and have a thin post-pass stack**. They pay ~0 on streams that uncompute by measurement (temp-AND) or were already taken through a truth-table simplifier. Measured gate_fold yields:

| Family | gate_fold effect |
|---|---|
| frogdrop 660 | -1.36% (gate_fold alone, 6d94a56a) |
| frogdrop 659 | ~-1.28% (round 1 alone); -1.39% together with named_controls + retained_sums |
| streams that uncompute by measurement, or that a truth-table simplifier already took | about 0 |

The other passes have only been measured on frogdrop. Before porting anything, run gate_fold alone on the target stream; if it removes ~0, the other pair folds probably will too. named_controls works on provably-constant control products, a different mechanism, so measure it separately.

## 2. The stack, in order

As in nasqret's 389f99c3 `build()`:
1. Raw emission.
2. Certified cut-list fused with gate_fold round 1: pair folding `C(a,b;t), C(a,c;t) -> t ^= a·(b XOR c)`, sandwich cancel, corridor pairs with lookahead 12, 16,384-op blocks.
3. `finish_rounds`: four more forward rounds.
4. `named_controls`: symbolic proof of 0/1/equal control products.
5. `retained_sums`: a second named-controls pass with a FIFO definition ring.
6. `reverse_fold`: three backward folds in fixed 2M-op regions, then adjacent-pair cancel.
7. `slack_fold`: forward/reverse/forward sweeps with lookahead 256 and capacity-bounded headroom, plus `commuting_pairs`.
8. Product holds, if used, from a table bound to the post-fold stream.
9. slack_fold again, at most 2 rounds, stopping early on a zero round.
10. Append the row's own nonce identity pair last.

Each pass needs its own off switch that reproduces the previous stream byte for byte, checked with every downstream op-index or fingerprint table disabled. With such a table active, switching off an upstream pass panics at the table's guard.

## 3. Exactness: two classes

- **Permutation identities** (gate_fold, finish_rounds, reverse_fold, slack_fold, commuting_pairs, the rerun): local Boolean identities and involution pairs inside one condition segment. Barriers keep phase, measurement and classical order. This holds for arbitrary wire values on well-formed ops: distinct control and target wires, empty unused fields. Hashes only choose table slots, and the full gate record is always compared.
- **Contract-relative proofs** (named_controls, retained_sums): immutable names and full-key compares. They are exact only under the register contract: declared registers arbitrary, every other wire and bit starting at 0. They must run on the whole stream with its declarations, never on a fragment.

A note on a mixed stack attributes each premise to the pass that carries it. Our relocating holds bring a hash-label premise; the folds do not.

## 4. Port steps

1. **F0: rebuild the base to the digit** from its public source. Done when your stream sha and fasteval T equal the published row.
2. **Copy the pass files verbatim** and wire them in the order above. Done when every off switch reproduces its predecessor byte for byte, with downstream tables disabled.
3. **Measure on the full stream only.** Prefix extrapolation is wrong in both directions: on the 2M-op prefix, retained_sums read 60x too high and slack_fold 3.8x too low. Log per-pass removed-instruction counts. Done when you have full-stream fasteval T for each cumulative stage.
4. **Regenerate everything op-index-bound** after the last upstream change: SIMPLIFY cut-lists, hold tables, fingerprint tables. Done when each table's own off-switch check passes on the new stream.
5. **Re-place the nonce last** (see H1). Every exact pass re-rolls the official shot set, so expect a CPU nonce retry about 1 time in 8 at lambda ~0.125. Done when the stock evaluator shows 9,024/9,024 OK at the baked nonce.
6. **Time and memory.** Time the build against an accepted row of the same family on the same box. Keep every pass in place, holding one ~67 GB vector, never two. Done when the emission plus eval fits the 45-minute grader envelope with margin.

## 5. Hazards

- **H1. Nonce erasure.** commuting_pairs cancels an identity nonce pair emitted before the post-passes, so nonce re-rolls stop working and fingerprint checks panic. Append a fresh pair after all passes.
- **H2. Op-index tables misapply silently.** The SIMPLIFY cut-list has no content check. A live SIMPLIFY run takes > 1 h and 128 GB, so ship a regenerated certified table instead.
- **H3. slack_fold depends on Vec capacity.** The same input with a different allocation history can give a different stream. Generate tables from the builder's own dump; never rerun slack_fold in a side tool.
- **H4. Boundaries are part of the output.** Block and region alignment changes results, so keep them verbatim.
- **H5. Out-of-memory kills.** nasqret attributes 14964ff2's exit 137 to holding a second full-size vector. The parent's two-vector path had passed, so the cause is not certain. His fix was an in-place mapped replay, with no rule change; keep every pass in place.

## 6. Process worth copying

He ships **one named mechanism per row**, about every 50-60 minutes. Each note follows a fixed order:
- parent id and graded T;
- why, with the measured residual of the previous pass;
- the identity, in notation, with a worked example;
- the barriers;
- the implementation constants;
- the evidence: an independent reference implementation compared on every record field;
- reproduction commands with the off switch;
- the line "the official evaluator decides".

After a failed row he published a fixed one 20 minutes later and said plainly what the failure did and did not show.

Source rows (nasqret, credit by id): 6d94a56a, 2e59f5be, 32ace839, 963dfad0, 4527e9d7, 15df559e, 389f99c3. His notes are public on the ecdsa.fail board. Related: `bounded-commuting-fold` (pass 7 and 9 detail), `hosted-carry-lending`, `exact-hold-pass`, `schedule-tail-truncation`.
