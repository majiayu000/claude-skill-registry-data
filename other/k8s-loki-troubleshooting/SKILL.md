---
name: k8s-loki-troubleshooting
description: >-
  Use when Grafana Loki on Kubernetes rejects, drops or cannot query logs: clients
  getting 400, 401 or 429 from /loki/api/v1/push, "write operation failed", "has
  timestamp too old", "entry too far behind", "Per stream rate limit exceeded",
  "ingestion rate limit exceeded", "maximum active stream limit exceeded", "no org id"
  (missing X-Scope-OrgID tenant), Loki crashing at start with "validating config" or
  "invalid schema config", "failed to flush chunks", ring or memberlist errors ("empty
  ring", "too many unhealthy instances in the ring"), or queries failing with "the query
  time range exceeds the limit" or timing out. Investigates with kubectl get, logs and
  read-only Loki endpoints, and proposes fixes. Reads first and asks before changing
  anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, loki 3.7"
  verified-on: "2026-10-25"
---

# Loki troubleshooting

Find out why Loki does not accept, keep or return logs, and propose a fix. **Read first,
ask before changing.** Run the investigation commands freely. Run a command under an "Ask
first" line only after the user approves that exact command; if your credentials do not
allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the user.

Clients (Promtail, Grafana Alloy, Fluent Bit, the OpenTelemetry Collector) push log
lines to `/loki/api/v1/push`. The **distributor** validates each line (labels, size,
age) and applies the tenant's ingestion rate; the **ingester** applies per-stream limits
and writes chunks to storage; queriers answer LogQL queries. In monolithic mode one pod
(`-target=all`) runs every part; in microservices mode each part is its own workload.
Loki answers a refused push with **400** (invalid, not retried), **429** (rate limit,
retried) or **401** (no tenant), and logs refused pushes as `msg="write operation
failed" details="<reason>"`, except 401s, which it does not log.

The commands use placeholders: `my-namespace`, `my-loki` (the Loki workload, its Service
and its ConfigMap) and `my-app-logger` (a client). Replace them with the real names.
Never read Secrets. Loki's config may hold storage keys: if it is in a Secret, do not
read it; if it is in a ConfigMap, read only the parts you need and never repeat a key,
password or token you see. Prefer the `/config` endpoint, which masks typed secret fields.
Avoid `kubectl describe pod` on Loki: it prints literal environment values.

**Never call `/flush` or `/ingester/shutdown`**, not even with GET: Loki flushes all
chunks or shuts the ingester down. Never POST to a ring page (`forget=` removes an
instance). Use only the read endpoints listed here.

## When to use

- A log agent reports 4xx errors from Loki, or logs are missing in Grafana.
- Loki pods crash, restart, or are not Ready.
- Queries fail, time out, or return nothing for data that was sent.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The client cannot reach Loki at all (DNS, Service, NetworkPolicy):
  `k8s-network-troubleshooting`.
- The log agent itself fails (Fluent Bit, the OpenTelemetry Collector):
  `k8s-fluent-bit-troubleshooting`, `k8s-opentelemetry-collector-troubleshooting`.
- Grafana's Loki datasource fails while Loki answers: `k8s-grafana-troubleshooting`.
- Loki pods are Pending or OOMKilled: `k8s-workload-troubleshooting`; a full volume:
  `k8s-storage-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See Loki's pods and the client's result.** The HTTP status the client got points to
the part that refused it.

```bash
kubectl get pods -n my-namespace -o wide
kubectl logs -n my-namespace deployment/my-app-logger --tail=20
```

**2. Read Loki's log**: refused pushes, start-up errors, storage and ring errors.

```bash
kubectl logs -n my-namespace deployment/my-loki --tail=200 | grep -E 'level=(error|warn)'
kubectl logs -n my-namespace deployment/my-loki --previous --tail=50
kubectl get events -n my-namespace --sort-by=.lastTimestamp
```

**3. Check where the config lives and what it sets**: `auth_enabled`, the limits and
the schema. Check the kind of object first; a Secret is not read. Match only the keys
you need, so storage credentials near them are not printed.

```bash
kubectl get deployment my-loki -n my-namespace -o jsonpath='{.spec.template.spec.containers[0].args}{"\n"}{range .spec.template.spec.volumes[*]}{.name}{" "}{.configMap.name}{.secret.secretName}{"\n"}{end}'
kubectl get configmap my-loki -n my-namespace -o jsonpath='{.data.config\.yaml}' | grep -E 'auth_enabled|store:|schema:|period:|reject_old_samples|ingestion_rate|ingestion_burst|per_stream_rate|max_global_streams|max_line_size'
```

**4. Ask Loki itself**, through the API server's service proxy, if your credentials
allow `get` on `services/proxy` (the built-in `view` role does not). With
`auth_enabled: true` the query endpoints need a tenant header and answer `no org id`
here; the status endpoints below do not.

```bash
kubectl get --raw /api/v1/namespaces/my-namespace/services/my-loki:http-metrics/proxy/ready
kubectl get --raw /api/v1/namespaces/my-namespace/services/my-loki:http-metrics/proxy/services
kubectl get --raw "/api/v1/namespaces/my-namespace/services/my-loki:http-metrics/proxy/config?mode=diff"
kubectl get --raw /api/v1/namespaces/my-namespace/services/my-loki:http-metrics/proxy/metrics | grep -E 'loki_discarded_samples_total|status_code="(4|5)'
```

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| Pushes refused (400, 401, 429), `write operation failed`, tenants, limits | [references/ingestion.md](references/ingestion.md) |
| Loki does not start, not Ready, ring and memberlist, storage, flushes, retention, queries | [references/startup-storage-queries.md](references/startup-storage-queries.md) |

## Read the results

What the common findings mean (Loki 3.7):

- **Client 400 and `msg="write operation failed" details="entry for stream '{app=\"my-app\",
  service_name=\"my-app\"}' has timestamp too old: 2020-09-13T12:26:40Z, oldest acceptable
  timestamp is: ..."`**: the lines are older than `reject_old_samples_max_age` (7 days by
  default). Loki adds the `service_name` label itself. The client's
  clock or its timestamps are wrong, or it replays old logs.
- **Client 401 and nothing in Loki's log**: `auth_enabled: true` (multi-tenant) and the
  client sends no `X-Scope-OrgID` header; Loki answers `no org id`. Every client and the
  Grafana datasource need the tenant ID.
- **Client 429 with `Per stream rate limit exceeded` or `ingestion rate limit exceeded for
  user ...`**: a stream or the tenant sends more than `per_stream_rate_limit` (3MB/s) or
  `ingestion_rate_mb` (4MB/s) allow. Clients retry 429s, so logs arrive late or not at
  all.
- **Loki in CrashLoopBackOff with `msg="validating config" err="CONFIG ERROR: invalid
  schema config: validating period_config: tsdb must always have periodic config for
  index set to 24h"`**: the `tsdb` index needs `period: 24h`. Clients then get `connection
  refused` or no endpoints.
- **`failed to flush chunks: ...`**: the ingester cannot write to object storage; the
  wrapped error names the bucket, credentials or network problem. Data stays in memory
  and the WAL until it can.
- **`too many unhealthy instances in the ring`** or **`empty ring`**: ingesters are not
  ACTIVE or not found (memberlist cannot join, pods not Ready).

State the cause in one sentence, then the evidence you saw (the client's status, Loki's
log line, the config field), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Loki's config, its limits and its storage are shared by every client and tenant: never
change them yourself; hand them to the user as proposed fixes. A client's own config
(its timestamps, its tenant header, its URL) belongs to that client's owners. Prefer
fixing the source (the Helm values, the manifests in Git). Write each undo with the
values you found.

Change Loki's config in its source and roll it out, for example `index.period: 24h`, or
`limits_config.reject_old_samples_max_age` for a client that must replay older logs:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl apply -f my-loki-config.yaml
kubectl rollout restart deployment/my-loki -n my-namespace
# Undo: kubectl apply -f my-loki-config-before.yaml, then restart my-loki again
```

After a client's fix rolls out, restart the client to retry at once:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout restart deployment/my-app-logger -n my-namespace
# Undo: none needed; the restart only recreates the pods with the same template
```

## Sources

Checked against the Loki 3.7 documentation and source (v3.7.9):

- [Troubleshoot log ingestion](https://grafana.com/docs/loki/latest/operations/troubleshooting/troubleshoot-ingest/)
  and [request validation and rate limits](https://grafana.com/docs/loki/latest/operations/request-validation-rate-limits/).
- [Troubleshoot operations](https://grafana.com/docs/loki/latest/operations/troubleshooting/troubleshoot-operations/):
  rings, memberlist, `-verify-config`.
- [Multi-tenancy](https://grafana.com/docs/loki/latest/operations/multi-tenancy/),
  [HTTP API](https://grafana.com/docs/loki/latest/reference/loki-http-api/),
  [deployment modes](https://grafana.com/docs/loki/latest/get-started/deployment-modes/),
  [schema](https://grafana.com/docs/loki/latest/operations/storage/schema/) and
  [retention](https://grafana.com/docs/loki/latest/operations/storage/retention/).
- [Helm install](https://grafana.com/docs/loki/latest/setup/install/helm/): the OSS chart
  is now in [grafana-community/helm-charts](https://github.com/grafana-community/helm-charts/tree/main/charts/loki).
- Messages from the source:
  [validation/validate.go](https://github.com/grafana/loki/blob/v3.7.9/pkg/validation/validate.go),
  [ingester/flush.go](https://github.com/grafana/loki/blob/v3.7.9/pkg/ingester/flush.go)
  and [storage/config/schema_config.go](https://github.com/grafana/loki/blob/v3.7.9/pkg/storage/config/schema_config.go).
  The docs' `failed to store chunks: storage unavailable` does not exist in 3.7. The
  refusals quoted here were seen on a Kubernetes 1.37 kind cluster with Loki 3.7.9.
