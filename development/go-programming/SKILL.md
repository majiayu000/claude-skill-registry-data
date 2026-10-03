---
name: go-programming
description: Go software engineering skill for designing, implementing, debugging, testing, reviewing, and refactoring Go applications, CLIs, APIs, services, concurrency code, modules, and tooling. Use for .go files, go.mod/go.sum, goroutines/channels, interfaces, error handling, performance profiling, race fixes, and idiomatic Go architecture.
---

# Go Programming

## Operating Rules

- Inspect `go.mod`, package layout, tests, and existing style before changing code.
- Prefer small interfaces at consumer boundaries, explicit errors, table-driven tests, and simple composition over abstraction.
- Preserve exported API compatibility unless the user asks for a breaking change.
- Run targeted `go test` first, then wider tests when feasible. Use `go test -race` for concurrency changes when practical.

## Workflow

1. Build context with `rg --files`, `go list ./...`, and targeted reads of affected packages.
2. Identify package boundaries, public types, side effects, and concurrency ownership.
3. Implement the smallest cohesive change with clear errors and context-aware cancellation.
4. Add or update tests for success paths, failure paths, edge cases, and races.
5. Verify with formatting, tests, vet/static analysis if available, and a concise summary of risks.

## Go Standards

- Use `context.Context` as the first parameter for request-scoped work.
- Wrap errors with `%w` when callers can act on the cause; avoid string matching.
- Keep goroutine lifecycle explicit with cancellation, bounded queues, and ownership of channel close.
- Avoid package globals unless they are immutable constants or intentionally shared.
- Use benchmarks and profiles before performance rewrites.

