---
name: tla-invariants-properties
description: Writing inductive invariants safety properties liveness properties and fairness conditions in TLA+. Use when defining what must always be true what must eventually happen or how to strengthen invariants for model checking or proof. Trigger on requests for invariants temporal properties or fairness.
---

# Invariants and Temporal Properties

## Persona Orientation

This skill operates under the professional persona and methodological standards of Leslie Lamport as established in the specification-master-agent. Safety properties and fairness conditions are written according to the discipline of Specifying Systems (especially Chapters 7 and 8). Prefer inductive invariants that are strong enough to be useful, and never claim liveness without the corresponding fairness hypotheses and machine closure.

## Overview

Invariants and temporal properties are the reason we write specifications. Safety properties are usually expressed as invariants (predicates that must hold in every reachable state). Liveness properties require temporal operators and almost always need fairness assumptions.

## Safety — Inductive Invariants

An inductive invariant I satisfies

- Init => I
- I /\ [Next]_vars => I'

The strongest useful inductive invariant is often TypeOK combined with the key application-specific predicates. When TLC finds a counterexample to a desired invariant either the model is wrong or the invariant is not inductive and must be strengthened.

Always state TypeOK. Then add the essential safety properties of the system (mutual exclusion agreement validity consistency etc.).

## Liveness and Fairness

- Weak fairness WF_vars(A) asserts that if A remains continuously enabled it will eventually be taken.
- Strong fairness SF_vars(A) asserts that if A is enabled infinitely often it will be taken infinitely often.
- Most systems need at least WF_vars(Next) or more precise fairness on the critical progress actions.
- Leads-to properties P ~> Q are the most common way to express liveness.

Never claim a liveness property without the corresponding fairness hypotheses; the property will be false under pure stuttering.

## Property Writing Discipline

1. Write the informal English statement of the property first.
2. Translate it into a TLA+ temporal formula.
3. Check that the formula is evaluated over the correct behaviors (those satisfying Spec).
4. For inductive invariants test preservation mentally or with TLC.

## Common Failures

- Stating a safety property that is true of the real system but not inductive for the model (missing auxiliary variables or history).
- Forgetting fairness and then wondering why a liveness property fails.
- Writing invariants that refer to implementation details that were abstracted away.
- Using []<> or <>[] incorrectly when a leads-to would be clearer.

When an invariant is hard to find consider adding history or prophecy variables carefully or moving to a coarser abstraction.
