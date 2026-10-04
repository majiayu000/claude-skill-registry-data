---
name: migrate-to-shoehorn
description: Migrate test files from `as` assertions to @total-typescript/shoehorn helpers. Use when tests need partial fixtures, intentionally invalid data, or safer replacements for TypeScript assertions.
---

# migrate-to-shoehorn

Use this skill to migrate **test code only** from TypeScript `as` assertions to `@total-typescript/shoehorn` helpers.

Shoehorn is for tests, fixtures, and test-only helpers. Do not recommend it for production or source files, and do not add `@total-typescript/shoehorn` imports outside `*.test.*` or `*.spec.*` files.

## When To Use

- A test creates a large object but only needs a few properties.
- A test uses `value as Type` to satisfy a function, component, or hook signature.
- A test intentionally passes invalid data and currently uses `value as unknown as Type`.
- A fixture needs a temporary full-shape wrapper while it is being migrated.

Do not use this skill to loosen production typing. If the assertion is in source code, fix the domain type, parser, or test boundary instead.

## Install

Install Shoehorn only when the target repository does not already depend on it, and use the package manager already used by that repository:

```bash
# bun.lock or bun.lockb
bun add -d @total-typescript/shoehorn

# pnpm-lock.yaml
pnpm add -D @total-typescript/shoehorn

# yarn.lock
yarn add -D @total-typescript/shoehorn

# package-lock.json or npm-shrinkwrap.json
npm install --save-dev @total-typescript/shoehorn
```

Do not switch package managers. If multiple lockfiles exist, ask which package manager owns the repo before installing.

## Find Candidate Tests

Search only test files and review every result manually:

```bash
rg "\bas\s+[A-Z][A-Za-z0-9_$]*(<[^>]+>)?" --glob "*.{test,spec}.{ts,tsx}"
rg "\bas\s+unknown\s+as\s+" --glob "*.{test,spec}.{ts,tsx}"
```

Avoid broad replacements. Migrate one assertion at a time so the new helper matches the test intent.

## Migration Patterns

### `value as Type` -> `fromPartial(value)`

Use `fromPartial()` when the test supplies a subset of a larger type and the supplied properties should still type-check.

Before:

```ts
getUser({ body: { id: "123" } } as Request);
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

If TypeScript cannot infer the target from context, provide the target type explicitly:

```ts
const request = fromPartial<Request>({
  body: { id: "123" },
});
```

### `value as unknown as Type` -> `fromAny(value)`

Use `fromAny()` only when the test intentionally passes invalid data, such as exercising validation or error handling paths. This replaces double assertions while keeping the intent visible.

Before:

```ts
getUser({ body: { id: 123 } } as unknown as Request);
```

After:

```ts
import { fromAny } from "@total-typescript/shoehorn";

getUser(fromAny({ body: { id: 123 } }));
```

### Full-Shape Fixtures -> `fromExact(value)`

Use `fromExact()` as a temporary helper when a fixture already has the full shape and you want to keep the migration mechanical before deciding whether it can be reduced.

```ts
import { fromExact } from "@total-typescript/shoehorn";

const request = fromExact<Request>({
  body: { id: "123" },
  headers: {},
  cookies: {},
});
```

Prefer `fromPartial()` once the test only needs a subset of the object. `fromExact()` should not become a dumping ground for unnecessary fixture fields.

## Workflow

1. Confirm the target files are tests (`*.test.ts`, `*.test.tsx`, `*.spec.ts`, or `*.spec.tsx`).
2. Check whether `@total-typescript/shoehorn` is already installed.
3. If installation is needed, use the existing package manager from the repo lockfile.
4. Search for candidate assertions with the `rg` commands above.
5. Replace `value as Type` with `fromPartial(value)` when the supplied data is partial but type-valid.
6. Replace `value as unknown as Type` with `fromAny(value)` when the supplied data is intentionally invalid.
7. Use `fromExact()` only for full-shape fixtures or short-lived migration steps.
8. Add the narrowest import needed from `@total-typescript/shoehorn`.
9. Run the target test file, the repo test suite, and the typecheck command.

## Validation

After migrating, run the repository's normal checks. For a Bun-based repo, use:

```bash
bun run typecheck
bun test
```

Verify Shoehorn remains test-only:

```bash
rg "@total-typescript/shoehorn"
rg "@total-typescript/shoehorn" --glob "!*.{test,spec}.{ts,tsx}"
```

The first command should show only intended test imports. The second command should return no source-file imports; if it finds any, remove Shoehorn from production/source code and fix the underlying type boundary instead.
