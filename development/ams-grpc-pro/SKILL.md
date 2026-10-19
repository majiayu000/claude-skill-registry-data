---
name: grpc-pro
description: gRPC guidance — protobuf design, service patterns, streaming, deadlines, load balancing, and debugging.
category: development
---

## Overview

gRPC is a high-performance RPC framework built on HTTP/2 and Protocol Buffers: strongly-typed contracts, efficient binary serialization, and first-class streaming in every direction. It shines for service-to-service communication inside a backend, where its speed and codegen pay off. It's a poor fit for browsers and public third-party APIs. This skill covers designing protobuf contracts that evolve safely, using streaming well, and operating gRPC (deadlines, retries, load balancing) in production.

## When to use

- Building service-to-service APIs in a microservices architecture.
- Designing protobuf schemas and versioning strategy.
- Choosing between gRPC, REST, and message queues.
- Adding streaming (server, client, bidirectional) to a service.
- Debugging gRPC (grpcurl, interceptors, status codes).
- Configuring deadlines, retries, and load balancing.
- Exposing gRPC to browsers (grpc-web) or bridging to REST (grpc-gateway).

## Core concepts

- **Protobuf is the contract.** Define services and messages in `.proto` files; generate clients/servers in any language. The schema is the API — design it deliberately and review changes like code.
- **Field numbers are forever.** Never reuse a field number or change a field's type incompatibly; reserve deleted fields (`reserved 4, 15;`). Backward/forward compatibility rules are strict and must be followed mechanically.
- **Four call patterns.** Unary (request/response), server streaming, client streaming, bidirectional streaming. Use streaming for event feeds, large datasets, and realtime coordination — not as a default for simple calls.
- **Deadlines, not just timeouts.** Every RPC should carry a deadline propagated across the call chain; servers must respect cancellation. A missing deadline turns one slow dependency into a cascading thread-pool exhaustion.
- **Status codes.** gRPC's rich codes (`NOT_FOUND`, `INVALID_ARGUMENT`, `UNAVAILABLE`, `DEADLINE_EXCEEDED`...) are the error contract — map domain errors to them consistently and put machine-readable details in `google.rpc.Status` details, not in stringly messages.
- **Interceptors.** Cross-cutting concerns (auth, logging, tracing, metrics, retries) belong in client/server interceptors, keeping handlers focused on business logic.
- **Load balancing.** gRPC's long-lived HTTP/2 connections defeat naive round-robin DNS. Use client-side LB (lookaside like xDS, or grpclb), or a service mesh / proxy that understands HTTP/2 (Envoy) — plain L4 load balancers will pin all traffic to one backend.
- **Retries with hedging awareness.** Retry only idempotent RPCs, only on retryable codes (`UNAVAILABLE`), with backoff + jitter and a retry budget. Blind retries amplify outages.
- **grpc-web and grpc-gateway.** Browsers can't speak gRPC natively: grpc-web needs a proxy translation layer; grpc-gateway generates a REST/JSON transcoding from the same protos. Both add operational surface — only expose to browsers when you must.
- **Reflection.** Enable server reflection in dev/staging for `grpcurl` exploration; disable or restrict it in production so your API surface isn't enumerable.
- **Buf.** The modern protobuf toolchain: linting, breaking-change detection, and schema registry. `buf breaking` in CI enforces compatibility rules mechanically instead of relying on reviewer memory.
- **Health checking protocol.** The standard `grpc.health.v1` service lets orchestrators and load balancers probe serving status per service — implement it rather than inventing your own.
- **xDS and service mesh.** For large deployments, xDS-based control planes (or a mesh sidecar) give gRPC rich traffic policy — retries, timeouts, circuit breaking — without client-side config.

## Practical workflow

1. **Design the protos.** One package per service boundary; request/response messages per method (never bare scalars — you can't extend them); stable field numbers; `google.api.http` annotations if you plan REST transcoding.
   ```proto
   syntax = "proto3";
   package shop.orders.v1;

   service OrderService {
     rpc GetOrder(GetOrderRequest) returns (Order);
     rpc StreamOrderEvents(StreamOrderEventsRequest) returns (stream OrderEvent);
   }
   message GetOrderRequest { string order_id = 1; }
   ```
2. **Generate and implement.** `buf generate` (or protoc) for stubs; keep handlers thin — validate, call domain services, map to responses. Never leak internal errors; map to status codes.
3. **Add interceptors.** Auth token validation, request logging with correlation IDs, OpenTelemetry tracing, and metrics (latency histograms, error rates by code) — on both client and server.
   ```go
   // unary server interceptor: auth + user injection
   func authInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (any, error) {
       token, err := bearerToken(ctx)
       if err != nil {
           return nil, status.Error(codes.Unauthenticated, "missing credentials")
       }
       return handler(withUser(ctx, validate(token)), req)
   }
   ```
4. **Set deadlines everywhere.** Client-side default deadlines (e.g., 5s for unary), server handlers checking `context.Context` cancellation; propagate deadlines through downstream calls with reduced budgets.
5. **Configure retries carefully.** Retry budget (e.g., 10-20% of traffic), idempotent methods only, exponential backoff with jitter; test what happens when the dependency is fully down.
6. **Handle streaming correctly.** Backpressure via bounded channels/queues; heartbeat/keepalive to detect dead peers; clean shutdown draining streams; never buffer unbounded streams in memory.
   - For bidirectional streams, define the protocol precisely (who speaks first, message ordering, termination) — document it in the proto comments.
7. **Debug with grpcurl.** `grpcurl -plaintext localhost:50051 list` and direct method invocation replace curl for gRPC; pair with server reflection in non-prod environments.
8. **Deploy.** Health checking protocol (`grpc.health.v1`) wired to orchestrator probes; TLS everywhere (even internally, via mesh or certs); connection-level settings (max message size, keepalive) tuned per service.

## Common pitfalls

- **Reusing field numbers** — silently corrupts data across versions; reserve deleted numbers forever.
- **No deadlines** — one slow downstream cascades into full thread exhaustion; deadline every RPC.
- **L4 load balancing** — all connections pin to one pod; use client-side or proxy-based HTTP/2-aware LB.
- **Retrying non-idempotent RPCs** — duplicated side effects; retry only safe methods on safe codes.
- **Unbounded streaming buffers** — memory exhaustion from fast producers; apply backpressure.
- **Leaking internal errors** — stack traces and DB details in status messages; map to codes with safe details.
- **Oversized messages** — stuffing megabytes into unary responses; stream or paginate instead, and set sane max-message limits.
- **Reflection on in production** — enumerable API surface; restrict to non-prod.
- **Changing field types incompatibly** — int32→int64 is fine on the wire but breaks generated code assumptions; treat type changes as breaking.
- **No health checks** — orchestrator can't tell a wedged server from a healthy one; implement the standard health protocol.
- **Default max-message-size surprises** — 4MB default too small for some payloads, too generous for others; set it explicitly per service.
- **Ignoring keepalive settings** — dead peers holding resources indefinitely; tune keepalive on both client and server.
- **One proto package for everything** — merge conflicts and unwanted coupling; keep one package per service boundary.
