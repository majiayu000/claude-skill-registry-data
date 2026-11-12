---
name: go-tcp-server-reliability
description: Checklist for validating Go TCP server infrastructure for reliability - goroutine safety, panic recovery, connection lifecycle, framing, resource limits, graceful shutdown, and reliability tests. Use when building, modifying, or reviewing TCP server code.
---

# Go TCP Server Reliability Checklist

Validate TCP server infrastructure against every item below. Scope is infrastructure only (accept loop, connections, framing, lifecycle, shutdown). Do not evaluate business logic or protocol business rules.

## Context

- `recover()` only catches panics in its own goroutine. Every goroutine that needs isolation needs its own recovery boundary.
- `SIGKILL` cannot be caught. Graceful shutdown applies to `SIGINT` and `SIGTERM`.

## How to Run

1. Read the whole server package before answering (for example the TCP server, handler, and decoder/encoder code).
2. Answer every item. Do not skip or merge items.
3. Mark each item `PASS`, `FAIL`, or `N/A`.
4. `PASS` needs evidence: the function, type, or config field name that satisfies it. No note.
5. `N/A` needs a reason. `FAIL` needs what is missing and where it should be fixed.
6. If evidence cannot be found, mark `FAIL`. Do not assume.
7. When building or modifying code, treat this checklist as the definition of done.

## Report Format

```text
ID    | Result | Checklist Item                                                         | Evidence / Note
GS-1  | PASS   | Does each per-connection goroutine have its own deferred recover()? | serve: deferred recover()
GS-2  | FAIL   | Does a recovered panic log the panic value and debug.Stack()?       | Missing stack trace logging in serve()
```

End with a summary: counts of PASS / FAIL / N/A, and the list of FAIL IDs. Any FAIL means the review fails.

## Checklist

### GS - Goroutine Safety

- GS-1: Does each per-connection goroutine have its own deferred `recover()`?
- GS-2: Does a recovered panic log the panic value and `runtime/debug.Stack()`?
- GS-3: After a recovered panic, is the connection closed and its resources released (tracking entry removed, slot freed)?
- GS-4: Does long-lived goroutines (background loops, workers) that require fault isolation have their own `recover()` to prevent unexpected panics from crashing the entire app?
- GS-5: Does every goroutine have a defined termination condition (context canceled, closed channel, or a closed connection)?
- GS-6: Is every started goroutine tracked (for example `sync.WaitGroup`) so none can be orphaned?

### CM - Connection Management

- CM-1: Are temporary connection accept failures retried with a backoff or delay allowing the server to continue accepting connections instead of terminating it? And exit cleanly on permanent errors only?
- CM-2: Is there a maximum concurrent connection limit enforced, with defined behavior? And is it appropriately logged when the limit is hit?
- CM-3: Are active connections tracked throughout their lifecycle, removed when closed, and force-closed during shutdown when necessary?
- CM-4: Are read deadlines set so the server doesn't wait forever for incoming data?
- CM-5: Are write deadlines set so the server doesn't wait forever when sending responses (for clients not receiving data)?
- CM-6: Are deadlines refreshed for each new read/write operation?
- CM-7: Are client disconnect, timeout, and unexpected EOF handled as normal connection ends rather than server failures?

### CS - Communication Safety

- CS-1: Does the reader use a framing strategy (length prefix, delimiter) instead of assuming one `Read()` equals one message?
- CS-2: Are reads done with `io.ReadFull` or an equivalent loop, so partial reads are handled?
- CS-3: Can multiple messages arriving in a single read be split and processed correctly?
- CS-4: Is there a maximum message size, checked before allocating the buffer from a length header?
- CS-5: Do malformed or incomplete messages result in an error or connection close, not a panic or hang?
- CS-6: Are write errors and short writes handled (full buffer written, or the connection is closed on failure)?
- CS-7: If multiple goroutines can write to the same connection, are writes serialized to prevent message frames from interleaving?

### RC - Resource and Concurrency

- RC-1: Is all shared mutable state (registry, counters, maps) protected by a mutex, `sync` primitive, or atomics?
- RC-2: Is any mutex held while doing blocking network I/O (`Read`, `Write`, `Accept`, `Close` on a slow conn)? It must not be.
- RC-3: Are goroutines, queues, channels, and buffers bounded (no unbounded growth per connection or per message)?
- RC-4: Are buffers and other per-connection resources released when the connection ends?
- RC-5: Do the configured connection limits take into account the OS file descriptor limit (documented, checked, or validated at startup)?

### SD - Graceful Shutdown

- SD-1: Are `SIGINT` and `SIGTERM` handled (for example `signal.NotifyContext`)?
- SD-2: When shutdown starts, is the listener closed & no new connections are accepted?
- SD-3: Do existing connections stop accepting new requests according to a defined policy (for example stop reading after the in-flight request)?
- SD-4: Is a root context cancelled on shutdown and passed to server-managed goroutines?
- SD-5: Does shutdown wait for in-flight work to finish, bounded by a configurable shutdown timeout?
- SD-6: When the timeout expires, are the remaining connections force-closed using the registry from CM-11?
- SD-7: Does shutdown wait for all server-managed goroutines to exit (`WaitGroup` or equivalent) after force-close?
- SD-8: Is there no path where shutdown blocks forever (every wait is bounded or unblocked by close/cancel)?
- SD-9: Is shutdown safe to trigger more than once (`sync.Once` or equivalent), with no double close panic?
- SD-10: Are other server-owned resources (listener, clients, pools) closed during shutdown?

### LG - Logging and Diagnostics

- LG-1: Are connection accept and close logged, with the remote address coming from the context logger?
- LG-2: Are unexpected server errors logged exactly once, at the transport boundary (`serve`), and not also by lower layers that return them?
- LG-3: Are recovered panics logged with stack trace (see GS-2)?
- LG-4: Are active connection count and goroutine count observable (log, metric, or debug endpoint)?
- LG-5: Are raw network payloads kept out of logs, with PANs masked via `MaskPAN` where any payload data is logged?

### TS - Reliability Tests

Check that tests exist and are meaningful. Search the test files by name or behavior.

- TS-1: Is there a test with many concurrent connections (hundreds or more)?
- TS-2: Is there a test where one handler deliberately panics and the other connections keep working?
- TS-3: Is there a test where clients disconnect during read and during write?
- TS-4: Are there tests for incomplete, malformed, and oversized messages?
- TS-5: Is there a test for slow or unresponsive clients (deadline triggers)?
- TS-6: Is there a test for graceful shutdown with active connections?
- TS-7: Is there a test for forced shutdown after the deadline expires?
- TS-8: Is there a test or assertion that goroutine and connection counts return to baseline after connections close?
- TS-9: Do the tests pass under `go test -race ./...`? Run it and report the result.
