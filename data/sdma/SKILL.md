---
name: sdma
description: |
  Structured Domain Modeling Architecture (SDMA) principles.
  Trigger when:
  - Designing domain models, building ologs (ontological graphs), verifying protocol equivalence, selecting schemas, or measuring architectural entropy.
  - Modeling structures using Category Theory, Coalgebra, or Information Theory.
  - Prompt contains keywords: sdma, olog, Category Theory, Coalgebra, Information Theory, entropy, schema, pullback, functor, monad.
---

# Structural Domain Modeling Atlas (SDMA)

**Reference corpus — `/form`, `/spec`, `boundary`, `engineering`.** This skill survives as the applied-methodology authority for formal domain modeling; the mandate to apply it is ambient, rooted in the workflows that invoke it as a lens. It is the [form](../form/SKILL.md) workflow's mathematical toolkit, the formalism-selection authority for [spec](../spec/SKILL.md)'s verification tier choices, and the structural vocabulary consulted by [boundary](../boundary/SKILL.md) and [engineering](../engineering/SKILL.md). Where applicable, the formalisms in this atlas close conditions on the symbolic path of the [Verification Dual](../../rules.md#2-prime-invariants) (coalgebraic bisimulation, session-type checking, linear-type discipline) or supply the structural representation that the adversarial path reviews for coherence.

This skill provides the _applied methodology_ for formal domain modeling. The mathematical foundations — SMC, Rosetta Stone, Curry-Howard, algebra/coalgebra duality — live in the `formal-foundations` skill ([skills/formal-foundations/SKILL.md](../formal-foundations/SKILL.md)). This skill tells you _how to wield them_.

The SDMA covers what are arguably the most critical isomorphisms in computer science — the categorical, coalgebraic, linear, and information-theoretic bedrock. But it is a _foundation_, not a ceiling. The full landscape of mathematical formalism is available. The SDMA provides the root from which to reach for _any_ relevant representation, guided by the **principle of minimal representation**: choose the simplest formalism that faithfully captures the domain's essential structure.

---

## Part I — The Atlas

### 1. Functorial Data Migration in Practice

The formal definitions of schemas-as-categories and adjoint migration functors live in the `formal-foundations` skill. Here we focus on _how to apply them_.

#### Schema Design as Category Design

Treat every database schema as a small category S. This isn't metaphorical — it's a precise correspondence:

- **Tables** are objects in S
- **Foreign keys** are morphisms between objects
- **Path equations** (e.g., "an employee's department's manager is the employee's supervisor") are commutativity constraints

The _signature_ S = (N, E, C) is the finite presentation: nodes (tables), edges (foreign keys), path equations (business rules). The _schema_ S is the category the signature generates.

#### Typed Signatures

Abstract categorical IDs are insufficient for real data. Bridge the gap with the Typed Signature (A, i, γ):

- **A** — a discrete category of attribute names (the "leaf" fields: strings, integers, dates)
- **i: A → S** — maps each attribute to the node (table) it belongs to
- **γ: A → Set** — maps each attribute to its concrete type

A database instance is then a functor I: S → **Set** in _categorical normal form_: structural parts (foreign keys, relationships) are compared for isomorphism; attribute parts (data values) are compared for equality.

#### The Three Migration Functors

When you have a functor F: C → D between schemas (a schema mapping), three adjoint functors handle data migration:

| Functor                 | Operation             | Engineering Use                             | Think Of It As   |
| :---------------------- | :-------------------- | :------------------------------------------ | :--------------- |
| Δ_F (Pullback)          | Pre-composition I ∘ F | Data access, reformatting, view creation    | SELECT + reshape |
| Σ_F (Left Pushforward)  | Left Kan Extension    | Data integration, dataset merging, colimits | UNION + project  |
| Π_F (Right Pushforward) | Right Kan Extension   | Constraint enforcement, joins, limits       | JOIN + filter    |

**When to use each:**

- **Δ_F** is your default tool. It restructures existing data into a new schema. Use it for migrations, views, and reformatting.
- **Σ_F** when merging datasets from multiple sources. It operates through discrete op-fibrations to maintain structural consistency.
- **Π_F** when enforcing constraints across schema boundaries. Technically demanding — it uses the comma category B_d := (d ↓ F) and limit tables (Cartesian product of node tables, filtered by edge equations).

#### Avoiding Semantic Loss

Traditional ETL processes suffer from _semantic loss_ — the meaning of relationships is destroyed during transformation. FDM prevents this because the migration functors are adjoint: they preserve the categorical structure by construction. If your migration doesn't factor through Δ/Σ/Π, you're likely losing semantic information.

---

### 2. Olog Construction

Ologs (Ontology Logs) are the SDMA's tool for rigorous knowledge representation. They make implicit domain knowledge explicit and verifiable.

#### Construction Rules

These rules are _not suggestions_ — violating them produces invalid ologs:

1. **Objects (Types):** Must be labeled with a _singular indefinite noun phrase_.
   - ✅ "An employee", "A department", "A purchase order"
   - ❌ "Employees", "The department", "Purchase orders"

2. **Morphisms (Aspects):** Must represent _functional_ relationships — each element of the domain maps to exactly one element of the codomain.
   - ✅ "An employee" →[works in]→ "A department" (each employee works in exactly one department)
   - ❌ "A department" →[has]→ "An employee" (a department has _many_ employees — not functional)

3. **Facts:** Represented as _commutative diagrams_ demonstrating path equivalence.
   - If "An employee" →[works in]→ "A department" →[is managed by]→ "A manager" equals "An employee" →[reports to]→ "A manager", that's a fact — the diagram commutes.

#### Why Ologs Matter

Ologs ensure that semantic models are "equivalent up to object identity." They eliminate the ambiguity of natural language by forcing relationships into categorical structure. When you build an olog, you're not just drawing boxes and arrows — you're constructing a formal category where every path equation is a verifiable business rule.

#### From Bags of Data to Knowledge Bases

The progression: unstructured data → relational schema → olog → functorial migration. Each step adds formal structure. An olog-backed data architecture can be migrated, merged, and verified using the adjoint functors from §1 — because the olog _is_ the category that the functors act on.

---

### 3. Coalgebraic Modeling

The `formal-foundations` skill defines coalgebra and bisimulation formally. Here we cover _when and how_ to apply them.

#### When to Reach for Coalgebra

Use coalgebra when your problem has these characteristics:

- **Hidden internal state** — you can observe outputs but not inspect internals
- **Potentially infinite behavior** — streams, protocols, reactive systems
- **Behavioral equivalence matters more than structural identity** — two implementations may differ internally but behave identically

If your problem is about _constructing_ finite data (lists, trees, ADTs), use algebra. If it's about _observing_ evolving state, use coalgebra.

#### Applying Bisimulation

Two systems are bisimilar if no external observer can distinguish them. This is the correct frame for:

- **Protocol equivalence:** Are two protocol implementations interchangeable? Check bisimulation, not structural equality.
- **API compatibility:** Does a refactored service behave identically to the original? Bisimilar behavior guarantees compatibility.
- **Behavioral testing:** Write tests that assert on _observable_ behavior, not internal state. This is the formal justification for black-box testing.

#### The Observer Pattern, Formalized

A coalgebra c: S → F(S) defines:

- **S** — the state space (hidden from observers)
- **F** — the interface functor (what observers see)
- For a stream: F(S) = A × S, where A is the observation and S is the next state

The _final coalgebra_ is the "most general" system — it contains all possible behaviors. Any concrete system maps into it via a unique morphism, which extracts the system's complete behavioral profile.

---

### 4. Linear Logic and Session Types

#### Resource Linearity in Practice

Linear logic's constraint — resources cannot be duplicated or discarded — maps directly to engineering concerns:

| Formal Principle                     | Engineering Application                               |
| :----------------------------------- | :---------------------------------------------------- |
| No duplication (A → A ⊗ A forbidden) | Unique tokens, ownership, single-use credentials      |
| No discarding (must consume)         | Memory management, resource cleanup, connection pools |
| Linear implication (A ⊸ B)           | State transitions that consume input                  |

**Where it prevents failures:**

1. **Memory leaks:** Every allocated resource must be consumed. Linear types guarantee this statically.
2. **Double-spending / race conditions:** Unique tokens cannot be copied to multiple processes. This is the No-Cloning principle applied to computation.
3. **Dangling references:** Ownership transfer is explicit — the source loses access when the target acquires it (Rust's borrow checker is a linear type system).

#### Session Types for Protocol Compliance

Session types represent communication protocols as types. They guarantee:

- **Deadlock-freedom:** If the types check, the protocol cannot deadlock.
- **Protocol compliance:** Each party's view of the channel is dual to the other's. Deviation is a type error.
- **Composability:** Session-typed channels compose — connecting two compliant endpoints produces a compliant system.

Use session types when modeling multi-party interactions where protocol correctness is critical — payment flows, consensus protocols, API handshakes.

---

### 5. Complexity Metrics and Architectural Entropy

#### Beyond Lines of Code

Traditional metrics (LoC, cyclomatic complexity) are _architecturally bankrupt_ — they measure syntax, not structure. The SDMA uses information-theoretic metrics that capture genuine structural properties.

#### SEIC: Measuring Architectural Decentralization

The Structural Entropy Index of a Community quantifies how decentralized and resilient an architecture is:

SEIC(C) = H_C / log₂ |C|

Where H_C is the Shannon entropy of the degree distribution within the community.

**Interpretation:**

- SEIC ≈ 1 → Highly decentralized, pluralistic. No single node dominates. Resilient to node failure.
- SEIC ≈ 0 → Highly centralized, hub-dominated. Fragile — the hub is a single point of failure.

**Practical use:**

1. Compute the SEIC for each module/service cluster in the architecture
2. Compare values across clusters to find fragile hotspots
3. Track SEIC over time — decreasing values signal growing centralization (architectural debt)

#### Scale-Invariance and Null-Model Analysis

SEIC enables comparison between microservices and monolithic cores — it's scale-invariant by construction.

Use _Maslov-Sneppen rewiring_ to distinguish between:

- **Structural entropy** — intentional design choices that produce centralization
- **Emergent entropy** — random noise from organic growth

If SEIC differs significantly from the null model, the centralization is deliberate (or at least systematic). If it matches the null model, the architecture has no more structure than random wiring.

#### Thermodynamic Cost

In HPC and exascale contexts, excessive software entropy is a _literal thermodynamic cost_. High entropy correlates with increased data movement, which degrades energy efficiency and maintainability. Managing this entropy is a strategic requirement for sustainable system evolution.

---

### 6. The Decision Matrix

This is the meta-model — the prescriptive logic for selecting the correct formalism. Selecting the wrong formalism is the primary driver of architectural debt. The matrix below covers the SDMA's foundational formalisms, but it is a _starting point_, not a closed set.

| If Problem Domain Involves...              | Select Representation | Formal Tool                |
| :----------------------------------------- | :-------------------- | :------------------------- |
| Evolving state with hidden variables       | Coalgebra             | Bisimilarity               |
| Non-duplicable resources / security tokens | Linear Logic          | Linear Type Systems        |
| Cross-database migration / schema merging  | Category Theory       | Adjoint Functors (Δ, Σ, Π) |
| Protocol-heavy multi-party concurrency     | Session Types         | Process Calculi            |
| Resilience of communicative influence      | Information Theory    | SEIC / Null-Model Analysis |

**Using the matrix:** Start here. Identify the dominant characteristic of your problem domain, select the representation, then apply the corresponding tools from this skill. If the domain maps cleanly to a row above, use that formalism. If it doesn't — or if a simpler or more domain-native formalism exists outside this matrix — use _that_ instead. The SDMA provides the mathematical bedrock; the principle of **minimal representation** governs the final selection: the simplest formalism that faithfully captures the domain's structure wins.

If the domain combines multiple characteristics (e.g., a protocol with hidden state AND resource constraints), layer the formalisms — session types for the protocol structure, linear logic for resource discipline, coalgebra for the state machine underneath.

---

### 7. Implementation Strategy: "Running Between the Boxes"

The architect's role is _translational research_ — linking pure mathematical truth to industrial engineering. This is a three-step pipeline:

#### Step 1: Translation

Map the engineering problem into the correct formal representation:

- Data integration problem → categorical signatures (schemas as categories)
- Protocol verification → coalgebraic observers (state machines as coalgebras)
- Resource management → linear types (resource-aware type systems)
- Architectural health → information metrics (SEIC, entropy analysis)

Use the Decision Matrix (§6) to guide the mapping.

#### Step 2: Formalization

Apply the selected tools to ensure structural and behavioral integrity:

- For data: adjoint data migration (Δ/Σ/Π) to verify semantic preservation
- For protocols: bisimulation checks to verify behavioral equivalence
- For resources: linear type checking to verify consumption discipline
- For architecture: SEIC computation to quantify resilience

#### Step 3: Validation

Deploy metrics to measure resilience against real-world failures:

- SEIC and null-model analysis to measure architectural entropy
- Bisimulation checking to verify refactoring correctness
- Session type inference to verify protocol compliance
- Thermodynamic entropy estimation for HPC/exascale systems

The pipeline is iterative — validation results feed back into translation when the model doesn't match reality.

---

## Part II — Advanced Extensions

These extensions close four gaps in the base Atlas, extending the SDMA from pure digital/discrete modeling into continuous, constrained, uncertain, and verifiable domains.

---

### 8. The Control Gap: Signal Flow and Linear Relations

The base Atlas models computation as _functional_ — unidirectional input-to-output maps. Physical and cyber-physical systems have _bidirectional constraints_: feedback loops, conservation laws, simultaneous equations. This extension closes that gap.

#### From Functions to Relations

The shift is from the category **Set** (functions) to the category **REL** (relations):

- A relation R: I ⊣↦ J is a "multi-function" I → PJ (where P is the powerset monad)
- **REL** is the Kleisli category of the powerset monad on **Set**
- In **REL**, the terminal object is ∅ and the Cartesian product is the disjoint union I + J

This deviation from discrete software logic allows modeling of physical interfaces as _subspaces of interaction_ rather than sequential execution steps. Relations naturally handle non-deterministic or partial outputs — a physical sensor may produce a range of values, not a single one.

#### Frobenius Algebras and Unbiased Connectivity

The mathematical basis for unbiased connectivity in signal flow diagrams is the _Frobenius property_:

Σ_m(m\*(n) ∧ k) ≅ n ∧ Σ_m(k)

In engineering terms, this governs the "splitting" and "merging" of signal paths. Treating signal flow as a Frobenius algebra ensures that:

- The diagonal (contraction) and its adjoints preserve logical consistency across junctions
- Reindexing a signal via u\* does not violate underlying physical conservation laws
- "Eq-mate" relationships between substituted constraints are maintained

#### Contrast: LinRel vs. Discrete Categories

| Feature        | Discrete Software Systems (Standard Categories) | Continuous Physical Systems (VectRel / LinRel) |
| :------------- | :---------------------------------------------- | :--------------------------------------------- |
| Composition    | Functional (g ∘ f)                              | Relational (R ⊆ I × J)                         |
| State Space    | Sets / Discrete Types                           | Vector Spaces over Field K                     |
| Fibration Type | Subobject Fibration Sub(B)                      | Vector Space Fibration **Vect** → **Fld**      |
| Identity/Proj  | Cartesian Products I × J                        | Disjoint Union I + J (Terminal ∅)              |
| Connectivity   | Sequential / Directed                           | Frobenius (Unbiased / Bidirectional)           |

#### When to Use

Use LinRel when modeling systems with:

- Feedback loops (control systems, PID controllers)
- Bidirectional physical constraints (electrical circuits, mechanical linkages)
- Simultaneous equations rather than sequential computation
- Physical conservation laws that must be preserved across junctions

---

### 9. The Constraint Gap: Fibrations, Hyperdoctrines, and Triposes

Ologs capture simple path equalities — "this path equals that path." Real-world systems require _quantified logic_: "for all employees in department X, there exists a manager who..." This extension layers first-order and higher-order logic over structural data.

#### The Fibration Framework

Logic is viewed as a fibration p: E → B:

- **Base category B** — "Types" or "Contexts" (the structural skeleton)
- **Fibres E_I** — the "Predicates" or "Logic" applicable to each context I in B
- **Reindexing functors u\*: E_J → E_I** — handle substitution, ensuring predicates remain consistent when moving between contexts

#### Quantifiers as Adjoints

First-order quantifiers are identified as adjoints to the weakening functors induced by projections w: I × J → I:

| Operation                    | Formal Identity         | Engineering Meaning                    |
| :--------------------------- | :---------------------- | :------------------------------------- |
| Substitution                 | Reindexing functor u\*  | Move a predicate into a new context    |
| Existential quantification ∃ | Left adjoint Σ_w ⊣ w\*  | "There exists" — search, existence     |
| Universal quantification ∀   | Right adjoint w\* ⊣ Π_w | "For all" — invariant, global property |
| Equality                     | Left adjoint Σ_δ ⊣ δ\*  | Diagonal contraction — identity check  |

#### The Olog → Hyperdoctrine → Tripos Hierarchy

This is a progression of expressive power:

1. **Ologs** (simple slice categories): Path equalities only (M//I over I). Basic data integrity without quantification. Use for: domain modeling, knowledge representation, simple business rules.

2. **Hyperdoctrines** (full slice categories): Enable first-order logic by providing Σ_w and Π_w across fibres. Complex, nested business rules. Use for: enterprise logic, regulatory compliance, constraint-heavy domains.

3. **Triposes**: Utilize the "realizability fibration" over the Effective Topos (Eff) to reason about the _provability_ of predicates. Higher-order reasoning. Use for: formal verification, provably correct systems, logic programming.

Select the appropriate level based on the complexity of constraints in your domain. Don't use a tripos when an olog suffices — the additional power comes with additional complexity.

---

### 10. The Uncertainty Gap: Probabilistic Categories and Many-Valued Logic

Structure alone is insufficient when the environment is noisy. This extension accommodates _graded belief_ and stochastic transitions.

#### Markov Kernels in Categorical REL

Extend standard relational models into uncertainty using j-separated families and sheaves:

- Standard relation in **REL**: multi-function I → PJ (definite outcomes)
- Uncertain relation in **PredREL**: "fuzzy" outcomes where truth values are not bits but objects of the power object Ω = PN
- The Effective Topos (Eff) provides the framework for "computable searches" under uncertainty

#### Markov's Principle

In the Effective Topos, Markov's Principle holds:

∀β: 2^N, ¬¬(∃n: N. β(n)) ⊃ ∃n: N. β(n)

In engineering terms: if the agent knows it is _impossible_ for a decidable predicate β to fail for all n, then it can _computably find a witness_. This justifies the use of search-based heuristics in uncertain environments — if you know a solution exists, you can find it.

#### Many-Valued Logic and Partial Equivalence Relations (PERs)

For incomplete belief states, use lattice-valued logic and Kleene equality (≃):

- In the category of PERs, partiality is modeled via the special PER N_⊥ = {(n, n') | n · 0 ≃ n' · 0}
- The quotient set N/N_⊥ = {[Kx.⊥]} ∪ {[Kx.n]} — natural numbers with an added "bottom" element for undefined states
- This allows maintaining consistent belief states even when information is incomplete or contradictory

**Practical applications:**

- Probabilistic programming (Bayesian inference, Monte Carlo methods)
- Agent reasoning under uncertainty (planning with incomplete information)
- Fuzzy constraint satisfaction (soft constraints, preference orderings)
- Fault-tolerant systems (graceful degradation, partial availability)

---

### 11. The Verification Gap: Coalgebraic Dynamics and Modal Duality

The base Atlas provides coalgebra for modeling behavior. This extension provides the _dual_ specification language — what properties a system _must_ satisfy — and the formal bridge between the two.

#### System Behavior (Coalgebra)

From the systems architecture perspective:

- State space and transitions are modeled as a coalgebra X → σ(X)
- The system is interpreted through its _observations_ — the "object-oriented" view
- The carrier Ω of the weakly terminal coalgebra represents the maximal possible behavior — the system's total "Ontology"
- This describes how a system behaves over time _without needing to know its internal construction_

#### System Specification (Modal Logic)

Dual to behavior is the _specification language_:

- Properties observed of a system (Epistemology) are captured in the classifying category Cl(Σ, H) of the specification
- High-level "Guarantees" are formulated as formulas within the fibres of the fibration
- A model M _validates_ a theory if it extends to a morphism of Eq-fibrations

#### Stone Duality Isomorphisms

The SDMA uses these isomorphisms to bridge behavior and specification:

| Behavioral Side                | ↔  | Specification Side                     |
| :----------------------------- | :-- | :------------------------------------- |
| System dynamics (coalgebra)    | ↔  | Modal operators in the dual logic      |
| System state                   | ↔  | Set of valid formulas in the fibre E_I |
| Terminal coalgebra (carrier Ω) | ↔  | Most refined specification possible    |

#### Engineering Applications

- **Change-of-Base operations:** Move between **Set** and **Eff** to translate engineering guarantees into verified behaviors
- **Specification-driven development:** Write the modal specification (what the system must satisfy), then verify that the coalgebraic model (how it behaves) satisfies it
- **Refinement checking:** A system refines its specification if the behavioral morphism factors through the specification's classifying category
- **Compositional verification:** Verify subsystems independently, then verify that composition preserves the global specification

This duality allows the agent to approach verification from _either direction_ — start with behavior and derive what properties hold, or start with desired properties and verify that the behavior satisfies them.

---

## Summary: The Complete SDMA Toolkit

| Atlas Section                   | What It Solves                        | Key Tool                        |
| :------------------------------ | :------------------------------------ | :------------------------------ |
| §1 Functorial Data Migration    | Semantic data integration             | Adjoint functors (Δ, Σ, Π)      |
| §2 Ologs                        | Knowledge representation              | Categorical ontology            |
| §3 Coalgebraic Modeling         | Behavioral equivalence                | Bisimulation                    |
| §4 Linear Logic / Session Types | Resource discipline, protocol safety  | Linear types, session types     |
| §5 SEIC / Entropy               | Architectural resilience              | Information-theoretic metrics   |
| §6 Decision Matrix              | Formalism selection                   | Prescriptive logic              |
| §7 Implementation Pipeline      | Theory-to-practice bridge             | Translation → Formal → Validate |
| §8 Control Gap                  | Continuous / bidirectional systems    | LinRel, Frobenius algebras      |
| §9 Constraint Gap               | Quantified business logic             | Hyperdoctrines, triposes        |
| §10 Uncertainty Gap             | Probabilistic / partial reasoning     | Markov kernels, PERs            |
| §11 Verification Gap            | Behavior-specification correspondence | Stone duality, modal logic      |