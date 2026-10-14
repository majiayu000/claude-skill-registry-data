---
name: dependency-seam-detection
description: "Trigger: dependency seam detection, hard dependencies. Find seams that make legacy code testable."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.1.1"
  status: testing
---

# Dependency Seam Detection
Find hard-to-control dependencies and propose seams that make tests possible before refactor.

## Dependency smells

- `new` inside business logic.
- Static calls and singletons.
- System clock, random, filesystem, environment, or global config.
- Direct DB access, external services, queues, event buses, cache, threading, or async work.

## Seam options

- Constructor injection.
- Interface seam.
- Object seam.
- Wrapper or adapter.
- Parameter injection.
- Protected method seam.
- Sprout method.
- Sprout class.

## Seams and enabling points

A seam is a place where behavior can be changed without editing the code at that place; every seam has an enabling point where the substitution is decided. Object seams (polymorphism, injection) are the default in OO code; link/classpath seams (test-time substitution of a dependency at the linker or classpath level) and preprocessing seams sit below them and matter when the code itself cannot be edited.

## Selection rule

Prefer the least invasive technique that lets a test run: parameter or constructor injection before interface extraction, interface extraction before subclass-and-override, subclass-and-override before brute force. Dependency-breaking is medicine, not vitamins — a scar (a slightly awkward seam) is acceptable and gets cleaned up in a later refactor once tests exist.

## References

- `references/dependency-breaking-catalog.md` — dependency-breaking catalog (WELC): four strategies, the individual techniques with contraindications, and the instantiation-blocker table.
