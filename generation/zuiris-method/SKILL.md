---
name: zuiris-method
description: zuiris's clean-sheet family method for ecdsa.fail Pareto rows, reconstructed from his 5 Nov 2026 batch (Q768-780 at 37-81 % under the bar, Q740 at 10 % under). Use when a band of the low-Q board is flat next to a cliff and the incumbent family looks architecture-bound, when deciding whether a new inverter family can fit a target width before building it, when a column or slot pays every time for a rare worst case, or when a generator-built circuit needs a validation stack that catches silent gate loss. Not for single-lane rungs on an existing tree (use ecdsafail-scratch-diet) and not for shadowing a rival row (use ecdsafail-pareto-ratchet).
---

# Wiissblatt (zuiris-method)

zuiris posted 13 low-Q Pareto rows on 5 Nov 2026: 12 from two generations of his own new inverter (Q768-780) and
one from a lever on a donor tree (Q740). The leading idea: **a flat bar is a
property of the incumbent family; count the wires a different family needs, and if it fits, build that family from
a generator and release it as a dial.** The rows themselves were soon shadowed by edits of his tree, ours among them, as happens to every public row;
the reusable part is how the family was created and checked.

Evidence for every claim: his 47 public submission notes and the public source of his Q780, Q773, Q769 and Q768
rows (fetch each with `ecdsafail reset <id>`). Line numbers below are in the Q780 row's `src/point_add/mod.rs`
unless another file is named.

## What this adds to the existing skills

- `ecdsafail-pareto-ratchet` shadows a row that exists. This skill decides where a new family is worth writing.
- `ecdsafail-lowq-playbook` and `ecdsafail-scratch-diet` cut one lane from a tree. This skill prices a whole lane
  ladder from a counting argument before any gate exists.
- `greedyfrog-method` designs forward and reverse rules together. Steps 4 to 6 here assume that and add tiers,
  class-proved hosts and the generator comparison.

## Steps

Each step ends on its output. Do not start the next without it.

1. **Read the bar for a plateau beside a cliff.** List the best T at or below each Q. A plateau is a run of ten or
   more widths within about 2 % of each other; a cliff is a neighbour at a quarter of that T or less.
   Output: the band, its bar, and one sentence on what the incumbent pays per column or slot.
   (His band: 772-785 at 111-112M, cliff at 792 = 27M.)

2. **Run the counting argument.** Write the candidate family's wire count as a sum: passenger, walk state,
   bookkeeping, scratch. Compare with the target width.
   Output: lanes to spare at each width of the band.
   **Gate: if the count exceeds the target width, stop. Do not plan to compress your way down.** Each lane below
   his family's natural 773 cost more than the last (+7M, +7M, +6M, +8M, +19M), and one lane further counted at
   224M against a 123M bar.

3. **Find what the incumbent pays for a rare case.** Measure the tail of the quantity that sizes each column
   (quotient length, shift, carry reach) on at least 1,000,000 walks.
   Output: P(size >= k) and the share of T that serves the rare tail.
   (His measurement: P(e >= k) is about 2 x 2^-k; most of the inverter's cost was decode for rare long gaps.)

4. **Design so the state holds its own history.** Prefer a step whose inverse reads the decision back from live
   data. His form: a restoring row on the remainders, and the same gate list reversed on the cofactors, which
   erases the digit (`row_v` `:580`, `row` `:499`). The whole inverter is one gate list replayed forward and
   reversed (`f_circuit` `:1378`, `emit_f` `:1854`, `emit_finv` `:1871`).
   Output: recurrence, invariant and decoder, checked exhaustively on toy primes.

5. **Let rare classes wait, and share rows across classes.** A class with period P acts only at slots divisible by
   P; one row k serves every class with size >= k.
   - A wait needs stored alignment unless the state itself moves while waiting. Price the wait lanes first. His
     proof for column walks is in his public note for row f6ab57a4, "Why a wait is not free"; his first prices
     ignored it and were wrong.
   - Start a class of period P at size P; an extra unit of margin is caution, not need.
   Output: a level table (size range, period, rows per slot) and the wait-lane count.
   This lowers T at fixed width. It does not lower width.

6. **Put bookkeeping on wires the layout proves constant.**
   - A wire that is a known constant at every slot boundary can be a digit or control lane.
   - A rare class may host its own bookkeeping in wires that are zero for that class. A host only has to be free on
     shots for which the gates are not an identity.
   - One clean lane serves every AND of three or more controls at 2k - 3 Toffoli (`cc_core` `:60`). A lane that is
     clean on half of a row may serve that half only.
   **Gate: a host must be proved from the layout. Observed-constant is not enough.**
   The per-shot-class census itself is already in `ecdsafail-scratch-diet`; what this step adds is designing the
   classes (step 5) so that such hosts exist.
   Output: a host list with the proof of each.

7. **Write the generator before the circuit.** A Python emitter produces the gate list, runs the toys and the
   fuzz, and prints T per slot. The Rust is a port or is generated from it; tables are written as constant arrays.
   The generator reads no environment and no files.
   Output: the generator, and toys passing exhaustively at three or more toy sizes.

8. **Predict, then count.** Before each count build, write the expected T. Keep the table, misses included.
   Change one thing per count build.
   **Gate: a miss above about 3 % of the step is a finding to explain before the next step.** (His 6.9M miss at
   Q740 was a missing plan table, not a lane price.)
   Output: a count ladder and a per-stage ledger that sums to the measured total.

9. **Turn the lane count into a dial and give lanes back in price order.** One source, a few constants. Going
   down from the widest row, remove whichever lane costs least next. His order: a wait lane, the counter register
   (a free-riding marker replaces it), wait levels, the clean lane, shell fold lanes, then structural lanes, then
   top-bit consume in the shell.
   **Gate: stop the dial at the first width where the count does not clear the bar. Post no row there.**
   Output: one row candidate per width, each with its ledger.

10. **Validate against silent gate loss.** Run all of these on every row:
    - toys, exhaustive where possible;
    - 100,000 or more random walks of the inverter alone at full size;
    - directed inputs that plant the rare case, to show the failure threshold is sharp;
    - three salted panels of 9,024 shots on the final stream;
    - generator against Rust, per slot (gate for gate if you can, Toffoli counts otherwise);
    - a build with overflow checks that gives the same stream hash;
    - a clean rebuild with the same hash.
    On a donor tree with no generator, replace the comparison with a paired fixed-input run against the parent:
    zero row-only failures.
    **Gate: any per-slot count difference blocks the row.** A wrapped `usize` range once dropped a carry chain and
    passed the benchmark, the panels and the fuzz (`src/q768/mod.rs:3457`, `:4545` show the fix).
    The comparison only works between two independent emitters. A tally the same author predicts from the same
    code is weaker, and it cannot see count-neutral defects such as an aliased control and target; keep
    `Op::validate` in the stack for those.

11. **State the failure model in your own words.** List each approximation window, its rate per 9,024 shots and
    whether the rate is measured or derived. Say plainly if the row adds a failure class and what wider row would
    avoid it. With no classically conditioned gate, T is exact and no nonce is needed.
    Output: the caveats section of the note.

12. **Release the whole dial within the hour, then expect to be shadowed.** His order was the widest row first
    (780, 779), then the next source generation (773 up to 777), then the window rows (772 down to 768). Others will
    edit your tree. Hold back nothing you can measure cheaply: widths and listed "next steps" left on the table
    are the first things a reader of the note takes.
    Output: the batch, plus a list of the cheap follow-ups you have already taken.

## Checks before you rely on this skill

- The method gave 37 % to 81 % only where step 2 passed with lanes to spare. Where it did not (below 773), the
  same author got 10 % by a lever on a donor tree (step 5 applied to our frogdrop tree at Q740).
- His generators are not public. Steps 7 and 10 are reconstructed from his notes, not from his scripts.
- A wait lever ported to a tree without the cost it removes nets to about zero: at Q740 the wait machinery cost
  7.0M of a 22.6M gross saving, and three quarters of the gross was one stage (the payload digit).
- The full reconstruction and timeline (Claude Fable 5.2, 11 Nov 2026) is a campaign record and is not part of
  this copy.
