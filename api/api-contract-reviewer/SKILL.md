---
name: api-contract-reviewer
version: 1.0.1
description: Reviews REST + gRPC contracts for stability, versioning, completeness, backwards compatibility. References rest-api-architect / protobuf-architect / grpc-architect for rules; runs `buf breaking` / `openapi-diff`. Severity-keyed findings. Use when reviewing a new endpoint, proto change, or before a breaking-change release.
---

# API Contract Reviewer

Reviews **contracts** — REST OpenAPI specs and protobuf `.proto` files — for stability, versioning hygiene, and completeness. Catches the contract issues architects encoded rules against before they ship to clients.

## 1. When to invoke

- A PR changes `.proto` files, OpenAPI YAML, or any handler that affects the wire contract.
- Before publishing a new major version of an API.
- Before deprecating a field or method.
- Periodic audit of an existing API for drift between spec and implementation.

## 2. Output format

Same shape as [security-reviewer §2](../security-reviewer/SKILL.md#2-output-format) — findings table with severity, then a one-line summary.

```markdown
| Severity | Rule | Location | Evidence | Fix |
|---|---|---|---|---|
| Critical | Breaking change to v1 | `proto/orders/v1/order.proto:23` | Field `status` type changed `string` → `int32` | Revert; introduce `status_v2` as a new field in v1, deprecate `status`, or bump to v2 |
| High | Versioning mismatch | `openapi.yaml` | Endpoint `/orders` lacks `/v1/` prefix | Add `/v1/` prefix per rest-api-architect §4 |
| Medium | Missing OpenAPI example | `openapi.yaml:42` | `CreateOrderRequest` has no `example:` | Add a realistic example — drives SDK gen + docs |
| Low | Inconsistent error shape | `openapi.yaml` | 404 returns `{detail: ...}` while 422 returns RFC 9457 | Standardize on RFC 9457 per rest-api-architect §7 |
```

Severity guide:

- **Critical** — wire-breaking change in a stable version (clients break on deploy).
- **High** — convention violation that's expensive to fix later (versioning, error shape).
- **Medium** — completeness gap that hurts client experience (missing examples, undocumented errors).
- **Low** — polish (inconsistent casing, missing descriptions).

## 3. Review approach

1. **Mechanical pass** (REST: `openapi-diff`; gRPC: `buf breaking`) — surfaces wire-breaking changes.
2. **Convention pass** — read the spec / proto files against the architect rules in §4.
3. **Completeness pass** — every endpoint, every model, every error has the metadata clients need (examples, descriptions, types).

## 4. What to check — by category

### Versioning

Per [rest-api-architect §4](../../protocols/rest-api-architect/SKILL.md#4-versioning--url-prefix) and [protobuf-architect §4](../../encoding/protobuf-architect/SKILL.md#4-versioning):

- **REST:** every endpoint under `/v1/`, `/v2/`, etc. Not in headers, not in query params.
- **gRPC / proto:** version is part of the package path (`acme.shop.orders.v1`), never appended to message names (`OrderV1` is wrong).
- **Additive changes don't bump the version** — new optional field, new endpoint, new enum value, new RPC method. Stay in the existing version.
- **Breaking changes always bump the major version** — field removal, type change, semantic change, required-field tightening. New `vN` package + run side-by-side.
- **Deprecate before remove** — add `[deprecated = true]` (proto) or `deprecated: true` (OpenAPI), set `Deprecation` / `Sunset` headers (RFC 9745 / 8594) for REST.

### Field & method hygiene (proto)

Per [protobuf-architect §3](../../encoding/protobuf-architect/SKILL.md#3-field-numbering--reservation-discipline):

- **Field numbers never reused.** Removed field → `reserved N;` + `reserved "name";`.
- **Field type never changed.** `int32 → string` is wire-breaking even if the runtime value fits both.
- **Field numbers 1–15** reserved for fields read on every request (1-byte wire encoding).
- **Enum: `*_UNSPECIFIED = 0` mandatory.** Enum value names `UPPER_SNAKE_CASE` prefixed with the enum name.
- **No primitive wrappers** (`StringValue`, `Int32Value`) — use `optional` instead.

### Error contracts

Per [rest-api-architect §7](../../protocols/rest-api-architect/SKILL.md#7-error-contracts--rfc-9457-problem-details) for REST and [grpc-architect §2](../../protocols/grpc-architect/SKILL.md#2-error-handling--statuserror-with-codes) for gRPC:

- **REST: every error returns `application/problem+json`** (RFC 9457) — `type`, `title`, `status`, `detail`, `instance`, `correlation_id`. Never `{"detail": "..."}` and `{"errors": [...]}` mixed in one API.
- **gRPC: `status.Error` with a standard code.** Domain-error → code mapping is centralized; no handler invents its own.
- **`type` URLs are stable** once published — clients switch on them.
- **422 validation errors include the structured field list** per rest-api-architect §7.
- **5xx responses always include `correlation_id`** ties to server logs.

### Idempotency and concurrency

Per [rest-api-architect §8](../../protocols/rest-api-architect/SKILL.md#8-idempotency--idempotency-key-mandatory) and [§9](../../protocols/rest-api-architect/SKILL.md#9-concurrency-control--etag--if-match-mandatory):

- **`Idempotency-Key` mandatory on POST/PATCH.** Missing → `400`. Documented in OpenAPI as a required header.
- **`ETag` + `If-Match` mandatory on PUT/PATCH.** Stale → `412`. Documented.
- **Cursor pagination, not offset.** Documented `next_cursor` and `limit` in response.

### JSON shape & encoding

Per [rest-api-architect §12](../../protocols/rest-api-architect/SKILL.md#12-content-negotiation--encoding):

- **`snake_case` JSON field names.**
- **ISO 8601 timestamps**, string-encoded with timezone.
- **Money as strings** (`"99.99"`), never JSON numbers.
- **UUIDs as canonical hex with dashes**, UUID v7 preferred.
- **`null` ≠ missing** — both are documented behaviors in PATCH.

### OpenAPI completeness (REST)

- **Tag, summary, description on every operation.** They drive docs and SDK code-gen.
- **`responses:` documents non-default codes** (`401`, `403`, `404`, `409`, `412`, `422`).
- **`examples:` on every request / response model.** SDKs render them; integration tests use them.
- **`requestBody.required: true`** when the body is mandatory — default is `false`, easy to miss.
- **`securitySchemes` declared** (Bearer / OAuth2) and referenced per-endpoint.
- **`servers:` and `info.contact` set** — these aren't FastAPI defaults but matter for published specs.
- **`info.version` matches the API major version** (`1.0.0`, not `0.1.7`).

### gRPC service hygiene

Per [grpc-architect §1](../../protocols/grpc-architect/SKILL.md#1-service-definition):

- **One service per file.**
- **Every RPC takes a `<Verb><Noun>Request` and returns `<Verb><Noun>Response`.** Never `google.protobuf.Empty` as input.
- **`ListXRequest`/`ListXResponse` use cursor pagination** matching REST conventions.
- **`google.protobuf.Empty`** only for fire-and-forget responses with no useful return.
- **Streaming pattern justified** in proto comments (server-stream vs client-stream vs bidi).

### Documentation drift

The spec is the contract; drift between code and spec is a contract failure:

- **OpenAPI generated from code, not hand-written.** Per [rest-api-architect §15](../../protocols/rest-api-architect/SKILL.md#15-openapi-as-the-source-of-truth).
- **Snapshot test in CI:** the spec is asserted against a committed snapshot file. Any change is reviewed.
- **gRPC equivalent:** generated code is committed under `gen/` per [protobuf-architect §6](../../encoding/protobuf-architect/SKILL.md#6-code-generation--buf-generate--bufgenyaml). PR shows the generated diff alongside the proto diff.

## 5. Tooling

Run these on the diff before the read pass; their output goes into the report.

| Tool | Catches |
|---|---|
| `buf breaking --against '.git#branch=main,subdir=proto'` | Wire-breaking changes in `.proto` files |
| `buf lint` | proto3 style + Buf-style package naming |
| `openapi-diff <old> <new>` | Wire-breaking changes in OpenAPI specs (additions, removals, type changes) |
| `swagger-cli validate openapi.yaml` (or `redocly lint`) | OpenAPI 3.1 validity + completeness rules |
| Snapshot diff in CI | `assert(app.openapi() == snapshot)` per [fastapi-architect §10](../../frameworks/fastapi-architect/SKILL.md#10-testing) |

These run in CI per [rest-api-architect §15](../../protocols/rest-api-architect/SKILL.md#15-openapi-as-the-source-of-truth) and [protobuf-architect §8](../../encoding/protobuf-architect/SKILL.md#8-breaking-change-detection--buf-breaking-in-ci) — review they're actually wired and failing builds on findings.

## 6. What this skill does NOT do

- **Performance review.** Slow queries, blocking I/O — see [performance-reviewer](../performance-reviewer/SKILL.md).
- **Security review.** Auth, injection, secrets — see [security-reviewer](../security-reviewer/SKILL.md).
- **Architecture review.** Whether the API surface is shaped right at the boundary level — see [improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md).

This skill is about whether the contract is *stable and complete*, not whether the underlying implementation is fast or safe.

## 7. Cross-skill ties

- [rest-api-architect](../../protocols/rest-api-architect/SKILL.md) — REST rules this skill verifies.
- [protobuf-architect](../../encoding/protobuf-architect/SKILL.md) — proto rules + `buf breaking` / `buf lint`.
- [grpc-architect](../../protocols/grpc-architect/SKILL.md) — gRPC service-definition conventions + error codes.
- [fastapi-architect](../../frameworks/fastapi-architect/SKILL.md) / [gin-architect](../../frameworks/gin-architect/SKILL.md) / [nethttp-architect](../../frameworks/nethttp-architect/SKILL.md) — implementation skills; reviewer confirms code matches the contract.
- [security-reviewer](../security-reviewer/SKILL.md) — when contract issues are also security issues (tokens in query params, sensitive data in URLs), promote severity.
- [commit-author](../../workflows/commit-author/SKILL.md) — breaking changes get the `BREAKING CHANGE:` footer in the commit.
