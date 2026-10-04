---
id: cors-security
version: "1.1.0"
title: "CORS Security"
description: "Strict CORS: no wildcard with credentials, exact-match origin allowlists, sane preflight cache, minimal exposed headers. Use when generating CORS middleware or framework config, setting CORS headers in API Gateway, CloudFront, or Nginx, or reviewing a cross-origin browser-facing endpoint."
category: prevention
severity: high
applies_to:
  - "when generating CORS middleware or framework config"
  - "when wiring API Gateway / Cloud Front / Nginx CORS headers"
  - "when reviewing a cross-origin browser-facing endpoint"
languages: ["*"]
token_budget:
  minimal: 1100
  compact: 1400
  full: 2200
rules_path: "rules/"
related_skills: ["frontend-security", "api-security"]
last_updated: "2026-08-12"
sources:
  - "OWASP HTML5 Security Cheat Sheet — CORS"
  - "CWE-942 — Permissive Cross-domain Policy with Untrusted Domains"
  - "Fetch Living Standard (CORS)"
---

# CORS Security

## Rules (for AI agents)

### ALWAYS
- For any non-public endpoint, allow origins from an explicit allowlist. `*` is
  correct only when the resource is intentionally public *and* cross-origin access
  never carries credentials.
- When a cross-origin request carries credentials — the browser's credentials mode is
  `include`, meaning cookies, TLS client certificates, or browser-managed HTTP auth —
  respond with `Access-Control-Allow-Credentials: true` and a **single explicit
  origin**. On a credentialed request every CORS header loses its wildcard meaning:
  `*` in `Allow-Origin`, `Allow-Methods`, `Allow-Headers`, or `Expose-Headers` is read
  as the literal string `"*"` and the browser blocks the response. That is why
  "just set it to `*` for now" fails in a way that is hard to debug.
- Compare origins by exact match on the **serialized** origin — scheme, host, and port,
  all three. Never substring, prefix, or suffix matching: `endsWith("example.com")`
  accepts `https://example.com.evil.com`, and an unescaped `.` in
  `^https://api.example.com$` accepts `https://apiXexample.com`.
- Include `Vary: Origin` on any response whose headers depend on the request `Origin`,
  so a shared cache cannot hand one origin's `Access-Control-Allow-Origin` to another.
- Restrict `Access-Control-Allow-Methods` to the methods the endpoint accepts and
  `Access-Control-Allow-Headers` to the headers it consumes. An app-set
  `Authorization: Bearer …` header is not "credentials" in the Fetch sense — it is an
  ordinary header that must be listed in `Allow-Headers` and that triggers a preflight.
- Set a bounded `Access-Control-Max-Age` sized to the deployment; an hour to a day is a
  conservative production default. Browsers cap this value regardless of what you send,
  so a very large number buys no extra caching — it only lengthens how long a bad
  allowlist entry stays cached in clients that already fetched it.
- Source allowed origins only from operator-controlled configuration. Do not derive
  them from tenant- or user-controlled data unless an addition passes an authenticated,
  authorized, validated administrative workflow. The risk is not "stored in a
  database", it is "writable by anyone who can create a row".
- When the request `Origin` is not in the allowlist, omit `Access-Control-Allow-Origin`
  entirely. Do not fall back to a default trusted origin and do not echo the rejected
  value — a default-origin fallback silently grants every rejected caller whatever that
  default origin is allowed to do.

### NEVER
- Reflect the `Origin` header without an allowlist check
  (`Access-Control-Allow-Origin: <Origin>` for every caller). With credentials this is
  strictly worse than `*`: the browser refuses `*`, but accepts a reflected origin, so
  the misconfiguration fails open instead of closed.
- Accept the serialized `null` origin on a credentialed or sensitive endpoint. Every
  browser serializes an opaque origin to `null` — sandboxed iframes without
  `allow-same-origin`, `data:` URLs, `file://` documents, some cross-origin redirects.
  Treat any exception as a documented compatibility decision that passed security
  review.
- Allow arbitrary subdomains (`.*\.example\.com$`) without accounting for subdomain
  takeover. Exact matching does not help here: the pattern is implemented correctly and
  a dangling DNS record hands an attacker a matching origin. Pin specific subdomains;
  treat a wildcard as a decision tied to subdomain-ownership controls.
- Expose internal headers via `Access-Control-Expose-Headers`. Limit it to the minimal
  set the frontend genuinely reads.
- Use CORS as authorization. It is a *browser* policy: it does not stop curl,
  server-to-server calls, or any non-browser client. Authenticate the request.

### KNOWN FALSE POSITIVES
- Intentionally public, non-credentialed resources legitimately use
  `Access-Control-Allow-Origin: *` — open-data APIs, and static assets served for
  cross-origin reuse (fonts, images, JS on a CDN). This is the common correct case
  for `*`.
- A few integrations (Stripe.js, Plaid, Auth0) expect specific CORS headers; read the
  provider's CORS section before relaxing the baseline.

## Context (for humans)

CORS is widely misunderstood as a security control. It isn't — it's a
*relaxation* of the same-origin policy. The security control is
authentication. CORS misconfiguration matters because, when combined with
cookies or credentialed requests, it gives untrusted origins the ability
to make cross-origin requests and read the response.

Two failure modes account for most real findings: an origin check that
matches loosely (suffix or unescaped-regex matching), and a mismatch path
that falls back to reflecting or defaulting instead of omitting the header.
Both look correct in review and both fail open.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `rules/cors_safe_config.json`
- [OWASP CORS Origin Header Scrutiny](https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny).
- [CWE-942](https://cwe.mitre.org/data/definitions/942.html).
- [Fetch — CORS protocol](https://fetch.spec.whatwg.org/#http-cors-protocol).
