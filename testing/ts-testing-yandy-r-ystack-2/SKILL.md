---
name: ts-testing
description: Guides TypeScript testing with Vitest and TDD. Use when adding TypeScript
  test coverage, mocking async behavior, or writing property and type-level tests.
---

# TypeScript Testing Patterns

Comprehensive TypeScript testing patterns for writing reliable, maintainable tests
using **Vitest** as the primary runner, following TDD methodology. Vitest pairs with
Vite (same team, shared config) so the transform pipeline used in development is the
same one used in tests — no duplicated build configuration.

## When to Use

- Writing new TypeScript functions, classes, or modules
- Adding test coverage to existing TypeScript code
- Creating benchmarks for performance-sensitive code
- Implementing property-based tests for input validation
- Writing type-level tests for library APIs
- Following TDD workflow in a TypeScript project

## How It Works

1. **Identify target code** — find the function, class, or module to test.
2. **Write a test** — use `describe` / `it` / `expect` in a colocated `*.test.ts`
   file (or `tests/` dir for integration tests).
3. **Mock external dependencies** — prefer dependency injection; fall back to
   `vi.mock()` for modules you can't control.
4. **Run tests (RED)** — confirm the test fails for the expected reason.
5. **Implement (GREEN)** — write the minimum code needed to pass.
6. **Refactor** — clean up while keeping tests green.
7. **Check coverage** — `vitest --coverage`, target 80%+.

## Critical Rules

- Vitest for unit and integration tests; Playwright only for real-browser E2E.
- Prefer dependency injection over `vi.mock()` when you control the seams.
- Use `vi.useFakeTimers()` instead of real `setTimeout`.
- Clear mocks between tests: `beforeEach(() => vi.clearAllMocks())`.
- Strict typing in tests — same `tsconfig` strict settings as source; no `any`.
- Type-level tests (`expectTypeOf`) for libraries with public type guarantees.

## References

Paths are relative to this SKILL.md's directory. Read only the file that matches the task. If a file cannot be read, say so.

- [references/vitest-core.md](references/vitest-core.md)
  Read when: TDD workflow; unit tests; assertions; error and rejection testing; integration tests; async tests and fake timers (`vi.useFakeTimers`).

- [references/advanced-testing.md](references/advanced-testing.md)
  Read when: parameterized tests with `test.each`; property-based testing with fast-check; mocking (`vi.mock`, `vi.fn`, `vi.spyOn`) and dependency injection; type-level testing with `expectTypeOf`; benchmarks; CI integration; alternatives to Vitest.

## Test Coverage

### Running Coverage

```bash
# Vitest's v8 provider is built in — no extra deps
vitest run --coverage
```

```ts
// vitest.config.ts — coverage config
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
      exclude: ['**/*.d.ts', '**/*.config.ts', 'tests/**', 'dist/**', 'src/**/*.bench.ts'],
    },
  },
});
```

### Coverage Targets

| Code type                | Target  |
| ------------------------ | ------- |
| Critical business logic  | 100%    |
| Public library API       | 90%+    |
| General application code | 80%+    |
| Generated / binding code | Exclude |

## Testing Commands

```bash
# Watch mode (default when running vitest interactively)
vitest

# Run once and exit (use in CI)
vitest run

# Run files/tests matching a pattern
vitest user                  # files matching "user"
vitest -t "valid email"      # test names matching "valid email"

# Coverage
vitest run --coverage

# Change the reporter
vitest run --reporter=verbose
vitest run --reporter=dot

# Benchmark mode
vitest bench

# Browser-based UI explorer
vitest --ui

# Type-check tests alongside runtime tests
vitest --typecheck

# Force single-thread (useful for debugging shared state)
vitest --poolOptions.threads.singleThread=true

# Run only changed files
vitest --changed
```

## Best Practices

**DO:**

- Write tests FIRST (TDD)
- Colocate unit tests with source (`foo.ts` + `foo.test.ts`)
- Keep integration tests in `tests/` with a `setupFiles` entry
- Test behavior, not implementation detail
- Use `describe` to group related tests; `it` / `test` for individual cases
- Prefer `toEqual` for objects and arrays, `toBe` for primitives
- Use `test.each` to eliminate duplication across input sets
- Inject dependencies so tests don't need `vi.mock()`
- Reset mocks between tests (`beforeEach(() => vi.clearAllMocks())`)
- Run tests under the same `tsconfig` strict settings as source

**DON'T:**

- Use `any` in test code — strict-mode rules still apply
- Use real `setTimeout` in tests — use `vi.useFakeTimers()`
- Reach for `vi.mock()` when dependency injection would work
- Test third-party libraries (trust their tests; test your integration with them)
- Ignore flaky tests — fix them or quarantine with `it.skip` and a tracking comment
- Share mutable state between tests — each test must be independent
