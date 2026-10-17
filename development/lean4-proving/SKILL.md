---
name: lean4-proving
description: Formal verification with Lean 4 — propositions as types, structured proofs, statements you can trust.
version: 1
triggers: lean 4, lean4, formal proof, theorem proving, propositions as types
category: Engineering & code
blurb: Formal verification with Lean 4 — propositions as types and structured proofs you can trust.
archetype: knowledge
example: Help me state and prove this property in Lean 4.
---

# Lean 4 Proving

For the invariants that must never break — protocols, consensus, critical algorithms — prove it or don't claim it. Lean 4 turns specs into checked theorems.

## When to use
- Critical invariants where a bug is unacceptable (protocol/consensus logic, state machines, safety properties).
- Formalizing a design before or alongside implementation.
- Reviewing proofs and verification claims.

## Method
1. **Project setup**: `elan` toolchain, `lake` build, Mathlib as needed; pin versions; CI runs `lake build` so proofs stay green.
2. **Types as propositions**: state the theorem first — `theorem name (args) : Prop` — and make sure the statement says what you mean before proving it.
3. **Definitions first**: total, executable definitions of the system model; specs separate from implementation.
4. **Proof craft**: structured proofs; `simp`, `rw`, `induction`, `cases`, `omega` where appropriate; keep proofs readable — they are code and docs.
5. **No cheating**: `sorry`, new axioms, and `native_decide` shortcuts are tracked (tickets), never smuggled into deliverables; a landmark proof ships with zero `sorry`.
6. **Statement review**: statements reviewed *independently* of tactics (a proof of the wrong theorem is worthless).
7. **Model ↔ code alignment**: keep the verified model and the implementation in sync — document the mapping; port changes go back through the model.

## Quality gates
- [ ] `lake build` green in CI (proofs compile).
- [ ] Zero `sorry`/axioms in delivered theorems (or explicitly tracked with sign-off).
- [ ] Statements reviewed by a second pair of eyes.
- [ ] Model-to-implementation mapping documented.

## Red lines
- Never weaken a statement silently to make it provable.
- No unproven claims dressed as "formally verified".

## Related
`architecture-decisions` · `rust-engineering` (verified models → code) · `secure-build-pattern`.
