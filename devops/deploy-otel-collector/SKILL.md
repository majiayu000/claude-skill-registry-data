---
name: deploy-otel-collector
description: Use when services emit OpenTelemetry and need one collector per environment — a Compose gateway with memory_limiter, batching, redaction and resource attributes, exporting to SigNoz, grafana/otel-lgtm or any OTLP backend, with a health check and a test span.
---

# Deploy OTel Collector

Services speak OTLP to one endpoint per environment. The collector owns everything after that: limits, redaction,
sampling, the backend credential, and the backend choice. Swapping a backend becomes a config-file change, not a redeploy of every service.

## 1. Audit current state

```bash
cat .claude/stack-profile.md 2>/dev/null || cat ~/.claude/stack-profile.md 2>/dev/null   # observability.otel, observability.backend, hosting
ls otel/ deploy/otel/ 2>/dev/null; grep -rln "opentelemetry-collector\|otelcol" --include='*.y*ml' . 2>/dev/null | head
grep -rn "OTEL_EXPORTER_OTLP\|OTEL_SERVICE_NAME" --include='*.y*ml' --include='.env*' --include='*.ts' --include='*.go' --include='*.py' . 2>/dev/null | head
docker compose ls 2>/dev/null
```

From the profile: `observability.otel` (false or absent: stop and say the skill does not apply; suggest `set-up-stack-profile`),
`observability.backend`, `hosting`. If `backend` is `sentry` or `none`, ask nothing more than: "which OTLP backend should the
collector export to?" Sentry captures errors through its own SDK, so it is not the collector's backend by default.

## 2. Decide what to do

- A collector already runs with `memory_limiter` first, `batch` last, a health check and a redaction step → "already in place"; verify only (step 7).
- A collector exists but lacks pieces → add only the missing ones from step 5.
- None → full setup.
- **Topology: one gateway collector per environment** (a Compose service), not an agent on every host and not a sidecar per
  service. Reason: the backend credential and redaction rules live in one place, tail sampling sees every span of a trace in
  one process, and there is one thing to monitor. Choose an agent (per host or per pod) only for host metrics or log files
  from nodes you do not control; see [otel-collector-patterns.md](./otel-collector-patterns.md#rule-one-gateway-per-environment-agents-only-for-host-data).

## 3. Detect the track

| `hosting` | Where the collector runs | How services reach it |
|---|---|---|
| `hetzner`, `ionos` (Compose) | A service in the same Compose project as the apps | `http://otel-collector:4318` over the Compose network |
| `vercel` (serverless) | On the Hetzner/IONOS host, behind TLS and a bearer token | `https://otel.<domain>` with `Authorization` header |
| `supabase` only | Edge Functions export to the same public endpoint; no collector inside Supabase | as Vercel |
| local dev | The same Compose service, ports on `127.0.0.1` | `http://localhost:4318` |

| `observability.backend` | Overlay file |
|---|---|
| `signoz` (self-hosted) | `backend-signoz.yaml` |
| `signoz` (Cloud) | `backend-signoz-cloud.yaml` |
| `grafana-lgtm` | `backend-lgtm.yaml` (**dev and stg only**: the image is built for development, demo and testing) |
| any other OTLP backend | `backend-generic.yaml` |

Hosting mechanics: [deploy-to-hetzner](../deploy-to-hetzner/SKILL.md), [deploy-to-ionos](../deploy-to-ionos/SKILL.md),
[deploy-to-vercel](../deploy-to-vercel/SKILL.md). Naming and signals contract: [observability](../../core/_shared/observability.md).

## 4. Install

Nothing to install on the host. Pull the `contrib` distribution (it has `redaction`, `tail_sampling`, `bearertokenauth`):
`otel/opentelemetry-collector-contrib:0.162.0` (verified 2026-10-09; re-verify, see [stack-versions](../_shared/stack-versions.md)).
The image is `FROM scratch`: it has no shell, `curl` or `wget`, so a Compose `healthcheck:` that execs into it cannot work.

## 5. Generate the config

Files: `otel/config.yaml` (base, backend-agnostic) and one `otel/backend-*.yaml` overlay.

```yaml
# otel/config.yaml
extensions:
  health_check:
    endpoint: 0.0.0.0:13133          # default is localhost; unreachable from outside the container

receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317       # default is localhost; set explicitly for containers
      http:
        endpoint: 0.0.0.0:4318

processors:
  memory_limiter:                    # always first
    check_interval: 1s
    limit_mib: 400                   # about 80% of the container limit
    spike_limit_mib: 100
  resource:
    attributes:
      - key: deployment.environment.name
        value: ${env:DEPLOY_ENV}
        action: upsert
  attributes/redact:
    actions:
      - { key: http.request.header.authorization, action: delete }
      - { key: http.request.header.cookie, action: delete }
      - { key: http.response.header.set-cookie, action: delete }
  redaction:
    allow_all_keys: true             # deny-list mode: keep every key, mask what matches below
    blocked_key_patterns:
      - '(?i).*(password|passwd|secret|token|api[_-]?key|authorization|cookie).*'
    blocked_values:
      - '(?i)bearer\s+[a-z0-9._~+/=-]+'
      - 'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'   # JWT
      - '(sk|pk|rk)_(live|test)_[A-Za-z0-9]{16,}'
    summary: info
  batch: {}                          # always last; defaults: 200 ms, 8192 items

service:
  extensions: [health_check]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, resource, attributes/redact, redaction, batch]
      exporters: [otlp/backend]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, resource, redaction, batch]
      exporters: [otlp/backend]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, resource, attributes/redact, redaction, batch]
      exporters: [otlp/backend]
```

Overlays define only the exporter `otlp/backend`, so a backend switch touches one small file. The four overlays (SigNoz
self-hosted, SigNoz Cloud, grafana/otel-lgtm, generic OTLP) are in
[otel-collector-patterns.md](./otel-collector-patterns.md#backend-overlays). Pick the one from the table in step 3.

Compose service (add to the project's `compose.yaml`; secrets come from the decrypted env file, see [manage-secrets](../manage-secrets/SKILL.md)):

```yaml
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.162.0   # then pin the digest: docker buildx imagetools inspect <image>
    command:
      - --config=/etc/otelcol/config.yaml
      - --config=/etc/otelcol/backend.yaml
    restart: unless-stopped
    environment:
      DEPLOY_ENV: ${DEPLOY_ENV:?set DEPLOY_ENV}
      BACKEND_ENDPOINT: ${BACKEND_ENDPOINT:-}
      SIGNOZ_REGION: ${SIGNOZ_REGION:-}
      SIGNOZ_INGESTION_KEY: ${SIGNOZ_INGESTION_KEY:-}
    volumes:
      - ./otel/config.yaml:/etc/otelcol/config.yaml:ro
      - ./otel/backend-signoz.yaml:/etc/otelcol/backend.yaml:ro   # swap the overlay per backend
    ports:                          # loopback only; apps use the Compose network
      - 127.0.0.1:4317:4317
      - 127.0.0.1:4318:4318
      - 127.0.0.1:13133:13133
    deploy:
      resources:
        limits:
          memory: 512M
```

## 6. Wire the services

Every service gets the same four variables; nothing else about the collector is known to application code:

```dotenv
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_SERVICE_NAME=<service>
OTEL_RESOURCE_ATTRIBUTES=service.version=<git sha>,deployment.environment.name=<env>
```

- `OTEL_EXPORTER_OTLP_ENDPOINT` is a base URL: the SDK appends `/v1/traces`, `/v1/metrics`, `/v1/logs`. Put it in the env schema ([validate-env](../../frontend/validate-env/SKILL.md) pattern) as optional: a missing collector must never stop an app from starting.
- Vercel and Supabase Edge: the endpoint is public, so enable auth (receiver `auth: authenticator: bearertokenauth`) behind a TLS reverse proxy; config in [otel-collector-patterns.md](./otel-collector-patterns.md#rule-a-public-ingest-endpoint-needs-tls-and-a-token).
- Pipeline: the deploy step in [set-up-delivery-pipeline](../set-up-delivery-pipeline/SKILL.md) passes `DEPLOY_ENV` and the image digest's commit as `service.version`.
- Do not log or trace secrets: [logging-contract](../../core/_shared/logging-contract.md), [security-baseline](../../core/_shared/security-baseline.md).

## 7. Verify

```bash
docker compose up -d otel-collector
curl -fsS http://127.0.0.1:13133/                        # expect HTTP 200, JSON containing "Server available"
docker compose logs otel-collector | grep -iE "error|failed|refused" ; echo "grep exit: $?"   # expect: grep exit: 1
```

Send one test span through OTLP/HTTP (hex IDs; times in nanoseconds):

```bash
NOW=$(date +%s)000000000
curl -fsS -X POST http://127.0.0.1:4318/v1/traces -H 'Content-Type: application/json' -d '{
  "resourceSpans": [{
    "resource": { "attributes": [{ "key": "service.name", "value": { "stringValue": "otel-smoke-test" } }] },
    "scopeSpans": [{ "spans": [{
      "traceId": "5b8efff798038103d269b633813fc60c", "spanId": "eee19b7ec3c1b174",
      "name": "smoke", "kind": 1, "startTimeUnixNano": "'"$NOW"'", "endTimeUnixNano": "'"$NOW"'",
      "attributes": [{ "key": "http.request.header.authorization", "value": { "stringValue": "Bearer abc.def.ghi" } }]
    }] }]
  }]
}'                                                       # expect: {"partialSuccess":{}}
```

Within a minute, the backend shows service `otel-smoke-test` with the resource attribute
`deployment.environment.name=<env>`, and the span has **no** `http.request.header.authorization` attribute. If the span
is missing: check the exporter endpoint and TLS setting first, then the backend's own ingest logs.

## References
- [otel-collector-patterns.md](./otel-collector-patterns.md): why one gateway, processor order, redaction, tail sampling, public ingest, per-backend notes.
- [../../core/_shared/observability.md](../../core/_shared/observability.md): signals and naming contract.
- [../_shared/environments.md](../_shared/environments.md): what each environment is.
