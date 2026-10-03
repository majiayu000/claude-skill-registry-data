---
name: code-generation-pipeline
description: What is generated, what generates it, and the rules around generated code (proto, GraphQL SDL, Prisma) in this repo.
---

# Code Generation Pipeline

## What is generated — never edit these manually

```
packages/api/src/generated/
├── {service}-grpc/proto/         ← from buf generate (protobuf → TypeScript), only if that
│   ├── {service}.ts                server has a .proto schema
│   ├── {service}_pb.ts
│   └── typeRegistry.ts
├── {service}-graphql/graphql/    ← from graphql-codegen, only if that server has a .graphql
│   ├── context.ts                  schema
│   ├── index.ts
│   ├── resolvers.ts
│   ├── typedefs.graphql
│   └── typedefs.ts
└── index.ts                      ← barrel re-exporting every {service}-*/ above

apps/servers/{service}-grpc/generated/prisma/   ← from `prisma generate` (Prisma client)
```

`packages/api` is a shared package (built with rslib) — every server/subgraph imports its
generated types from `api`, not from another workspace's local `generated/` folder directly.

## What generates it, and how it actually runs

There is **one** codegen entry point per workspace, not separate per-artifact tasks: each
server/subgraph's `package.json` has a `gen` script —

```
"gen": "bun ../../../packages/script/src/bin/generate-api.ts"
```

`generate-api.ts` runs `APIGenerator` (`packages/script/src/generator/APIGenerator.ts`), which:
1. Runs `graphql-codegen --config ./src/configs/graphql/codegen.ts` — only if
   `graphql-codegen` is an installed dependency in that workspace (skipped otherwise, e.g. for
   a gRPC-only server).
2. Runs `buf generate --template ./src/configs/proto/buf.gen.yaml` — only if `protoc` is
   available (skipped otherwise).
3. Writes barrel exports for everything under `packages/api/src/generated/`.

Prisma generation is separate and automatic: each DB-backed server's `package.json` has
`"postinstall": "prisma generate"`, driven by that workspace's own `prisma.config.ts` — it
runs on `bun install`, not via `gen`.

### Triggering regeneration

```bash
# One workspace, after changing its .proto and/or .graphql schema:
cd apps/servers/{service}-grpc && bun run gen
cd apps/servers/{service}-graphql && bun run gen

# Prisma schema changes (schema.prisma) — re-run install, or manually:
cd apps/servers/{service}-grpc && bunx prisma generate

# All workspaces at once, then rebuild the api package:
bun run gen   # root: `turbo run gen && turbo run build --filter=api`
```

There is no `gen:proto` / `gen:graphql` / `gen:prisma` split — that granularity doesn't exist
in this repo; `gen` always regenerates whichever of proto/GraphQL a given workspace actually
has configured.

### After a GraphQL SDL change

Regenerating a subgraph's types does not touch Apollo Router's composed schema — run

```bash
bun run supergraph   # root: turbo run supergraph (packages/script/src/bin/compose-supergraph.ts)
```

to recompose the supergraph after any subgraph's SDL changes.

## Rules

1. NEVER edit any file inside `packages/api/src/generated/` or `apps/servers/*/generated/prisma/`
   — they're overwritten on the next `gen` / `prisma generate` regardless.
2. ALWAYS regenerate (`bun run gen` in the affected workspace) after changing a `.proto`,
   `.graphql`, or `schema.prisma` file, and commit the regenerated output — it's the typed
   contract every consumer imports from `api`.
3. Proto changes that remove or renumber existing fields break wire compatibility with any
   deployed consumer still on the old schema — treat that as a breaking-change migration, not
   a normal edit.
4. After a subgraph's SDL changes, run `bun run supergraph` — a regenerated subgraph with a
   stale supergraph composition is a silent mismatch at the gateway.
