---
name: go-architect
version: 1.7.1
description: Go 1.26 architectural standards — memory-aligned structs, typed enums, interface design, goroutine safety, iterators, idiomatic errors, sqlx + //go:embed SQL pattern, go.work multi-module layout. Use when writing, reviewing, or scaffolding Go code.
---

# Go Architecture & Domain Modeling

Targets **Go 1.26**. See [STACK.md](STACK.md) for pinned dependency versions.

## 1. Constants & Enums

- **Enums:** Custom types with `iota` and an implemented `String()` method. Avoid bare primitives. Use `1 << iota` for bitmasks.
- **Errors:** Export package-level sentinel errors (`var ErrNotFound = ...`) for `errors.Is()`. Use `errors.Join` to aggregate multiple errors.
- **Grouping:** When a file declares multiple `type`, `const`, or `var` at package level, consolidate each kind into a single parenthesized block (`type (...)`, `const (...)`, `var (...)`) rather than repeating the keyword. Keep unrelated groups separated by a blank line inside the block.
- **File-level ordering:** type → const → var → func (decorder's default order). Enforced via code review; linter checking disabled to avoid friction with tooling defaults.
- **Magic values:** a bare numeric or string literal used more than once becomes a named constant. Enforced by `mnd` (numbers) and `goconst` (strings) (see §14).

## 2. Structures & Memory

- **Design:** Explicit struct tags, standard audit fields, composition via embedding. Keep tag casing (`json`, `yaml`) consistent across the codebase — `tagliatelle` catches drift, opt-in and scoped since legacy tags often can't be renamed without a breaking change (see §14).
- **Optimization:** Order fields largest → smallest to minimize padding.
- **Semantics:** Pointers for mutation or mutex-protected state; values for small, immutable payloads.
- **Validation:** `Validate() error` for structs taking external input; tag-based validation via `go-playground/validator`.
- **Ordering:** Use `cmp` (`cmp.Compare[T]`, `cmp.Or`, `cmp.Less`) as the default ordering toolkit.
- **Typed models over maps:** Prefer a defined struct to `map[string]any`/`map[string]interface{}` for shaped data — the compiler catches typos and missing fields a map silently swallows. `forbidigo` flags the anti-pattern (see §14); `exhaustruct` (opt-in, scoped to specific structs) catches incomplete struct literals once you've made the switch.

## 3. Instantiation

- **Constructors:** Always provide `New...` to initialize maps, slices, channels safely.
- **Configuration:** Functional Options pattern for complex setup; never large config structs passed by value.

## 4. Interfaces

- **Design:** Define interfaces where they're *used*, not where implemented. Keep them small (1–3 methods) — enforced by `interfacebloat` (see §14).
- **Signatures:** Accept interfaces (for easy mocking); return concrete structs — enforced by `ireturn` (see §14).

## 5. Stdlib defaults

Prefer stdlib over hand-rolled or third-party when stdlib now covers it.

- `slices`, `maps` — collection helpers (`Sort`, `Contains`, `Index`, `Clone`, `Equal`, `Concat`, etc.)
- `cmp` — `Compare`, `Less`, `Or`, `Ordered` — the default ordering toolkit.
- `iter` — `iter.Seq[T]`, `iter.Seq2[K,V]` for sequence-shaped returns (see §6).
- `log/slog` — structured logging; **default for new code**. Reach for `zap`/`zerolog` only when slog's allocator perf is provably insufficient.
- `errors` — `errors.Is`, `errors.As`, `errors.Join`.
- `net.JoinHostPort` / `net.SplitHostPort` — idiomatic host:port assembly (enforced by `nosprintfhostport` linter). Never `fmt.Sprintf("%s:%d", host, port)`.

## 6. Iterators (Go 1.23+)

- **Range-over-func:** `for x := range seq { ... }` where `seq` is `iter.Seq[T]`.
- **Return `iter.Seq[T]` when:** the sequence is large/unknown-size, consumer might short-circuit, or it's backed by an underlying cursor (DB pagination, HTTP pages).
- **Return `[]T` when:** the result is small, bounded, and the caller almost always wants the whole thing.
- **Anti-pattern:** wrapping a `[]T` in `slices.Values` just to look modern. Round-tripping back to `slices.Collect` is wasted ceremony.

## 7. Concurrency

- **State:** Embed `sync.RWMutex` directly above the fields it protects. `sync/atomic` for simple counters.
- **Context fields:** Never embed `context.Context` in structs (`containedctx` linter enforces this). Pass it as a parameter; contexts are designed as function arguments, not persistent state.
- **Duration:** Use `time.Duration` primitives; never multiply durations (`durationcheck` catches `time.Second * 60` — use `time.Minute` instead).
- **Context nesting:** Avoid nested contexts in loops or closures (`fatcontext` catches this anti-pattern).
- **WaitGroup:** Use `sync.WaitGroup.Go(fn)` (Go 1.25+) — replaces `Add(1) / go func() { defer Done(); ... }()` boilerplate.
- **Context:** Pass `context.Context` as the first parameter for any blocking or I/O. Use `signal.NotifyContext` for shutdown; the cancellation cause now records which signal fired (Go 1.26).
- **Containers:** `GOMAXPROCS` respects cgroup CPU limits since Go 1.25 — don't hardcode in containerized deploys.

## 8. Errors & Panics

- **Checking:** `errors.As` for custom types; `errors.Is` for sentinels. Never force type assertions on error results — use `ok` check or `errors.As` (`forcetypeassert` enforces this).
- **Aggregation:** `errors.Join(errs...)` when collecting multiple errors (validation, parallel fan-out).
- **Wrapping:** `fmt.Errorf("op: %w", err)` to add context while preserving the chain. When wrapping external package errors, use `wrapcheck` to verify proper context addition (prevents "swallowing" errors).
- **Panics:** Restrict to initialization (`MustCompile` style). Never as control flow.

## 9. Testing

- **Patterns:** Table-driven tests and black-box testing (`package mypkg_test`). Parallelize tests with `t.Parallel()` — checked and enforced by `paralleltest` and `tparallel` linters. Avoid deprecated testing APIs (`ioutil.TempDir` → `t.TempDir()`); `usetesting` enforces modern stdlib testing functions.
- **Helpers:** `t.Helper()` as the first line in any custom assertion — enforced by `thelper`.
- **Concurrent code:** Use `testing/synctest` (GA in Go 1.25) — virtualizes time, waits for goroutines to quiesce, makes async tests deterministic.
- **Library:** `stretchr/testify` for assertions/mocks/suites when stdlib alone is awkward. Use `testifylint` to catch incorrect assertion patterns (`assert` vs `require`).
- **Integration tests against Docker dependencies:** `testcontainers-go` — spins up real Postgres/Redis/Kafka/etc. containers per test run instead of mocking the driver or relying on a shared dev instance. Gate behind a build tag (e.g. `//go:build integration`) or `testing.Short()` check so `go test ./...` stays fast by default.

## 10. Packages

- **Naming:** Short, lowercase, single-word. Never `util`, `common`, `helpers`.
- **Layout:** Organize by domain/feature, not by technical layer.
- **Domain modeling & interface placement:** See [hexagonal-arch](../../design/hexagonal-arch/SKILL.md) for ports/adapters and [ddd-architect](../../design/ddd-architect/SKILL.md) for aggregates/bounded contexts. For `go.work` multi-module layout, see §16.

## 11. Dependencies & Logging

- **Injection:** Pass dependencies via constructors. No global state, no package `init()` setups. For larger graphs use `uber-go/fx` or `google/wire`.
- **Config:** `spf13/viper` for layered env + file + flag configuration.
- **Logging:** `log/slog` (stdlib). Structured, context-aware. `zap`/`zerolog` only when slog is provably the bottleneck — start with slog.

## 12. Database access — sqlc (default), sqlx + `//go:embed` (alternative)

**Default: `sqlc`.** Schema-first, code-generated queries — write named queries in `.sql` files against your real migrated schema, run `sqlc generate`, get back typed Go row structs and query methods, checked at generate-time against the actual database. No ORM magic, no hand-written scanning code, queries stay plain auditable SQL in git.

```sql
-- query.sql
-- name: GetUserByID :one
SELECT * FROM users WHERE id = $1;
```

```yaml
# sqlc.yaml
version: "2"
sql:
  - engine: "postgresql"
    queries: "query.sql"
    schema: "migrations"
    gen:
      go:
        package: "db"
        out: "db"
```

```go
func (r *UserRepo) GetByID(ctx context.Context, id int64) (db.User, error) {
    return r.queries.GetUserByID(ctx, id)
}
```

Layout:

```
internal/userrepo/
├── repo.go
├── sqlc.yaml
├── query.sql
└── db/              # generated: models.go, query.sql.go, db.go — never hand-edit
```

- **Migrations:** `goose` or `golang-migrate` — versioned up/down pairs in `migrations/`. `sqlc`'s `schema:` reads the same migration files, so schema drift between the two is impossible by construction.
- **Regeneration:** run `sqlc generate` in CI (or a pre-commit hook) and fail the build if the generated tree differs from what's committed — generated code is committed, not built on the fly.

**Alternative: `jmoiron/sqlx` + `//go:embed`.** Reach for this when a query needs genuine runtime composition sqlc's static named-query model can't express (e.g. an arbitrary number of optional filter clauses), or when a package deliberately avoids a codegen step. Write raw SQL in `.sql` files, embed at compile time, execute via `sqlx`'s struct-tag scanning:

```go
//go:embed queries/get_user_by_id.sql
var getUserByIDSQL string

func (r *UserRepo) GetByID(ctx context.Context, id int64) (User, error) {
    var u User
    err := r.db.GetContext(ctx, &u, getUserByIDSQL, id)
    return u, err
}
```

Layout:

```
internal/userrepo/
├── repo.go
└── queries/
    ├── get_user_by_id.sql
    ├── insert_user.sql
    └── list_users.sql
```

- **Dynamic queries:** even here, write the static fragments in `.sql` files and join them in Go rather than building SQL by string concatenation against user input — always use parameter binding.
- Don't mix the two within one repository package — pick per-package, not per-query, so a reader knows which scanning convention to expect from the file layout alone.

## 13. Generics

- **Usage:** Data structures and utility functions only. If an interface would serve, prefer it.
- **Self-referential constraints (Go 1.26):** `type Adder[A Adder[A]] interface { Add(A) A }` is valid — useful for fluent-style domain types.
- **Type aliases with type params (Go 1.24):** `type IntMap[V any] = map[int]V`.

## 14. Tooling

- **Lint:** `golangci-lint` **v2** — a single binary that aggregates `staticcheck`, `govet`, `gofmt`, `goimports`, `revive`, and dozens more. Pin via `.golangci.yml` (v2 config schema). Run on every commit and in CI. Treat warnings as errors. Drop-in template: [`assets/golangci.yml`](assets/golangci.yml) — copy to your project root as `.golangci.yml` and set `goimports.local-prefixes` to your module path.
  - **Essential linters:** `govet`, `staticcheck`, `unused`, `gocritic`, `revive`, `errorlint`, `gosec`, `misspell`, `sloglint`, `godoclint`.
  - **Code quality:** `nolintlint` validates that `//nolint` directives are specific and actually suppress something — enforces intentional, clean ignores. `varnamelen` enforces minimum variable name length (catches `x`, `i` outside loops; configure `max-distance: 5, min-name-length: 1`). `errname` ensures error types follow convention (`ErrFoo`, `FooError`) — complements §1's sentinel error pattern. `stylecheck` enforces naming conventions across the codebase (e.g., exported/unexported consistency).
  - **Idiomatic patterns:** `prealloc` detects slices that could pre-allocate capacity — idiomatic Go performance practice. `reassign` flags package variable reassignment in favor of const/new-var idiom. `makezero` catches unintended zero-length slice declarations. `predeclared` prevents shadowing Go builtins. `looppointer` detects address-of-loop-variable bugs (memory safety). `recvcheck` ensures method receiver types are consistent within an interface. `dogsled` flags excessive blank identifiers (e.g., `_, _, _, v := ...` suggests destructuring instead). `mirror` catches bytes/strings type mismatches (e.g., comparing `[]byte` to `string` idiomatically). `exptostd` replaces `golang.org/x/exp` packages with stdlib equivalents — use stdlib for idiomatic Go. `modernize` suggests modern Go simplifications (range-over-int, slices API, etc.).
  - **Duplication & magic values:** `dupl` (structural clones), `goconst` (repeated string literals), `mnd` (magic numbers) — all push toward named constants/enums (see §1).
  - **Complexity & size:** `nestif`, `gocognit` (cognitive complexity), `maintidx` (maintainability index), plus revive's `file-length-limit` and `argument-limit` rules — catch functions/files that should be split before they rot.
  - **Declaration structure:** `decorder` enforces file-level `type → const → var → func` ordering (decorder's default). Set `disable-dec-order-check: false` in your `.golangci.yml` to enable (see §1). `gochecknoinits` flags `init()` outright (see §11).
  - **Interfaces & enums:** `interfacebloat` caps interface method count, `ireturn` enforces concrete returns (see §4); `exhaustive` forces enum-typed `switch` statements to cover every value; `forbidigo` bans `map[string]interface{}`/`map[string]any` in favor of typed structs (see §2) — requires careful regex tuning for your codebase (consider enforcing struct typing via code review if regex patterns get unwieldy; template includes reference patterns in `assets/forbidigo-patterns.yml`).
  - **modernize** (standalone linter, golangci-lint v1.57+): all checks on by default — catches `range n` (Go 1.22+), `slices.Sort`, `slices.Contains`, `maps.Keys`, `maps.Values`, etc. If too noisy, constrain via `modernize.settings` (e.g., `forRangeInts: true` only).
  - **intrange** (standalone linter): explicitly enabled — flags `for i := 0; i < n; i++` where `range n` is cleaner. Lightweight alternative to the `modernize` coverage.
  - **copyloopvar** / **perfsprint**: modernization nudges — `copyloopvar` flags now-redundant `x := x` loop-variable copies (Go 1.22+ semantics), `perfsprint` suggests faster alternatives to `fmt.Sprintf`/`fmt.Errorf` (e.g. `strconv`, `err.Error()`). Both low-noise, safe to enable by default.
  - **Optional: Scoped Linters** (enable when appropriate for your project):
    - `exhaustruct`: Flags incomplete struct literals; scoped to config/DTO structs to manage noise. Enable once you've migrated to fully-typed structs (see §2).
    - `tagliatelle`: Enforces struct-tag casing consistency (`json`/`yaml` naming). Scope to new code since legacy tags often can't be renamed without breaking changes; useful when refactoring APIs (see §2).
    - `depguard`: Controls allowed imports (e.g., no test frameworks in prod code). Requires careful allowlist configuration per project structure — enable after establishing import boundaries.
  - **Testing linters:**
    - `paralleltest`: Detects tests missing `t.Parallel()` — encourages test suite parallelization for faster feedback.
    - `tparallel`: Catches inappropriate `t.Parallel()` usage in subtests, preventing race conditions and serialization bugs.
    - `thelper`: Ensures test helper functions call `t.Helper()` — prevents test output pollution and clarifies stack traces.
    - `testifylint`: Best practices for testify assertions — flags incorrect `assert` vs `require` usage and other testify pitfalls (see §9).
    - `usetesting`: Replaces deprecated testing helpers (e.g., `ioutil.TempDir` → `t.TempDir()`) with modern stdlib equivalents.
  - **Correctness & safety patterns:**
    - `containedctx`: Detects `context.Context` embedded in structs — pass as parameter instead (see §7).
    - `durationcheck`: Prevents duration multiplication bugs (e.g., `time.Second * 60` vs `time.Minute`).
    - `forcetypeassert`: Flags forced type assertions without `ok` check — use `errors.As` or check the boolean (see §8).
    - `fatcontext`: Detects nested contexts in loops/closures — anti-pattern that escapes context cancellation.
    - `mirror`: Catches bytes/strings type mismatches; encourages idiomatic type usage.
    - `exptostd`: Flags `golang.org/x/exp` packages — use stdlib equivalents instead (core idiom).
    - `wrapcheck`: Ensures external package errors are wrapped with context; prevents "swallowing" errors (see §8).
    - `unparam`: Reports unused function parameters — aids cleanup (can be noisy during refactoring).
    - `funcorder`: Enforces consistent function/method/constructor ordering within types.
    - `modernize`: Suggests modern Go simplifications (range-over-int, slices API, maps functions, etc.) — complement to `copyloopvar` + `perfsprint`.
  - **Template:** The [`assets/golangci.yml`](assets/golangci.yml) template includes sane defaults for all recommended linters with tested configuration values for `linters.settings`. Copy it to `.golangci.yml` and customize thresholds (e.g., `gocognit.max` for cognitive complexity) to match your project's complexity profile.
- **Dead code (`deadcode`, opt-in, not golangci-lint):** `unused` only flags unused *unexported* symbols, so an exported function no `main` reaches passes the lint gate forever. Run `deadcode -test ./...` (`golang.org/x/tools/cmd/deadcode`) so tests count as roots — without `-test` every test helper looks dead. It does not follow dynamic dispatch (cobra `RunE`, handler funcs stored in maps), so confirm each hit before deleting. Re-run after a deletion pass: removing one function can be the last use of another. Wire it into its own task target rather than the lint gate, since it needs a `main` to root from.

- **Doc-comment coverage (opt-in):** the main config disables revive's `exported`/`package-comments` rules — doc coverage isn't part of the standard gate (see §15). Run it on demand with the secondary config [`assets/golangci.doccheck.yml`](assets/golangci.doccheck.yml): `golangci-lint run -c golangci.doccheck.yml ./...`.
- **Repo-level style guards (opt-in, not golangci-lint):** two conventions golangci-lint has no linter for — no one-line function bodies, no decorative separator comments (`// ──`, `# ═══`). Ship as shell scripts, not lint rules, since existing codebases likely have violations needing a separate cleanup pass first: [`assets/check-no-oneline-functions.sh`](assets/check-no-oneline-functions.sh), [`assets/check-no-separator-comments.sh`](assets/check-no-separator-comments.sh). Wire each into its own task-runner target (see `repo-tooling-architect` §4 for Task/just setup) rather than the main lint gate, so a legacy-codebase failure doesn't block unrelated CI.
- **Modernization:** Run `go fix` periodically (revamped in Go 1.26 as push-button modernizers). It rewrites legacy patterns toward current stdlib APIs and respects `//go:fix inline` directives for local refactors. Ongoing hygiene, not a one-off.
- **Format:** `gofmt` (built-in) plus `goimports` (via `golangci-lint`) — no other formatter, no debate.
- **Build/run:** `go build`, `go test`, `go vet`, `go work` for multi-module repos. Stdlib only — avoid Make/Task wrappers unless multi-language CI demands it.

## 15. Documentation

- **Format:** Exported names get full-sentence comments starting with the identifier name. Include a package-level comment.
- **Style:** Weave parameter and return names into prose (no `@param`). Document specific error conditions.
- **Focus:** Explain *why* (business rules, edge cases) — code already shows *what*.

## 16. Multi-module workspaces (`go.work`)

For repos where `go.work` ties together independently-versioned modules — one per bounded context, plus shared libraries — rather than a single `go.mod`.

- **Module boundary is the real privacy/reuse unit.** Once something is its own module (own `go.mod`), nesting it under a directory named `internal/` adds nothing — Go's `internal/` import restriction is a single-module-tree mechanism and does nothing extra for something already module-isolated. Treat the directory name as organizational labeling, not enforcement. If a service module needs a genuine internal-only boundary, nest a further `internal/` inside that module (`internal/order/internal/wire/`).
- **`pkg/*`** — each subdirectory its own module, for code genuinely shared by 2+ service modules (validation, observability, an RFC 9457 problem-detail mapper). Don't default to creating `pkg/`; per [hexagonal-arch §7](../../design/hexagonal-arch/SKILL.md#7-when-not-to-use-it), a shared seam is only real once two consumers need it.
- **Root-level `domain`** — only for value objects/types genuinely shared *across* bounded contexts (e.g. a `Money` type used by both Order and Payment). Most contexts should keep their domain private inside their own service module. A shared root `domain` module is a deliberate Shared Kernel (see [ddd-architect's context-mapping table](../../design/ddd-architect/PATTERNS.md#1-context-mapping-patterns)), not a default.
- **`internal/<service>`** — one bounded context = one module. Internally structured per [hexagonal-arch](../../design/hexagonal-arch/SKILL.md): `domain/`, `app/`, `adapters/{primary,secondary}` — or flatter, since hexagonal-arch mandates the dependency direction, not the folder split. "Service" here means the deployable module itself, not [ddd-architect's Domain/Application Service patterns](../../design/ddd-architect/SKILL.md#7-domain-vs-application-services) — a single `internal/<service>` module typically contains several Application Services inside its `app/` layer (e.g. `PlaceOrderService`).
- **`cmd/<service>` vs `app/<service>`** — keep distinct rather than merging composition into `cmd`. `cmd/<service>/main.go` stays minimal: parse flags/env, wire `signal.NotifyContext`, call into `app`, handle the exit code. `app/<service>` is the actual composition root — DI graph, adapter wiring, server lifecycle — so it's exercisable independently of process-level concerns.
- **Cross-context calls never reach into another context's `domain/` or `adapters/`.** They go through that context's public API (HTTP/gRPC, since each service is a separate deployable in a multi-module workspace). The calling context defines its *own* ports shaped for what it needs (`OrderCreator`, not `order.Repository`) — the same "define interfaces where used" rule from §4, applied across a context boundary. This is the Go-flavored version of [ddd-architect's Customer/Supplier or Open Host Service patterns](../../design/ddd-architect/PATTERNS.md#1-context-mapping-patterns).
- **Full worked example** — an order-owning service plus a checkout orchestrator service, with code — lives in [RECIPES.md](RECIPES.md).

## Canonical libraries

See [STACK.md](STACK.md) for the full pinned list — viper, validator, cobra/pflag, gin, sqlx, grpc, protobuf-go, testify, fx, golang-migrate, buf.
