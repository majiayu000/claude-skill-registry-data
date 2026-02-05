---
name: backend-patterns
description: Backend entity patterns - services with DI, Drizzle schemas (3-file pattern), ORPC routers, TypeIDs, neverthrow. Use when creating services, schemas, routers, or new entities.
---

# Backend Patterns

Use this skill when building backend features. Follow these patterns for consistency.

## Project Setup

Replace these placeholders for your project:
- `@project/` → your package scope (e.g., `@myapp/`)
- `packages/` paths follow standard monorepo layout

Expected packages:
- `@project/db` - Drizzle database client, DB_SCHEMA export
- `@project/shared` - TypeIDs, constants, shared schemas
- `@project/logger` - Pino logger wrapper

## Quick Reference

| Entity Type | Pattern | Files to Create/Modify |
|-------------|---------|------------------------|
| Service | Factory function with deps, neverthrow | `packages/api/src/services/xxx-service.ts`, `context.ts` |
| Schema | 3-file pattern | `.db.ts`, `.zod.ts`, `.relations.ts` in `packages/db/src/schema/` |
| Router | ORPC procedures, Result→Error mapping | `packages/api/src/routers/xxx-router.ts`, `routers.ts` |
| TypeID | Prefixed ID | `packages/shared/src/typeid.schema.ts` |

## Key Conventions

- **db.query** preferred over db.select for simple lookups (see [service.md](service.md))
- **neverthrow** for service error handling, `.match()` in routers (see [router.md](router.md))
- **Zod enums** with `as const` + `z.enum()` pattern (see [schema.md](schema.md))

## Pattern Details

- For service creation, see [service.md](service.md)
- For schema creation, see [schema.md](schema.md)
- For router creation, see [router.md](router.md)

## Workflow: Adding a New Entity

1. **Add TypeID prefix** to `packages/shared/src/typeid.schema.ts`
2. **Create schema files** in `packages/db/src/schema/{domain}/`
3. **Create service** in `packages/api/src/services/`
4. **Add to context** in `packages/api/src/context.ts`
5. **Create router** in `packages/api/src/routers/`
6. **Export router** in `packages/api/src/routers/routers.ts`
7. Run `bun run db:generate` if schema changed
