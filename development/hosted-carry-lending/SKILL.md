---
name: hosted-carry-lending
description: Lend role wires that are proved clean during a column interval as exact scratch inside a fixed-role walk circuit (boundary-clean words, manufactured zeros, X-basis erasure with a retained mask, cross-traversal carry pairing). Use when a width-starved layout pays for a missing scratch role, when a scratch allocator reports exhaustion while role wires sit idle at column boundaries, or when porting nasqret's 659 lending levers to another width.
---

# Untermieter (hosted-carry-lending)

A walk/traversal circuit gives its wires fixed roles. Between columns some of them are provably clean, and lending them as scratch can replace a missing scratch role. On ecdsa.fail this is what moved 659, and it does nothing at 660. **Price the layout you are at before porting.**

## Where it pays

| Width / layout | Effect | Evidence |
|---|---|---|
| 659, three scalar roles (C659_THREE_ROLES) | large | nasqret 8cbf5b45: -56.7M vs our 506e8a66; 119047a6: -13.9M more |
| 660, four-role frogdrop | **zero** for the boundary loans, the normalization recovery and the X-basis erasure. All three are already in the 660 tree (`with_terminal_loans`, `g = scratch[8]`, `D660_DEFER_S/TAG/TZ=1`) | read from the public 660 source |

The 659 gain comes from recovering the three-role width penalty: +88.4M T versus the four-role 660 layout, measured paired. A layout that already has its fourth role gains nothing from these levers.

## The levers (nasqret 8cbf5b45 / 119047a6, unless marked)

- **Boundary-clean words (L1).** In the no-payload traversals T2 and T3, the 256-bit terminal word occupies P2..P257, so P0/P1 start every column clean. nasqret binds P0 as the 4th scalar owner in columns 36-119. The payload traversals never lend P0/P1. A wire serving as a scalar source must be excluded from the donor bank until the role's last use.
- **Manufactured zero (L2, quotient normalization).** A reversible transposition moves the capped low-bit exception into an unreachable shift/parity code, so a quotient wire is zero during ring-only shifts. That wire is lent, then restored from the parity and the zero-exponent predicate. Exact by an unreachable-code argument, tested on 512 lanes at four columns; no proof is shipped.
- **X-basis erasure with a retained mask (L5).** odinfree's lever (eb32c57a, 25 Oct; `D660_DEFER_*`), which nasqret back-ported to the 659 code. Where a tag or sum wire is erased, measure it in the X basis and keep the classical mask; the matching return traversal recomputes the same function and applies the phase correction. The erasure recipe is built from the three common scratch roles, ring and quotient, so both directions build the same recipe.
- **T1/T4 row loans (L6) and carry pairing across forward/inverse traversals (L7).** Row loans use the tag, the normalized Q0 and counter-pad lanes. Carry pairing pairs row recipes between two payload traversals that share one physical row bank. **nasqret removed both in 9a8559f7, without a stated reason** (~0.94M T given up on his own local figure).

## Pairing discipline, for L7

A forward recipe and its inverse pair only when:
- the builder checks the tag, the output wires, a digest of the typed recipe and the stack order;
- the stack is empty at the end of each pair;
- only recipes created inside a marked map scope pair;
- the inverse checks every physical operand, mask count and direction.

nasqret's L7 directed test covered 12,288 cases across both payload directions, comparing all quantum wires and the phase with independent measurement tapes.

## Before porting L6 or L7

Treat both as unproven until a directed falsifier passes: tag = 0, the counter-pad cutoffs +-1 column, and the Q0 cap exception.
- Keep L6 loans on a frame-local copy of the map core; on the outer core they leak into `walk_clean`, where Q0 is not zero.
- L7 needs a dirty bank that is identical in both traversals. The 660 `finish()` bank differs between T1 and T2.

## Counting

His per-map figures are raw pre-compile counts and do not sum to the official deltas. For example, 16,489,024 is L1 per T2/T3 traversal, and 65,422,156 is L1+L2 summed over all four traversals. Only the evaluator's executed count is evidence. Compare the official T of each row with its parent's.

## Board semantics

ecdsa.fail has a scalar product lane and a Pareto width lane. A row that cannot beat the best product counts on the Pareto lane only when no row at width <= Q has T <= its T: 389f99c3 (660) and c7997b07 (659) landed dominated. Pick the lane and the bar before you build.

Sources: nasqret's public notes for rows 8cbf5b45 and 119047a6, and 9a8559f7 (source read from its validation commit). Related: `quantum-mbundo-lifetimes`, `exact-postpass-stack`, `ecdsafail-scratch-diet`.
