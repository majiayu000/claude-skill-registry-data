---
name: go-http-server-reliability
description: Checklist for validating Go HTTP server reliability, covering application goroutines, server configuration, request lifecycle, resource management, graceful shutdown, logging, and reliability tests. Use when building, modifying, or reviewing Go HTTP servers using net/http, Echo, or Gin.
---

# Go HTTP Server Reliability Checklist

Validate application-level HTTP server infrastructure against every item below.

**Scope:** Server configuration, application-managed goroutines, request lifecycle, resource management, graceful shutdown, and reliability tests.

Do not audit TCP connection handling, HTTP parsing, framing, or other functionality already handled by Go's `net/http`.

## Context

- Echo and Gin are built on Go's `net/http`.
- `net/http` already handles HTTP transport, connection management, and handler panic isolation.
- `recover()` only catches panics in its own goroutine. Application-created goroutines need their own recovery boundary when fault isolation is required.
- `http.Server.Shutdown()` handles graceful shutdown of ordinary HTTP connections. Hijacked connections require separate handling.
- `SIGKILL` cannot be caught. Graceful shutdown applies to `SIGINT` and `SIGTERM`.

## How to Run

1. Read the whole HTTP server package before answering (server initialization, middleware, handlers, background workers, and shutdown code).
2. Answer every item. Do not skip or merge items.
3. Mark each item `PASS`, `FAIL`, or `N/A`.
4. `PASS` needs evidence: the function, type, middleware, or config field name that satisfies it. No note.
5. `N/A` needs a reason. `FAIL` needs what is missing and where it should be fixed.
6. If evidence cannot be found, mark `FAIL`. Do not assume.
7. When building or modifying code, treat this checklist as the definition of done.

## Report Format

```text
ID    | Result | Checklist Item                                     | Evidence / Note
GS-1  | PASS   | Do application goroutines have managed lifecycles? | worker: context cancellation
SV-1  | FAIL   | Are HTTP server timeouts configured appropriately? | Missing ReadHeaderTimeout
```

End with a summary: counts of PASS / FAIL / N/A, and the list of FAIL IDs. Any FAIL means the review fails.

## Checklist

### GS - Goroutine Safety

- GS-1: Does every application-created goroutine have a defined termination condition and appropriate lifecycle tracking?
- GS-2: Do long-lived application goroutines that require fault isolation have their own panic recovery?

### SV - Server Configuration and Limits

- SV-1: Are HTTP server timeouts (`ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout`) configured appropriately for the application?
- SV-2: Are HTTP headers and request bodies protected by appropriate size limits?
- SV-3: Are concurrent requests and connections bounded where necessary, with defined behavior when limits are reached?

### RE - Request Lifecycle

- RE-1: Are request contexts propagated to downstream operations, with appropriate timeouts and cancellation handling?
- RE-2: Are request and response objects used safely within the handler lifecycle, without concurrent response writes or unsafe background access?

### RC - Resource and Concurrency

- RC-1: Is shared mutable application state protected by mutexes, synchronization primitives, or atomics?
- RC-2: Are application-managed goroutines, queues, worker pools, and buffers bounded to prevent unbounded resource growth?
- RC-3: Are application-owned resources properly released when operations, requests, or workers finish?

### SD - Graceful Shutdown

- SD-1: Are `SIGINT` and `SIGTERM` handled, and does shutdown use `http.Server.Shutdown()` with a configurable timeout?
- SD-2: When graceful shutdown expires, are remaining ordinary connections force-closed, with hijacked connections handled separately where applicable?
- SD-3: Are application-managed workers stopped and awaited, and are other application-owned resources closed during shutdown?

### LG - Logging and Diagnostics

- LG-1: Are HTTP requests and unexpected server errors logged appropriately without redundant error logging?
- LG-2: Are sensitive payment details and raw payloads kept out of logs, masked wherever necessary?
- LG-3: Are relevant application metrics observable, including request counts, active requests, and goroutine counts?

### TS - Reliability Tests

Check that tests exist and are meaningful. Search test files by name or behavior.

- TS-1: Are concurrent HTTP requests and concurrency-limit behavior tested?
- TS-2: Are request cancellation, client disconnects, and configured timeouts tested?
- TS-3: Are oversized request bodies and malformed application payloads tested?
- TS-4: Is panic recovery tested where application-specific recovery middleware or goroutine isolation is implemented?
- TS-5: Are graceful shutdown, forced shutdown, and application worker cleanup tested?
- TS-6: Do application goroutine and resource counts return to baseline after operations finish?
- TS-7: Do the tests pass under `go test -race ./...`? Run it and report the result.

## Framework Responsibilities (Do Not Reimplement)

Go's `net/http` already handles:

- TCP connection acceptance and ordinary connection lifecycle.
- HTTP parsing, framing, and partial reads.
- HTTP connection-serving goroutines.
- Ordinary connection tracking and cleanup.
- Recovery of panics escaping HTTP handlers.
- Graceful connection draining through `Server.Shutdown()`.
- Forced closure of ordinary HTTP connections through `Server.Close()`.

Do not report these as missing application functionality.

Focus on configuring and correctly integrating these capabilities with application-owned resources and goroutines.

Important exceptions:
- Application-created goroutines need their own lifecycle management and panic recovery where required.
- Request body limits must be configured separately from `MaxHeaderBytes`.
- `net/http` does not provide a general maximum concurrent request or connection limit.
- Hijacked connections, such as WebSockets, require separate lifecycle management.
- HTTP server shutdown does not automatically stop application-managed background workers.
