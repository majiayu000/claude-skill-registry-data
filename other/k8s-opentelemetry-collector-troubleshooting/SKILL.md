---
name: k8s-opentelemetry-collector-troubleshooting
description: >-
  Use when telemetry (traces, metrics, logs) does not get through the OpenTelemetry
  Collector on Kubernetes: the collector crashes at start ("invalid configuration",
  "references receiver ... which is not configured", "unknown type"), applications get
  "connection refused" on 4317 or 4318 (a receiver listening on localhost, or not in a
  pipeline), exporters fail ("Exporting failed. Will retry the request after interval",
  "Exporting failed. Dropping data.", "sending queue is full", "no children to pick
  from"), the memory_limiter refuses data, k8s_attributes lacks RBAC, or the
  OpenTelemetry Operator does not create a collector or inject auto-instrumentation.
  Investigates with kubectl get, logs and the collector's own metrics, and proposes
  fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, opentelemetry-collector 0.163"
  verified-on: "2026-10-25"
---

# OpenTelemetry Collector troubleshooting

Find out why telemetry does not pass through the OpenTelemetry Collector, and propose a
fix. **Read first, ask before changing.** Run the investigation commands freely. Run a
command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed
fix"; hand it to the user.

A collector's config defines **receivers** (OTLP on 4317 for gRPC and 4318 for HTTP,
Prometheus, ...), **processors** (`memory_limiter`, `batch`, `k8s_attributes`, ...),
**exporters** (`otlp_grpc`, `otlp_http`, `debug`, ...) and **extensions**
(`health_check`, ...), and then the `service.pipelines` that connect them. A component
that no pipeline uses is not started at all, without a warning. The collector checks the
config at start and exits with `Error: ...` when it is invalid. At run time it logs
failed exports with the exporter's name and the error. Collectors often run as an agent
(DaemonSet, sidecar) that forwards to a gateway (Deployment), so follow the data hop by
hop.

The commands use placeholders: `my-namespace`, `my-collector` (the collector workload,
its ConfigMap and Service), `my-backend` (where it exports to) and `my-app` (an
application that sends telemetry). Replace them with the real names. Never read Secrets.
Exporters and auth extensions can carry API keys and tokens in headers: read the
receivers, the pipelines and each exporter's `endpoint`, never dump whole `exporters` or
`extensions` blocks, and never repeat a header value. Do not use `print-config`: it
resolves `${env:...}` values, which may come from Secrets.

## When to use

- Traces, metrics or logs are missing at the backend.
- The collector pods crash, restart, or are OOMKilled.
- Applications log export errors to the collector (`connection refused`, timeouts).
- The OpenTelemetry Operator's collector or auto-instrumentation does not appear.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The collector's Service has no endpoints, or a NetworkPolicy blocks it:
  `k8s-network-troubleshooting`.
- The backend refuses the data (Loki 400 or 429, Prometheus remote write errors):
  `k8s-loki-troubleshooting`, `k8s-prometheus-troubleshooting`.
- `k8s_attributes` or the operator is refused by RBAC: `k8s-rbac-troubleshooting`.
- The operator's webhook certificate comes from cert-manager and is not issued:
  `k8s-cert-manager-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the collector and the application.** A crash points to the config; an
application error names what it could not reach.

```bash
kubectl get pods -n my-namespace -o wide
kubectl logs -n my-namespace deployment/my-app --tail=20
kubectl get services,endpointslices -n my-namespace
```

**2. Read the collector's log**, current and before the last restart: config errors,
the endpoints its receivers listen on (`Starting GRPC server`, `Starting HTTP server`),
and export failures.

```bash
kubectl logs -n my-namespace deployment/my-collector --tail=100
kubectl logs -n my-namespace deployment/my-collector --previous --tail=30
kubectl logs -n my-namespace deployment/my-collector --tail=500 | grep -E 'error|warn|Starting (GRPC|HTTP) server|Exporting failed'
```

**3. Read the config's pipelines, receivers and exporter endpoints**, not the whole
config.

```bash
kubectl get deployment my-collector -n my-namespace -o jsonpath='{.spec.template.spec.containers[0].args}{"\n"}{range .spec.template.spec.volumes[*]}{.name}{" "}{.configMap.name}{.secret.secretName}{"\n"}{end}'
kubectl get configmap my-collector -n my-namespace -o jsonpath='{.data.config\.yaml}' | grep -E '^ *(receivers|exporters|processors|pipelines|protocols|grpc|http|endpoint|traces|metrics|logs):'
```

**4. If the OpenTelemetry Operator manages the collector**, read its resource and its
status.

```bash
kubectl get opentelemetrycollectors,instrumentations -A
kubectl get opentelemetrycollector my-collector -n my-namespace -o jsonpath='{.spec.mode}{" "}{.spec.image}{"\n"}{.spec.config.service}{"\n"}{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}'
kubectl get events -n my-namespace --field-selector involvedObject.kind=OpenTelemetryCollector
```

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A crash at start, config errors, components not in a pipeline, localhost receivers, ports and protocols | [references/config-and-receivers.md](references/config-and-receivers.md) |
| Export failures, retries, queues, memory_limiter, k8s_attributes, internal metrics, the operator and auto-instrumentation | [references/export-and-operator.md](references/export-and-operator.md) |

## Read the results

What the common findings mean (collector 0.163):

- **`Error: invalid configuration: service::pipelines::logs: references receiver
  "otlp/app" which is not configured`**: a pipeline names a component that has no
  definition (a typo, or a missing `/name` suffix). The collector exits; CrashLoopBackOff.
- **`unknown type: "..." for id: "..." (valid values: [...])`**: a component type this
  distribution does not include, or a misspelled one. The core image has fewer
  components than `contrib` and `k8s`.
- **Applications get `connection refused` from the collector's Service, and the log shows
  `Starting GRPC server {"endpoint": "127.0.0.1:4317"}`** (or no such line for that
  receiver): the receiver listens on localhost only; `0.0.0.0` shows as `[::]:4317`. Since v0.104.0 the OTLP receiver
  defaults to `localhost`; in Kubernetes it needs `endpoint: 0.0.0.0:4317` (or the pod
  IP). A receiver missing from every pipeline gives the same symptom and logs no
  `Starting` line at all.
- **`Exporting failed. Will retry the request after interval.`** with `"error": "rpc
  error: code = Unavailable desc = no children to pick from"`: the gRPC exporter's
  `endpoint` resolves to no address (a misspelled or missing Service); gRPC does not say
  "no such host". `connection refused` or `context deadline exceeded` instead means the
  name resolves but nothing answers (the backend is down, a wrong port, a
  NetworkPolicy). Logged at info level; data waits in the
  queue until retries run out (`Dropping data.`, `no more retries left`).
- **`Exporting failed. Rejecting data.` with `sending queue is full`**: the backend is too
  slow or down for longer than the queue holds.
- **`Memory usage is above soft limit. Refusing data.`**: the `memory_limiter` protects
  the collector; senders get `data refused due to high memory usage` and retry.

State the cause in one sentence, then the evidence you saw (the log line, the config
entry, the application's error), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it. A
collector's config is shared by every application that sends to it: never change it
yourself; hand it to the user as a proposed fix. Prefer fixing the source (the Helm
values, the OpenTelemetryCollector resource, the manifest in Git). The collector reads
its config at start, so a changed ConfigMap needs a restart (the operator rolls its
collectors itself). Write each undo with the values you found.

Fix the config in its source, apply it and restart the collector:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl apply -f my-collector-config.yaml
kubectl rollout restart deployment/my-collector -n my-namespace
# Undo: kubectl apply -f my-collector-config-before.yaml, then restart my-collector again
```

Once the collector works, restart an application whose client gave up, so it retries:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout restart deployment/my-app -n my-namespace
# Undo: none needed; the restart only recreates the pods with the same template
```

## Sources

Checked against the OpenTelemetry documentation and the collector source (core and
contrib v0.163.0, distribution v0.163.2) and the operator v0.162.0:

- [Collector configuration](https://opentelemetry.io/docs/collector/configuration/)
  and [troubleshooting](https://opentelemetry.io/docs/collector/troubleshooting/).
- [Internal telemetry](https://opentelemetry.io/docs/collector/internal-telemetry/):
  metrics on 8888 and their names.
- The `localhost` default:
  [core CHANGELOG v0.104.0](https://github.com/open-telemetry/opentelemetry-collector/blob/v0.163.0/CHANGELOG.md)
  and [otlpreceiver factory.go](https://github.com/open-telemetry/opentelemetry-collector/blob/v0.163.0/receiver/otlpreceiver/factory.go).
- Messages from the source:
  [otelcol/config.go](https://github.com/open-telemetry/opentelemetry-collector/blob/v0.163.0/otelcol/config.go)
  and [exporterhelper](https://github.com/open-telemetry/opentelemetry-collector/tree/v0.163.0/exporter/exporterhelper).
  "Dropping data because sending_queue is full" no longer exists in 0.163.
- [Operator](https://github.com/open-telemetry/opentelemetry-operator/blob/v0.162.0/README.md),
  its [compatibility table](https://github.com/open-telemetry/opentelemetry-operator/blob/v0.162.0/docs/getting-started/compatibility.md)
  and [auto-instrumentation troubleshooting](https://opentelemetry.io/docs/platforms/kubernetes/operator/troubleshooting/automatic/).
- The log lines quoted here were seen on a Kubernetes 1.37 kind cluster with the
  contrib collector 0.163.2.
