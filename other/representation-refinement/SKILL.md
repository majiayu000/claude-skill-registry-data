---
name: representation-refinement
description: >-
  Diagnose information lost by a mathematical representation and refine it to
  support intended observations and operations. Use when equal summaries hide
  different outcomes, a proposed composition law fails, or a calculus needs
  additional dependence, sign, transition, or remainder data. Distinguish lost
  information from a false target, a false law, an object-class failure, and a
  missing estimate; use finite partition refinement when explicit finite models fit.
---

# Representation Refinement

Find what a representation must remember for the mathematics it is meant to
support. Work on a specific observation, operation, or failed law, rather than
inventing a general abstraction without a concrete comparison question.

This is a focused process usable within theory building, calculus construction,
or an ordinary proof attempt. It does not require a campaign or a previous failed
proof. In a campaign, return the witness, repaired representation, proved laws,
and remaining obligations to the existing state.

## Diagnose Before Repairing

Recover the actual definitions, known results, and previous corrections. Specify
concrete objects X, a representation alpha:X->A, intended observations Q, and the
operations the representation should support. Record quantitative hypotheses and
what success means: exact recovery, an upper bound, an approximation, or a usable
composition law.

Classify the evidence and its scope:

| Failure | Appropriate work |
|---|---|
| A concrete object violates the target | Correct or refute the target |
| A proposed auxiliary identity is false | Change the law; the target may survive |
| Equal retained data hide different required outcomes | Refine the representation or weaken its intended use |
| A natural construction leaves the object class | Enlarge the objects or presentations and prove comparisons |
| An identity holds but its quantitative control is missing | Prove the estimate with its actual assumptions |

Several diagnoses can coexist. Do not infer falsity of a target from failure of
one sufficient surrogate, or infer lost information merely from an unsuccessful
proof search.

## Test Sufficiency And Construct A Repair

For exact recovery of Q:X->Y, a map q:alpha(X)->Y with Q(x)=q(alpha(x)) exists
exactly when Q is constant on every alpha-fibre. A witness pair with equal alpha
and unequal Q rules out this exact use. Unequal Q values alone do not refute a
common upper bound: an inequality witness must violate the proposed bound itself.
For deterministic operations u, an induced operation on alpha(X) also requires
alpha(x)=alpha(y) to imply alpha(u(x))=alpha(u(y)), on the appropriate domains.
Track definedness as well as outputs for partial operations.

Choose candidate extra data from the failed operation: signed coefficients for
cancellation, source provenance for dependence, transitions for gluing, or a
remainder for an inexact identity. One repair is alpha'(x)=(alpha(x),r(x)). Show
that it separates the witness, then prove the intended recovery/composition laws
on the claimed class. Separating one pair does not prove sufficiency everywhere.

Compare alternative repairs, including changing the law, weakening the conclusion,
retaining a latent presentation, or using a known richer representation. Added
data should have mathematical meaning and an available construction; recording
the unknown answer or a complete object can be sufficient yet offer no progress.
Assess cost and usefulness after accounting for the work of constructing it.

## Use Finite Refinement When Its Inputs Are Available

Read [finite sufficient representations](references/finite-refinement.md) when X,
its operations, and the observations are supplied explicitly. It gives a terminating
partition procedure and a related observable-space/operator-algebra construction.
The quotient is relative to those operations and observations; it may retain all
of X. A supplied observable cannot be an oracle for the unresolved problem.

The finite construction uses standard automata partition-refinement ideas.
Counterexample-guided abstraction refinement is a related verification precedent;
its termination and correctness results do not automatically transfer to arbitrary
mathematical research. Bounded countermodel search can find informative witnesses;
not finding one does not prove an infinite-class law.

## Integrate The Mathematics

Produce a concrete witness, a proved sufficiency/comparison result, a repaired law,
or a precisely located remaining obligation. Keep examples, definitions, proofs,
and the failed representation's scope in the existing project artifacts.

Use `proof-calculus` when repaired data support a language of arguments and a
validity theorem; `mathematical-framework-design` when the setting or a substantial
correspondence must be constructed; `grothendieck-rising-sea` when developing the
surrounding theory. These processes can inform each other without fixed gates.
Do not present a more elaborate representation as a solution until its concrete
models, comparisons, and required estimates are proved.
