---
name: api-docs
description: "Generate OpenAPI 3.1 documentation from your API codebase. Auto-detects Express, Fastify, NestJS, Django, FastAPI, Flask, Rails, Spring, Go, and more. Triggers: you need API documentation, OpenAPI spec, Swagger docs, endpoint reference, or REST API docs."
version: "2.0.1"
category: docs
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze the project's API
layer and produce complete OpenAPI documentation.

INPUT:
$ARGUMENTS

If no arguments provided, auto-detect the API framework and document all endpoints.
If a specific path, module, or endpoint group is provided, scope documentation to that area.

============================================================
PHASE 1: FRAMEWORK DETECTION
============================================================

Detect the API framework by scanning for config files and import patterns:

| Framework | Detection Signals |
|-----------|------------------|
| Express | `require('express')`, `import express`, `app.get(`, `router.post(` |
| Fastify | `require('fastify')`, `import Fastify`, `fastify.route(`, `fastify.get(` |
| NestJS | `@Controller(`, `@Get(`, `@Post(`, `nest-cli.json` |
| Hono | `import { Hono }`, `new Hono()`, `app.get(` with Hono types |
| Django REST | `urls.py`, `views.py`, `serializers.py`, `rest_framework` imports |
| FastAPI | `from fastapi`, `@app.get(`, `@router.post(`, `APIRouter` |
| Flask | `from flask`, `@app.route(`, `Blueprint` |
| Go net/http | `http.HandleFunc(`, `http.ListenAndServe(`, `mux.Handle(` |
| Gin | `gin.Default()`, `r.GET(`, `r.POST(` |
| Rails | `routes.rb`, `config/routes`, `resources :` |
| Spring | `@RestController`, `@RequestMapping`, `@GetMapping` |
| ASP.NET | `[ApiController]`, `[HttpGet]`, `MapGet(`, `app.MapControllers()` |

Record the detected framework as API_FRAMEWORK for subsequent phases.

If no API framework is detected, check for:
- GraphQL schemas (schema.graphql, typeDefs)
- gRPC proto files (*.proto)
- WebSocket handlers
- Serverless function handlers (Lambda, Cloud Functions)

Report the finding and adapt accordingly.

============================================================
PHASE 2: ROUTE EXTRACTION
============================================================

Systematically extract all API routes:

Step 2.1 -- Find Route Files

Based on API_FRAMEWORK, locate route definitions:
- Express/Fastify/Hono: scan for `router.`, `app.get/post/put/delete/patch`
- NestJS: scan for `@Controller` decorated classes
- Django REST: read all `urls.py` files and `viewsets`
- FastAPI: scan for `@app.` and `@router.` decorators
- Go: scan for `HandleFunc`, `Handle`, `mux.` calls
- Rails: read `config/routes.rb`
- Spring: scan for `@RequestMapping`, `@GetMapping`, etc.

Step 2.2 -- Extract Route Details

For each route, extract:
- HTTP method (GET, POST, PUT, PATCH, DELETE)
- Path pattern (including path parameters like `:id` or `{id}`)
- Handler function name and file location
- Middleware chain (auth, validation, rate limiting)
- Request body schema (from validation libraries, DTOs, or type annotations)
- Response schema (from return types, serializers, or response helpers)
- Query parameters (from parsing logic or decorators)
- Path parameters and their types
- Status codes returned (from explicit responses and error handlers)

Step 2.3 -- Extract Authentication Requirements

Identify auth patterns:
- JWT middleware / Bearer token checks
- API key validation
- Session/cookie auth
- OAuth scopes
- Role-based access control (RBAC) decorators or middleware
- Public vs protected routes

Step 2.4 -- Extract Validation Schemas

Look for request validation:
- Zod schemas
- Joi schemas
- class-validator decorators (NestJS)
- Pydantic models (FastAPI)
- JSON Schema definitions
- TypeScript interfaces/types used for request/response
- Django serializers

============================================================
PHASE 3: OPENAPI SPEC GENERATION
============================================================

Generate an OpenAPI 3.1.0 specification:

Generate a valid OpenAPI 3.1.0 YAML spec with: info (title, description, version
from package config), servers (localhost with detected port), paths (from extracted
routes), components/schemas (from extracted types), and securitySchemes.

For each path item include: operationId, summary, description, tags (grouped by
controller/router or URL prefix), parameters, requestBody, responses with status
codes, and security requirements.

For schemas: convert TypeScript interfaces, Pydantic models, Zod schemas, or Django
serializers to JSON Schema. Mark required vs optional fields. Include examples from
test fixtures or seed data where available. Generate both success and error examples.

============================================================
PHASE 4: INTERACTIVE DOCS SETUP
============================================================

Set up interactive API documentation:

Step 4.1 -- Choose Tool

Based on the framework and existing dependencies:

| Condition | Tool | Setup |
|-----------|------|-------|
| Fastify project | @fastify/swagger + @scalar/fastify-api-reference | Plugin registration |
| Express project | swagger-ui-express | Middleware mount |
| NestJS project | @nestjs/swagger | Module configuration |
| FastAPI project | Built-in (Swagger UI at /docs) | Already available |
| Django REST | drf-spectacular or drf-yasg | Settings configuration |
| Any project | Redoc standalone | Static HTML page |
| Any project | Scalar | CDN-based HTML page |

Step 4.2 -- Integration

If the project supports it, add interactive docs as a development dependency:
- Install the appropriate package
- Add the route/middleware to serve docs (typically at /docs or /api-docs)
- Configure to load the generated OpenAPI spec
- Add a script to package.json or equivalent to regenerate the spec

If the project does not support middleware-based docs, generate a standalone
HTML file using Scalar or Redoc CDN that references the spec file.

============================================================
PHASE 5: VALIDATION
============================================================

Validate the generated spec against the actual codebase:

Step 5.1 -- Route Coverage

- Count total routes extracted from code
- Count total paths in generated spec
- Flag any routes missing from the spec
- Flag any spec paths that do not match actual routes

Step 5.2 -- Schema Accuracy

- Compare generated request schemas against validation middleware
- Compare generated response schemas against actual handler return values
- Flag mismatches or missing schemas

Step 5.3 -- Spec Lint

- Verify the spec is valid OpenAPI 3.1.0
- Check for missing descriptions on operations
- Check for missing response schemas
- Check for undocumented error responses


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing documentation, validate completeness:

1. Verify all required sections are present and non-empty.
2. Verify internal cross-references and links resolve correctly.
3. Verify no placeholder text remains ("{TODO}", "[TBD]", "...", "etc.").
4. Verify code examples are syntactically valid.

IF VALIDATION FAILS:
- Identify which sections are incomplete or contain placeholders
- Re-generate only the deficient sections
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

Write the following files:

1. `docs/openapi.yaml` -- The complete OpenAPI 3.1.0 specification
2. `docs/api-docs.md` -- Human-readable API reference (for GitHub browsing)

Report:

## API Documentation Generated

### Framework
- **Detected:** [framework name and version]
- **API Style:** REST / GraphQL / gRPC / Mixed

### Coverage
- **Total Routes:** N
- **Documented:** N
- **Missing Docs:** N (list any gaps)

### Files Created
- `docs/openapi.yaml` -- OpenAPI 3.1.0 specification
- `docs/api-docs.md` -- Markdown API reference

### Interactive Docs
- **Tool:** [Swagger UI / Redoc / Scalar / Built-in]
- **URL:** [localhost:PORT/docs or path to HTML file]
- **Setup:** [any manual steps needed]

### Endpoint Summary

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /api/users | Bearer | List all users |
| POST | /api/users | Bearer | Create a user |
| ... | ... | ... | ... |

### Validation Results
- Schema mismatches: [list or "none"]
- Missing response docs: [list or "none"]
- Undocumented error codes: [list or "none"]


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /api-docs — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT fabricate endpoints. Only document routes found in the actual code.
- Do NOT include internal/private routes unless they are part of the API surface.
- Do NOT hardcode example API keys, tokens, or secrets in examples.
- Do NOT overwrite an existing OpenAPI spec without reading it first and
  preserving any manually-written descriptions or examples.
- Do NOT install packages in production dependencies -- docs tools go in devDependencies.
- Do NOT generate docs for test endpoints or health checks unless they are
  part of the documented API surface.

NEXT STEPS:

After generating API documentation:
- "Run `/document` to audit overall documentation coverage."
- "Run `/qa` to verify API endpoint behavior matches the spec."
- "Run `/secure` to audit API security (auth, rate limiting, input validation)."
