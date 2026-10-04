---
name: Go
slug: go
version: 1.0.4
changelog: Display name shown correctly
description: 'Writes, debugs, and reviews Go: goroutine leaks, data races, nil interfaces, slices and maps, go.mod, and net/http. Use when Go panics or misbehaves — "all goroutines are asleep - deadlock!", "concurrent map writes", "send on closed channel", "assignment to entry in nil map", or a WARNING: DATA RACE from `go test -race`; when a goroutine, timer, or connection leaks and memory climbs; when a service hangs for want of a timeout; when errors.Is or errors.As stops matching after a %v wrap; when a slice mutates its parent, a map iterates in a new order, or a typed nil returned as error compares non-nil; when go.mod, go.sum, workspaces, replace, or a /v2 path fight over dependencies; when cross-compiling, cgo, build tags, go:embed, or a static container binary fail; when tests are flaky under -race or -parallel or benchmarks lie; when GOGC, GOMEMLIMIT, GOMAXPROCS, or escape analysis need tuning; or when writing handlers, CLIs, database access, or generics. Not for Kubernetes operators or framework internals.'
homepage: https://clawic.com/skills/go
metadata:
  clawdbot:
    emoji: 🐹
    requires:
      bins:
      - go
    os:
    - linux
    - darwin
    - win32
    displayName: Go
    configPaths:
    - ~/Clawic/data/go/
    - ~/go/
    - ~/clawic/go/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/go/
      - ~/go/
      - ~/clawic/go/
---

User preferences live in `~/Clawic/data/go/config.yaml` (see Configuration); nothing else is stored on the user's machine. If you have data at an old location (`~/go/` or `~/clawic/go/`), move it to `~/Clawic/data/go/`, and say in one line that you moved it and from where. Note that `~/go/` may also be the user's GOPATH — never write skill data there, and never delete it.

## When To Use

- Writing or reviewing Go — scan Core Rules and Output Gates before committing
- Any panic, `fatal error:`, or race warning whose cause is not obvious in ten seconds
- Hangs, goroutine growth, rising RSS, and CPU that appears without traffic
- Concurrency design: channels vs mutexes, worker pools, cancellation, fan-in/fan-out
- Toolchain and dependency work: modules, versions, build tags, cross-compilation, containers
- API and package design decisions: interfaces, generics, error contracts, layout
- Not for Kubernetes operators, gRPC service design, or web-framework internals — those live in their own skills

## Quick Reference

| Situation | Play |
|-----------|------|
| Goroutine count only goes up; process never releases memory | Every `go` needs an exit path: closed channel, `ctx.Done()`, or a bounded loop → `concurrency.md` |
| `WARNING: DATA RACE`, or "it only fails under load" | Read both stacks in the report; the fix is a mutex, a channel, or `atomic` — never a `time.Sleep` → `concurrency.md` |
| A call hangs forever, or shutdown never completes | Missing deadline or a `cancel()` that was never deferred → `context.md` |
| `errors.Is`/`errors.As` stopped matching after a refactor | Someone wrapped with `%v` instead of `%w`, or dropped `Unwrap()` → `errors.md` |
| A returned `error` is non-nil but holds nothing | Concrete nil pointer in an interface: nil only when type AND value are nil → `interfaces.md` |
| Deciding between a type parameter, an interface, and `any` | Interface first; type parameters when the body is identical for every type → `generics.md` |
| Append mutated data someone else was holding | `b := a[1:3]` shares the array; `cap(a[i:j]) == cap(a)-i` → `collections.md` |
| Byte/rune confusion, `len()` disagreeing with what you see, slow concatenation | `range` yields runes; `strings.Builder` for loops → `strings.md` |
| Struct copies, embedding, tags, map keys that panic, oversized structs | Comparability, promotion, and field alignment → `structs.md` |
| Timers, tickers, DST, parsing `2006-01-02`, elapsed time that goes negative | Monotonic clock for durations, wall clock for instants → `time.md` |
| JSON decodes but fields are zero, big integers lose digits, `omitempty` misfires | Exported fields + tags; numbers land as `float64` in `any` → `json.md` |
| Writing handlers or clients: timeouts, middleware, graceful shutdown, leaked bodies | Never `http.DefaultClient` in a service; drain and close every body → `http.md` |
| `database is locked`, connection pool exhaustion, NULLs, transactions that leak | `rows.Close()` on every path; size the pool against the DB limit → `database.md` |
| Reading/writing files and streams; `Close()` errors; partial writes | `io.Reader`/`io.Writer` composition; write temp then `os.Rename` → `io.md` |
| Building a CLI: flags, exit codes, signals, piping, stdin detection | `flag` for simple, exit through `main` so defers run → `cli.md` |
| Nothing appears in the logs; deciding what to log and at which level | `log/slog` handler and level; attributes, not formatted strings → `logging.md` |
| Writing tests, table tests, fakes, fuzzing, benchmarks, golden files | Subtests + `t.Parallel()`; `-race` on the suite → `testing.md` |
| A panic stack, a hung binary, or a flake you cannot reproduce | SIGQUIT stack dump, `-race`, `GODEBUG`, delve → `debugging.md` |
| "It is slow" — before optimizing anything | Benchmark, then `pprof`; fix the top line or nothing → `performance.md` |
| RSS grows, GC runs constantly, or a container gets OOM-killed | `GOGC`, `GOMEMLIMIT`, escape analysis, retained references → `memory.md` |
| `go.mod`/`go.sum` errors, version selection, `replace`, private repos, monorepos | MVS picks the minimum that satisfies everyone, not the latest → `modules.md` |
| Build tags, cross-compilation, `go:embed`, cgo, `-ldflags`, `go generate` | `CGO_ENABLED=0 GOOS=… GOARCH=… go build` → `build.md` |
| Shipping the binary: container image, GOMAXPROCS in a cgroup, health, rollout | Static binary + explicit resource ceilings → `deployment.md` |
| Untrusted input, secrets, tokens, TLS, templates, dependency CVEs | `crypto/rand`, `html/template`, `govulncheck` → `security.md` |
| Naming, package boundaries, receivers, exported API shape, linters | Package name is part of every identifier; no stutter → `idioms.md` |
| Choosing or upgrading a Go version; a feature that "should exist" but doesn't | Two releases are supported at a time; upgrade with `-race` and vet first → `versions.md` |
| Anything else | Core Rules below, then reduce to a `main.go` that reproduces it in under 30 lines and add one thing back at a time |

Each file above is one sub-job and is self-contained: read SKILL.md by default, open exactly one guide when the situation matches.

## Core Rules

1. **No goroutine without a written exit path.** A closed channel, a `ctx.Done()` case, or a loop with a bound — decided before the `go` keyword is typed. A handler that starts one un-cancellable goroutine per request at 1,000 rps leaks 3.6M goroutines an hour; at ~2 KB of initial stack each that is the whole heap (`concurrency.md`).
2. **Check the error at the call site; wrap with `%w` when you add context.** `fmt.Errorf("load config %s: %w", path, err)`. `%v` flattens the chain and silently breaks `errors.Is`/`errors.As` for every caller above you. Ignoring an error needs `_ =` plus a written reason (`errors.md`).
3. **An interface is nil only when its type word AND its value word are nil.** `var e *MyErr = nil; var err error = e` → `err != nil` is true and every `if err != nil` above fires. Declare the return as `error` and return the literal `nil`, never a typed nil (`interfaces.md`).
4. **`ctx context.Context` is the first parameter of every call that can block, and every `WithCancel`/`WithTimeout` is followed by `defer cancel()`.** Skipping `cancel()` leaks the timer and the child context until the parent finishes — `go vet`'s `lostcancel` catches the common shape (`context.md`).
5. **`defer` fires at function return, not at end of block.** `for ... { rows, _ := db.Query(...); defer rows.Close() }` holds every result set until the function returns and exhausts the pool. Move the body into its own function, or call `Close()` explicitly at the end of the iteration (`io.md`).
6. **Any variable touched by two goroutines needs a mutex, a channel, or `sync/atomic`.** "It is just an int" is the most common data race in Go. `go test -race` proves nothing about code paths it did not execute, so run it on the suite, not on one test (`debugging.md`).
7. **Reslicing shares the array; appending may or may not copy.** `b := a[1:3]`; `append(b, x)` overwrites `a[3]` whenever `len(b) < cap(b)`, and `cap(a[i:j]) == cap(a) - i`. Force a copy with the three-index form `a[1:3:3]`, which sets `cap` to `len` so the next append must reallocate (`collections.md`).
8. **Zero values are usable except for maps and channels.** `var s []int` appends fine and marshals as `null`; `var m map[string]int` reads fine and *panics* on write; `var ch chan int` blocks forever on both send and receive. `make` maps and channels; leave slices, `sync.Mutex`, `bytes.Buffer`, and `strings.Builder` at zero.
9. **Loop-variable capture is gated on the `go` line in go.mod, not on the toolchain.** With `go >=1.22` the variable is per-iteration, so `for _, v := range xs { go f(v) }` is correct; below that line every goroutine sees the last element, even when built with a new compiler. Check the `go` directive before trusting the pattern (`versions.md`).

## Version Floors

The floors that shape everyday Go. Individual guides carry more floors inline in this same `go >=X.Y` form, next to the instruction each one gates. Release policy, upgrade procedure, and removals: `versions.md`.

| Feature | Needs |
|---|---|
| `errors.Is`/`As`/`Unwrap` and `%w` wrapping | go >=1.13 |
| `go:embed`, `io/fs`, `os.ReadFile`/`WriteFile`, `go install pkg@version`, modules on by default | go >=1.16 |
| `//go:build` lines (replacing `// +build`), module graph pruning | go >=1.17 |
| Generics, `any`, native fuzzing, workspaces (`go work`) | go >=1.18 |
| `GOMEMLIMIT` soft memory limit, GC CPU limiter | go >=1.19 |
| `errors.Join`, `context.WithCancelCause`, coverage for binaries (`go build -cover`) | go >=1.20 |
| `slices`, `maps`, `cmp`, `log/slog`; `min`/`max`/`clear` builtins; `context.AfterFunc`/`WithoutCancel`; `toolchain` directive | go >=1.21 |
| Per-iteration loop variables, `for i := range 10`, `net/http` method+wildcard routing patterns, `math/rand/v2` | go >=1.22 |
| Range-over-function iterators (`iter.Seq`), `maps.Keys`/`Values` as iterators, unreferenced timers collectable without `Stop` | go >=1.23 |
| Generic type aliases, `os.Root` for directory-scoped file access, `testing.B.Loop`, `go tool` directive | go >=1.24 |
| Container-aware default `GOMAXPROCS` from the cgroup CPU limit, `testing/synctest` | go >=1.25 |

## Panics And Fatal Errors

`panic` unwinds and runs defers, so `recover()` can catch it. `fatal error:` does not: the runtime kills the process immediately and no defer, `recover`, or handler sees it. Knowing which one you got halves the search.

| Message | Cause | First move |
|---|---|---|
| `assignment to entry in nil map` | Map declared but never made | `m := map[K]V{}`; struct fields need it in the constructor |
| `send on closed channel` | A second sender, or the receiver closed | Only the sole sender closes; stop senders with a done channel (`concurrency.md`) |
| `close of closed channel` | Two owners closing | One owner, or `sync.Once` around the close |
| `fatal error: all goroutines are asleep - deadlock!` | *Every* goroutine is blocked — fires only in that total case, so partial deadlocks stay silent forever | Dump all stacks with SIGQUIT and find the blocked pair (`debugging.md`) |
| `fatal error: concurrent map writes` | Unsynchronized map access; not recoverable, and it is always a real bug | Mutex around the map, or `sync.Map` for its two documented shapes (`concurrency.md`) |
| `invalid memory address or nil pointer dereference` | Nil pointer, or a method promoted from an embedded nil pointer | Suspect the receiver, not only the arguments (`structs.md`) |
| `index out of range [5] with length 3` | Off-by-one, or a length read before a concurrent write | The message prints both numbers — compare them before reading code |
| `interface conversion: interface {} is string, not int` | Type assertion without comma-ok | `v, ok := x.(T)` (`interfaces.md`) |
| `comparing uncomparable type` | A struct containing a slice, map, or func used as a map key through an interface | Key on a derived comparable value (`structs.md`) |
| `sync: negative WaitGroup counter` | `Done()` called more often than `Add()`, or `Add()` moved inside the goroutine | `Add(1)` before the `go` statement, always |
| `WARNING: DATA RACE` | Two unsynchronized accesses, at least one a write | Read both stacks; the older one names the unprotected owner (`debugging.md`) |
| `missing go.sum entry` / `ambiguous import` | Dependency graph edited without tidying, or two modules provide the same path | `go mod tidy`, then `go mod why` on the loser (`modules.md`) |
| `declared and not used` / `imported and not used` | Compile error by design, not a lint | Delete it; `_ = x` belongs only in generated code |

## Output Gates

Before delivering Go code, check:

- Every `go` statement has a stated exit path, and every `WithCancel`/`WithTimeout` has `defer cancel()`
- Every error is checked; context added with `%w`; every discarded error has `_ =` and a written reason
- `ctx` is the first parameter of every exported call that blocks, and every network, database, lock, and subprocess call has a deadline
- No exported function returns a concrete error type as `error`; no typed nil escapes as an interface
- Every acquired resource closes on every path, including the error paths, and `Close()` errors on writers are checked
- `go vet` is clean and `go test -race ./...` ran at least once against the changed packages
- Syntax and stdlib stay within `min_go`, and the `go` directive in go.mod actually allows what you emitted
- Nothing untrusted reaches `text/template` for HTML, a concatenated SQL string, `os/exec` with a shell, or a path join without containment; no `math/rand` for anything secret

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/go/config.yaml`. Never interview the user — record a preference the moment it is stated.

| Variable | Type | Default | Effect |
|---|---|---|---|
| min_go | 1.21 \| 1.22 \| 1.23 \| 1.24 \| 1.25 | 1.22 | Gates which Version Floors features may be emitted unguarded, and which fallback appears instead (`versions.md`) |
| package_layout | flat \| cmd-internal | cmd-internal | Where new packages and files go, and whether `internal/` is used (`idioms.md`) |
| test_style | stdlib \| testify | stdlib | Assertion, fake, and mock style in emitted tests (`testing.md`) |
| http_stack | net/http \| chi \| gin \| echo | net/http | Router, middleware, and handler idiom in emitted server code (`http.md`) |
| logger | slog \| zap \| zerolog \| log | slog | Logging calls, handler setup, and how context is carried into log lines (`logging.md`) |
| error_wrapping | always \| boundaries \| never | always | How much `%w` context is added: every hop, only at package boundaries, or opaque errors only (`errors.md`) |
| cgo | enabled \| disabled | disabled | Whether builds assume `CGO_ENABLED=0` static binaries; gates cross-compile, Alpine, and DNS-resolver advice (`build.md`) |
| target_platform | linux/amd64 \| linux/arm64 \| darwin/arm64 \| windows/amd64 \| cross | linux/amd64 | Assumed GOOS/GOARCH in build, deploy, and file-path guidance; `cross` flags every platform-specific assumption |
| change_workflow | test-first \| fix-first | test-first | Order of the work: test-first writes the failing test before the fix, fix-first patches first and backfills the test against the reverted change (`testing.md`) |
| upgrade_cadence | continuous \| monthly \| quarterly \| security-only | monthly | How eagerly toolchain and dependency upgrades are proposed, and how big a batch: `continuous` takes each release as it lands, `quarterly` batches them, `security-only` moves for `govulncheck` findings and patch releases and nothing else. Also decides whether "one release behind latest" is reported as fine or as debt (`versions.md`, `modules.md`) |
| default_timeout | number (seconds, 1-300) | 10 | The budget emitted when the caller states none. `http.Client.Timeout` = this value; the server set scales off it — `ReadHeaderTimeout` ×0.5, `ReadTimeout` ×1.5, `WriteTimeout` ×3, `IdleTimeout` ×6 (10s → 5/15/30/60s); every per-call `context.WithTimeout` with no stated deadline uses it (`http.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling**: linter set (`go vet` only, golangci-lint standard or strict), mock generator, migration tool, task runner, `go work` vs one module per repo — affects every emitted config block and command (`idioms.md`)
- **Conventions**: receiver names and pointer-vs-value policy, error message phrasing, table-test naming, comment and doc style, struct-tag conventions — affects generated code and review comments
- **Platform**: deployment target (container, serverless, CLI distribution, embedded), CPU architecture, private module proxy, CI provider — affects `deployment.md` and `modules.md` guidance
- **Safety posture**: how aggressively to flag missing timeouts, unchecked errors, `panic` in library code, unbounded goroutines, and unpinned dependencies — affects `security.md` and review depth
- **Dependencies**: stdlib-only constraints, banned or mandated libraries (`pkg/errors` vs stdlib, `sqlx` vs `database/sql`, ORM policy), tolerance for new transitive dependencies — affects every recommendation
- **Output format**: whole file vs minimal diff, how much explanation, whether tests and benchmarks accompany every change — affects the shape of the answer, never the correctness rules
- **Work order**: which gates run before a change is proposed rather than after — `go vet` and `-race` green first, a benchmark before any optimization, a plan approved before restructuring packages — affects the sequence of every task, never the correctness rules
- **Cadence**: beyond `upgrade_cadence` — the day and batch size for `go get -u` runs, whether a new Go release is adopted in its first weeks or after `.1`, how often `govulncheck` and `go mod tidy` run in CI, and the review interval for pinned `replace` directives — affects `versions.md` and `modules.md`, never the correctness rules
- **Thresholds and sizing**: the numbers a team standardises beyond `default_timeout` — `SetMaxOpenConns`/`SetMaxIdleConns` against the database's own connection cap divided by instance count, `GOMEMLIMIT` headroom (default ~90% of the container limit), benchmark `-count` (default 10) and the `benchstat` delta that counts as a win, `http.MaxBytesReader` body cap (default 1 MiB), worker-pool width — affects which value gets emitted, while **Safety posture** governs whether a *missing* one is flagged

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `http.Get` or `http.DefaultClient` in a service | Its timeout is zero: one unresponsive server pins a goroutine and a connection until the process dies | Own client with an explicit `Timeout` and a tuned `Transport` (`http.md`) |
| `defer resp.Body.Close()` without draining | An unread body cannot be returned to the pool, so every call opens a fresh connection | `io.Copy(io.Discard, resp.Body)` before `Close()` (`http.md`) |
| `time.After` inside a `select` loop | Allocates a timer per iteration; on `go <1.23` each one also stayed alive until it fired | One `time.Timer` with `Reset`, or `context.WithTimeout` (`time.md`) |
| Passing `sync.WaitGroup`, `sync.Mutex`, or a struct containing one by value | The copy has its own counter or lock, so `Wait` returns early and mutual exclusion is gone | Pass the pointer; `go vet`'s `copylocks` catches it |
| `_ = json.Unmarshal(b, &v)` on lowercase struct fields | `encoding/json` only sees exported fields — no error, all zeros | Export the fields and tag them (`json.md`) |
| `panic` on an expected failure in a library | Turns the caller's recoverable case into a process kill they cannot handle | Return an error; reserve `panic` for programmer bugs (`errors.md`) |
| `math/rand` for tokens, IDs, or passwords | Predictable from a few outputs regardless of seeding | `crypto/rand` (`security.md`) |
| `os.Exit` or `log.Fatal` below `main` | Deferred cleanup, flushes, and traces never run | Return the error up to `main` and exit there (`cli.md`) |
| `init()` that reads files, dials, or reads env | Runs on import — in every test binary, in every tool that links the package, in an order you do not control | Explicit constructor called from `main` |
| `t.Setenv` in a test that also calls `t.Parallel()` | Panics by design: the environment is process-wide | Inject config, or keep that test serial (`testing.md`) |
| `interface{}`/`any` in a signature "to stay flexible" | Moves a compile error to a runtime assertion in someone else's code | A small interface, or a type parameter (`generics.md`) |
| Storing `context.Context` in a struct field | Freezes one request's deadline into a long-lived object; cancellation stops matching the caller | Pass it per call (`context.md`) |
| `time.Now().Sub(start)` after a value round-trip | Marshaling or `Round` strips the monotonic reading, so NTP steps can make elapsed time negative | `time.Since(start)` on an untouched `time.Time` (`time.md`) |
| Goroutine that only sends on an unbuffered channel nobody reads after an early return | Blocks forever and holds every variable it captured | Buffer of one, or `select` with `ctx.Done()` (`concurrency.md`) |

## Where Experts Disagree

- **Channels vs mutexes.** "Share memory by communicating" is the slogan; the Go team's own guidance is that a mutex around shared state is often simpler and faster. Boundary: channels when ownership of a value moves between goroutines or you need cancellation and fan-out; a `sync.Mutex` when several goroutines read and write one struct in place. A channel used purely as a lock is a slower lock (`concurrency.md`).
- **Project layout.** The `golang-standards/project-layout` tree (`pkg/`, `api/`, `build/`) is community folklore, not a Go team standard, and the standard library itself is flat. Boundary: a single binary starts flat and grows `internal/` when a package must not be imported outside; multi-binary repos earn `cmd/`. Ceremony before the second binary exists is cost without benefit (`idioms.md`).
- **How opaque errors should be.** One school wraps at every hop so callers can `errors.Is` anything; the other treats error identity as API surface and exports only a few sentinels, hiding the rest behind behavioral checks. Boundary: within one module, wrap freely; across a published API, every exported sentinel and error type is a compatibility promise you cannot retract (`errors.md`).
- **Generics vs interfaces.** Type parameters remove `any` from container and algorithm code, but Go compiles them with GC-shape stenciling: all pointer-shaped instantiations share one body plus a dictionary, so generic code over pointers can call indirectly where an interface would too. Boundary: identical logic across types that share no methods → type parameters; behavior that differs per type → interface (`generics.md`).

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/go (install if the user confirms):
- `concurrency` — language-agnostic memory model: happens-before, atomics, lock-free tradeoffs
- `debugging` — hypothesis-driven fault isolation; the Go-specific version of that job is this skill's `debugging.md`
- `profiling` — choosing the right clock and reading flame graphs, whatever the language
- `docker` — building and running the container the Go binary ships in
- `api-design` — the HTTP contract itself, above the handler code

## Feedback

- If useful, star it: https://clawic.com/skills/go
- Latest version: https://clawic.com/skills/go

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/go.
