---
name: setup-vitest
description: Set up Vitest for a TypeScript project, or migrate from Jest. Use for faster test execution, native ESM/TypeScript support, and Jest-compatible API. Covers config, dependency swaps, and test file updates.
---

# Set Up Vitest

## Goal

Add Vitest for fast test execution with native ESM and TypeScript support. If migrating from Jest, replace Jest + ts-jest with minimal code changes.

## Why

- Native ESM support (no ts-jest transform overhead)
- Native TypeScript support (no configuration needed)
- 2-5x faster test execution for ESM TypeScript projects
- Jest-compatible API (minimal code changes when migrating)

## Steps

### 1. Install Vitest

```bash
pnpm add -D vitest
```

### 2. Create vitest.config.ts

```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    include: ['src/**/*.test.ts'],
  },
})
```

### 3. Update package.json Scripts

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest"
  }
}
```

### 4. Remove Jest (if migrating)

```bash
pnpm remove jest ts-jest @types/jest
```

Also delete `jest.config.*` if it exists.

### 5. Update Test Files (if migrating from Jest)

With `globals: true`, most Jest tests work unchanged. Key differences:

**Mock changes (find and replace):**

```ts
// jest.fn → vi.fn
// jest.mock → vi.mock
// jest.spyOn → vi.spyOn
// jest.clearAllMocks → vi.clearAllMocks
// jest.resetAllMocks → vi.resetAllMocks
// jest.restoreAllMocks → vi.restoreAllMocks
// jest.useFakeTimers → vi.useFakeTimers
```

**Imports (if not using globals):**

```ts
import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest'
```

### 6. TypeScript Config

Add vitest types if using globals:

```json
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

Or create a separate `tsconfig.test.json` that extends the main one.

### 7. Verify

```bash
pnpm test           # All tests pass
pnpm test:watch     # Watch mode works
```

## Gotchas

- Vitest uses esbuild for transforms (fast but no type-checking during tests — use `tsc --noEmit` separately)
- Snapshot files are compatible (`.snap` extension, same as Jest)
- If Jest config uses `moduleNameMapper`, use `resolve.alias` in vitest config instead
