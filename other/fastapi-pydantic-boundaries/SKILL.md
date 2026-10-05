---
name: fastapi-pydantic-boundaries
description: >-
  Use when FastAPI request, dependency, response, or OpenAPI behavior interacts
  with Pydantic v2 models, validation, aliases, serialization, generics, or
  error contracts. Do not use for standalone FastAPI routing or standalone
  Pydantic models with no ASGI boundary.
argument-hint: "[endpoint, input/output model, validation, and wire contract]"
---

# FastAPI and Pydantic wire boundaries

FastAPI selects where data comes from and when validation occurs; Pydantic owns
the typed validation/serialization contract. Define the HTTP wire shape
independently from ORM/domain objects.

## Workflow

1. Inspect FastAPI, Pydantic, Starlette, and HTTP client versions plus the
   generated OpenAPI for the target route.
2. Declare path/query/header/cookie/body sources explicitly. Do not rely on a
   parameter rename to preserve external names.
3. Use input models for accepted fields and output models for public response
   fields. Do not return ORM/internal objects and assume response filtering will
   compensate for an undefined secret boundary.
4. Decide aliases, strictness/coercion, discriminators, extra-key behavior,
   status codes, error translation, and JSON serialization as HTTP contracts.
5. Create resources in dependencies/lifespan with clear cleanup. Validation
   code remains deterministic and free of database/network I/O.
6. Test request locations and malformed values, response filtering, alias
   direction, status/body/headers, OpenAPI schemas, and secret exclusion through
   the ASGI test client.

## Invariants

- A Pydantic `ValidationError` inside application logic is not automatically a
  client request error; translate only at the boundary that understands it.
- Response-model validation failure is a server defect, not client input
  failure. Do not expose internal details.
- Use separate create/update/read models when optionality or exposure differs.
- Annotated dependencies and fields can combine metadata; inspect the generated
  OpenAPI instead of guessing precedence.

Read [request/response contracts](references/contracts.md), [ownership and errors](references/ownership.md),
and [ASGI verification](references/testing.md).
