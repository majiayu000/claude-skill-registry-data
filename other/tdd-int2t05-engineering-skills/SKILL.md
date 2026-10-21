---
name: tdd
description: Implement behavior through a focused red-green-refactor loop. Triggers on "tdd", "测试驱动开发".
---

# Test-Driven Development

## When to use

- Implement behavior through a focused red-green-refactor loop.

**Not for:** implement for planned delivery; test-generation for existing behavior.

## Steps

1. Find real commands, layout and public seam; use real code and controlled data, disclosing external substitutes.

2. Write one behavior test, run it and confirm failure from missing or incorrect behavior rather than harness errors.

3. Implement minimally, run the focused test and relevant regressions, and refactor while green.

4. Repeat for the next behavior and finish relevant verification; report observed red/green evidence and commit only on request.

## Verify

- A meaningful failure preceded the passing fix; assertions use independent expected behavior and checks are not disabled.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/test-strategy.md](references/test-strategy.md) — test pyramid, test-double hierarchy (Real > Fake > Stub > Mock), DAMP over DRY
- [references/testing-anti-patterns.md](references/testing-anti-patterns.md) — mock misuse, test-only methods, partial mocks, gate functions
- [references/mocking.md](references/mocking.md) — when to mock, designing for mockability
- [references/good-tests.md](references/good-tests.md) — good vs bad test examples, tautological tests
