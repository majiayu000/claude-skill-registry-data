---
name: sdk-semver-governance
description: >
  Use this when classifying a public-API diff into patch / minor / major —
  reading the current API manifest against the proposed API stub, applying
  language-adapter-specific compatibility rules (added symbols, struct/class
  field changes, interface/Protocol expansion, sentinel add/remove, exception
  hierarchy changes), and verifying TPRD §12 declares the matching bump.
  Triggers: semver, major, minor, patch, breaking, api-surface, stable-since, gorelease, griffe, TPRD-§12.
version: 1.1.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [semver, governance, api-surface, language-pluggable]
cross_language_ok: true
---

<!-- Semver classification rules are language-neutral; the reference tooling differs per pack: `gorelease` for Go (`golang.org/x/exp/cmd/gorelease`), `griffe` or `pylint --diff` for Python. Examples in this skill are Go-flavored because Go is the canonical pack; the same rules apply to Python with `class` instead of `struct`, `Protocol` instead of `interface`, and exception classes instead of sentinel `var`s. The leakage scripts honor `cross_language_ok: true`. -->


# sdk-semver-governance (v1.0.0)

## Rationale

Go's import-compatibility rule (rsc.io/go-import-versioning) makes semver mistakes uniquely painful: `v2+` requires a module path suffix, and a consumer who took `v1.3.0` cannot absorb an accidental breaking change in `v1.4.0` without a code change they did not sign up for. Every time the pipeline emits a signature change, it must render a bump verdict (patch / minor / major) that matches what `golang.org/x/exp/cmd/gorelease` would compute — gorelease is the canonical Go-community reference implementation for this classification. Skipping the classification hands breaking changes to consumers as patch-level updates; shipping a major change without the `/vN` path suffix breaks the module cache.

## Activation signals

- A design phase (D1–D5) emits `design/api.go.stub` or `design/interfaces.md`
- Mode B (extension) or Mode C (incremental update) runs — existing `current-api.json` is present
- TPRD §12 declares the intended bump; agent must verify the declaration matches the change scope
- `[stable-since:]` markers change signature (ties in to G101)
- `sdk-semver-devil` or `sdk-breaking-change-devil-go` agents are scheduled

## Classification rules (follows gorelease)

Reference: `golang.org/x/exp/cmd/gorelease`. Install + run: `go run golang.org/x/exp/cmd/gorelease@latest -base=vX.Y.Z`.

| Change | Bump | Why |
|---|---|---|
| Add new exported symbol | minor | Additive |
| Add field to exported struct | minor (usually) | Breaking IFF struct is a composite literal key elsewhere (named-field = safe; positional = break) |
| Add method to concrete type | minor | Additive |
| Add method to interface | **major** | Interface expansion — all implementers now fail to compile |
| Remove / rename any exported symbol | **major** | Callers break |
| Change func signature (param types, return types, arity, variadic arity) | **major** | Callers break |
| Change field type on exported struct | **major** | Consumers doing `x.Field = y` may break |
| Tighten generic type constraints | **major** | Callers passing previously-valid types break |
| Loosen generic type constraints | minor | Strict superset |
| Un-export a symbol (lowercase first letter) | **major** | Same as removal |
| Fix bug in unexported impl of exported symbol | patch | Observable behavior unchanged at type level |
| Godoc-only change | patch | No API movement |
| Add sentinel error (new `var ErrX = errors.New(...)`) | minor | Additive |
| Remove sentinel error | **major** | `errors.Is(err, pkg.ErrX)` breaks at compile time |

v0.y.z escape hatch: `gorelease` allows breaking changes between any v0.a.b → v0.a.(b+1). Prefer staying v0.x while the API is in flux; move to v1.0.0 only when the §7-API is frozen and at least one internal consumer has integrated without finding design flaws.

## GOOD examples

Initial package ships at v1.0.0 with `[stable-since:]` markers on every exported symbol — Mode A new-package shape:

```go
// Config is the primary user-facing configuration for Cache.
// [stable-since: v1.0.0]
// [traces-to: TPRD-§6-Config]
type Config struct {
    Addr     string
    // ...
}

// New constructs a Cache from the supplied options.
// [stable-since: v1.0.0]
// [traces-to: TPRD-§5.1-New]
func New(opts ...Option) (*Cache, error) { ... }
```
(Source: dragonfly P0 — every P0 symbol carries `[stable-since:]`; design-time verdict was ACCEPT @ v1.0.0.)

Minor bump adding a new sentinel — no existing caller breaks, bumps v1.0.0 → v1.1.0:

```go
// ErrCodec wraps any codec-layer marshal/unmarshal failure.
// [stable-since: v1.1.0]
// [traces-to: TPRD-§5.2 TPRD-§7.1]
var ErrCodec = errors.New("dragonfly: codec failure")
```
(Source: `core/l2cache/dragonfly/errors.go` line 95 — P1 addition; note `stable-since: v1.1.0` not v1.0.0 because the symbol did not exist in v1.0.0.)

Major bump declaration in TPRD §12 when a signature change is intentional — G101 clears because the keyword is present:

```md
## §12 Breaking-Change Risk

This release is **MAJOR** (v1.x.y → v2.0.0). Rationale:
- `Cache.Get` signature adds a `GetOption` variadic — interface `CacheReader` in `contracts/cache.go` changes.
- `ErrNotFound` renamed to `ErrNil` — all `errors.Is(err, ErrNotFound)` callsites break.
- Module path bumps to `motadatagosdk/core/l2cache/dragonfly/v2`.

No Deprecated-then-remove path available — see §13 Rollout.
```

## BAD examples (anti-patterns)

Silent-break patch bump — adding a required method to an exported interface tagged as a patch release:

```go
// v1.4.0 — v1.4.1 "patch release":
type CacheReader interface {
    Get(ctx context.Context, key string) (string, error)
    MGet(ctx context.Context, keys ...string) ([]string, error)   // NEW, unannotated
}
```
Why it breaks: every external type implementing `CacheReader` compiled against v1.4.0 now fails to satisfy the interface at compile time. gorelease classifies this as major; calling it patch misleads consumers into an unreviewed update. Either add a new interface (`CacheReaderV2`) or ship as major.

Struct-field-type coercion disguised as minor — changing `int` to `int64` looks harmless until you hit a caller:

```go
// v1.4.0:
type Config struct { PoolSize int }

// v1.5.0 (claimed minor):
type Config struct { PoolSize int64 }   // not minor
```
Why it breaks: `cfg.PoolSize = runtime.NumCPU()` now requires an explicit cast. gorelease flags it major. The only minor-safe widening is adding fields.

Removing a sentinel error without a deprecation window:

```go
// v1.4.0:
var ErrPoolExhausted = errors.New("...")

// v1.5.0:
// (ErrPoolExhausted deleted — replaced by ErrUnavailable)
```
Why it breaks: `errors.Is(err, pkg.ErrPoolExhausted)` now fails to compile. Required path: v1.4.1 adds `Deprecated:` godoc + `[deprecated-in: v1.4.1]` marker, v2.0.0 removes it. Removing at a minor is G101 BLOCKER.

## Decision criteria

When the auto-classification disagrees with TPRD §12:
1. Trust gorelease, flag TPRD §12 as needing update. Pipeline must not silently accept a lower bump than the diff warrants.
2. If TPRD §12 declares major and diff is minor-equivalent, ACCEPT — over-declaration is a safe human choice (maybe the author knows about behavioral changes gorelease cannot see).
3. If the `/vN` path suffix is missing for a major bump, emit BLOCKER with suggested module path rewrite.

For Mode A (new package): initial v1.0.0 is reasonable if SDK conventions are v1.x.y throughout. v0.1.0 acceptable only if TPRD §13 Rollout declares "experimental — API may change before v1". Seed every symbol with `[stable-since: v1.0.0]` at first ship.

For Mode B (extension): verify each new export carries `[stable-since: <current-or-next-version>]`. Existing stable-since strings must not regress (v1.1.0 → v1.0.0 is meaningless and G102 rejects the syntax anyway).

## Per-language adapter realization

| Aspect | Go pack | Python pack |
|---|---|---|
| Reference classifier | `golang.org/x/exp/cmd/gorelease` | `griffe` (or `pylint --diff` against pinned baselines) |
| API stub artifact | `design/api.go.stub` | `design/api.pyi.stub` |
| API manifest | `current-api.json` (gorelease format) | `current-api.json` (griffe diff format) |
| Module path bump on major | `motadatagosdk/.../v2` | `motadatapysdk` package version in `pyproject.toml`; consumers pin via constraints |
| Sentinel-error model | `var ErrX = errors.New(...)` package vars | exception class hierarchy under `MotadataError` |
| Interface expansion | `interface { ... }` adding a method = major | `Protocol` / ABC adding an abstract method = major |
| `errors.Is` / `isinstance` semantics | `errors.Is(err, ErrX)` | `isinstance(exc, ErrX)` |

The classification table above is Go-flavored; the same rules apply per-pack. The bump verdict, TPRD §12 cross-check, and `[stable-since:]` marker enforcement are identical across packs.

## Cross-references

- `sdk-marker-protocol` — consumes `[stable-since:]` and `[deprecated-in:]`; G101 is the enforcement arm
- `go-error-handling-patterns` / `python-exception-patterns` — sentinel/exception addition is minor; removal is major
- `sdk-convention-devil-go` / `sdk-convention-devil-python` — flag missing `[stable-since:]` on new exports
- `api-ergonomics-audit` — an ergonomics NEEDS-FIX finding may force an API rewrite that triggers major bump

## Guardrail hooks

- **G101** — `[stable-since:]` signature changes require TPRD §12 `MAJOR` or `breaking` keyword present. BLOCKER. Baseline at `baselines/<target_language>/stable-signatures.json` (per-language partition; G101 resolves the path from `runs/<run-id>/context/active-packages.json:target_language`), whitespace-normalized.
- **G102** — `[stable-since:]` value grammar: `^v\d+\.\d+\.\d+$`. BLOCKER on malformed.
- Reference tool (not run as a guardrail, used at design time): `go run golang.org/x/exp/cmd/gorelease@latest -base=<prev-tag>` — emits the canonical classification. If gorelease and pipeline disagree, pipeline wins (it has TPRD §12 context), but the divergence is logged for human review.
