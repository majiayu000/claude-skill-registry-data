---
name: openapi-drift
description: This skill should be used when the user mentions "openapi", "swagger", "spec drift", "api contract", "breaking change", "oasdiff", "graphql schema", "api versioning", "the docs don't match the code", "requestBody", "response schema", or reconciling an API specification with its handler code. It provides a static methodology for detecting spec-vs-code drift across web frameworks and for classifying changes as breaking or non-breaking with oasdiff-style semantics.
---

# OpenAPI Drift

## Purpose
Provide a standardized, static methodology for keeping an API specification and its implementation in sync, without starting the server. Two problems live here: **drift** (the spec and the code disagree about what the API does) and **breaking-change classification** (does a change to the surface break existing clients?). Both are read off the source: OpenAPI/Swagger YAML/JSON or GraphQL SDL on one side, and framework route/validation/serializer code on the other. This is the gap left when Optic (the popular OSS drift tool) was archived in January 2026.

## The two-model method
1. **Build the spec model**: endpoints (path + method), parameters, request/response schemas per status, required/nullable, security. From OpenAPI `paths`/`components`, or GraphQL `type`/`input`/`enum`/field args.
2. **Build the code model**: the same facts, read from the framework (routes, validators, DTOs, serializers, status calls). See `references/drift-signals.md`.
3. **Align** by path template + method (normalize `/x/{id}` ≡ `/x/:id`) or GraphQL type + field.
4. **Diff each axis** and record which side each fact came from, that provenance is what lets you assign authority.

## Drift classes and default authority

| Drift class | Example | Usually authoritative |
|---|---|---|
| Undocumented endpoint | Route in code, absent from spec | Code (add to spec) |
| Phantom endpoint | Endpoint in spec, no handler | Code (remove/implement), confirm intent |
| Missing param | Handler reads `?status`, spec omits it | Code |
| Param type mismatch | Spec `integer`, code parses string | Investigate; often code |
| Response field mismatch | Code returns a field the schema lacks | Depends, may be intentionally internal |
| Status-code mismatch | Code returns `409`, spec lists only `200/400` | Code |
| Nullability mismatch | Spec `nullable: false`, code can return null | Code (bug) or spec (fix) |
| Auth mismatch | Spec `security: []`, code requires a token | Code |

"Authoritative" is a default, not a law: a deliberate public contract can be the source of truth over an accidental code change. When ambiguous, surface it for a human rather than silently rewriting either side.

## Breaking vs non-breaking, in one rule
Direction decides safety: **request** schemas are contravariant, *widening is safe, narrowing breaks*; **response** schemas are covariant, *adding is safe, removing breaks*. Adding a required request field, narrowing a type, removing a response field, changing a status code, or dropping/renaming anything are the breaking cases. The full matrix is in `references/breaking-change-rules.md`.

## Semver mapping
- Any breaking change → **major**.
- Backward-compatible additions → **minor**.
- Description/example/docs-only → **patch**.
- Unclassifiable (dynamic schema, external `$ref` moved, `oneOf` reshuffle) → default to **breaking** until a human confirms.

## Additional Resources
### Reference Files
- **`references/drift-signals.md`**: per-framework: exactly where routes, params, request/response schemas, and status codes live in Express, Fastify, NestJS, Koa, FastAPI, Django REST Framework, Flask, Spring Boot, Go net/http/Gin, and Rails, plus GraphQL SDL vs resolvers, and how to read each into the code model.
- **`references/breaking-change-rules.md`**: the full breaking vs non-breaking classification for request bodies, response bodies, parameters, status codes, enums, and nullability, with oasdiff-style semantics and GraphQL-specific rules.
