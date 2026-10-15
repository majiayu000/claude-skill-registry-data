---
name: boundary-driven-defense
description: Enforce boundary-driven defense strategy — parse at system boundaries, trust types internally, crash on invariant violations. Use when writing validation logic, adding error handling, reviewing defensive code, or when code has redundant null checks, scattered Zod schemas, or try-catch blocks deep inside business logic.
---

# Boundary-Driven Defense

Defense belongs at system boundaries. Internal code trusts the type system.

## Core Principle

```
System boundary  → parse (runtime validation, reject invalid data)
Module internals → trust (type system guarantees, zero redundant checks)
Invariant broken → crash (fail fast, never silently correct)
```

## System Boundaries (Parse Here)

A boundary is where data crosses a trust boundary — from uncontrolled to controlled.

| Boundary                 | Example                               |
| ------------------------ | ------------------------------------- |
| API route handler        | `User.parse(await req.json())`        |
| Environment variables    | `EnvSchema.parse(process.env)`        |
| Third-party API response | `ApiResponse.parse(await res.json())` |
| URL / search params      | `QuerySchema.parse(searchParams)`     |
| localStorage / cookies   | `Settings.parse(JSON.parse(raw))`     |
| File system reads        | `Config.parse(yaml.parse(content))`   |
| Message queue consumer   | `Event.parse(message.body)`           |

Use **parse, not validate** — the result must carry the validated type so downstream code gets compile-time guarantees, not just a runtime boolean.

```typescript
// parse: unknown → User, type-safe from here on
const user = UserSchema.parse(raw);

// validate: returns boolean, type unchanged, compiler learns nothing
if (isValidUser(raw)) {
  /* raw is still unknown */
}
```

## Internal Code (Trust Here)

After parsing at the boundary, internal functions receive typed data. Do not re-validate.

```typescript
// boundary
async function handleRequest(req: Request) {
  const user = UserSchema.parse(await req.json());
  await saveUser(user);
}

// internal — User type is the contract, no defensive checks
async function saveUser(user: User) {
  await db.users.insert(user);
}
```

**Anti-patterns to reject in code review:**

- Zod `.parse()` / `.safeParse()` inside business logic or utility functions
- `if (!user)` checks when `user: User` already excludes nullability
- `if (!user.email)` checks when the type requires `email: string`
- try-catch around internal function calls that cannot throw by contract
- Optional chaining (`?.`) on non-optional typed properties

## Invariants (Crash Here)

An invariant is a condition that must always hold if the code is correct. Violation means a bug in your code, not bad input.

- **Do not** silently correct — this hides the root cause.
- **Do not** return a fallback — this lets the bug survive.
- **Do** fail fast at the current execution boundary.

```typescript
// correct: crash exposes the bug with a stack trace
console.assert(items.length > 0, "invariant: items must not be empty after filter");

// wrong: silent correction hides a logic error
if (items.length === 0) {
  items = [defaultItem]; // who broke the filter?
}
```

"Crash" is context-dependent:

| Context           | Crash means                                                       |
| ----------------- | ----------------------------------------------------------------- |
| Library / utility | `throw` — let the caller's error boundary handle it               |
| API request       | 500 response — this request fails, process stays alive            |
| React component   | Error boundary catches — component tree fails, rest of page works |
| Background job    | Job fails and retries — other jobs unaffected                     |

The point is not killing the process — it is **refusing to continue the current operation in an inconsistent state**.

## Decision Checklist

When writing error handling, ask:

1. **Is this data from outside my trust boundary?** → Parse at the boundary with a schema.
2. **Is this data already typed from a prior parse?** → Trust the type. Remove the check.
3. **Is this a condition that should never be false if my code is correct?** → Assert. Do not handle gracefully.
4. **Is this a recoverable runtime failure (network, disk, timeout)?** → Handle with error recovery (retry, fallback, user message).

## Common Operator Misuse

### `?.` — Optional Chaining

Only use on properties whose type includes `undefined` or `null` with genuine business semantics.

```typescript
// wrong: User.name is string, not string | undefined
return <h1>{user?.name}</h1>;

// right: bio is optional by business rule
return <p>{profile.bio?.slice(0, 100)}</p>;
```

If you find `?.` everywhere, the root cause is usually one of:

- Boundary parse is missing, so types default to `T | undefined`
- Types are over-permissive (`Partial<T>` leaking beyond creation flows)
- API codegen emits nullable types by default — fix the codegen config or narrow at the boundary

### `??` and `||` — Fallback Operators

Fallbacks should express intentional defaults for valid optional states, not mask data problems.

```typescript
// right: displayName is optional, fallback is a UX decision
const label = user.displayName ?? "Anonymous";

// wrong: name is required — a fallback hides the bug that produced ""
const label = user.name || "Unknown";
```

If a field should never be empty, enforce it in the schema (`z.string().min(1)`), not with a runtime fallback at every call site.

### Type Width Is the Root Cause

When operators like `?.`, `??`, `||` appear on fields that "shouldn't" be empty or absent, the fix is almost always to tighten the type or schema — not to add more operators.

| Symptom                         | Fix                                                                       |
| ------------------------------- | ------------------------------------------------------------------------- |
| `?.` on required fields         | Remove `?` from the type definition; ensure parse rejects `undefined`     |
| `\|\|` fallback on strings      | Add `.min(1)` to schema; distinguish `null` (unset) from `""` (empty)     |
| `?? 0` on numbers               | Decide if `0` is valid; if not, parse with `.positive()` or `.min(1)`     |
| `Partial<T>` leaking everywhere | Create separate types: `CreateInput` (partial) vs `Entity` (all required) |

## Smell: Defense in the Wrong Place

If you find yourself adding defensive code deep inside a module, the real problem is usually one of:

- **Boundary parse is missing** — raw data leaked past the entry point.
- **Type is too wide** — use branded types, discriminated unions, or `NonEmptyArray<T>` to encode the constraint.
- **Contract is unclear** — the function signature does not express its preconditions.

Fix the root cause at the boundary or in the type definition, not by adding checks at the call site.
