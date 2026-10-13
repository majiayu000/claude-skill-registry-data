---
name: go-otel-instrumentation
description: >
  Use this when standing up OpenTelemetry in a Go service — TracerProvider,
  MeterProvider, OTLP exporters, slog trace-correlation handler, NATS header
  carrier, standard service metrics, span attribute conventions, and the
  graceful Shutdown ordering rules.
  Triggers: TracerProvider, MeterProvider, OTLP, slog, trace correlation, span attributes, NATS propagation, resource.New, otel.Shutdown.
---



# OTel Instrumentation Patterns

OpenTelemetry API patterns for client SDKs in the motadata platform. SDKs use
the global OTel API (`otel.Tracer(name)`); provider lifecycle (TracerProvider,
MeterProvider, LoggerProvider) is the CONSUMER's responsibility. For SDK
lifecycle and the `motadatagosdk/otel` facade, see
`skills/go-sdk-otel-hook-integration/SKILL.md` — that is the canonical reference.

This skill covers:
- OTel API surface (Tracer / Meter / Logger client side)
- Resource construction patterns (NewResource pitfalls)
- Trace-correlation handler for `slog`
- Span attribute conventions (semconv)
- Error / status pairing (`RecordError` + `SetStatus`)
- W3C baggage for consumer-side runtime attrs (e.g., tenant_id)

This skill does NOT cover:
- Provider initialization (consumer's job; see go-sdk-otel-hook-integration facade if SDK author owns the consumer-side wiring)
- Service-flavor `cmd/main.go` boot patterns (move to platform docs)

## When to Activate
- When designing the observability SDK (`pkg/observability/`)
- When implementing TracerProvider, MeterProvider, or log setup in any service
- When adding custom metrics or spans to business logic
- When propagating trace context through NATS JetStream messages
- When reviewing code for observability completeness
- Used by: sdk-designer, sdk-implementor, code-generator, infrastructure-architect, component-designer, observability-test-agent

## Provider Initialization

### TracerProvider Setup

```go
// pkg/observability/tracer.go
func NewTracerProvider(ctx context.Context, cfg OTelConfig, res *resource.Resource) (*sdktrace.TracerProvider, error) {
    if cfg.Exporter == "none" {
        return sdktrace.NewTracerProvider(sdktrace.WithResource(res)), nil
    }

    exporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint(cfg.OTLPEndpoint),
        otlptracegrpc.WithInsecure(), // TLS handled by mesh/sidecar
    )
    if err != nil {
        return nil, fmt.Errorf("creating trace exporter: %w", err)
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter,
            sdktrace.WithMaxExportBatchSize(512),
            sdktrace.WithBatchTimeout(5*time.Second),
        ),
        sdktrace.WithResource(res),
        sdktrace.WithSampler(sdktrace.ParentBased(
            sdktrace.TraceIDRatioBased(cfg.SampleRate),
        )),
    )
    return tp, nil
}
```

### MeterProvider Setup

```go
// pkg/observability/meter.go
func NewMeterProvider(ctx context.Context, cfg OTelConfig, res *resource.Resource) (*sdkmetric.MeterProvider, error) {
    if cfg.Exporter == "none" {
        return sdkmetric.NewMeterProvider(sdkmetric.WithResource(res)), nil
    }

    exporter, err := otlpmetricgrpc.New(ctx,
        otlpmetricgrpc.WithEndpoint(cfg.OTLPEndpoint),
        otlpmetricgrpc.WithInsecure(),
    )
    if err != nil {
        return nil, fmt.Errorf("creating metric exporter: %w", err)
    }

    mp := sdkmetric.NewMeterProvider(
        sdkmetric.WithReader(sdkmetric.NewPeriodicReader(exporter,
            sdkmetric.WithInterval(15*time.Second),
        )),
        sdkmetric.WithResource(res),
    )
    return mp, nil
}
```

### Resource Construction

```go
func NewResource(ctx context.Context, serviceName, serviceVersion string) (*resource.Resource, error) {
    return resource.New(ctx,
        resource.WithAttributes(
            semconv.ServiceNameKey.String(serviceName),
            semconv.ServiceVersionKey.String(serviceVersion),
            semconv.DeploymentEnvironmentKey.String(os.Getenv("ENVIRONMENT")),
        ),
        resource.WithHost(),
        resource.WithProcess(),
    )
}
```

**IMPORTANT**: Do NOT use `resource.Merge(resource.Default(), ...)` — it causes
schema URL conflicts with transitive OTel SDK dependencies. Always use
`resource.New(ctx, ...)`.

### Structured Logging with Trace Correlation

```go
// pkg/observability/logger.go
func NewLogger(cfg OTelConfig) *slog.Logger {
    opts := &slog.HandlerOptions{Level: parseLevel(cfg.LogLevel)}
    var handler slog.Handler
    handler = slog.NewJSONHandler(os.Stdout, opts)
    // Wrap with trace-correlation handler
    handler = &traceCorrelationHandler{inner: handler}
    return slog.New(handler)
}

type traceCorrelationHandler struct {
    inner slog.Handler
}

func (h *traceCorrelationHandler) Handle(ctx context.Context, r slog.Record) error {
    sc := trace.SpanContextFromContext(ctx)
    if sc.IsValid() {
        r.AddAttrs(
            slog.String("trace_id", sc.TraceID().String()),
            slog.String("span_id", sc.SpanID().String()),
        )
    }
    return h.inner.Handle(ctx, r)
}
```

## Service-flavor bootstrap

Out of scope for client SDKs. If you are wiring a consumer-side application,
see `skills/go-sdk-otel-hook-integration/SKILL.md` for the facade pattern.

## NATS Trace Propagation

```go
// Inject trace context into NATS message headers
func InjectTraceContext(ctx context.Context, msg *nats.Msg) {
    carrier := NATSHeaderCarrier(msg.Header)
    otel.GetTextMapPropagator().Inject(ctx, carrier)
}

// Extract trace context from NATS message headers
func ExtractTraceContext(ctx context.Context, msg *nats.Msg) context.Context {
    carrier := NATSHeaderCarrier(msg.Header)
    return otel.GetTextMapPropagator().Extract(ctx, carrier)
}

// NATSHeaderCarrier adapts nats.Header to propagation.TextMapCarrier
type NATSHeaderCarrier nats.Header

func (c NATSHeaderCarrier) Get(key string) string    { return nats.Header(c).Get(key) }
func (c NATSHeaderCarrier) Set(key, val string)       { nats.Header(c).Set(key, val) }
func (c NATSHeaderCarrier) Keys() []string {
    keys := make([]string, 0, len(c))
    for k := range c {
        keys = append(keys, k)
    }
    return keys
}
```

## Client-library metric naming

SDK clients emit metrics under `motadata.<sdk-name>.<thing>` namespace following
OTel `<domain>.client.*` semconv:

| Domain | Pattern |
|---|---|
| Messaging | `motadata.<sdk>.publish.requests` (counter), `.duration_ms` (histogram), `.errors` (counter) |
| RPC | per `rpc.client.*` semconv (`rpc.client.duration` etc) |
| DB | per `db.client.*` semconv |
| Generic | `motadata.<sdk>.requests`, `.duration_ms`, `.errors` |

Default metric bundle (request / duration / error counters) is provided by the
`motadatagosdk/otel/metrics` facade — see go-sdk-otel-hook-integration §"Lazy-init
metric bundle" pattern. SDKs DO NOT register custom counters per call (cardinality
explosion); use the lazy `sync.Once` bundle.

**NEVER** add `tenant_id`, `user.id`, `password`, `token`, `api_key`, or `secret`
to metric labels or span attributes (G38 BLOCKER — see §"Tenant attribution at
runtime" below).

## Span Conventions

- Span names: `{Service}.{Method}` (e.g., `IdentityService.CreateUser`)
- Use semconv attribute keys (`messaging.*`, `rpc.*`, `db.*`)
- Set `otel.status_code` on errors
- Use `span.RecordError(err)` for error spans

```go
ctx, span := otel.Tracer("identity-service").Start(ctx, "IdentityService.CreateUser",
    trace.WithAttributes(
        attribute.String("rpc.system", "motadata"),
        attribute.String("rpc.method", "CreateUser"),
    ),
)
defer span.End()

if err != nil {
    span.RecordError(err)
    span.SetStatus(codes.Error, err.Error())
}
```

## Tenant attribution at runtime — consumer baggage

The pipeline forbids `tenant_id` (and other sensitive keys) in pipeline-generated
SDK code (G38 BLOCKER). Tenant tagging happens at the CONSUMER's runtime via W3C
baggage propagation:

```go
// CONSUMER application code at request entry
import "go.opentelemetry.io/otel/baggage"

m, _ := baggage.NewMember("tenant_id", tid)
b, _ := baggage.New(m)
ctx = baggage.ContextWithBaggage(ctx, b)

client.Publish(ctx, topic, payload)  // SDK propagates baggage via traceparent
```

The SDK propagates baggage via `propagation.Baggage{}` automatically — it does
NOT need to know any specific keys. The OTel Collector's `baggage` processor
copies `tenant_id` from baggage onto spans at the backend boundary (Tempo,
Honeycomb, Jaeger). Backend dashboards filter by `tenant_id` without the SDK
ever emitting the attribute itself.

This is how G38 compliance works in production:
- SDK code = sensitive-key-free
- Consumer = adds via baggage at runtime
- Collector = unpacks at backend
- Backend = filters/dashboards per tenant

## Examples

### GOOD
```go
// Trace context propagated through NATS; semconv-keyed attrs only
ctx = observability.ExtractTraceContext(ctx, msg)
ctx, span := tracer.Start(ctx, "NotificationService.SendEmail",
    trace.WithAttributes(
        attribute.String("messaging.system", "motadata"),
        attribute.String("messaging.destination.name", topic),
    ),
)
defer span.End()
```

### BAD
```go
// Missing trace propagation from NATS — creates orphan spans
span := tracer.Start(context.Background(), "SendEmail")
defer span.End()

// G38 BLOCKER — sensitive key on span attribute
ctx, span := tracer.Start(ctx, "SendEmail",
    trace.WithAttributes(attribute.String("tenant_id", tid.String())),
)
```

## Common Mistakes
1. **Using `resource.Merge` with `resource.Default()`** — Causes schema URL conflicts. Use `resource.New` with explicit attributes.
2. **Forgetting NATS trace propagation** — Every NATS publish/consume MUST inject/extract trace context, otherwise traces are broken across service boundaries.
3. **Adding `tenant_id` / `user.id` / `password` / `token` to span attrs or metric labels** — G38 BLOCKER. Tenant attribution rides W3C baggage from consumer; collector unpacks at backend boundary.
4. **Not calling provider Shutdown** — Telemetry providers MUST be shut down in graceful shutdown to flush pending data.
