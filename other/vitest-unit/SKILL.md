---
name: vitest-unit
description: "World Pulse: When writing or modifying tests in `src/**/*.test.{ts,tsx}`."
---

# Vitest Unit Test

**When to use:** When writing or modifying tests in `src/**/*.test.{ts,tsx}`.

---

## Framework Setup (from `vitest.config.ts`)

- **Test runner:** Vitest with `globals: true` — `describe`, `it`, `expect`, `vi` are global (no import needed, but importing is also fine).
- **Environment:** Auto-selected per path:
  - `src/renderer/**` → `jsdom`
  - `src/server/**` → `node`
- **Setup file:** `src/test/setup.ts` — imports `@testing-library/jest-dom` matchers.
- **Coverage:** V8 provider, target >70%.

---

## Test File Convention

Co-locate tests next to source:

```
src/server/collectors/earthquakes.ts
src/server/collectors/earthquakes.test.ts   ← same directory
```

File pattern: `*.test.{ts,tsx}`.

---

## Test Structure

```ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MyClass } from './myClass';

describe('MyClass', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('methodName', () => {
    it('returns expected value when ...', () => {
      const result = new MyClass().methodName();
      expect(result).toBe(expected);
    });
  });
});
```

---

## Mocking Conventions

Use `vi.fn()` for function mocks and `vi.spyOn()` for method spies:

```ts
const mockFetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ data: [] }) });
global.fetch = mockFetch;
```

For Socket.io tests, mock the entire `socket.io-client` module:

```ts
vi.mock('socket.io-client', () => ({
  io: vi.fn(() => ({
    on: vi.fn(),
    off: vi.fn(),
    emit: vi.fn(),
    disconnect: vi.fn(),
    io: { on: vi.fn(), opts: {} },
  })),
}));
```

---

## Collector Tests (from `base.test.ts`)

The BaseCollector test pattern uses concrete subclasses that override `fetch()` and `validate()`:

```ts
class FailingCollector extends BaseCollector {
  constructor() { super('fail-test', 'earthquake', 1000, 2, 1000); }
  async fetch(): Promise<Event[]> { throw new Error('simulated failure'); }
  validate() { return false; }
}
```

Always test:
1. Happy path — returns correct data shape.
2. Error path — increments error count, disables after `maxErrors`.
3. Recovery — re-enables after cooldown when errors clear.

---

## Component Tests

Use `@testing-library/react`:

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MyComponent } from './MyComponent';

it('shows label text', () => {
  render(<MyComponent label="STATUS" />);
  expect(screen.getByText('STATUS')).toBeInTheDocument();
});
```

Always query by accessible role or text, not by class name or test-id unless unavoidable.

---

## Store Tests

Wrap store resets around each test to prevent state leakage:

```ts
import { act } from '@testing-library/react';
import { useAppStore } from './useAppStore';

beforeEach(() => {
  act(() => {
    useAppStore.setState({
      events: [],
      connectionStatus: 'connecting',
    });
  });
});
```

---

## Running Tests

```bash
npx vitest run src/server/collectors/earthquakes.test.ts  # single file
npm test                                                   # all tests
npm run test:coverage                                      # with V8 coverage
```

---

## Anti-Patterns

- Do not use `jest` APIs — this project uses Vitest.
- Do not test implementation details — test public behavior.
- Do not leave `vi.spyOn` without `vi.restoreAllMocks()` or `beforeEach(() => vi.clearAllMocks())`.
- Do not write tests that depend on execution order.
- Coverage target >70% is enforced in CI — new code without tests will fail the gate.
