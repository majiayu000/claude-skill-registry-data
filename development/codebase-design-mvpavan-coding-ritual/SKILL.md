---
name: codebase-design
description: Use for substantive module-interface, encapsulation, or testability decisions. Skip ordinary code explanations and cosmetic refactors.
---

# Codebase Design

Design interfaces that hide useful complexity and concentrate change. Apply this
lens to real interface or module decisions, not every explanation of code.

## Vocabulary

- **Module:** an interface and its implementation, at a useful scale.
- **Interface:** what callers must know, including invariants, ordering, errors,
  configuration and performance constraints, not just type signatures.
- **Depth:** useful behavior hidden behind a manageable interface.
- **Seam:** a place where behavior can vary without changing its callers.
- **Adapter:** a concrete implementation filling a role at that seam.
- **Locality:** related knowledge, changes and checks stay together.

Use established project vocabulary, including API, service or boundary where
precise. These definitions aid reasoning rather than replacing the domain glossary.

## Design checks

Ask what callers gain, what complexity disappears from them, and what knowledge
still leaks through. If deleting a layer merely removes forwarding, question its
value; if it spreads complexity across callers, the layer may be earning its keep.

An interface can be justified by encapsulation, ownership or a present testing
need even with one implementation. Additional adapters are evidence of variation,
not a universal prerequisite. Internal seams and focused internal tests are valid;
do not expose internals merely to satisfy a testing rule.

Prefer explicit dependencies and pure calculations where they clarify behavior;
side effects are legitimate responsibilities when isolated and well specified.
Preserve compatibility and operational constraints when deepening a module.

For dependency-oriented deepening, use `DEEPENING.md`. For a consequential interface
choice with multiple credible designs, optionally use `DESIGN-IT-TWICE.md`;
ordinary design decisions do not require multiple agents or variants.
