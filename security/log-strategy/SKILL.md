---
name: log-strategy
description: Design logging that supports investigations without becoming a privacy liability. Covers what to log and what never to log (PII, secrets), structured logging, retention tiers, centralization choices, alert routing, and the operational-versus-access-versus-audit log split. Invoke when starting a new service, when investigation revealed missing log fields, or when log volume is becoming expensive.
---

# Log Strategy

Most teams either log too little to investigate anything or too much to find anything (and end up storing PII they didn't mean to). This skill is the middle path: enough to support incident response, not so much that the log becomes a liability of its own.

Pairs with [`incident-response`](../incident-response/SKILL.md) (where logs get used) and [`gdpr-technical-controls`](../gdpr-technical-controls/SKILL.md) (where log privacy lives).

## When to invoke

- Starting a new service or workflow
- Investigation revealed missing fields ("we don't know what request triggered this")
- Logs are leaking PII or secrets
- Log volume is becoming expensive / unwieldy
- Consolidating to a central logging stack (Loki, ELK, OpenObserve, hosted)
- After an incident where the log was insufficient

## Three classes of log, three retention tiers

Treat your logs as three distinct streams. Conflating them is where the trouble starts.

| Class | Purpose | Typical retention | Storage tier |
|---|---|---|---|
| **Operational** | Debugging, performance, errors | 7–30 days | Hot index |
| **Access** | Who hit what, when (webserver + app request log) | 30–90 days | Hot + warm |
| **Audit** | Security-relevant events (auth, permission changes, sensitive actions) | 12 months+ | Append-only, immutable where possible |

Costs and tools differ per class. Mixing them gives the audit log's slow-and-expensive retention to the operational stream and is the most common reason logging gets killed by finance.

## Operational logs — what to capture

Structured logging beats freeform every time. Choose JSON (or logfmt) and a single library for the whole app.

```ts
// pino example — Node
import pino from 'pino';

const log = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  redact: {
    paths: ['password', 'token', 'authorization', '*.password', '*.token', 'req.headers.authorization', 'req.headers.cookie'],
    censor: '[REDACTED]',
  },
  serializers: {
    req: (req) => ({
      method: req.method,
      url: req.url,
      requestId: req.id,
      // explicitly NOT: headers (except a few safe ones), body
    }),
    err: pino.stdSerializers.err,
  },
});

log.info({ orderId, userId: anonymize(userId) }, 'order created');
log.warn({ requestId, latencyMs }, 'slow query');
log.error({ requestId, err }, 'unhandled error in handler');
```

Patterns:

- **One event per line, structured**. Greppable, parseable by any log system.
- **A `requestId` / `traceId` on every log line** within a request — lets you reconstruct a request's full path. Generate at the edge (Nginx / Cloudflare / app middleware), pass through to downstream services.
- **Log levels mean something**. `error` = an unhandled exception or a degraded user outcome; `warn` = a recoverable surprise; `info` = state changes worth knowing about; `debug` = noisy diagnostics that ship off by default.
- **No secrets, no PII** — redact in the serializer, not at the call site (humans forget; serializers don't).
- **Bounded volume per request** — a handler logging 50 lines per request creates a $/month problem. Tighten before launch.

## Access logs — webserver + app

Webserver-level access logs (nginx, Caddy, Cloudflare logs) are usually fine with their defaults plus a few tweaks:

```nginx
# nginx — log format that includes useful diagnostic + minimal PII
log_format main escape=json '{'
  '"time":"$time_iso8601",'
  '"remote_addr":"$remote_addr",'           # consider hashing — see below
  '"request_id":"$request_id",'
  '"method":"$request_method",'
  '"path":"$request_uri",'
  '"status":$status,'
  '"body_bytes_sent":$body_bytes_sent,'
  '"referer":"$http_referer",'
  '"user_agent":"$http_user_agent",'
  '"request_time":$request_time,'
  '"upstream_response_time":"$upstream_response_time"'
'}';
access_log /var/log/nginx/access.log main;
```

Considerations:

- **IPs in DACH/EU** — full IP storage is widely treated as personal data. Options:
  - Hash with HMAC + rotating key (anonymous but consistent within rotation window)
  - Truncate to `/24` for IPv4, `/64` for IPv6 (lossy but acceptable for most analytics)
  - Keep full only for the abuse-investigation tier with shorter retention (e.g. 7 days)
- **No bodies in access logs**. Bodies leak passwords on login routes, payment data on checkout, PII on profile updates. The webserver default doesn't log bodies; don't be tempted by "let's just log the request body for debugging".
- **Cookies and `Authorization` header** stripped — they include session identifiers and tokens.

## Audit logs — security-relevant events

These are the events you want to find six months from now during an investigation.

What deserves an audit-log entry:

- **Authentication**: successful login, failed login, MFA challenge result, password change, password reset request, password reset use, account locked, email change request, email change confirm, account deletion
- **Authorization**: role/permission granted or revoked, admin actions affecting other users, sensitive data export (SAR), data deletion
- **Configuration**: feature-flag flips, security-setting changes, API key issued/revoked, integration enabled/disabled
- **Sensitive data access**: who viewed which PII record, who exported the database, who downloaded an attachment containing PII
- **Money-touching**: refunds issued, manual ledger adjustments, fee waivers, balance transfers

Per entry, capture:

```json
{
  "ts": "2026-05-12T14:23:00Z",
  "actor": { "type": "user", "id": "u_abc", "via": "session" },
  "action": "user.password.reset.request",
  "target": { "type": "user", "id": "u_abc" },
  "context": {
    "ip_hash": "...",
    "user_agent": "...",
    "request_id": "...",
    "result": "ok"
  }
}
```

Patterns:

- **Append-only.** Use a write-only database role, an append-only S3 bucket with object lock, or a managed audit-log service. The app's normal role must not be able to delete or update audit rows.
- **Tamper-evidence** for high-stakes contexts: hash-chain each entry against the previous one, or write to a service that does (e.g. AWS QLDB, Tigris).
- **Separate storage** from operational logs — different retention, different access controls.
- **Indexed by actor, target, and action** for investigation queries.
- **Visible to the user** for their own audit trail ("recent activity" view) — surfaces own compromises faster than you do.

## What NEVER to log

A handful of values that turn the log into a new liability:

- Passwords, password hashes, password reset tokens
- Session cookies / `Authorization` headers / API keys / JWTs / OAuth tokens
- Credit card numbers, CVVs, bank account numbers (PCI scope explodes if you do)
- Private keys, signing keys, encryption keys
- Full social security / national-ID numbers
- Full email or phone of users when an identifier alone would do
- Raw request/response bodies on any auth, payment, or profile endpoint

If a regex / structured-log redactor catches these, you're protected when a future code change accidentally tries to log one.

## Centralization choices

Pick a stack and stick to it. Mixing is operational hell.

**Self-hosted options**:

- **Grafana Loki + Promtail / Vector** — store JSON logs in object storage, query in Grafana. Cheap, simple, fine for small/medium scale.
- **OpenSearch / ELK** — full text + dashboarding. More moving parts.
- **OpenObserve** — newer, integrates logs+metrics+traces, lower operational footprint than ELK.

**Hosted options**:

- **Datadog / New Relic / Honeycomb** — turn-key, expensive at volume, easiest pickup
- **Better Stack / Axiom / Baselime** — affordable mid-tier
- **Cloudflare Logpush** — if you're already on Cloudflare, ship to R2/S3 cheaply

For audit logs specifically, consider a separate destination (immutable bucket, or a service like AWS CloudTrail / Google Cloud Audit Logs equivalent).

## Alerts vs logs

Logs are for investigation; alerts are for getting woken up. They should not be the same thing.

- **From operational logs**: 5xx rate per service, error-class spike, slow-query rate, queue depth
- **From access logs**: spike in 4xx per route (especially 401/403/404), spike in 429, unusual ASNs
- **From audit logs**: admin actions on other users, sensitive data exports, password-reset bursts on a single account, MFA-disabled events

Route each alert class to a different channel — paged for ops, weekly digest for audit anomalies, etc. Reduces alert fatigue.

## Cost control

Logs scale linearly with traffic; cost surprises are universal.

- **Cap volume at the source.** A handler emitting 50 log lines per request is the most common cause of bills.
- **Sample debug-level logs in production.** Keep 1–10% of `debug` and `trace`.
- **Drop bot traffic at the ingest layer** if it's clean (otherwise it dominates the access log).
- **Retain warm tier short, archive long.** Most queries hit the last 7 days; cold storage in S3/R2 is pennies vs hot indexing.
- **Reduce field count.** Every JSON key in every log line costs at index time. Audit which fields are queried, drop the rest.

## Privacy checklist (DACH / EU)

- [ ] No bodies of POST/PUT/PATCH in access logs
- [ ] IPs hashed/truncated, or kept full only on a separate stream with short retention
- [ ] `Authorization`, `Cookie`, `Set-Cookie` headers stripped
- [ ] Known-sensitive JSON fields redacted in structured logs by key name
- [ ] Retention period documented per log stream, matches privacy policy
- [ ] Sub-processor list updated if logs ship to a hosted service
- [ ] Audit logs separate from operational, with separate retention and access controls
- [ ] Log queries by employees are themselves audited (who searched what)

## What this skill will not do

- Recommend logging request bodies on auth or payment routes
- Help build a logging stack for systems you do not own
- Replace a regulated-environment (HIPAA / PCI / SOC 2) audit-log requirement — those have specifics this doesn't cover
