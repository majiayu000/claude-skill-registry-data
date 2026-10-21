---
name: test-generation
description: Add meaningful tests for existing behavior with actual project tooling. Triggers on "generate tests", "生成测试".
---

# Test Generation (Language-Agnostic)

## When to use

- Add meaningful tests for existing behavior with actual project tooling.

**Not for:** tdd for test-first changes; e2e-testing for journeys.

## Steps

1. Read the contract, public interface and tests; identify genuine gaps.

2. Build a compact normal, boundary, error and relevant state or concurrency matrix.

3. Use project layout, isolated data and independently derived expectations; label substitutes separately from integration.

4. Run cases and affected regressions and verify they detect the intended defect or missing behavior.

## Verify

- Tests exercise actual behavior reproducibly and detect meaningful failures rather than mirroring implementation.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [clean-code.md](../../../references/clean-code.md) — clean code principles for test quality
- [references/language-patterns.md](references/language-patterns.md) — per-language Test Framework | Assertion Style | Mock Library mapping
