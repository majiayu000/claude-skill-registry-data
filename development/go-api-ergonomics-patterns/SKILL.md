---
name: go-api-ergonomics-patterns
description: >
  Use this for the Go-specific realization of the api-ergonomics-audit
  checklist — `(*Cache).Close()` shape, `errors.Is(err, ErrX)` discoverability,
  `Example_*` runnable godoc with `// Output:`, ctx-as-first-param convention,
  godoc starting with the symbol name, package-level sentinels with
  `[traces-to:]` markers, and stdlib-shaped constructors.
  Triggers: Example_, godoc, errors.Is, ErrX sentinel, ctx context.Context, var Err, http.Client, // Output:.
version: 1.0.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [go, ergonomics, sdk, api-design]
---

# go-api-ergonomics-patterns (v1.0.0)

## Scope

Go realization of the 8-point checklist in shared-core `api-ergonomics-audit`. The audit defines what to check; this skill defines what "good" looks like in Go.

## 5-line quickstart

The first ten minutes of a new integrator's life decide whether the SDK ships. "Hello world" is **construct → use → close**:

```go
cache, err := dragonfly.New(dragonfly.WithAddr("localhost:6379"))
if err != nil { return err }
defer cache.Close()
if err := cache.Set(ctx, "k", "v", 0); err != nil { return err }
v, err := cache.Get(ctx, "k")
```

If the quickstart exceeds 5 lines, either the Config has too many required fields (consider sensible defaults) or `New` has the wrong shape.

## Runnable Example with `// Output:` block

`Example_*` functions live in `*_example_test.go`. Two wins simultaneously: `go test` runs them (they catch silent breakage), and `pkg.go.dev` renders them as the intro:

```go
// Example demonstrates Set/Get round-trip and miss classification via errors.Is.
func Example() {
    mr, _ := miniredis.Run()
    defer mr.Close()
    cache, _ := dragonfly.New(dragonfly.WithAddr(mr.Addr()), dragonfly.WithProtocol(2))
    defer cache.Close()

    ctx := context.Background()
    _ = cache.Set(ctx, "greeting", "hello", 0)
    v, _ := cache.Get(ctx, "greeting")
    fmt.Println(v)

    _, err := cache.Get(ctx, "absent")
    if errors.Is(err, dragonfly.ErrNil) {
        fmt.Println("absent: miss")
    }
    // Output:
    // hello
    // absent: miss
}
```

Source: `core/l2cache/dragonfly/example_test.go` lines 20-57.

Naming convention: package-level `Example()` for the intro; `ExampleType_Method()` for each significant method (renders as a section under the type's godoc on pkg.go.dev).

## Sentinel-error discoverability

Every failure mode is a package-level `var ErrX = errors.New(...)`, with godoc starting with the symbol name and a `[traces-to:]` provenance marker:

```go
// ErrNil is the sentinel for "key not found" (mirrors redis.Nil).
// [traces-to: TPRD-§7-ErrNil]
var ErrNil = errors.New("dragonfly: key not found")

// ErrTimeout wraps context.DeadlineExceeded and net.Error timeouts.
// [traces-to: TPRD-§7-ErrTimeout]
var ErrTimeout = errors.New("dragonfly: timeout")
```

Caller pattern:

```go
v, err := cache.Get(ctx, "k")
if errors.Is(err, dragonfly.ErrNil) {
    return cacheMiss // discriminated, not string-matched
}
```

The sentinel set is semver-public — adding is minor, removing/renaming is major. Document the set in package godoc.

## ctx-first parameter ordering

Every I/O method takes `ctx context.Context` as the FIRST parameter:

```go
// GOOD
func (c *Cache) Get(ctx context.Context, key string) (string, error)

// BAD
func (c *Cache) Get(key string, ctx context.Context) (string, error)
```

`staticcheck` enforces this; reviewers flag deviations. Code generators that wrap your API also assume ctx-first.

## godoc starts with the symbol name

```go
// Cache is a Dragonfly L2 client...     ← good: starts with type name
type Cache struct { ... }

// Get fetches the value at key...        ← good
func (c *Cache) Get(...) (...)

// fetches the value at key                ← bad: doesn't start with name
func (c *Cache) Get(...) (...)
```

`staticcheck`'s `ST1020` and `gofmt` flag missing first-word-is-name. CLAUDE.md rule 6 requires godoc on every exported symbol.

## Compile-time interface assertion

When implementing a port:

```go
var _ ports.Cache = (*Cache)(nil) // compiles only if *Cache satisfies ports.Cache
```

Catches "I forgot to implement the new method" at build time, before tests.

## Anti-patterns

**1. String-matching error discrimination.** `if strings.Contains(err.Error(), "not found")` — fragile to godoc rewords. Fix: export `ErrNotFound`; consumer uses `errors.Is`.

**2. Two-error returns** `(T, error1, error2)` — always wrong. Pick a single error chain; use `errors.Is`/`errors.As` to discriminate.

**3. Surprising zero-value defaults.** `cache, _ := dragonfly.New()` returning a Cache that panics on first use. Either reject the zero-value config (return `ErrInvalidConfig`) OR provide an explicit `Default()` constructor.

**4. Missing `Example_*`.** pkg.go.dev shows "Examples" section with nothing in it. First-time users reverse-engineer construction from tests. Author at minimum a package-level `Example()`.

## Severity ladder

- **BLOCKER** — ctx not first, two-error returns, panic on documented valid input, forged zero-value
- **HIGH** — missing `Example_*`, missing sentinel for documented failure mode, quickstart >5 lines
- **MEDIUM** — sibling-package inconsistency (Shutdown vs Close, int-seconds vs Duration)
- **LOW** — godoc phrasing, ordering of options functions, package-doc thinness

## Cross-references

- shared-core `api-ergonomics-audit` — the 8-point checklist this realizes
- `go-sdk-config-struct-pattern` — constructor shape (drives quickstart length)
- `go-example-function-patterns` — Example function structure, `// Output:` discipline
- `go-error-handling-patterns` — sentinel taxonomy, `errors.Is`/`errors.As` discipline
- `sdk-marker-protocol` — `[traces-to:]` marker on every sentinel
- `sdk-semver-governance` — ergonomics-driven API rewrite triggers semver bumps
