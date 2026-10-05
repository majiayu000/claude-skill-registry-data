---
name: goroutine-leak-check
description: Use when adding/changing concurrent Go (goroutines, channels, worker fan-out, context cancellation) or when asked to find/verify/fix goroutine leaks — instruments tests with uber-go/goleak (and the Go 1.26 goroutineleak profile), runs the caged suite, diagnoses leaks against this repo's known patterns, and fixes the production code.
---

# Goroutine-leak verification & repair

UnPixel's hot path fans out across goroutines (offset discovery, intra-node DFS,
per-font sweeps, blind/mosaictext decoders) and streams a `Progress` channel. A leaked
goroutine — one blocked forever on a channel send/receive or a lock no runnable
goroutine can release — is a real correctness and memory bug. This skill verifies there
are none, and fixes any it finds.

State of the art (2026): **[uber-go/goleak](https://github.com/uber-go/goleak)** at test
boundaries (the portable default), and **Go 1.26's experimental `goroutineleak` pprof
profile** (GC-based, *no false positives* — it reports only goroutines it can prove are
stuck). This project is on Go 1.26, so both are available.

## Checklist (create a todo per item)

1. **Instrument the concurrent packages** with goleak at the test boundary.
2. **Run the caged suite** and collect every leak goleak reports.
3. **Diagnose** each leak against the known patterns below (real leak vs. test artifact).
4. **Fix the production code** (not the test) for real leaks; suppress only proven
   framework goroutines, narrowly and with a reason.
5. **Re-run caged** until clean; confirm the panel is 17/17.
6. Keep the gate: `mise run leak`. Because the per-package `TestMain` activates goleak on
   *every* `go test` run, `mise run test` and `mise run ci` (via `test:ci`) already
   detect leaks for free — `mise run leak` is the explicit, thorough caged run.

## 1. Instrument with goleak

Add the dependency (pure Go, no CGO — allowed):

```bash
go get go.uber.org/goleak
```

For each package that starts goroutines, add **one** `TestMain` so the check runs after
the whole package's tests (this is compatible with `t.Parallel`, unlike a per-test
`defer goleak.VerifyNone(t)`):

```go
package search

import (
	"testing"

	"go.uber.org/goleak"
)

func TestMain(m *testing.M) {
	goleak.VerifyTestMain(m)
}
```

Packages to instrument (those with `go func` / `WaitGroup` / fan-out): the root
`unpixel`, `internal/search`, `blind`, `mosaictext`, `internal/blinddecode`,
`internal/fontrank`, and `cmd/unpixel`. (Re-derive the list with
`grep -rln 'go func\|sync.WaitGroup\|errgroup' --include='*.go' . | grep -v _test.go`.)

If a package already has a `TestMain`, fold the goleak verification in around the
existing `m.Run()` and propagate its exit code; do not add a second one.

Per-test, sequential checks can use `defer goleak.VerifyNone(t)` — but **never** with
`t.Parallel`.

### Go 1.26 profile (deeper, no false positives)

For a hard-to-pin leak, capture the GC-backed profile (proves stuck goroutines):

```go
import "runtime/pprof"
pprof.Lookup("goroutineleak").WriteTo(os.Stderr, 1) // Go 1.26+, experimental
```

Use it to confirm a goleak finding is genuinely blocked (and on what) before fixing.

## 2. Run (ALWAYS caged)

NEVER run `go test` bare on this machine — it OOM-freezes Fedora. Always:

```bash
mise run leak                                   # the dedicated gate (caged, CGO-free)
scripts/gotest-caged.sh go test ./internal/search   # a single package
```

goleak needs no special flags — it runs via `TestMain`, so a plain caged `go test`
detects leaks. A leak prints as `found unexpected goroutines` with each one's stack — the
bottom frame is the `go func` that leaked; the top frame is where it is blocked.

> **No `-race` in the gate.** The race detector requires `CGO_ENABLED=1`, and this project
> is **pure Go, no CGO** (an absolute rule — see `CLAUDE.md`). goleak detects *leaks*
> without `-race`. Use `-race` only as a manual, local-only deep check for *data races*
> (a different class of bug): `CGO_ENABLED=1 scripts/gotest-caged.sh go test -race ./...`
> — never wire it into a committed task or the CI gates.

## 3. Known leak patterns in this repo

- **Unconsumed `Progress` / results channel.** `(*Engine).Run` returns
  `(<-chan Progress, <-chan Result)`. High-frequency events are drop-on-full
  (`select … default`), but `EventNewBest`/`EventDone` and the result send must not
  block forever. A producer that does a *blocking* send on a channel the caller stopped
  reading leaks. Fixes: make the terminal send `select` on `ctx.Done()`; buffer the
  results channel by 1; or document+guarantee the producer always returns when ctx is
  cancelled. Tests must drain to completion or cancel ctx.
- **Worker fan-out without join.** Each fan-out (search offsets, font sweep, blinddecode
  Cartesian, mosaictext sweeps) must `wg.Wait()` (or errgroup `Wait()`) on **every**
  return path, including early error/`ctx` cancellation. A worker blocked on a full
  results channel after the collector returned is a leak — give the results channel
  enough buffer, or have workers `select` on `ctx.Done()`.
- **Context not honored.** A goroutine looping on work must check `ctx.Done()`; a
  `time.After`/`ticker` must be stopped. Store no `context.Context` in a struct.
- **Test-only background goroutines.** A goroutine the *test* starts (e.g. draining
  progress) must finish before the test returns, or goleak attributes it to the package.

## 4. Fixing

Fix the **production** goroutine's lifecycle, not the test. The correct shapes:

- Owner holds the goroutine and exposes `Close`/`Stop`, or the goroutine is bounded by a
  `WaitGroup` the spawning function waits on before returning.
- Every channel a goroutine sends on is either buffered enough that the send can't block
  after consumers stop, or the send is `select { case ch<-v: case <-ctx.Done(): }`.
- Cancellation (`ctx`) unblocks every goroutine; the function that created the `ctx`
  (or derived a `cancel`) calls `cancel` on all paths (`defer cancel()`).

Suppress only a *proven* framework goroutine, narrowly:

```go
goleak.VerifyTestMain(m, goleak.IgnoreTopFunction("<pkg>.<func>")) // reason: …
```

## Done when

`mise run leak` is clean (CGO-free, caged), the recovery panel is still 17/17, and every
real leak was fixed in production code (suppressions, if any, name a proven-external
goroutine and a reason).
