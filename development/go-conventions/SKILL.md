---
name: go-conventions
description: "Go rules for package layout, error wrapping, context propagation, structured logging, configuration and license headers. Use when writing, reviewing or refactoring Go code."
---

# Go conventions

Baseline conventions for Go code in services, CLIs and libraries.

## When to use

- Writing, reviewing or refactoring Go code.
- Setting up a new Go module.

## Rules

### Layout

- `cmd/<binary>/main.go`: wiring only. Flags, config, construction, shutdown.
- `internal/`: everything else, by default.
- `pkg/`: only when another module imports it.
- No `util`, `common` or `helpers` package. Split by domain, not by layer.

### Errors

- Wrap with `fmt.Errorf("load config: %w", err)`. Lowercase, no punctuation, no "failed to".
- Compare a sentinel with `errors.Is`. Use `errors.As` when a caller needs fields off a typed
  error.
- No panic in library code.
- Never log and return the same error. The caller that stops the chain logs it.
- Ignore a return value only as `_`, with a comment saying why.

### Context

- `ctx` is the first parameter on anything doing IO, blocking or spawning work.
- `context.Background()` only in `main` and in tests.
- No context stored in a struct field outside a request scoped struct.
- `context.WithTimeout` at IO boundaries.
- Context values carry request metadata only, keyed by an unexported type. Never a dependency.

### Logging

- `log/slog` only. Built once in `main`, injected everywhere else.
- No package level logger, no `slog.Default()` in library code.
- Key value pairs, not formatted strings.
- `Info` for lifecycle, `Warn` for degradation, `Error` for a handled failure. No `log.Fatal`
  (the standard library `log` package) outside `main`.
- Never log a secret, a token or a request body.

### Config and state

- One struct, loaded from the environment and flags once in `main`, validated fully before
  startup.
- Aggregate every invalid field into one error. No scattered `os.Getenv`.
- A secret comes from the environment or a file path, never committed.
- No global mutable state. A package level variable holds only a constant, a sentinel, a
  compiled regex or a template.
- No `init` side effects. A constructor takes its dependencies as parameters.

### Dependencies

- Define an interface at the consumer, not the implementation. One or two methods, named for
  behavior.
- Accept an interface, return a struct.
- No interface until a second implementation or a test fake needs one.
- Prefer the standard library. Every third party dependency needs a reason in the pull request.
- `go.mod` declares the oldest supported Go version. Run `go mod tidy` before commit and commit
  `go.sum`.

### License header

- Every source file carries the license header matching the repository's license, as the first
  comment after any build tags.

## Guardrails

- `internal/` holds the logic, `cmd/` only wires, `pkg/` justified or absent.
- Errors wrapped with `%w`, no panic in library code, no error logged more than once.
- `ctx` is the first parameter, no `context.Background()` outside `main` and tests.
- `log/slog` injected, no package level logger, no secret ever logged.
- Config loaded and validated once, no global mutable state, no `init` side effects.
- Interfaces small and defined at the consumer, each dependency justified.
- License header present on every source file.

## References

- <https://go.dev/wiki/CodeReviewComments>
