---
name: tla-state-machines
description: Core modeling methodology for TLA+ state machines. Use when choosing variables defining Init and Next designing actions structuring the state space or deciding abstraction level for concurrent or distributed systems. Trigger on questions about how to model a system as a state machine or how to write good actions and Next relations.
---

# TLA+ State Machines

## Persona Orientation

This skill operates under the professional persona and methodological standards of Leslie Lamport as established in the specification-master-agent. All decisions about variables, grain of atomicity, and state-space structure are governed by the advice in Specifying Systems, especially Chapter 7. Justify every abstraction choice in the spirit of Lamport’s own writing.

## Overview

Every TLA+ specification is a state machine. The art lies in choosing the right state representation and especially the right grain of atomicity so that the model is both faithful to the system and tractable for model checking or proof. This skill follows the methodology of Specifying Systems Chapters 1–7.

## Grain of Atomicity (The Central Decision)

The single most important modeling choice is the grain of atomicity — what system changes are represented as a single step of a behavior. 

- Coarser grain simplifies the model and reduces state space but may hide interleavings that matter.
- Finer grain reveals more concurrency errors but can make the model larger and harder to check.
- Justify the chosen grain explicitly. Prefer the coarsest grain that still exposes the properties of interest and the potential errors.
- When actions commute (no shared variables, neither enables/disables the other), coarser models are often equivalent for the properties being checked.

Always begin by writing a few sample behaviors; the natural step boundaries in those behaviors usually reveal the right grain.

## Decision Process for Variables

1. List every piece of information that must be observed to state the properties of interest.
2. Eliminate anything that can be derived from other variables or that is pure implementation detail.
3. Prefer finite domains or domains that can be bounded for TLC.
4. Represent collections as functions, sets, or sequences according to the access patterns needed by the actions.

A good variable set produces a state space whose geometry is easy to reason about.

## Init and Next

- Init must be a predicate that is true of exactly the starting states (or a nondeterministic set of them).
- Next is almost always written as a disjunction of named actions. Each action is a predicate relating the current state to the next state (using primed variables).
- Every action should have an explicit UNCHANGED clause for variables it does not modify. This prevents accidental nondeterminism and makes the model easier to read.

## Action Design Principles

- An action should correspond to a single atomic step of the system at the chosen level of abstraction.
- Guards (enabling conditions) appear as the unprimed part of the action formula.
- Prefer small orthogonal actions over large monolithic ones when concurrency is important; this exposes interleavings.
- When modeling a real implementation, study how the code decomposes operations into atomic steps and mirror that decomposition (or deliberately coarsen it with justification).

## Abstraction Geometry

Think of the reachable states under Next as a directed graph (more precisely as a set of infinite paths). The model is good when:

- the graph contains every behavior the real system can exhibit (up to stuttering)
- the graph does not contain extra behaviors that would violate the intended properties
- the graph is small enough that TLC can explore it or that inductive invariants can be found

## Practical Checklist Before Declaring a Model Complete

- Sample behaviors have been written and the grain of atomicity justified.
- TypeOK holds in Init and is preserved by every action.
- Every variable that can change appears primed in at least one action.
- No action leaves a variable unconstrained when it should be unchanged.
- The fairness conditions match the progress assumptions of the system and preserve machine closure.
- The key safety invariants are stated and appear plausible.
- Internal variables that are not part of the external interface are candidates for hiding.

When these conditions are satisfied the state machine is ready for property checking and for refinement toward an implementation.
