---
name: quantum-borrowed-wire-counterexample
description: Prove or falsify a proposed Boolean recovery rule for a borrowed qubit using two reachable, baseline-passing states with equal available signals and opposite required host bits. Use when a narrow multiply or divide passes random tests but fails rare inputs.
---

# Schnorrichaib (quantum-borrowed-wire-counterexample)

*Find a counterexample to a borrowed-wire rule*

At the exact use, write the proposed invariant as `host = f(available signals)` on the enabled branch. Distinguish a known clean host, a known-one host that needs an X frame, and an arbitrary dirty host that must be restored. Specify the frame, program point, direction, classical controls and allowed inputs to the recovery function.

1. Derive the stable basis from every relevant write and alias in the *lowered* interval. Include allowed classical signals or state explicitly that the proposed function cannot read them. Collect ordered basis bits and the required logical host from a reference with an independent host. Record baseline success including product, cleanup and phase. Compare samples at the same enabled use in the same frame.
2. Challenge a missing branch through the arithmetic. For the secp256k1 example, choose a nontrivial cube root of unity `w` and a nonzero denominator `d`. Set `a=d/(1-w²)` in the field. When `a³+7` has a square root `b`, the finite points `(a,b)` and `(aw,b)` have horizontal slope and sum `(aw²,-b)`. Check each point against the curve, the nonzero denominator, and the precise stage-entry encoding. Compare a sparse boundary value such as `d=1` against dense denominators under the same stage contract. Record whether the upstream circuit actually reached that entry or only the component contract was exercised.
3. Group eligible rows by (use, frame, complete allowed projection). Within any bucket, two opposite required values disprove **every deterministic Boolean function of that basis**. Save both input IDs and projection, baseline results and first divergence. In one physical multiply two examples agreed on all 253 unchanged wires and needed opposite values of the proposed host.
4. Stop fitting larger predicates on the same basis once a collision exists. To reopen, split the loan at an actual use or write, admit a new observable, move a passenger, or build a reversible dirty-safe gadget. For a shorter loan check entry, every enabled use and restoration at exit. Check phase as well as basis data. A collision-free sample still needs a proof or independent validation under the intended contract.

A compact CSV checker is included in [scripts/find_collision.py](scripts/find_collision.py). The header is `use,frame,shot,enabled,baseline_ok,basis,required`. Use a fixed named bit order per use and frame, and prefix shot IDs with their panel. Run `python scripts/find_collision.py trace.csv`. It prints the witness and exits 1 on a contradiction, 0 after a collision-free eligible sample, and 2 on invalid input.

For the distinction between dirty and conditionally clean workspace, see [Khattar and Gidney](https://arxiv.org/abs/2407.17966).
