---
name: computer-algebra-oracles
description: "Route exact algebra, finite-field, coding-theory, polynomial-system, group-theory and number-theory questions through SageMath, Magma, OSCAR, Singular, GAP/GUAVA, PARI/GP or Hecke, with replayable evidence and an independent check."
---

# Rächeschieber (computer-algebra-oracles)

Use an exact computer-algebra system to expose structure, compute a witness, or falsify a claim. Produce a replayable mathematical receipt; do not silently promote oracle output into a proof.

## Route by structure

Read [references/routing.md](references/routing.md) when more than one system is plausible or a specialist feature is required.

- Start with SageMath for broad interactive exploration and cross-domain glue.
- Prefer OSCAR for integrated exact algebra and geometry, and Singular for ideals, Groebner bases, elimination, and polynomial systems.
- Prefer GAP/GUAVA for finite groups, automorphisms, equivalence, and coding-theory constructions.
- Prefer PARI/GP or Hecke for algebraic-number-theory computations.
- Use Magma when a named Magma algorithm, database, or independent implementation supplies a concrete advantage and a licensed route is available.

Do not infer mathematical independence merely because two front ends have different names. Record shared backends such as FLINT, Singular, GAP, or PARI.

## Execution contract

1. State the ring, field, characteristic, coefficient domain, variable order, quotient, and normalization conventions before computing.
2. Probe capability with a small representative calculation. Binary presence or a successful import is not a workload check.
3. Use exact literals and exact types. Any floating-point approximation must be explicitly bounded and cannot certify an exact claim by itself.
4. Save minimal executable input, tool and package versions, seed when used, and output sufficient to replay the claim.
5. Check load-bearing results through a semantically equivalent route with a genuinely distinct implementation or translate them into the target proof system.
6. Report the narrowest status supported: explored, witnessed, falsified on the declared domain, independently reproduced, or formally proved.

Read [references/receipts.md](references/receipts.md) before handing a result to another lane or treating a computation as exhaustive.

## Stop conditions

- Stop and repair the model if the mathematical object in the program is not demonstrably equivalent to the stated object.
- Stop calling a route independent when its decisive computation shares the same backend or generated artifact.
- Stop before using an online calculator, licensed installation, paid service, or external upload unless that action is authorized.
