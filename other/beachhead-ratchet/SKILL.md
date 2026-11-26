---
name: beachhead-ratchet
description: "Take a left Pareto move even when it raises Toffoli, under a T budget written down first, then win the cost back on your own tree, attributing every lever to the component the width cut made dearer. Learned from bulengerk's ecdsa.fail record (9 left moves, 61 down rows). Use when a width cut works but costs T, when you hold the leftmost row of a band, or when a rival posts rows built on your tree."
---

# Brüggechopf (beachhead-ratchet)

A **beachhead** is a left move taken even though it raises Toffoli: the narrower row is posted first, under a written
T budget, then the same tree is **ratcheted** down by recovering the cost the width cut added. bulengerk made nine
left moves on ecdsa.fail; seven raised T, by roughly +11% to +122%, and he ground each one back on his own tree. Q770:
three left moves in about six hours took T from 186.6M to 304,134,670 (+63%; his stated target was 300M and the
overrun of 1.38% was explicitly permitted). Then 13 down rows in about 31 h reached 115.4M (-62%), and about 62% of
that cut recovered his own purchase. Q792: landed at +31%, then 37 reductions (38 rows in all) to -54%. Cites:
[EVIDENCE.md](EVIDENCE.md).

Board rule: a narrower row with higher T is a valid **Pareto** row when no official row at <= its Q has a lower T. It
is never a product (spacetime) record; all nine of his left moves were graded "rejected: score did not improve current
best", the board's status for a validated Pareto row.

## Use it / leave it

- Use when a width cut works but costs T; when you hold the leftmost row of a band; when a rival posts rows built on
  your tree.
- Leave to other skills: base reproduction, integer gates, the serial queue, validator preflight and lambda accounting
  (`ecdsafail-pareto-ratchet`); the qubit cut itself
  (`invariant-chart`, `ecdsafail-scratch-diet`, `ecdsafail-lowq-playbook`); failed shots (`shot-autopsy`).

## Steps

1. **Freeze the frontier and the base.** Snapshot the official board (save the API response with its read time) and
   rebuild the base row in an empty environment. Done when your build reproduces the base's ops sha256 and graded T to
   the digit, and the snapshot file is saved.
2. **Write the T budget, then buy the qubits.** Record a number before building (e.g. "target 300,000,000 T; overrun
   allowed up to x%") and build the width cut. Done when the narrower build passes 9,024/9,024 on all three channels
   locally, T is within the written budget, and a fresh read seconds before submitting shows
   `T_new < min(T_official : Q_official <= Q_new)` (an empty minimum counts as infinite). His two misses (Q774, Q695)
   landed after a better rival row and were not advances.
3. **Attribute the purchase.** Write the baseline circuit's component costs, then the signed delta each component
   took from the width cut (wire count, Toffoli per call, call count), measured from instrumented builds of both trees,
   not from a model alone. Done when baseline + signed deltas reproduces the narrower row's measured executed mean
   within a stated tolerance (his Q770 component model: 196,250,688 vs 196,250,710 measured; 0.01% is a proposed
   tolerance, not his rule).
4. **Recover the purchase first.** Attack the components with the largest positive delta before generic levers; each
   lever is an exact transformation (pay precision, never trade error for score). Post only when an integer gate
   against the immediate parent passes: his gates were ">= 5% below that parent's executed cost" (Q665 row),
   `10 x new_sum <= 9 x baseline_sum` (a 10% gate, Q660 row) and "the user's strict four-percent threshold" (final
   Q792 row); write yours down with its operator. Keep call signatures so overlays stay small (his -9.63% row was a
   13-line diff). Done per post: gate met, 9,024 clean on all channels, frontier re-read as in step 2, queued through
   `ecdsafail-pareto-ratchet`'s serial submit.
5. **Chain locally on frozen parents.** Build each child on the frozen parent archive while the parent validates. A
   chained row is only done when its own official metrics come back for its exact artifact, or when it is repaired and
   requalified (`shot-autopsy`), or explicitly abandoned with the reason recorded.
6. **Defend your lineage.** Against the frozen snapshot, diff every rival row at your Q that was built on your tree:
   list its edited files, re-absorb the byte-identical ones, and merge the rest with yours (his row 11 beat nasqret by
   4.1% five hours after nasqret posted on his tree). Record a disposition per rival row (absorbed, merged, rejected
   with reason). When rivals open a lower band, consider leaving your lineage for theirs (9 Oct: he left Q792 for
   gnuchev's frogdrop tree the same day). Done when every rival row at your Q in the snapshot has a recorded disposition.

## Gates and kills

| gate | pass | kill |
|---|---|---|
| budget | left move within the written T budget | over budget: shelve or re-plan the cut |
| attribution | baseline + signed deltas within the stated tolerance | outside: a component is missing; find it before the next lever |
| ratchet | your written integer gate passes; exact; 9,024 clean | below the gate: accumulate levers into one post |
| frontier | `T_new < min(T_official : Q_official <= Q_new)` at submit time | fails: rebase on the better row (step 6) |
| contract | the inherited limiting contract (PR 419 terms 1-4) checked and copied verbatim into the note | missing: no submission |

## Generalize (untested analogy)

Boards where a structural step costs a temporary penalty: take the step under a written budget, then recover on your
own artifact with a fixed gate. Not yet tried outside ecdsa.fail.

## Sources

[EVIDENCE.md](EVIDENCE.md), which cites bulengerk's public submission notes by submission id and note line.
