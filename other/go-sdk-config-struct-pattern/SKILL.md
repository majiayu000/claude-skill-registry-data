---
name: go-sdk-config-struct-pattern
description: >
  Use this when designing the constructor for a new motadatagosdk client —
  picking between Config struct + New(cfg) (otel/, events/jetstream/) or
  functional options + exported Config (core/l2cache/dragonfly/) based on
  sibling-package shape and field count, with applyDefaults + validate split.
  Triggers: Config, func New, WithX, Option, constructor, applyDefaults, validate, functional-options.
---

# go-sdk-config-struct-pattern (v1.0.0)

## Rationale

motadatagosdk has two legitimate constructor shapes in production — `otel.Init(cfg config.Config) (*OTEL, error)` (Config-struct primary) and `dragonfly.New(opts ...Option) (*Cache, error)` (functional-options primary). Both are correct for their context. What is incorrect is inventing a third: builder chains, opaque `interface{}` args, package-level `init()` side effects, or silent global config. New clients must pick one of the two established shapes and match the siblings they live next to (otel/* follows otel.Init; core/l2cache/* follows dragonfly.New). Divergence fragments consumer mental models and breaks `api-ergonomics-audit` quickstart-boilerplate checks. This is an instance of CLAUDE.md rule 18 (Target SDK Convention Respect).

## Activation signals

- Designing a new client under `core/` or `events/` — need to pick a constructor shape
- Design lead rejecting a proposed builder-pattern API
- `sdk-convention-devil-go` finding a constructor-shape mismatch
- TPRD §6 Config section is empty or proposes non-standard shape
- Reviewing quickstart for a new package — should be ≤5 lines

## Target SDK Convention

Current convention in motadatagosdk:

- **`otel/`** — Config struct primary. `otel.Init(cfg config.Config) (*OTEL, error)`. No options functions. `MustInit(cfg)` variant panics on error for main() use.
- **`core/l2cache/dragonfly/`** — Functional options primary, but `Config` struct is still exported so power-users can build literal configs. `dragonfly.New(opts ...Option) (*Cache, error)`; each option is a tiny `WithX` function.
- **`events/jetstream/`** — Config struct primary (mirrors otel/).

Rule of thumb: if the client has >6 commonly-set fields, functional options beat a fat Config literal at callsites. Below that, Config struct wins (shorter, discoverable via godoc, named-field literal is self-documenting).

If TPRD requests divergence: require §6 to explicitly cite the target precedent (e.g., "matches `dragonfly.New` because there are 14 config fields and only 3 are commonly set"). Without citation, the design MUST match the immediate sibling directory's shape.

## GOOD examples

Config struct + New pattern from `otel/otel.go` — cfg is a typed struct, error returned, no hidden global state:

```go
func Init(cfg config.Config) (*OTEL, error) {
    otelInstance := &OTEL{config: cfg}

    loggerInstance, loggererror := logger.Init(cfg.GetLoggerConfig())
    if loggererror != nil {
        return nil, fmt.Errorf("initialize logger: %w", loggererror)
    }
    otelInstance.Logger = loggerInstance
    // ... metrics + tracer init, cleanup on partial failure ...
    return otelInstance, nil
}
```
(Source: `motadatagosdk/otel/otel.go` lines 120-176. Note: partial-failure cleanup is mandatory — half-init is worse than no-init.)

Functional options + exported Config hybrid from `core/l2cache/dragonfly/cache.go` — `Config` is exported for literal construction, but `New(opts...)` is the primary callsite:

```go
// Config is the primary user-facing configuration for Cache.
// Populated via New(opts ...Option); exported so power-users can build
// a Config directly and inject via a single option.
// [traces-to: TPRD-§6-Config]
type Config struct {
    Addr            string
    DialTimeout     time.Duration
    // ... 15 more fields
}

func New(opts ...Option) (*Cache, error) {
    cfg := &Config{}
    for _, opt := range opts {
        if opt != nil { opt(cfg) }
    }
    cfg.applyDefaults()
    if err := cfg.validate(); err != nil {
        return nil, err
    }
    // ... build client ...
}
```
(Source: `core/l2cache/dragonfly/cache.go` lines 43-96, `options.go` lines 17-22.)

Separate `applyDefaults` + `validate` methods on `*Config` — centralizes invariant logic, idempotent so repeated calls are safe, keeps `New` readable:

```go
func (c *Config) applyDefaults() {
    if c.DialTimeout == 0 { c.DialTimeout = defaultDialTimeout }
    if c.ReadTimeout == 0 { c.ReadTimeout = defaultReadTimeout }
    // ...
}

func (c *Config) validate() error {
    if c.Addr == "" {
        return fmt.Errorf("%w: Addr is required", ErrInvalidConfig)
    }
    if c.TLS != nil && c.TLS.ServerName == "" && !c.TLS.SkipVerify {
        return fmt.Errorf("%w: TLS.ServerName required unless SkipVerify", ErrInvalidConfig)
    }
    // ...
    return nil
}
```
(Source: `core/l2cache/dragonfly/config.go` lines 101-156. Errors wrap `ErrInvalidConfig` so callers get `errors.Is(err, dragonfly.ErrInvalidConfig)` matching.)

## BAD examples (anti-patterns)

Builder pattern — fluent chains that hide zero-state and defeat godoc's ability to show the full option set:

```go
// BAD
cache := dragonfly.Builder().
    WithAddr("host:6379").
    WithPool(10).
    WithTLS().
    Build()
```
Why it breaks: (1) no sibling in motadatagosdk uses this — violates rule 18; (2) error path is awkward (Build returns error, but intermediate calls may panic); (3) nil-safety is non-obvious (what does `WithTLS()` do without a config?); (4) godoc on `*Builder` buries options behind method listings instead of the exported `Config`.

Config-as-map — opaque `map[string]interface{}` or `map[string]any`:

```go
// BAD
func New(cfg map[string]any) (*Cache, error) {
    addr, _ := cfg["addr"].(string)
    // ...
}
```
Why it breaks: no compile-time field safety, no godoc on fields, no autocomplete, no zero-value semantics, type assertions explode at runtime. Go made structs first-class for this reason.

Package-level `init()` or mandatory `SetGlobal()` before New — hidden coupling, defeats unit-test isolation, violates CLAUDE.md rule 6 ("No init() functions"):

```go
// BAD
func init() {
    defaultCache = newInternalCache()
}

func New() *Cache {
    return defaultCache.Clone()  // requires init to have run
}
```
Why it breaks: parallel tests (`t.Parallel`) race on the global; `goleak.VerifyTestMain` detects leaks the init spawned; import-cycle risk grows with every new global. The fix is to thread state through `New(cfg)` and make the consumer own the lifecycle (including `Close(ctx)`).

Required positional args instead of Config struct — breaks minor-bump safety:

```go
// BAD — v1.0.0
func New(addr string, poolSize int) (*Cache, error) { ... }

// v1.1.0 wants to add a required retry policy:
func New(addr string, poolSize int, retryPolicy RetryPolicy) (*Cache, error) { ... }  // MAJOR break
```
Why it breaks: every signature expansion is a major bump (see `sdk-semver-governance`). Config-struct or functional options let you add fields without touching the constructor signature.

## Decision criteria

| Question | Go with Config struct + New(cfg) | Go with functional options |
|---|---|---|
| Sibling package shape | otel/, events/jetstream/ | core/l2cache/dragonfly/ |
| Number of commonly-set fields | ≤6 | >6 |
| Likelihood of future optional-field growth | Low (stable domain) | High (evolving feature set) |
| Need for per-option side-effect (e.g., Warn on nil breaker) | Awkward | Natural — options can `logger.Warn(...)` |
| Config struct exposed publicly | Yes (primary) | Yes (power-user escape hatch — still export it) |

Always export `Config` and `Default() Config` (or package-level `defaultX` consts) even when functional options are primary — it lets advanced callers build literal configs, enables YAML/JSON unmarshal, and simplifies testing.

Always separate `applyDefaults` and `validate` into methods on `*Config`. `New` becomes a 5-line assembler: apply opts → defaults → validate → build → return.

## Cross-references

- `sdk-convention-devil-go` — runs the "which shape matches sibling" check at design phase
- `api-ergonomics-audit` — quickstart-check fails if construction takes >5 lines; a well-shaped Config/options design keeps this clean
- `sdk-marker-protocol` — `[stable-since:]` on Config fields and option functions gates future signature changes via G101
- `go-error-handling-patterns` — validation errors wrap a package sentinel (`ErrInvalidConfig`) so callers can `errors.Is`
- `go-client-shutdown-lifecycle` — the `New → Close` pair is symmetric; a Config that takes a `context.Context` for construction hints at a coupling that should instead live on the methods

## Guardrail hooks

No single `Gxx.sh` enforces "Config struct vs options" directly — this is a design-phase convention check handled by `sdk-convention-devil-go` (read-only verdict in `runs/<id>/design/reviews/convention-devil.md`). Related guardrails that reject bad shapes indirectly:

- **G41** (no `init()` functions) — blocks the init-pattern anti-example. BLOCKER.
- **G99** — every exported symbol (including Config + New) must carry `[traces-to:]`. BLOCKER.
- **G101** — once v1.0.0 ships with `[stable-since:]` on Config fields, any field type-change requires TPRD §12 MAJOR. BLOCKER.

Design-phase verdict loop: if `sdk-convention-devil-go` flags NEEDS-FIX on the shape choice, design-lead rewrites `api.go.stub` before Phase 1 exit. No Phase 2 entry without ACCEPT.
