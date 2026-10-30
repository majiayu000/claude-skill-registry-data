---
name: typescript-forms
description: Katara's TypeScript forms, practiced until every move is exact. Use for typescript-best-practices, /typescript-best-practices, "TypeScript best practices", and whenever reading or editing any .ts or .tsx file. Discriminated unions, branded types, constructive modeling, unknown over any, schemas before guards, no as casts, exhaustiveness, satisfies, and boundary validation.
paths: ["**/*.ts", "**/*.tsx"]
---

# Katara's TypeScript forms

A waterbender drills each form until her hands cannot get it wrong. Then, in a real fight, the form holds without thought. Types are forms for code. Shape them so the wrong move cannot be made, and the compiler holds the line when you are not looking.

Apply Type System Discipline (Earth in `four-elements`) first.

| Form | Summary |
|------|---------|
| Discriminated unions | Model variants with a `kind` literal discriminant so impossible states cannot be represented. No optional-field bags. |
| Branded types | Brand primitives with `& { readonly __brand: "X" }` so they cannot be mixed up. Validate once at the boundary. |
| Constructive modeling | Build the shape so the illegal value cannot be constructed. `[T, ...T[]]` for non-empty, `[T, T][]` for even length, `start` plus `duration` for a range. Not a runtime guard, and not a wish for refinement types. |
| Simplest total type | Keep `T[]` while every operation on it stays total. Strengthen to `NonEmpty<T>` only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | External data is `unknown`. |
| Schemas before guards | Before hand-writing a property-by-property type guard, use the repository's runtime schema library and infer the type from the schema, such as `z.infer`. |
| No `as` casts | Every `as` is a runtime crash waiting to happen. Cast only after validation. |
| Narrowing hierarchy | Discriminant switch, then the `in` operator, then `typeof` or `instanceof`, then a user-defined type guard, and `as` last. |
| Type guards | A guard must verify its claim. A lying guard is worse than `as`, because the bug hides behind a name that says it is safe. Name them `isX` or `hasX`. |
| Exhaustiveness | Inline `const _exhaustive: never = x;` in default arms so the compiler errors when a new variant is added. |
| `satisfies` over `as` | Validates the value without widening literal types. |
| Boundary validation | Parse where data crosses in, into a named domain type. `Record<string, unknown>` (however spelled) stops at that parse. Trust the types inside. See Boundary Discipline (Earth in `four-elements`). |
| Schema-derived types | Reach for `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, and `typeof` before declaring a new interface. |
| Object args | Pass objects, not positional arguments, so argument order documents itself. Skip this on hot paths (per-frame render, tokenizers, parsers). |
| Real tests | Do not mock what you can run. Prefer the framework's real test primitives with leak and disposable checks, and verify UI in a running build. Mock only what you cannot run locally. See `push-and-pull`. |
| Structured telemetry | Prefer structured logger diagnostics with enough context to debug from an id. No `console.log` in shipped code. |

Examples for every form: [references/patterns.md](references/patterns.md).
