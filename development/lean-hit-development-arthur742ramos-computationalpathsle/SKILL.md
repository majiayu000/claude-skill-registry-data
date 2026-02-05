---
name: lean-hit-development
description: Guides adding new Higher Inductive Types to the ComputationalPaths library. Use when creating new HITs, defining fundamental group (pi1) calculations, implementing encode-decode proofs, or adding new topological spaces.
---

# Higher Inductive Type Development

This skill guides the implementation of new Higher Inductive Types (HITs) in the ComputationalPaths Lean 4 library, following established patterns for axiom declarations, recursion principles, and fundamental group calculations.

## File Location

New HITs go in `ComputationalPaths/Path/HIT/YourHIT.lean`

## Required Module Structure

```lean
/-
# [HIT Name] Higher Inductive Type

Brief mathematical description of the space.

## Key Results

- `yourHITBase`: The base point constructor
- `yourHITLoop`: The path constructor(s)
- `piOneEquiv*`: π₁(YourHIT) ≃ [Group]

## Mathematical Background

[Explain the topology/homotopy theory]

## References

- [Cite relevant papers]
-/

import ComputationalPaths.Path.Homotopy.FundamentalGroup
import ComputationalPaths.Path.Rewrite.SimpleEquiv
-- other imports as needed

namespace ComputationalPaths
namespace Path.HIT

/-! ## Type and Constructor Axioms -/

axiom YourHIT : Type u
axiom yourHITBase : YourHIT
axiom yourHITLoop : Path yourHITBase yourHITBase  -- or other path constructors

/-! ## Recursion Principle -/

axiom YourHIT.rec {β : Type v} (base : β) (loop : Path base base) : YourHIT → β
axiom YourHIT.rec_base : YourHIT.rec base loop yourHITBase = base

/-! ## Path Recursion (for encode) -/

axiom YourHIT.recPath {a : YourHIT} (P : YourHIT → Type)
  (pbase : P yourHITBase)
  (ploop : Path (transport P yourHITLoop pbase) pbase)
  : (x : YourHIT) → P x

/-! ## Presentation Type -/

-- Define the group presentation
inductive YourGroupWord
  | e : YourGroupWord           -- identity
  | gen : YourGroupWord         -- generator(s)
  | inv : YourGroupWord → YourGroupWord
  | mul : YourGroupWord → YourGroupWord → YourGroupWord

inductive YourGroupRel : YourGroupWord → YourGroupWord → Prop
  | inv_left : YourGroupRel (mul (inv w) w) e
  | inv_right : YourGroupRel (mul w (inv w)) e
  -- group-specific relations

def YourGroupPresentation := Quot YourGroupRel

/-! ## Encode-Decode -/

-- Decode: presentation → π₁
noncomputable def decode : YourGroupPresentation → π₁(YourHIT, yourHITBase) :=
  Quot.lift
    (fun w => wordToLoop w)
    (fun _ _ h => Quot.sound (decode_respects_rel h))

-- Encode: π₁ → presentation (often needs axioms)
axiom encodePath : Path yourHITBase yourHITBase → YourGroupWord
axiom encodePath_respects_rweq : RwEq p q → YourGroupRel (encodePath p) (encodePath q)

noncomputable def encode : π₁(YourHIT, yourHITBase) → YourGroupPresentation :=
  Quot.lift
    (fun p => Quot.mk _ (encodePath p))
    (fun _ _ h => Quot.sound (encodePath_respects_rweq h))

/-! ## Round-Trip Proofs -/

theorem decode_encode (α : π₁(YourHIT, yourHITBase)) : decode (encode α) = α := by
  induction α using Quot.ind with
  | _ p => exact Quot.sound (decode_encode_path p)

theorem encode_decode (x : YourGroupPresentation) : encode (decode x) = x := by
  induction x using Quot.ind with
  | _ w => exact Quot.sound (encode_decode_word w)

/-! ## Main Equivalence -/

noncomputable def piOneEquivYourGroup : SimpleEquiv (π₁(YourHIT, yourHITBase)) YourGroupPresentation where
  toFun := encode
  invFun := decode
  left_inv := decode_encode
  right_inv := encode_decode

/-! ## Summary -/

/-
This module establishes:
1. YourHIT as an axiomatized higher inductive type
2. π₁(YourHIT, yourHITBase) ≃ YourGroupPresentation
-/

end Path.HIT
end ComputationalPaths
```

## Checklist for New HITs

1. **Define axioms** for type and constructors
2. **Define recursion principle** (non-dependent and dependent)
3. **Define computation rules** (β-rules as axioms)
4. **Create group presentation type** (words + relations)
5. **Implement decode** (presentation → π₁)
6. **Implement encode** (π₁ → presentation, may need axioms)
7. **Prove decode_respects_rel** using RwEq lemmas
8. **Prove round-trip properties** (decode_encode, encode_decode)
9. **Package as SimpleEquiv**
10. **Add to imports** in `ComputationalPaths/Path.lean`
11. **Update README** with new result

## Common HIT Patterns

### Circle (S¹)
- One base point, one loop
- π₁(S¹) ≃ ℤ

### Torus (T²)
- One base point, two loops (a, b) with `aba⁻¹b⁻¹ = refl`
- π₁(T²) ≃ ℤ × ℤ

### Sphere (S²)
- One base point, one 2-cell (surface) filling a constant loop
- π₁(S²) ≃ 1 (trivial)

### Wedge Sum (A ∨ B)
- Glue base points together
- π₁(A ∨ B) ≃ π₁(A) * π₁(B) (free product)

### Orientable Surface (Σ_g)
- Genus g with 2g generators and surface relation
- π₁(Σ_g) ≃ ⟨a₁,b₁,...,a_g,b_g | [a₁,b₁]⋯[a_g,b_g] = 1⟩

## Key Imports

```lean
import ComputationalPaths.Path.Basic.Core           -- Path, refl, symm, trans
import ComputationalPaths.Path.Basic.Congruence     -- congrArg, transport
import ComputationalPaths.Path.Rewrite.RwEq         -- RwEq and lemmas
import ComputationalPaths.Path.Rewrite.SimpleEquiv  -- SimpleEquiv structure
import ComputationalPaths.Path.Homotopy.FundamentalGroup  -- π₁ notation
import ComputationalPaths.Path.Homotopy.Loops       -- LoopSpace
```

## Axiom Minimization

Only use axioms for:
- The HIT type itself
- Point constructors
- Path constructors
- Higher path constructors (2-cells, etc.)
- Recursion/elimination principles
- Computation rules (β-rules)
- Encode function (when not definable)

Everything else should be **proved** from these axioms.
