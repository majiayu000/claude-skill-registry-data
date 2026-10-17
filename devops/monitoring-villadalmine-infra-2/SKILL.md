---
name: monitoring
description: >
  Observability stack: kube-prometheus-stack (Prometheus + Grafana + AlertManager),
  Grafana Tempo (distributed tracing), Grafana Loki (log aggregation),
  and Grafana Alloy (OTLP telemetry pipeline).
  All on K3s ARM64 with local-path storage and Gateway API routing.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, prometheus, grafana, tempo, loki, alloy, monitoring, observability, tracing, metrics, logging]
---

# Monitoring Skill

## Stack Overview

| Component | Chart | Version | App Version | Namespace |
|-----------|-------|---------|-------------|-----------|
| Prometheus + Grafana + AlertManager | `prometheus-community/kube-prometheus-stack` | 82.17.0 | v0.89.0 | monitoring |
| Tempo (tracing backend) | `grafana-community/tempo` | 1.26.7 | 2.10.1 | monitoring |
| Loki (log aggregation) | `grafana/loki` | 6.55.0 | 3.x | monitoring |
| Alloy (telemetry pipeline) | `grafana/alloy` | 1.7.0 | v1.15.0 | monitoring |
| version-checker (image version tracking) | `jetstack/version-checker` | 0.10.0 | 0.10.0 | monitoring |
| helm-dashboard (Helm release UI, read-only) | `komodorio/helm-dashboard` | 2.0.6 | 2.1.1 | monitoring |
| Docker registry:2 (ARM64 image storage) | N/A (kubectl) | 2 | registry |

Grafana is included in kube-prometheus-stack — **do NOT install a separate Grafana chart**.

---

## Helm Repositories

```bash
# prometheus-community (kube-prometheus-stack)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# grafana (alloy, loki, etc.)
helm repo add grafana https://grafana.github.io/helm-charts

# grafana-community (tempo — migrated here after Jan 2026)
helm repo add grafana-community https://grafana-community.github.io/helm-charts
```

> **IMPORTANT:** `grafana/tempo` and `grafana/tempo-distributed` are **deprecated**.
> Use `grafana-community/tempo` (single-binary) or `grafana-community/tempo-distributed`.

---

## Critical: Tempo chart version

`grafana-community/tempo` **v2.0.0 has a template bug**:
it generates `overrides.defaults: {}` in the Tempo config which Tempo 2.10.x rejects:
```
field defaults not found in type overrides.legacyConfig
```

**Use v1.26.7** (latest 1.26.x) — same app version 2.10.1, no bug.

---

## Architecture

```
Apps (OpenTelemetry instrumented)          All Pod Logs
        │ OTLP gRPC :4317 / HTTP :4318            │
        ▼                                         ▼
   [Alloy DaemonSet]                    discovery.kubernetes → discovery.relabel
   otelcol.receiver.otlp → otelcol.exporter.otlp.tempo   (traces)
   loki.source.kubernetes  → loki.write                   (logs)
        │                                │
        │ OTLP gRPC                      │ HTTP push
        ▼                                ▼
   [Tempo StatefulSet]           [Loki StatefulSet + MinIO]
   ← single binary, local-path   ← single binary, MinIO 1Gi object storage
   metricsGenerator → remote_write   ← chunksCache/resultsCache disabled (CM4 memory)
        │
        │ remote_write → :9090/api/v1/write
        ▼
   [Prometheus StatefulSet]      ← local-path PVC 20Gi
        │
        ▼
   [Grafana Deployment]
   datasources: Prometheus + Tempo + Loki
   HTTPRoute: grafana.cluster.home → kube-prometheus-stack-grafana:80
```

---

## k3s-specific: disabled components

These k8s components are **embedded in the k3s server process** and do NOT expose metrics:

```yaml
kubeControllerManager:
  enabled: false   # embedded in k3s
kubeScheduler:
  enabled: false   # embedded in k3s
kubeEtcd:
  enabled: false   # embedded etcd, no external port
kubeProxy:
  enabled: false   # replaced by Cilium BPF
```

Enabled (work fine on k3s):
- `kubelet`, `coreDns`, `kubeStateMetrics`, `nodeExporter`, `prometheusOperator`

---

## Grafana: Gateway API routing

Grafana uses `ClusterIP` + `HTTPRoute` — same pattern as ArgoCD and Pi-hole.

```yaml
# HTTPRoute (created by install-kube-prometheus-stack role):
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: grafana
  namespace: monitoring
spec:
  parentRefs:
    - name: cluster-gateway
      namespace: gateway
  hostnames:
    - grafana.cluster.home
  rules:
    - backendRefs:
        - name: kube-prometheus-stack-grafana
          port: 80
```

Pi-hole wildcard `*.cluster.home → .200` covers DNS automatically.
cert-manager wildcard TLS cert already covers `*.cluster.home`.

---

## Tempo: metricsGenerator

Generates RED (Rate, Error, Duration) metrics from traces → remote_write to Prometheus.
Enables trace↔metric correlation in Grafana.

Processors enabled: `service-graphs`, `span-metrics`.

Remote write URL: `http://kube-prometheus-stack-prometheus.monitoring:9090/api/v1/write`

---

## Alloy: OTLP pipeline + Kubernetes log collection

Alloy runs as a DaemonSet on every node with two pipelines:

**Traces pipeline:**
- Receives traces via OTLP from instrumented apps
- Service ports: `4317` (gRPC), `4318` (HTTP)
- Forwards to Tempo via `otelcol.exporter.otlp`

**Logs pipeline:**
- `discovery.kubernetes` discovers all pods
- `discovery.relabel` maps K8s metadata to labels (namespace, pod, container, job)
- `loki.source.kubernetes` tails container logs on each node
- `loki.write` sends to Loki with `tenant_id: fake`

To instrument an app (environment variables):
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy.monitoring:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
```

Query logs in Grafana Explore: `{namespace="monitoring"}` or `{pod="my-app-xyz"}`

---

## Loki: log aggregation

SingleBinary mode with MinIO for object storage.

Key details:
- **Chart**: `grafana/loki` v6.55.0 (from `grafana` Helm repo)
- **Mode**: `singleBinary` — all components in one pod
- **Object storage**: MinIO (bundled, 1Gi PVC via local-path)
- **Retention**: 24h (CM4 has limited storage)
- **Endpoint**: `loki-gateway.monitoring:80`
- **Multi-tenancy**: enabled by default. All requests require `X-Scope-OrgId: fake` header.
- **Caches**: `chunksCache` and `resultsCache` are **disabled** — they request 8GB+ memory which exceeds CM4 capacity.

Querying Loki from outside the cluster:
```bash
kubectl port-forward -n monitoring svc/loki-gateway 3100:80
curl -H 'X-Scope-OrgId: fake' 'http://localhost:3100/loki/api/v1/labels'
```

Grafana datasource config (set via kube-prometheus-stack `additionalDataSources`):
```yaml
- name: Loki
  type: loki
  url: http://loki-gateway.monitoring:80
  access: proxy
  jsonData:
    httpHeaderName1: X-Scope-OrgId
  secureJsonData:
    httpHeaderValue1: fake
```

---

## Grafana Datasources

Automatically configured via kube-prometheus-stack values:

| Datasource | URL | Notes |
|---|---|---|
| Prometheus | `http://kube-prometheus-stack-prometheus.monitoring:9090` | auto by chart |
| Tempo | `http://tempo.monitoring:3200` | added via additionalDataSources |
| Loki | `http://loki-gateway.monitoring:80` | added via additionalDataSources; requires `X-Scope-OrgId: fake` header |

Tempo datasource features enabled:
- `tracesToMetrics` → correlate traces to Prometheus metrics
- `serviceMap` → service dependency graph
- `nodeGraph` → node graph visualization

---

## Ansible Roles

| Role | File |
|---|---|
| `install-kube-prometheus-stack` | `roles/install-kube-prometheus-stack/` |
| `install-tempo` | `roles/install-tempo/` |
| `install-loki` | `roles/install-loki/` |
| `install-alloy` | `roles/install-alloy/` |

Bootstrap order (after `install-argocd`):
```
install-kube-prometheus-stack → install-tempo → install-loki → install-alloy
```

Tempo depends on Prometheus being up (metricsGenerator remote_write).
Loki is independent — installs after Tempo for ordering consistency.
Alloy depends on Tempo being up (OTLP exporter endpoint).

---

## Health Checks

```bash
# All monitoring pods
kubectl get pods -n monitoring

# Helm releases
helm list -n monitoring

# Prometheus targets (check k3s components are scraped)
kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090
# then: http://localhost:9090/targets

# Grafana (via HTTPRoute)
curl -s https://grafana.cluster.home/api/health

# Tempo ready
kubectl exec -n monitoring tempo-0 -- wget -qO- http://localhost:3200/ready

# Loki ready
kubectl port-forward -n monitoring svc/loki-gateway 3100:80 &
curl -s -H 'X-Scope-OrgId: fake' http://localhost:3100/ready

# Loki labels (verify it's receiving logs)
curl -s -H 'X-Scope-OrgId: fake' 'http://localhost:3100/loki/api/v1/labels'

# Alloy UI
kubectl port-forward -n monitoring svc/alloy 12345:12345
# then: http://localhost:12345
```

---

## Upgrade Procedure

1. Check latest versions:
   ```bash
   helm search repo prometheus-community/kube-prometheus-stack --versions | head -3
   helm search repo grafana-community/tempo --versions | head -5
   helm search repo grafana/loki --versions | head -3
   helm search repo grafana/alloy --versions | head -3
   ```
2. Update version in `roles/<role>/defaults/main.yml`
3. Check release notes for breaking changes
4. Re-run bootstrap:
   ```bash
   ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini \
     --start-at-task "Add prometheus-community Helm repository"
   ```

---

## Troubleshooting

### CRITICAL: NEVER delete Helm secrets or uninstall releases on upgrade failure
→ If `helm upgrade` fails with "release: already exists" or "another operation in progress":
  1. Check `helm status <release> -n <namespace>` — the release may already be deployed
  2. Check `helm history <release> -n <namespace>` — see if the upgrade actually succeeded
  3. Check `kubectl get pods -n <namespace> -l app.kubernetes.io/name=<release>` — pods may be running fine
  4. If the release is "deployed" and pods are healthy, the upgrade likely succeeded despite the error
→ Deleting Helm secrets (`kubectl delete secret sh.helm.release.v1.*`) or running `helm uninstall`
  destroys the release state and makes idempotent re-runs impossible. Only do this as absolute
  last resort after confirming the release is genuinely corrupted.

### CRITICAL: NEVER delete Helm secrets or uninstall releases on upgrade failure
→ If `helm upgrade` fails with "release: already exists" or "another operation in progress":
  1. Check `helm status <release> -n <namespace>` — the release may already be deployed
  2. Check `helm history <release> -n <namespace>` — see if the upgrade actually succeeded
  3. Check `kubectl get pods -n <namespace> -l app.kubernetes.io/name=<release>` — pods may be running fine
  4. If the release is "deployed" and pods are healthy, the upgrade likely succeeded despite the error
→ Deleting Helm secrets (`kubectl delete secret sh.helm.release.v1.*`) or running `helm uninstall`
  destroys the release state and makes idempotent re-runs impossible. Only do this as absolute
  last resort after confirming the release is genuinely corrupted.

### Tempo TraceQL metrics: "localblocks processor not found"
→ Tempo needs `local-blocks` processor for TraceQL metrics queries (`{ } | rate()`, etc.)
→ Add to `overrides.defaults.metrics_generator.processors`: `[service-graphs, span-metrics, local-blocks]`
→ See `roles/install-tempo/tasks/main.yml` for the correct config
→ The `kubernetes.core.helm` module 6.2.0 has a bug where it reports "release does not exist"
  and "already exists" simultaneously on `upgrade -i`. All roles now use `helm list -o json --filter <name>`
  + `set_fact` to check deployment status and skip install when already deployed.

### Alloy not collecting pod logs (Grafana Explore shows no logs)
→ `loki.source.kubernetes` requires `discovery.relabel` to map K8s metadata labels.
  Using `stage.labels` in `loki.process` does NOT work for discovery metadata.
→ Correct pattern: `discovery.kubernetes` → `discovery.relabel` → `loki.source.kubernetes` → `loki.write`
→ Verify: `kubectl logs -n monitoring -l app.kubernetes.io/name=alloy | grep "opened log stream"`

### Tempo CrashLoopBackOff: `field defaults not found in type overrides.legacyConfig`
→ You are using chart v2.0.0. It has a template bug. Use v1.26.7.

### Grafana pod 0/3 (third container not ready)
→ Grafana has a slow readiness probe (60s initialDelay). Wait ~2 minutes after pods start.

### Prometheus targets showing `0/1 up` for k3s components
→ Expected for `kubeControllerManager`, `kubeScheduler`, `kubeEtcd`, `kubeProxy` — these are disabled.
→ If `kubelet` or `coredns` shows down, check Cilium network policies.

### Alloy not forwarding traces
→ Check Alloy config: `kubectl get configmap -n monitoring alloy -o yaml`
→ Check Alloy logs: `kubectl logs -n monitoring -l app.kubernetes.io/name=alloy`
→ Verify Tempo endpoint: `kubectl get svc -n monitoring tempo`

### Grafana HTTPRoute not working
→ Check route: `kubectl get httproute -n monitoring`
→ Check Gateway: `kubectl get gateway -n gateway`
→ Verify DNS: `dig grafana.cluster.home @192.168.178.203`

### Loki not receiving logs / Grafana shows no data
→ Check Loki pods: `kubectl get pods -n monitoring -l app.kubernetes.io/name=loki`
→ Check Loki gateway: `kubectl get svc loki-gateway -n monitoring`
→ Verify ready: `kubectl port-forward -n monitoring svc/loki-gateway 3100:80` then `curl -H 'X-Scope-OrgId: fake' http://localhost:3100/ready`
→ Missing `X-Scope-OrgId` header → Grafana datasource must set it (via `secureJsonData.httpHeaderValue1: fake`)

### Loki MinIO not ready
→ Check MinIO pod: `kubectl get pods -n monitoring -l app.kubernetes.io/name=minio`
→ Check PVC: `kubectl get pvc -n monitoring`
→ MinIO needs `local-path` StorageClass — ensure K3s has it enabled

### loki-chunks-cache-0 stuck in Pending
→ Optional cache component. Safe to ignore — Loki works without it.
→ If you want to fix: ensure a StorageClass exists that can provision PVCs for the cache.
