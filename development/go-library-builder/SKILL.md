---
name: go-library-builder
version: 1.1.0
description: Scaffolds reusable Go 1.26 library modules in the ralvarezdev house style — flat, vertical-slice, toolkit or framework-adapter shapes; domain-pure root package, ports as narrow interfaces, technology-named adapter subpackages (prod/dev/test), config structs over options, testcontainers over mocks, mise + Task + golangci tooling. Module namespace is a parameter (default github.com/ralvarezdev). Use when bootstrapping a new Go library, adding an adapter, or auditing one against the house style.
---

# Go Library Builder

Scaffolds a new **reusable Go library module** in the ralvarezdev house style, distilled from the `identity`, `ratelimit`, and `email` libraries, and extended for the toolkit and framework-adapter modules (`restkit`, `pgkit`, `ginkit`). **Check [go-house-libs](../go-house-libs/SKILL.md) first:** if a module already covers the need, use it; scaffold a new one only when none fits and a second consumer exists. This skill is the *composition root* for three others — it does not restate them:

- **[go-architect](../../languages/go-architect/SKILL.md)** — every Go idiom (memory alignment, errors, iterators, linters, `//go:embed` SQL). This skill assumes it.
- **[hexagonal-arch](../../design/hexagonal-arch/SKILL.md)** — ports & adapters, dependency direction. This skill applies it *at library scale*.
- **[ddd-architect](../../design/ddd-architect/SKILL.md)** — entities, value objects, bounded contexts. This skill uses it for domain shape.

Also leans on [repo-tooling-architect](../../tooling/repo-tooling-architect/SKILL.md) (mise/Task/editorconfig/renovate) and [sql-architect](../../databases/sql-architect/SKILL.md) (persistence adapters). File skeletons and full tooling templates live in [RECIPES.md](RECIPES.md) and [assets/](assets). Pinned versions in [STACK.md](STACK.md).

## 1. What it produces

A standalone Go module publishable as `<namespace>/<name>` where **hexagonal layers map onto Go package boundaries**, not layer-named folders. There is never a `domain/`, `application/`, `ports/`, or `adapters/` directory — the package *is* the layer.

**`<namespace>` is a parameter** — ask for it at bootstrap (§13.1); default `github.com/ralvarezdev`. It sets the module prefix, every intra-repo import path, `goimports -local`, and `sqlc` type-override package paths. Nothing else in the house style changes with it.

Four shapes, same rules (§9 decides between the first two; the last two are for libraries with no domain):

- **Flat single-port library** (`ratelimit`, `email`) — root package = domain + one port; one subpackage per adapter.
- **Vertical-slice library** (`identity`) — one package per bounded context, each internally hexagonal, plus an `app/` application layer and `internal/acl/` seams.
- **Toolkit library** (`restkit`, `pgkit`, `termkit`, `mcpkit`) — helpers with no domain port. The root holds the framework-free core, and each heavy dependency lives in exactly one subpackage (`pgkit/migrate` owns goose, `pgkit/pgtest` owns testcontainers), so a consumer that skips a subpackage never compiles its dependency.
- **Framework-adapter module** (`ginkit` over `restkit`, `identitygin` over `identity`) — its own module wrapping one framework around a framework-free core, so the core never imports the framework. Named for what it adapts (`<core>gin`, `<framework>kit`); depends on the core, never the reverse.

## 2. Module & naming convention

- **Module path:** `<namespace>/<name>` (default namespace `github.com/ralvarezdev`) — `<name>` is the domain noun only. No `go-` prefix, no methodology prefix (`ddd-`, `hex-`).
- **Packages:** short, lowercase, single word. Root/slice package = the domain concept (`email`, `user`, `auth`). Adapter package = the **technology** (`smtp`, `valkey`, `postgres`, `jwt`), never the pattern (`repository`, `infra`).
- **The adapter file is named for the port it implements**, identical across adapters (`mailer.go`, `limiter.go`, `store.go`). The package disambiguates, so the type is `smtp.Mailer`, not `SmtpMailer` — kill the stutter.
- **Concrete type** = `Mailer` / `Store` / `Service` / `Issuer`; **constructor** = `New` (or `NewMailer` when the package holds several). Docs dated `docs/YYYY-MM-DD-<topic>.md`.

## 3. Domain purity — the load-bearing invariant

The root/domain package imports **stdlib + `google/uuid` only**. Zero third-party. This is the invariant everything else protects: only adapters may import a driver, an HTTP client, or a crypto library. A toolkit's root core (`restkit`) is held to the same stdlib-only rule, and a heavy dependency in a toolkit sits in its own subpackage. Static check: grep the domain package's imports — a single third-party line is a bug. See [hexagonal-arch §2](../../design/hexagonal-arch/SKILL.md#2-dependency-direction--always-inward).

## 4. Ports — narrow, composed, domain-owned

Interfaces are declared **by the domain, where consumed**, per [go-architect §4](../../languages/go-architect/SKILL.md#4-interfaces). House specifics:

- **Cap at ~3 methods** (`interfacebloat`). Grow by **composition, not method count**: `UserStore = UserRecordReader + UserRecordWriter + UserRecordQuery`. Callers depend on the narrowest sub-interface they use.
- **`context.Context` first, plain domain data across the seam.** No driver types in a port signature — that's a leaky port ([hexagonal-arch §6](../../design/hexagonal-arch/SKILL.md#6-common-mistakes)).
- **Name for role, not tech:** `TokenIssuer`, `AttemptLimiter`, `UserLookup`. Suffix `…Port` only when `…er`/`…Store` would collide.
- **One instance may satisfy many ports** — a single `*postgres.Store` can implement eight interfaces; wiring passes the same pointer.

## 5. Constructors & configuration

- **Accept interfaces, return concrete `*T`** (`ireturn`). Callers hold interfaces; wiring holds structs.
- **Constructor injection only.** No globals, no `init()` (`gochecknoglobals` + `gochecknoinits`). Dependencies are constructor parameters.
- **Config is a plain validated struct, not functional options.** The house style deliberately rejects `Option func(*T)`. Fill zero values with a `setDefaults()` method over `Default*` constants; validate in `New` via `Config.Validate() error`. Rationale + the one exception in [RECIPES §2](RECIPES.md#2-config--constructors).
- **The library never reads env, files, or viper.** The consuming app owns all config and passes secrets/DSNs/TTLs as plain values (`jwt.New(secret, accessTTL, refreshTTL)`).

## 6. Errors

Follows [go-architect §8](../../languages/go-architect/SKILL.md#8-errors--panics) with three house rules:

- **Sentinels are package-prefixed:** `var ErrNotFound = errors.New("user: not found")`. Parametrized cases get a constructor func (`ErrPasswordTooShort(min int) error`). `errname` enforces the `Err…` form.
- **Validation aggregates with `errors.Join`**; every returned error is wrapped `fmt.Errorf("<pkg>: <op>: %w", err)` — a breadcrumb chain the caller reads with `errors.Is`/`errors.As`.
- **Adapters translate infra errors to domain sentinels at the boundary** (`pgx.ErrNoRows → user.ErrNotFound`, unique-violation → `ErrEmailTaken`). A driver error must never escape an adapter. A typed error (`SendError{Permanent bool}`) may live *in* an adapter when the caller needs to branch (retry classification), but the domain only knows sentinels.
- **Business "no" is not an error.** `Result{Allowed: false}` with `nil` error is a valid outcome; a non-nil error means the mechanism itself failed.

## 7. Domain shape — entities & value objects

Per [ddd-architect §3](../../design/ddd-architect/SKILL.md#3-tactical-ddd--building-blocks):

- **Value objects self-validate at construction**, unexported fields, zero value invalid, built via `New…` (`NewEmail`, `NewAddress`). Reach for them aggressively — a validated `Email` beats a bare `string` everywhere.
- **Entities carry behavior**, not just data — `User.Activate(now)`, with private transition maps enforcing legal state changes. No anemic bags of getters.
- **Generics for data structures and utility functions only**, as in [go-architect §13](../../languages/go-architect/SKILL.md#13-generics): `restkit.Response[T]`, `client.Do[T]`, `Callers[V]`. Reuse across ports still comes from interface composition, never from a type parameter that hides which adapter you wrote; if an interface would serve, use it.

## 8. Adapters — one per technology, N per port

The reuse axis is **multiple adapters behind one port**, swapped at wiring time:

- **Production** — the real backing tech (`smtp`, `postgres`, `valkey`).
- **Dev/observability** — e.g. a `logger` adapter that logs instead of sending.
- **Test** — a real, hand-written **in-memory** adapter (`memory`) with `Sent()`/`Reset()` helpers. This *is* the test double — see §10.

Each adapter imports the domain, translates errors inward (§6), and keeps its third-party dep contained. A port with only ever **one** adapter is ceremony — inline it until a second (the in-memory test double counts) justifies the seam ([hexagonal-arch §7](../../design/hexagonal-arch/SKILL.md#7-when-not-to-use-it)).

## 9. Scaling — start flat, grow to slices

Default to the **flat** shape. Split into vertical slices only when a genuine second bounded context appears (distinct ubiquitous language, per [ddd-architect §1](../../design/ddd-architect/SKILL.md#1-strategic-ddd--bounded-contexts)). When you do:

- **One package per bounded context** (`user/`, `auth/`), each internally hexagonal (domain + ports + service + adapter subpackages).
- **`app/`** is the application layer — cross-context use-case orchestration (`Register` → policy → hash → create → issue OTT → email). No business rules here; it sequences ports. Mirrors [go-architect §16](../../languages/go-architect/SKILL.md#16-multi-module-workspaces-gowork)'s `app` vs `cmd` split.
- **A context never imports another's domain.** It declares its own port (`UserLookup`) and an **`internal/acl/`** adapter translates the neighbor's service and errors across the seam — the anticorruption layer of [ddd-architect §8](../../design/ddd-architect/SKILL.md#8-anticorruption-layers-acl).

## 10. Testing — real doubles, no mock framework

Per [go-architect §9](../../languages/go-architect/SKILL.md#9-testing), sharpened:

- **No mock library, no generated mocks.** Unit isolation comes from the narrow ports — a fake is a plain struct, and the in-memory adapter (§8) is the reusable one.
- **Integration via `testcontainers-go`** — one container per package started in `TestMain` (`main_test.go`); each test gets isolation via a rolled-back transaction (`BeginTx` + `t.Cleanup`) or per-test uuid keys. Table/keyspace named `<name>_test`. **Postgres and Valkey already have the harness:** use `pgkit/pgtest` (`Start` in `TestMain`, or `NewPool`/`NewDB` per test) and `ratelimit/valkeytest` (`Start`/`StartClient`) instead of a hand-written `internal/testhelper`; write one only for another technology ([RECIPES §7](RECIPES.md#7-test-harness-testcontainers-one-container-per-package)).
- **`t.Parallel()` at parent and subtest**, table-driven, black-box `package x_test` for the public API plus white-box `package x` (`*_internal_test.go`) only to reach unexported helpers. Gate container tests so `go test -short ./...` stays fast.

## 11. Persistence & codegen (when a DB adapter exists)

- **Typed access** — `sqlc` (pgx/v5) is the default, per [go-architect §12](../../languages/go-architect/SKILL.md#12-database-access--sqlc-default-sqlx--goembed-alternative): hand-written `queries/*.sql`; DB enums overridden to domain types in `sqlc.yaml` so generated code maps to your VOs. Schema is derived from migrations by a `cmd/gen` step, never hand-maintained. `sqlx` + `//go:embed` is the alternative for a handful of static queries.
- **Migrations** — `goose` SQL with `//go:embed`, run through `pgkit/migrate` (`Config{FS, TableName}`) behind a thin public `migrate.Up(ctx, db)` and a **library-owned version table** (`<name>_schema_version`) so the lib's history is independent of the host app. Follow `identity/migrate` and `webpush/migrate`: a wrapper of a few lines that binds the embedded FS and table name and forwards to `pgkit/migrate`. Do not re-implement goose provider handling. See [sql-architect](../../databases/sql-architect/SKILL.md).
- **Value conversion** — `pgkit` (`OptText`, `UUIDString`, `MapNoRows`, `RunInTx`, …), not per-library copies. A library that uses Postgres depends on `pgkit` from its adapter subpackage only; its domain root stays clean.

## 12. Tooling (every repo gets the same set)

Copy from [assets/](assets); details in [repo-tooling-architect](../../tooling/repo-tooling-architect/SKILL.md) and [go-architect §14](../../languages/go-architect/SKILL.md#14-tooling):

- **`mise.toml`** pins the toolchain (go, task, golangci-lint, goimports, betteralign, trivy, and sqlc/goose when used).
- **`Taskfile.yml`** — `build`, `test` (`-race -count=1`), `test:short`, `fmt` (goimports `-local`), `lint`, `lint:fix`, `lint:doccheck`, `modernize` (`go fix`), `align:check/fix` (betteralign), `scan` (trivy), `tag` (semver-validated), and `check` = the pre-commit gate.
- **`.golangci.yml`** (v2) — copy [go-architect's `assets/golangci.yml`](../../languages/go-architect/assets/golangci.yml), set `goimports.local-prefixes` to the module path, scope `exhaustruct` to the `Config` structs. Ship the separate **`.golangci.doccheck.yml`** for on-demand doc coverage.
- **`.github/workflows/ci.yml`** — copy the asset. It is **manual-dispatch only, deliberately**: CI runs locally through `act`, so a push or tag never starts a billed runner. Dependencies under `github.com/ralvarezdev/*` are private for now, so each job takes the optional `GH_PRIVATE_MODULES_TOKEN` and sets `GOPRIVATE`; drop both once they are public.
- **`.editorconfig`**, **`.gitignore`**, **`renovate.json`**, and a **spec-first `docs/YYYY-MM-DD-spec.md`** written so an agent can rebuild the module from it alone (list the invariants explicitly).
- **`.rsk/`** — pin the architecture skills this repo was built with (`go-architect`, `hexagonal-arch`, `ddd-architect`, plus `sql-architect`/`repo-tooling-architect` as used) so the conventions travel with the repo.

## 13. Bootstrap procedure

1. Check [go-house-libs](../go-house-libs/SKILL.md): stop if an existing module covers the need. Then ask for `<name>`, `<namespace>` (default `github.com/ralvarezdev`), the shape (§1; §9 for flat vs slice) and the port(s) the library exposes.
2. `git init`; write `go.mod` (`module <namespace>/<name>`, `go 1.26`).
3. Copy the [assets/](assets) tooling set, including `.github/workflows/ci.yml`; `mise install`; set `Taskfile.yml`'s `MODULE` var and `goimports` `local-prefixes` to `<namespace>/<name>`. Add `.rsk/` and `CLAUDE.md` (§12).
4. Write the domain: value objects, entities, sentinel errors, the port interface(s) — stdlib + uuid only (§3–§7). For a toolkit or framework adapter, write the framework-free core first and give each heavy dependency its own subpackage or module (§1).
5. Write the in-memory adapter first (it doubles as the test double), then the production adapter(s) (§8).
6. Add persistence/codegen only if a DB adapter exists, on `pgkit` (§11).
7. Write the spec-first doc and the README (Packages table → Quick start → Testing).
8. `task check` must pass green before the first `task tag VERSION=0.1.0`.
9. When the module is tagged, add it to [go-house-libs](../go-house-libs/SKILL.md): a row in its table, a `references/<NAME>.md`, and its `STACK.md` entry.

## 14. Out of scope

- **Deployable services / `cmd/` binaries** — this scaffolds *libraries* consumers wire into their own composition root. Service layout → [go-architect §16](../../languages/go-architect/SKILL.md#16-multi-module-workspaces-gowork).
- **Functional-options APIs, ORMs, viper-in-library** — deliberately rejected by the house style (§5, §11).
- **The Go idioms and linter catalog themselves** — owned by [go-architect](../../languages/go-architect/SKILL.md).
