---
name: sota-api-design
description: >-
  State-of-the-art API design and audit guidance (2026) covering REST/HTTP,
  GraphQL, gRPC, WebSockets/SSE/realtime, webhooks, versioning/evolution, and
  API security/operations. Use when designing or building any API surface
  (endpoints, schemas, protos, realtime channels, webhook senders/receivers)
  AND when auditing/reviewing existing APIs for correctness, evolvability,
  security, and operational robustness. Not for browser UI, rendering, or
  client-framework concerns — use sota-web-frameworks or sota-frontend-design.
  Trigger keywords: API, REST, GraphQL,
  gRPC, endpoint, websocket, SSE, realtime, WebRTC, webhook, versioning, OpenAPI,
  pagination, idempotency, rate limit, problem+json, protobuf, deprecation.
---

# SOTA API Design & Audit

## Purpose

Expert-level rules for building and auditing API surfaces: HTTP/REST semantics,
GraphQL, gRPC/protobuf, realtime (WebSocket/SSE/WebTransport), webhooks, contract
evolution, and the security/operational envelope around all of them. Rules are
imperative with rationale and good/bad examples; every rules file ends with an
audit checklist. Use the index table below to load only the files relevant to the
task — do not read all files for a narrow question.

## BUILD mode

When designing or implementing an API:

1. **Pick the protocol deliberately.** Read `rules/04` §1 first if the choice
   (REST vs GraphQL vs gRPC vs realtime transport) is open. Default: gRPC
   service-to-service, REST at the edge, GraphQL only for multi-client shape
   diversity, SSE for server-push, WS only for true bidirectional.
2. **Contract first.** Write the OpenAPI/SDL/proto before handlers. Get the
   resource model, error shape (RFC 9457), pagination, and naming right in the
   spec — they are nearly impossible to fix later (`rules/01`, `rules/02`).
3. **Design for a decade of additive change.** String enums not booleans, RFC
   3339 timestamps, opaque IDs, open enums, tolerant-reader contract, CI
   breaking-change diff from day one (`rules/02`).
4. **Build the unhappy paths with the happy path**: idempotency keys, 429 +
   Retry-After, timeout budgets, problem+json errors, size limits — these are
   features, not hardening passes (`rules/01` §6, `rules/07`).
5. **Realtime and webhooks are protocols, not endpoints.** Specify auth,
   heartbeat, resume, ordering, backpressure, and close semantics (`rules/05`);
   signing, retries, SSRF egress controls (`rules/06`) before writing code.
6. **Security envelope is part of the design**: authn scheme per consumer type,
   per-principal rate limits, tenant isolation derived from credentials, audit
   logging (`rules/07`).
7. Before declaring done, run the relevant files' **Audit checklists** against
   your own design as a self-review.

## AUDIT mode

When reviewing an existing API:

1. Identify the surfaces in scope (REST endpoints, GraphQL schema, protos, WS/SSE
   handlers, webhook senders/receivers, gateway config) and load the matching
   rules files.
2. Work through each file's **Audit checklist** against the actual code/spec —
   verify in code, don't trust docs or comments. Prefer reading: route
   definitions, middleware chains, error handlers, pagination queries, proto
   history, WS connection handlers, webhook dispatch code, gateway/limiter
   config.
3. Actively probe the classic gaps: missing object-level authz (BOLA), offset
   pagination on big tables, `200 {"error":…}`, missing deadlines, unbounded WS
   send buffers, unsigned webhooks, SSRF in webhook egress, origin-reflection
   CORS, tenant ID taken from the request body.

### Severity conventions

- **Critical** — exploitable security flaw or guaranteed data corruption/loss:
  missing object-level/tenant authz, unsigned or non-constant-time-verified
  webhooks, SSRF-able webhook egress, credential leakage (query strings/logs),
  origin-reflection CORS with credentials, reused proto field numbers,
  double-execution of payments (no idempotency on money writes).
- **High** — breaks clients or production under normal conditions: breaking
  change shipped without versioning/deprecation, no rate limiting on authed
  surface, missing deadlines/timeout hierarchy, unbounded pagination or
  request sizes, no WS backpressure/resume (silent data gaps), non-idempotent
  webhook consumers.
- **Medium** — erodes the contract or operability: wrong status codes, non-RFC
  9457 error sprawl, offset pagination at scale, spec/implementation drift, no
  Sunset/Deprecation signaling, missing rate-limit headers, N+1 resolvers,
  closed response enums.
- **Low** — polish and convention: naming inconsistency, missing `operationId`s,
  missing preflight cache, suboptimal cache headers, missing pagination link
  hints.

### Finding format

```
[SEVERITY] <one-line title>
Where: <file:line | endpoint | schema element>
Rule: <rules-file §section>
Issue: <what is wrong, with the observed evidence (code/HTTP exchange)>
Impact: <concrete consequence — who breaks, what leaks, what corrupts>
Fix: <specific change; example snippet/header/schema where load-bearing>
```

Order findings by severity; one finding per root cause; no speculative findings
without evidence in code or spec.

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-rest-http-design.md` | Designing/auditing REST endpoints: resource modeling, methods/status codes, cursor pagination, filtering, partial responses, idempotency keys, ETags/conditional requests, HATEOAS pragmatism, RFC 9457 errors, OpenAPI-first, contract testing. |
| `rules/02-versioning-evolution.md` | Changing an existing API, adding/removing fields, choosing URL vs header versioning, planning deprecation (Sunset/Deprecation headers), enum/schema evolution, tolerant readers, CI breaking-change gates. |
| `rules/03-graphql.md` | Any GraphQL work: schema/nullability/connections design, N+1 and dataloaders, depth/cost/alias limits, persisted-query allowlists, error channels (userErrors vs errors), resolver authz, when GraphQL is the wrong choice. |
| `rules/04-grpc-protocols.md` | gRPC/protobuf work or protocol selection: field-number/reserved evolution rules, deadlines and cancellation propagation, streaming patterns, rich error details, gRPC-Web/Connect, L7 load balancing, REST vs GraphQL vs gRPC decision table. |
| `rules/05-realtime-websockets-sse.md` | WebSocket/SSE/realtime features: transport choice (WS vs SSE vs WebTransport), upgrade auth & CSWSH, heartbeats, reconnect backoff + resume tokens, ordering/delivery guarantees, backpressure, close codes, SSE replay, pub/sub fanout scaling, presence; WebRTC server hardening (TURN relay abuse, DTLS-SRTP, signaling) when self-hosted. |
| `rules/06-webhooks.md` | Sending or receiving webhooks: HMAC signing + timestamp + rotation, replay protection, retry/backoff design, ordering caveats, idempotent consumers, outbox dispatch, reconciliation APIs, SSRF defenses for user-supplied URLs. |
| `rules/07-security-operations.md` | Cross-cutting security/ops on any API: authn scheme selection (keys/OAuth2/mTLS), per-message request signing (RFC 9421 + Content-Digest), rate limiting + 429/Retry-After, layered bot management, quotas, request size limits, HTTP message framing / request smuggling, timeout budgets, CORS, audit logging, multi-tenant isolation, cross-tenant testing. |

## Top-10 non-negotiables

1. **Object-level authorization on every handler** — derive tenant/ownership from
   the credential, never from the request; cross-tenant access returns a
   consistent 404. (rules/07 §1, §7)
2. **Never `200 {"error":…}`** — correct status codes, single RFC 9457
   problem+json error shape API-wide, machine-readable codes, trace ID, no
   internals leaked. (rules/01 §3, §9)
3. **Cursor pagination with enforced max limit** on every collection that can
   grow; stable sort with unique tiebreaker; no unbounded lists in REST or
   GraphQL. (rules/01 §4, rules/03 §2)
4. **Idempotency for unsafe operations**: Idempotency-Key with stored-response
   replay on anything that moves money or sends things; webhook consumers dedupe
   on event ID. (rules/01 §6, rules/06 §4)
5. **Additive-only evolution, enforced by CI** (oasdiff/buf breaking/schema
   check); clients ignore unknown fields; breaking changes go through the
   announce→Deprecation/Sunset→measure→410 pipeline. (rules/02)
6. **Deadlines/timeouts everywhere, outer > inner**, propagated and cancellable;
   long work is async (202 + status resource), never a long-held connection.
   (rules/04 §3, rules/07 §4)
7. **Per-principal rate limits + quotas** with 429, Retry-After, and RateLimit
   headers, enforced in a shared store; expensive operations cost-weighted.
   (rules/07 §2)
8. **Realtime must resume**: heartbeats, jittered reconnect backoff, sequence
   IDs + bounded replay buffer, explicit resume-failure → snapshot; bounded send
   queues with a defined slow-consumer policy. (rules/05 §2)
9. **Webhooks signed and SSRF-proof**: HMAC(id.timestamp.raw body) verified in
   constant time with replay window; senders block private/metadata IPs with
   resolve-pin-connect and follow no redirects. (rules/06 §2, §8)
10. **Proto/GraphQL schema discipline**: never reuse a proto field number
    (reserve removed ones), enum zero = UNSPECIFIED, GraphQL non-null only when
    guaranteed, every data-touching resolver behind a dataloader. (rules/04 §2,
    rules/03 §2–3)
