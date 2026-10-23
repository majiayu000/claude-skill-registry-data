---
name: ts-patterns
description: Guides framework-agnostic TypeScript types, modules, and async code.
  Use when designing typed APIs, configuring strict tsconfig, or publishing ESM and
  CJS libraries.
---

# TypeScript Development Patterns

Idiomatic TypeScript patterns for building safe, maintainable, inference-friendly
applications and libraries. TypeScript is JavaScript with a layered type system;
this skill covers language-level idioms, the type system, modules, async,
cross-runtime concerns, and the Vite + Vitest toolchain stack. Framework-agnostic —
for Next.js, React components, or Node backend architecture, defer to
`nextjs-ux-ui-expert`, `frontend-ui-developer`, or `nodejs-backend-architect`.

## Critical Rules

- Strict `tsconfig`: `"strict": true`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`.
- `catch` binds `unknown` — narrow explicitly; never assume `Error`.
- Discriminated unions with `never` exhaustiveness for states; `satisfies` over annotation.
- Inference-first APIs: design so callers don't pass type arguments.
- `Result<T, E>` for expected failures; `throw` only for bugs.
- Pass `AbortSignal` through every async call boundary.
- Web standards first (`fetch`, `URL`, `crypto.subtle`); `node:` prefix when Node-only.

## References

Paths are relative to this SKILL.md's directory. Read only the file that matches the task. If a file cannot be read, say so.

- [references/types-errors-modules.md](references/types-errors-modules.md)
  Read when: type system (generics, conditional types, discriminated unions, `satisfies`, branded types, `unknown` narrowing in `catch`); error handling with `Result` for expected failures; modules, ESM/CJS dual publishing, `exports` maps.

- [references/async-runtimes-tooling.md](references/async-runtimes-tooling.md)
  Read when: async and concurrency with `Promise` combinators and `AbortController`; iterators and higher-order functions; runtimes (Node/Deno/Bun/browser/edge); Vite + Vitest toolchain.

## When to Use

- Writing new TypeScript code
- Reviewing TypeScript code
- Refactoring existing TypeScript
- Designing libraries for npm (dual ESM/CJS publishing)
- Tuning `tsconfig.json` for strict mode
- Choosing a runtime (Node / Deno / Bun / browser / edge)
- Configuring Vite for apps or libraries

## How It Works

This skill enforces idiomatic TypeScript across seven key areas: a strict,
type-driven design that encodes invariants into the compiler; generic APIs where
inference flows naturally so callers don't annotate; discriminated unions with
`never` exhaustiveness to make illegal states unrepresentable; errors as values
with `unknown` in `catch` and typed boundaries; ESM-first modules with dual-publish
`exports` maps for libraries; `Promise`/`AbortController`-based async with Web
standards preferred over Node-only APIs; and a Vite + Vitest toolchain on a Node
host with clean paths to Deno, Bun, browser, and edge deploys.

## Core Principles

1. **Strict by default** — `"strict": true`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`
2. **Inference over annotation** — design APIs so callers don't pass type arguments
3. **Errors as values** — `Result<T, E>` at expected-failure boundaries; narrow `unknown` in `catch`
4. **Type-driven design** — encode invariants in types, not comments
5. **Zero-`any`** — except at clearly documented external boundaries
6. **Cross-runtime aware** — Web standards first; `node:` prefix when Node-only

## Quick Reference: TypeScript Idioms

| Idiom                       | Description                                                                        |
| --------------------------- | ---------------------------------------------------------------------------------- |
| Strict by default           | `"strict": true` + `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes`       |
| Discriminated unions        | Model states as `\| { kind: 'a'; … } \| { kind: 'b'; … }` + `never` exhaustiveness |
| `satisfies` over annotation | Preserves literal types while type-checking against a wider shape                  |
| `unknown` in `catch`        | Narrow explicitly; never assume `Error`                                            |
| Errors as values            | `Result<T, E>` for expected failures; throw for bugs                               |
| Inference-first APIs        | Design so callers don't pass type arguments                                        |
| Branded types               | `T & { readonly [brand]: true }` prevents primitive mixups                         |
| ESM-first + `exports` map   | Dual-publish with conditional exports; `sideEffects: false`                        |
| `AbortController`           | Thread `signal` through every async boundary                                       |
| Web standards first         | Prefer `fetch` / `URL` / `crypto.subtle` over Node-only when portable              |
| `readonly` at boundaries    | Signal intent; prevent accidental mutation                                         |
| Union over `enum`           | `const` object + `keyof typeof` instead of `enum`                                  |

## Anti-Patterns to Avoid

```ts
// Bad: `any` leaks type errors everywhere
function process(data: any) {
  return data.items.map((x: any) => x.name); // zero type safety
}

// Bad: double-cast bypasses the type system
const user = json as unknown as User; // use zod/valibot to parse+validate instead

// Bad: non-null assertion `!` in production code
const el = document.getElementById('root')!.innerHTML; // crashes if null

// Bad: `namespace` (legacy; use modules)
namespace MyLib {
  export function foo() {}
}

// Bad: `enum` (generates runtime code, weird semantics)
enum Status {
  Active = 'active',
  Inactive = 'inactive',
}
// Better: const object + union type
const Status = { Active: 'active', Inactive: 'inactive' } as const;
type Status = (typeof Status)[keyof typeof Status];

// Bad: `Function` / `Object` / `{}` (no safety)
function run(cb: Function) {
  cb();
}
// Better: explicit signature
function runGood(cb: () => void) {
  cb();
}

// Bad: throwing from a library where failure is part of the contract
export function parseConfig(text: string): Config {
  const data = JSON.parse(text); // throws — caller may not expect
  return data;
}
// Better: return a Result or throw a typed error

// Bad: blocking in async context
async function badAsync() {
  const buf = fs.readFileSync('file.txt'); // blocks the event loop
}
// Better:
import { readFile } from 'node:fs/promises';
async function goodAsync() {
  const buf = await readFile('file.txt');
}

// Bad: fire-and-forget await
async function saveUser(user: User): Promise<void> {
  /* … */
}
saveUser(user); // errors swallowed silently
// Enable `@typescript-eslint/no-floating-promises` to catch this

// Bad: `as` cast instead of narrowing
function handle(value: unknown) {
  const str = value as string;
  return str.toUpperCase(); // crashes if value is not a string
}
// Better: type guard
function handleGood(value: unknown) {
  if (typeof value !== 'string') throw new TypeError('expected string');
  return value.toUpperCase();
}
```

**Remember**: Great TypeScript is invisible. Let the type system encode invariants,
let inference do the work, and reach for `any` only at clearly documented boundaries.
If the compiler can't catch it, the runtime will — and by then it's too late.
