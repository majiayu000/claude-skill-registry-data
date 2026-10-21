---
name: self-hosted-stack
category: observability
description: Use when an "enable observability" card targets self_hosted - a minimal Grafana LGTM stack (Loki, Grafana, Tempo, Mimir or Prometheus, with Alloy or an OpenTelemetry Collector) by docker-compose or Helm, its resources and retention, and adding it back as TaskTrooper data sources
source: grafana/docker-otel-lgtm, grafana/helm-charts, prometheus-community/helm-charts docs (Apache-2.0), adapted
---

# A self-hosted observability stack

The stack is infrastructure, not application code. If the repository already holds the team's infrastructure (a `deploy/`, `charts/`, `infra/` or Terraform directory), standing it up can be its own developer task; otherwise it is a `before_deploy` step for a person, written so they can follow it. Either way the application's instrumentation task (see `otel-instrumentation`) only points its OTLP exporter at the stack's collector.

## Smallest that works

- **One machine, a small team:** the `grafana/otel-lgtm` image is Grafana, Loki, Tempo, Prometheus and an OpenTelemetry Collector in one container — OTLP on 4317 (gRPC) and 4318 (HTTP), Grafana on 3000. Good for a staging environment or a single small service; it is not meant to scale or to survive a lost volume, so mount `/data` on a persistent volume and say that in the task.
- **docker-compose, one component each:** `grafana/loki` (single binary, filesystem storage), `grafana/tempo` (monolithic), `prom/prometheus` (or `grafana/mimir` monolithic), `grafana/alloy` or `otel/opentelemetry-collector-contrib` receiving OTLP and fanning out, and `grafana/grafana`.
- **Kubernetes:** the `grafana/loki` chart in `SingleBinary` mode, `grafana/tempo` (monolithic), `prometheus-community/kube-prometheus-stack` for Prometheus + Alertmanager + Grafana, and `grafana/alloy` (or the `opentelemetry-collector` chart) as the OTLP entry point.

## Resources and retention

Start small and say so: Loki and Tempo at 0.5 CPU / 1 GiB each, Prometheus at 1 CPU / 2 GiB, Grafana at 0.25 CPU / 256 MiB. Retention is a decision to write down, not a default to inherit:

- Loki: `limits_config.retention_period: 168h` with the compactor's `retention_enabled: true` (without it nothing is ever deleted).
- Tempo: `compactor.compaction.block_retention: 72h`.
- Prometheus: `--storage.tsdb.retention.time=15d` (and `--storage.tsdb.retention.size` on a small disk).

Object storage (S3, GCS) instead of a local volume once more than one replica is needed.

## Security

None of these ship with authentication on their ingest or query ports. Keep them on a private network; put Grafana behind SSO or at least its own admin password from a secret; an OTLP endpoint reachable from the internet needs an authenticating proxy or the collector's `bearertokenauth` extension.

## Back into TaskTrooper

Once it runs, a person adds the stack as data sources under Operations → Data sources: `prometheus` (the Prometheus or Mimir query URL), `loki`, `tempo`. Then bind the component's signals (`list_data_source_metrics`, `propose_signal_binding`) and, where the team alerts from the stack itself, see `alert-as-code`.
