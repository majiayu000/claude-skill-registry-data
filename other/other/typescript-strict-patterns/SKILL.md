---
name: typescript-strict-patterns
description: Use when writing or reviewing any TypeScript code. Covers tsconfig, ESLint strict config, Zod at boundaries, discriminated unions, branded types, and safe access patterns.
globs: ["**/*.ts", "**/*.tsx"]
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor
---

# TypeScript Strict Patterns

## tsconfig: Use @total-typescript/tsconfig

Always extend `@total-typescript/tsconfig`. Pick a base by: **build tool** (`tsc/` or `bundler/`), **runtime** (`dom/` or `no-dom/`), **project type** (`app`, `library`, `library-monorepo`).

```json
{
  "extends": "@total-typescript/tsconfig/tsc/no-dom/app",
  "compilerOptions": { "outDir": "./dist", "rootDir": "./src" }
}
```

The base enables `strict`, `noUncheckedIndexedAccess`, `noImplicitOverride`, `verbatimModuleSyntax`, `isolatedModules`, and correct `module`/`lib` for the target. Read the source bases before adding overrides.

## ESLint Baseline

Projects using this skill expect the following flat config (or equivalent rules). Lint-enforceable rules live here, not in prose.

```javascript
// eslint.config.mjs — baseline expected by typescript-strict-patterns
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  eslint.configs.recommended,
  tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: { projectService: true },
    },
    rules: {
      "@typescript-eslint/switch-exhaustiveness-check": "error",
      "@typescript-eslint/no-unnecessary-condition": "error",
      "no-restricted-syntax": [
        "error",
        { selector: "TSEnumDeclaration", message: "Use const arrays or z.enum()" },
      ],
    },
  },
  {
    files: ["**/*.test.ts", "**/*.spec.ts"],
    rules: {
      "@typescript-eslint/no-non-null-assertion": "off",
      "@typescript-eslint/no-explicit-any": "off",
      "@typescript-eslint/no-unsafe-assignment": "off",
    },
  },
);
```

Key rules enforced: no `enum` (use const arrays or `z.enum()`), exhaustive `switch`, no `!`/`as` in production (relaxed in tests).

## ts-reset

Install `@total-typescript/ts-reset` in application code (not libraries) to fix built-in return types (`.filter(Boolean)`, `.json()`, `Map.get`, etc.). Import once in a global `.d.ts`.

## Discriminated Unions + Exhaustive Checking

Model variants as discriminated unions — never bags of optional properties:

```typescript
// GOOD — each variant carries exactly its data
type Result =
  | { status: "ok"; data: string }
  | { status: "error"; message: string };

// Exhaustive check helper — will fail to compile if a variant is missed
function assertNever(x: never): never {
  throw new Error(`Unexpected: ${JSON.stringify(x)}`);
}

function handle(r: Result) {
  switch (r.status) {
    case "ok": return r.data;
    case "error": return r.message;
    default: assertNever(r); // compile error if a case is missing
  }
}
```

Use `satisfies never` or the `assertNever` helper at the `default:` branch. ESLint's `switch-exhaustiveness-check` enforces this at lint time.

## Branded Types

Prevent accidental interchange of structurally identical types with a brand:

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function getUser(id: UserId) { /* ... */ }

const uid = "abc" as UserId; // cast once at the boundary
getUser(uid);    // OK
getUser("abc");  // compile error — plain string is not UserId
```

Brand at system boundaries (API response parsing, DB reads). Internal code then carries the brand without further casts.

## Template Literal Types

Enforce string formats at the type level:

```typescript
type HexColor = `#${string}`;
type Route = `/${string}`;
type EventName = `on${Capitalize<string>}`;

function setColor(c: HexColor) { /* ... */ }
setColor("#ff0000"); // OK
setColor("red");     // compile error
```

Useful for config keys, route paths, and event names where runtime validation is overkill but typos are common.

## No `!` or `as` in Production Code

Non-null assertions (`!`) and type assertions (`as`) are banned in production code. They hide type errors. Allowed in test files where the tradeoff is acceptable (enforced by ESLint config above).

Replacements:
- **Destructuring with defaults** instead of `obj.prop!`: `const { name = '' } = config;`
- **`.at()` + nullish coalescing** instead of `arr[0]!`: `const first = arr.at(0) ?? fallback;`
- **Guard clause** instead of `value as Foo`: narrow with a type guard, then the type flows naturally.

## Const Arrays Over Enums

Never use `enum` (enforced by ESLint). Use `as const` arrays with derived types:

```typescript
const STATUSES = ["pending", "active", "done"] as const;
type Status = (typeof STATUSES)[number];
```

At system boundaries where Zod already validates, prefer `z.enum(STATUSES)` — it gives you the union type and runtime validation in one step.

## Zod Schemas at System Boundaries

Use Zod schemas as the single source of truth for data crossing system boundaries (disk I/O, env vars, API responses, config files). Derive types with `z.infer<>` — never duplicate a hand-written interface alongside a schema.

```typescript
export const sessionMetaSchema = z.object({
  token: z.string(),
  status: z.enum(["running", "completed", "error"]),
});
export type SessionMeta = z.infer<typeof sessionMetaSchema>;
```

- Use `safeParse()` for data that may be corrupt (disk reads, JSONL) — skip gracefully
- Use `parse()` for startup validation (env vars) where failure is fatal
- Skip Zod for internal function arguments between trusted modules and for SDK-owned types

## Safe Indexed Access

With `noUncheckedIndexedAccess`, bracket access returns `T | undefined`. Always narrow:

- Use `.at(index)` — clearer intent than bracket access
- Handle with `if (item !== undefined)` or `??`
- Prefer `.find()`, `.filter()`, or destructuring over index access

## Type Helpers (type-fest as Inspiration)

Use [type-fest](https://github.com/sindresorhus/type-fest) as a **reference catalog** when strict patterns make code verbose. Browse its source for solutions like `SetRequired`, `Simplify`, `JsonValue`. Copy the single type definition you need into `src/types/` with attribution. Don't add the full package as a dependency — keep the dependency graph small.
