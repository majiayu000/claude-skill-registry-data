---
name: typescript
description: Apply when writing TypeScript code. Strict types, discriminated unions, async patterns, and runtime safety.
license: MIT
version: 1.0.0
tokens_target: 2500
triggers:
  - typescript code
  - strict types
  - async typescript
loads_after:
  - code-quality
supersedes: []
---

# Sub-Skill: TypeScript Best Practices
<!-- target: ~2500 tokens (real tiktoken count) | 17 rules with severity classification -->

**Purpose:** Prevents the TypeScript-specific mistakes LLMs make repeatedly — weak types, unsafe assertions, and patterns that compile but fail at runtime.

## Rule classification

- **MUST** — load-bearing. Violating leaks runtime errors past the type checker. Never break.
- **SHOULD** — default behavior. Deviation needs a documented reason in the code or PR.
- **AVOID** — usually wrong; documented exception inline where needed.

**Where these rules don't strictly apply:** test fixtures, generated types (e.g. from GraphQL codegen, OpenAPI generators, Prisma), declaration files (`*.d.ts`) for untyped third-party libraries, and migration scripts may legitimately differ. The rules below apply to **production application code**.

---

## Type Safety

1. **MUST: Never use `any`. Use `unknown` and narrow it.** `any` disables the type checker entirely. `unknown` forces you to prove the type before use. *Exception: third-party libraries without types and explicit dynamic-data boundaries (e.g. JSON parse at the API edge), with a comment explaining why.*
   ```ts
   // Wrong
   function parse(data: any) { return data.name; }

   // Correct
   function parse(data: unknown): string {
     if (typeof data === 'object' && data !== null && 'name' in data) {
       return String((data as { name: unknown }).name);
     }
     throw new Error('Invalid data shape');
   }
   ```

2. **AVOID: `Object` or `{}` as a type.** Both accept nearly everything. Use `Record<string, unknown>` for arbitrary objects or define an explicit interface.
   ```ts
   // Wrong
   function merge(a: {}, b: Object): {} { ... }

   // Correct
   function merge<T extends Record<string, unknown>>(a: T, b: Partial<T>): T { ... }
   ```

3. **SHOULD: Use `as` only when you know more than the compiler — and document why.** Prefer type guards or `satisfies` instead.
   ```ts
   // Wrong — silences the error, hides the bug
   const user = response.data as User;

   // Correct — validate first
   function isUser(v: unknown): v is User {
     return typeof v === 'object' && v !== null && 'id' in v && 'email' in v;
   }
   const user = isUser(response.data) ? response.data : null;
   ```

4. **SHOULD: Mark immutable data `readonly`.** Prevents accidental mutation and communicates intent.
   ```ts
   // Avoid
   function process(ids: string[]) { ids.push('extra'); }

   // Prefer
   function process(ids: readonly string[]) { /* ids.push() is a compile error */ }
   ```

5. **MUST: Enable `strictNullChecks` and handle every `T | undefined`.** Optional chaining `?.` returns `undefined` — always handle that branch.
   ```ts
   // Wrong
   const name = user?.profile.name.toUpperCase(); // crashes if name is undefined

   // Correct
   const name = user?.profile.name?.toUpperCase() ?? 'Anonymous';
   ```

6. **SHOULD: Use branded types for IDs.** Prevents passing a `UserId` where an `OrderId` is expected — both are `string` at runtime.
   ```ts
   type UserId = string & { readonly _brand: 'UserId' };
   type OrderId = string & { readonly _brand: 'OrderId' };

   function createUserId(raw: string): UserId { return raw as UserId; }

   function getUser(id: UserId): User { ... }
   // getUser(orderId) → compile error
   ```

---

## Patterns

7. **SHOULD: Use discriminated unions for state, not optional fields.** Optional fields force you to reason about all combinations. A discriminated union makes illegal states unrepresentable.
   ```ts
   // Avoid — 8 possible combinations, most invalid
   type Request = { loading?: boolean; data?: User; error?: Error };

   // Prefer — exactly 3 valid states
   type Request =
     | { status: 'idle' }
     | { status: 'loading' }
     | { status: 'success'; data: User }
     | { status: 'error'; error: Error };
   ```

8. **SHOULD: Use `satisfies` to validate shape without widening the type.** `as const` preserves literals; `satisfies` validates against an interface without losing them.
   ```ts
   const config = {
     host: 'localhost',
     port: 5432,
   } satisfies DatabaseConfig;
   // config.port is still typed as 5432, not number
   ```

9. **SHOULD: Use `const` objects instead of `enum`.** Enums emit runtime code, have surprising reverse-mapping behavior, and are not idiomatic TypeScript.
   ```ts
   // Avoid
   enum Direction { Up, Down, Left, Right }

   // Prefer
   const Direction = { Up: 'Up', Down: 'Down', Left: 'Left', Right: 'Right' } as const;
   type Direction = typeof Direction[keyof typeof Direction];
   ```

10. **AVOID: Barrel `index.ts` re-exports in large modules.** They cause circular dependency chains that are hard to debug. Export directly from source files or use explicit named re-exports only.
    ```ts
    // Wrong — index.ts re-exports everything, A imports B through index, B imports A through index
    export * from './userService';
    export * from './orderService';

    // Correct — import directly
    import { getUser } from './services/userService';
    ```

---

## Error Handling

11. **MUST: Type your thrown errors explicitly.** `catch (e)` gives you `unknown` in strict mode. Narrow before accessing properties.
    ```ts
    try {
      await fetchUser(id);
    } catch (e) {
      // Wrong: e.message — e is unknown
      // Correct:
      const message = e instanceof Error ? e.message : String(e);
      logger.error('fetchUser failed', { message, id });
    }
    ```

12. **SHOULD: Use `Result` types for expected failures instead of throwing.** Throwing for control flow forces callers to know which functions throw and what.
    ```ts
    type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

    function parseConfig(raw: string): Result<Config> {
      try {
        return { ok: true, value: JSON.parse(raw) };
      } catch (e) {
        return { ok: false, error: e instanceof Error ? e : new Error(String(e)) };
      }
    }
    ```

---

## Performance

13. **MUST: Use `Promise.all` for independent async operations, not sequential `await`.** Sequential awaits multiply latency.
    ```ts
    // Wrong — 300ms total if each takes 100ms
    const user = await getUser(id);
    const orders = await getOrders(id);
    const prefs = await getPrefs(id);

    // Correct — 100ms total
    const [user, orders, prefs] = await Promise.all([
      getUser(id),
      getOrders(id),
      getPrefs(id),
    ]);
    ```

14. **SHOULD: Use `Promise.allSettled` when partial failure is acceptable.** `Promise.all` rejects on the first failure. `allSettled` collects all results.
    ```ts
    const results = await Promise.allSettled(ids.map(fetchItem));
    const succeeded = results
      .filter((r): r is PromiseFulfilledResult<Item> => r.status === 'fulfilled')
      .map(r => r.value);
    ```

---

## Testing

15. **MUST: Type test helpers and mocks — never use `as any` to silence mock errors.** Untyped mocks let type errors hide until runtime. *Exception: prototyping spikes that are explicitly thrown away before merge.*
    ```ts
    // Wrong
    const mockUser = { id: '1' } as any;

    // Correct
    const mockUser: User = { id: createUserId('1'), email: 'a@b.com', name: 'Alice' };
    ```

16. **SHOULD: Test the discriminated union branches explicitly.** Each `status` variant is a separate code path. One test per branch minimum.
    ```ts
    it('renders error state', () => {
      const state: Request = { status: 'error', error: new Error('timeout') };
      render(<RequestView state={state} />);
      expect(screen.getByRole('alert')).toHaveTextContent('timeout');
    });
    ```

17. **SHOULD: Use `expectTypeOf` or `assertType` for type-level tests.** Runtime tests cannot catch type regressions.
    ```ts
    import { expectTypeOf } from 'vitest';
    expectTypeOf(createUserId('x')).toEqualTypeOf<UserId>();
    ```

---

## Why This Sub-Skill Earns Stars

These rules target the gap between "TypeScript that compiles" and "TypeScript that is safe". LLMs default to `any`, skip discriminated unions, and reach for `as` assertions because they are the path of least resistance. Each rule here closes a specific escape hatch that lets type errors reach production. The MUST/SHOULD/AVOID classification means safety-critical rules are strict and stylistic rules respect context.
