---
name: go-credential-provider-pattern
description: >
  Use this when an SDK client needs a password, API key, token, or mTLS cert
  that may rotate — designing a Provider interface with Get(ctx), static / K8s
  mounted-file / IAM-STS-Vault-API impls, finite ConnMaxLifetime so rotation
  propagates, and .env / .env.example test plumbing per CLAUDE.md rule 27.
  Triggers: CredentialProvider, Credentials, os.ReadFile, ConnMaxLifetime, MOTADATA_*_PASSWORD, .env, refresh, rotation.
---

# go-credential-provider-pattern (v1.0.0)

## Rationale

Credentials rotate. The SDK must not force callers to re-construct the client
every rotation, and it must not embed secrets in source. Three common sources
need to be supported with **one** abstraction:

1. **Static** (test / dev) — a `string` read once from env.
2. **Mounted file** (K8s Secret / HashiCorp Vault Agent / IAM-instance-metadata-cached-to-disk) — the file changes on rotation; the client must re-read before the next dial.
3. **IAM / STS / Vault API** (cloud-native) — credentials are minted on demand, expire every few minutes, require a refresh goroutine.

The **credential provider interface** abstracts all three behind one `Get(ctx)
(Credentials, error)` call. The SDK wires this into its dialer so each new
connection picks up the *current* creds. Rotation timeliness is bounded by
`ConnMaxLifetime` on the pool — set it to a finite value (10m in
`dragonfly`) so connections recycle on a cadence shorter than the rotation
interval.

CLAUDE.md rule 27 is binding: integration tests read from `.env.example`
(committed, fake) and `.env` (gitignored). No creds in spec / design / test
source. Guardrail G69 scans for AWS keys, GitHub PATs, PEM private keys, and
`password = "..."` literals — any hit is a BLOCKER.

## Activation signals

- Client needs a password, API key, token, or mTLS cert
- TPRD §Skills-Manifest lists `go-credential-provider-pattern`
- Design mentions IAM, STS, Vault, K8s Secret, rotation
- Security-devil flags hardcoded cred
- `ConnMaxLifetime = 0` in a Config

## GOOD examples

### 1. Minimal provider interface, static + file impls

```go
package creds

import (
    "context"
    "fmt"
    "os"
    "sync"
    "time"
)

// Credentials is the opaque payload the SDK injects into the wire call.
// Fields are deliberately minimal; richer shapes (mTLS cert bundle,
// signed-URL pair) compose by embedding.
type Credentials struct {
    Username string
    Password string
    Expires  time.Time // zero = no known expiry (static)
}

// Provider yields the current credentials. Safe for concurrent use.
// Get MUST be fast (cached) on the hot path; refresh happens out-of-band.
type Provider interface {
    Get(ctx context.Context) (Credentials, error)
}

// --- static (test/dev) ---

type Static struct{ c Credentials }

func NewStatic(user, pass string) *Static {
    return &Static{c: Credentials{Username: user, Password: pass}}
}
func (s *Static) Get(_ context.Context) (Credentials, error) { return s.c, nil }

// --- mounted file (K8s Secret / Vault Agent) ---

type FileProvider struct {
    userPath, passPath string
    mu                 sync.RWMutex
    cached             Credentials
    cachedAt           time.Time
    ttl                time.Duration // re-read after ttl
}

func NewFileProvider(userPath, passPath string, ttl time.Duration) *FileProvider {
    return &FileProvider{userPath: userPath, passPath: passPath, ttl: ttl}
}

func (f *FileProvider) Get(ctx context.Context) (Credentials, error) {
    f.mu.RLock()
    if time.Since(f.cachedAt) < f.ttl && f.cached.Username != "" {
        c := f.cached
        f.mu.RUnlock()
        return c, nil
    }
    f.mu.RUnlock()
    return f.refresh(ctx)
}

func (f *FileProvider) refresh(_ context.Context) (Credentials, error) {
    f.mu.Lock()
    defer f.mu.Unlock()
    u, err := os.ReadFile(f.userPath)
    if err != nil {
        return Credentials{}, fmt.Errorf("read username: %w", err)
    }
    p, err := os.ReadFile(f.passPath)
    if err != nil {
        return Credentials{}, fmt.Errorf("read password: %w", err)
    }
    f.cached = Credentials{Username: string(u), Password: string(p)}
    f.cachedAt = time.Now()
    return f.cached, nil
}
```

### 2. Wiring the provider through the SDK dialer

```go
type Config struct {
    Addr            string
    Credentials     creds.Provider // injected; may be nil for unauthed endpoints
    ConnMaxLifetime time.Duration  // MUST be finite so rotated creds are picked up
}

func (c *Config) applyDefaults() {
    if c.ConnMaxLifetime == 0 {
        c.ConnMaxLifetime = 10 * time.Minute // TPRD §9 floor
    }
}

// dialer is called by the pool for every new connection. It re-asks
// the provider so rotated creds propagate at ConnMaxLifetime cadence.
func (c *Client) dialer(ctx context.Context) (net.Conn, error) {
    var creds creds.Credentials
    if c.cfg.Credentials != nil {
        got, err := c.cfg.Credentials.Get(ctx)
        if err != nil {
            return nil, fmt.Errorf("%w: credentials: %v", ErrAuth, err)
        }
        creds = got
    }
    return c.dialAuth(ctx, creds) // injects on the handshake
}
```

### 3. Env-sourced config at construction (integration-test pattern)

```go
// TestMain reads .env (gitignored) and .env.example (committed, fake)
// per CLAUDE.md rule 27. No literals in source.
func TestMain(m *testing.M) {
    _ = godotenv.Load(".env", ".env.example") // .env wins
    user := os.Getenv("MOTADATA_DRAGONFLY_USERNAME")
    pass := os.Getenv("MOTADATA_DRAGONFLY_PASSWORD")
    if user == "" || pass == "" {
        fmt.Fprintln(os.Stderr, "missing MOTADATA_DRAGONFLY_* env; skipping integration")
        os.Exit(0)
    }
    os.Exit(m.Run())
}
```

## BAD examples

### 1. Password literal in source

```go
// BAD: G69 BLOCKER. Even in a test file.
cfg := dragonfly.Config{
    Addr:     "dfly.internal:6379",
    Password: "super-secret-1234", // FORBIDDEN
}
```

### 2. Password in a Config String() method / log line

```go
// BAD: leaks creds to the log aggregator.
func (c *Config) String() string {
    return fmt.Sprintf("Addr=%s User=%s Pass=%s", c.Addr, c.User, c.Password)
}
```

Fix: either don't implement `String()`, or mask (`Pass=***`).

### 3. `ConnMaxLifetime = 0` with a rotating secret

```go
// BAD: pool holds connections forever; rotated secret never picked up.
cfg := Config{
    ConnMaxLifetime: 0, // infinite — rotated K8s secret is ignored
    Credentials:     creds.NewFileProvider(userPath, passPath, time.Minute),
}
```

## Decision criteria

| Source | Provider | Refresh |
|---|---|---|
| Env var at startup | `Static` | Never (process restart) |
| K8s mounted Secret | `FileProvider` | Re-read every `ttl` (e.g. 30s); pool rotates at `ConnMaxLifetime` |
| Vault Agent sidecar | `FileProvider` | Same as K8s Secret |
| AWS IAM / STS | Custom provider with background refresh goroutine | On expiry - 60s |
| HashiCorp Vault API | Custom with lease-renewal goroutine | Before lease expiry |
| mTLS cert rotation | `FileProvider` variant returning `*tls.Certificate` | Watch dir via `fsnotify` or ttl re-read |

Rules:

- The Config struct holds a `Provider`, **never** a raw `Password string` that outlives construction. A convenience constructor may accept a string and wrap it with `NewStatic`.
- Credentials MUST NOT appear in `fmt.Sprintf`, `log.Print`, OTel span attributes, or metric labels.
- A rotating provider MUST pair with a finite `ConnMaxLifetime` (commonly 10m). A stale connection with stale creds fails on server-side ACL change.
- A refresh goroutine MUST stop on `Close()` (see `go-client-shutdown-lifecycle`).

## Cross-references

- `go-client-tls-configuration` — cert files loaded via `LoadX509KeyPair`; rotation via `ConnMaxLifetime`
- `go-client-shutdown-lifecycle` — refresh goroutine must stop on Close
- `network-error-classification` — provider errors wrap `ErrAuth`
- `environment-prerequisites-check` — CI asserts `.env.example` committed, `.env` gitignored

## Guardrail hooks

- **G69.sh** — hardcoded creds detector; BLOCKER on AWS keys, PEMs, `password = "..."`
- **G48.sh** — no `init()`; blocks "load creds in init and stash globally"
- Devil: `sdk-security-devil` — checks `InsecureSkipVerify`-analogue on creds, `Stringer` leakage, missing `ConnMaxLifetime` pairing
- Pipeline rule 27 — `.env.example` / `.env` convention enforced at intake
