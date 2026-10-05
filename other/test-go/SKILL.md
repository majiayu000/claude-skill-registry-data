---
name: test-go
description: "Write, review, and improve Go test code for this project. Use whenever generating, reviewing, or modifying Go tests - including when invoked by the Tester agent, the /test prompt, or any test-related request. Covers table-driven tests, subtests, t.Parallel(), test helpers with t.Helper(), error assertions via errors.As/errors.Is, fixture loading from testdata/, httptest servers, env-gated integration tests, mock/fake/spy patterns, and adapter conformance. Do NOT use for benchmarks or performance profiling."
metadata:
  author: Serghei Iakovlev
  version: "1.0"
  category: testing
---

# Go Testing

## Placeholders

Examples below use two placeholders. They are not literal - substitute the actual names from the project being worked on, matching the case of the surrounding context:

- `{PROJECT}` - the project's identifier (e.g. env-var prefix, repo name). In env vars: `MYAPP_…`. In prose: `MyApp` or `myapp`.
- `{integration}` - an external system or adapter name (e.g. `jira`, `stripe`, `claude`). In paths: `internal/tracker/jira/`. In env vars: `JIRA_…`. In type names: `JiraAdapter`.

`.go` files in `assets/` and the examples below use sample names (package `example`, `Adapter`, `NewAdapter`, `FunctionName`, `MYAPP_INTEGRATION_TEST`) so they stay syntactically valid Go. Rename each to the project's real name. The templates carry no comments; see [Comments](#comments) before adding one.

## Decision Framework

Before writing any test, determine which category it belongs to:

| Category               | Characteristics                                    | Run condition                                           |
| ---------------------- | -------------------------------------------------- | ------------------------------------------------------- |
| **Unit**               | Deterministic, no I/O, no network                  | Always (`make test`)                                    |
| **Unit with fixtures** | Reads `testdata/` files, uses `t.TempDir()`        | Always                                                  |
| **Unit with httptest** | Spins up `httptest.NewServer`, tests HTTP adapters | Always                                                  |
| **Integration**        | Talks to real external service                     | Env-gated by per-adapter variable: `{PROJECT}_{INTEGRATION}_TEST=1`     |

Pick the lightest category that validates the behavior.

---

## Canonical Test Structure

Every test file in this project follows this skeleton: helpers first, then test functions. Internalize it - do not deviate. Declaration order carries the structure, so do not add banner comments to mark the sections; the `go-codestyle` rule bans them.

```go
package pkg

import "testing"

func mustThing(t *testing.T) *Thing {
    t.Helper()
    thing, err := NewThing()
    if err != nil {
        t.Fatalf("NewThing: %v", err)
    }
    t.Cleanup(thing.Close)
    return thing
}

func TestThingDoesWork(t *testing.T) {
    t.Parallel()

    thing := mustThing(t)
    if err := thing.DoWork(); err != nil {
        t.Fatalf("DoWork() = %v, want nil", err)
    }
}
```

The package clause is `pkg`, or `pkg_test` for a black-box test.

**Key rules this project enforces:**

1. `t.Helper()` is the first statement in every helper - no exceptions.
2. `t.Cleanup()` for teardown in helpers; `defer` only in test functions themselves, and never to wait on background work.
3. `t.Parallel()` at both test and subtest level for independent cases.
4. `t.TempDir()` for filesystem isolation - never write to fixed paths.
5. `t.Setenv()` for environment variables and `t.Chdir()` for the working directory, never in a parallel test.
6. Errors use `errors.As()` / `errors.Is()` - never string comparison.
7. `t.Fatal` / `t.Fatalf` / `t.FailNow` only from the goroutine running the test; `t.Error` never from one that can outlive it.

### Waiting on background work

`t.Context()` is canceled *just before* Cleanup functions run, and a `defer` in the test body runs *before* both. So `defer wg.Wait()` on a goroutine that exits on `t.Context().Done()` waits for something nothing has told to stop, and the test hangs to `panic: test timed out`. Register the wait with `t.Cleanup(wg.Wait)`, which runs after the cancellation. This is the one exception to rule 2.

### Process-wide state and t.Parallel

`t.Setenv` and `t.Chdir` mutate the whole process, so calling either in a parallel test or a test with a parallel ancestor panics with `testing: test using t.Setenv, t.Chdir, or cryptotest.SetGlobalRandom can not use t.Parallel`. Two ways out: drop `t.Parallel()` from that one test, or have the code under test take the value as a parameter instead of reading the process, which keeps the test parallel. `testing.AllocsPerRun` is the same class: it panics when a parallel test is running while it is called, so never call it from a parallel test or from a subtest of one.

### Failing from a goroutine that is not the test

`FailNow` stops the goroutine it runs on and nothing else, so `t.Fatal` from a server handler fails the test without stopping it and the caller sees a connection error instead of the real cause. `t.Error` is no safer: once the test has returned, it panics with `Fail in goroutine after <test> has completed`, `net/http` recovers that panic inside the handler, and the assertion disappears - the test prints PASS while the suite exits FAIL naming no test at all. Record what the goroutine saw and assert on it from the test body.

---

## Comments

A test file carries no comments by default. The test name, the case names, and the failure messages say what is checked; a comment that repeats them is one more thing the next reader has to verify, and it goes stale when the test changes. Write the test so it needs no explanation.

- No doc comment on a `Test`, `Benchmark`, or `Fuzz` function, a helper, or a test double. When the name does not say what the test checks, rename it.
- No comment inside a test body that narrates setup, the call, or the assertions. Extract the block into a helper whose name says it, or rename the variable that raised the question.
- A comment earns its place only for what the code cannot say: the upstream issue or RFC a regression test pins, a protocol or business constraint, a workaround, or a warning about call order, a race, or a hidden cost. The `loadFixture` comment in [HTTP Adapter Testing](#http-adapter-testing) is one.
- Do not copy comments from the surrounding tests. In a test file you edit, delete every comment that breaks these rules, including the ones already there. When a comment mixes a reason with a restatement, keep the reason and drop the restatement. Cleaning comment noise out of a file you already change is part of the change.

---

## Table-Driven Tests

Use when multiple cases share identical execution logic. This is the dominant pattern in this project.

```go
func TestSanitizeKey(t *testing.T) {
    t.Parallel()

    tests := []struct {
        name    string
        input   string
        want    string
        wantErr bool
    }{
        {"simple key", "ABC-123", "ABC-123", false},
        {"empty input", "", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()

            got, err := SanitizeKey(tt.input)

            if tt.wantErr {
                if err == nil {
                    t.Fatalf("SanitizeKey(%q) = %q, want error", tt.input, got)
                }
                return
            }
            if err != nil {
                t.Fatalf("SanitizeKey(%q) unexpected error: %v", tt.input, err)
            }
            if got != tt.want {
                t.Errorf("SanitizeKey(%q) = %q, want %q", tt.input, got, tt.want)
            }
        })
    }
}
```

**When NOT to use tables:** cases needing different setup, conditional mocking, or complex branching. Write separate `t.Run` blocks or separate test functions instead.

**Table struct conventions:**

- Always include `name string` as the first field
- Use `wantErr bool` for error presence; add `wantKind` field for typed error checking
- Use field names (not positional) when structs have more than 3 fields
- Include inputs in failure messages: `FuncName(%v) = %v, want %v`

---

## Error Testing

This project uses custom typed errors extensively. Test error semantics, never strings.

```go
func assertTrackerErrorKind(t *testing.T, err error, want domain.TrackerErrorKind) {
    t.Helper()
    if err == nil {
        t.Fatalf("expected error with kind %q, got nil", want)
    }
    var te *domain.TrackerError
    if !errors.As(err, &te) {
        t.Fatalf("error type = %T, want *domain.TrackerError", err)
    }
    if te.Kind != want {
        t.Errorf("TrackerError.Kind = %q, want %q", te.Kind, want)
    }
}
```

**Error testing rules:**

- `errors.As()` for type assertion - validates the error chain, not just the top
- `errors.Is()` for sentinel comparison
- Test the `Kind`/`Field`/`Op` of typed errors, not `.Error()` strings
- `t.Fatal` when nil-error means subsequent assertions will panic; `t.Error` otherwise

---

## Test Helpers

Helpers belong at the top of the test file, before test functions. Each adapter package defines its own helpers - do not create a shared `testutil` package.

**Common helper patterns in this project:**

```go
func mustAdapter(t *testing.T, config map[string]any) *Adapter {
    t.Helper()
    a, err := NewAdapter(config)
    if err != nil {
        t.Fatalf("NewAdapter: %v", err)
    }
    return a.(*Adapter)
}

func loadFixture(t *testing.T, name string) []byte {
    t.Helper()
    data, err := os.ReadFile("testdata/" + name)
    if err != nil {
        t.Fatalf("reading fixture %s: %v", name, err)
    }
    return data
}

func validConfig(endpoint string) map[string]any {
    return map[string]any{
        "endpoint": endpoint,
        "api_key":  "user@test.com:api_token_123",
        "project":  "PROJ",
    }
}

func closeStore(t *testing.T, s *Store) {
    t.Helper()
    if err := s.Close(); err != nil {
        t.Errorf("Close: %v", err)
    }
}
```

**Naming conventions:**

- `mustX` - creates X or fatals (setup that cannot fail gracefully)
- `validX` / `defaultX` - returns baseline config/params for test customization
- `loadFixture` - reads from `testdata/`
- `assertX` / `requireX` - assertion helpers (`require` fatals, `assert` errors)

---

## HTTP Adapter Testing

Adapter tests use `httptest.NewServer` with handler functions that return fixture data. Never mock the `http.Client` itself.

```go
func TestFetchIssues(t *testing.T) {
    t.Parallel()

    // loadFixture fatals, and t.Fatal cannot stop the test from a handler.
    fixture := loadFixture(t, "search_single_page.json")

    var gotAuth atomic.Value
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        gotAuth.Store(r.Header.Get("Authorization"))
        w.Header().Set("Content-Type", "application/json")
        w.Write(fixture)
    }))
    defer srv.Close()

    adapter := mustAdapter(t, validConfig(srv.URL))
    issues, err := adapter.FetchIssuesByStates(context.Background(), []string{"To Do"})
    if err != nil {
        t.Fatalf("FetchIssuesByStates: %v", err)
    }
    if auth, _ := gotAuth.Load().(string); auth == "" {
        t.Errorf("Authorization header = %q, want non-empty", auth)
    }
    if len(issues) != 1 {
        t.Errorf("FetchIssuesByStates returned %d issues, want 1", len(issues))
    }
}
```

**Rules for httptest usage:**

- Read every fixture before `httptest.NewServer`; the handler writes bytes it already holds. A handler that calls a `t.Fatal`-ing helper leaves the client with `Get "http://127.0.0.1:PORT": EOF` instead of the real cause
- Capture request headers, query params, and method in the handler; assert on the captured values from the test body, where a failed assertion can still stop the test
- Return fixture JSON from `testdata/` - do not inline large JSON strings
- Assert on domain-level objects after adapter normalization, not raw payloads
- Use `atomic` values and counters for anything the handler records, because the handler runs on another goroutine

---

## Integration Tests (Env-Gated)

Integration tests talk to real external services. They MUST be gated by environment variables and skip cleanly when disabled.

> Read [references/integration-tests.md](references/integration-tests.md) for the full integration testing protocol including skip helpers, required env vars, and CI configuration.

**Quick reference:**

```go
func skipUnlessIntegration(t *testing.T) {
    t.Helper()
    if os.Getenv("MYAPP_INTEGRATION_TEST") != "1" {
        t.Skip("skipping integration test: set MYAPP_INTEGRATION_TEST=1 to enable")
    }
}
```

- File naming: `integration_test.go` (separate from unit tests)
- Skip with `t.Skip`, not silent pass - skipped tests are visible in output
- Use isolated test data; clean up artifacts when practical
- Never fail CI when env var is absent

---

## Adapter Conformance Testing

Every adapter (tracker or agent) must prove it satisfies the domain interface. Use compile-time interface checks and conformance test suites.

```go
var _ domain.TrackerAdapter = (*Adapter)(nil)
var _ domain.AgentAdapter = (*mockAgentAdapter)(nil)
```

**What conformance tests must cover (per architecture Section 17):**

- Normalized field mapping (issue state, priority, labels → domain types)
- Pagination handling (order preserved across pages)
- Error category mapping (transport, auth, API, payload → typed errors)
- Config validation (required fields, defaults, invalid combinations)

---

## Mock and Test Double Patterns

This project uses three kinds of test doubles - pick the lightest one that works.

| Double   | Purpose                                  | Example                                                        |
| -------- | ---------------------------------------- | -------------------------------------------------------------- |
| **Stub** | Returns fixed data                       | `validConfig()` returning a map                                |
| **Fake** | Simplified working implementation        | `internal/agent/mock` package, `internal/tracker/file` adapter |
| **Spy**  | Records interactions for later assertion | `httptest` handler with `atomic` counters                      |

**Registered fakes** (when this project provides them, e.g. `internal/agent/mock/`, `internal/tracker/file/`) are first-class adapters in the registry. Use them for orchestrator-level tests that need controllable adapter behavior - check the project layout for the actual package paths.

**Mock struct pattern:**

```go
type mockTrackerAdapter struct{}
var _ domain.TrackerAdapter = (*mockTrackerAdapter)(nil)

func (m *mockTrackerAdapter) FetchIssuesByStates(ctx context.Context, states []string) ([]domain.Issue, error) {
    return nil, nil
}
```

Implement every method of the interface; the compile-time check fails until you do.

---

## Fixture Management

Store test data in `testdata/` within the package directory. Go tooling ignores this directory during builds.

```
internal/tracker/{integration}/testdata/
    search_single_page.json
    search_multi_page_1.json
    search_multi_page_2.json
    issue_detail.json
    comments.json
```

**Rules:**

- One `testdata/` directory per package that needs fixtures
- Name fixtures descriptively: `search_empty.json`, `malformed.json`, `comments_multi_page_1.json`
- Load via `loadFixture(t, name)` helper - never hardcode paths in test functions
- JSON fixtures should be real (or realistic) API responses, not minimal stubs

---

## Failure Message Format

Every assertion must produce a message diagnosable without reading the test source.

```
Format: FuncName(inputs) = got, want expected
```

Correct, naming the function, the input, got, and want:

```go
t.Errorf("SanitizeKey(%q) = %q, want %q", tt.input, got, tt.want)
t.Errorf("TrackerError.Kind = %q, want %q", te.Kind, want)
```

Incorrect, missing context:

```go
t.Errorf("got %q, want %q", got, tt.want)
t.Error("wrong result")
```

- Always `got` before `want` in message ordering
- Use `%q` for strings (shows quotes and escapes), `%v` for general values
- Use `%d` for integers, `%f` for floats - match the type

---

## Validation Checklist

After writing or modifying tests, verify:

- [ ] `make test` passes with `-race` (the default)
- [ ] Independent test functions and subtests call `t.Parallel()`; those using `t.Setenv`, `t.Chdir` or `testing.AllocsPerRun` do not
- [ ] No `t.Fatal` / `t.Error` inside an `http.HandlerFunc` or any other spawned goroutine
- [ ] All helpers call `t.Helper()` as first statement
- [ ] No doc comment on a test, helper, or double, and no comment in the file restates the code; every remaining comment gives a reason
- [ ] Error assertions use `errors.As()` / `errors.Is()`, not string comparison
- [ ] Failure messages include function name, inputs, got, and want
- [ ] Integration tests skip cleanly without their env var
- [ ] No external assertion libraries introduced (use stdlib + `cmp.Diff` if needed)
- [ ] Fixtures live in `testdata/` and are loaded via helper
- [ ] `t.TempDir()` used for any filesystem operations
