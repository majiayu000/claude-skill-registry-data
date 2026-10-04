---
name: zerolog-observability
category: observability
description: Use when adding logging to Go code - the repository's logger with structured fields, request-scoped correlation, correct levels, no secrets or double-logging
tech_stack: Go
source: samber/cc-skills-golang (MIT), uber-go/guide (Apache-2.0), adapted
---
# Structured Logging (Go)

## Overview

Logs are for machines first: structured fields you can filter and correlate, not prose. The recurring defects are `fmt.Println` debugging left in, data interpolated into the message instead of fields, the same error logged at every layer, and secrets leaking into logs.

**Core principle:** log the failure at its site, with fields, once — and use the repository's own logger.

## Which logger

Follow the repository's existing logger: `github.com/rs/zerolog`, `log/slog` (stdlib), or `go.uber.org/zap` all give structured fields and are fine to continue. Use zerolog only when the repo has no logger yet. Never introduce a second logging library alongside one the repo already uses (rule repo-conventions-win). Never `fmt.Println` / `log.Printf` in production code regardless of which structured logger the repo picked.

## Rules

- **Fields, not interpolation:** ids and operation names are structured fields, not baked into the message string.
- **Correlate with a request-scoped logger**, not the global one. Middleware attaches `request_id` (and relevant entity ids) once and puts the enriched logger in the request's context; handlers and services pull it back out instead of re-adding the id everywhere:

  ```go
  // middleware, once per request
  l := log.With().Str("request_id", reqID).Logger()
  c.SetUserContext(l.WithContext(c.UserContext()))

  // anywhere downstream
  zerolog.Ctx(ctx).Error().Err(err).Str("task_id", id.String()).Msg("dispatch failed")
  ```
  (`slog`: `slog.Default().With("request_id", reqID)` carried the same way via context, or a custom `Handler`.)
- **Handle errors once (samber "single handling rule" / Uber "Handle Errors Once"):** an error is either logged OR returned/wrapped, never both. Log-and-return at every layer reports the same failure N times. Log at the site that has the most context (usually where it's finally handled, e.g. the HTTP error mapper), propagate elsewhere with `%w` and say nothing.
- **Never log secrets, tokens, full request bodies, or other PII** that may carry user data. Treat user-supplied strings as values only — never splice them into the message template (log injection: a user-controlled newline or field name can forge log entries).

## Levels

| Level | Use for |
|-------|---------|
| Debug | development detail, verbose tracing |
| Info | state changes worth auditing (task moved, migration applied) |
| Warn | handled anomaly (retry, fallback taken) |
| Error | a failure needing attention |

## Worked Example

```go
// ❌ prose message, interpolated id, will be logged again by the caller too
log.Error().Msg(fmt.Sprintf("dispatch failed for task %s: %v", id, err))

// ✅ structured fields, error attached, logged once at the handling site, request-scoped logger
zerolog.Ctx(ctx).Error().
    Err(err).
    Str("task_id", id.String()).
    Str("op", "dispatch").
    Msg("dispatch failed")
// upstream callers propagate with fmt.Errorf("dispatch: %w", err) — they do NOT re-log
```

Now a query like `op="dispatch" level="error"` finds every dispatch failure with its task id and request id, and each failure appears exactly once.

## Java

Follow the repo's existing setup: SLF4J (with JBoss Logging or Logback underneath) using MDC for `request_id` and other correlation fields; Spring Boot's built-in structured logging (`logging.structured.format.console=ecs`, 3.4+); or Quarkus's `quarkus-logging-json` extension. The same rules apply — fields not string concatenation, handle once, never log secrets.

## Common Mistakes

- `fmt.Println`/`log.Printf` left in production paths.
- `Msg(fmt.Sprintf(...))` interpolating ids instead of `.Str(...)` fields.
- The same error logged in the repo, the service, AND the handler.
- Logging a token, password, or full request body.
- Reading `request_id` from a global/package variable instead of the request-scoped context logger.
- Everything at Info (or everything at Error) — levels lose meaning.

## Red Flags

- A message string with `%s`/`+id` inside it.
- The same failure appears three times in the logs for one request.
- A secret or auth header value in a log line.
- User input spliced directly into a log message template rather than passed as a field value.
