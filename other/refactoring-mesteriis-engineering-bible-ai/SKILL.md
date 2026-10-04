---
name: refactoring
description: "Improves structure without behavior changes, using tests and focused slices; not for features unless behavior change is explicit."
---

# Skill: refactoring

## Purpose

Improve structure without changing behavior unless behavior change is explicitly requested.

## Refactoring Rules

- Refactor only when it serves the task.
- Identify behavior that must remain unchanged.
- Prefer small mechanical steps.
- Keep tests green between steps when possible.
- Do not mix broad refactoring with feature changes unless necessary.
- Do not rename public APIs casually.
- Do not move code across architectural boundaries without understanding dependencies.

## When Refactoring Is Justified

Refactoring is justified when it improves:

- correctness;
- maintainability;
- cohesion;
- boundary clarity;
- testability;
- safety;
- removal of duplication of knowledge;
- reduction of large/god files;
- isolation of infrastructure details.

## Large File Refactoring

For large files:

1. Identify responsibilities.
2. Identify public API surface.
3. Identify tests or behavior contracts.
4. Extract cohesive units.
5. Keep imports and dependency direction sane.
6. Validate after each meaningful slice.

Do not split files mechanically by line count. Split by responsibility.

## Safe Extraction Checklist

Before extraction:

- know callers;
- preserve public names or provide compatibility where required;
- avoid circular imports/dependencies;
- keep private helpers private;
- move tests or add tests for extracted behavior;
- preserve errors and logging behavior unless intentionally changed.

## Reporting

Report:

- behavior preserved;
- responsibilities extracted;
- files moved/changed;
- validation;
- risks.
## Extended References


For deeper refactoring work, read:

- `../../engineering/07_complexity_budget.md`
- `../../engineering/08_engineering_smells.md`
- `../../engineering/11_refactoring_catalog.md`
