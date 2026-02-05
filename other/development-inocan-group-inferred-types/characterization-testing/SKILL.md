---
name: Characterization Testing
description: Create tests that describe what legacy code actually does (not what it should do) as safety net before refactoring
when_to_use: when working with legacy code that has no tests and unclear behavior, before attempting any changes or refactoring
version: 1.0.0
languages: all
---

# Characterization Testing

## Overview

Characterization tests capture current behavior of legacy code, warts and all. They're a safety net before refactoring, not a specification of correctness.

**Core principle:** Document what IS, not what SHOULD BE. Fix behavior later, after safety net exists.

**This is NOT unit testing.** Unit tests specify desired behavior. Characterization tests document actual behavior.

## When to Use

Use characterization testing when:
- Legacy code has no automated tests
- Unclear what code is supposed to do
- Before refactoring risky/critical areas
- Documentation doesn't match reality
- Need safety net without understanding all edge cases

**Don't use when:**
- Code already has comprehensive tests
- You're implementing new features (use TDD instead)
- Code is so simple testing is unnecessary

## The Iron Law

```
NO REFACTORING WITHOUT CHARACTERIZATION TESTS FIRST
```

Refactoring without tests = gambling with production. Always create safety net first.

## The Process

### Step 1: Identify Target

Choose smallest meaningful unit to characterize:
- Single function/method (best starting point)
- Single class (if functions are tightly coupled)
- Module (if class boundaries unclear)

**Start small.** You can always expand coverage later.

### Step 2: Write Failing Test

Write test with unknown expectation:

```typescript
test('processes user data', () => {
  const result = processUserData({ name: 'John', age: 30 });
  expect(result).toEqual(/* ??? what does it return? */);
});
```

**Don't guess.** Leave expectation blank or use placeholder.

### Step 3: Run and Capture

Run the test. It will fail. **Copy the actual output exactly:**

```bash
$ npm test
FAIL: expected ???, received { fullName: 'John', isAdult: true, category: 'standard' }
```

This is the characterization: what the code actually does right now.

### Step 4: Lock In Behavior

Update test with actual output:

```typescript
test('processes user data', () => {
  const result = processUserData({ name: 'John', age: 30 });
  expect(result).toEqual({
    fullName: 'John',
    isAdult: true,
    category: 'standard'
  });
});
```

**Run test again → should pass.** You've characterized the behavior.

### Step 5: Add Edge Cases

Find weird inputs and capture outputs:

```typescript
test('handles missing age', () => {
  const result = processUserData({ name: 'John' });
  // Run test, see what happens, lock it in
  expect(result).toEqual({
    fullName: 'John',
    isAdult: false,
    category: 'unknown'
  });
});

test('handles negative age (current behavior - BUG)', () => {
  const result = processUserData({ name: 'John', age: -5 });
  // This is wrong but it's what code does now
  expect(result).toEqual({
    fullName: 'John',
    isAdult: true,  // BUG: negative age treated as adult!
    category: 'standard'
  });
});

test('handles empty name', () => {
  const result = processUserData({ name: '', age: 30 });
  expect(result).toEqual({
    fullName: '',
    isAdult: true,
    category: 'standard'
  });
});

test('handles null input', () => {
  // Might throw error, might return null - capture what happens
  expect(() => processUserData(null)).toThrow('Cannot read property');
});
```

**Key insight:** You're documenting bugs, not fixing them. Tests show what code does, including incorrect behavior.

### Step 6: Document Known Issues

Mark tests for known bugs:

```typescript
test.skip('FIXME: should reject negative age', () => {
  // This is what SHOULD happen (not what happens now)
  expect(() => processUserData({ name: 'John', age: -5 }))
    .toThrow('Invalid age: must be non-negative');
});

test('handles negative age (CURRENT BEHAVIOR - BUG)', () => {
  // This is what ACTUALLY happens now
  const result = processUserData({ name: 'John', age: -5 });
  expect(result.isAdult).toBe(true); // Wrong! But it's current behavior
});
```

**Why both tests?**
- `.skip` test shows desired behavior (for future)
- Active test locks in current behavior (prevents regressions during refactoring)

### Step 7: Verify Coverage

Ensure main execution paths covered:

- Happy path (valid inputs)
- Edge cases (empty, null, undefined, zero, negative)
- Boundary values (max/min for your domain)
- Error cases (invalid inputs, external failures)

**Not 100% code coverage.** Focus on behavior coverage: scenarios that matter.

## Checklist

- [ ] Identified smallest testable unit
- [ ] Wrote test with unknown expectation (???)
- [ ] Ran test and captured actual output
- [ ] Locked in current behavior (test passes)
- [ ] Added edge cases (empty, null, invalid, boundary values)
- [ ] Documented known bugs with comments
- [ ] Created .skip tests for desired behavior (future fixes)
- [ ] All tests pass (green for current behavior)
- [ ] Tests cover main execution paths

## Example: Full Workflow

**Legacy code we need to refactor:**

```typescript
function calculateDiscount(user, cart) {
  let total = 0;
  for (let i = 0; i < cart.items.length; i++) {
    total += cart.items[i].price * cart.items[i].quantity;
  }

  if (user.isPremium) {
    total = total * 0.9;
  }

  if (cart.items.length > 5) {
    total = total * 0.95;
  }

  return Math.round(total * 100) / 100;
}
```

**Characterization tests:**

```typescript
describe('calculateDiscount - characterization', () => {
  test('standard user, small cart', () => {
    const user = { isPremium: false };
    const cart = {
      items: [
        { price: 10, quantity: 2 },
        { price: 5, quantity: 1 }
      ]
    };

    const result = calculateDiscount(user, cart);
    expect(result).toBe(25); // 10*2 + 5*1 = 25
  });

  test('premium user gets 10% discount', () => {
    const user = { isPremium: true };
    const cart = { items: [{ price: 100, quantity: 1 }] };

    const result = calculateDiscount(user, cart);
    expect(result).toBe(90); // 100 * 0.9 = 90
  });

  test('more than 5 items gets additional 5% discount', () => {
    const user = { isPremium: false };
    const cart = {
      items: Array(6).fill({ price: 10, quantity: 1 })
    };

    const result = calculateDiscount(user, cart);
    expect(result).toBe(57); // 60 * 0.95 = 57
  });

  test('premium + bulk discounts stack (CURRENT BEHAVIOR)', () => {
    const user = { isPremium: true };
    const cart = {
      items: Array(6).fill({ price: 10, quantity: 1 })
    };

    const result = calculateDiscount(user, cart);
    expect(result).toBe(51.3); // 60 * 0.9 * 0.95 = 51.3
  });

  test('empty cart returns 0', () => {
    const user = { isPremium: false };
    const cart = { items: [] };

    const result = calculateDiscount(user, cart);
    expect(result).toBe(0);
  });

  test('missing isPremium field (CURRENT BEHAVIOR - BUG?)', () => {
    const user = {}; // no isPremium field
    const cart = { items: [{ price: 100, quantity: 1 }] };

    const result = calculateDiscount(user, cart);
    expect(result).toBe(100); // Falsy check treats missing as non-premium
  });

  test('null user throws error', () => {
    const cart = { items: [{ price: 100, quantity: 1 }] };

    expect(() => calculateDiscount(null, cart))
      .toThrow("Cannot read property 'isPremium' of null");
  });
});
```

**Now safe to refactor!** If refactoring breaks these tests, you've changed behavior (maybe accidentally).

## Anti-Patterns

### ❌ Fixing Bugs While Characterizing

**Bad:**
```typescript
test('negative price should be rejected', () => {
  expect(() => calculateDiscount(user, { items: [{ price: -10, quantity: 1 }] }))
    .toThrow('Invalid price');
});
```

This is what SHOULD happen, not what DOES happen. You're writing specification, not characterization.

**Good:**
```typescript
test('negative price (CURRENT BEHAVIOR - BUG)', () => {
  const user = { isPremium: false };
  const cart = { items: [{ price: -10, quantity: 1 }] };

  const result = calculateDiscount(user, cart);
  expect(result).toBe(-10); // Bug: negative total! But this is current behavior
});

test.skip('FIXME: negative price should be rejected', () => {
  // This is desired future behavior
  expect(() => calculateDiscount(user, { items: [{ price: -10, quantity: 1 }] }))
    .toThrow('Invalid price');
});
```

### ❌ Refactoring Before Tests

**Bad:**
```
1. Look at legacy code
2. "This is messy, let me clean it up"
3. Refactor
4. Add tests
```

**Good:**
```
1. Look at legacy code
2. Add characterization tests
3. Verify tests pass
4. Refactor with confidence
5. Tests still pass → safe refactoring
```

### ❌ Mocking Everything

**Bad:**
```typescript
test('calls database with correct params', () => {
  const mockDB = jest.fn();
  processUserData(mockDB, user);
  expect(mockDB).toHaveBeenCalledWith('users', { id: 123 });
});
```

This tests interactions, not behavior. You don't know what the function returns.

**Good:**
```typescript
test('processes user data from database', () => {
  // Use real database or test database
  const result = processUserData({ id: 123 });
  expect(result).toEqual({ name: 'John', email: 'john@example.com' });
});
```

Characterization tests should test real behavior with real dependencies when possible.

### ❌ Skipping "Embarrassing" Bugs

**Bad:**
```typescript
// I found this bug but I'm not going to test it because it's embarrassing
```

**Good:**
```typescript
test('allows XSS in user input (CURRENT BEHAVIOR - SECURITY BUG)', () => {
  const result = renderUserProfile({ name: '<script>alert("xss")</script>' });
  expect(result).toContain('<script>alert("xss")</script>');
  // Bug exists! But test documents it so we can fix it later
});
```

Document all bugs, especially security issues. Better to know than to be surprised.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Code is too complex to test" | Characterization tests don't need full understanding. Capture behavior empirically. |
| "I'll refactor, then add tests" | Refactoring without tests = hoping you didn't break anything. Tests first. |
| "Tests will take too long" | Hours of characterization vs days of debugging production. Tests are faster. |
| "I know what the code should do" | Great! But what does it actually do? They might differ. |
| "I'll just be careful" | You will miss edge cases. Tests catch what you forget. |
| "Bugs are embarrassing to test" | Documented bugs can be fixed. Hidden bugs cause incidents. |

## After Characterization

Now you have safety net. Next steps:

1. **Refactor with confidence** - Tests catch if you break something
2. **Fix bugs one at a time** - Update characterization test to desired behavior
3. **Add unit tests** - For new features, use TDD going forward
4. **Remove characterization tests** - Once you have proper unit tests covering behavior

**Characterization tests are temporary.** They're scaffolding for refactoring, not permanent test suite.

## Integration with Other Skills

- **skills/analysis/code-archaeology** - Understand code before characterizing
- **skills/refactoring/strangler-fig-pattern** - Replace characterized code safely
- **skills/testing/test-driven-development** - Add new features with TDD after characterization
- **skills/refactoring/seam-finding** - Find boundaries for characterization
- **skills/safety/approval-testing** - Alternative for complex outputs

## Remember

- Characterization tests document what IS, not what SHOULD BE
- Run test → capture output → lock it in
- Document bugs, don't fix them (yet)
- Tests are safety net for refactoring
- NO REFACTORING without characterization tests first
- Characterization tests are temporary scaffolding
