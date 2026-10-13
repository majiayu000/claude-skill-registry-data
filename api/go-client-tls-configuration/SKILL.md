---
name: go-client-tls-configuration
description: >
  Use this when wiring tls.Config into a new SDK client that dials a remote
  endpoint — TLS 1.2 floor (1.3 preferred), SNI ServerName required, mTLS via
  LoadX509KeyPair, custom CA layered on x509.SystemCertPool, and ErrTLS
  sentinel wrapping. Covers Mozilla / CIS / NIST guidance.
  Triggers: tls.Config, MinVersion, RootCAs, ServerName, InsecureSkipVerify, x509.SystemCertPool, LoadX509KeyPair.
---

# go-client-tls-configuration (v1.0.0)

## Rationale

TLS is the SDK's only defence against MITM on the wire. Misconfiguration is
silent (certs still verify, handshake still completes) until the day an old
cipher or forged chain is used against production. The SDK therefore commits
to a **floor of TLS 1.2** (Mozilla "intermediate" / CIS Benchmark for legacy
systems), with **TLS 1.3 preferred** for any new deployment. SSL 3.0 / TLS
1.0 / TLS 1.1 are forbidden — they are explicitly deprecated by IETF (RFC
8996) and disallowed by Mozilla "modern" config.

Every TLS-speaking client in the SDK MUST:

1. Set `tls.Config.MinVersion` to at least `tls.VersionTLS12`.
2. Populate `ServerName` (SNI) unless `InsecureSkipVerify` is deliberately set (and the validator MUST warn when it is).
3. Trust the OS system pool first (`x509.SystemCertPool`) and layer custom CA bytes on top via `AppendCertsFromPEM`.
4. Load client certs (mTLS) via `tls.LoadX509KeyPair`, never by passing PEM bytes inline.
5. Wrap any TLS error in a package-local sentinel (e.g. `ErrTLS`) so callers can `errors.Is` cleanly.

The target SDK's `core/l2cache/dragonfly` package is the reference:
`config.go` sets `MinVersion = tls.VersionTLS12` by default and `tls.go`
builds the cert pool by seeding from the OS store and appending the custom CA.

## Activation signals

- New client dials a remote endpoint over TCP that could be TLS
- TPRD §Skills-Manifest lists `go-client-tls-configuration`
- Security-devil flags TLS defaults
- Config struct gains a `TLS *TLSConfig` field

## GOOD examples

### 1. Default TLS 1.2 floor with the reference shape

From `core/l2cache/dragonfly/config.go`:

```go
type TLSConfig struct {
    CertFile   string // mTLS client cert
    KeyFile    string // mTLS client key
    CAFile     string // custom CA bundle
    ServerName string // SNI; required unless SkipVerify
    SkipVerify bool   // prod-unsafe; validator warns
    MinVersion uint16 // defaults to tls.VersionTLS12
}

func (c *Config) applyDefaults() {
    // ... other defaults ...
    if c.TLS != nil && c.TLS.MinVersion == 0 {
        c.TLS.MinVersion = tls.VersionTLS12
    }
}

func (c *Config) validate() error {
    if c.TLS != nil && c.TLS.ServerName == "" && !c.TLS.SkipVerify {
        return fmt.Errorf("%w: TLS.ServerName required unless SkipVerify", ErrInvalidConfig)
    }
    return nil
}
```

### 2. Layered CA pool: OS roots + custom bytes

From `core/l2cache/dragonfly/tls.go`:

```go
// systemCertPoolWithExtra returns a *x509.CertPool seeded from the OS
// store plus any extra PEM bytes. If system pool load fails, builds an
// empty pool and appends. Never returns nil pool with nil err.
func systemCertPoolWithExtra(extraPEM []byte) (*x509.CertPool, error) {
    pool, err := x509.SystemCertPool()
    if err != nil || pool == nil {
        pool = x509.NewCertPool()
    }
    if len(extraPEM) == 0 {
        return pool, nil
    }
    if !pool.AppendCertsFromPEM(extraPEM) {
        return nil, fmt.Errorf("no PEM certificates parsed")
    }
    return pool, nil
}
```

### 3. Building `*tls.Config` with mTLS and error wrapping

```go
func (c *Config) tlsClientConfig() (*tls.Config, error) {
    if c.TLS == nil {
        return nil, nil
    }
    t := c.TLS

    out := &tls.Config{
        ServerName:         t.ServerName,
        InsecureSkipVerify: t.SkipVerify, // false by default
        MinVersion:         t.MinVersion, // already defaulted to TLS12
    }
    if out.MinVersion == 0 {
        out.MinVersion = tls.VersionTLS12 // belt + braces
    }

    if t.CertFile != "" && t.KeyFile != "" {
        cert, err := tls.LoadX509KeyPair(t.CertFile, t.KeyFile)
        if err != nil {
            return nil, fmt.Errorf("%w: load client cert: %v", ErrTLS, err)
        }
        out.Certificates = []tls.Certificate{cert}
    }

    if t.CAFile != "" {
        caPEM, err := os.ReadFile(t.CAFile)
        if err != nil {
            return nil, fmt.Errorf("%w: read CA file: %v", ErrTLS, err)
        }
        pool, err := systemCertPoolWithExtra(caPEM)
        if err != nil {
            return nil, fmt.Errorf("%w: build cert pool: %v", ErrTLS, err)
        }
        out.RootCAs = pool
    }
    return out, nil
}
```

## BAD examples

### 1. `InsecureSkipVerify: true` in defaults

```go
// BAD: security-devil BLOCKER. Ships MITM-vulnerable client.
return &tls.Config{InsecureSkipVerify: true}
```

### 2. Omitting MinVersion (defaults to TLS 1.0 in older Go; even stdlib
moved floor to 1.2 in Go 1.20+, but relying on default is fragile)

```go
// BAD: silent TLS 1.0/1.1 acceptance on old runtimes.
return &tls.Config{ServerName: "api.example.com"}
```

### 3. Replacing the system pool instead of layering

```go
// BAD: a single custom CA now means the client no longer trusts
// Let's Encrypt, DigiCert, etc. for unrelated endpoints.
pool := x509.NewCertPool()
pool.AppendCertsFromPEM(customCA)
return &tls.Config{RootCAs: pool} // ← throws away OS trust
```

Correct: seed from `x509.SystemCertPool()`, then append.

## Decision criteria

| Question | Answer |
|---|---|
| Minimum TLS version | `tls.VersionTLS12` (floor); prefer `tls.VersionTLS13` for new deployments |
| Cipher suites | Do NOT set — Go's defaults are curated. Setting `CipherSuites` is for experts; misconfig silently weakens. |
| ServerName empty? | Reject in `Config.validate()` unless `SkipVerify` is set. |
| `SkipVerify` allowed? | Only behind an explicit opt-in field; emit a WARN on every call that sets it. |
| Custom CA? | Layer on `x509.SystemCertPool()` — do not replace. |
| mTLS? | `tls.LoadX509KeyPair(certFile, keyFile)` — files, not inline bytes. |
| Credential refresh? | Set `ConnMaxLifetime` on the pool so rotated K8s-secret-mounted certs are re-read on redial. |

Reference configs:

- **Mozilla TLS Configurator** — "intermediate" profile: TLS 1.2 + 1.3; "modern": TLS 1.3 only.
- **CIS Benchmark** — disable SSL/TLS <1.2 on all services.
- **NIST SP 800-52 Rev 2** — TLS 1.2 minimum, TLS 1.3 preferred for US-federal.

## Cross-references

- `go-credential-provider-pattern` — cert rotation via file watch + `ConnMaxLifetime`
- `network-error-classification` — `ErrTLS` sentinel; `tls.CertificateVerificationError` / `x509.UnknownAuthorityError` typed checks
- `environment-prerequisites-check` — CI job to `openssl s_client -tls1_2` smoke
- `go-sdk-config-struct-pattern` — `TLSConfig` nested struct shape

## Guardrail hooks

- **G69.sh** — no hardcoded keys / certs in source (blocks inline PEM)
- **G48.sh** — no `init()` registering a shared `*tls.Config`
- **G98/G99** — TLS-touching symbols must carry `[traces-to:]` markers
- Devil: `sdk-security-devil` — BLOCKER on `InsecureSkipVerify: true` default, missing ServerName, missing MinVersion, replaced (not layered) cert pool
