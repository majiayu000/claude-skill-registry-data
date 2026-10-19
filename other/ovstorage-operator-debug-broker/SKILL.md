---
name: ovstorage-operator-debug-broker
description: Use when triaging a misbehaving ovstorage-broker - covers startup failures, authz denies, listener authn mismatches, streaming write aborts, reload misfires, and drain hangs.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, broker, debugging]
tools: [Read, Bash]
compatibility: Requires access to broker logs, metrics, configuration, and operator-approved diagnostic commands. Credentials are user-supplied.
---

# Debug the Broker

## Goal

Triage a misbehaving broker using the typed errors, metric labels,
and tracing fields the daemon emits. The broker fails closed by
design; most live-incident classes surface as a typed error before
any backend dispatch.

## Recipe

1. Read
   [`docs/public/broker-operator/README.md`](../../docs/public/broker-operator/README.md)
   § *Debug runbook* for the structured walkthrough.
2. For startup failures, run
   `cargo run -p ovstorage-cli -- list-routes --config /etc/ovstorage/broker.toml`
   against the broker's config. The same TOML validator the daemon
   runs at startup will report bad routes, unresolvable secret
   refs, and invalid listener authn config without binding any
   sockets.
3. For authz denies, look at the tracing output for
   `broker_authz_decisions_total{outcome="deny"}`. The deny path
   threads the plugin's `reason` and `explanation` into the gRPC
   `PermissionDenied` message; the `explanation` is typically a
   stable rule id from the built-in policy evaluator.
4. For `PolicyEpochStale` errors, the request was stamped with a
   pre-reload epoch. Nothing in the SDK refreshes and retries it:
   it reaches the caller as `FailedPrecondition` (HTTP 409), which
   the caller re-issues itself against the reloaded policy.
5. For listener authn failures (`Unauthenticated`), confirm the
   mode matches what your callers send:
   - `jwt_verify` mode: bearer JWT against the configured
     `issuer` / `audience` / `jwks_url`. JWKS is cached
     5 minutes; an unknown `kid` triggers one refetch before
     `Unauthenticated`.
   - `peer_cred` mode: UDS / npipe only. Invalid on TCP
     listeners.
   - `trusted_*` modes: only on `trusted_proxy = true` listeners
     with `trusted_peers` CIDR allow-list.
   - `mtls`: reserved; startup fails with `Unsupported` if
     configured.
6. For "broker is up but no routes are visible," check
   `[[connections]]` blocks: backends register at startup; a
   missing or misnamed plugin manifest fails startup. Confirm
   `OVSTORAGE_PLUGIN_DIR` is set and readable. Remember that
   `list-routes` shows only roots marked `visible`: the broker carries a
   `hidden` root to clients marked hidden, and the client keeps it routable
   without listing it. A `suppressed` root is absent from the wire and a direct
   caller receives `NoRoute`, as does an address whose scheme is not in
   `anonymous_fallback_schemes` when no connection serves it. A granted scheme
   reaches clients as a hidden `s3:///` root, and a brokered client honours it
   only when its own `[ovstorage.layers.broker]` table grants the scheme too.
7. For streaming-write issues (slow, corrupted, aborted),
   distinguish:
   - **Graceful EOF** (`Ok(None)` from the inbound stream) —
     broker commits with the chunks received.
   - **RST_STREAM(CANCEL)** (`Err(status)` with
     `status.code() == Cancelled`) — broker aborts with
     `Status::cancelled`. Look for `broker.write` spans
     ending in `Cancelled` to identify these.
   - Inline upload is bounded by `WRITE_BODY_BYTE_CAP` (64 MiB)
     after authz. Larger writes need the redirect branch (S3
     multipart, GCS resumable, etc.); the plugin must mint
     redirects via `WriteStep::Redirects`.
8. For lifecycle issues:
   - `broker_lifecycle_events_total{event="reload_failed"}`
     increments on validation failure; old broker stays live.
   - `broker_policy_epoch_advances_total` increments on
     successful reload.
   - Drain hangs: tune `drain_timeout` (default
     `DEFAULT_DRAIN_TIMEOUT`). A wedged plugin / upstream
     pushes the broker past the deadline and forces truncated
     in-flight RPCs.

## Common live-incident classes

- **Cert expired.** TCP+TLS handshake fails; rotate via SIGHUP
  (Unix) or process restart (Windows). Cert hot-reload is not
  implemented.
- **JWKS unreachable.** `Unauthenticated` for every `jwt_verify`
  request. Check the IdP's reachability from the broker host.
- **Authorization latency.** The built-in policy evaluator is local and
  synchronous; rising RPC latency points to listener authentication, storage
  dispatch, or an outer timeout rather than a remote policy plugin. Watch
  `histogram_quantile(0.99, rate(broker_rpc_seconds_bucket[5m]))`
  trending up — though note the RPC-latency histogram is
  dormant today (registered but not observed), so this query
  may return empty.
- **State root I/O error.** Policy-epoch persistence fails;
  `broker_lifecycle_events_total{event="reload_failed"}`
  increments and the broker keeps the previous epoch.
- **Watch fan-out exhausted.** The 257th concurrent watcher for one
  principal (summed across every watch key on the connection) receives
  `ResourceExhausted` (the per-principal cap is 256).

## Pre-deploy validation

Always run
`cargo run -p ovstorage-cli -- list-routes --config <broker-config>`
against a config change before SIGHUP or restart. The same
validator the daemon runs at startup will surface typed errors
without binding any socket.

## What's not debuggable today

- No `explain-decision <audit-id>` tool. Trace the `audit_id`
  through your log aggregator.
- No durable audit sink; rely on `tracing` output.
- `route.id` and `backend.id` are not stamped on per-RPC spans
  yet — closing that gap is a tracked work item.

## References

- [`docs/public/broker-operator/README.md`](../../docs/public/broker-operator/README.md)
  — full debug runbook + observability + implementation gaps.
- [`ovstorage-operator-monitor-broker`](../ovstorage-operator-monitor-broker/SKILL.md)
  — what to scrape and which spans carry which fields.
- [`ovstorage-operator-configure-broker-policy`](../ovstorage-operator-configure-broker-policy/SKILL.md)
  — interpreting authz denies and policy-epoch advances.
- [`ovstorage-operator-deploy-broker`](../ovstorage-operator-deploy-broker/SKILL.md) —
  baseline deployment checklist.
