---
name: formal-foundations
description: |
  Mathematical foundations, logical structures, and formal verification guidance.
  Trigger when:
  - Designing protocol contracts, formal specifications, verifying state spaces, or using proof assistants.
  - Tasks involve: TLA+, Alloy, Lean, Coq, model checkers, invariants, temporal logic.
  - Prompt contains keywords: formal verification, alloy, tla+, lean, coq, invariant, state machine, model checker, liveness, safety.
---

# Formal Mathematical Foundations

**Reference corpus — `/form`, `/spec`, `boundary`.** This skill survives as the mathematical-language authority; the mandate to apply it is ambient, rooted in the workflows that invoke it as a lens. It supplies the foundational vocabulary for [form](../form/SKILL.md)'s structural representations, the verification semantics for [spec](../spec/SKILL.md)'s formal tiers, and the theoretical grounding consulted by [boundary](../boundary/SKILL.md). The formalisms here anchor the symbolic path of the [Verification Dual](../../rules.md#2-prime-invariants): types-as-propositions (Curry-Howard), bisimulation as behavioral equivalence, and adjoint functors as the semantic spine of data migration.

**Disposition directive:** Recognize that the structures you encounter in software engineering — types, protocols, state machines, data schemas — are instances of deeper mathematical patterns. This skill equips you with the vocabulary to see those patterns. The `sdma` skill provides the domain-specific toolkit for _applying_ these foundations to concrete problems; this skill provides the _language_.

---

## 1. Categorical Foundations

Category theory is the algebra of composition. Its value to engineering is not abstraction for abstraction's sake — it provides a _universal language_ for describing how things combine, transform, and relate.

### 1.1. Symmetric Monoidal Categories (SMC)

A symmetric monoidal category is a quintuple (C, ⊗, I, α, λ, ρ, γ) defining a category C equipped with a bifunctor ⊗: C × C → C and a unit object I.

- **Associator (α):** A natural isomorphism α\_{X,Y,Z}: (X ⊗ Y) ⊗ Z ≅ X ⊗ (Y ⊗ Z). _Grouping doesn't matter — only the components and their order._
- **Left and Right Unitors (λ, ρ):** Natural isomorphisms λ*X: I ⊗ X ≅ X and ρ_X: X ⊗ I ≅ X. \_The unit is invisible — combining with "nothing" changes nothing.*
- **Braiding (γ):** A natural isomorphism γ\_{X,Y}: X ⊗ Y ≅ Y ⊗ X such that γ\_{Y,X} ∘ γ\_{X,Y} = id\_{X ⊗ Y}. _Order can be swapped — swapping twice returns to the original._

**Coherence Axioms:**

1. **Pentagon Identity:** For any objects W, X, Y, Z, the following diagram commutes:

   (id_W ⊗ α\_{X,Y,Z}) ∘ α\_{W, X⊗Y, Z} ∘ (α\_{W,X,Y} ⊗ id_Z) = α\_{W, X, Y⊗Z} ∘ α\_{W⊗X, Y, Z}

   _All possible re-bracketings of four objects yield the same result. There is exactly one way to re-associate._

2. **Hexagon Identity:** Connects the braiding γ to the associator α:

   α\_{Y,Z,X} ∘ γ\_{X, Y⊗Z} ∘ α\_{X,Y,Z} = (id_Y ⊗ γ\_{X,Z}) ∘ α\_{Y,X,Z} ∘ (γ\_{X,Y} ⊗ id_Z)

   _Braiding is compatible with association. Swapping "through" a group works the same as swapping then regrouping._

### 1.2. Closed Categories

A monoidal category is **closed** if the functor (− ⊗ Y) has a right adjoint, denoted as the internal hom [Y, −] or Y ⊸ −.

- **Currying Isomorphism:** The adjunction is defined by the natural isomorphism:

  Hom(X ⊗ Y, Z) ≅ Hom(X, Y ⊸ Z)

  _A function of two arguments is equivalent to a function that takes one argument and returns a function of the other. This is the mathematical foundation of currying in every programming language._

### 1.3. Compact Closed Categories

A compact closed category is a symmetric monoidal category where every object X has a dual X\*, a unit η_X: I → X\* ⊗ X, and a counit ε_X: X ⊗ X\* → I satisfying the **Zig-Zag (Yanking) Identities:**

(ε_X ⊗ id_X) ∘ α\_{X, X\*, X} ∘ (id_X ⊗ η_X) = id_X

(id\_{X\*} ⊗ ε_X) ∘ α\_{X\*, X, X\*}⁻¹ ∘ (η_X ⊗ id\_{X\*}) = id\_{X\*}

_Every type has a "dual" (its continuation, its adjoint space, its negation). Creating a pair and then collapsing it is the same as doing nothing. This is the mathematical spine of evaluation, measurement, and resource consumption._

---

## 2. The Rosetta Stone Isomorphisms

The Rosetta Stone (Baez-Stay) maps the structural primitives of four disparate fields onto the common core of compact closed categories. **This is the central insight:** these four fields are not merely analogous — they are _formally isomorphic_. A proof about one transfers to the others via functorial mapping.

### 2.1. Physics (Hilbert Spaces)

- **Objects:** Finite-dimensional Hilbert spaces H.
- **Morphisms:** Linear operators f: H → K.
- **Bell States:** Formulated via the unit η: ℂ → H\* ⊗ H, representing the preparation of an entangled state.
- **Inner Product:** Formulated via the counit ε: H ⊗ H\* → ℂ, representing measurement or annihilation.

### 2.2. Topology (Cobordisms)

- **Objects:** (n−1)-dimensional manifolds representing spatial slices.
- **Morphisms:** n-dimensional cobordisms M: X → Y representing spacetime evolution.
- **String Diagrams:** A graphical syntax where "Cups" represent the unit η and "Caps" represent the counit ε.

### 2.3. Logic (Multiplicative Linear Logic — MILL)

- **Objects:** Propositions (resources) A, B.
- **Morphisms:** Proofs π: A ⊢ B.
- **Tensor (⊗):** Simultaneous conjunctive resource usage.
- **Linear Implication (⊸):** Resource transformation; distinct from the "Par" (⅋) used in classical linear logic.
- **Negation (A^⊥):** The linear dual, satisfying A ⊸ B ≅ A^⊥ ⅋ B.

### 2.4. Computation (Linear Type Theory)

- **Objects:** Types A, B.
- **Morphisms:** Programs or terms f: A → B.
- **β-reduction:** Computation as the elimination of a detour (application of a lambda abstraction).
- **η-expansion:** The principle of extensionality: (λx. f x) ≡ f.

---

## 3. Curry-Howard and Compositional Reasoning

The Curry-Howard correspondence — **types are propositions, programs are proofs** — is the computational column of the Rosetta Stone, but its implications extend beyond type theory:

- **Type checking is proof checking.** A well-typed program is a constructive proof that a proposition holds. A type error is a failed proof attempt.
- **Composition is inference.** If you have a proof of A → B and a proof of B → C, function composition gives you a proof of A → C. This is _modus ponens_ expressed as pipeline composition.
- **Parametric polymorphism is universal quantification.** A function `∀a. a → a` must be the identity — there is _no other_ inhabitant of that type. The type constrains the implementation absolutely.
- **Linearity is resource discipline.** In linear type theory, every value must be used exactly once. This isn't just a programming restriction — it's the logical principle that resources cannot be duplicated or discarded. This is the foundation of session types, ownership systems (Rust's borrow checker), and protocol verification.

---

## 4. Algebra vs. Coalgebra

This is the fundamental duality in formal modeling. Recognizing which side of this duality a problem lives on determines the correct tools.

| Aspect      | Algebra                          | Coalgebra                                               |
| :---------- | :------------------------------- | :------------------------------------------------------ |
| Defined by  | Constructors (how to build)      | Observers (how to interact)                             |
| Identity    | Structural (isomorphism)         | Behavioral (bisimulation)                               |
| Reasoning   | Induction (from parts to whole)  | Co-induction (from observations)                        |
| Data model  | Finite, inductive (lists, trees) | Potentially infinite, co-inductive (streams, processes) |
| Typical use | Data structures, ADTs            | State machines, protocols, reactive systems             |

### Coalgebra (formal definition)

A coalgebra is a morphism c: X → F(X) where X is the state space and F is a behavior endofunctor.

### Bisimulation

A relation R ⊆ X × X is a **bisimulation** if for all (x₁, x₂) ∈ R, their transitions c(x₁) and c(x₂) map to equivalent behaviors in F(R). Bisimulation is the formal tool for checking behavioral equivalence in dynamical systems — two systems are "the same" if no external observer can distinguish them, regardless of internal structure.

_When you ask "are these two state machines equivalent?" you are asking about bisimulation, not structural equality. This is the correct frame for protocol equivalence, API compatibility, and behavioral testing._

---

## 5. Foundational Vocabulary: Data and Structure

These definitions provide the _formal vocabulary_ for the structures that the `sdma` skill applies in practice.

### Database Schemas as Categories

- **Database Schema:** A small category S.
- **Database Instance:** A functor I: S → **Set**.
- **Data Migration Adjoints:** For a functor F: C → D between schemas, the migration of data is governed by the triple (Σ_F ⊣ Δ_F ⊣ Π_F):
  1. **Pullback (Δ_F):** Pre-composition I ∘ F. _Restructure existing data into a new schema._
  2. **Left Pushforward (Σ_F):** The Left Kan Extension, used for data integration and colimits. _Merge data from multiple sources._
  3. **Right Pushforward (Π_F):** The Right Kan Extension, used for defining data constraints and limits. _Enforce invariants across schema boundaries._

### Ologs (Ontology Logs) — Structural Constraints

1. **Objects (Types):** Must be labeled with a singular indefinite noun phrase (e.g., "An employee", "A department").
2. **Morphisms (Aspects):** Must represent functional relationships (mathematical functions), where each element of the domain maps to exactly one element of the codomain.
3. **Facts:** Represented as commutative diagrams demonstrating path equivalence.

### Signal Flow and Control

Signal flow is analyzed via Linear Relations using four categorical generators:

1. **Addition (+):** ℝ × ℝ → ℝ.
2. **Duplication (Δ):** ℝ → ℝ × ℝ.
3. **Integration (∫):** The storage or delay operator.
4. **Scalar Multiplication:** Gain factor k ∈ ℝ.

### Information Metrics

- **Shannon Entropy (H):** H(X) = −Σᵢ pᵢ log₂ pᵢ. In the SDMA, pᵢ is defined as the probability distribution of node interactions (degree/strength) per network science.
- **Structural Entropy Index of a Community (SEIC):** SEIC(C) = H_C / log₂ |C|, where H_C is calculated using the distribution pᵥ = deg(v) / Σ\_{u∈C} deg(u), measuring the internal decentralization of a community C.
- **Algorithmic Thermodynamics:** Relates the information state to physical entropy S: dE = TdS − PdV. Entropy S acts as a measure of "surprise," where higher disorder corresponds to increased metric entropy and lower Kaplan-Yorke attractor dimensions.

---

## 6. Summary Reference Table

The Rosetta Stone in full — the correspondences that unify four fields under one algebraic structure:

| Feature            | Physics                     | Topology                | Logic               | Computation              |
| :----------------- | :-------------------------- | :---------------------- | :------------------ | :----------------------- |
| **Objects**        | Hilbert Space (H)           | (n−1)-dim Manifold      | Proposition (A)     | Type (A)                 |
| **Morphisms**      | Linear Operator (f)         | n-dim Cobordism         | Proof (π)           | Program (P)              |
| **Tensor Product** | Composite System (H ⊗ K)    | Disjoint Union (X ⊔ Y)  | Conjunction (A ⊗ B) | Pair Type (A × B)        |
| **Duals**          | Adjoint (H\*)               | Reversed Manifold (X\*) | Negation (A^⊥)      | Continuation (A → ⊥)     |
| **Internal Hom**   | Linear Maps (H ⊸ K)         | (N/A)                   | Implication (A ⊸ B) | Function Type (A → B)    |
| **Unit (η)**       | Bell State / Preparation    | Cup (Creation)          | Identity (Axiom)    | Variable / Unit Value    |
| **Counit (ε)**     | Inner Product / Measurement | Cap (Annihilation)      | Cut (Elimination)   | Application / Evaluation |

---

## 7. Integration

### Relationship to `engineering.md`

The `engineering` skill mandates strong typing, composition, and structural soundness. This skill provides the _mathematical justification_ for why those mandates work: types are propositions (Curry-Howard), composition is inference (categorical composition), and structural soundness is a consequence of coherence (pentagon and hexagon identities). When engineering intuition says "this feels wrong," these foundations often reveal _why_ — a violated commutativity condition, a broken adjunction, a misidentified duality.

### Relationship to Cognitive Disposition (`ambient.md`)

The holonic lens in [ambient.md's Cognitive Disposition](../../ambient.md#cognitive-disposition) — every component is both a whole and a part — is a natural language description of what category theory formalizes: objects that are simultaneously domains and codomains, algebras that are simultaneously initial and terminal, structures that compose fractally. The formal foundations give that ambient intuition _teeth_: instead of "think holistically," you can verify that the diagram commutes.

### Relationship to SDMA

This skill tells you _what these structures are_. The `sdma` skill tells you _how to wield them_. If you need applied methodology — building an olog, verifying protocol equivalence via bisimulation, selecting between formalisms — load `sdma` alongside this skill.