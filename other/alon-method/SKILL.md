---
name: alon-method
description: >-
  Attack a mathematical problem by importing powerful techniques from adjacent
  fields in the spirit of Noga Alon: probabilistic method, polynomial method,
  algebraic encodings, topological theorems, spectral tools, entropy,
  combinatorial geometry, coding theory, additive combinatorics, and related
  transfer principles. Use this skill when a direct proof route is stale, when
  the problem has a combinatorial surface but may be encoded into algebra,
  topology, probability, geometry, or linear algebra, or when the goal is to
  develop a new proof technique by adapting a theorem from another domain.
---

# Alon Method

Use this skill when the right move is not another local reduction but a method import: find a
powerful theorem or technique from another area, encode the problem so that the theorem can see it,
and refine the encoding until the original obstruction becomes accessible.

This skill broadens the proof toolkit. In a campaign, `honest-conjecture-resolution` owns progress
accounting, route reviews, and effort limits; use its rules rather than a second checklist here.

## Core Principle

Do not ask "how do we prove this in the native language?" first. Ask:

- What hidden structure would make this problem look probabilistic, polynomial, topological,
  spectral, geometric, algebraic, entropic, or algorithmic?
- Which famous theorem would solve a neighboring problem if only the hypotheses matched?
- What encoding, auxiliary object, or relaxation makes those hypotheses almost true?
- If the theorem does not apply, what new lemma is the smallest missing transfer principle?

## Method-Import Workflow

1. **Choose the level of attack.** State the conjecture obstacle or reusable capability the import
   should address. A method for manipulating a natural class of objects may warrant development
   before its implication for the conjecture is known. At a plateau, reconsider the whole formulation.
2. **Generate a transfer menu.** Try several external languages before committing:
   probability/random choice, polynomial vanishing, linear algebra rank, topology/compactness,
   spectral expansion, entropy/information, finite fields, convexity/duality, geometry, additive
   combinatorics, coding theory, or algorithmic amplification.
3. **Build the dictionary.** For each candidate language, map objects, constraints, witnesses,
   extremizers, and failure modes. Record what structure is preserved and what is lost.
4. **Match theorem hypotheses.** Pick one or two major theorems whose assumptions almost match the
   encoded problem. The useful work is often the gap between the true hypotheses and the desired
   hypotheses.
5. **Stress the encoding.** Test whether the encoding sees the known hard examples, counterexamples,
   and equality cases. If it makes them invisible, the import is probably a false proxy.
6. **Assess the missing transfer.** State the exact lemma needed for the theorem to apply. Explain
   why it should be easier than the original difficulty; merely renaming that difficulty does not
   justify pursuing it. Identify where the target's defining hypothesis supplies the needed input.
   If the formalism applies to a larger class, what additional consequence distinguishes the target
   class? Check that consequence rather than assuming it under a new name. State the gained
   capability: a now-applicable theorem, new witness operation, distinguishing invariant, or
   genuinely smaller residual problem. Check the most doubtful input before routine consequences.
7. **Return to the native problem.** Translate the imported conclusion back into the original
   statement and check constants, quantifiers, boundary cases, and whether the result is equivalent,
   sufficient, or only heuristic.

## Useful Import Patterns

- **Probabilistic existence.** Replace explicit construction by a random object plus expectation,
  alteration, local lemma, concentration, or entropy compression.
- **Polynomial encoding.** Turn forbidden configurations into polynomial vanishing/non-vanishing,
  degree constraints, finite-field identities, or rank conditions.
- **Topological obstruction.** Encode colorings, partitions, intersections, or equivariant maps so a
  fixed-point/Borsuk-Ulam/Tucker/Tverberg-type theorem forces a witness.
- **Linear algebra and rank.** Represent incidence, independence, or set systems by vectors,
  matrices, exterior algebra, eigenvalues, or low-rank factorizations.
- **Spectral or expansion transfer.** Replace local combinatorics by an operator, Laplacian,
  adjacency matrix, Markov chain, or high-dimensional expansion statement.
- **Entropy and information.** Prove counting, concentration, or extremal statements via entropy,
  mutual information, Shearer's lemma, compression, or information monotonicity.
- **Geometry and convexity.** Translate discrete data into convex bodies, separating hyperplanes,
  polytopes, LP duals, Helly/Radon/Caratheodory phenomena, or geometric inequalities.
- **Algorithmic viewpoint.** If a randomized or algebraic algorithm detects the object, its analysis
  may contain the proof technique.

## Anti-Patterns

- Importing a theorem by analogy without writing the exact dictionary.
- Applying a powerful theorem to a proxy that discards the structure making the target true.
- Treating a theorem's conclusion as useful before translating it back to the original quantifiers.
- Letting the imported technique become a broad literature survey rather than a named route.
- Producing many plausible method imports without choosing one operational crux.
- Keeping an import active because it produces more terminology or diagnostics while neither the
  conjecture route nor the method's general mathematical capabilities advance.

## Discovery And Commitment

A discovery pass may compare several encodings or rederive a neighbouring theorem without producing
an immediate lemma. Set its scope and review point first. Use `references/examples.md` for analogy
patterns when useful; locate and verify the exact primary source before relying on a theorem.

After discovery, choose the most promising import by the native consequence it could yield, the
plausibility of its missing transfer, and the cost of a decisive check. A broad literature menu is
background until this connection is made. Do not force every method to attack a convenient local
subclaim if a different formulation of the whole problem has greater potential.

The consequence may be a general transfer principle, new operation, or reusable method rather than
a solution of the initiating conjecture. Such a development can become a distinct theory branch and
a journal paper. Assess its natural scope and substantive contribution under the campaign's theory
criteria; speculative applications should remain labelled as such.

For the chosen encoding, check visibility before theorem strength: does it distinguish examples that
the proposed characterization must distinguish? Can it preserve the data needed by the intended
one-sided implication? Check hypotheses and the translation back before building substantial
machinery. If the encoding fails, repair it only when a concrete change addresses the failure and
makes a new test worthwhile. Otherwise park it under the campaign's route review rules.

## Scope Of Failed Imports

Two objects with the same encoded data and different target status rule out characterizing that
status from that data alone. They do not rule out the whole polynomial, spectral, probabilistic, or
topological method, nor prove that every possible proof must explicitly retain a named feature.
State exactly what failed. Repeated failures of an already excluded encoding are local variants
unless they rule out a materially broader live proposal.

A missing hypothesis is not automatically a theorem of non-transfer. Distinguish a verified
counterexample, a proved limitation, an unproved transfer lemma, and a merely unsuccessful attempt.
A failed pass may be worth recording without being progress on the goal.

## Return To The Problem

Report the chosen theorem or technique, exact dictionary and hypotheses, native conclusion, evidence
status, and consequence for route selection or theory development. Link the precise source theorem
when used. Keep promising proof or theory objectives active; preserve other ideas compactly. If no import is justified, say so rather
than manufacturing an easy claim to refute. Promotion to a manuscript follows relevance and proof
validation, not completion of the method-import workflow.
