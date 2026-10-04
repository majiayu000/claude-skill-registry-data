---
name: ait
description: Knowledge pack for AIt — a personal AI platform with monorepo architecture, RAG pipeline, OAuth connectors, and BullMQ scheduling.
metadata:
  author: mateonunez
  version: 1.0.0
  source: private
  stack: pnpm monorepo, Fastify, Drizzle ORM, Qdrant, Ollama, BullMQ, React + Vite
---

# ait

Personal AI platform built as a pnpm monorepo. Connects to external services (GitHub, Spotify, Linear, Notion, Slack, Google) via OAuth, syncs data through an ETL pipeline, stores embeddings in Qdrant, and provides RAG-powered AI responses via Ollama.

## Preferences

- **Package manager**: pnpm (corepack, workspace protocol)
- **Linter/formatter**: Biome 1.9 — 2-space indent, single quotes, semicolons
- **Error handling**: `Result<T, E>` pattern with `ok()` / `err()` — never throw in business logic
- **Testing**: Node.js native `node:test` with `describe`/`it`, `borp` runner, `c8` coverage
- **Naming**: PascalCase classes, `I` prefix interfaces, camelCase methods, SCREAMING_SNAKE constants, kebab-case files
- **Type files**: `.types.ts`, spec files: `.spec.ts`
- **All packages**: scoped `@ait/*`

## References

| Category | Reference | Description |
|----------|-----------|-------------|
| Core | [core-architecture](references/core-architecture.md) | Layered architecture, data flow, package structure |
| Core | [core-entity-types](references/core-entity-types.md) | Normalized entity types with `__type` strings |
| Core | [core-result-type](references/core-result-type.md) | `Result<T,E>`, `ok()`, `err()` usage patterns |
| Features | [features-oauth](references/features-oauth.md) | Encrypted credentials, factory pattern, token refresh |
| Features | [features-rag](references/features-rag.md) | Qdrant, multi-query retrieval, reranking, streaming |
| Features | [features-scheduler](references/features-scheduler.md) | BullMQ, priority queues, repeatable jobs |
| Features | [features-connectors](references/features-connectors.md) | GitHub, Spotify, Linear, Notion, Slack, Google connectors |
| Best Practices | [best-practices-testing](references/best-practices-testing.md) | Node.js native test runner, Docker services, c8 coverage |

## Quick Reference

```bash
# Development
pnpm dev                    # Start all packages in parallel
pnpm start:services         # Docker: PostgreSQL, Qdrant, Redis, Ollama, MinIO
pnpm test                   # Run all tests (starts test services automatically)
pnpm migrate                # Run Drizzle migrations
pnpm generate:openapi       # Generate OpenAPI specs for connectors

# Ports
# PostgreSQL: 5432 | Qdrant: 6333 | Redis: 6379
# Ollama: 11434 | MinIO: 9090 | Langfuse: 3333
# Gateway: 3000 | UIt (UI): 5173

# Models (env)
GENERATION_MODEL=gemma3:latest
EMBEDDINGS_MODEL=mxbai-embed-large:latest
```

```typescript
// Result pattern
const result = await someOperation();
if (result.ok) {
  console.log(result.value);
} else {
  console.error(result.error);
}

// Connector factory
const service = connectorServiceFactory.getServiceByConfig(configId, userId);
```
