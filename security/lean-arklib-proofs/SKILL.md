---
name: lean-arklib-proofs
description: "Formalize and verify mathematical or cryptographic claims in Lean 4 with ArkLib: exact-target builds, axiom audits, dependency checks, and the build evidence an evaluator expects."
---

# Magerquark (lean-arklib-proofs)

*Lean and ArkLib proofs*

Convert an informal argument or computational finding into a theorem accepted by the target Lean 4 and ArkLib project. The exact repository target and its policy define acceptance.

## Proof workflow

1. Read the governing project instructions, pinned Lean and ArkLib revisions, target file, build command, and acceptance rules.
2. State the theorem with the intended quantifiers, domains, side conditions, definitions, and normalization. Compare it directly with the external claim.
3. Isolate computational evidence as a lemma hypothesis or re-prove it inside Lean. CAS, solver, or search output does not enter the trusted result merely because it guided the proof.
4. Implement the smallest maintainable proof using existing project lemmas before adding custom infrastructure.
5. Build the exact target in the authoritative worktree. Confirm that the build consumed the edited file rather than a shadow copy or stale artifact.
6. Apply every relevant gate in [references/acceptance-gates.md](references/acceptance-gates.md).
7. Preserve theorem name, repository commit, toolchain lock, ArkLib revision, commands, and outputs.

## Boundaries

- Do not claim completion while `sorry`, `admit`, an unapproved axiom, or a placeholder theorem remains in the trusted dependency path.
- Do not assume `native_decide`, code generation, or an external oracle is accepted; follow the target repository's trust policy.
- A successful editor check or unrelated package build does not replace the exact target build.
- A formal theorem can still formalize the wrong statement. Keep statement equivalence as a separate reviewed obligation.
