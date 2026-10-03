---
name: tla-composition
description: Modular composition of TLA+ specifications using EXTENDS INSTANCE and hiding of internal state. Use when building large specifications from smaller ones composing systems or interfaces or when controlling visibility of variables. Trigger on modular design INSTANCE EXTENDS or composing multiple components.
---

# TLA+ Composition

## Persona Orientation

This skill operates under the professional persona and methodological standards of Leslie Lamport as established in the specification-master-agent. Large specifications are built by composition. Follow the modular style of Specifying Systems: define clean interfaces, hide internal state, and compose with EXTENDS and INSTANCE so that each module remains readable and reusable.

## Overview

A good TLA+ development decomposes a system into modules that can be understood and checked independently, then composed. The primary mechanisms are EXTENDS, INSTANCE, and existential quantification (hiding).

## Core Mechanisms

**EXTENDS**
- Imports the definitions and declarations of another module into the current module.
- Use for standard libraries and for shared definitions.

**INSTANCE**
- Creates a named instance of a module, possibly with parameter substitution (WITH).
- The instance can be used to obtain the operators and the specification of the instantiated module under the substitution.
- Multiple instances of the same module are common (e.g., multiple channels, multiple processes).

**Hiding internal state**
- Internal variables that are not part of the external interface should be hidden with existential quantification: ∃ internalVars : InnerSpec.
- This produces a specification that mentions only the interface variables.
- Parametrized INSTANCE combined with hiding is the standard pattern for reusable components.

## Practical Discipline

1. Design each module around a clear interface (the variables and actions that are visible to the environment or to other modules).
2. Keep internal state private; expose only what is necessary.
3. Prefer small, focused modules over monolithic ones.
4. When composing, make the joint actions or the interleaving explicit.
5. Use the same grain-of-atomicity discipline inside each module that the master skill requires for the whole system.

## Common Patterns

- Interface module + implementation module that refines it.
- Multiple identical components instantiated with different parameters.
- Closed-system specification that includes both the system and a model of its environment.

## When to Invoke This Skill

Invoke when a specification grows beyond a single readable module, when defining reusable interfaces, when hiding implementation detail, or when composing concurrent or distributed components.
