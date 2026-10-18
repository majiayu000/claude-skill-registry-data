---
name: codebase-design
description: Design deep modules with small interfaces, clean seams, adapters, leverage, locality, and testable boundaries. Use when designing or improving module interfaces, finding deepening opportunities, deciding where a seam goes, making code testable, or when another skill needs codebase-design vocabulary.
---

# Codebase Design

Design deep modules: lots of behavior behind a small interface, placed at a clean seam, testable through that interface.

Use this vocabulary consistently during planning, TDD, implementation, and architecture review.

## Glossary

**Module**: anything with an interface and implementation. A function, class, package, or slice can be a module.

**Interface**: everything a caller must know to use the module correctly: types, invariants, ordering, error modes, configuration, and performance expectations.

**Implementation**: what sits inside the module.

**Depth**: leverage at the interface. A deep module exposes a small interface that exercises substantial behavior.

**Seam**: a place where behavior can change without editing the caller. The seam is where the module interface lives.

**Adapter**: a concrete implementation that satisfies an interface at a seam.

**Leverage**: more capability per unit of interface a caller must learn.

**Locality**: change, bugs, knowledge, and verification concentrate in one place.

## Principles

- Depth is a property of the interface, not line count.
- The interface is the test surface.
- One adapter means a hypothetical seam. Two adapters means a real seam.
- Internal seams can exist inside a module without becoming part of the public interface.
- The deletion test: if deleting the module makes complexity vanish, it was pass-through; if complexity reappears across callers, it was earning its keep.

## Testability Checks

- Accept dependencies instead of creating them inside behavior.
- Return observable results instead of hiding side effects.
- Keep the interface small enough that tests can cover behavior through it.
- Test through the same seam callers use.

## Deepening

When deepening a shallow cluster, classify dependencies:

- **In-process**: pure computation or in-memory state; merge and test through the new interface.
- **Local-substitutable**: use a local stand-in such as an in-memory filesystem or local database.
- **Remote but owned**: define a port at the seam; use production and test adapters.
- **True external**: inject the external dependency behind a port and test with a mock adapter.

See [DEEPENING.md](DEEPENING.md) for the full deepening checklist.

## Exploring Alternatives

When the interface choice is important, design it twice. Produce multiple radically different interfaces and compare depth, locality, and seam placement before choosing.

See [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md).
