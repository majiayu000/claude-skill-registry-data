---
name: network-error-classification
description: >
  Use this when an SDK client returns errors from a wire call and callers need
  to know whether to retry, fail-fast, or re-auth — building the sentinel
  taxonomy (retriable / fatal / auth-failure), the mapErr precedence ladder,
  and chaining the original cause through the language's wrapping idiom.
  Cross-language; pairs language-pack realizations.
  Triggers: sentinel, mapErr, classify, retriable, fatal, auth-failure, ErrTimeout, ErrAuth, ErrUnavailable, TLS, PoolError, PoolTimeout, asyncio.TimeoutError, raise from.
version: 1.1.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [errors, taxonomy, sdk, cross-language]
cross_language_ok: true
---

<!-- This skill is intentionally cross-language: the body shows side-by-side Go and Python realizations of the same taxonomy. The leakage scripts honor `cross_language_ok: true` and skip strict scanning. See README in /sanitize-tools/. -->


# network-error-classification (v1.1.0)

## Rationale

Every SDK client returns errors from a wire call. Callers need to know, from the error alone, whether to: **retry** (transient), **fail-fast** (fatal / programmer error), or **re-auth** (credentials no longer valid). Without a taxonomy, callers string-match on the error message — fragile, breaks on dependency upgrades.

The SDK commits to a sentinel-based taxonomy at minimum three classes:

1. **Retriable / transient** — timeout, unavailable, pool exhausted, pool closed. Safe to retry with backoff (subject to idempotency).
2. **Fatal / permanent** — invalid config, wrong type, syntax error, out of range, not connected. Retrying is useless; the caller or the data is wrong.
3. **Auth-failure** — auth failed, no permission, TLS verification failure. Retrying won't help; the caller must rotate credentials or fix the cert chain.

Classification happens at the adapter boundary via a `mapErr(err) → typed-error` helper. It chains every return value through the language's error-wrapping idiom so callers can use the language's typed-discrimination idiom AND the original cause survives for logs.

## Sentinel catalog (language-neutral)

A new SDK client should declare at minimum the following sentinels (concrete names per pack):

| Intent | Class |
|---|---|
| `Timeout` | retriable |
| `Unavailable` | retriable |
| `PoolExhausted` | retriable |
| `PoolClosed` | retriable (transient) or fatal (caller-initiated) |
| `InvalidConfig` | fatal |
| `NotConnected` | fatal |
| `WrongType` | fatal |
| `Syntax` | fatal |
| `Canceled` | fatal (caller-driven) |
| `NotFound` (or "Nil") | fatal — caller decides whether "miss" is an error |
| `Auth` | auth-failure |
| `NoPerm` | auth-failure |
| `TLS` | auth-failure |

Exact names follow each language's idioms — see Go and Python realizations below.

## Decision criteria (language-neutral)

| Category | Default sentinel | Retry? |
|---|---|---|
| Caller deadline exceeded | `Timeout` | Yes, fresh deadline |
| Caller cancellation | `Canceled` | No — caller asked to stop |
| Network read/write timeout | `Timeout` | Yes |
| TLS certificate verification | `TLS` | No — rotate creds |
| Server "auth-failed" wire response | `Auth` | No — re-auth |
| Server "no-permission" wire response | `NoPerm` | No — fix ACL |
| Pool acquire timeout | `PoolExhausted` | Yes — backoff |
| Closed pool | `PoolClosed` | No — client closed |
| Unclassified wire error | `Unavailable` | Yes, with caution |
| Config validation | `InvalidConfig` | No |

Precedence rules:

1. **Check sentinel identity before message string.** Short-circuits double-wrapping.
2. **Use typed checks for stdlib error types.** Whatever the language's "match by type" idiom is — Go's `errors.As`, Python's `isinstance`.
3. **String scan is LAST.** Server wire-protocol strings only checked after typed checks fail.
4. **Sentinel set is semver-public.** Adding is minor; removing or renaming is major. Document the set in package docs.

## Go realization

Sentinels as package-level `var ErrX = errors.New(...)`. Caller uses `errors.Is`. Pattern from `core/l2cache/dragonfly/errors.go`:

```go
var (
    // Retriable
    ErrTimeout       = errors.New("dragonfly: timeout")
    ErrUnavailable   = errors.New("dragonfly: unavailable")
    ErrPoolExhausted = errors.New("dragonfly: pool exhausted")
    // Fatal
    ErrInvalidConfig = errors.New("dragonfly: invalid config")
    ErrNotConnected  = errors.New("dragonfly: not connected")
    // Auth-failure
    ErrAuth = errors.New("dragonfly: auth failed")
    ErrTLS  = errors.New("dragonfly: tls failure")
)

func mapErr(err error) error {
    if err == nil { return nil }
    switch {
    case errors.Is(err, context.Canceled):
        return fmt.Errorf("%w: %v", ErrCanceled, err)
    case errors.Is(err, context.DeadlineExceeded):
        return fmt.Errorf("%w: %v", ErrTimeout, err)
    }
    var ne net.Error
    if errors.As(err, &ne) && ne.Timeout() {
        return fmt.Errorf("%w: %v", ErrTimeout, err)
    }
    var certErr *tls.CertificateVerificationError
    if errors.As(err, &certErr) {
        return fmt.Errorf("%w: %v", ErrTLS, err)
    }
    return fmt.Errorf("%w: %v", ErrUnavailable, err)
}

// Caller side
v, err := cache.Get(ctx, "k")
if errors.Is(err, dragonfly.ErrTimeout) {
    return retryWithBackoff(ctx, cache, "k")
}
```

Wrap with `%w` (not `%v`) so identity check traverses the chain. See `go-error-handling-patterns` for fuller wrapping discipline.

## Python realization

Exception class hierarchy under a single SDK base. Caller uses `isinstance` or `try/except`:

```python
class MotadataError(Exception):
    """Base for all SDK exceptions."""

# Retriable
class NetworkError(MotadataError): pass
class TimeoutError(NetworkError): pass
class PoolExhaustedError(NetworkError): pass

# Fatal
class ValidationError(MotadataError): pass
class NotConnectedError(MotadataError): pass

# Auth
class AuthError(MotadataError): pass
class TLSError(AuthError): pass

def map_exc(exc: BaseException) -> MotadataError:
    if isinstance(exc, asyncio.CancelledError):
        raise  # never wrap cancellation
    if isinstance(exc, asyncio.TimeoutError):
        return TimeoutError("network timeout") from exc
    if isinstance(exc, ssl.SSLCertVerificationError):
        return TLSError("certificate verification failed") from exc
    if isinstance(exc, ConnectionError):
        return NetworkError("network failure") from exc
    return MotadataError("unclassified") from exc

# Caller side
try:
    v = await cache.get("k")
except TimeoutError:
    return await retry_with_backoff(cache, "k")
except AuthError:
    raise  # rotate creds, don't retry
```

Use `raise X from y` (not bare `raise X`) so `__cause__` preserves the original. See `python-exception-patterns` for fuller chaining discipline.

## Universal anti-patterns

1. **Wrong wrapping verb.** `%v` instead of `%w` (Go) or no `from` clause (Python) breaks the cause chain.
2. **Ad-hoc error types per call site.** Every adapter defines its own — callers can't compose. Use the shared taxonomy.
3. **String matching the message.** Fragile to dependency upgrades. Map to a sentinel in `mapErr` / `map_exc`, then caller uses typed checks.

## Cross-references

- shared-core `idempotent-retry-safety` — which sentinels are retriable
- `go-error-handling-patterns` — `fmt.Errorf %w` chain, sentinel definition discipline
- `python-exception-patterns` — `raise from` chaining, `__cause__` walk
- `go-client-tls-configuration` / `python-client-tls-configuration` — TLS sentinel pairing
- `go-credential-provider-pattern` / `python-credential-provider-pattern` — Auth sentinel triggers provider refresh
