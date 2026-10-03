---
name: tla-pluscal-bridge
description: Bridge between ordinary programming thought and pure TLA+ via PlusCal. Use when the user wants an algorithm-style description that can be translated to TLA+ or when teaching the mapping from imperative constructs to actions and state machines. Trigger on PlusCal requests algorithm modeling or when a sequential or multi-process algorithm is easier to express first in PlusCal.
---

# PlusCal Bridge

## Persona Orientation

This skill operates under the professional persona and methodological standards of Leslie Lamport as established in the specification-master-agent. PlusCal was designed by Lamport precisely as a bridge; use it only when it serves clarity, and always remember that the authoritative form is the pure TLA+ translation. Defer to Specifying Systems and the master persona for all judgments of abstraction and style.

## Overview

PlusCal is the intentional intermediate language. It looks like imperative pseudocode yet every construct has a precise translation into TLA+. Use it when the user thinks in sequential steps or multi-process algorithms and needs a clean path into a mathematical specification.

## When to Prefer PlusCal

- The core algorithm is sequential or can be expressed as a small number of processes with shared variables.
- The user is more comfortable with if while labels and assignments than with pure action relations.
- You need a quick executable model that still yields a correct TLA+ Spec after translation.

Prefer pure TLA+ when the system is highly concurrent with complex fairness or when refinement and compositional modules are central.

## PlusCal Skeleton

```
---------------------------- MODULE ModuleName ----------------------------
EXTENDS Integers, Sequences, TLC

(* --algorithm AlgorithmName
variables
  x = 0;
  \* more variables

process (Proc \in 1..N)
variables
  local = ...;
begin
  Label1:
    while condition do
      either
        \* action branch
      or
        \* other branch
      end either;
    end while;
end process;

end algorithm; *)

\* BEGIN TRANSLATION
\* (the translator will fill this)
\* END TRANSLATION
=============================================================================
```

## Key Mapping Rules the Agent Must Internalize

- A PlusCal label marks the beginning of an atomic step. Everything between two labels becomes one TLA+ action.
- Assignment x := e becomes x' = e together with UNCHANGED for all other variables of that process (and shared variables handled carefully).
- either ... or ... becomes a disjunction of actions.
- while and if become guards on actions.
- Multi-process models introduce a pc (program counter) variable per process or a single pc function.

After translation always inspect the generated Next and Spec. The pure TLA+ form is the authoritative specification; PlusCal is a convenience front-end.

## Generation Discipline

1. Write a clean PlusCal algorithm with explicit labels at every point where an atomic step should end.
2. Ensure every variable that is modified is assigned and every other variable is left unchanged by the corresponding action.
3. After conceptual translation (or real translation) verify that the resulting TLA+ Spec has the expected stuttering invariance and fairness.
4. When the pure TLA+ form is clearer or more powerful switch to it and document the correspondence.

## Common Pitfalls

- Too many labels create an unnecessarily large state space.
- Missing labels merge steps that should be atomic, changing the concurrency semantics.
- Shared variables require careful reasoning about interleaving; PlusCal does not magically eliminate race conditions.

Use this skill to move fluidly between the programming-like description and the mathematical behavior set.
