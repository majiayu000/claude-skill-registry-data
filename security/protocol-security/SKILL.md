---
id: protocol-security
version: "2.0.0"
title: "Protocol Security"
description: "Transport security where the client establishes trust: TLS version floor, certificate chain and hostname verification, the trust store, connecting by IP, mTLS and workload identity as authentication, gRPC channel credentials, and SMTP STARTTLS. Use when generating HTTP, gRPC, or SMTP clients and servers, configuring TLS in code or platform config, wiring service-to-service authentication, or when tempted to disable certificate verification."
category: hardening
severity: critical
applies_to:
  - "when generating an HTTP, gRPC, or SMTP client or server"
  - "when configuring TLS in application code or platform config"
  - "when wiring service-to-service authentication"
  - "when a certificate error appears and verification is about to be disabled"
languages: ["*"]
token_budget:
  minimal: 1200
  compact: 1600
  full: 2100
rules_path: "rules/"
related_skills: ["crypto-misuse", "auth-security", "database-security", "websocket-security"]
last_updated: "2026-08-12"
sources:
  - "NIST SP 800-52 Rev. 2 (TLS Guidelines)"
  - "RFC 8446 — TLS 1.3"
  - "RFC 9110 / RFC 6125 — hostname verification"
  - "OWASP Transport Layer Security Cheat Sheet"
  - "CWE-295, CWE-319, CWE-757"
external_tools:
  - name: testssl.sh
    purpose: "live TLS/SSL endpoint configuration test (ciphers, protocols, known vulns)"
    command: "testssl.sh <host:port>"
---

# Protocol Security

## Rules (for AI agents)

### ALWAYS
- Default to **TLS 1.3**, and permit TLS 1.2 only where a peer genuinely requires it.
  Disable TLS 1.0, 1.1, and every SSL version. Cipher-suite selection is a
  consequence of the version floor rather than a separate decision —
  `references/tls-configuration.md` carries the suite lists and the per-platform
  config keys.
- Verify the full certificate chain on every connection: a trusted issuer, an
  unexpired validity window, and a hostname that matches a **`subjectAltName`
  dNSName** entry. The hostname is checked *against* the SAN — SAN is not an
  alternative place to look, and a `CN` match is not a fallback, because current
  browsers and TLS libraries removed CN as a hostname source.
- When connecting to an **IP address** rather than a name, set the expected name
  explicitly (`ServerName` in Go's `tls.Config`, the equivalent SNI/verification
  hostname elsewhere) so verification has something to check, or require a
  certificate carrying an `iPAddress` SAN. Reaching an endpoint by IP is the single
  most common reason a developer disables verification — this is the fix that keeps
  it on.
- Resolve a self-signed or internal-CA endpoint by **adding that CA to the client's
  trust configuration**, not by turning verification off. Every language has a way to
  supply a custom root pool; using it keeps hostname and expiry checks intact, which
  is exactly what the shortcut discards.
- Use **mutual TLS** for service-to-service traffic inside a trust domain, and treat
  it as what it is: a cryptographic caller identity, which *is* authentication —
  unlike network position, which is not. A SPIFFE workload identity
  (`spiffe://trust-domain/...`) with short-lived certificates is the form of this
  worth reaching for over a long-lived shared API key.
- For gRPC, build the channel with credentials: Python `grpc.secure_channel(target,
  grpc.ssl_channel_credentials())`, Go `grpc.WithTransportCredentials(
  credentials.NewTLS(cfg))`. The insecure variants exist for local development and
  say so in their names.
- For SMTP, either connect with **implicit TLS** (submissions, port 465) or issue
  `STARTTLS` on submission (port 587) and **fail if the upgrade does not happen**. An
  on-path attacker strips the server's STARTTLS advertisement and a client that
  treats TLS as opportunistic then sends credentials in plaintext without error.
  Verify the certificate after the upgrade, exactly as for any other connection.
- Track certificate expiry and automate renewal. An expired certificate is among the
  most common real transport incidents, and the pressure it creates is what produces
  the `InsecureSkipVerify` that outlives it.
- Consult `frontend-security` for HSTS and the browser response-header set,
  `websocket-security` for `Origin` validation and handshake authentication,
  `database-security` for database transport, and `mobile-security` before adding
  certificate pinning — that skill owns the rotation planning that decides whether a
  pin is a control or a future outage.

### NEVER
- Disable certificate verification: `InsecureSkipVerify: true`, `verify=False`,
  `rejectUnauthorized: false`, `CURLOPT_SSL_VERIFYPEER=0`,
  `NODE_TLS_REJECT_UNAUTHORIZED=0`, `OpenSSL::SSL::VERIFY_NONE`. Each of these turns
  off chain, expiry, and hostname checking together, which is why "just to get past
  this one certificate error" removes three controls rather than one.
- Implement a custom trust callback that accepts everything — an `X509TrustManager`
  with an empty `checkServerTrusted`, a `HostnameVerifier` returning `true`, a
  `URLSessionDelegate` that trusts any challenge, a
  `ServerCertificateValidationCallback` returning `true`. These are the same defect
  as the flag above, written so a reviewer has to read the body to see it.
- Send credentials, tokens, or session material over plaintext — including on a
  private network, where an internal foothold or a co-tenant reads it.
- Use `grpc.insecure_channel(...)` or `insecure.NewCredentials()` in production.

### KNOWN FALSE POSITIVES
- A test that runs against a localhost ephemeral certificate may pin a custom root or
  skip verification, provided the code path cannot be reached by a production build.
  The finding is a dev shortcut that ships, not the existence of the test.
- Pinning `MinVersion` to TLS 1.2 is correct where a named peer requires it and the
  reason is recorded. What is not correct is a 1.2 floor with no such peer, which is
  the version this skill's default rules out.
- A client that supplies its own root CA pool is doing verification, not bypassing
  it — the finding is an empty or always-true trust callback, not a non-system trust
  store.
- A plaintext listener that exists only to redirect to HTTPS is expected. The finding
  is a plaintext listener that serves content.

## Context (for humans)

Transport security fails in a characteristic way: not because someone chose a weak
cipher, but because verification was switched off to make something work. The
sequence is almost always the same — a self-signed certificate in staging, an
endpoint reached by IP, a certificate that expired on a Friday — and the fastest fix
is a flag that disables chain, expiry, and hostname checking at once. That flag then
survives into production, where it converts every network path into a trusted one.

So the rules above spend more effort on the alternatives than on the prohibition.
Supplying a custom root pool, setting an explicit `ServerName`, automating renewal:
each of these is the thing that should have been reachable at the moment someone
typed `InsecureSkipVerify`.

The second theme is that a cryptographic identity is authentication and a network
location is not. mTLS and SPIFFE give a caller a verifiable name; a private subnet
gives it an address. Several skills in this library reject "internal only" as a
control — this is the skill that generates the code which replaces it.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/tls-configuration.md` — cipher suites per version, per-language client
  configuration, platform config keys (nginx, Envoy, cloud load balancers), custom
  trust stores, SMTP specifics, and certificate renewal
- `rules/tls_defaults.json`
- `rules/cert_validation_sinks.json`
- [NIST SP 800-52 Rev. 2](https://csrc.nist.gov/pubs/sp/800/52/r2/final).
- [RFC 8446 — TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446).
- [CWE-295](https://cwe.mitre.org/data/definitions/295.html) · [CWE-319](https://cwe.mitre.org/data/definitions/319.html).
