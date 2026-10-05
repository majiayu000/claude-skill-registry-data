---
name: go
description: Use when writing Go services, CLIs, or libraries. Covers idiomatic error wrapping, goroutine and context discipline, interface design, table-driven tests, and the race detector.
metadata:
  category: languages
  version: 1.0.0
  tags: [go, golang, concurrency, context, testing]
---

# Go

## Purpose

Write Go that is boring in the best sense: explicit errors, bounded concurrency, small interfaces, and tests that read like a specification.

## When to Use

- Building HTTP services, gRPC servers, or CLI tools in Go.
- Reviewing Go code for concurrency correctness or leaked goroutines.
- Designing package boundaries and interfaces.
- Diagnosing performance with pprof or the race detector.

## Capabilities

- Idiomatic error handling: wrapping, `errors.Is`, `errors.As`, sentinel errors.
- Concurrency: contexts, worker pools, `errgroup`, channel patterns, graceful shutdown.
- Interface design at the point of consumption.
- Table-driven tests, golden files, fuzzing, benchmarks.
- Profiling with pprof; escape analysis and allocation reduction.

## Inputs

- Package path or module.
- Go version (default: latest stable).
- Concurrency and latency requirements.

## Outputs

- Code that passes `go vet`, `staticcheck`, and `go test -race`.
- Table-driven tests covering error paths.
- A shutdown path that drains work and honors context cancellation.

## Workflow

1. **Define the contract** — Types and function signatures first. Errors are part of the signature.
2. **Implement the happy path** — Then handle every error explicitly. No `_ = err`.
3. **Bound concurrency** — Every goroutine has an owner, a cancellation path, and a place its error is read.
4. **Test the table** — Cases as data, including the error cases.
5. **Gate** — `go vet ./...`, `staticcheck ./...`, `go test -race ./...`.

## Best Practices

- Accept interfaces, return structs. Define the interface in the consuming package, not the producing one.
- Wrap errors with context: `fmt.Errorf("load user %s: %w", id, err)`. Wrap once per layer, no more.
- Pass `context.Context` as the first parameter to anything that does I/O. Never store it in a struct.
- A goroutine started without a way to stop it is a leak. Use `errgroup.WithContext` for anything fan-out.
- Do not use `panic` for control flow. It is for programmer error only.
- Preallocate slices when the size is known: `make([]T, 0, n)`.

## Examples

**Bounded fan-out with error propagation:**

```go
func FetchAll(ctx context.Context, ids []string, limit int) ([]User, error) {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(limit)

    users := make([]User, len(ids))
    for i, id := range ids {
        i, id := i, id
        g.Go(func() error {
            u, err := fetch(ctx, id)
            if err != nil {
                return fmt.Errorf("fetch user %s: %w", id, err)
            }
            users[i] = u
            return nil
        })
    }
    if err := g.Wait(); err != nil {
        return nil, err
    }
    return users, nil
}
```

**Table-driven test including failures:**

```go
func TestParseDuration(t *testing.T) {
    tests := map[string]struct {
        in      string
        want    time.Duration
        wantErr error
    }{
        "seconds":     {in: "30s", want: 30 * time.Second},
        "empty":       {in: "", wantErr: ErrEmptyInput},
        "bad unit":    {in: "5 fortnights", wantErr: ErrUnknownUnit},
    }
    for name, tc := range tests {
        t.Run(name, func(t *testing.T) {
            got, err := ParseDuration(tc.in)
            if !errors.Is(err, tc.wantErr) {
                t.Fatalf("err = %v, want %v", err, tc.wantErr)
            }
            if got != tc.want {
                t.Errorf("got %v, want %v", got, tc.want)
            }
        })
    }
}
```

## Notes

- `go test -race` catches data races only on code paths it actually executes. Race-test the concurrent paths deliberately.
- Since Go 1.22, loop variables are per-iteration; the `i, id := i, id` shadowing above is redundant on 1.22+ but harmless and still required on older versions.
- Generics are useful for containers and constraints, not as a substitute for interfaces.
