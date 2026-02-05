---
name: logging-standards
description: Zap logging standards for Go services. Use when writing, generating, or reviewing code that includes logging.
---

# Logging Standards

## Required Package

All logging MUST use **`go.uber.org/zap`**. Never use:
- `fmt.Print*` statements for logging
- Standard library `log.*` package
- `log/slog` package

## Logger Injection

Services and handlers receive the logger via dependency injection:

```go
type Service struct {
    logger *zap.Logger
}

func NewService(logger *zap.Logger) *Service {
    return &Service{logger: logger}
}
```

## Log Levels

| Level | Method | When to Use |
|-------|--------|-------------|
| **Debug** | `logger.Debug()` | Detailed diagnostic info, disabled in production |
| **Info** | `logger.Info()` | Normal operations, state changes, request handling |
| **Warn** | `logger.Warn()` | Unexpected but recoverable situations |
| **Error** | `logger.Error()` | Failures requiring attention, operation failed |
| **Fatal** | `logger.Fatal()` | Unrecoverable errors, exits program |

## Structured Fields

Use zap field constructors, not string interpolation:

```go
// Good - structured with typed fields
logger.Info("order processed",
    zap.String("order_id", order.ID),
    zap.String("user_id", user.ID),
    zap.Int64("amount", order.Amount),
)

// Bad - string interpolation
logger.Info(fmt.Sprintf("order %s processed for user %s", order.ID, user.ID))
```

## Zap Field Constructors

| Constructor | Use For |
|-------------|---------|
| `zap.String("key", val)` | String values |
| `zap.Int("key", val)` | Integers |
| `zap.Int64("key", val)` | 64-bit integers |
| `zap.Uint64("key", val)` | Unsigned 64-bit integers |
| `zap.Float64("key", val)` | Floating point |
| `zap.Bool("key", val)` | Booleans |
| `zap.Duration("key", val)` | `time.Duration` values |
| `zap.Time("key", val)` | `time.Time` values |
| `zap.Error(err)` | Error values (key is "error") |
| `zap.Any("key", val)` | Any type (use sparingly, prefer typed) |

## Contextual Fields

Every log entry should include relevant context:

| Context | Example Fields |
|---------|---------------|
| **Request** | `zap.String("request_id", id)`, `zap.String("method", method)` |
| **Entity** | `zap.String("order_id", id)`, `zap.Uint64("chain_id", chainID)` |
| **Operation** | `zap.String("operation", op)`, `zap.String("action", action)` |

## Error Logging

Error logs MUST include:
- The error via `zap.Error(err)`
- Enough context to debug without reproducing
- Operation that failed

```go
// Good
logger.Error("failed to process deposit",
    zap.Error(err),
    zap.String("deposit_id", deposit.ID),
    zap.String("pool_address", pool.Address),
    zap.Int64("amount", deposit.Amount),
)

// Bad - no context
logger.Error("deposit failed", zap.Error(err))
```

## Fatal Logging

Use `logger.Fatal()` only for unrecoverable startup errors:

```go
logger.Fatal("failed to connect to database", zap.Error(err))
```

## Sensitive Data

NEVER log:
- Passwords, tokens, API keys, or secrets
- Private keys or seed phrases
- Full request/response bodies with sensitive fields
- PII without proper redaction

```go
// Bad
logger.Info("user login", zap.String("password", password))
logger.Debug("request body", zap.Any("body", reqBody))

// Good
logger.Info("user login", zap.String("user_id", userID))
logger.Debug("request received", zap.Int("content_length", len(reqBody)))
```

## Review Checklist

- [ ] No `fmt.Print*` statements for logging
- [ ] No standard library `log.*` statements
- [ ] `go.uber.org/zap` used consistently
- [ ] Logger injected via `*zap.Logger` parameter
- [ ] Appropriate log levels used
- [ ] Typed zap field constructors used (not `zap.Any`)
- [ ] Contextual fields included (IDs, operation names)
- [ ] Error logs include `zap.Error(err)` and context
- [ ] No sensitive data exposure
