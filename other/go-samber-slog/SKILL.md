---
name: go-samber-slog
description: "Advanced structured logging with samber/slog extensions. Covers handler composition, sampling, formatting, and backend routing."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 07:35:00 GMT
---

## Core Philosophy

`samber/slog` provides a collection of 20+ composable handlers and utilities for the standard Go `slog` package (introduced in Go 1.21). It allows you to build sophisticated logging pipelines with minimal boilerplate.

- **Composability**: Use `slog-multi` to combine or route logs to multiple handlers.
- **Efficiency**: Use `slog-sampling` to drop noisy logs at the source.
- **Safety**: Use `slog-formatter` to scrub PII (Personally Identifiable Information) before it leaves the process.
- **Integration**: Built-in handlers for Datadog, Sentry, Loki, Slack, and more.

## Core Libraries

| Library | Purpose |
| --- | --- |
| **`slog-multi`** | Fan-out logs to multiple sinks or route them based on level/attribute. |
| **`slog-sampling`** | Rate-limit logs to prevent overwhelming your logging backend. |
| **`slog-formatter`** | Transform log attributes (e.g., masking emails, formatting errors). |
| **`slog-http`** | Framework-specific middlewares (Gin, Echo, Fiber, Chi). |

## Pipeline Ordering (The "Golden Order")

Always order your logging pipeline as follows to minimize wasted CPU:
1. **Sampling**: Drop records early.
2. **Formatting**: Scrub/Transform attributes once.
3. **Routing/Fan-out**: Send the clean, sampled records to your sinks.

## Basic Usage

### Multi-Handler Routing
```go
// Route Errors to Sentry, everything else to JSON Stdout
logger := slog.New(
    slogmulti.Router().
        Add(sentryHandler, slogmulti.LevelIs(slog.LevelError)).
        Add(slog.NewJSONHandler(os.Stdout, nil)).
        Handler(),
)
```

### Formatting (PII Scrubbing)
```go
logger := slog.New(
    slogmulti.Pipe(
        slogformatter.NewFormatterMiddleware(
            slogformatter.PIIFormatter("email", "password"),
        ),
    ).Handler(slog.NewJSONHandler(os.Stdout, nil)),
)
```

## HTTP Middleware Example (Gin)
```go
router := gin.New()
router.Use(sloggin.New(logger))
```

## Why use `samber/slog`?

- **Standardization**: Based on the official `log/slog` package.
- **Cloud-Ready**: Native handlers for modern observability platforms.
- **Reduced Noise**: Sampling and filtering are first-class citizens.
- **Graceful Shutdown**: Handlers like `slog-datadog` support flushing buffered logs on exit.

## Best Practices

1. **Flush Batch Handlers** — Sinks like Datadog and Loki buffer logs. Always call `.Stop()` or `.Close()` on them during application shutdown.
2. **Sample Before Formatting** — Formatting is expensive; don't do it for logs you're about to drop.
3. **Use Context** — Leverage `slog.HandlerOptions.AddSource` and `slog.AttrFromContext` to inject trace IDs and request IDs automatically.
4. **Prefer `slog-multi.Pool` for Latency** — `Fanout` is sequential; `Pool` is concurrent and faster for many sinks.

## Anti-patterns

- ❌ **Sequential Fan-out with Slow Sinks** — Logging to 5 remote APIs sequentially will kill your app's performance. Use `Pool`.
- ❌ **Missing Catch-all** — A `Router` without a default handler will silently drop logs that don't match any predicate.
- ❌ **Leaking PII** — Always use a formatter to mask sensitive fields like tokens or personal data.
- ❌ **High Cardinality in Messages** — Don't put unique IDs in the log message string. Use attributes.
