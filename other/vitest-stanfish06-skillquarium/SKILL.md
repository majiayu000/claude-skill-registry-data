---
name: vitest
description: JavaScript/TypeScript unit testing with Vitest — fast Vite-native test runner with Jest-compatible API. Use when writing or running tests in a Vite-based project (React, Vue, Svelte, vanilla TS/JS), migrating from Jest, benchmarking code, testing browser APIs with jsdom/happy-dom, or needing in-source testing. Native ES modules, TypeScript, and JSX support with zero config. Pairs with test-driven-development for the methodology.
---

# Vitest — Fast Vite-Native Testing

## Overview

Vitest is a blazing-fast JavaScript/TypeScript test runner powered by Vite. It shares Vite's configuration and plugin pipeline, supports ES modules natively, and has a Jest-compatible API — migrate from Jest with minimal changes. This skill is the **tool reference**; for the red-green-refactor *methodology* see [[test-driven-development]].

## Installation

```bash
# Vite project
npm install --save-dev vitest

# With UI dashboard
npm install --save-dev @vitest/ui

# Browser mode (v4: also install the provider package — see Browser Mode section)
npm install --save-dev @vitest/browser @vitest/browser-playwright

# Coverage (required for `vitest run --coverage`)
npm install --save-dev @vitest/coverage-v8
```

Add to `package.json`:
```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage"
  }
}
```

## Configuration

```ts
// vite.config.ts — add test block to existing Vite config
import { defineConfig } from 'vite';

export default defineConfig({
  test: {
    globals: true,              // no need to import describe/it/expect
    environment: 'jsdom',       // or 'happy-dom', 'node', 'edge-runtime'
    setupFiles: ['./src/test-setup.ts'],
    coverage: {
      provider: 'v8',           // or 'istanbul'
      reporter: ['text', 'html'],
      thresholds: { lines: 80 },
    },
  },
});
```

Or a standalone `vitest.config.ts`:
```ts
import { defineConfig } from 'vitest/config';
export default defineConfig({ test: { globals: true } });
```

## Running Tests

```bash
vitest               # watch mode (default)
vitest run           # single run (CI)
vitest --ui          # browser UI dashboard
vitest --coverage    # with coverage report
vitest src/utils     # filter by path
vitest -t "user"     # filter by test name
vitest bench         # run benchmarks
```

## Test Structure (Jest-compatible API)

```ts
// utils.test.ts — files *.test.ts or *.spec.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { add, createUser } from './utils';

describe('add', () => {
  it('adds two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });
});

describe('createUser', () => {
  it('creates a user with default role', () => {
    const user = createUser('Alice');
    expect(user).toEqual({ name: 'Alice', role: 'user' });
  });
});
```

With `globals: true` in config, you can omit imports:
```ts
// No import needed
test('works without imports', () => {
  expect(1 + 1).toBe(2);
});
```

## Mocking

```ts
import { vi } from 'vitest';

// Mock a module
vi.mock('./api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: 1, name: 'Alice' }),
}));

// Spy on an object method
const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
// ...
expect(spy).toHaveBeenCalledWith('expected warning');
spy.mockRestore();

// Fake timers
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.useRealTimers();

// Mock environment variables
vi.stubEnv('NODE_ENV', 'test');
vi.unstubAllEnvs(); // cleanup

// Mock global objects
vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ json: () => ({ ok: true }) }));
```

## Async Tests

```ts
it('fetches data', async () => {
  const data = await fetchData();
  expect(data).toMatchObject({ status: 'ok' });
});

// Expect a promise to resolve/reject
await expect(fetchUser(1)).resolves.toHaveProperty('name');
await expect(fetchUser(-1)).rejects.toThrow('Not found');
```

## Snapshot Testing

```ts
import { renderToString } from 'react-dom/server';

it('matches snapshot', () => {
  const result = renderToString(<Component />);
  expect(result).toMatchSnapshot();
});

// Inline snapshots (stored in the test file)
expect(add(1, 2)).toMatchInlineSnapshot('3');
```

Update snapshots: `vitest -u` or `vitest --update-snapshots`

## In-Source Testing

Vitest supports placing tests directly inside source files:
```ts
// src/utils.ts
export function add(a: number, b: number) { return a + b; }

// Only active during test runs
if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest;
  it('adds', () => expect(add(1, 2)).toBe(3));
}
```

Enable in config: `test: { includeSource: ['src/**/*.ts'] }`. For production builds you must
also strip the test block so it never ships — define `import.meta.vitest` as `undefined` so
the bundler can dead-code-eliminate it:
```ts
// vite.config.ts
export default defineConfig({
  define: { 'import.meta.vitest': 'undefined' },
});
```

## Benchmarks

```ts
import { bench, describe } from 'vitest';

describe('sort algorithms', () => {
  bench('native sort', () => {
    [3, 1, 2].sort();
  });

  bench('custom sort', () => {
    customSort([3, 1, 2]);
  });
});
```

Run: `vitest bench`

## Browser Mode (Real Browser Testing)

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config';
// v4: provider is an imported factory, not a string — install the matching
// package, e.g. `npm i -D @vitest/browser-playwright` (or @vitest/browser-webdriverio)
import { playwright } from '@vitest/browser-playwright';

export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: playwright(),
      // `browser.name` was deprecated in v3 and removed in v4 — use `instances`
      instances: [
        { browser: 'chromium' },
      ],
    },
  },
});
```

## Migrating from Jest

Vitest's API is intentionally Jest-compatible. Key differences:
- Replace `jest` global with `vi` (`jest.fn()` → `vi.fn()`, `jest.mock()` → `vi.mock()`)
- `jest.useFakeTimers()` → `vi.useFakeTimers()`
- `jest.spyOn()` → `vi.spyOn()`
- Import from `'vitest'` instead of `@jest/globals`
- Remove `jest.config.*` and add `test:{}` to `vite.config.ts`

```bash
# Quick migration: find all jest. usages
grep -r "jest\." src --include="*.test.*"
# Replace: jest.fn → vi.fn, jest.mock → vi.mock, jest.spyOn → vi.spyOn
```

## Coverage

```bash
vitest run --coverage
# HTML report: coverage/index.html
```

```ts
// vitest.config.ts
test: {
  coverage: {
    provider: 'v8',
    include: ['src/**/*.ts'],
    exclude: ['src/**/*.d.ts', 'src/test-*'],
    thresholds: { statements: 80, branches: 70, lines: 80 },
  },
}
```

## Type Checking

Vitest doesn't type-check by default (Vite strips types). Use alongside:
```bash
tsc --noEmit    # type check without emitting
# or: vue-tsc, svelte-check, etc.
```

## Related Skills

- [[test-driven-development]] — TDD methodology and workflow
- [[jest]] — Jest testing (for non-Vite projects)
- [[playwright-best-practices]] — End-to-end browser testing
- [[playwright-cli]] — Browser automation from CLI
