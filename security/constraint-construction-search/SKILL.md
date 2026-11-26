---
name: constraint-construction-search
description: "Encode and verify finite construction or optimization searches with CryptoMiniSat, Z3, OR-Tools CP-SAT or Gurobi, including witness extraction, model audits, and calibrated UNSAT or optimality claims."
---

# Zwangsjagge (constraint-construction-search)

Translate a finite mathematical construction problem into constraints, solve it, and verify the result outside the solver. The encoding is a proof obligation, not clerical glue.

## Choose the formulation

Read [references/solver-routing.md](references/solver-routing.md) when choosing between Boolean, SMT, CP-SAT, and MIP formulations.

- Use CryptoMiniSat for Boolean structure with substantial XOR or parity constraints.
- Use Z3 for bit-vectors, bounded integers, arrays, symbolic relations, or mixed logical structure.
- Use OR-Tools CP-SAT for bounded-integer combinatorial models with global or scheduling-style constraints.
- Use Gurobi for linear or mixed-integer formulations when a licensed installation is available and numerical tolerances are controlled.

## Encoding contract

1. Define variables, domains, symmetry breaking, constraints, objective, and the mathematical map between models and objects.
2. Bound every integer and bit-vector operation. State overflow, wraparound, and signedness semantics.
3. Test the encoding on hand-built satisfiable and unsatisfiable fixtures, including boundary cases.
4. Emit a witness in a solver-neutral format and verify the original mathematical predicate with separate code.
5. Freeze model text or generated-model hash, solver version, parameters, seed, time limit, termination status, and logs.
6. Treat feasibility, infeasibility, bounded objective, and proved optimum as different outcomes.
7. Apply the certification rules in [references/certification.md](references/certification.md) before reporting UNSAT or optimality.

## Stop conditions

- Stop if the independent verifier reconstructs the solver's encoding instead of checking the original object.
- Stop if a real-valued tolerance, big-M constant, overflow, or implicit coercion can change feasibility.
- Stop if symmetry breaking has no proof that every equivalence class retains a representative.
- Stop before using licensed software, remote services, or paid compute without the required authority.
