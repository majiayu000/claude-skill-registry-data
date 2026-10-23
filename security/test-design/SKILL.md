---
name: test-design
description: Design or write reproducible tests matched to behavioral risk before implementation. Use for product behavior; for tooling or infrastructure, use it only when native checks such as linters, validators, dry runs, or plans cannot show the behavior.
---

# Test Design

Own the prospective test contract and test code, not the production implementation or retrospective evidence audit.

## Workflow

1. Confirm that dedicated automated tests are warranted. For tooling or infrastructure, name the native checks that prove the change and stop, unless those checks cannot show behavior that matters.
2. Identify the authoritative contract, condition, action, observable result, invariants, important side effects, assumptions, and state preserved on failure.
3. Choose the lowest test level that proves the contract through a stable public or system boundary.
4. Match the method to the risk: use examples for concrete cases, property or model-based tests for invariants and sequences, fuzzing for broad or hostile input, and systematic concurrency or fault-injection tests for ordering, restart, and recovery. Select only methods that address a material risk.
5. Make every test deterministic: control time, randomness, and concurrency, wait for states instead of sleeping, and avoid real network calls and shared mutable state. Async waits, concurrency, and test-order dependence cause most flaky tests. Make generated or scheduled cases reproducible with a recorded seed, useful bounds, and a minimized counterexample or retained failing input where the tooling supports them.
6. Select only cases that materially define the behavior: one check that fails when the logic breaks, plus a boundary, failure, cleanup, or external-effect case only where the behavior carries that risk.
7. Derive each expected value from the requirement or a small fixed example, never from the logic, constants, or mappings of the code under test. Prefer real implementations, then fakes; stub or mock only dependencies that the system does not own, and assert an interaction only when the interaction is the observable behavior.
8. Follow the repository's existing test structure, helpers, fixtures, and commands.
9. Design test code to the same engineering standard as product code. Reuse existing focused helpers before adding new ones. Extract cohesive repeated setup while keeping scenario inputs and expected results visible. Prefer named table-driven cases when they share one setup, action, and assertion path; use direct tests when they do not.
10. Write the smallest reproducible test whose failure identifies the broken contract. When you write a test, run it against the unfixed code or a deliberate temporary break, and confirm that it fails.
11. State what remains unverified when the behavior cannot be tested economically instead of adding a weak proxy assertion.

Use `technical-spike` when a high-consequence claim may need unfamiliar model checking or proof beyond tests. Use `behavior-implement` for red-green behavior changes, `test-gap-review` for retrospective verification sufficiency, `cli-control` for terminal evidence, and `ui-control` for graphical interface evidence.

Prefer repository-supported tools. Do not change production code, add dependencies, or introduce broad test infrastructure unless the parent task already authorizes it. Report the missing method, expected benefit, and residual risk instead.

Finish with the test boundary, cases, test code when requested, command to run, and any residual gap.
