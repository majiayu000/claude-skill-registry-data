---
name: go-testing
description: 'Guides Go testing with TDD, table-driven tests, and fuzzing. Use when adding Go test coverage, writing benchmarks, or fuzzing input validation.'
---

# Go Testing Patterns

Comprehensive Go testing patterns for writing reliable, maintainable tests following TDD methodology.

## When to Activate

- Writing new Go functions or methods
- Adding test coverage to existing code
- Creating benchmarks for performance-critical code
- Implementing fuzz tests for input validation
- Following TDD workflow in Go projects

## Critical Rules

- Write the failing test first (RED-GREEN-REFACTOR).
- Use table-driven tests with `t.Run` subtests.
- Mark helpers with `t.Helper()`; use `t.Cleanup()` and `t.TempDir()` for cleanup.
- Run tests with `-race`.
- Do not use `time.Sleep()` for synchronization; use channels or conditions.
- Test error paths, not only the happy path.
- Test behavior through the public API, not private functions.

## References

Paths are relative to this SKILL.md's directory. Read only the file that matches the task. If a file cannot be read, say so.

- [references/test-structure.md](references/test-structure.md)
  Read when: TDD Workflow for Go, Table-Driven Tests, Subtests and Sub-benchmarks, Test Helpers (t.Helper, t.Cleanup, t.TempDir).

- [references/advanced-testing.md](references/advanced-testing.md)
  Read when: Golden Files, Mocking with Interfaces, Benchmarks, Fuzzing (Go 1.18+), HTTP Handler Testing, Integration with CI/CD.

## Test Coverage

### Running Coverage

```bash
# Basic coverage
go test -cover ./...

# Generate coverage profile
go test -coverprofile=coverage.out ./...

# View coverage in browser
go tool cover -html=coverage.out

# View coverage by function
go tool cover -func=coverage.out

# Coverage with race detection
go test -race -coverprofile=coverage.out ./...
```

### Coverage Targets

| Code Type               | Target  |
| ----------------------- | ------- |
| Critical business logic | 100%    |
| Public APIs             | 90%+    |
| General code            | 80%+    |
| Generated code          | Exclude |

### Excluding Generated Code from Coverage

```go
//go:generate mockgen -source=interface.go -destination=mock_interface.go

// In coverage profile, exclude with build tags:
// go test -cover -tags=!generate ./...
```

## Testing Commands

```bash
# Run all tests
go test ./...

# Run tests with verbose output
go test -v ./...

# Run specific test
go test -run TestAdd ./...

# Run tests matching pattern
go test -run "TestUser/Create" ./...

# Run tests with race detector
go test -race ./...

# Run tests with coverage
go test -cover -coverprofile=coverage.out ./...

# Run short tests only
go test -short ./...

# Run tests with timeout
go test -timeout 30s ./...

# Run benchmarks
go test -bench=. -benchmem ./...

# Run fuzzing
go test -fuzz=FuzzParse -fuzztime=30s ./...

# Count test runs (for flaky test detection)
go test -count=10 ./...
```

## Best Practices

**DO:**

- Write tests FIRST (TDD)
- Use table-driven tests for comprehensive coverage
- Test behavior, not implementation
- Use `t.Helper()` in helper functions
- Use `t.Parallel()` for independent tests
- Clean up resources with `t.Cleanup()`
- Use meaningful test names that describe the scenario

**DON'T:**

- Test private functions directly (test through public API)
- Use `time.Sleep()` in tests (use channels or conditions)
- Ignore flaky tests (fix or remove them)
- Mock everything (prefer integration tests when possible)
- Skip error path testing
