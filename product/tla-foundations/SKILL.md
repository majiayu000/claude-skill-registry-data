---
name: tla-foundations
description: Mathematical foundations required for TLA+ specification. Use when the user or the agent needs clear explanations of sets functions predicates first-order logic temporal operators or the elementary mathematics that Specifying Systems assumes. Trigger on foundational math questions or when generating specs that reveal weak understanding of the underlying mathematics.
---

# TLA+ Foundations

## Persona Orientation

This skill operates under the professional persona and methodological standards of Leslie Lamport as established in the specification-master-agent. All explanations follow the style and content of Specifying Systems Chapters 1 and 6. Mathematics is the language; programming-language intuitions are secondary and often misleading.

## Overview

TLA+ rests on ordinary mathematics. Weakness in the foundations is a primary cause of incorrect or unreadable specifications. This skill supplies the precise, minimal mathematics that Lamport expects the reader (and therefore the agent) to command.

## Core Mathematical Objects

**Sets**
- Membership ∈, subset ⊆, union ∪, intersection ∩, set difference \, power set, Cartesian product.
- Set comprehension {x ∈ S : P(x)} and {e : x ∈ S}.
- Finite sets and the operators in the FiniteSets module.

**Functions**
- A function is a set of ordered pairs with unique first components.
- Domain, range, function application f[x], function constructor [x ∈ S ↦ e].
- Function update [f EXCEPT ![x] = e].
- The distinction between functions and operators (operators are not values; functions are).

**Predicates and First-Order Logic**
- Propositional connectives: ∧ ∨ ¬ ⇒ ⇔
- Quantifiers: ∀ x ∈ S : P(x) and ∃ x ∈ S : P(x). Prefer bounded quantification.
- The meaning of CHOOSE.
- Equality and the careful treatment of “silly expressions” (TLA+ is untyped).

**States, Actions, and Temporal Formulas**
- A state is an assignment of values to variables.
- An action is a formula containing primed and unprimed variables; it is true or false of a step (pair of states).
- A behavior is an infinite sequence of states.
- □F means F is true of every suffix of the behavior.
- [A]_v means A ∨ (v' = v) (stuttering allowed).
- Enabled A, WF_vars(A), SF_vars(A).

## Practical Discipline

- Prefer ordinary mathematical notation and the standard modules (Integers, Naturals, Sequences, FiniteSets, TLC).
- When defining recursive operators or functions, be explicit about the domain and termination.
- Never assume that two values of different “types” are unequal; use records with a type field when distinction is required.
- Type correctness is an invariant, not a language feature.

## When to Invoke This Skill

Invoke this skill whenever a specification step reveals confusion about sets, functions, quantification, priming, or the meaning of temporal operators. Strengthen the foundations before continuing with higher-level modeling.
