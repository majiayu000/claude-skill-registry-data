---
name: codebase-design
description: Use when designing or improving a module interface, choosing a seam, reducing shallow modules, making code easier to test, or reviewing architecture for locality, leverage, adapters, and deep-module design.
---

# Codebase Design

Use this vocabulary when shaping code so Decisions workflows and future agents talk about architecture consistently.

## Vocabulary

- **Module:** anything with an interface and implementation: function, class, package, or vertical slice.
- **Interface:** everything a caller must know: type shape, invariants, ordering, errors, config, and performance.
- **Implementation:** what sits behind the interface.
- **Depth:** how much behavior sits behind a small interface.
- **Seam:** where behavior can vary without editing the caller.
- **Adapter:** a concrete implementation at a seam.
- **Leverage:** capability gained by callers.
- **Locality:** change and verification concentrated in one place.

## Rules

- Prefer deep modules: small interface, rich implementation.
- Use the deletion test: if removing the module only moves complexity, it was shallow.
- Tests should cross the same interface callers use.
- One adapter means a hypothetical seam. Two adapters means a real seam.
- In Decisions tickets, name modules with project domain terms and record durable decisions in project docs or workflow memory.
