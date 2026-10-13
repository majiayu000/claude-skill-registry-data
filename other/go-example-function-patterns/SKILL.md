---
name: go-example-function-patterns
description: >
  Use this when authoring or reviewing Example_* testable godoc functions for
  exported SDK symbols, deciding between in-package and _test black-box examples,
  or wiring deterministic // Output: blocks. Covers ExampleFoo_Bar naming,
  Ordered/Unordered output variants, package _test conventions, and the
  [traces-to:] marker requirement.
  Triggers: ExampleCache_, godoc example, Example_ function, docs wave, // Output:, Example_, testable example.
---

# go-example-function-patterns (v1.0.0)

## Rationale

`Example_*` functions in `_test.go` files serve three simultaneous purposes: (1) they render on pkg.go.dev as live, editable code samples; (2) `go test` executes them and diffs stdout against the `// Output:` comment — any mismatch fails the test; (3) they prove the exported API surface is ergonomic enough to call in isolation. Rule 14 of `CLAUDE.md` ("Every exported func has at least one `Example_*` where applicable") and rule 16 (story-level completeness, requirement (e)) make these mandatory for generated SDK symbols. The Go `testing` package documentation (`go doc testing` §Examples) is the canonical spec; this skill codifies the SDK-specific conventions on top.

## Target SDK Convention

Current convention in motadatagosdk (see `core/l2cache/dragonfly/example_test.go`):
- Examples live in `example_test.go` in the package (either `package foo` or `package foo_test` — black-box preferred for public API).
- Package-level example: `func Example()`.
- Method on type `T`: `func ExampleT_Method()`.
- Multiple variants of the same method: `func ExampleT_Method_suffix()` (lowercase suffix).
- Every example that produces deterministic output terminates in a `// Output:` block (or `// Unordered output:` when order is an artifact of map iteration).
- The first non-test dep for in-package examples of network clients is a local fake (e.g., `miniredis`) — examples must RUN, not just compile.
- `[traces-to: TPRD-§11.1 G16-examples]` marker on the example file header (required by G99).

If TPRD requests divergence: never. These are contract tests. Only add variants; do not subtract.

## Activation signals

- TPRD §7 adds a new exported function / method / type.
- `sdk-impl-lead` wave M6 ("docs / examples") is active.
- `sdk-marker-scanner` reports a generated symbol without an `Example_` in the same package (rule 16 check).
- `example-drop` compensating baseline warning (rule 28 signal 4) fires — someone removed an example.
- Reviewer sees a godoc with no runnable example on an exported method.

## GOOD examples

### 1. Package-level `Example()` with deterministic `// Output:`

```go
// example_test.go
package buffer_test

import (
    "fmt"

    "motadatagosdk/utils/buffer"
)

// Example demonstrates constructing a Buffer, writing bytes, and reading
// them back. The Output block is verified by `go test`.
func Example() {
    b := buffer.New(16)
    b.WriteString("hello")
    fmt.Println(b.String())
    fmt.Println(b.Len())
    // Output:
    // hello
    // 5
}
```

`go test` tokenises stdout after the example returns and diffs it against the lines after `// Output:`. Leading/trailing whitespace is trimmed per line. Any mismatch = FAIL.

### 2. `ExampleT_Method` naming — one per exported method

```go
// ExampleCache_Set shows a Set + Get round trip against a miniredis fake.
// The Output block proves the key is readable after Set returns.
func ExampleCache_Set() {
    mr, _ := miniredis.Run()
    defer mr.Close()

    c, _ := dragonfly.New(dragonfly.WithAddr(mr.Addr()), dragonfly.WithProtocol(2))
    defer c.Close()

    ctx := context.Background()
    _ = c.Set(ctx, "k", "v", 0)
    v, _ := c.Get(ctx, "k")
    fmt.Println(v)
    // Output:
    // v
}
```

Naming rule from `go doc testing`: `ExampleF`, `ExampleT`, `ExampleT_M`, or any of those suffixed with `_<lowercase-suffix>`.

### 3. Multiple variants via lowercase suffix

```go
func ExampleCache_Set_withTTL() {
    mr, _ := miniredis.Run()
    defer mr.Close()
    c, _ := dragonfly.New(dragonfly.WithAddr(mr.Addr()), dragonfly.WithProtocol(2))
    defer c.Close()
    ctx := context.Background()
    _ = c.Set(ctx, "session:42", "token", 30*time.Second)
    ttl, _ := c.TTL(ctx, "session:42")
    fmt.Println(ttl > 0)
    // Output:
    // true
}

func ExampleCache_Set_withKeyPrefix() {
    mr, _ := miniredis.Run()
    defer mr.Close()
    c, _ := dragonfly.New(
        dragonfly.WithAddr(mr.Addr()),
        dragonfly.WithKeyPrefix("tenant42:"),
        dragonfly.WithProtocol(2),
    )
    defer c.Close()
    ctx := context.Background()
    _ = c.Set(ctx, "user:1", "alice", 0)
    // Raw key stored in backend reflects the prefix.
    raw, _ := mr.Get("tenant42:user:1")
    fmt.Println(raw)
    // Output:
    // alice
}
```

### 4. `// Unordered output:` when iteration order is not guaranteed

```go
// ExampleStats_Keys iterates a map's keys — Go randomises map iteration,
// so the output order is NOT stable between runs. `// Unordered output:`
// makes the testing framework sort both sides before comparing.
func ExampleStats_Keys() {
    s := stats.New()
    s.Inc("hits")
    s.Inc("misses")
    s.Inc("errors")
    for _, k := range s.Keys() {
        fmt.Println(k)
    }
    // Unordered output:
    // errors
    // hits
    // misses
}
```

Mismatch: using `// Output:` on a map-iteration example will randomly fail CI on the runs where iteration order flips.

### 5. Example that documents an error path

```go
// ExampleCache_Get_miss documents the sentinel returned when a key is
// absent. errors.Is is the contract callers rely on.
func ExampleCache_Get_miss() {
    mr, _ := miniredis.Run()
    defer mr.Close()
    c, _ := dragonfly.New(dragonfly.WithAddr(mr.Addr()), dragonfly.WithProtocol(2))
    defer c.Close()

    _, err := c.Get(context.Background(), "never-set")
    if errors.Is(err, dragonfly.ErrNil) {
        fmt.Println("miss")
    }
    // Output:
    // miss
}
```

## BAD examples

### 1. `// Output:` comment mismatched with printed text

```go
// BAD: Example compiles but fails under `go test`.
func ExampleCache_Set() {
    fmt.Println("hello")
    // Output:
    // Hello        ← capital H; go test will report a diff and fail.
}
```

Fix: the Output block is exact-match after per-line trim. Copy the literal output; do not paraphrase.

### 2. Non-deterministic output with `// Output:` (randomised iteration or time)

```go
// BAD: fmt.Println of a map prints keys in random order → flaky test.
func ExampleStats_Dump() {
    s := stats.Dump()
    fmt.Println(s)
    // Output:
    // map[hits:1 misses:0]
}
```

Fix: either sort the keys before printing, or use `// Unordered output:` (each line independent, order-agnostic).

### 3. Network call with no fake / no hermetic execution

```go
// BAD: Example hits a real Dragonfly at a hardcoded IP. Fails in CI,
// fails on pkg.go.dev's sandbox, fails everywhere except the author's
// laptop.
func ExampleCache_Get() {
    c, _ := dragonfly.New(dragonfly.WithAddr("10.0.0.5:6379"))
    v, _ := c.Get(context.Background(), "k")
    fmt.Println(v)
}
```

Fix: use `miniredis.Run()` (already a test dep on the dragonfly package), a `net.Listen("tcp", "127.0.0.1:0")` local stub, or a `*httptest.Server` — whatever makes the example run hermetically.

### 4. Wrong naming — `TestExampleFoo` or `Example_Foo` (underscore-prefix)

```go
// BAD: TestExampleFoo is a normal test, not an example; godoc won't pick
// it up and the Output comment is ignored.
func TestExampleFoo(t *testing.T) { ... }

// BAD: leading underscore makes the name "_Foo" per the grammar; not a
// valid Example name.
func Example_Foo() { ... }
```

Fix: the grammar from `go doc testing` is strict — `Example`, `ExampleF`, `ExampleT`, `ExampleT_M`, optionally suffixed with `_<lowercase>`. Anything else is silently dropped.

### 5. Missing `// Output:` — example runs but nothing is verified

```go
// BAD: Compiles + is discoverable by godoc, but `go test` does NOT
// execute it (no Output block = treated as compile-only). Typos in
// the body never fail CI.
func ExampleCache_Set() {
    c, _ := dragonfly.New(dragonfly.WithAddr("..."))
    _ = c.Set(context.Background(), "k", "v", 0)
}
```

Fix: every example that has a meaningful observable effect should end with `// Output:` lines. If truly no output, add `// Output:` with no following lines — explicit "expect empty stdout" still runs the body.

## Decision criteria

| Situation | Choice |
|---|---|
| Exported method of type `T` | `ExampleT_Method()` |
| Package-level function / overall package demo | `Example()` or `ExampleFuncName()` |
| Second variant of the same method | `ExampleT_Method_<lowercase-suffix>()` |
| Output depends on map iteration / parallel goroutines | `// Unordered output:` |
| Output is deterministic | `// Output:` |
| No meaningful stdout (pure side effect) | Either omit entirely (compile-only), OR add empty `// Output:` to prove no stderr noise — preferred for contract-bearing examples |
| Network / DB involved | Use hermetic fake (`miniredis`, `httptest`, in-memory sqlite); NEVER real endpoints |

## Cross-references

- `sdk-marker-protocol` — `[traces-to: TPRD-§11.1 G16-examples]` file-header marker
- `go-testing-patterns` — unit-test conventions (don't confuse TestXxx with ExampleXxx)
- `go-sdk-config-struct-pattern` — examples illustrating `Config{} + New(cfg)` are the canonical doc surface
- `go-mock-patterns` / `go-testcontainers-setup` — hermetic fake choice for runnable examples

## Guardrail hooks

- **G99** — `[traces-to:]` marker required on pipeline-generated `example_test.go` files.
- **Rule 14 / rule 16** — `sdk-marker-scanner` reports missing `Example_*` per exported symbol; maps to the `coverage-baselines.json` example count per package.
- **Compensating baseline signal 4** (rule 28) — `example-drop` warning fires if the per-package example count decreases between runs; WARN-level, surfaced at H10.
- `go test -run '^$' -v ./<pkg>` — the standard CI invocation runs examples along with tests; any `// Output:` diff fails the build (no special configuration needed).
