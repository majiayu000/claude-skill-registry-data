---
name: bupkis-assertion-patterns
description: How to write idiomatic assertions with the Bupkis assertion library for TypeScript and JavaScript
---

# Bupkis Assertion Patterns

Write idiomatic, expressive assertions using bupkis' powerful assertion vocabulary to make tests more readable and maintainable.

## When to Use

- Writing tests with the bupkis assertion library
- Checking properties, types, or structure of objects
- Verifying arrays or collections
- Want clearer, more expressive test failures

## When NOT to Use

- When a simple, direct assertion is clearer (don't over-complicate)
- When the pattern doesn't improve readability

## Core Principles

1. **Use semantic assertions**: Choose assertions that express intent, not implementation
2. **Combine related checks**: Use `to satisfy` for multiple properties rather than separate assertions
3. **Leverage bupkis vocabulary**: Use built-in assertions like `to have property`, `to be empty`, etc.
4. **Let assertions imply related checks**: e.g., `to be an object` already implies non-null

## Patterns

### 1. Property Existence

**Prefer semantic property checks over truthiness checks.**

```typescript
// ❌ DON'T - unclear intent, indirect check
expect('filesCompleted' in state, 'to be truthy');

// ✅ DO - clear, semantic assertion
expect(state, 'to have property', 'filesCompleted');
```

**Why:** `to have property` expresses the intent clearly and provides better error messages.

---

### 2. Type Checking Multiple Properties

**Combine related type checks using `to satisfy` instead of separate assertions.**

```typescript
// ❌ DON'T - repetitive, verbose
expect(typeof state.filesCompleted, 'to equal', 'number');
expect(typeof state.suitesCompleted, 'to equal', 'number');
expect(typeof state.tasksCompleted, 'to equal', 'number');

// ✅ DO - concise, shows structure at a glance
expect(state, 'to satisfy', {
  filesCompleted: expect.it('to be a number'),
  suitesCompleted: expect.it('to be a number'),
  tasksCompleted: expect.it('to be a number'),
});
```

**Why:** `to satisfy` lets you verify multiple properties in one assertion, showing the expected structure clearly. Better error messages show exactly which properties failed.

---

### 3. Non-Empty Collections

**Use semantic collection assertions instead of length comparisons.**

```typescript
// ❌ DON'T - indirect, requires mental math
expect(result.files.length, 'to be greater than', 0);

// ✅ DO - direct, semantic
expect(result.files, 'not to be empty');
```

**Why:** `not to be empty` directly expresses the intent. Works for arrays, strings, objects, Maps, Sets, etc.

---

### 4. Object and Null Checks

**Don't redundantly check for null when object check already implies it.**

```typescript
// ❌ DON'T - redundant null check
expect(config, 'to be an object');
expect(config, 'not to be null');

// ✅ DO - object check implies non-null
expect(config, 'to be an object'); // already implies non-null
```

**Why:** In bupkis, `to be an object` already ensures the value is not null. Redundant checks add noise.

---

### 5. Object Structure Verification

**Verify object structure with `to satisfy` instead of multiple property assertions.**

```typescript
// ❌ DON'T - fragmented, hard to see expected structure
expect(config, 'to be an object');
expect(config.iterations, 'to equal', 500);
expect(config.reporters[0], 'to equal', 'json');
expect(config.reporters.length, 'to equal', 1);

// ✅ DO - clear, declarative structure check
expect(config, 'to satisfy', {
  iterations: 500,
  reporters: expect.it('to deep equal', ['json']),
});
```

**Why:** `to satisfy` lets you declaratively specify the expected structure. Combines type check and property validation in one assertion. Shows the expected shape at a glance.

---

### 5b. Multiple Conditions on the Same Result Object

**Combine multiple checks on a result object with `to satisfy` instead of separate assertions.**

```typescript
// ❌ DON'T - multiple separate assertions
expect(result.exitCode, 'to equal', 0);
expect(result.stdout, 'to match', /No historical data/);
expect(result.stderr, 'not to match', /toLocaleDateString is not a function/);

// ✅ DO - single to satisfy assertion
expect(result, 'to satisfy', {
  exitCode: 0,
  stdout: expect.it('to match', /No historical data/),
  stderr: expect.it('not to match', /toLocaleDateString is not a function/),
});
```

**Why:** Groups all related checks on the same object. Shows the expected result state clearly. Easier to maintain - add/remove checks in one place. Better error messages show exactly which property failed.

---

### 6. Defined Value Checks

**Use positive assertions instead of negated ones when possible.**

```typescript
// ❌ DON'T - negated assertion
expect(result, 'not to be undefined');

// ✅ DO - positive, semantic
expect(result, 'to be defined');
```

**Why:** `to be defined` is clearer and more idiomatic than negating undefined. It's a positive assertion that directly expresses intent.

---

### 7. Chaining Assertions with 'and'

**Use concatenation when making multiple assertions on the same subject.**

```typescript
// ❌ DON'T - separate assertions
expect(config, 'to be an object'); // implies non-null
expect(config, 'to have property', 'reporters');

// ✅ DO - chain with 'and'
expect(config, 'to be an object', 'and', 'to have property', 'reporters');
```

**Why:** Chaining assertions with `'and'` keeps related checks together in a single statement. More concise and shows that you're checking multiple aspects of the same value. Better error messages that show which part of the chain failed.

---

### 8. Multiple Property Checks with Array

**Use `to have properties` with an array when checking for multiple properties.**

```typescript
// ❌ DON'T - chain multiple property checks
expect(
  config,
  'to be an object',
  'and',
  'to have property',
  'outputDir',
  'and',
  'to have property',
  'reporters',
);

// ✅ DO - use 'to have properties' with array
expect(config, 'to have properties', ['outputDir', 'reporters']);
```

**Why:** `to have properties` with an array is specifically designed for checking multiple properties at once. More concise than chaining. Shows all required properties clearly in one place. Better error messages that list all missing properties.

---

### 9. Promise Rejection Checks

**Use `expectAsync` with `'to reject'` for testing promise rejections.**

```typescript
// ❌ DON'T - wishy-washy try/catch
try {
  await configManager.load('nonexistent.config.json');
  expect(true, 'to be truthy'); // Maybe it works?
} catch (error) {
  expect(error, 'to be an', Error); // Or maybe it throws?
  expect((error as Error).message, 'not to be empty');
}

// ✅ DO - explicit promise rejection check
await expectAsync(configManager.load('nonexistent.config.json'), 'to reject');
```

**Why:** Makes the contract explicit - either it should reject or it shouldn't. No ambiguity. `expectAsync` is specifically designed for promise-based assertions. `'to reject'` clearly expresses that rejection is the expected behavior.

**Related assertions:**

- `'to reject'` - promise should be rejected
- `'to reject with error satisfying'` - promise should reject with specific error

---

## Advanced `to satisfy` Patterns

### Partial Object Matching

```typescript
// Only check specific properties, ignore others
expect(result, 'to satisfy', {
  status: 'complete',
  // other properties ignored
});
```

### Nested Structure

```typescript
expect(benchmark, 'to satisfy', {
  name: expect.it('to be a string'),
  results: expect.it('to satisfy', {
    mean: expect.it('to be a number'),
    median: expect.it('to be a number'),
  }),
});
```

### Array Element Values

```typescript
// Check specific array values within to satisfy
expect(config, 'to satisfy', {
  iterations: 100,
  reporters: ['human'], // checks first element matches
});

// Or check multiple elements
expect(config, 'to satisfy', {
  tags: ['performance', 'critical'],
});
```

### Arrays with Patterns

```typescript
// All items must satisfy condition
expect(results, 'to have items satisfying', {
  duration: expect.it('to be a number'),
  status: 'success',
});
```

## Quick Reference

| Instead of...                          | Use...                                                 |
| -------------------------------------- | ------------------------------------------------------ |
| `'prop' in obj, 'to be truthy'`        | `obj, 'to have property', 'prop'`                      |
| `typeof x.prop, 'to equal', 'number'`  | `x, 'to satisfy', {prop: expect.it('to be a number')}` |
| `arr.length, 'to be greater than', 0`  | `arr, 'not to be empty'`                               |
| `result, 'not to be undefined'`        | `result, 'to be defined'`                              |
| Separate expect() on same subject      | Chain with `'and'`: `expect(x, 'a', 'and', 'b')`       |
| Multiple 'to have property' assertions | `to have properties`, `['prop1', 'prop2']`             |
| try/catch for promise rejection        | `await expectAsync(promise, 'to reject')`              |
| Multiple assertions on the same object | `to satisfy` with object structure                     |
| Separate object + null checks          | Just `to be an object`                                 |

## Benefits

1. **Clearer intent**: Semantic assertions express what you're testing, not how
2. **Better error messages**: bupkis shows exactly what failed in structural checks
3. **More maintainable**: Related checks grouped together, easier to update
4. **Less code**: Combine multiple assertions into expressive structure checks
5. **Discover structure**: `to satisfy` shows expected object shape at a glance

## Tools Used

- `expect()` with bupkis assertion vocabulary
- `expect.it()` for nested assertions within `to satisfy`
- Semantic assertions: `to have property`, `not to be empty`, `to be an object`
- Structural assertions: `to satisfy`, `to deep equal`
