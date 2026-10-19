---
name: ovstorage-operator-monitor-broker
description: Use when wiring observability for a running ovstorage-broker - covers the Prometheus /metrics surface, the 11 metric families, the tracing span fields, and the audit-safe diagnostic shape.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, broker, observability]
tools: [Read, Bash]
compatibility: Requires access to broker metrics, tracing, logs, and the operator's approved observability stack.
---

# Monitor the Broker

## Goal

Wire Prometheus scraping, log aggregation, and trace consumption
against `ovstorage-broker` using its built-in surfaces. No
audit-record subsystem ships today; tracing fields are the audit
trail.

## Recipe

1. Read
   [`docs/public/broker-operator/README.md`](../../docs/public/broker-operator/README.md)
   § *Observability* for the full reference.
2. Enable Prometheus by adding
   `[observability] prometheus_bind = "HOST:PORT"` to the broker
   TOML. The broker spawns an axum listener serving
   `text/plain; version=0.0.4` exposition.
3. Scrape the listener with your Prometheus / VictoriaMetrics /
   etc. setup. Expect these 11 metric families (some are dormant
   today — registered but not yet observed):
   - `broker_rpc_seconds{op}` — RPC latency. **Dormant.**
   - `broker_cache_metadata_hits_total` — metadata-cache hits.
   - `broker_cache_object_hits_total` — object-byte-cache hits.
   - `broker_cache_object_fills_total` — object-byte-cache fills.
   - `broker_cache_evictions_total` — **dormant.**
   - `broker_authz_decisions_total{outcome}` — labels are
     `allow`, `deny`, `error`.
   - `broker_watch_fanout` (gauge) — **dormant.**
   - `broker_redirect_emissions_total{kind}` — labels are
     `read`, `write`. Increments at every fixture-driven and
     plugin-driven redirect emission site.
   - `broker_continuation_seal_refusals_total{reason}` — labels are
     `malformed`, `tag`, `mac`. All three series start at zero. `mac`
     includes wrong-key, wrong-address, and edited-envelope failures.
   - `broker_lifecycle_events_total{event}` — labels are
     `reload_ok`, `reload_failed`, `drain_start`,
     `drain_complete`.
   - `broker_uptime_seconds`.
4. Pipe `grpc.health.v1.Health/Check` to your health-check probe.
   Reports `Serving` whenever backend-kind introspection on the active
   Stack succeeds. **Readiness is not flipped during drain** (the gRPC
   server stops accepting new connections via
   `serve_with_incoming_shutdown` but `Health/Check` keeps the
   last reported state until the server thread exits).
5. Wire tracing. The broker uses
   `init_tracing_from_env` so the standard `RUST_LOG` /
   `OTEL_*` env vars apply. OTLP push as a `[observability]
   otlp_endpoint` field is reserved (surfaces `Unsupported` if
   set); layer `opentelemetry_otlp` onto `init_tracing_from_env`
   manually if you need it.

## Tracing fields to collect

Per the broker-operator persona doc:

- `principal.id` — on every object-IO span (`broker.stat`,
  `broker.read`, `broker.write`, `broker.list`,
  `broker.list_versions`, `broker.list_address_roots`).
- `policy_epoch` — on every object-IO span and every
  `pb::ErrorDetail`.
- `object.address` — redacted via `RedactedUrl` (scheme + host +
  port + path only, no query / fragment / userinfo).
- `audit_id` — on `ReadRedirect` and `WriteRedirect` envelopes
  and on every `pb::ErrorDetail`. Freshly minted when the host's
  `RequestContext.audit_id` is `None`.
- `cache.hit`, `redirect.kind` — when applicable.
- `outcome ∈ {allow, deny, error}` — on the
  `broker_authz_decisions_total` counter.

Fields **not** stamped today: `route.id` and `backend.id` on
per-RPC spans. Closing the gap is tracked.

## Audit log shape (what you don't get)

There is no `AuditRecord` / `AuditEvent` type, durable sink, or
operator-facing `explain-decision <audit-id>` tool. Diagnostic
fields land in tracing spans, error details, and redirect
envelopes only. Operators that need an audit log point a log
aggregator at the broker's tracing output and filter on
`audit_id` + `policy_epoch` + `principal.id`.

**Sinks must redact physical URLs before logging query strings or
signed headers.** The pipeline must never log raw bearer tokens,
credential bytes, or usable signed URLs.

## Suggested alerts

- `rate(broker_lifecycle_events_total{event="reload_failed"}[5m]) > 0`
  — a SIGHUP reload failed validation; the old broker is still live
  on stale config.
- `rate(ovstorage_auth_decisions_total{outcome="error"}[5m]) > 0` —
  the built-in auth Layer returned evaluation errors (not denies). Check the
  active policy and listener authentication configuration.
- `broker_uptime_seconds` reset implies a process restart. Successful
  in-process reloads increment
  `broker_lifecycle_events_total{event="reload_ok"}` instead.
- `rate(broker_continuation_seal_refusals_total{reason="mac"}[5m]) > 0`
  — check for a mismatched shared key or an incomplete key rotation when the
  failures concentrate on part of a replica fleet. Address substitution and
  continuation edits produce the same reason.
- `rate(broker_redirect_emissions_total{kind="write"}[5m])` falling
  to zero on a route that previously emitted them suggests the
  plugin can no longer mint redirects (and the broker is falling
  back to inline upload, which has the 64 MiB
  `WRITE_BODY_BYTE_CAP`).

## References

- [`docs/public/broker-operator/README.md`](../../docs/public/broker-operator/README.md)
  § Observability — the full reference.
- [`ovstorage-operator-debug-broker`](../ovstorage-operator-debug-broker/SKILL.md) —
  using these surfaces to triage runtime issues.
- [`ovstorage-operator-configure-broker-policy`](../ovstorage-operator-configure-broker-policy/SKILL.md)
  — interpreting `broker_authz_decisions_total{outcome="deny"}`.
