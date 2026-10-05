---
name: otel-fanout
description: Single OTLP endpoint pattern with OpenTelemetry Collector/Alloy fan-out to OpenLIT, Grafana stack (Tempo/Loki/Mimir), and other backends; SkyPilot deploy + validation.
---

# OTEL Fan-out (Single Endpoint) Skill

Use this to design/deploy a single OTLP endpoint (4317/4318) that fans out telemetry to multiple backends (OpenLIT, Grafana Tempo/Loki/Mimir, others) via OpenTelemetry Collector or Grafana Alloy. Targeted to our SkyPilot/AWS setup.

## Core pattern
- One public/priv endpoint: OTLP gRPC/HTTP with TLS + auth.
- Collector/Alloy pipeline: receivers (otlp/grpc, otlp/http) → processors (memory_limiter, batch, retry; optional tail_sampling) → exporters:
  - otlphttp → OpenLIT (traces/metrics/logs)
  - otlp/otlphttp → Grafana Tempo (traces)
  - loki → Grafana Loki (logs) or otlp logs if supported
  - prometheusremotewrite → Mimir/Prometheus for metrics
  - logging exporter for debug only
- Configure resource attributes (service.name, env, version, team) and enforce them.

## Deployment (SkyPilot)
- Create a SkyPilot task/cluster for `otel-gateway` (m5.large ok) with:
  - Alloy/otelcol container (TLS certs, basic auth/token)
  - NLB/ALB forwarding 4317/4318 to the gateway
  - S3 bucket/role if using file or S3 storage for Loki/Mimir/Tempo (optional)
- Grafana stack: separate SkyPilot manifest for Tempo + Loki + Mimir (or Prometheus) + Grafana UI; use S3 for object storage; IAM role with least privilege.
- OpenLIT: keep existing openlit cluster; configure collector exporter to OpenLIT endpoint.

## Config snippet (collector)
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
processors:
  batch: {}
  memory_limiter: { check_interval: 2s, limit_mib: 1024 }
  resourcedetection/system: {}
  attributes:
    actions:
      - key: service.name
        action: upsert
        value: default-service
exporters:
  otlphttp/openlit:
    endpoint: https://<openlit-endpoint>
    headers: { Authorization: "Bearer ${OPENLIT_TOKEN}" }
  otlphttp/tempo:
    endpoint: https://<tempo-endpoint>
  loki:
    endpoint: https://<loki-endpoint>/loki/api/v1/push
  prometheusremotewrite:
    endpoint: https://<mimir-prometheus>/api/v1/push
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [otlphttp/openlit, otlphttp/tempo]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [prometheusremotewrite]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [loki]
```

## Validation checklist
- `otelcol --config config.yaml --dry-run` or `alloy --check` before deploy.
- Health: `curl https://<gateway>:4318/healthz` (or /livez); check logs for exporter failures.
- Fan-out: send test spans/metrics/logs (e.g., `otel-cli span` or `hey` against an OTLP generator) and confirm arrival in OpenLIT, Tempo, Loki, Mimir.
- Status scripts: extend `scripts/openlit-control.sh` and `scripts/status-dashboard.sh` to read collector endpoints and report status; add port-kill protection for SkyPilot API (46580) already in sky-status.sh.

## Client config (one endpoint)
- Set env vars: `OTEL_EXPORTER_OTLP_ENDPOINT=https://<gateway>:4318` plus auth headers or basic auth; prefer OTLP over proprietary formats.
- For tools lacking OTLP logs, ship to file then tail with a sidecar to OTLP.
- Batching: set OTEL_EXPORTER_OTLP_TRACES_EXPORT_TIMEOUT, OTEL_BSP_* as needed to prevent drops; keep retries on.

## Security
- TLS on gateway; basic auth or bearer token; restrict NLB/SG to trusted IPs/VPC endpoints.
- Least privilege IAM for any S3/object stores; no plaintext secrets in configs.

## References
- OpenTelemetry Collector docs (pipelines/exporters)
- Grafana Alloy docs
- OpenLIT ingest endpoints
- Grafana Tempo/Loki/Mimir deployment guides
