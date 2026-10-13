---
name: go-sdk-otel-hook-integration
description: >
  Use this when wiring a new motadatagosdk client into the motadatagosdk/otel
  facade (tracer, metrics, logger) — NEVER raw go.opentelemetry.io/otel.
  Covers the instrumented-call wrapper pattern, bounded-cardinality label
  rules, lazy sync.Once metric handles, and span.End discipline.
  Triggers: tracer.Start, metrics.NewCounter, metrics.Histogram, logger.L, instrumentedCall, span.SetAttributes, otel.Init, OTLP.
---

# go-sdk-otel-hook-integration (v1.0.0)

## Rationale

`motadatagosdk/otel` is a facade over the OTel SDK that (a) unifies logger/tracer/metrics lifecycle (Init once, shutdown in correct order: tracer→metrics→logger), (b) provides a fixed `Config` shape readable from YAML/env, and (c) hides API churn — the underlying `go.opentelemetry.io/otel` has made breaking changes across versions that the facade absorbs. Every new client MUST use this facade. Importing raw OTel directly defeats lifecycle coordination (spans outlive the flushed provider), duplicates metric registration under different names, fragments configuration, and breaks `otel.Shutdown(ctx)` ordering guarantees. This is CLAUDE.md rule 6 bullet ("OTel via `motadatagosdk/otel` (NOT raw OTel API)") operationalized.

## Activation signals

- A new client package is being created under `core/` or `events/`
- Design lists a `Tracer`, `Meter`, or imports `go.opentelemetry.io/otel/*` directly — pull this skill to redirect
- Hot-path method needs instrumentation — use the `instrumentedCall` wrapper pattern
- Reviewing spans for attribute cardinality (BLOCKER: unbounded-cardinality labels like raw keys, userIDs)
- `sdk-convention-devil-go` flagging raw-otel imports

## Target SDK Convention

Current convention in motadatagosdk:

The facade lives at `motadatagosdk/otel/` and exposes three sub-packages plus a top-level `Init/Shutdown`:
- `motadatagosdk/otel/tracer` — `tracer.Start(ctx, name) (ctx, Span)`, `tracer.StringAttr/IntAttr/...`, `span.SetAttributes`, `span.SetError`, `span.SetOK`, `span.End`
- `motadatagosdk/otel/metrics` — `metrics.NewCounter`, `metrics.NewHistogram`, `metrics.NewGauge`, `metrics.Labels` (a map), `.Inc/Observe/Set` take `ctx` + labels
- `motadatagosdk/otel/logger` — `logger.L()` returns the global, package-level `logger.Info/Warn/Error(ctx, msg, fields...)`, structured fields via `logger.String/Int/Error(key, val)`
- `motadatagosdk/otel` — top-level `Init(cfg) (*OTEL, error)`, `Shutdown(ctx)` (coordinated), `MustInit(cfg)` for main()

Application-level entry: consumer's `main()` calls `otel.Init(cfg)` once, defers `otel.Shutdown(ctx)`. Clients under `core/` never call `Init` — they use the global accessors on the assumption init has happened.

If TPRD requests divergence: the only legitimate exception is when the client itself exposes OTel-compatibility (e.g., an OTLP collector wrapper). In that case, `sdk-perf-architect-go` + `sdk-convention-devil-go` co-sign a §6 footnote. Every other deviation is rejected.

## GOOD examples

The instrumented-call wrapper — every data-path method routes through a single choke point that starts a span, increments `requests`, records `duration`, maps error, increments `errors` with classified label, marks span outcome:

```go
func (c *Cache) instrumentedCall(ctx context.Context, cmd string, fn func(context.Context) error) error {
    ctx, span := tracer.Start(ctx, "dfly."+cmd)
    defer span.End()
    span.SetAttributes(
        tracer.StringAttr("db.system", "redis"),
        tracer.StringAttr("server.address", c.cfg.Addr),
        tracer.StringAttr("dfly.cmd", cmd),
    )

    m := globalMetrics()
    cmdLabels := metricsLabels("cmd", cmd)
    start := time.Now()
    m.requests.Inc(ctx, cmdLabels)

    err := c.runThroughCircuit(ctx, fn)
    mapped := mapErr(err)
    m.duration.ObserveDuration(ctx, start, cmdLabels)

    if mapped != nil {
        m.errors.Inc(ctx, metricsLabels("cmd", cmd, "error_class", classify(mapped)))
        span.SetError(mapped)
    } else {
        span.SetOK()
    }
    return mapped
}
```
(Source: `core/l2cache/dragonfly/cache.go` lines 185-218.) Invariants enforced by this shape: `cmd` is a compile-time literal at every callsite (bounded cardinality); payloads/keys/credentials never land in span attributes; metrics and span outcomes stay consistent because they share the error classification.

Lazy-init metric bundle — one `sync.Once` builds the Counter/Histogram/Gauge handles on first `New()`, so hot-path lookups are allocation-free and the package has no `init()`:

```go
var (
    metricsOnce sync.Once
    metricsPkg  *cacheMetrics
)

func globalMetrics() *cacheMetrics {
    metricsOnce.Do(func() {
        metricsPkg = &cacheMetrics{
            requests: metrics.NewCounter(
                metricsNamespace+".requests",
                "Count of Dragonfly client command invocations, by cmd."),
            duration: metrics.NewHistogram(
                metricsNamespace+".duration_ms",
                "Dragonfly client command duration in milliseconds, by cmd."),
            // ... more handles
        }
    })
    return metricsPkg
}
```
(Source: `core/l2cache/dragonfly/metrics.go` lines 39-86. Note: `metricsNamespace` is a package-const like `"dragonfly"` — namespacing is per-client, not per-instance.)

Bounded-cardinality labels + structured log — `cmd` is one of a fixed ~30-command set; `error_class` is the output of a `classify(err)` function that returns one of 8 strings:

```go
m.errors.Inc(ctx, metricsLabels("cmd", cmd, "error_class", classify(mapped)))
// ...
func classify(err error) string {
    switch {
    case errors.Is(err, ErrTimeout):     return "timeout"
    case errors.Is(err, ErrNil):         return "nil"
    case errors.Is(err, ErrWrongType):   return "wrong_type"
    case errors.Is(err, ErrAuth):        return "auth"
    case errors.Is(err, ErrCodec):       return "codec"
    case errors.Is(err, ErrCircuitOpen): return "circuit_open"
    case errors.Is(err, ErrUnavailable): return "unavailable"
    default:                              return "other"
    }
}
```
(Source: `core/l2cache/dragonfly/errors.go` lines 216-240.)

## BAD examples (anti-patterns)

Raw OTel imports — bypass the facade, break coordinated shutdown, double-register with differently-shaped names:

```go
// BAD
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/metric"
)

var meter = otel.Meter("dragonfly")
var requestsCounter, _ = meter.Int64Counter("dragonfly.requests")

func (c *Cache) Get(ctx context.Context, k string) (string, error) {
    _, span := otel.Tracer("dragonfly").Start(ctx, "Get")
    defer span.End()
    requestsCounter.Add(ctx, 1)
    // ...
}
```
Why it breaks: `otel.Shutdown(ctx)` only flushes the providers the facade registered; this client's spans silently drop at process exit. Global `otel.Meter` returns a different provider than `metrics.NewCounter` builds against — two names for the same signal, one without the service resource attributes the facade adds. `sdk-convention-devil-go` flags this as BLOCKER.

Unbounded-cardinality labels — embedding raw keys, user IDs, or payload content in span attributes or metric labels:

```go
// BAD
span.SetAttributes(
    tracer.StringAttr("dfly.key", key),          // <-- arbitrary user key
    tracer.StringAttr("dfly.value", string(val)), // <-- payload
    tracer.StringAttr("user.id", userID),         // <-- unbounded
)
m.requests.Inc(ctx, metrics.Labels{"key": key})   // <-- cardinality explosion
```
Why it breaks: Prometheus / OTel collectors index on label values; unbounded cardinality blows up the tsdb (GB of series per hour for a busy cache). Credentials in `Password`/`token` attrs also leak to logs. Rule: labels + attrs are identifiers for operational buckets (command name, error class, tenant if bounded), never raw inputs.

Forgetting `span.End()` — goroutine-leak analog for spans:

```go
// BAD
func (c *Cache) Get(ctx context.Context, k string) (string, error) {
    ctx, span := tracer.Start(ctx, "dfly.Get")
    // ... no defer span.End() ...
    if err := c.validate(k); err != nil {
        return "", err   // <-- span leaks, never flushed
    }
    // ...
}
```
Why it breaks: the trace exporter buffers "in-flight" spans; without `End`, they sit forever and count against the span queue quota (default 2048; exhaust = dropped-span warnings + memory growth). Always `defer span.End()` on the line immediately after `tracer.Start`.

Per-call metric construction — rebuilding Counter/Histogram handles on every method invocation:

```go
// BAD
func (c *Cache) Get(ctx context.Context, k string) (string, error) {
    counter := metrics.NewCounter("dragonfly.requests", "...")  // <-- constructs a handle
    counter.Inc(ctx, metrics.Labels{"cmd": "GET"})
    // ...
}
```
Why it breaks: `NewCounter` is idempotent (deduped by name) but it still takes a mutex on `Registry` and allocates. Do this on a hot path and you lose 10-30 ns/op. Build once in `globalMetrics()` (see GOOD examples), reference the handle on the hot path.

## Decision criteria

When to add a new span:
- At every data-path method entry — spans are the unit of trace-level visibility
- At every external-IO boundary (dial, request, flush) if the boundary is not itself inside a library that instruments

When to add a new metric:
- Counter for every "event" (request, error, retry, circuit transition) with bounded label shape
- Histogram for every duration (prefer `_ms` suffix; the facade already multiplies units sensibly)
- Gauge for every resource-quantity poll (pool size, queue depth, goroutine count)

When to add a log line inside the client:
- `logger.Warn` on misconfiguration the constructor can tolerate (dragonfly warns on non-zero `MaxRetries`)
- `logger.Error` is RARE inside a client — the client returns errors; logging them too duplicates the signal. Only log when the error is unreachable to the caller (background goroutine failure).

Never:
- Instrument in an `init()` — violates G41 and breaks lifecycle ordering
- Pass `context.Background()` to `tracer.Start` when the caller gave you a `ctx` — destroys trace parent linkage
- Hardcode the service name — comes from `config.Config.ServiceName`, set once at `otel.Init`

## Cross-references

- `go-sdk-config-struct-pattern` — `otel.Init(cfg config.Config) (*OTEL, error)` is the Config-struct archetype; clients should match the shape
- `sdk-convention-devil-go` — enforces no-raw-otel-imports at design phase
- `go-concurrency-patterns` — graceful shutdown sequence: cancel ctx → drain workers → `otel.Shutdown(ctx)` → exit
- `go-otel-instrumentation` — general OTel patterns and semantic-conventions reference (this skill is the motadatagosdk-specific operationalization)
- `go-client-shutdown-lifecycle` — the `Cache.Close(ctx)` method must not block `otel.Shutdown` — it should be idempotent + time-bounded

## Guardrail hooks

No dedicated `Gxx.sh` for otel-vs-raw-otel imports (proposed for v0.4.0 as G111-ish). Current enforcement is design-phase via `sdk-convention-devil-go`. Related guardrails:

- **G41** — no `init()` functions. Catches the "register metrics at package init" anti-pattern. BLOCKER.
- **G99** — every pipeline-authored file carries `[traces-to:]`. Instrumented-call wrapper carries markers per dragonfly example. BLOCKER.
- **G104** — `allocs/op` budget. Per-call metric construction busts this; lazy-init handles keep it clean. BLOCKER.
- **G109** — profile-shape coverage. If span/metric overhead dominates the CPU profile, that is a design-phase signal to revisit hot-path instrumentation depth. BLOCKER.

Manual verification during review: grep the client's source for `go.opentelemetry.io/otel` — zero hits outside `motadatagosdk/otel/` itself. Any hit = NEEDS-FIX.
