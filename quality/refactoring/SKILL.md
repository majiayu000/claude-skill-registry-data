---
name: refactoring
description: Identifies and executes code improvements including deduplication, simplification, and naming clarity while maintaining backward compatibility.
---

# Refactoring Skill

When refactoring code, improve internal quality without changing external behavior. Follow these guidelines systematically.

## 1. Identify Code Duplication

- Search for identical or near-identical code blocks across the codebase
- Look for repeated patterns: similar validation logic, error handling, data transformations
- Check for copy-pasted functions with only minor parameter differences
- Identify duplicated business rules that should be centralized
- Use tooling (e.g., jscpd, PMD CPD, or project-specific linters) when available

## 2. Extract Reusable Functions and Components

- Extract duplicated code into shared utility functions or base classes
- Create shared hooks, mixins, or middleware for cross-cutting concerns
- Extract configuration and magic numbers into named constants
- Move shared types and interfaces to a common location
- Ensure extracted functions have clear, single responsibilities
- Prefer pure functions (no side effects) for extracted utilities

## 3. Simplify Complex Logic

- Break down functions longer than 30 lines into smaller, named subfunctions
- Reduce cyclomatic complexity: replace nested conditionals with guard clauses or early returns
- Replace complex boolean expressions with well-named boolean variables or functions
- Simplify state machines by making states and transitions explicit (use enums or state pattern)
- Convert imperative loops to declarative collection operations (map, filter, reduce) where it improves clarity
- Remove dead code, unreachable branches, and commented-out code blocks

## 4. Improve Naming Clarity

- Rename variables and functions to express intent, not implementation
- Replace abbreviations with full words unless the abbreviation is universally understood
- Use domain vocabulary consistently (if the business says "order", do not call it "purchase" in code)
- Boolean variables should read as predicates: `isValid`, `hasAccess`, `shouldRetry`
- Function names should describe what they do: `calculateTotalPrice`, not `process`
- Avoid generic names: `data`, `info`, `result`, `temp`, `handler`, `manager` without qualification

## 5. Improve Code Structure

- Organize code by feature or domain, not by technical layer
- Reduce coupling: minimize dependencies between modules; depend on abstractions, not concretions
- Increase cohesion: keep related data and behavior together
- Apply the Single Responsibility Principle to classes and modules
- Extract interfaces where multiple implementations exist or are anticipated
- Move helper functions closer to their only call site if they are not shared

## 6. Maintain Backward Compatibility

- Do not change public API signatures without a deprecation and migration path
- If renaming a public function, keep the old name as a deprecated alias
- Verify that configuration files, environment variables, and CLI arguments still work
- Run the full test suite after each refactoring step — not just at the end
- Use feature flags if the refactoring must be rolled out incrementally

## 7. Verification Checklist

- All existing tests pass without modification (unless tests were testing implementation details)
- No new warnings from linters or type checkers
- Code coverage has not decreased
- The refactored code is measurably simpler (fewer lines, lower complexity, fewer dependencies)
- Performance has not degraded (run benchmarks for performance-critical paths)
- Review the diff to confirm no accidental behavior changes slipped in

## 8. When NOT to Refactor

- Do not refactor code you do not understand — read it thoroughly first
- Do not refactor in the same PR as a feature change — separate the concerns
- Do not refactor stable, well-tested code for purely aesthetic reasons
- Do not refactor if there are no tests — write tests first, then refactor
- Do not over-abstract: if something is only used once, inline is fine
