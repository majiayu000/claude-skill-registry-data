---
name: tla-syntax
description: Authoritative reference and generation rules for pure TLA+ surface syntax. Use when writing or correcting TLA+ modules operators expressions modules EXTENDS INSTANCE VARIABLES Init Next Spec priming UNCHANGED fairness or any syntactic construct. Trigger on requests for correct TLA+ syntax examples or when fixing SANY errors.
---

# TLA+ Syntax

## Persona Orientation

This skill operates under the professional persona and methodological standards of Leslie Lamport as established in the specification-master-agent. All syntactic decisions defer to the mathematical style and clarity requirements of Specifying Systems. Prefer the classic ASCII operators that Lamport uses throughout the book and the official tools. Never introduce programming-language habits.

## Overview

Produce only syntactically valid TLA+ that passes SANY. Prefer the classic ASCII operators. Never emit programming-language syntax (semicolons != = for definition backticks Unicode operators unless the user explicitly requests Unicode).

## Core Syntax Rules

- Definition operator is == (never =)
- Inequality is # (never !=)
- Conjunction is /\   Disjunction is \/   Negation is ~
- Implication is =>   Equivalence is <=>
- Primed variable is x'   (the value in the next state)
- Stuttering-tolerant next-state relation is [Next]_vars
- Module terminator is ====
- Comments use \* for single line or (* ... *) for blocks

## Module Skeleton (Always Start From This)

```
---------------------------- MODULE ModuleName ----------------------------
EXTENDS Integers, Sequences, FiniteSets, TLC   \* add only what is needed

CONSTANTS ...
VARIABLES ...

vars == << ... >>     \* tuple of all variables

TypeOK == ...         \* type invariant

Init == ...

Action1 == ...
Action2 == ...
Next == Action1 \/ Action2 \/ ...

Spec == Init /\ [][Next]_vars /\ WF_vars(Next)   \* adjust fairness

=============================================================================
```

## Critical Constructs

**Variables and priming**
- Every variable that may change must appear primed in at least one action or be declared UNCHANGED.
- An action that does not mention a variable leaves its value unconstrained. Always write UNCHANGED <<v1, v2, ...>> for the variables that stay the same.

**Operators**
- Recursive operators need the RECURSIVE keyword and careful domain restriction.
- Higher-order operators are allowed and useful for abstraction.

**Quantifiers and set constructs**
- \A x \in S : P(x)
- \E x \in S : P(x)
- {x \in S : P(x)}
- [x \in S |-> e]   for functions
- CHOOSE x \in S : P(x)

**Temporal operators**
- []P     always
- <>P     eventually
- P ~> Q  leads-to
- WF_vars(A)   weak fairness
- SF_vars(A)   strong fairness

## Common Syntax Errors to Prevent and Repair

- Using = instead of == for definitions
- Using != instead of #
- Missing module header or ==== terminator
- Forgetting to list all variables in vars or in UNCHANGED
- Priming a constant or an expression that is not a variable
- Nested temporal operators without proper parentheses
- Unicode operators (∨ ∧ ≠) unless the environment supports them and the user requests them

## Generation Discipline

When writing a full module always emit the complete text including the MODULE line and the terminating ====.  
When repairing an existing fragment identify the exact SANY error class and rewrite only the offending construct while preserving the surrounding logic.

## References

For deeper examples of well-formed modules see the standard TLA+ Examples repository patterns and the companion skills on state machines and invariants.
