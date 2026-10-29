---
name: proof-developer
description: Develop rigorous mathematical proofs of precisely stated conjectures. Use when the user wants a proof or a campaign has selected a substantive proof step; prior computational testing is helpful when informative, but not required. Guides the process from proof strategy selection through step-by-step development to publication-ready LaTeX. Handles strategy identification, lemma decomposition, gap checking, and iterative refinement. Works for proofs in combinatorics, topology, algebra, and related areas of pure mathematics.
---

# Proof Developer

Develop complete mathematical arguments with explicit hypotheses and justified steps. In a campaign,
`honest-conjecture-resolution` selects routes and reviews their value; this skill constructs and
checks the selected proof. Keep proof correctness distinct from relevance to the original goal.

## Understand The Statement And Its Role

Restate the claim with all objects, quantifiers, and conditions defined. Identify whether it asks for
an implication, equivalence, construction, exhaustive classification, or bound. Review available
examples, counterexamples, and exact source theorems. Look up literature when an unfamiliar theorem
or plausible known result could discharge the difficult step; do not substitute vague name matching
for checking its hypotheses.

For an auxiliary claim, identify its place in a sufficient proof route and the assumptions still
needed afterward. Mark arrows as equivalent, necessary, sufficient, or special-case. A strengthened
claim can be unnecessarily hard or false even when the original target is true.

For a construction from auxiliary data, write both implications: the hypotheses supply admissible
data, and those data produce the desired witness. Identify which theorem supplies each input and
whether the inputs can be chosen jointly. Separately existing witnesses need not be compatible.
Compare choices permitted by the target with those frozen by the construction; failure for a fixed
reference or boundary assignment need not refute existence after reselection.

A selected claim may instead develop general theory: a new operation, structural law, representation,
or comparison on a natural class. Give its independent mathematical purpose; do not demand a known
implication to the initiating conjecture. Develop its proof with the same rigor, and assess a possible
standalone paper by the coherent contribution of the theory.

## Work Backward Before Filling In Details

Outline how the conclusion would follow. Identify the most uncertain indispensable implication;
attempt to prove or falsify it before proving routine supporting lemmas. Check cheap prerequisites
and known counterexamples first. Do not work in exposition order merely because notation and easy
lemmas come first on the page.

If no strategy is selected, compare a few approaches by their hardest step and its plausibility:
direct argument, induction or minimal counterexample, construction, extremal counting, duality,
algebra, geometry, or topology. Different technique names do not make independent routes when they
all require the same unresolved implication. Select and proceed without asking the user to decide
routine proof tactics.

A toy case is useful when it isolates this difficult mechanism. Explain what its proof would teach
about the full statement; avoid solving successively easier variants with no transfer back.

## Build A Sufficient Proof Architecture

State needed intermediate claims precisely and check that together they imply the conclusion.
Expose hidden assumptions, circular dependencies, and degenerate cases before investing in the
individual proofs. If a reduction introduces a new central lemma, explain what makes that lemma
more accessible; equivalence alone does not make the problem easier.

For induction or minimal-counterexample arguments, give the strictly decreasing quantity, verify
closure of hypotheses, and state exactly what the smaller-instance theorem supplies. Existence of
some witness on a smaller object does not grant arbitrary prescribed boundary values. Prove that
stronger extension property separately if the assembly requires it.

Develop a proof in the most informative order, then write it in the reader's logical order. A single
substantive lemma may deserve sustained work. Do not fragment every nontrivial sentence into a named
lemma or add generalizations merely to increase the number of finished results.

## Develop And Challenge The Argument

For every step:

- state what is proved and justify it from definitions, proved lemmas, or an exact cited theorem;
- keep quantifiers, implication direction, and dependence on parameters explicit;
- handle all cases, including boundary and degenerate cases;
- preserve the data used by the target when passing to a proxy, quotient, or auxiliary object;
- test the proposed inference against discriminating examples where useful.

Challenge the step most likely to fail. A small computational test can be decisive for a dubious
subclaim, but successful tests do not discharge it. A proof does not require a ritual computational
replay of every consequence when no unresolved concern motivates one.

If stuck, check whether the claim is false, too strong, or simply beyond the current technique. Try a
contrapositive, different representation, exact literature match, or a weaker statement that still
suffices. Do not repeatedly weaken the conclusion or strengthen assumptions without rechecking the
connection to the original goal. Report the exact unresolved implication and follow the campaign's
cumulative route review; a new lemma name does not reset that review.

## Assemble And Audit

Write the argument so the reader can reconstruct every inference. For a long proof, give a roadmap,
then the details. Verify:

- every object and assumption is defined before use;
- intermediate claims imply exactly the stated conclusion without circularity;
- theorem citations match the actual hypotheses, conventions, and scope;
- every case is proved, or its reduction to a proved case is explained precisely;
- boundary cases and any examples used to check the proof agree with the argument;
- provisional claims and computational evidence are not silently used as theorems.

Correctness fixes remain necessary even when they produce no new result. If the proof fails, preserve
what is justified and state the gap; do not call the theorem essentially proved. A failed route says
nothing conclusive about the truth or ultimate tractability of the original problem by itself.

## Write At The Appropriate Fidelity

When the user requests a finished proof or manuscript, provide a complete, readable argument. For
campaign work, preserve a full auditable proof of any relied-on lemma, then decide whether its role
warrants promotion into the curated paper or a standalone theory paper. A substantial general theory
need not remain a side note because the initiating conjecture is open. An isolated local result can
remain a research note.
Do not automatically add sections, corollaries, or examples after every successful attempt.

For promoted material, follow the project's LaTeX conventions and the relevant writing skill:
introduce definitions and intuition, give useful examples, state the theorem precisely, and provide
a proof sketch when length warrants it followed by the full proof. Match macros, notation, labels,
and cross-references. Keep required PDFs current with SyncTeX when source changes warrant a build.

Conclude with what is proved, its general theoretical contribution, any effect on the original
conjecture, and what remains open. A proof of a
substantial sufficient lemma can be real progress even before the final theorem closes; make the
remaining dependencies explicit rather than demanding an immediate complete solution.
