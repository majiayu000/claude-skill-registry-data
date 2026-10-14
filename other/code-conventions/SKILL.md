---
name: code-conventions
description: "Trigger: writing production code or tests, applying test naming/assert style, extracting constants, placing DTOs or characterization tests. Andres's personal code and test conventions."
license: MIT
metadata:
  author: andresnator
  status: in-progress
  version: "2.0.1"
---

# Code Conventions

## Activation Contract

Load this skill when writing production code or tests. Planners select its name through `implementation-skill-routing`; they do not load this body.

Do not use for documentation, prose artifacts, or infrastructure config with no code.

## Precedence

These conventions are the default for new code and for repos without an established convention. When the target repo already follows a different convention consistently, the repo wins; note the deviation in the plan or summary instead of fighting it.

## Production Code

- **No magic literals**: extract hardcoded numbers and strings into named constants placed where tests can reuse them. Tests reuse constants for fixtures and setup; when the constant itself IS the behavior under test, assert against the expected literal value to avoid tautological tests.
- **Top-level DTOs**: DTOs and helper types are independent top-level classes/files — never inner or nested classes (Java), even when only one private method uses them. In TS, exported types in their own module following the repo layout.
- **Stepdown order (soft)**: code reads top-down like a page; private methods appear in the order they are called. A preference for new or already-touched code, never a reason to churn diffs.
- **Principles that carry weight**: Single Responsibility and Open-Closed. Introduce interfaces or dependency inversion only for real variation, test seams, or architectural boundaries — never as SOLID dogma (consistent with the `dependency-inversion` skill).

## Tests

- **Naming**: `should{Behavior}When{Condition}` or `when{X}Then{Y}`. Never Given-When-Then in the name.
- **Section markers**: every non-trivial test body is visually split with `// Given`, `// When`, `// Then` comments. These delimit phases; they are not explanatory comments.
- **Unified asserts**: fluent single-entry assertions — AssertJ `assertThat` in Java, `expect` in TS.
- **Whole-object asserts**: for complex objects or DTOs with many fields, assert the full object — `usingRecursiveComparison()` or ApprovalTests (Java), `toMatchObject`/`toMatchSnapshot` (Vitest/Jest) — never a cascade of field-by-field asserts. Prefer structured comparison (recursive comparison, `toMatchObject`) over raw snapshots when golden-master fragility hurts.
- **Characterization tests live apart**: place them in a dedicated class/file per unit — `{ClassName}CharacterizationTest` (Java), `<name>.characterization.test.ts` (TS). They are a permanent regression net and never mix with intent-revealing unit tests.

## Plans

Every plan or design document records the detected language and tool versions with evidence (e.g. `java.version` in `pom.xml`, `typescript` in `package.json`) so the implementer can fetch version-correct documentation.

## Output Contract

Code and tests follow the rules above or the repo's winning convention; any deviation from this contract is named explicitly in the plan, design, or summary.

## References

- `assets/examples/OrderServiceTest.java` — Java test with G/W/T sections, `assertThat`, recursive comparison, and a separate characterization class note.
- `assets/examples/order-service.test.ts` — Vitest test with G/W/T sections and `toMatchObject`.
