---
name: typescript
description: |
  Idiomatic programming style, patterns, and conventions for TypeScript and JavaScript development.
  Trigger when:
  - Writing, refactoring, reviewing, or debugging TypeScript or JavaScript code.
  - Files matching the patterns **/*.ts, **/*.tsx, **/*.js, **/*.jsx, package.json are in the workspace or referenced.
  - Tasks involve: tsc, npm, yarn, pnpm, bun, eslint, prettier, vite, next.js.
  - Prompt contains keywords: typescript, ts, js, javascript, interface, type, async, await, promise, es6, node, deno.
---

# TypeScript / JavaScript Language Idioms

Work _with_ the language. Embrace its asynchronous nature, its structural type system, and its functional roots. Fight the urge to write Java-in-TypeScript.

---

## Core Philosophy

- **Immutability by default** — `const` everything, spread to copy, never mutate in place
- **Type safety without ceremony** — let inference work, annotate at boundaries
- **Composition over inheritance** — functions, modules, and interfaces beat class hierarchies
- **Explicit over implicit** — no coercion tricks, no hidden state, no magic

---

## References and Variables

### The Rules

| Keyword | Usage                                 | Rationale                                    |
| :------ | :------------------------------------ | :------------------------------------------- |
| `const` | Default for all bindings              | Prevents reassignment, signals intent        |
| `let`   | Only when reassignment is unavoidable | Loops, accumulators, state machines          |
| `var`   | **Prohibited**                        | Function-scoped, hoists, leaks out of blocks |

### Destructuring and Spread

Use destructuring to extract what you need. Use spread to copy without mutation:

```typescript
// ✅ Destructure at the call site
const { name, age } = getUser();

// ✅ Shallow-copy with spread — never mutate the original
const updated = { ...config, timeout: 5000 };
const extended = [...items, newItem];

// ❌ Mutating the original
config.timeout = 5000;
items.push(newItem);
```

Use `Object.hasOwn(obj, key)` instead of `obj.hasOwnProperty(key)` — the latter can be shadowed.

---

## Functions

### Arrow Functions

Use arrow functions for callbacks and short expressions. They preserve lexical `this`:

```typescript
// ✅ Arrow for callbacks
const sorted = items.sort((a, b) => a.name.localeCompare(b.name));

// ✅ Arrow for inline transforms
const names = users.map((u) => u.name);

// ❌ Legacy — don't use `function` for callbacks
const names = users.map(function (u) {
  return u.name;
});
```

Use `function` declarations for top-level named functions (they hoist and have clear stack traces).

### Options Objects

When a function's parameter list becomes unwieldy, use a single options object:

```typescript
// ❌ Positional parameter overload
function createServer(
  port: number,
  host: string,
  ssl: boolean,
  timeout: number,
);

// ✅ Options object — extensible, self-documenting
interface ServerOptions {
  port: number;
  host?: string;
  ssl?: boolean;
  timeout?: number;
}
function createServer(options: ServerOptions);
```

### Rest Parameters

Use rest syntax. The `arguments` object is prohibited:

```typescript
// ✅ Rest gives you a real Array
function log(level: string, ...messages: string[]) {}

// ❌ arguments is not a real Array and has no type safety
function log() {
  console.log(arguments);
}
```

### Pure Functions

Prefer functions that return values based solely on inputs. Reserve side effects for explicit boundaries (I/O, event handlers, logging).

### Functional Iterators

Use `map`, `filter`, `reduce` to build declarative pipelines that produce new data:

```typescript
// ✅ Declarative pipeline — new array, no mutation
const active = users.filter((u) => u.isActive).map((u) => u.email);

// ❌ Imperative mutation
const active: string[] = [];
users.forEach((u) => {
  if (u.isActive) active.push(u.email);
});
```

`forEach` is acceptable for genuine side effects (logging, DOM, events) — not for data transformation.

---

## Async Patterns

JavaScript is async-first. Treat asynchrony as the normal case, not the exception.

### `async`/`await`

Prefer `async`/`await` over `.then()` chains:

```typescript
// ✅ Linear, readable
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new HttpError(res.status);
  return res.json();
}

// ❌ Nested chains obscure flow
function fetchUser(id: string): Promise<User> {
  return fetch(`/api/users/${id}`).then((res) => {
    if (!res.ok) throw new HttpError(res.status);
    return res.json();
  });
}
```

### Concurrent Operations

| Pattern              | Behavior                      | Use When                      |
| :------------------- | :---------------------------- | :---------------------------- |
| `Promise.all`        | Fails fast on first rejection | All must succeed              |
| `Promise.allSettled` | Waits for all, reports each   | Partial failure is acceptable |
| `Promise.race`       | Resolves/rejects with first   | Timeouts, fastest-wins        |

### Cancellation

Use `AbortController` for cancellable operations:

```typescript
const controller = new AbortController();
const res = await fetch(url, { signal: controller.signal });

// Cancel from elsewhere
controller.abort();
```

---

## Modules

### ES Modules Only

Use `import`/`export`. CommonJS (`require`) is legacy.

### Named Exports

Prefer named exports. They enable compile-time reference checks and explicit dependency graphs:

```typescript
// ✅ Named — IDE catches broken imports immediately
export function parse(input: string): Token[] {
  /* ... */
}
export interface Token {
  type: string;
  value: string;
}

// ⚠️ Default — permits arbitrary rename at import site
export default function parse(input: string): Token[] {
  /* ... */
}
```

Default exports are acceptable for framework conventions (e.g., Vue SFCs, Next.js pages) but never preferred.

### Barrel Files

Use barrel files (`index.ts`) sparingly. They defeat tree-shaking and create circular dependency traps. Export directly from source modules when possible.

---

## Type System

### Strict Mode

Enable `strict: true` in `tsconfig.json`. This is non-negotiable — it activates `strictNullChecks`, `noImplicitAny`, and other critical checks.

### Type Inference vs. Annotation

Let TypeScript infer when the type is obvious. Annotate at boundaries — function parameters, return types, and public APIs:

```typescript
// ✅ Inferred — obvious from the literal
const count = 0;
const name = "alice";

// ✅ Annotated — boundary, not obvious
function parseConfig(raw: string): Config {
  /* ... */
}
```

### `unknown` over `any`

`any` disables type checking. Use `unknown` and narrow explicitly:

```typescript
// ✅ Forces narrowing before use
function handle(input: unknown) {
  if (typeof input === "string") {
    console.log(input.toUpperCase());
  }
}

// ❌ Silently accepts anything — bugs hide here
function handle(input: any) {
  console.log(input.toUpperCase()); // runtime bomb
}
```

### Discriminated Unions

Model variant state with a literal discriminant. This enables exhaustive `switch` checking:

```typescript
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };

function handle(result: Result<string>) {
  if (result.ok) {
    console.log(result.value); // narrowed to { ok: true; value: string }
  } else {
    console.error(result.error); // narrowed to { ok: false; error: Error }
  }
}
```

### `satisfies`

Validate that a value conforms to a type without widening:

```typescript
// ✅ Validates shape, preserves literal types
const routes = {
  home: "/",
  about: "/about",
  users: "/users",
} satisfies Record<string, string>;

// TypeScript still knows routes.home is "/" (literal), not just string
```

### `as const`

Use `as const` for immutable literal types. Replaces enums in most cases:

```typescript
// ✅ as const object — runtime value + narrow types
const Status = {
  Active: "active",
  Inactive: "inactive",
  Pending: "pending",
} as const;

type Status = (typeof Status)[keyof typeof Status];
// "active" | "inactive" | "pending"
```

### Utility Types

Use built-in utility types to derive types from existing ones:

| Type           | Purpose                 | Example                |
| :------------- | :---------------------- | :--------------------- |
| `Partial<T>`   | All properties optional | Patch/update payloads  |
| `Required<T>`  | All properties required | Validated config       |
| `Readonly<T>`  | All properties readonly | Frozen state           |
| `Pick<T, K>`   | Subset of properties    | API response shaping   |
| `Omit<T, K>`   | Exclude properties      | Remove internal fields |
| `Record<K, V>` | Map of key-value pairs  | Lookup tables          |

### Branded Types

Simulate nominal typing for domain safety:

```typescript
type UserId = string & { readonly __brand: unique symbol };
type PostId = string & { readonly __brand: unique symbol };

function createUserId(id: string): UserId {
  return id as UserId; // validated assertion at construction
}

// Now UserId and PostId are incompatible at compile time
```

### Type Erasure

TypeScript types are stripped at build time. They cannot guard runtime execution.

- **Prefer erasable-only syntax** — types, interfaces, type aliases all vanish cleanly
- **Avoid enums** — they emit runtime JavaScript; use `as const` objects or union types instead
- **Use `#field` for private** — not the `private` keyword, which is TypeScript-only
- **Validate at boundaries** — external data (API responses, user input) must be validated at runtime, not just typed

```typescript
// ✅ Native private — survives type erasure
class User {
  #email: string;
  constructor(email: string) {
    this.#email = email;
  }
}

// ❌ TypeScript private — erased, accessible at runtime
class User {
  private email: string;
  constructor(email: string) {
    this.email = email;
  }
}
```

---

## Error Handling

### Custom Error Classes

Extend `Error` with domain-specific types. Always set `name`:

```typescript
class HttpError extends Error {
  constructor(
    public readonly status: number,
    message?: string,
  ) {
    super(message ?? `HTTP ${status}`);
    this.name = "HttpError";
  }
}
```

### Async Error Handling

Catch at the appropriate level. Don't swallow errors silently:

```typescript
// ✅ Catch and handle or rethrow with context
try {
  const user = await fetchUser(id);
} catch (err) {
  if (err instanceof HttpError && err.status === 404) {
    return null; // expected case
  }
  throw err; // unexpected — propagate
}
```

### Error Narrowing

TypeScript's `catch` clause types as `unknown`. Narrow before accessing:

```typescript
try {
  await riskyOperation();
} catch (err) {
  if (err instanceof Error) {
    console.error(err.message);
  } else {
    console.error("Unknown error:", err);
  }
}
```

---

## Naming Conventions

| Scope                                | Style                          | Example                        |
| :----------------------------------- | :----------------------------- | :----------------------------- |
| Classes, interfaces, type aliases    | `PascalCase`                   | `UserAccount`, `ServerOptions` |
| Functions, variables, properties     | `camelCase`                    | `calculateTotal`, `isActive`   |
| Exported constants (true invariants) | `SCREAMING_SNAKE`              | `MAX_RETRIES`, `API_VERSION`   |
| Private class fields                 | `#camelCase`                   | `#connectionPool`              |
| Generic type parameters              | Single uppercase or `T`-prefix | `T`, `K`, `TResult`            |

### Equality

Use strict equality (`===` / `!==`). Never rely on abstract coercion (`==`).

Use shortcuts for booleans (`if (isValid)`) but explicit comparisons for strings and numbers (`if (name !== "")`, `if (count > 0)`) to prevent coercion surprises.

### Nullish Handling

Prefer `??` over `||` for defaults — `||` coerces `0`, `""`, and `false` to falsy:

```typescript
// ✅ Only falls through on null/undefined
const timeout = options.timeout ?? 3000;

// ❌ Falls through on 0, "", false
const timeout = options.timeout || 3000;
```

Use optional chaining (`?.`) for safe property access.

---

## Anti-Patterns

| Anti-Pattern               | Description                                                | Remedy                                      |
| :------------------------- | :--------------------------------------------------------- | :------------------------------------------ |
| **`any` leakage**          | Using `any` to silence the compiler                        | Use `unknown` and narrow                    |
| **Enum abuse**             | TypeScript enums that emit runtime code                    | `as const` objects or union types           |
| **Class-heavy OOP**        | Porting Java patterns (abstract classes, deep hierarchies) | Composition, interfaces, plain functions    |
| **Barrel file sprawl**     | Re-exporting everything through `index.ts`                 | Direct imports from source modules          |
| **Swallowed errors**       | Empty `catch {}` blocks                                    | Handle, log, or rethrow                     |
| **Type assertions**        | `as Type` to override the compiler                         | Annotations (`const x: Type`) or narrowing  |
| **Mutation in map/filter** | Side effects inside declarative pipelines                  | `forEach` for effects, `map` for transforms |

---

## Tooling

```bash
tsc --noEmit              # Type-check without emitting
npx eslint .              # Lint
npx prettier --check .    # Format check
npx prettier --write .    # Auto-format
npx biome check .         # All-in-one (alternative to eslint + prettier)
```

Formatting is not a debate. Pick `prettier` or `biome` and enforce it in CI.

---

## Quick Reference

- **`const` by default** — `let` only when unavoidable, `var` never
- **`strict: true`** — always, no exceptions
- **`unknown` over `any`** — narrow explicitly
- **`async`/`await`** — not `.then()` chains
- **Named exports** — not default exports
- **`as const`** — not enums
- **`#field`** — not `private` keyword
- **`===`** — not `==`
- **`??`** — not `||` for defaults
- **Spread to copy** — never mutate the original
- **Annotate boundaries** — infer the rest

> These idioms refine but are subordinate to the [Code-Edit Constraints](../../ambient.md#code-edit-constraints).