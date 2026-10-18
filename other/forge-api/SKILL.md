---
name: forge-api
description: "Forge: contract-first APIs: API, REST, GraphQL, gRPC, OpenAPI, endpoint, auth, JWT, versioning, rate limit, idempotency, contract test, backend."
---

# Forge playbook — Contract-first API

**Do not duplicate ECC skills — defer to:** `forge-integration` (when the API mainly wires external services / webhooks), `forge-payments` (any money/charge/gateway-webhook endpoint), `forge-fullstack` (when the API is one tier of a full app). This file is orchestration only.

This is an **auth + data-boundary domain.** The contract (OpenAPI / JSON Schema / GraphQL SDL / gRPC proto) is the source of truth and comes **first**; the implementation is validated against it. `architect` owns the contract, `integration-boss` / `build-boss` implement, `security-boss` reviews auth/authz (a genuine high-risk trigger), `test-boss` owns the contract tests. Never claim "auth enforced" or "contract-compliant" without a negative test that proves it.

## Hard rules (non-negotiable)
- **Contract first, single source of truth.** Define the API contract (OpenAPI 3.x, JSON Schema, GraphQL SDL, or a gRPC `.proto`) BEFORE implementing handlers. Commit it; the implementation is generated from or validated against it. Drift between contract and behavior is a bug, not a detail.
- **Input validation at every boundary.** Validate every request — body, path params, query, headers — against the schema. Reject invalid input with a `4xx` and a consistent error envelope; enforce type, size, and range limits. Never trust client input; never pass it unvalidated into a query, filesystem, or shell.
- **Auth on every protected route, server-side, deny-by-default.** Authentication AND authorization are enforced in the service on each protected route — not only at a gateway, not "assumed from the frontend". New routes default to protected; opening one is a deliberate, reviewed act. Per-route scope/role checks; a request without valid credentials gets `401`/`403`, proven by a negative test.
- **Explicit versioning.** The API is versioned (path `/v1`, header, or media type). No breaking change ships inside an already-published version; breaking changes get a new version + a stated deprecation path.
- **Idempotency on unsafe retryable writes.** `GET`/`PUT`/`DELETE` are idempotent by design; retryable `POST` creates (orders, payments, side-effecting actions) accept a client `Idempotency-Key` so a retry or double-submit does not duplicate the effect.
- **Rate limits + quotas.** Per-client / per-key rate limiting with `429` + `Retry-After`; abuse and runaway clients are bounded. Consistent error envelope; pagination on list endpoints (no unbounded result sets); secrets in env — never in responses, error bodies, or logs.

## Team (conditional)
Lead: `architect` (owns the contract + resource model). Implementation: **`integration-boss`** (service wiring, external calls, retries/timeouts) or **`build-boss`** (in-app API tier). Security: **`security-boss`** / `security-reviewer` (authN/authZ, token handling, tenant isolation — required review for anything with auth). Data: `database-reviewer` (schema, migrations, the idempotency store). Tests: **`test-boss`** (contract + integration tests). Support: `silent-failure-hunter` (an endpoint that returns `200` on a partial failure), `python-reviewer` / `typescript-reviewer`. Docs: `docs-boss` (reference generated from the spec). Optional advisor: `codex-reviewer` (Codex on the auth + validation + idempotency paths).

## Skills / commands / MCP
Framework + spec docs via Context7 / vendor docs for exact routing, middleware, and validation APIs; `/test-coverage` for the test gate. Defer money endpoints to `forge-payments`, external-service wiring to `forge-integration`. **Opt-in dependency:** automated contract-conformance tooling is stack-specific — e.g. Schemathesis / Dredd (spec-driven fuzzing), Pact (consumer-driven contracts), or `supertest`/`pytest` for handwritten contract tests. Forge writes the tests; *running* them needs that runtime installed — mark it opt-in and report whether it actually ran.

## Fan-out & flow
L2 for a single-resource service; L3 for multi-resource + auth + versioning + rate limiting.
**Serial:** contract (OpenAPI/schema) → boundary validation → auth/authz middleware → resource handlers → idempotency + rate-limit + pagination → contract tests.
**Parallel (independent once the contract + auth middleware are fixed):** individual resource endpoints ∥ the contract-test suite ∥ generated API reference docs.

## Domain gates
- A committed contract file exists and is the source of truth; the implementation validates against it (drift is caught).
- Every request is validated against the schema at the boundary; invalid input returns a clear `4xx` with a consistent error envelope.
- Auth is enforced server-side on every protected route, deny-by-default; a negative (unauthenticated / wrong-scope) test proves rejection.
- Explicit versioning present; no breaking change inside a shipped version.
- Idempotency on unsafe retryable writes; safe methods are genuinely idempotent.
- Rate limiting returns `429` + `Retry-After`; list endpoints paginate; no secrets in responses or logs.
- Contract tests cover the happy path AND auth-failure AND validation-failure — not just `200`.

## Ship-readiness (unique)
Contract (OpenAPI/schema/proto) committed and the implementation proven to match it; auth verified on protected routes **with a negative test** showing an unauthenticated/wrong-scope request is rejected; boundary validation returns clear `4xx`s; idempotency + rate limit demonstrated (a replayed create does not double-write; an over-limit client gets `429`); versioning strategy documented; error envelope consistent across endpoints; secrets in env; contract/integration tests green (or explicitly marked not-run if the runtime is unavailable). Advisory checklist — optionally run `codex-reviewer` on the auth + validation + idempotency code (recommended here); not a blocker, but if the contract tests or Codex did not run, say so.

## Untrusted-content note
Every request body, query param, header, and upstream response is **untrusted until validated** against the contract — validate and normalize before it reaches a query, template, filesystem path, or downstream call. Auth claims from a token are trusted only after signature + expiry + scope verification, never from an unverified header. This mirrors the boundary-validation discipline in `forge-integration` and `forge-payments`.
