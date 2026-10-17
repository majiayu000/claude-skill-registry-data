---
name: derive-test-shape-from-name
description: Given a clear test name, produce given/when/then scaffolding and an assertion structure. Use after derive-test-name-from-behavior to write the actual test body.
---

# Derive a test shape from a name

Given a test name like `should reject empty username with a ValidationError`, produce a Vitest test body with explicit Given/When/Then sections.

## Template

```typescript
it("should <observable behavior>", () => {
  // Given: <setup, no assertions>
  const input = ...;

  // When: <invoke the SUT>
  const result = ...;

  // Then: <assertions>
  expect(result).toBe(...);
});
```

## Rules

1. **Given** sets up state but never asserts.
2. **When** invokes exactly one method or computes one value.
3. **Then** asserts on the result of When. If you have to compute another value to assert on, the test is doing too much.
4. Prefer concrete inputs over fixtures. `expect(validate(""))` beats `expect(validate(emptyInput))` for readability.

## Reusable outside TDD

Used in red phase to scaffold a failing test. Also used by code-review skills to suggest restructuring overly-complex existing tests.
