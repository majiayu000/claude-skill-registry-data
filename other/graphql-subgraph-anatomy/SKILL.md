---
name: graphql-subgraph-anatomy
description: Canonical folder structure and architecture pattern for GraphQL Federation subgraphs under apps/servers/. No concrete reference implementation currently exists on disk — this is the pattern to follow when scaffolding the next one.
---

# GraphQL Subgraph Anatomy

No concrete reference implementation currently exists in `apps/servers/` — the previous
examples (`server1-graphql`, `server2-graphql`, each the GraphQL-facing sibling of a
same-numbered gRPC server) were removed. This doc captures the pattern they established; treat
it as the spec for the next subgraph scaffolded, and update this doc to point at it once one
exists. See `backend-server-anatomy` skill for the sibling gRPC server pattern.

## Folder structure

```
apps/servers/{name}-graphql/
├── Dockerfile
├── README.md
├── .env.sample
├── helm/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-prod.yaml
│   └── templates/deployment.yaml
├── index.ts                  ← entry point, calls src/app.ts
├── package.json              ← scripts: dev, gen (no postinstall — no DB here)
├── tsconfig.json
└── src/
    ├── app.ts                ← ServerApp with ApolloDriver
    ├── clients/
    │   └── {Entity}GrpcClient.ts   ← thin gRPC client to the sibling gRPC server
    ├── configs/
    │   └── graphql/codegen.ts      ← graphql-codegen config
    ├── schemas/
    │   └── graphql/{service}.graphql   ← SDL — not actually a separate file in every
    │                                     reference impl; typeDefs may instead live inline in
    │                                     the router (see below) — check the router first
    ├── routers/
    │   ├── index.ts
    │   └── {Entity}GraphqlRouter.ts    ← extends GraphqlRouter
    └── usecases/
        ├── index.ts
        ├── Create{Entity}UseCase.ts
        ├── Get{Entity}UseCase.ts
        ├── List{Entity}UseCase.ts
        ├── Update{Entity}UseCase.ts
        └── Delete{Entity}UseCase.ts
```

## Architecture axioms

- GraphQL subgraphs **never** have their own database. `.database(...)` is not called in
  `app.ts`. All data access goes through the sibling gRPC server via a `{Entity}GrpcClient` in
  `src/clients/`.
- `{Entity}GrpcClient` wraps the generated gRPC stub (from `api`, see
  `code-generation-pipeline` skill) in plain promise-returning methods; it is registered into
  the DI container as a `singleton(...)` (one persistent connection, not one per request).
- `{Entity}GraphqlRouter extends GraphqlRouter` holds:
  - `get typeDefs()` — the federated SDL for this subgraph. The previous reference servers
    wrote it as a template string directly on the router rather than a separate `.graphql`
    file loaded from disk — follow whichever your target server already does before adding a
    new file. Federated entity types use `@key(fields: "id")` from
    `@link(url: "https://specs.apollo.dev/federation/v2.14", import: ["@key"])`.
  - `get handlers()` — maps `Query`/`Mutation` fields (and any `__resolveReference` for
    federated entity resolution) to UseCase classes, same one-class-per-operation UseCase
    pattern as the backend server.
- UseCases here call the gRPC client, not a repository — they are a thin translation layer
  between the GraphQL field arguments and the gRPC request/response shape.
- Apollo Router composes every subgraph's schema into the supergraph — run `bun run
  supergraph` (root) after any SDL change, or nothing changes at the gateway.

## Scaffolding — never build this by hand

```bash
bun run generate
# select: server, then add the graphql driver to an existing (or new) server
```
