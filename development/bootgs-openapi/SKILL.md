---
name: bootgs-openapi
description: Generates an OpenAPI 3.0 specification from bootgs @RestController classes via static TypeScript AST analysis (not runtime reflection), and documents the DTO-first contract workflow between a bootgs backend and its client. Use when adding or changing a bootgs endpoint, keeping openapi.json in sync with controllers, or generating a typed client from a bootgs backend. Not for writing the client that consumes the spec or for debugging a route miss (`bootgs-client`), nor for entry-point wiring (`bootgs-quickstart`).
license: Apache-2.0
compatibility: Requires Node.js and the `typescript` package (already a devDependency in any TS-based bootgs project).
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
  framework: bootgs
---

# Bootgs OpenAPI

## Available scripts

- **`scripts/generate-openapi.ts`** — walks the TS AST and writes an OpenAPI 3.0 `openapi.json`. Run `npx tsx scripts/generate-openapi.ts --help` for the full flag reference.

## Why static analysis, not runtime reflection

bootgs's own routing metadata (via `reflect-metadata`) only exists once a controller class is instantiated inside a live Apps Script execution — there's no server process you can query for its route table from a build machine. Generating a spec at build time means walking the TypeScript AST directly with the `typescript` compiler API, before any of it runs. `scripts/generate-openapi.ts` in this skill does exactly that: it loads your `tsconfig`, finds every class decorated with `@RestController`/`@Controller`, and reads its routes, parameters, and JSDoc straight off the syntax tree.

## DTO-first contract workflow

1. Define or change **one request/response DTO per file** under `domain/dto/`, exported through a barrel `index.ts`. Never share a TS type directly between frontend and backend build targets — `openapi.json` is the only contract boundary; the two sides may not even share a `tsconfig`.
2. Add or change the controller method. Type its parameters and return value with the DTO, and give the method a JSDoc comment — the generator lifts it verbatim into the operation's `description`.
3. Run the generator (see Usage below).
4. Diff-review the produced `openapi.json` before committing — an unexpected diff (a route disappearing, a schema losing a field) usually means a decorator or type the generator can't see, not a real API change.
5. Regenerate/update the frontend client from the spec (see the `bootgs-client` skill for the transport layer the client must speak).

## How the generator resolves a route

For each source file in the TS program:
1. Find `ClassDeclaration`s carrying a decorator whose **identifier text** is `RestController` or `Controller`. This is a textual match, not a type-checked import resolution.
2. Read the first string-literal argument of that decorator as the base path.
3. For each method, look for a routing decorator by the same textual matching: `Get`/`Post`/`Put`/`Delete`/`Patch`/`Head`/`Options`, their `*Mapping` aliases, or `RequestMapping`. The method's own string-literal argument (if any) is appended to the base path.
4. For each parameter, read `@Param`/`@PathVariable` as a `path` parameter, `@Query`/`@RequestParam` as a `query` parameter, and `@Body`/`@RequestBody` as the `requestBody`. The parameter's TypeScript type is resolved through the `TypeChecker` into a JSON Schema fragment under `components.schemas`.
5. Route placeholders (`{id}`) map directly to OpenAPI path parameter syntax — no translation needed, bootgs already uses the OpenAPI convention.

## Usage

```bash
npx tsx scripts/generate-openapi.ts --tsconfig ./tsconfig.appsscript.json --output ./openapi.json
```

Wire it into `package.json`:

```json
{ "scripts": { "openapi:generate": "tsx scripts/generate-openapi.ts --tsconfig tsconfig.appsscript.json --output openapi.json" } }
```

And into CI as a drift check:

```bash
npm run openapi:generate && git diff --exit-code openapi.json
```

## Gotchas

- **Identifier matching, not import resolution.** A local class or a differently-sourced decorator that happens to be named `RestController`/`Get`/etc. will be picked up as if it were bootgs's own. Don't shadow these names.
- **One `@RestController` per class.** The generator takes the first path string-literal it finds; a class with two controller-style decorators produces one path, silently ignoring the second.
- **Path param names must match exactly.** The `{id}` placeholder in the route string and the string passed to `@Param("id", ...)` are matched by exact, case-sensitive string equality to build the `parameters` array — a typo in either produces a spec where the path has a placeholder with no matching declared parameter.
- **Complex types degrade gracefully, not silently correctly.** Primitives, arrays, enums (string literal unions), and flat object/interface shapes resolve to real schemas. Generics, mapped types, and deep conditional types fall back to an open `{}` schema — treat a suspiciously permissive schema in the output as a signal to simplify the DTO's type, not a generator bug to work around.
- **Regenerate before every PR that touches a controller.** The CI drift check above is a floor, not a substitute for running it locally — a stale `openapi.json` merged alongside a route change breaks every client generated from it.

## Verification checklist

- [ ] `openapi.json` reflects every route, including newly added path/query params.
- [ ] `git diff --exit-code openapi.json` passes after running the generator (nothing hand-edited it out of sync).
- [ ] Every schema referenced by an operation actually appears under `components.schemas` (no dangling `$ref`).
