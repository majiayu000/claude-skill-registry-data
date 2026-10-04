---
name: http-api
description: "Shape HTTP/JSON APIs—resources and verbs, error payloads, pagination, idempotency, and docs. Use when designing new endpoints, reviewing PRs, or aligning teams on REST-ish conventions (versioning lifecycle is a separate concern)."
---

# HTTP API

Design and review **HTTP-facing APIs** (usually JSON): predictable URLs, honest status codes, and errors clients can build on—**without** duplicating everything your **api-compat** skill covers for long-lived versioning policy.

## Scope

- **Modeling**: nouns/resources, collections, actions when RPC-style is clearer than fake REST.
- **HTTP semantics**: which methods, **idempotency**, caching headers when relevant.
- **Errors**: stable machine-readable codes, correlation ids, avoid leaking internals.
- **DX**: examples, OpenAPI snippets, consistent pagination/filter patterns.

## Out of scope (hand off)

- **OAuth/OIDC** protocol details → identity-focused skills.
- **GraphQL-only** schema design → graphql-schema skill.
- **Multi-year deprecation policy** and client migration programs → pair with **api-compat**.

## Review order

1. **Read paths** — Can a client navigate the domain without guessing?
2. **Write safety** — Retries safe? Duplicate submits handled?
3. **Errors** — One shape everywhere; 4xx vs 5xx honest.
4. **Evolution** — Document what may change vs what is stable (compat details in api-compat).

## Smells

- Status 200 with `{error: ...}`; **every** POST returns 200; unbounded list endpoints; secrets in error bodies.

## Done when

- A new engineer can call the API from docs alone; failure cases are **testable** and **consistent**.
