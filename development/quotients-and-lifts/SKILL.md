---
name: quotients-and-lifts
description: Work effectively with Lean 4 quotients in ComputationalPaths (Quot.lift/Quot.ind/Quot.sound), including nested lifts and common proof obligations.
---

# Quotients & Lifts (Lean 4)

This skill is a practical guide to working with `Quot`-based quotients in the ComputationalPaths codebase (e.g. `LoopQuot`, `PiOne`, group presentations, rewrite quotients).

## Core patterns

### 1) Defining a function out of a quotient: `Quot.lift`

To define a map `Quot r → B`, provide:
- a function on representatives `f : A → B`
- a proof it respects the relation `hf : ∀ a b, r a b → f a = f b`

```lean
def encode : Quot r → B :=
  Quot.lift f (by
    intro a b hab
    -- show f a = f b
    exact hf a b hab)
```

In this repo, the “respects” proof is often built from an `RwEq` lemma, e.g. `circleEncodePath_rweq` in `ComputationalPaths/Path/HIT/Circle.lean`.

### 2) Proving something for all quotient elements: `Quot.ind`

Use quotient induction to reduce to representatives:

```lean
theorem myThm (x : Quot r) : P x := by
  induction x using Quot.ind with
  | _ a =>
    -- goal becomes P (Quot.mk _ a) (up to definitional equality)
    ...
```

### 3) Proving equality in a quotient: `Quot.sound`

When the goal is an equality of quotient terms, typically:

```lean
-- goal: Quot.mk r a = Quot.mk r b
exact Quot.sound hab
```

`hab` must have the quotient’s underlying relation type (often `RwEq` in this project). If you have the relation in the “wrong direction”, use symmetry (e.g. `rweq_symm`).

## Nested quotient lifts (Lean 4)

Lean 4 does not provide some Lean 3 conveniences (e.g. patterns like `Quot.liftOn2` in older code). Prefer nested `Quot.lift`:

```lean
def f2 : Quot r1 → Quot r2 → C :=
  fun x => Quot.lift
    (fun a => Quot.lift (fun b => g a b) (by intro b b' hb; exact ...) )
    (by intro a a' ha; funext y; -- prove functions are equal
        induction y using Quot.ind with
        | _ b => ... )
    x
```

This pattern appears in HIT / SVK developments where you map pairs of quotient classes into another quotient.

## Practical checklist for “respects relation” proofs

When `Quot.lift` fails due to the second argument:
1. Identify the quotient relation `r` (often a rewrite equivalence).
2. Prove a lemma of the shape `r a b → f a = f b` (or `→ RwEq (f a) (f b)` then turn into equality via `Quot.sound` where appropriate).
3. If the lemma naturally produces the reverse direction, wrap with symmetry.
4. Use `simp` lemmas for quotient constructors (e.g. `LoopQuot.ofLoop`) when applicable.

## Common pitfalls (and fixes)

- **Wrong obligation shape**: `Quot.lift` wants equality in the codomain, not a relation proof. If your codomain is itself a quotient, you usually finish with `Quot.sound`.
- **Direction mismatch**: `Quot.sound` expects `r a b`; use symmetry of the relation when you have `r b a`.
- **Getting stuck on function equality** (nested lifts): use `funext` + `Quot.ind` on the remaining quotient argument(s).

