---
name: behavior-implement
description: Implement one observable behavior or bug fix with red-green-refactor, writing a focused test that fails first, the minimum code that passes it, and then a behavior-preserving cleanup. Use for product behavior changes; for tooling or infrastructure, use it only when native checks such as linters, validators, dry runs, or plans cannot show the behavior.
---

# Test-Driven Implementation

Implement one coherent observable behavior and prove it with a test that failed before the change and passes after it.

## Workflow

1. Read the behavior contract, the repository instructions, the closest implementation and test patterns, and the callers of the code you will change.
2. For tooling or infrastructure, prove the change with the native checks and skip the red test, unless those checks cannot show behavior that matters.
3. Define the observable result, the side effects, and the state that must stay unchanged on failure. Rely only on the documented behavior of dependencies.
4. Choose the smallest mechanism, and stop at the first option that works: no change, existing code, the standard library or platform, an installed dependency, or one clear line. Never drop validation, data-loss prevention, security, accessibility, or an explicit requirement to make the change smaller. If the contract needs much more scope than expected, explain the gap and ask for direction instead of building an approximation.
5. Use `test-design` when the test level, cases, or fixtures are not obvious. Otherwise extend the existing test pattern.
6. Write the smallest focused test in the repository's style, with the scenario values visible. Run it and confirm that it fails because the behavior is missing or wrong, not because of a setup, import, or compile error.
7. Write the minimum production code that makes the test pass.
8. For several cases, repeat steps 6 and 7 one case at a time.
9. Refactor only where the new code needs it for clarity. Run the tests after each refactoring step.
10. Run the surrounding tests and the checks that the repository requires. Use `crap-index-assess` when the user asks for it or the repository's CRAP check covers the changed methods.

Never edit the new test or an existing test to make it pass. If a test seems wrong or the contract seems impossible, stop and explain why.

If a test is impractical for an in-scope behavior, say why before you edit, name the evidence that will replace it, and state the remaining risk. Do not build a test harness that grows the scope. Do not use this workflow for documentation, formatting, metadata, or generated-state changes that do not change behavior.

## Result

Finish when the behavior passes a test that you saw fail first, or the exception is evidenced, and the regression checks pass. Report the failing run, the passing run, and the checks you ran.
