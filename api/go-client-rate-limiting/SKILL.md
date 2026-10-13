---
name: go-client-rate-limiting
description: >
  Use this when an SDK client calls a remote API with documented rate limits
  (HTTP 429, gRPC RESOURCE_EXHAUSTED) and needs token-bucket pacing,
  Retry-After honouring, and per-method vs per-client scope decisions.
  Covers golang.org/x/time/rate, ctx-aware Wait, and adaptive shaping.
  Triggers: rate.Limiter, token bucket, leaky bucket, Retry-After, rate.NewLimiter, Wait(ctx), Allow().
---

# go-client-rate-limiting (v1.0.0)

## Rationale

Client-side rate limiting protects **both sides** of the wire: the server from
misconfigured clients that burst past capacity, and the client from wasting its
own tail-latency budget on requests the server will 429 anyway. The standard
Go tool is `golang.org/x/time/rate` (a token-bucket limiter). It is lock-free
on the fast path, supports bursts, and composes with `context.Context` via
`Limiter.Wait(ctx)`.

Two bucket shapes exist: **token bucket** (x/time/rate — fills at rate r, burst
b, Allow() non-blocking, Wait() blocks until token) and **leaky bucket**
(smooths at a fixed drain rate — strictly stricter, almost always unnecessary).
Default to token bucket unless a spec names leaky bucket specifically.

An **adaptive** limiter adjusts its rate based on server feedback:
`Retry-After` header on 429, quota-remaining headers (e.g. `X-RateLimit-*`), or
repeated timeouts. The SDK must honour `Retry-After` as a floor (sleep at
least that long) before re-dispatching. Without adaptation, a statically-tuned
client will thrash against a throttled server.

## Activation signals

- TPRD §Skills-Manifest lists `go-client-rate-limiting`
- Client calls a remote API with documented rate limits (HTTP 429, gRPC RESOURCE_EXHAUSTED)
- Design mentions "burst", "quota", "throttle", "Retry-After"
- Reviewer flags unbounded request fan-out

## GOOD examples

### 1. Per-client token bucket with context-aware Wait

```go
import "golang.org/x/time/rate"

type Client struct {
    limiter *rate.Limiter
    hc      *http.Client
}

// New returns a client limited to rps requests/sec with burst capacity.
// rps=10, burst=20 → steady 10/s, allows a 20-request spike.
func New(rps float64, burst int) *Client {
    return &Client{
        limiter: rate.NewLimiter(rate.Limit(rps), burst),
        hc:      &http.Client{Timeout: 5 * time.Second},
    }
}

func (c *Client) Do(ctx context.Context, req *http.Request) (*http.Response, error) {
    if err := c.limiter.Wait(ctx); err != nil {
        return nil, fmt.Errorf("rate limit wait: %w", err) // ctx.Err()
    }
    return c.hc.Do(req.WithContext(ctx))
}
```

### 2. Adaptive shaping from Retry-After

```go
// onThrottle is invoked when the server responds 429. It parses
// Retry-After (seconds OR HTTP-date) and blocks the limiter for that
// duration by temporarily lowering the rate.
func (c *Client) onThrottle(resp *http.Response) time.Duration {
    ra := resp.Header.Get("Retry-After")
    if ra == "" {
        return 0
    }
    // RFC 7231: delta-seconds | HTTP-date.
    if secs, err := strconv.Atoi(ra); err == nil && secs >= 0 {
        return time.Duration(secs) * time.Second
    }
    if t, err := http.ParseTime(ra); err == nil {
        if d := time.Until(t); d > 0 {
            return d
        }
    }
    return 0
}

// Reserve a slot that will not be released until after `wait`.
func (c *Client) backoff(ctx context.Context, wait time.Duration) error {
    if wait <= 0 {
        return nil
    }
    t := time.NewTimer(wait)
    defer t.Stop()
    select {
    case <-ctx.Done():
        return ctx.Err()
    case <-t.C:
        return nil
    }
}
```

### 3. Per-method scoping when endpoints have different limits

```go
type Client struct {
    readLim  *rate.Limiter // 100/s read
    writeLim *rate.Limiter // 10/s  write
}

func (c *Client) Get(ctx context.Context, id string) (*Item, error) {
    if err := c.readLim.Wait(ctx); err != nil { return nil, err }
    return c.get(ctx, id)
}

func (c *Client) Put(ctx context.Context, it *Item) error {
    if err := c.writeLim.Wait(ctx); err != nil { return err }
    return c.put(ctx, it)
}
```

## BAD examples

### 1. `time.Sleep` without context cancellation

```go
// BAD: blocks even after ctx is done; leaks on shutdown.
func (c *Client) Do(ctx context.Context, req *http.Request) (*http.Response, error) {
    time.Sleep(c.minGap) // DO NOT DO THIS
    return c.hc.Do(req)
}
```

### 2. Ignoring Retry-After and retrying immediately

```go
// BAD: server said "wait 30s"; client retries in 10ms; gets 429 forever.
if resp.StatusCode == 429 {
    return c.Do(ctx, req) // no backoff, no Retry-After read
}
```

### 3. A shared global `rate.Limiter` behind `init()`

```go
// BAD: global mutable state; can't test; can't per-tenant scope;
// violates "no init()" rule.
var globalLim *rate.Limiter
func init() { globalLim = rate.NewLimiter(100, 200) } // FORBIDDEN
```

## Decision criteria

| Situation | Choice |
|---|---|
| Remote API has documented RPS | `rate.NewLimiter(rate.Limit(rps), burst)` on the client |
| Server returns `Retry-After` | Parse and honour as minimum wait |
| Different endpoint costs (read vs write, cheap vs expensive) | One limiter per endpoint class |
| Caller already rate-limits upstream | Skip SDK limiter (document as caller responsibility) |
| Need strictly uniform spacing (no burst) | Token bucket with `burst=1` (still x/time/rate; leaky bucket rarely needed) |
| Goroutine-fan-out pattern | Share the limiter; `rate.Limiter` is safe for concurrent use |

Do not put a rate limiter "just in case" on every SDK client. Add it only when
a TPRD, a devil review, or a known downstream limit motivates it. An
unnecessary limiter hides concurrency bugs and adds one goroutine-wake per
call.

## Cross-references

- `idempotent-retry-safety` — retry only idempotent ops; Retry-After gates retries
- `go-context-deadline-patterns` — `limiter.Wait(ctx)` honours deadlines
- `network-error-classification` — 429 maps to a retriable sentinel
- `go-backpressure-flow-control` — token bucket is one form of backpressure

## Guardrail hooks

- **G48.sh** — no `init()`; blocks global limiter anti-pattern
- **G63.sh** — `-race` catches unsynchronised limiter state
- **G38** family — sentinel for `ErrRateLimited` must exist if SDK surfaces 429 back to caller
- Devil: `sdk-api-ergonomics-devil-go` — unbounded fan-out finding
