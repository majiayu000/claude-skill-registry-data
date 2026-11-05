---
name: connectrpc-architect
version: 1.0.0
description: ConnectRPC standards — one .proto serving Connect, gRPC and gRPC-Web from a single http.Handler via protoc-gen-connect-go, connect.Code error mapping, the mandatory interceptor chain, streaming caveats (HTTP/2 for client/bidi, gRPC-Web server-stream only), browser callers with no proxy, generic typed clients and conformance testing. Use when designing or reviewing a Connect handler, choosing Connect over vanilla gRPC, or serving proto to browser callers.
---

# ConnectRPC Architecture

ConnectRPC (`connectrpc.com/connect`) serves **Connect**, **gRPC** and **gRPC-Web** from one generated `http.Handler` — one `.proto`, no gateway in front of the browser. Pair with [protobuf-architect](../../encoding/protobuf-architect/SKILL.md) for schema design. Go skeletons in [RECIPES.md](RECIPES.md); pinned deps in [STACK.md](STACK.md). Other languages follow the same protocol-level conventions with idiomatic substitutions.

## 1. The value proposition — one handler, three protocols

A single `buf`-generated handler is mounted once and answers all three wire protocols:

| Protocol | Wire | Callers | Notes |
|---|---|---|---|
| **Connect** | `POST` + JSON or Protobuf, HTTP/1.1 or 2 | Any HTTP client, browsers | No proxy; `curl`-able with `-H 'Content-Type: application/json'` |
| **gRPC** | Length-prefixed Protobuf, HTTP/2 | gRPC clients, backend-to-backend | Same `grpc-status` trailers as vanilla gRPC |
| **gRPC-Web** | Protobuf, trailers encoded in the body | Browsers via `@connectrpc/connect-web` | No proxy/gateway required |

**House position:**

- **`.proto` is the RPC contract** — the source of truth for the RPC surface, exactly as for [grpc-architect](../grpc-architect/SKILL.md).
- **Connect is the primary adapter.** New Go services generate the Connect handler and mount it as the RPC entrypoint.
- **Keep a native gRPC adapter from the same proto as deliberate insurance.** Registering the same implementation on a `*grpc.Server` costs one more generated stub; if Connect is ever deprecated, or a pure-gRPC peer appears, the swap is mechanical. That path and the house `grpckit` live in [grpc-architect](../grpc-architect/SKILL.md) and [GRPCKIT](../../personal/go-house-libs/references/GRPCKIT.md).
- **REST is a separate public surface, not generated from proto.** Where the contract is OpenAPI (public, `curl`-first, cache-friendly), follow [rest-api-architect](../rest-api-architect/SKILL.md) — don't transpile proto to REST with `grpc-gateway`. Internal RPC and public REST coexist without a shared type layer.

## 2. Service definition & generated surface

Proto layout, message naming, pagination and `google.protobuf.Empty` rules come from [protobuf-architect](../../encoding/protobuf-architect/SKILL.md). This skill covers only the generated Connect surface.

- **Generate with `buf`** (`buf.build/connectrpc/go`), `paths=source_relative`, through `task generate` — never by hand. Config in [RECIPES.md](RECIPES.md). The generated `*connect.go` is never edited; write helpers in sibling hand-written files.
- **The generated interface is the port.** `protoc-gen-connect-go` emits `UserServiceHandler` (one method per RPC) plus `NewUserServiceHandler(svc, opts...) (string, http.Handler)`. Your `userServer` struct implements `UserServiceHandler`; the generated shim holds no business logic.
- **Mount the returned path on a `http.ServeMux`** — one `mux.Handle(path, handler)` per service, alongside non-RPC routes (health, reflection, CORS). Use the path `NewUserServiceHandler` returns; don't hand-write route strings.
- **Request/response are always typed messages.** Unary handlers take `*connect.Request[T]` and return `*connect.Response[T]`; streaming handlers take `*connect.ServerStream[T]`, `*connect.ClientStream[T]` or `*connect.BidiStream[Req, Resp]`.

## 3. Error handling — `connect.NewError`

Return errors via `connect.NewError(connect.Code, err)`. Map domain errors to codes in one central place (skeleton in [RECIPES.md](RECIPES.md)).

| Code | HTTP | Use for |
|---|---|---|
| `CodeInvalidArgument` | 400 | request fails schema or business validation |
| `CodeFailedPrecondition` | 412 | request valid but system state forbids it (e.g. delete a non-empty resource) |
| `CodeOutOfRange` | 400 | numeric / range-specific violation distinct from `InvalidArgument` |
| `CodeUnauthenticated` | 401 | missing or invalid credentials |
| `CodePermissionDenied` | 403 | authenticated but not authorized |
| `CodeNotFound` | 404 | resource doesn't exist |
| `CodeAlreadyExists` | 409 | unique-constraint or idempotency-key collision |
| `CodeAborted` | 409 | concurrency conflict (ETag-equivalent) — re-fetch and retry |
| `CodeResourceExhausted` | 429 | rate limit; per-tenant quota |
| `CodeDeadlineExceeded` | 504 | the request didn't complete in time — set by the runtime |
| `CodeUnavailable` | 503 | transient — load-balancer drained, restart in progress; client retries |
| `CodeUnimplemented` | 404 | method exists in proto but server doesn't handle it (rollout) |
| `CodeInternal` | 500 | unexpected server-side failure |
| `CodeDataLoss` | 500 | corrupted or lost data |
| `CodeCanceled` | 499 | the client went away |
| `CodeUnknown` | 500 | fallback when nothing else fits |

- **Don't reach for `CodeInternal` as a default.** Map every known domain error to a specific code; `CodeUnknown` is even worse.
- **`connect.CodeOf(err)`** recovers the code from any error — use it in the logging interceptor and in tests, never invent your own `error → int` map.
- **`connect.NewErrorDetail`** attaches structured detail (`google.rpc.ErrorInfo`, `google.rpc.BadRequest`), read back with `connect.DetailsFromError` — the RPC analogue of REST's RFC 9457 (see [rest-api-architect §7](../rest-api-architect/SKILL.md)). Include a request id in the detail.
- **Never leak stack traces or DB errors** to clients. Log server-side; return a generic message plus the correlation id. The HTTP status mapping differs per protocol — gRPC-Web can't render every detail the way Connect's JSON body does, so if a detail matters to a browser, also put it in the message text.

## 4. Interceptors — mandatory chain

Interceptors are Connect's middleware, built with `connect.UnaryInterceptorFunc` and composed with `connect.ChainUnaryInterceptors`. **Order matters** — outermost first: **recovery → request-id → logging → auth → validation → metrics**. Full chain in [RECIPES.md](RECIPES.md).

- **Recovery first** — catches panics anywhere downstream and converts to `CodeInternal` with the correlation id (never a stack trace). Use named returns in the interceptor so the deferred recover can set both response and error.
- **Request-id second** — read `X-Request-Id` from `req.Header()` or mint one, inject it into `context.Context`, and echo it on the response header.
- **Auth before validation** — no point validating an unauthenticated request's body. Auth reads the bearer token, verifies it locally against cached JWKS, and stores the principal in the context; per-method authorization happens in the handler.
- **Validation is centralized** via [connectrpc.com/validate](STACK.md) (protovalidate, per [protobuf-architect §5](../../encoding/protobuf-architect/SKILL.md#5-validation--protovalidate-cel)) — `validate.NewInterceptor()`, no hand-written checks per handler.
- **Metrics/OTel last** — [connectrpc.com/otelconnect](STACK.md) instruments every call (latency, codes, RPC attributes) without touching handlers. Streams need their own chain (`connect.ChainStreamInterceptors`), but it runs for all three protocols; only the rendered error detail differs.

## 5. Streaming patterns

Connect supports the four gRPC call types through the same handler.

| Pattern | Use for | Pitfalls |
|---|---|---|
| **Unary** | Default — request/response | None — start here |
| **Server-stream** | Server emits N responses to one request (event feeds, tail, chunked export) | Connection state outlives the request; needs resume tokens |
| **Client-stream** | Client uploads N messages, server returns one summary (batch ingest) | Needs HTTP/2 on the wire |
| **Bidi-stream** | Genuinely interactive (chat, control protocols) | Needs HTTP/2; reconnect/resume logic; always bounded by a deadline |

- **The protocol gotcha:** Connect's own protocol carries unary and server-streaming over HTTP/1.1, but **client- and bidi-streaming require HTTP/2**. Browsers are server-stream only — gRPC-Web (what `@connectrpc/connect-web` speaks) has no client- or bidi-streams, so make browser uploads unary and only subscriptions stream.
- **Server-streams need resume tokens** — pass `start_after_id` or a cursor in the request so a disconnected client resumes from a known point rather than replaying from zero.
- **Don't stream to save round-trips** — unary with cursor pagination is usually simpler; streaming earns its place when the response is unbounded or genuinely incremental. **Always set a deadline on streams** — an unbounded stream is a leak.

## 6. Deadlines, metadata & context

Every call carries a deadline. Clients set it; servers respect it; downstream calls inherit the remaining time. Skeleton in [RECIPES.md](RECIPES.md).

- **Set deadlines with `context.WithTimeout`** on the client; the runtime propagates them as `grpc-timeout` metadata. Defaults: unary 5–30s; server-stream often minutes but always bounded.
- **Servers check `ctx.Err()`** in long handlers and abort the moment it fires; propagate `ctx` to DB and outbound calls.
- **Metadata is HTTP headers.** Read request metadata with `req.Header().Get(...)`; write response metadata with `resp.Header().Set(...)` and trailers with `resp.Trailer().Set(...)`. Standardize one correlation-id header (`X-Request-Id`) — Connect uses plain HTTP header casing, so don't rely on gRPC's lowercase normalization.

## 7. Health, reflection & ops

- **Health:** `connectrpc.com/grpchealth` implements `grpc.health.v1.Health` over all three protocols — `grpchealth.NewHandler(grpchealth.NewStaticChecker(serviceName))`. Always on; orchestrators and load balancers need it.
- **Reflection:** `connectrpc.com/grpcreflect` enables `grpcurl` and IDE introspection without the `.proto` — mount `NewHandlerV1` (and `NewHandlerV1Alpha` for older clients) from a `NewStaticReflector(...)`. **Dev only, off in prod**; it leaks the whole service surface.
- **CORS:** when browsers call the service directly, wrap the mux with `connectrpc.com/cors` (`cors.New(cors.WithAllowedOrigins(...), cors.AllowedMethods(), cors.AllowedHeaders(), cors.ExposedHeaders(), cors.MaxAge(...))`) — never `Allow-Origin: *` for authenticated endpoints (same rule as [rest-api-architect §10](../rest-api-architect/SKILL.md)). Opt into response compression with `connect.WithSendGzip()` / `connect.WithCompressMinBytes(...)`.

## 8. Client side

Generated clients are generic and typed — no reflection at call time.

- **`NewUserServiceClient(httpClient, baseURL, opts...)`** from the generated package, backed by `connect.NewClient[Req, Resp](...)` under the hood. Pass `*http.Client` (with sane timeouts, TLS config, and your tracing transport).
- **Force a protocol when needed:** `connect.WithGRPC()` or `connect.WithGRPCWeb()`; the default is Connect. `connect.WithProtoJSON()` selects JSON on the Connect protocol. Set a `context.WithTimeout` on every call, then `defer cancel()`.
- **Compose retries/backoff through the house `resilience` module** ([RESILIENCE](../../personal/go-house-libs/references/RESILIENCE.md)) rather than hand-rolling a loop around the client — it classifies permanent vs transient errors and adds jitter.
- **No per-request internal calls** — validate tokens locally against cached JWKS; don't call an auth service on the hot path. Client interceptors use the same `connect.UnaryInterceptorFunc` shape via `connect.WithInterceptors(...)`, so outbound calls reuse the request-id/tracing interceptors.

## 9. Testing & conformance

- **`httptest` for Connect.** Build the mux, wrap it in `httptest.NewServer`, and point a generated client at `srv.URL` using `srv.Client()`. Call the handler directly with `connect.NewRequest(...)` when you don't need the wire; use `httptest` when protocol behavior (headers, codes, streaming) matters. No `bufconn` — that is a gRPC-only convenience for testing the native adapter ([grpc-architect §9](../grpc-architect/SKILL.md)).
- **The house pattern is a conformance suite.** Define scenarios once (success, each error code, deadline exceeded, unauthenticated, not-found, pagination) and run each against three transports of one Go port: Connect over `httptest`, native gRPC over `bufconn`, and the REST surface if one exists. A single shared table with a per-transport client factory proves all surfaces map errors identically — see [RECIPES.md](RECIPES.md).
- **Table-driven tests** per [go-architect §9](../../languages/go-architect/SKILL.md#9-testing) — one row per (input, expected `connect.Code`, expected error type), asserted with `connect.CodeOf`. `grpcurl` remains the ad-hoc tool against a reflection-enabled dev server.

## 10. When to pick Connect vs vanilla gRPC vs REST

| Dimension | Connect | vanilla gRPC | REST / OpenAPI |
|---|---|---|---|
| Browser callers | ✅ no proxy | ❌ needs a gRPC-Web proxy | ✅ |
| Client/bidi streaming to browsers | ❌ (gRPC-Web: server-stream only) | ❌ | n/a |
| Streaming (backend) | ✅ all four, HTTP/2 | ✅ all four | ❌ (SSE/long-poll only) |
| Contract | `.proto` | `.proto` | OpenAPI |
| `curl` / manual testing | ✅ JSON mode | ❌ (grpcurl) | ✅ |
| HTTP caching (ETag/Cache-Control) | ❌ | ❌ | ✅ |
| Public API discoverability | ❌ | ❌ | ✅ |

- **Connect is the default for a new Go RPC service.** It costs nothing over vanilla gRPC when the caller is another backend, and removes the gateway when the caller is a browser.
- **Vanilla gRPC stays the right call** when every peer is pure gRPC and you want the leanest possible server, or when an existing gRPC ecosystem (interceptors, `bufconn` tooling) is already in place — both can share the same `.proto`.
- **REST is the right call for the public surface** — external consumers, cache-friendly reads, `OpenAPI` documentation — authored separately, not generated from proto.
