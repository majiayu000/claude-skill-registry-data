---
name: fixing-flaky-tests
description: Diagnose and fix flaky tests. Covers race conditions, timing issues, test pollution, async leaks.
type: workflow
tier: library
domains: [testing]
trigger: "flaky test, race condition, async test, intermittent fail, sometimes fails, non-deterministic"
---

## Root Cause Categories

### 1. Timing Dependency

```typescript
// BUG: assumes operation completes within 100ms
await new Promise(r => setTimeout(r, 100));
expect(result).toBe('done');

// FIX: wait for the actual condition
await vi.waitFor(() => expect(result).toBe('done'), { timeout: 5000 });
// or
await waitFor(() => screen.getByText('Done'));
```

### 2. Test Pollution (Shared State)

```typescript
// BUG: test 1 creates user, test 2 fails because user already exists
it('test 1', () => createUser({ email: 'test@example.com' }));
it('test 2', () => createUser({ email: 'test@example.com' })); // CONFLICT

// FIX: clean up after each test
afterEach(async () => {
  await db.user.deleteMany({ where: { email: 'test@example.com' } });
});

// BETTER FIX: use unique values per test
const email = `test-${Date.now()}@example.com`;
```

### 3. Async Leak

```typescript
// BUG: async operation continues after test ends
it('fetches data', () => {
  const result = [];
  fetchData().then(data => result.push(data)); // not awaited!
  // test ends, but fetchData is still running
  // it might complete and affect the next test
});

// FIX: always await async operations
it('fetches data', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});
```

### 4. Global State / Singleton Pollution

```typescript
// BUG: EventEmitter accumulates listeners across tests
const emitter = new EventEmitter(); // global singleton

// FIX: reset global state in beforeEach/afterEach
beforeEach(() => { emitter.removeAllListeners(); });

// BETTER: inject dependencies instead of using singletons
```

### 5. Order Dependency

```typescript
// BUG: test B relies on state set by test A
describe('CartService', () => {
  it('test A: adds item', () => { cart.add(item); });
  it('test B: removes item', () => { cart.remove(item.id); }); // fails if A didn't run
});

// FIX: each test is self-contained
describe('CartService', () => {
  beforeEach(() => { cart = new Cart(); }); // fresh state
  it('test B: removes item that exists', () => {
    cart.add(item);       // set up in this test
    cart.remove(item.id);
    expect(cart.items).toHaveLength(0);
  });
});
```

## Debugging Flaky Tests

```bash
# Run just the flaky test 20 times to see failure rate
for i in {1..20}; do vitest run --reporter verbose flaky.test.ts 2>&1 | grep -E "PASS|FAIL"; done

# Detect test order dependency
vitest run --sequence.shuffle  # random order

# Find long-running tests
vitest run --reporter verbose 2>&1 | grep "ms"
```

## When to Skip vs Fix

**Fix:** All flaky tests should be fixed. "Flaky" = unreliable = wrong.

**Skip temporarily** (with explanation):
```typescript
it.skip('FLAKY: #123 race condition in payment service', async () => {
  // This will be re-enabled when #123 is resolved
});
```

Never commit a flaky test without a ticket. Never.
