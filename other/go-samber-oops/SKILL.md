---
name: go-samber-oops
description: "Structured error handling in Go with samber/oops. Covers stack traces, error codes, and contextual metadata."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 07:15:00 GMT
---

## Core Philosophy

`samber/oops` is a library that treats errors as **structured data** rather than just strings. It allows you to attach context (stack traces, domains, user IDs, request IDs) to errors as they propagate up the call stack.

- **Stack Traces**: Automatically captures the call stack where the error was created.
- **Error Codes**: Machine-readable slugs for client-side error handling.
- **Contextual Metadata**: Attach key-value pairs (e.g., `user_id`, `query_id`) to the error.
- **User-Facing Messages**: Separate technical error details from friendly messages intended for the end-user.

## Basic Usage

### Creating and Wrapping Errors
```go
// Create a new error with context
return oops.
    In("user-service").
    Code("not_found").
    With("user_id", id).
    Errorf("user not found")

// Wrap an existing error
if err != nil {
    return oops.Wrapf(err, "failed to fetch user")
}
```

### Adding Metadata
| Builder Method | Purpose |
| --- | --- |
| `.In(domain)` | Set the domain or layer (e.g., "db", "api"). |
| `.Code(code)` | Set a machine-readable error code. |
| `.With(key, val)` | Attach custom metadata. |
| `.User(id)` | Attach the ID of the affected user. |
| `.Public(msg)` | Set a safe, user-facing error message. |
| `.Hint(msg)` | Provide a hint for developers (e.g., "check db connection"). |

## Advanced Patterns

### Panic Recovery
Convert a panic into a structured `oops` error:
```go
func RiskyOperation() (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = oops.
                Code("panic_recovered").
                With("panic", r).
                Errorf("operation panicked")
        }
    }()
    // ...
}
```

### Context Propagation
You can store an `oops.Builder` in a `context.Context` and use it later:
```go
ctx := oops.WithBuilder(ctx, oops.In("api").Trace(traceID))

// Later in a nested call
return oops.FromContext(ctx).Wrapf(err, "call failed")
```

## Why use `oops`?

- **Better Observability**: When logged, `oops` errors provide a complete picture of why and where the failure happened.
- **Clean APM Data**: Use error codes and domains to group and alert on errors effectively in tools like Sentry or Datadog.
- **Improved UX**: Easily provide clear, safe error messages to end-users without exposing internal system details.

## Anti-patterns

- ❌ **Variable Data in Message** — Don't do `Errorf("user %s not found", id)`. Use `.With("user_id", id).Errorf("user not found")`. This allows log aggregators to group the errors correctly.
- ❌ **Ignoring `oops.Wrap`** — Passing a raw error up the stack loses the stack trace and context provided by `oops`.
- ❌ **Leaking Technical Details** — Avoid putting SQL queries or internal paths in the message. Put them in `.With()` metadata and use `.Public()` for the user.
- ❌ **Redundant Wrapping** — Only wrap an error when you have meaningful context to add at that specific layer.
