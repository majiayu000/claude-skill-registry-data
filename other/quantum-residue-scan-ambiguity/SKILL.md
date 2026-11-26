---
name: quantum-residue-scan-ambiguity
description: Diagnose a reversible residue or CRT scan when more than one label passes a truncated predicate. Separate physical implementation errors from predicate ambiguity and test whether an independent residue can resolve the tie.
---

# Zwickmüli (quantum-residue-scan-ambiguity)

*Audit every accepted label*

Bind the emitted loader, exact mark predicate, threshold, rounding, erased-bit count and label order. Obtain the true label independently using full-precision arithmetic. For each source-valid input record **all** accepted labels, their order, and the accumulated output.

1. Compare the narrow circuit to a wider reference implementing exactly the same predicate, on the same entries. Check mark decisions at every label, phase, workspace including dirty scratch, and final output. Compare alternative thresholds against the full-precision predicate in a second experiment so a changed acceptance rule has its own failure set.
2. Track zero hits, missing true label, extra labels, and the actual decoded result. In an XOR accumulator, two accepted labels produce the XOR of the two, a third label. An even-hit parity flag detects this example but cannot distinguish zero from two hits or select the correct member. A first-hit/last-hit repair needs an ordering proof. A quantum bit erased in the X basis gives a random classical result and can introduce phase.
3. Compare the true and spurious labels on all proposed discriminator signals. Reject a bit that separates one pair but rejects a legitimate root on another input. An independent CRT check can be useful when a truncated residue wraps close to a multiple of the modulus. Derive its scale and carry explicitly, prove it accepts every true root, and price extra precision, scratch, guard and inverse in the narrow emitter.
4. Record shared and candidate-only failures on paired inputs. Estimate the rate on an independently drawn sample. For zero errors in `n` independent shots the exact one-sided 95% upper error bound is `1−0.05^(1/n)`. For combined stages, count the union by input ID. Report which stages entered the union and validate the complete circuit on its prescribed draw.

In one case a truncated predicate produced one bad input in a panel of 524,288 and zero in an independent panel of equal size. The first panel's complete accepted-label list exposed the collision. Neither the improvement in average rate nor the second panel establishes uniqueness for all inputs.
