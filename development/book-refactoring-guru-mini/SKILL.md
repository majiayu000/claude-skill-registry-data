---
name: book--refactoring-guru--mini
description: >-
  Refactoring Guru (Refactoring.Guru) — Condensed rules — key principles distilled. Use when asked to apply Refactoring Guru principles or review code against Refactoring Guru standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Refactoring.Guru

## When to use

Use when changing existing code where code smells, refactoring technique choice, behavior preservation, and cleanup scope control matter.

## Primary bias to correct

Refactoring is not general cleanup or pattern application. It is a small, smell-driven, behavior-preserving treatment with verification and a stop condition.

## Decision rules

- Separate refactoring from feature work and bug fixes. If behavior changes, name it as behavior change and isolate it from structural edits.
- Diagnose the smell before choosing a technique: symptom, maintenance cost, scope, expected cleaner end state, verification path, and stop condition.
- Prefer the smallest treatment that directly reduces the diagnosed smell; escalate only when the smaller technique is blocked.
- Keep the code runnable and understandable through small named transformations rather than broad redesign.
- Run relevant checks after risky moves, public interface changes, state-flow changes, or algorithm substitution.
- Stop when the named smell is gone or materially reduced; record new smells separately unless they block the current change.
- Use the Rule of Three: tolerate uncertain duplication early, but refactor the third similar occurrence unless the similarity is coincidental.
- Treat technical debt as compounding cost; pay down the debt that slows current change speed, correctness, or team understanding.
- Scan smells by category: bloaters, object-orientation abusers, change preventers, dispensables, couplers, and incomplete library gaps.
- For bloaters, prefer extraction, parameter/data modeling, and responsibility splits before creating method objects, subclasses, or interfaces.
- For switch/type-code smells, isolate the decision first; use polymorphism, subclasses, or state/strategy only when variation is stable and repeated.
- For change preventers, move behavior and data toward the owner of the changing concept so one conceptual change has one main edit site.
- For dispensables, delete or inline unused structure, but check public, generated, reflected, serialized, plugin-facing, and framework extension uses first.
- For couplers, reduce navigation and private knowledge; keep delegating layers only when they hide volatile structure, policy, or a real boundary.
- Use comments for rationale, constraints, contracts, or hard algorithms; use names, variables, methods, or assertions when comments explain unclear code.
- Keep behavior with the data it changes unless separation deliberately supports interchangeable behavior.
- Encapsulation is not finished by adding getters and setters; move behavior inward when callers are still manipulating exposed data.
- Avoid speculative abstractions: do not create wrappers, parameter objects, interfaces, superclasses, or hierarchy variants without a real concept or client.
- Preserve public compatibility or provide a transition path when changing signatures, constructors, visibility, type hierarchy, or externally reachable APIs.
- Before extraction or movement, identify inputs, outputs, mutated variables, callers, visibility, construction paths, and invariants.
- Before condition consolidation or algorithm substitution, verify side effects, ordering, truth tables, edge cases, and performance-sensitive behavior.
- Before data reorganization, decide identity, value/reference semantics, mutability, equality, lifecycle ownership, association direction, and synchronization.
- Before generalization changes, prove shared behavior is real; preserve substitutability and avoid inheriting unused behavior.
- Choose exceptions deliberately: a simple conditional, useful comment, intentional strategy separation, small extension point, or clear duplication may be better than a mechanical treatment.

## Trigger rules

- When a method needs comments, scrolling, or local-state reconstruction, try `Extract Method`; use `Replace Temp with Query`, `Introduce Parameter Object`, or `Preserve Whole Object` when locals block extraction.
- When a class has multiple reasons to change, use `Extract Class`; use subclass/interface extraction only for stable variants or real client-facing subsets.
- When primitives, arrays, magic numbers, or type codes carry meaning, model the concept only if the model adds naming, validation, behavior, or safer variation handling.
- When a parameter list grows beyond local reasoning, replace derived parameters, preserve a whole object, or introduce a parameter object only for a real recurring concept.
- When the same change requires edits across many files, move methods/fields or extract ownership so the knowledge is centralized.
- When client code navigates object chains, hide the delegate or move behavior closer to the data; do not add pure forwarding.
- When a class mostly forwards, remove the middle man unless it protects boundary policy or volatile structure.
- When a method both queries and mutates, separate query from modifier unless atomic read-modify behavior is the public contract.
- When branches repeat behavior, decompose, consolidate, or move duplicate fragments only after checking side effects and execution order.
- When null checks dominate, introduce a null object only if absence can obey the same interface; keep absence explicit when it is an error.
- When inheritance creates refused bequest or intimacy, push members down or replace inheritance with delegation.
- When deleting dead or speculative code, verify external reachability and test-only access before removal.
- When a library class is incomplete, use a foreign method for one narrow gap and a local extension only for substantial repeated gaps.
- When cleanup keeps expanding, stop at the diagnosed smell and report the next smell separately.

## Final checklist

- Is this change clearly refactoring, feature work, or bug fixing?
- Which smell was diagnosed, and what cost did it create?
- Was the smallest suitable treatment used before riskier structure?
- Did behavior stay preserved under relevant checks?
- Did the named smell become materially better?
- Did the change avoid speculative abstraction and mechanical pattern use?
- Were public compatibility, state flow, and ownership checked?
- Is any intentionally untreated smell documented rather than hidden?
