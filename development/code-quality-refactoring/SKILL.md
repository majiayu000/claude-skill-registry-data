---
name: code-quality-refactoring
description: Improve maintainability and structure while preserving behavior using framework-agnostic refactoring principles.
metadata:
  internal: true
---

# Code Quality and Refactoring

Use this skill for cleanup, simplification, decomposition, duplication removal, complexity reduction, and maintainability improvements.

This skill is language and framework agnostic.

## Preserve Behavior

Unless the task explicitly changes behavior, refactoring should preserve observable behavior.

Separate:

- behavior changes
- structural changes

when practical.

## Scope

Prefer focused refactoring over broad rewrites.

Avoid touching unrelated code merely for style consistency.

## Complexity

Reduce complexity where it materially improves understanding or correctness.

Potential signals include:

- deeply nested control flow
- large functions
- duplicated logic
- mixed responsibilities
- hidden side effects
- unclear state transitions
- repeated mapping/validation logic
- excessive branching

Do not optimize for arbitrary complexity numbers without considering readability.

## Responsibilities

Keep distinct responsibilities separate when this improves clarity.

Common separations include:

- validation
- authorization
- orchestration
- persistence
- transformation
- external communication
- presentation

Do not introduce abstractions merely to increase abstraction count.

## Duplication

Remove meaningful duplicated behavior when shared behavior genuinely belongs together.

Some duplication may be preferable to premature coupling.

## Naming

Names should communicate purpose rather than implementation trivia.

Prefer terminology already established by the project.

## Dependencies

Avoid unnecessary dependencies between unrelated modules.

Prefer clear boundaries and explicit data flow.

## Refactoring Safety

Before substantial refactoring:

- identify expected behavior
- identify relevant tests
- understand external interfaces
- preserve public contracts unless intentionally changed

After refactoring:

- run relevant tests
- verify behavior
- check affected integration boundaries

## Framework Adaptation

Follow the architectural conventions already used by the project.

Project evidence or relevant specialist skills may identify framework-native boundaries and patterns.

Do not force a framework pattern where a simpler existing project convention is sufficient.

<!-- ENGINEER_FLOW_ABSORBED_REFACTORING_START -->

## Absorbed Legacy Capability: refactoring

The following framework-agnostic knowledge was preserved from the
previous Engineer Flow capability during consolidation.

# Refactoring

Refactor only to support the task.

- Preserve public behavior.
- Keep changes mechanical when possible.
- Extract helpers only when they reduce real duplication or complexity.
- Prefer clearer names and smaller functions over clever abstractions.
- Back behavior with tests or focused checks.

<!-- ENGINEER_FLOW_ABSORBED_REFACTORING_END -->