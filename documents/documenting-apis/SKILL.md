---
name: documenting-apis
description: >
  Generate API specification documentation from codebase analysis.
  Detects REST endpoints, function signatures, type definitions, and schemas.
  Triggers: API specification, endpoints, REST API, type definitions,
  OpenAPI, Swagger, API documentation.
allowed-tools: Read, Write, Grep, Glob, Bash, Task
---

# docs:api - API Specification Generation

Auto-generate API documentation from codebase analysis.

## Detection Items

| Category | Targets |
| --- | --- |
| REST Endpoints | Express, Fastify, Hono, Next.js, Flask, FastAPI, Django REST |
| Functions | tree-sitter extraction, TypeScript types, JSDoc, docstrings |
| Types | interface, type, Zod, Yup, dataclass, Pydantic |
| OpenAPI | openapi.yaml/json, swagger.yaml/json |

## Framework Detection Patterns

| Framework | Pattern |
| --- | --- |
| Express/Fastify/Hono | `app.get()`, `router.post()` |
| Next.js | `app/api/**/route.ts`, `pages/api/**/*.ts` |
| Flask | `@app.route()` |
| FastAPI | `@app.get()`, `@app.post()` |
| Django REST | `@api_view` |

## Analysis Scripts

| Script | Purpose |
| --- | --- |
| `scripts/detect-endpoints.sh` | HTTP method, path, handler, file location |
| `scripts/extract-types.sh` | Type name, fields, related types |

## Generated Structure

```markdown
# API Specification

## Endpoint List
### GET /api/users
**Request**: params table
**Response**: JSON example

## Type Definitions
### User
| Field | Type | Description |
```

## Usage

```bash
/docs:api                    # Generate API docs
"Generate API specification" # Natural language
```

## Markdown Validation

After generation, validate output with:

```bash
~/.claude/skills/scripts/validate-markdown.sh {output-file}
```

Non-blocking (warnings only) - style issues don't block document creation.

## References

- Related: `documenting-architecture`, `setting-up-docs`, `documenting-domains`
