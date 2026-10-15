---
name: Endpoint Check
description: HTTP probe (status + latency) and TLS certificate inspection (expiry, issuer, SANs).
requires:
  bins: []
  env: []
---

# Endpoint Check

Use when the user wants to verify that an HTTP endpoint is alive, measure
its latency, or inspect a TLS certificate's expiry and issuer. Combines
naturally with Phase 7 heartbeat for periodic monitoring.

## Use when

- "Is my API up?"
- "How long until cert X expires?"
- "Check my endpoints and alert me if something fails" (pair with heartbeat)
- Verify that a deployment published new code (compare response body)

## Do not use when

- You need complex auth (OAuth, mTLS) — use `fetch-url` or a dedicated extension
- You need full body download — use `fetch-url`
- It is an internal container health check — use the orchestrator-native check

## Tools

### `status`
No args. Info + limits.

### `http_probe { url, method?, timeout_secs?, follow_redirects?, expected_status? }`
- `url` required (http/https)
- `method` GET (default) or HEAD
- `timeout_secs` 1..60 (default 10)
- `follow_redirects` default true
- `expected_status` optional: returns `matches_expected: bool`

Returns `{status, latency_ms, final_url, content_type, body_preview (≤500 chars), [matches_expected]}`.

### `ssl_cert { host, port?, timeout_secs?, warn_days? }`
- `host` required
- `port` default 443
- `timeout_secs` 1..60 (default 10)
- `warn_days` default 30 — sets `expiring_soon: true` below threshold

Returns `{subject, issuer, sans, serial_hex, signature_algorithm, chain_length, not_before_unix, not_after_unix, seconds_until_expiry, days_until_expiry, expiring_soon, expired}`.

Note: this tool **does not validate trust chains** — expired/self-signed
certs still return parsed metadata. Use `expired`/`expiring_soon` to decide.

## Execution guidance

- For periodic monitoring, combine with heartbeat: probe every N minutes
  and alert when `status` changes or `expiring_soon` flips true.
- For deploy comparisons, store baseline probe output in TaskFlow
  `state_json` and diff against new runs.
- `ssl_cert` is informational; for actionable alerts, use
  `days_until_expiry` with a stricter threshold (e.g., 14 days).
- Error `-32005` timeout means server did not reply within `timeout_secs`.
- Errors `-32060/-32061` in `ssl_cert` usually indicate DNS/TCP connect issues.
