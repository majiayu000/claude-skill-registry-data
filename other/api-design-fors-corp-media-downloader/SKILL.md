---
name: api-design
description: API design conventions for any interface a caller depends on — HTTP/REST endpoints, RPC/GraphQL, CLI flags, or a library's public function signatures. Use when designing new endpoints/functions, versioning a breaking change, or reviewing an interface for consistency.
---

# API design

"API" here means any boundary another piece of code (or another team, or your own
code six months from now) depends on — an HTTP endpoint, a CLI's flags, a library's
exported functions, an RPC/GraphQL schema. The same discipline applies to all of them.

## Consistency over cleverness

- One naming convention per surface (all endpoints/functions `verbNoun` or all
  `nounVerb`, consistently) — don't mix conventions across an API because different
  people added different parts at different times.
- Consistent casing per ecosystem convention (camelCase JSON keys for JS-facing APIs,
  snake_case for Python-facing, kebab-case CLI flags) — match what callers of *that*
  ecosystem already expect, not a preference.
- Pagination, filtering, and sorting parameters named and shaped the same way across
  every list-returning endpoint/function in the same API.

## Errors

- Distinguish caller error (4xx / invalid-argument) from server/internal error (5xx
  / internal) — never return 200 with an error buried in the body, and never return
  500 for something the caller could have avoided by passing valid input.
- Error responses carry a stable machine-readable code/type in addition to a
  human-readable message — callers should be able to branch on the code without
  string-matching the message.
- Never leak internals in an error message reaching an external caller (stack
  traces, SQL, file paths, internal service names) — log those internally, return a
  sanitized message externally.

## Versioning & compatibility

- Additive changes (new optional field, new endpoint) don't need a version bump.
  Anything that changes the meaning or shape of existing data for existing callers
  does.
- Decide the versioning strategy explicitly (URL path `/v2/`, header, or
  field-level deprecation) rather than accumulating breaking changes with no
  signal — and document what "supported" means (how long old versions stay live).
- Deprecate loudly before removing: a warning header/log line, a changelog entry, a
  removal date — never a silent breaking change on top of a "stable" version.

## Input validation & idempotency

- Validate at the boundary (the endpoint/function signature), not deep inside
  business logic — fail fast with a clear error rather than propagating bad data.
- Mutating operations that might be retried (network blip, client retry logic) should
  be idempotent where feasible (idempotency keys for POST, PUT semantics for
  full-replace) — a retried request shouldn't double-charge/double-create.

## Documentation

- The shape of a request/response (or function signature) should be enough to use it
  correctly without reading the implementation — types/schemas over prose where the
  language/tooling supports it (TypeScript types, OpenAPI/JSON Schema, docstrings
  with real examples).
- Document what happens at the edges explicitly: empty list vs missing field vs
  null, what an unauthenticated/unauthorized caller sees, rate limits.
