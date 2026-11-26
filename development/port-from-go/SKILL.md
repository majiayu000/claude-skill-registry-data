---
name: port-from-go
description: Port Go into Rust — goroutines and channels onto tasks and async, interfaces onto traits, error values onto Result, and the value-semantics traps (zero values, integer wraparound, slice aliasing, nil). Use when porting, rewriting, or migrating Go, Golang, a Go service, or a Go CLI into Rust, when replacing a Go component with a Rust one behind the same interface, or when the user asks how a Go construct translates to Rust.
---

# Port from Go

## A construct mapping and a boundary, nothing else

This skill maps Go semantics and owns the Go boundary; process is
`/port-to-rust`. Go syntax maps almost mechanically and the runtime
model does not, so the easy-looking translation is where the port
goes wrong.

## The end state, and why Go usually lands on A

`/port-to-rust` names three end states; Go ports land on A — no
bindings — far more often than Python or JavaScript ports do,
because the cost of the alternative is cgo and a Go system almost
always already has a boundary to strangle at. A default, not a
rule: B is real when the deliverable is a Go-importable package;
C when a leaf function moves before its callers.

## The seam is usually a process, not a function call

Go has no cheap in-process FFI: cgo works in both directions but is
slow at the call, awkward in the build, and drags the Go runtime
along. For most Go ports the right seam is one the system already
has — an HTTP route, a gRPC service, a subcommand, a queue consumer
— and the strangler strategy in `/port-to-rust` is the default, not
in-place FFI; mechanics and the cgo escape hatch are in
`BOUNDARY.md`.

## The traps that break parity silently

| Trap | What actually differs |
|---|---|
| Integer overflow | Go wraps on overflow, always. Rust panics in debug and wraps in release. Any arithmetic that could overflow needs an explicit choice — `wrapping_add` to reproduce Go, or checked arithmetic plus a decision about what the new error path does |
| Zero values | Every Go type is constructible with all fields zeroed, and code relies on it — an empty struct is a valid, meaningful value. Rust has no implicit zero value, so each such site becomes either a `Default` impl (reproducing the behaviour) or a constructor that refuses (changing it). Reproducing is parity; refusing is an improvement, and improvements wait |
| `nil` is several things | A nil pointer, a nil slice (which appends fine and has length zero), a nil map (which reads fine and panics on write), and a nil interface holding a typed nil. `Option<T>` covers the first; the rest are behaviour, not absence, and mapping them all to `Option` produces subtle breakage |
| Slice aliasing | Go slices share a backing array, so a subslice mutation is visible through the original and `append` may or may not copy depending on capacity. Rust makes this impossible, which is the point — but if the source relied on the aliasing, the port must reproduce the *observable effect* deliberately, and if it relied on it accidentally, that is a bug found by the port and recorded |
| Error strings as contract | Go code branches on `err.Error()` text and on sentinel values via `errors.Is`. A port that redesigns the error taxonomy breaks callers that were matching on strings. Map the sentinel set first, then design — `/rust-errors` |

## Mapping, in one line

`MAPPING.md` holds the full table; a row is a starting point, not a
rewrite rule. The syntax maps easily and the runtime model does not
— the easy-looking rows are the ones to read twice.

## Interfaces are implicit; traits are not

A Go interface is satisfied by shape, so the port finds the
implementers and writes `impl Trait for Type` for each: an interface
with one implementer is a struct, not a trait, and one used purely
for test substitution maps to a generic parameter, not `dyn`.

## The test suite is the corpus

Go table-driven tests port almost directly and are characterization
input; benchmarks are not parity evidence. Go suites are thin on
concurrent interleaving, where the port changes behaviour — a race
the GC and scheduler hid is still a race. Harness shapes are
`/rust-testing`.

## Goroutines and channels are the port

`go f()` maps to `tokio::spawn` or a thread depending on whether the
work is IO-bound or CPU-bound — per call site, not per codebase.
Channels map to `tokio::sync::mpsc` (or `crossbeam` for threads),
`select` to `tokio::select!`, `sync.WaitGroup` to collected
`JoinHandle`s. Three differences worth stating plainly: a Rust
future is lazy until polled while a goroutine starts immediately;
`tokio::select!` cancels the losing branches, so anything holding
state across it needs cancellation safety (`/async-rust`); and an
unbounded Go channel pattern usually wants a bounded Rust channel,
which introduces backpressure the source did not have — a contract
change if it can block a caller.

## context.Context maps to structure, not a parameter

Cancellation becomes a `CancellationToken` or a shutdown channel
selected on; deadlines become `tokio::time::timeout`; request-scoped
values threaded through `context` become explicit parameters or a
request struct, which is usually a readability win and always a
diff-size problem — decide before starting, not per function.

## Verification

Both sides:

```bash
cargo test --all-features
cargo clippy --all-targets --all-features   # add -- -D warnings only if the target repo has no lint config
go test ./...                                # the source still passes while both implementations run
go vet ./...
```

Then the differential run with its denominator, and the Go-specific
corpus requirement: at least one case per trap — arithmetic at the
wraparound boundary, a zero-valued struct, a nil map or nil slice,
a subslice that was mutated, and a caller that matched on an error
sentinel. Add the concurrency check: run the Rust side under load
with more than one worker, because a single-threaded differential
run proves nothing about the part of the port that changed most.
