---
name: property-based-testing
description: Property-based and generative testing patterns (fast-check, Hypothesis). Use when testing complex business invariants, mathematical algorithms, data serialization/deserialization, parsing logic, or discovering unexpected edge case crashes.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0
category: algorithms-logic
---

# Property-Based Testing

> **Generative Invariant Testing, Input Shrinking & Edge-Case Discovery**

---

## 🏗️ Core Principles

| Principle | Rule |
|-----------|------|
| **Test Invariants, Not Examples** | Don't test `add(2, 3) === 5`. Test mathematical properties that must hold true for ALL inputs: commutative (`a + b === b + a`), identity (`a + 0 === a`). |
| **Automatic Shrinking** | When a failure is detected, property-based frameworks automatically shrink the input to the simplest minimal failing example. |
| **Roundtrip Invariant** | Serialization / deserialization must always be lossless: `decode(encode(data)) === data`. |
| **Idempotency Invariant** | Running an operation twice yields the identical state as running once: `format(format(str)) === format(str)`. |
| **Metamorphic Invariant** | A known change to an input results in a predictable change to output: `sort(arr).length === arr.length`. |

---

## 📋 Fast-Check Pattern (TypeScript)

```typescript
import fc from 'fast-check';
import { describe, it, expect } from 'vitest';
import { serializeUser, deserializeUser, User } from './user-codec';

describe('User Codec Property Tests', () => {
  it('should roundtrip any valid user object without data loss', () => {
    fc.assert(
      fc.property(
        fc.record<User>({
          id: fc.uuid(),
          email: fc.emailAddress(),
          age: fc.integer({ min: 0, max: 120 }),
          tags: fc.array(fc.string({ minLength: 1, maxLength: 20 })),
          isActive: fc.boolean(),
        }),
        (user) => {
          const encoded = serializeUser(user);
          const decoded = deserializeUser(encoded);
          expect(decoded).toEqual(user);
        }
      ),
      { numRuns: 1000 } // Test 1,000 distinct generated variants
    );
  });
});
```

---

## 📋 Common Invariant Archetypes

1. **Symmetric Operations**: `decrypt(encrypt(m, k), k) === m`.
2. **Oracle Comparison**: Verifying an optimized algorithm against an unoptimized but provably correct simple implementation.
3. **Hard-to-Compute, Easy-to-Verify**: Sorting is $O(n \log n)$, but verifying an array is sorted is $O(n)$ where every $a[i] \le a[i+1]$.

---

## ❌ Anti-Patterns

- ❌ Re-implementing the function logic inside the property test assertion.
- ❌ Testing with overly constrained input generators that miss real-world edge cases (empty strings, Unicode, null bytes, max integers).
- ❌ Ignoring non-deterministic property test failures instead of investigating root-cause edge cases.
