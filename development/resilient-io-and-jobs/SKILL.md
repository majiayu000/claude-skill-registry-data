---
name: resilient-io-and-jobs
category: reliability
description: Use when code calls another service, runs in the background, consumes a queue or retries anything — timeouts, safe retries, idempotent handlers, outbox, graceful shutdown
tech_stack: Go
source: uber-go/guide (Apache-2.0), github/awesome-copilot go.instructions (MIT), adapted
---
# Resilient I/O and Background Work

## Overview

Everything outside your process can be slow, down, or duplicate its own delivery. The recurring defects: an HTTP client with no timeout (Go's default client has none), a retry on a non-idempotent call, a goroutine nobody waits for, and a consumer that isn't safe to redeliver to.

**Core principle:** every call out has a timeout, every retry is on an idempotent operation, and every background task is tracked, not fired and forgotten.

## Outbound HTTP

- One shared `*http.Client{Timeout: ...}` per downstream — the zero-value `http.DefaultClient` has **no** timeout and will hang a goroutine forever on a stuck peer.
- `http.NewRequestWithContext(ctx, ...)` so a canceled request actually stops; `defer resp.Body.Close()`; check the status code before decoding; cap how much of the body you read (`io.LimitReader`) even on success.
- Retry only idempotent requests (GET, PUT, DELETE, or a POST carrying an idempotency key the server honors — api-design-conventions) with exponential backoff and jitter and a hard cap on attempts. Retrying a bare POST "to be safe" is how a flaky network turns into a duplicate charge or duplicate task.
- Java: configure timeouts on `RestClient`/the MicroProfile REST Client, and use the framework's fault-tolerance annotations (`@Retry`/`@Timeout` on Quarkus, Resilience4j on Spring) only where the repo already has the dependency — don't add a new resilience library for one call site.

## Background work

- **Never fire-and-forget a goroutine from a request handler** (Uber guide) — if the handler returns before the goroutine finishes, there's no way to know it ran, and a panic inside it with no recover brings down the process.
- Work that must genuinely outlive the request uses `context.WithoutCancel(ctx)` (Go ≥1.21, keeps request-scoped values like the logger/trace id without inheriting cancellation) and is tracked so the process can wait for it on shutdown — `sync.WaitGroup` or `wg.Go` (Go ≥1.25).
- Graceful shutdown: `signal.NotifyContext(ctx, os.Interrupt, syscall.SIGTERM)`, then `srv.Shutdown(ctx)` (`app.ShutdownWithContext` on Fiber) so in-flight requests finish instead of being cut off mid-response.

## Consumers and jobs

Mirrors what QA's `worker-job-testing` will probe — build it in from the start:

- **Idempotent by construction.** A dedupe key or a unique constraint on the side-effect table means redelivery is a no-op, not a double-apply.
- **Poison messages don't hot-loop.** A message that fails every retry gets logged with enough context to diagnose, then parked (dead-letter queue, or a `failed` status row) — never retried forever in a tight loop that starves the rest of the queue.
- **Restart-safe.** No half-applied state: either the whole unit of work is one transaction, or use the transactional-outbox pattern (write the state change and the "event to publish" row in the same DB transaction, publish from the outbox afterward) so a crash between "wrote the row" and "published the event" can't lose or duplicate the event.

## Tests

- Duplicate delivery of the same message/request → asserts no duplicate side effect.
- Dependency returns 5xx or times out (`httptest.Server` that sleeps past the client timeout, or returns 503) → asserts the caller's handling (retry, circuit, or clean failure) rather than hanging or panicking.
- Simulated restart mid-job (kill between steps in a test harness that allows it) → asserts the retried run reaches the same end state, not a duplicated or corrupted one.

## Common Mistakes

- Using `http.Get`/`http.DefaultClient` directly instead of a client with a configured timeout.
- Retrying a non-idempotent POST because "it probably failed before it took effect."
- A handler that spawns `go doSomething()` with no error handling and no shutdown tracking.
- A consumer that `ack`s before the side effect is durably committed (loses the message on crash) or never acks a poison message (hot loop).

## Red Flags

- `http.Client{}` with no `Timeout` field set anywhere near the call site.
- A `go func() { ... }()` inside a handler with no `recover` and no `WaitGroup`.
- A job handler with no idempotency key and a side effect that isn't naturally idempotent (e.g. "increment a counter" instead of "set to value").
- A retry loop with no maximum attempt count or no backoff.
