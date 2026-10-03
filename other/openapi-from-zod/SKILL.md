---
name: openapi-from-zod
description: Generating an OpenAPI spec from existing Zod schemas instead of hand-writing or duplicating one. Use when a TypeScript API already validates requests/responses with Zod and needs published API docs, a client-generation source, or a contract-testing artifact.
---

# OpenAPI from Zod

If request/response shapes are already defined as Zod schemas (this is exactly the
`packages/shared`-style pattern this template's example app uses), don't hand-write a
second, parallel OpenAPI document — generate it from the schemas that are already the
source of truth. A hand-maintained spec drifts from the code the first time someone
changes a schema and forgets the doc; a generated one can't drift.

## Picking a library

- **Zod v4 project → [`zod-openapi`](https://github.com/samchungy/zod-openapi).**
  Attaches OpenAPI metadata with Zod's own `.meta()` (no `extendZodWithOpenApi` step,
  no parallel `.openapi()` method to remember) and produces 3.1.x documents via a
  single `createDocument()` call. This is the lower-friction default for anything on
  Zod v4.
- **Zod v3 project → [`@asteasolutions/zod-to-openapi`](https://github.com/asteasolutions/zod-to-openapi).**
  Requires `extendZodWithOpenApi(z)` once at startup, then a `OpenAPIRegistry` to
  `.register()` schemas and `.registerPath()` per route before generating with
  `OpenApiGeneratorV31`. More ceremony, but it's the established option pre-v4.
- **Only need JSON Schema, not a full OpenAPI document** (e.g. feeding a schema to an
  LLM tool-use definition or a non-HTTP validator) → [`zod-to-json-schema`](https://github.com/StefanTerdell/zod-to-json-schema)
  — skip OpenAPI's request/response/path envelope entirely.

Check `package.json`/lockfile for the installed Zod major version before picking —
don't assume; the two OpenAPI libraries above are not interchangeable.

## Where metadata belongs

Add `description`/`example` (and `id` for anything that should become a reusable
`#/components/schemas/*` ref instead of being inlined everywhere it's used) directly
on the shared schema definitions, not on ad-hoc copies at each call site. If a schema
is already exported from a shared package for both server validation and client
typing, the OpenAPI metadata is one more thing that schema owns — keep it in the same
file as the schema, not scattered across route handlers.

## Generating and keeping it current

- Generate into a build/output directory (e.g. `docs/openapi.json`), not by hand-
  editing the generated file — same discipline as `.claude/code-graph/graph.json` in
  this template: it's a cache of the schemas, not something to diverge from them.
- Wire generation into a script (`scripts/generate-openapi.ts` or equivalent) rather
  than a one-off REPL session, so it's re-run — and the output re-committed or
  re-published — every time a schema changes, not just once at setup.
- If the spec is published (a docs site, a client-generation pipeline), treat a
  schema change that alters the generated spec's shape the same way `api-design`'s
  versioning guidance treats any other breaking API change — this is a good moment to
  apply that skill's rules, not a separate concern.
- CI can diff the freshly generated spec against the committed one and fail if they
  disagree, catching a schema change that someone forgot to regenerate docs for
  before merging — worth adding once the generation script exists.
