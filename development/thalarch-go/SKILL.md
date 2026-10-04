---
name: thalarch-go
description: >
  Project-aware Go engineering for services, CLIs, libraries, concurrency, networking, and
  systems code. Use for Go source, modules, goroutines/channels, APIs, tests, profiling,
  performance, or Go-specific refactoring.
---

# Thalarch Go

Use the Go version and module/tooling declared by the repository. Keep code simple and explicit;
do not import patterns from Java/C++ when Go's standard library and conventions already solve
the problem.

## Preflight

Inspect `go.mod`, workspace files, generated-code markers, build tags, configured linters,
Make/Task scripts, tests, and CI commands.

## Idiomatic Go

- Keep interfaces small and consumer-owned when abstraction is genuinely needed.
- Prefer concrete types until multiple implementations or test seams justify an interface.
- Return useful errors rather than sentinel booleans that discard context.
- Wrap errors when the added context helps diagnosis while preserving `errors.Is/As` semantics.
- Use `defer` for clear ownership cleanup when its lifetime/cost is appropriate.
- Preserve zero-value usability when the existing API depends on it.

Avoid unnecessary getters, inheritance-shaped abstractions, and package-level mutable state.

## Concurrency

Every goroutine needs an owner and termination path.

Review:

- context propagation/cancellation;
- goroutine leaks;
- channel close ownership;
- blocked sends/receives;
- data races;
- mutex scope and lock ordering;
- unbounded fan-out;
- timer/ticker cleanup;
- backpressure and worker limits.

Do not create a goroutine merely to make a synchronous call look concurrent.

## HTTP/services

When building services, preserve:

- request context;
- timeout/cancellation behavior;
- body/resource cleanup;
- stable error/status semantics;
- bounded concurrency and connection reuse;
- structured logging/observability conventions already used by the repo.

Combine with `thalarch-api`, `thalarch-security`, and `thalarch-data-sql` when relevant.

## Testing

Use table-driven tests when they make a behavior matrix easier to see, not as mandatory style.
Use subtests, fuzz tests, race checks, integration tests, and benchmarks when they prove a real
risk or regression.

Useful commands may include `go test`, `go test -race`, `go vet`, configured linters, and
benchmarks — but run repository-native scripts/flags first.

## Performance

Measure with available tools such as benchmarks, pprof, execution traces, allocation profiles,
and application metrics. Fix algorithmic/I/O/concurrency bottlenecks before micro-tuning.

## Verification

Run formatting plus the project's targeted tests/static checks/build. For concurrency-sensitive
changes, include race detection when feasible and relevant.
