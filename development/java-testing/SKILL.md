---
name: java-testing
description: "Trigger: Java tests, JUnit, Mockito, AssertJ, legacy code, characterization tests, seams. Generate and retrofit Java tests safely."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "3.2.1"
---

# Java Testing Skill

## Activation Contract

Use this skill for Java tests: unit tests, JUnit/Mockito/AssertJ examples, characterization tests, Golden Master tests, seams, or dependency-breaking.

Do not use for non-Java projects, generic strategy, frontend/E2E, performance, security, or refactoring without a testing objective.

## Responsibility

Own Java test workflow: detect the local stack, choose the smallest safe technique, create or propose tests, and explain seam/dependency tradeoffs. The caller owns product behavior, dependency approval, and running project commands when validation exists.

## Required Context

Before writing tests, inspect or ask for:

- Java version, build tool, and test dependencies.
- Existing test naming, package layout, assertions, fixtures, and mocking style.
- Class under test, observable behavior, collaborators, and failure/edge cases.
- For legacy code: change point, test point, hidden dependencies, and whether the seam is for Sensing or Separation.

## Hard Rules

- Detect Java level, build tool, JUnit/Mockito versions, assertion style, and dependency management independently.
- Preserve the project test stack unless a dependency change is explicitly needed and justified.
- Prefer the simplest useful test: pure unit test first, Mockito only across real boundaries, Spring/context tests only when the framework behavior is the subject.
- For clean code, test behavior and avoid over-verifying collaborators.
- For existing untested or hard-to-test code, use Cover → Modify → Refactor: characterize current behavior before changing it.
- When breaking dependencies, name whether the seam is for Sensing or Separation.
- Generated examples must be complete, compilable, and match local package, naming, and style conventions.
- Do not add or upgrade JUnit, Mockito, AssertJ, PowerMock, or ApprovalTests unless the existing stack cannot support the required test and the tradeoff is stated.
- Do not modify production behavior before a safety test exists for legacy code.

## Decision Gates

| Situation | Route |
|---|---|
| Clean, injectable class needs tests | Use Simple Unit Tests below. |
| Existing code has no tests but is easy to instantiate | Write characterization tests first, then improve. |
| Constructor/static/global/framework dependencies block testing | Use `references/quick-decision-flow.md` and dependency-breaking references. |
| Dependency setup is missing or unclear | Read `references/dependency-setup.md` before adding imports or build snippets. |
| Golden Master or ApprovalTests is needed | Read `references/characterization-tests.md`, then `references/approvaltests-setup.md` before creating baselines. |
| Static/final mocking or captors are needed | Read `references/mockito-patterns.md` before choosing Mockito features. |
| Large legacy cluster or unclear effect propagation | Read `references/advanced-patterns.md` for pinch points, effect sketches, and hot spots. |

## Execution Steps

1. Detect local Java test stack and conventions.
2. Identify behavior and smallest observable test point.
3. Select a route; load only the referenced file needed.
4. For legacy code, characterize current behavior before production changes.
5. Write focused tests matching local style; avoid over-mocking.
6. State seam/dependency tradeoffs, including Sensing vs Separation.
7. Report validation performed or command to run.

## Simple Unit Tests

- Follow the `code-conventions` skill as the general contract; the rules below are its Java specifics.
- Place tests under `src/test/java/` mirroring the source package.
- Name classes `{ClassName}Test` and methods `should{Behavior}When{Condition}` unless the project already uses another convention.
- Split every non-trivial test body with `// Given`, `// When`, `// Then` section markers; avoid other comments/Javadocs.
- For JUnit 5 + Mockito, use `@ExtendWith(MockitoExtension.class)`, `@Mock`, and `@InjectMocks` only when constructor setup adds noise.
- Prefer AssertJ `assertThat()` / `assertThatThrownBy()` when already present; `WithAssertions` is acceptable if it matches project style.
- For complex objects/DTOs, assert the whole object with `usingRecursiveComparison()` or ApprovalTests instead of field-by-field cascades.
- Use parameterized tests for meaningful input matrices, and `ArgumentCaptor` only when the passed object is the behavior under test.

## Legacy Testing Flow

1. Identify change points.
2. Find test points with effect sketches.
3. Break dependencies only where needed for Sensing or Separation.
4. Write characterization tests that document what the code does now, in a dedicated permanent `{ClassName}CharacterizationTest` class separate from intent-revealing unit tests.
5. Modify and refactor behind the safety net.

## References

Load progressively; do not read the full catalog by default.
Use `references/` to understand when and why to apply a technique. Use `assets/examples/` only as copyable starting points: adapt package names, dependencies, naming, and project conventions before committing.

| Reference | Load when |
|---|---|
| `references/dependency-setup.md` | Dependency setup or version compatibility is unclear. |
| `references/mockito-patterns.md` | Mockito annotations, captors, verification, static/final mocking, or interaction boundaries are needed. |
| `references/characterization-tests.md` | Existing behavior must be locked before modification, including Golden Master tests. |
| `references/approvaltests-setup.md` | ApprovalTests setup or baseline workflow is needed. |
| `references/seam-model.md` | Seams and enabling points must be classified before breaking dependencies. |
| `references/dependency-breaking.md` | Constructor, interface, override, parameter adaptation, or global-reference techniques are needed. |
| `references/quick-decision-flow.md` | The code is hard to test and you need a first route. |
| `references/sensing-separation.md` | Decide whether the seam observes behavior or separates dependencies. |
| `references/pass-null-subclass-override.md` | Pass Null, null object, subclass-and-override, or extract-and-override is the likely seam. |
| `references/sprout-wrap-techniques.md` | Risky legacy additions call for Sprout Method/Class or Wrap Method/Class. |
| `references/method-object-skin-wrap.md` | Long methods, API skin wrapping, or method-object extraction is needed. |
| `references/tdd-legacy.md` | The task asks for TDD while modifying existing legacy Java. |
| `references/advanced-patterns.md` | Pinch points, effect sketches, God classes, hot spots, or scratch refactoring are needed. |
| `assets/examples/ExampleServiceTest.java` | Service test template with JUnit 5, Mockito, and AssertJ. |
| `assets/examples/ExampleConfigTest.java` | Configuration/value-object style example. |
| `assets/examples/ExampleHandlerTest.java` | Handler/controller collaborator example. |
| `assets/examples/ExampleCacheTest.java` | Cache/stateful behavior example. |
| `assets/examples/ExampleListenerTest.java` | Listener/event-driven example. |

## Output Contract

Return:

- Chosen route and references used.
- Detected Java test stack and conventions.
- Files changed or proposed.
- Tests added, including behaviors and edge cases covered.
- Dependency/seam tradeoffs, including Sensing vs Separation when applicable.
- Validation performed or recommended command.
