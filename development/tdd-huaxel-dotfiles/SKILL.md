---
name: tdd
description: Develop features or fix bugs test-first using red-green-refactor. Use when the user asks for TDD, test-first work, or a regression test before a fix. Not for every integration-test request, test review, or mutation campaign.
---

# Test-Driven Development

Build one behavior at a time through a failing test, a minimal implementation, and a behavior-preserving refactor. Preserve existing work; never delete implementation merely because it predates a test.

## Choose the boundary

Inspect applicable project guidance, relevant architecture decisions, and existing tests. Infer the stable public boundary and test framework from the task and code. State the boundary briefly and proceed; ask only when a consequential interface or requirement decision cannot be inferred safely.

Test behavior callers rely on, not incidental implementation. A useful boundary may be a function, CLI, API, UI, persistent effect, or integration with another component. Prefer the narrowest test that can falsify the intended contract; use integration tests when the interaction itself matters.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for isolation guidance. No companion plugin or separate approval ceremony is required.

## Red → green → refactor

1. **Red:** Write one test for the next behavior or reported defect. Run it and confirm it fails for the intended reason—not a broken import, missing service, or unrelated baseline failure. For a regression, retain a concrete reproducer.
2. **Green:** Make the smallest causal change that satisfies that behavior. Run the focused test and relevant existing checks. Do not add speculative features or unrelated refactors.
3. **Refactor:** With tests green, improve structure where useful without changing the contract. Rerun affected tests. Refactoring is part of the loop, not a reason to postpone verification.
4. Repeat for the next behavior, using what the previous slice taught you. Do not write an entire speculative suite against an imagined design before validating the first slice.

For an already implemented feature, add characterization or regression tests as appropriate and describe the evidence honestly. If no pre-fix failure was demonstrated, do not claim a completed red-green cycle.

## Keep tests meaningful

- Derive expected results from an independent example, specification, or oracle—not a copy of the implementation.
- Assert the relevant observable outcomes. Several assertions may describe one coherent behavior; arbitrary assertion counts are not the objective.
- Isolate external effects and unstable dependencies at meaningful boundaries. Avoid mocks that merely verify internal call order or mirror class structure.
- Preserve unrelated parallel changes and use isolated test state. Do not stash, reset, or clean others’ work to manufacture a baseline.
- Use property-based-testing when meaningful invariants need generated inputs; mutation-testing remains a separate explicit opt-in.

Finish with behavior covered, red/green observations actually obtained, commands run, and any remaining verification gaps. Run the project gate when available.
