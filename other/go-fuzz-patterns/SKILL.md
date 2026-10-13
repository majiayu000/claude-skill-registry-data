---
name: go-fuzz-patterns
description: >
  Use this when adding fuzz tests for input parsers (JSON, query params,
  headers), validating that handlers never panic on malformed input, or testing
  query builders for injection vulnerabilities. Covers Go native fuzzing
  (1.18+): FuzzXxx signature, f.Add corpus seeding, testdata/fuzz layout, and
  crash triage workflow.
  Triggers: FuzzXxx, fuzz target, corpus, testdata/fuzz, f.Add, f.Fuzz, crash triage.
---



# Fuzz Patterns

Standardizes fuzz testing across all microservices. Fuzzing finds edge
cases, panics, and security vulnerabilities by feeding random inputs to
parsers, handlers, and validators. Uses Go's native fuzzing (Go 1.18+).

## When to Activate
- When testing input parsing (JSON, query params, headers)
- When validating that handlers never panic on malformed input
- When testing query builders for injection vulnerabilities
- Used by: test-generator, simulated-security-reviewer, simulated-qa-engineer

## Go Native Fuzzing (Go 1.18+)

### Basic Fuzz Function

```go
func FuzzParseRequest(f *testing.F) {
    // Seed corpus with known inputs
    f.Add([]byte(`{"email":"user@example.com","name":"Test"}`))
    f.Add([]byte(`{}`))
    f.Add([]byte(`{"email":""}`))
    f.Add([]byte(`null`))
    f.Add([]byte{}) // empty

    f.Fuzz(func(t *testing.T, data []byte) {
        req, err := ParseCreateUserRequest(data)
        if err != nil {
            // Errors are expected for invalid input — not a bug
            return
        }
        // If parsing succeeded, validate invariants
        if req.Email == "" {
            t.Error("parsed request has empty email")
        }
    })
}
```

### Multi-Parameter Fuzzing

```go
func FuzzAuthenticate(f *testing.F) {
    f.Add("user@example.com", "password123")
    f.Add("", "")
    f.Add("admin@test.com", strings.Repeat("a", 10000))

    f.Fuzz(func(t *testing.T, email, password string) {
        // Must not panic regardless of input
        _, err := svc.Authenticate(ctx, email, password)
        if err == nil && email == "" {
            t.Error("authenticated with empty email")
        }
    })
}
```

### Corpus Management

```
testdata/
  fuzz/
    FuzzParseRequest/
      corpus/
        seed1           # Auto-generated corpus entries
        seed2
      crash-abc123      # Crash-causing inputs (bugs to fix)
```

- Corpus files are stored in `testdata/fuzz/<FuncName>/`
- `f.Add()` seeds are compiled into the binary
- The fuzzer discovers new inputs and saves interesting ones to corpus
- Crash inputs are saved with `crash-` prefix

### Running Fuzz Tests

```bash
# Run for 60 seconds
go test -fuzz=FuzzParseRequest -fuzztime=60s ./...

# Run until a crash is found
go test -fuzz=FuzzParseRequest ./...

# Run specific fuzz target
go test -fuzz=^FuzzAuthenticate$ -fuzztime=30s ./pkg/auth/

# Run all fuzz targets in a package
go test -fuzz=. -fuzztime=10s ./pkg/handlers/
```

### Crash Triage

When a fuzz crash is found:

1. **Reproduce**: `go test -run=FuzzParseRequest/crash-abc123 ./...`
2. **Analyze**: Read the crash input file — is it a realistic attack vector?
3. **Classify**:
   - Panic in production code = BUG (fix immediately)
   - Index out of bounds = BUG
   - Nil pointer dereference = BUG
   - Unhandled error = BUG (add validation)
   - Expected error not returned = BUG
4. **Fix**: Add input validation, then verify the crash input no longer causes failure
5. **Keep**: The crash file stays in corpus as a regression test

### Common Fuzz Targets

| Target | What to Fuzz | What to Assert |
|--------|-------------|----------------|
| JSON handlers | Random bytes as request body | No panic, valid error on invalid input |
| Query params | Random strings for filter/sort/page | No SQL injection, no panic |
| Path params | Random UUIDs, empty, special chars | 400 on invalid, no panic |
| Template renderer | Random merge field values | No SSTI, no panic |
| Auth tokens | Malformed JWTs, truncated tokens | Proper rejection, no panic |

### Integration with CI

```bash
# In CI, run fuzz tests for limited time (not indefinitely)
go test -fuzz=. -fuzztime=60s ./...

# Exit code 0 = no crashes found in time window
# Exit code 1 = crash found (investigate)
```

### Anti-Patterns

- Do NOT fuzz pure functions with bounded inputs (enums, booleans)
- Do NOT ignore panics — every panic in production code is a bug
- Do NOT run fuzz tests with `-race` in CI (too slow) — run separately
- Do NOT commit crash files without fixing the underlying bug first
