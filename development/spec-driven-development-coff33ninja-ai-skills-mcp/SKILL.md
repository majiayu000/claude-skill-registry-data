---
name: spec-driven-development
description: Forces writing a specification before any code changes. Defines goals, inputs/outputs, constraints, edge cases, and acceptance criteria before implementation. Use when starting any non-trivial feature, refactor, or bug fix. Prevents solving the wrong problem.
---

# Spec-Driven Development

## Problem it solves

The most common failure mode in AI-assisted development is jumping straight to implementation. The agent hears a request and starts writing code before understanding what "done" looks like. This causes:
- Solving the wrong problem (implementing what was asked, not what was needed)
- Scope creep (adding features not in scope because there was no scope)
- Wasted tokens on discarded implementations
- Rework cycles that could have been avoided with 30 seconds of planning
- Unclear acceptance criteria — neither the user nor the agent knows when it's done

## Protocol

### 1. Detect the trigger

When asked to implement, fix, refactor, or add anything non-trivial, do NOT start coding. Instead, pause and write a spec.

Trivial means: a single-file change with obvious intent and no ambiguity. Everything else needs a spec.

### 2. Write the spec

Create a concise specification covering:

```markdown
## Goal
One sentence: what should be true when this is done?

## Scope
- **In scope**: what changes are made
- **Out of scope**: what is explicitly NOT changing

## Interface / Contract
- Inputs: what the code receives
- Outputs: what the code produces
- Error states: what happens when things go wrong

## Constraints
- Performance targets (if any)
- Compatibility requirements
- Security considerations
- Existing patterns to follow

## Edge Cases
- Empty/null inputs
- Boundary values
- Concurrent access
- Unhappy paths

## Acceptance Criteria
Checklist of concrete, testable items. Each must be verifiable:
- [ ] Criterion 1
- [ ] Criterion 2
```

Keep the spec short — 10-20 lines for most tasks. Only expand for complex features.

### 3. Confirm with the user

Present the spec and ask:
- "Does this match what you want?"
- "Is anything missing or wrong?"

Do not proceed to implementation until the user confirms or corrects the spec.

If the user says "just do it, no spec needed", skip to implementation but note the risk.

### 4. Implement against the spec

During implementation:
- Refer back to the spec at each step — am I still building what was agreed?
- If you discover something the spec missed, pause and ask, don't silently expand scope
- If the spec says something is out of scope, do not implement it

### 5. Verify against acceptance criteria

Before declaring done:
- Walk through each acceptance criterion
- Show evidence (test output, file content, command result)
- If any criterion is not met, do not declare done

## Detection triggers

Activate when:
- User asks to build a new feature or component
- User asks to refactor existing code
- User reports a bug (write a spec for the fix)
- User gives a vague or multi-step request
- Starting work on any task with more than one file change

## When NOT to use

- Single-line or trivial changes (typo fix, rename, one-liner)
- User explicitly says "no spec, just do it"
- Exploratory or research tasks where the goal is to learn, not to produce
- Rapid prototyping where the spec is the code

## Cross-references

- **requirements-clarify** — Use before the spec to gather requirements when the request is ambiguous. Spec-driven-development formalizes what requirements-clarify uncovers.

- **anti-premature-termination** — Acceptance criteria in the spec serve as completion criteria. Do not declare done until all criteria are verified.

- **follow-existing-patterns** — The spec should reference which existing code patterns the implementation will follow.

- **test-driven-development** — TDD is the natural next step after the spec is written. The spec defines what the tests should cover.

- **code-review** — The spec is the review baseline. Review checks if the implementation matches the spec.
