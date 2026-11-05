---
name: mathematical-framework-design
description: >-
  Construct a new mathematical setting or a substantial two-way correspondence
  when existing objects, morphisms, or foundations obstruct useful constructions.
  Use for diagnosing structural failures, designing completions or enriched
  objects, and developing duality dictionaries with explicit comparison theorems.
  Distinct from routine method import or general exploration of a conjecture.
---

# Mathematical Framework Design

Make the setting itself a research object. Determine what objects, morphisms,
notions of equivalence, and constructions would support the mathematics being
sought. A replacement setting or a bridge between two theories can be a major
contribution independently of the problem that motivated it.

In a campaign, `honest-conjecture-resolution` selects the objective and integrates
the results; this skill owns framework construction and comparison. Return the
mathematical output and transfer status to the existing campaign state.

Use `grothendieck-rising-sea` for sustained development of the resulting theory.
Use `alon-method` when an existing theorem and a one-way encoding suffice. This
skill addresses construction of the setting or correspondence itself, including
the substantial mathematics needed to make it work.

## Identify The Structural Question

Inspect concrete examples, source proofs, and relevant existing theories in the
campaign, sibling repositories, and shared literature. Describe the construction
that is unavailable, fails, or repeatedly demands extra data. Distinguish:

- a mathematical obstruction in the chosen objects or morphisms;
- a representation that forgets essential information;
- inconvenient notation or a missing implementation;
- a promising correspondence whose mathematical content is still unknown.

Failure of a desirable categorical property is relative to a purpose, not proof
that an entire subject has defective foundations. A category need not be abelian
or Cartesian closed to support the intended mathematics. State why the missing
property would help and what would remain difficult even if it were available.

## Build A Setting Or A Bridge

Choose the direction suggested by the examples; these may develop together.

**Repair or enlargement.** Explore extra structure, a changed morphism class,
quotients, completions, localization, test objects, or an internal language.
Define the construction and its intended universal or comparison property.
Build concrete models. Determine what original information is retained, what is
identified or added, and what new operations become available. Simple changes
may suffice; a sheaf category or new foundation is an option, not a destination.

**Two-way correspondence.** Use matching examples and invariants as clues, then
construct maps on objects and morphisms with the correct variance. Work out what
happens to composition, constructions, and relevant quantitative data. Specify
whether the proposed result is an equivalence, duality, adjunction, embedding,
correspondence on a restricted class, or only a useful translation. Matching
invariants do not establish any of these. Prove the laws appropriate to the claim:
for example, functoriality and natural isomorphisms for quasi-inverses, or an
adjunction with its compatibility laws. The bridge may deserve extensive research
before it can transport a theorem.

Read [comparison obligations](references/comparisons.md) when choosing what must
be proved for completions, categorical bridges, or new internal languages.

## Prove The Comparison

Track separately the existence of the proposed setting, its internal structural
theorems, the construction of intended models, and the transfer back to the
original mathematics. Distinguish preservation from reflection: proving something
about an image need not prove it about the original object.

Check behavior under the operations that motivated the change. Specify domains,
size restrictions, regularity, exactness, and quantitative constants where relevant.
Treat singular objects, degeneration, or failure of a proposed law as mathematical
information about the framework's scope. Do not repair every counterexample by
adding the desired conclusion as another axiom without explaining the loss.

A more convenient language can move an obligation to a comparison theorem; it
does not remove it. Sheafification alone does not prove an analytic estimate,
faithful recovery of arbitrary original objects, or exactness of a chosen
completed tensor product. A qualitative compactness argument does not by itself
supply effective finite bounds.

When a new logic or type theory is genuinely relevant, distinguish a notation or
library extension from new axioms or kernel rules. Give semantics and identify
the claimed soundness or conservativity theorem precisely. Existence of a model
is not automatically conservativity over an earlier theory. Check the particular
translation needed for the original statement. Proposed formal sketches must be
labelled as such; do not change a proof assistant's trusted foundation as an
incidental implementation step.

## Develop And Assess The Mathematics

Work on actual definitions, examples, constructions, comparison proofs, and
obstructions. A list of desirable axioms is an agenda, not a completed framework.
It can nonetheless be a useful starting point for serious foundational work.

At consolidation points, explain which phenomena now have a common account,
which constructions are justified, what original information is recoverable, and
what remains conjectural. Account for the work of realizing models and proving
comparisons, even if downstream proofs become short. Syntax length, graph
centrality, and matching invariant data are discovery heuristics rather than
evidence of correctness, equivalence, or significance.

Assess progress cumulatively and respect the user's scope and resources. Do not
terminate a coherent theory merely because its return to the initiating conjecture
is unknown. Seek independent structural results, useful constructions, and new
questions; propose a standalone paper or exploration branch when they warrant it.
A proliferation of names or case lists without deeper explanation is a reason
to revise the direction. Record mathematical output and comparison status in the
owning campaign's artifacts, keeping reusable guidance generic.
