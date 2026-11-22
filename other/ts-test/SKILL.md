---
name: ts-test
description: >
  TypeScript/Node.js test rules using Vitest (runner config, file naming, mocking,
  coverage). Use when writing or running tests in a TypeScript or Node.js project.
---

## Prerequisites

- Project root with `vitest.config.ts`

## Test Runner

- **Framework**: Vitest (`globals: true`, `environment: node`)
- **Config**: `vitest.config.ts` at project root
- **Run all**: `<pm> test` (package manager from `detect-techstack`)
- **Run single file**: `npx vitest run <path>`
- **Targeted run** (per commit): `npx vitest run <path> <path>`; unknown mapping: the project's fast script (e.g. `<pm> run test:unit`)

### File Naming

- Unit tests: `*.test.ts`, co-located with the source file
- Integration / E2E: by suffix, `*.int.test.ts` or `*.e2e.test.ts`

### Coverage

```powershell
npx vitest run --coverage
```

- Requires `@vitest/coverage-v8` as a devDependency (`ts-create-project` adds it and the `test:ci` script)
- Output: `coverage/` directory; CI publishes `cobertura-coverage.xml`

### Mocking

- Function-level: `vi.fn()`
- Module-level: `vi.mock("module-path")` — only when unavoidable; avoid when inline mocking suffices
- Reset mocks in `beforeEach` (`vi.clearAllMocks()`) so tests stay isolated

## Gotchas

- Tests must be hermetic — no network calls, no shared state
- Use `vi.useFakeTimers()` for timer-dependent code
- Coverage threshold may be enforced in CI
- Assert directly in test methods, no test logic in helpers; prefer specific assertions
- No debug code or `console.log` in committed tests
