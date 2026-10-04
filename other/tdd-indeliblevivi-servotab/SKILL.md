---
name: tdd
description: "Apply risk-based test-driven development to bugs, domain logic, state transitions, parsers, contracts, migrations, and behavior where a failing test sharpens the design."
---

# TDD

Use tests as design and evidence. Preserve strict red-green discipline where it pays off, and use lighter verification where the ceremony would add little signal.

## Choose the testing mode

### Strict red-green

Prefer for:

- Bug fixes with a reproducible failure
- Domain rules and calculations
- State machines and mutations
- Parsers, serializers, validators, and data transforms
- API contracts and compatibility behavior
- Migrations
- Concurrency or race-condition fixes
- Security-sensitive behavior

Cycle:

1. Write the smallest behavior-focused test.
2. Execute it once and verify that the failure matches the intended behavioral gap.
3. Implement the minimum coherent change.
4. Run the focused test and confirm it passes.
5. Refactor while keeping it green.
6. Run nearby tests.

### Characterization-first

Use for legacy code whose behavior is poorly documented.

1. Add tests that capture relevant current behavior.
2. Add a failing test for the behavior that must change.
3. Implement the change.
4. Keep unrelated characterized behavior stable.

### Test-alongside

Reasonable for:

- Pure styling and visual polish
- Copy changes
- Simple configuration or wiring
- Generated files
- Small adapters already covered by higher-level tests
- Prototypes or short-lived spikes

Use the most meaningful existing checks. Add automated tests when there is a real regression surface, not to satisfy a quota.

## Existing implementation

Do not delete valid work merely because implementation preceded the test.

When code already exists:

- Reproduce the bug against the current code.
- Add a test that fails on the current behavior when possible.
- If the fix has already been applied, temporarily revert or mutate the narrow change only when safe and efficient to prove the test catches it.
- Otherwise document why red-state proof was impractical and use strong behavior verification.

## Test quality

Prefer tests that:

- Assert externally meaningful behavior
- Fail for one understandable reason
- Are deterministic
- Use real code through stable boundaries
- Survive internal refactoring
- Cover important edge and error paths
- For optional host capabilities, distinguish absence (no doomed action plus useful degradation), rejection, cancellation, policy denial, and success when those are separate observable results

Avoid:

- One test for every trivial function
- Snapshot tests that hide semantic changes
- Mocking the unit under test
- Asserting private implementation details
- Huge fixtures when a focused case works
- Adding sleeps for asynchronous behavior when a condition can be awaited

## Mocks and fakes

Use real collaborators when cheap and deterministic. Mock or fake:

- Network boundaries
- Time
- Randomness
- External services
- Slow or destructive infrastructure

Keep mocks at stable interfaces. If every internal call must be mocked, reconsider coupling.

## Regression proof

For a bug fix, the ideal evidence is:

- Test fails before fix for the expected reason
- Test passes after fix
- Nearby suite remains green

Do not perform risky repository surgery merely to reenact red-green after the fact. Evidence should increase confidence, not damage the workspace.

## Completion checklist

Before claiming test-backed behavior:

- The test targets the requested behavior.
- Failure and success reasons are understood.
- Important boundary cases are represented.
- Focused tests pass after the final relevant change.
- Broader checks were run when risk justifies them.
- Any untested area is stated honestly.
