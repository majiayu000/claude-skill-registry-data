---
name: book--refactoring-guru--nano
description: >-
  Refactoring Guru (Refactoring.Guru) — Minimal rules — essential one-liners only. Use when asked to apply Refactoring Guru principles or review code against Refactoring Guru standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Refactoring.Guru

## When to use

Use as a compact always-on bias for safe, smell-driven refactoring during existing-code changes.

## Primary bias to correct

Refactoring is not cleanup for its own sake: diagnose one smell, treat it with the smallest behavior-preserving move, verify, then stop.

## Decision rules

- Separate structural refactoring from feature and bug behavior; if behavior changes, name and isolate it.
- Diagnose the smell before choosing a technique: symptom, cost, smallest treatment, verification, and stop condition.
- Prefer small named transformations over broad redesign.
- Keep the program runnable and run relevant checks after risky movement, state-flow changes, public API changes, or algorithm replacement.
- Stop when the diagnosed smell is reduced; do not chase new smells unless they block the current change.
- Prefer extraction, naming, movement, inlining, and encapsulation before adding hierarchy, polymorphism, wrappers, or method objects.
- Do not create abstractions from coincidental similarity, random parameter bags, simple conditionals, or speculative future needs.
- Keep behavior with the data it changes unless separation intentionally supports interchangeable behavior.
- Preserve public compatibility when changing signatures, constructors, visibility, hierarchy, or externally reachable code.
- Delete or inline dispensable code only after checking public, generated, reflected, serialized, plugin-facing, framework, and test-only uses.

## Trigger rules

- When a method needs comments or local-state reconstruction, extract a named method after checking inputs, outputs, and mutated variables.
- When a class changes for unrelated reasons, extract the responsibility; use subclass/interface only for stable variants or real client subsets.
- When conditionals repeat by type or state, isolate the decision before using polymorphism; leave simple honest conditionals alone.
- When duplicate code appears the third time, refactor unless the similarity is likely to diverge.
- When parameter lists or primitive clumps carry one concept, model the concept; do not pass a huge object to hide dependency.
- When clients navigate chains or internals, hide the delegate or move behavior; remove pass-through middle men that add no policy.
- When null, error code, assertion, value/reference, or association changes are considered, verify semantics before changing structure.

## Final checklist

- Smell named?
- Smallest treatment?
- Behavior verified?
- Stop condition reached?
- No hidden feature change?
- No speculative abstraction?
