---
name: design-patterns-pragmatic
description: "Trigger: design patterns, GoF patterns, Java patterns, strategy, adapter, factory, builder, decorator, observer. Choose patterns only when they solve real design forces."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "1.1.0"
---

# Skill: design-patterns-pragmatic

## Activation Contract

Use this skill when asked whether to use a design pattern, how to apply a pattern, or how to compare pattern-based alternatives. Examples include Strategy, Factory, Builder, Adapter, Decorator, Template Method, Observer, Command, Repository, and Specification.

Do **not** use this skill to add patterns for decoration, replace simple code without a change pressure, or perform full architecture design unrelated to a specific pattern choice.

## Responsibility

This skill teaches pragmatic pattern selection and application. It does not call other skills, force GoF terminology, or choose complexity without tradeoff justification.

## Required Context

- Current problem and change pressure.
- Existing code shape or intended collaboration.
- Language and framework constraints.
- Expected variants, extension points, or integration boundaries.

## Context Budget

- Keep this `SKILL.md` focused on selection workflow.
- Use `references/pattern-selection.md` for the pattern decision table.

## Hard Rules

- Start from the design force, not the pattern name.
- Prefer no pattern when simple code is clearer.
- Introduce indirection only when it reduces real change cost.
- Name the cost: extra types, navigation, testing surface, and cognitive load.
- Check the candidate pattern's contraindications (`references/pattern-forces.md`) before recommending it.
- Patterns belong to the consolidation phase of a design, not the prototyping phase: recommend one when variation is proven, not anticipated.
- For Java, consider lambdas, records, sealed classes, and composition before classic boilerplate-heavy patterns.

## Decision Gates

| Condition | Action |
|---|---|
| Behavior varies behind one operation | Consider Strategy. |
| External API shape does not match local model | Consider Adapter. |
| Object construction is complex with meaningful optional parts | Consider Builder. |
| Creation logic must vary by family/type | Consider Factory. |
| Feature wraps another object transparently | Consider Decorator. |
| Algorithm skeleton is stable but steps vary | Consider Template Method, but check inheritance cost. |
| Simple branch is enough | Do not introduce a pattern yet. |

## Execution Steps

1. State the design force and expected variation.
2. Compare simple code vs candidate pattern.
3. Choose the smallest pattern shape that solves the force.
4. Explain tradeoffs and rejected alternatives.
5. Provide a minimal sketch when useful.

## Output Contract

Return:

- Pattern verdict: `no_pattern`, `pattern_candidate`, or `pattern_recommended`.
- Design force.
- Chosen pattern or simpler alternative.
- Tradeoffs.
- Minimal implementation sketch or next step.

## References

- `references/pattern-selection.md` — Pattern selection and tradeoff table.
- `references/pattern-forces.md` — Redesign causes → candidate patterns, per-pattern contraindications, and pattern relations/combinations.

## Assets

- None.
