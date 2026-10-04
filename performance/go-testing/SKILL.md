---
name: go-testing
description: "Comprehensive guide for writing production-ready Golang tests. Covers table-driven tests, mocks, unit/integration tests, benchmarks, and fuzzing."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:25:00 GMT
---

## Best Practices

1. **Table-driven tests** — Use them for testing multiple scenarios. Always use named subtests with `t.Run`.
2. **Build tags for integration tests** — Use `//go:build integration` to separate slow or dependency-heavy tests.
3. **Independence** — Tests MUST NOT depend on execution order.
4. **Parallelism** — Use `t.Parallel()` for independent tests to speed up the suite.
5. **Mock interfaces, not types** — Define interfaces where they are consumed.
6. **Race detection** — Always run tests with `-race` in CI.
7. **Goroutine leaks** — Use `go.uber.org/goleak` to ensure no goroutines are left running.
8. **Examples** — Write `func ExampleXxx()` to provide executable documentation.

## Table-Driven Test Example

```go
func TestCalculate(t *testing.T) {
    tests := []struct {
        name     string
        input    int
        expected int
        wantErr  bool
    }{
        {
            name:     "positive number",
            input:    10,
            expected: 20,
        },
        {
            name:    "negative number",
            input:   -1,
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Calculate(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("Calculate() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.expected {
                t.Errorf("Calculate() = %v, want %v", got, tt.expected)
            }
        })
    }
}
```

## Integration Tests

Use a build tag at the top of the file:
```go
//go:build integration

package service_test
```

Run with: `go test -tags=integration ./...`

## Naming Conventions

- `TestXxx(*testing.T)` — Unit/Integration tests.
- `BenchmarkXxx(*testing.B)` — Performance tests.
- `ExampleXxx()` — Documentation examples.
- `FuzzXxx(*testing.F)` — Fuzz tests.

## Common Commands

```bash
go test ./...                # Run all tests
go test -race ./...          # Run with race detector
go test -coverprofile=c.out  # Generate coverage profile
go test -bench=. -benchmem   # Run benchmarks with memory stats
go test -fuzz=FuzzName       # Run fuzz test
```

## Anti-patterns

- ❌ **Tests depending on shared state** (e.g., global variables) that aren't reset.
- ❌ **Slow tests in the default suite** (should use build tags).
- ❌ **Testing unexported implementation details** instead of behavior.
- ❌ **Missing `t.Run` name**, making failures hard to debug.
- ❌ **Hardcoded file paths** that only work on one machine.
