---
model_tier: medium
name: api-endpoint
description: "Use when creating an API endpoint or HTTP route handler — detects the project stack and routes to the matching carve-out (laravel-api-endpoint, nextjs-patterns, symfony-workflow)."
domain: engineering
workspaces:
  - engineering
packs:
  - engineering-base
---

# api-endpoint


> **Grounded corpus:** endpoint-shape decisions (pagination, error
> shape, idempotency, rate limits) are grounded via the
> [`api-design`](../api-design/SKILL.md) corpus — `./scripts-run
> <skills-root>/corpus-grounding/scripts/ground search
> --manifest <skills-root>/api-design/data/manifest.json "<concern>"`.

## When to use

Use this skill when the user asks to create a new API endpoint, REST route, or HTTP handler.

Do NOT use when:
- Modifying existing endpoints — use the code-refactoring skill.
- API design decisions (versioning, deprecation, contract shape) — use [`api-design`](../api-design/SKILL.md).

## Stack routing

Detect the stack, then hand off to the matching carve-out skill for the framework-specific procedure (file layout, validation primitive, response-shaping convention).

| Detected stack | Carve-out skill |
|---|---|
| Laravel (`artisan` + `composer.json` with `laravel/framework`) | [`laravel-api-endpoint`](../laravel-api-endpoint/SKILL.md) |
| Symfony (`bin/console` + `composer.json` with `symfony/framework-bundle`) | [`symfony-workflow`](../symfony-workflow/SKILL.md) |
| Next.js (`next` in `package.json`) | [`nextjs-patterns`](../nextjs-patterns/SKILL.md) |
| Express / Fastify / NestJS / plain Node | follow project conventions in `agents/` + `package.json scripts` |
| FastAPI / Django / Flask | follow project conventions in `agents/` + `pyproject.toml` |
| Go (`net/http`, `gin`, `echo`, `fiber`) | follow project conventions in `agents/` + `go.mod` |
| Rust (`axum`, `actix-web`, `rocket`) | follow project conventions in `agents/` + `Cargo.toml` |

If the project doc folder (`agents/`) has an endpoint-creation guide, that is the source of truth — read it before generating code.

## Procedure: Create an API endpoint (stack-neutral)

1. **Read project docs** — Check `./agents/` and `AGENTS.md` for endpoint conventions, routing layout, response shape.
2. **Detect stack** and route to the carve-out per the table above.
3. **Plan the endpoint** — method, path, request shape, response shape, auth requirement, idempotency.
4. **Create the route registration** in the project's routing surface (route file, decorator-annotated handler, file-based router).
5. **Create the request handler / controller** — thin; delegate business logic to a service / use-case.
6. **Validate input at the boundary** via the framework's validation primitive (FormRequest, Zod, class-validator, Pydantic, struct-tag validators, etc.) — never inline ad-hoc `if` checks.
7. **Authorize the action** via the framework's authz primitive (Policy, voter, guard, middleware, route dependency).
8. **Shape the response** through a transformer / serializer / DTO — never return raw ORM entities.
9. **Document** the endpoint (OpenAPI annotations / generated spec / project doc).
10. **Verify** — run the project type-checker + targeted tests + smoke probe (`curl` / Bruno / Postman / integration test).

## Conventions (apply on every stack)

- **One handler, one responsibility** — prefer single-purpose handlers over multi-action controllers when the framework supports it.
- **No business logic in the handler** — delegate to a service / use-case layer.
- **Validate at the boundary** — never trust raw request data inside the handler.
- **Authorize every state-changing action** — no unprotected mutating endpoints.
- **Shape responses through a transformer** — DTO, serializer, API resource, response model — never expose raw ORM entities.
- **Version the API surface** explicitly (`/v1/`, header, content-type) — don't rely on implicit versioning.

## Stack-specific procedures

For Laravel projects (the most fully-fleshed-out carve-out in this package), see [`laravel-api-endpoint`](../laravel-api-endpoint/SKILL.md) — covers single-action controllers, `FormRequest`, `Resource`, `Policy`, `CollectionFormRequest`, OpenAPI attributes, and the versioned route layout.

For other stacks, read the matching carve-out from the table above and combine with the project's `agents/` docs.

## Output format

1. Generated files — route registration, handler, request validator, response shaper, authorization rule.
2. Test file with happy path and validation-error cases (using the project's test framework).
3. Summary of created files and their locations.

## Gotcha

- Don't forget to register the route — creating the handler without the route is a common miss.
- Always check if a similar endpoint already exists — duplicates cause confusion.
- Validation rules must match the documented contract (OpenAPI / schema / typed client) — keep them in sync.
- Response shapes are part of the public contract — adding a field is additive; renaming or removing is breaking.

## Do NOT

- Do NOT put business logic in the handler — delegate to services / use-cases.
- Do NOT skip request validation — every handler validates at the boundary via the framework's primitive.
- Do NOT return raw ORM entities — always go through a transformer / serializer / response model.
- Do NOT create unprotected state-changing endpoints — authorize every mutation.
- Do NOT improvise framework idioms — read the carve-out (`laravel-api-endpoint`, `nextjs-patterns`, etc.) for the stack-correct shape.

## Auto-trigger keywords

- create endpoint
- new API route
- route handler
- controller creation
- REST endpoint
- add endpoint
