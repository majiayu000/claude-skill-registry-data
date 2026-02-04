---
name: noop-generator
description: Generate production-ready Express + TypeScript + PostgreSQL + Redis projects. Use when the user wants to create a new backend service, API, or microservice from scratch. Automatically invoked when discussing project scaffolding or generation.
---

# Noop Generator Skill

This skill generates complete backend projects following a function-first, layered architecture.

## When Claude Should Use This

Automatically use this skill when the user:
- Wants to create a new backend service or API
- Asks to scaffold or generate a new project
- Needs a production-ready Express + TypeScript template
- Wants to generate a microservice
- Mentions "noop" and creating something new

## Framework Context

### Core Philosophy
@docs/universal-framework/PHILOSOPHY.md

### Architecture Specification
@docs/universal-framework/ARCHITECTURE_SPEC.md

### Scaffolding Specification
@docs/universal-framework/SCAFFOLDING_SPEC.md

### Generator Instructions
@docs/universal-framework/GENERATOR_INSTRUCTIONS.md

---

## Template Location

The scaffold template is at: `scaffold-template/`

## Placeholder System

| Placeholder | Format | Example |
|-------------|--------|---------|
| `{{PROJECT_NAME}}` | lowercase-dashes | `my-api-service` |
| `{{PROJECT_DESCRIPTION}}` | Free text | `API for user management` |
| `{{DATABASE_NAME}}` | lowercase_underscores | `my_api_service` |
| `{{DEFAULT_PORT}}` | Number | `3005` |
| `{{EXAMPLE_ENTITY}}` | PascalCase | `Widget` |
| `{{EXAMPLE_ENTITY_LOWER}}` | camelCase | `widget` |
| `{{EXAMPLE_ENTITY_PLURAL}}` | lowercase plural | `widgets` |
| `{{EXAMPLE_TABLE}}` | snake_case | `widgets` |

## Generated Project Structure

```
{project-name}/
├── src/
│   ├── index.ts              # Entry point
│   ├── config.ts             # Zod-validated configuration
│   ├── routes.ts             # Route registration
│   ├── handlers/             # HTTP handlers
│   │   └── services/         # Business logic
│   ├── middleware/           # Auth, error handling
│   ├── db/pg/                # PostgreSQL layer
│   │   ├── PgClientStore.ts  # Aggregated Ops
│   │   └── migrations/sql/   # Versioned migrations
│   ├── redis/                # Caching
│   ├── types/                # Domain types
│   └── utils/                # Logger, errors, validation
├── .claude/                  # Claude config for the project
│   ├── CLAUDE.md            # Architecture guidelines
│   └── hooks/               # Auto-lint, pattern checks
├── docker-compose.yml        # Postgres + Redis
└── Dockerfile               # Production build
```

## Key Principles

1. **No fallbacks** - Errors are explicit, never hidden
2. **Explicit dependencies** - Pass dbStore as parameter
3. **Organization scoping** - Every DB op requires organizationId
4. **Type safety** - Never use `any`
5. **Fail fast** - Validate configuration at startup

## Verification

After generation:
- `npm run typecheck` passes
- `npm run lint` passes
- `npm run build` succeeds
- `GET /healthz` returns 200
