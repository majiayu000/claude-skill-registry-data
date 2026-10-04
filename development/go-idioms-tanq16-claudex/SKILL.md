---
name: go-idioms
description: Modern Go 1.27+ idioms and dependency selection, applied to every Go file written or reviewed. Use when writing or refactoring any Go code, when reading or writing JSON, when choosing between a standard-library helper and a hand-rolled loop, or when adding, auditing, or upgrading a dependency in go.mod. Triggers on interface{}, wg.Add, errors.As, atomic.LoadInt32, manual index loops, sync.Once, time.Now().Sub, encoding/json, json.MarshalIndent, json.NewDecoder, google/uuid, and on any go.mod change.
user-invocable: false
---

# Go Idioms

**The Go 1.27+ baseline every file in these projects is written to, and how a dependency earns its place in `go.mod`.**

The `go` directive reads `go 1.27` or newer on every project. There is no version detection and no fallback path, so a current idiom is always available and an outdated one is always a choice. `go test` runs the `stdversion` vet check by default, so a symbol newer than the directive is reported rather than discovered by a user on an older toolchain.

`go fix` applies part of this file mechanically: `atomictypes` moves `sync/atomic` calls onto the typed atomics, and `waitgroupgo` rewrites an `Add`, `go`, `Done` trio into `wg.Go`.

## Types and Built-ins

`any` replaces `interface{}`, because the two are identical to the compiler and only one of them reads as deliberate.

`min` and `max` replace hand-rolled comparisons: `max(a, b)`, `min(start+size-1, end)`.

`clear` empties a map (`clear(m)`) or zeroes a slice's elements (`clear(s)`), which frees the caller from a loop whose only job is bookkeeping.

## slices

Prefer these over manual loops, since each one states the intent that a loop only implies.

- `slices.Contains(items, x)` for membership.
- `slices.Index(items, x)` and `slices.IndexFunc(items, func(it T) bool { ... })`, returning `-1` when absent.
- `slices.Sort(items)` for ordered types, and `slices.SortFunc(items, func(a, b T) int { return cmp.Compare(a.X, b.X) })` otherwise.
- `slices.Max(items)` and `slices.Min(items)`.
- `slices.Reverse`, `slices.Compact` (drops consecutive duplicates), `slices.Clone`, `slices.Clip`.
- `slices.Delete(s, i, i+1)` to remove one element, rather than the `append(s[:i], s[i+1:]...)` splice.

## maps

- `maps.Clone(m)` instead of a copy loop.
- `maps.Copy(dst, src)` to merge entries.
- `maps.DeleteFunc(m, func(k K, v V) bool { ... })` for conditional deletion.
- `maps.Keys(m)` and `maps.Values(m)` return iterators rather than slices.

## cmp

`cmp.Compare(a, b)` pairs with `slices.SortFunc`. `cmp.Or` returns the first non-zero value, which collapses a chain of fallbacks into one line:

```go
name := cmp.Or(os.Getenv("NAME"), cfg.Name, "default")
```

## Iteration

Range over an integer when you only need a count: `for i := range len(items)` or `for range n`. The three-clause form leaves a mutable index in scope that nothing needs.

```go
keys := slices.Collect(maps.Keys(m))       // not a manual append loop
sortedKeys := slices.Sorted(maps.Keys(m))  // collect and sort in one step
for k := range maps.Keys(m) {
    process(k)
}
```

## sync

`wg.Go(fn)` spawns a WaitGroup goroutine and handles `Add` and `Done` internally, which removes the commonest concurrency bug in Go: an `Add`/`Done` pair that stops matching after an early return.

```go
var wg sync.WaitGroup
for _, item := range items {
    wg.Go(func() { process(item) })
}
wg.Wait()
```

`sync.OnceFunc` and `sync.OnceValue` replace a `sync.Once` plus its wrapper, keeping the guarded value and its guard in one expression:

```go
warmCache := sync.OnceFunc(func() { /* runs at most once */ })
getConfig := sync.OnceValue(func() Config { return loadConfig() })
```

Typed atomics (`atomic.Bool`, `atomic.Int64`, `atomic.Pointer[T]`) replace the `atomic.LoadInt32` and `atomic.StoreInt32` free functions, because the typed form makes the atomicity a property of the variable rather than of each call site that remembers to use it.

## errors

`errors.Is(err, target)` replaces `err == target`, since it sees through wrapping and the comparison does not.

`errors.Join(err1, err2, ...)` combines several errors into one that `errors.Is` still matches against each.

`errors.AsType[T](err)` replaces the `errors.As(err, &target)` two-step:

```go
if pathErr, ok := errors.AsType[*os.PathError](err); ok {
    handle(pathErr)
}
```

## Context cancellation causes

`context.WithCancelCause(parent)` returns a `cancel(err)` whose reason `context.Cause(ctx)` reads back, which turns a bare "context canceled" into the actual failure.

`context.WithTimeoutCause` and `context.WithDeadlineCause` attach a cause to a timeout. `context.AfterFunc(ctx, cleanup)` runs `cleanup` on cancellation without a goroutine of your own.

## strings and bytes

`strings.Cut(s, sep)` returns `before, after, found` in one call, replacing an `Index` plus two slice expressions that can disagree about the separator length. `bytes.Cut` behaves the same.

```go
if rest, ok := strings.CutPrefix(s, "id:"); ok {
    use(rest)
}
```

`strings.SplitSeq` and `strings.FieldsSeq` (and their `bytes` equivalents) iterate without allocating the full slice:

```go
for part := range strings.SplitSeq(s, ",") {
    process(part)
}
```

`strings.CutLast` and `bytes.CutLast` cut around the last occurrence instead of the first, replacing a `LastIndex` plus the two slice expressions that have to agree with it.

## JSON

`encoding/json/v2` is what new code imports, with `encoding/json/jsontext` supplying the options that shape the output. The import binds the identifier `json`, so the call sites read as they always did.

```go
import (
    "encoding/json/jsontext"
    "encoding/json/v2"
)

data, err := json.Marshal(state, jsontext.WithIndent("  "))
```

There is no `MarshalIndent` in v2, because indentation is an option rather than a second function. `json.RawMessage` is gone too, and a field holding a raw JSON value takes `jsontext.Value`.

`MarshalWrite` and `UnmarshalRead` take an `io.Writer` and an `io.Reader` directly, which removes the `Encoder` or `Decoder` built to carry a single value:

```go
if err := json.UnmarshalRead(resp.Body, &payload); err != nil {
    return err
}
return json.MarshalWrite(w, result)
```

v2 rejects a duplicate object member name and invalid UTF-8 inside a string, both of which v1 accepts silently. A state file or an endpoint that was tolerating either starts reporting it.

`encoding/json` keeps working and is now backed by the v2 implementation, so an existing file already gets the faster unmarshal without being rewritten.

## time

`time.Since(start)` and `time.Until(deadline)` replace the `Sub` forms, which read backwards.

`time.Tick` is safe to use freely. Since Go 1.23 the garbage collector reclaims unreferenced tickers, so `NewTicker` plus `Stop` buys nothing when `Tick` will do.

## Pointers

`new` takes an expression and returns a pointer to it, with the type inferred (`new(0)` is `*int`). It replaces the `x := v; &x` dance, which needed a named variable purely to have an address.

```go
cfg := Config{
    Timeout: new(30),   // *int
    Debug:   new(true), // *bool
}
```

A redundant cast (`new(int(0))`) adds nothing the inference did not already do.

## Dependency Selection

The standard library goes first whenever it can reasonably do the job, because every dependency is a version to track, a release note to read, and a supply chain to trust.

These are always fine:

| Package | For | Project types |
|---|---|---|
| `spf13/cobra` | CLI framework | any with commands |
| `rs/zerolog` | logging | any with an entry point |
| `charm.land/bubbletea/v2`, `charm.land/lipgloss/v2`, `charm.land/bubbles/v2` | TUI | CLI Only, CLI + Web |
| `github.com/charmbracelet/x/term` | terminal detection, which decides log format and output styling | any with an entry point |
| `gorilla/websocket` | WebSocket | any |
| `goccy/go-yaml` | YAML, since `yaml.v2` is deprecated | any |

Web Only and Headless API Service projects have no terminal UI, so bubbletea, lipgloss, and bubbles do not appear in their `go.mod` at all. zerolog does, since every project type logs through it.

Anything else is acceptable when it fills a genuine need the standard library cannot reasonably cover: database drivers, cloud SDK clients, `golang.org/x/...`. Judge whether the dependency is justified rather than whether it appears on a list, because a fixed allow-list either blocks legitimate work or grows until it means nothing.

`google/uuid` is not one of them any more. The standard library's `uuid` package covers `New`, `NewV7` for a time-ordered identifier, `Parse`, and `MustParse`.

Prefer the well-maintained standard choice over the niche alternative (`zerolog` over `logrus`, `cobra` over `urfave/cli`), since the standard choice is the one whose breaking changes are documented and whose issues are already answered.

Dependencies stay at their latest stable version. Prefer stable over pre-release, and read the release notes before a major bump rather than after the build breaks. Auditing means scanning `go.mod` and any pinned asset versions in the Makefile, checking each against its current release, and bumping deliberately.
