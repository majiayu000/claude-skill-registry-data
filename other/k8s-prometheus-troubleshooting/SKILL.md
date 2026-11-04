---
name: k8s-prometheus-troubleshooting
description: >-
  Use when Prometheus on Kubernetes does not collect or alert as expected: a
  ServiceMonitor or PodMonitor whose targets never appear, targets that are down
  ("server returned HTTP status 404 Not Found", "connection refused", "context deadline
  exceeded"), a PrometheusRule that does not load or alerts that do not fire or reach
  Alertmanager, a Prometheus or Alertmanager custom resource that is not Available,
  "InvalidConfiguration" events from the Prometheus Operator, or Prometheus pods that are
  OOMKilled or out of disk. Covers the Prometheus Operator (kube-prometheus,
  kube-prometheus-stack). Investigates with kubectl get, describe, events, logs and
  Prometheus' HTTP API through the API server, and proposes fixes. Reads first and asks
  before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, prometheus-operator 0.94, prometheus 3.14"
  verified-on: "2026-10-24"
---

# Prometheus troubleshooting

Find out why Prometheus does not scrape a target, does not load a rule, or does not
alert, and propose a fix. **Read first, ask before changing.** Run the investigation
commands freely. Run a command under an "Ask first" line only after the user approves
that exact command; if your credentials do not allow it, give it to the user to run.
Never run a "Proposed fix"; hand it to the user.

With the **Prometheus Operator**, a `Prometheus` custom resource selects
**ServiceMonitors**, **PodMonitors**, **Probes**, **ScrapeConfigs** and
**PrometheusRules** by label and namespace, and the operator turns them into
Prometheus' configuration. A ServiceMonitor selects Services by label and names one of
their ports. Something can go wrong at each step: the selection, the Service, the port,
the scrape itself.

The commands use placeholders: `monitoring` (where Prometheus runs), `my-prometheus`
(the Prometheus resource), `my-namespace`, `my-app` (the ServiceMonitor and its
Service) and `my-rules`. Replace them with the real names. Prometheus' HTTP API is
reached through the API server's service proxy on the governing Service
`prometheus-operated` (port name `web`); this needs `get` on `services/proxy`, which the
built-in `view` role does not have. If the proxy is forbidden, say so and ask the user
for the Targets page of the Prometheus UI.

Never read Secrets. The operator stores the generated Prometheus and Alertmanager
configuration in Secrets (`prometheus-<name>`, `alertmanager-<name>-generated`), and
the upstream troubleshooting guide decodes them. Do not: use the selection rules, the
operator's events and logs, and Prometheus' own API instead. For the same reason never
call Prometheus' `/api/v1/status/config` or Alertmanager's `/api/v2/status`: they return
that generated configuration (credentials masked, but webhook URLs and routes not).
Access to the service proxy covers the whole Service, so this rule is yours to keep.

## When to use

- A new ServiceMonitor or PodMonitor shows no targets, or the job is missing.
- Targets are `down`.
- A PrometheusRule's alerts do not appear, do not fire, or do not reach Alertmanager.
- The `Prometheus` or `Alertmanager` resource is not `Available`, or its pods crash.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The target's pods are not running or not Ready: `k8s-workload-troubleshooting`.
- The target is up but a NetworkPolicy or DNS blocks the scrape:
  `k8s-network-troubleshooting`.
- Prometheus' volume is full or will not bind: `k8s-storage-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Read the Prometheus resource**: its status, and which monitors and rules it
selects.

```bash
kubectl get prometheuses -A
kubectl get prometheus my-prometheus -n monitoring -o jsonpath='{.spec.serviceMonitorSelector}{"\n"}{.spec.serviceMonitorNamespaceSelector}{"\n"}{.spec.podMonitorSelector}{"\n"}{.spec.ruleSelector}{"\n"}{.spec.ruleNamespaceSelector}{"\n"}{.status.conditions}{"\n"}'
```

**2. Read the ServiceMonitor** and compare it with the selection and with the Service.

```bash
kubectl get servicemonitors,podmonitors -A
kubectl get servicemonitor my-app -n my-namespace -o yaml
kubectl get service my-app -n my-namespace -o jsonpath='{.metadata.labels}{"\n"}{.spec.ports}{"\n"}'
kubectl get endpointslices -n my-namespace -l kubernetes.io/service-name=my-app
kubectl get namespace my-namespace --show-labels
```

**3. Ask Prometheus what it scrapes**: the jobs it has, the active targets with their
health and last error, and the targets it dropped.

```bash
kubectl get --raw '/api/v1/namespaces/monitoring/services/prometheus-operated:web/proxy/api/v1/scrape_pools'
kubectl get --raw '/api/v1/namespaces/monitoring/services/prometheus-operated:web/proxy/api/v1/targets?state=active' | jq -r '.data.activeTargets[] | [.labels.job, .health, .scrapeUrl, .lastError] | @tsv'
kubectl get --raw '/api/v1/namespaces/monitoring/services/prometheus-operated:web/proxy/api/v1/targets?state=dropped' | jq -r '.data.droppedTargets[].discoveredLabels | [.__meta_kubernetes_service_name, .__meta_kubernetes_endpoint_port_name, .__address__] | @tsv'
```

A ServiceMonitor appears as the job `serviceMonitor/<namespace>/<name>/<endpoint index>`.

**4. Read the operator's events and logs.** The operator rejects invalid objects with an
event and logs objects it skips.

```bash
kubectl events -n my-namespace --for servicemonitor/my-app
kubectl get deployments -A -l app.kubernetes.io/name=prometheus-operator
kubectl logs -n monitoring deployment/prometheus-operator --tail=200 | grep -i -E "skipping|rejected|my-app"
```

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| No job or no targets for a ServiceMonitor or PodMonitor, dropped targets | [references/discovery.md](references/discovery.md) |
| Targets `down`: HTTP status, `connection refused`, timeouts, body size, content type | [references/targets-down.md](references/targets-down.md) |
| A PrometheusRule not loaded, alerts not firing or not reaching Alertmanager | [references/rules-and-alerts.md](references/rules-and-alerts.md) |
| The Prometheus resource not Available, pods OOMKilled, disk full, ingestion errors | [references/prometheus-health.md](references/prometheus-health.md) |

## Read the results

What the common findings mean (Prometheus Operator 0.94, Prometheus 3.14):

- **No job `serviceMonitor/<ns>/<name>/...` in `scrape_pools`**: the Prometheus does not
  select the ServiceMonitor. Its labels do not match `serviceMonitorSelector`, or its
  namespace does not match `serviceMonitorNamespaceSelector`. An empty selector (`{}`)
  matches everything; an unset (null) selector matches nothing for monitors and rules,
  and only Prometheus' own namespace for the namespace selectors.
- **The job exists, no active targets, a dropped target**: the ServiceMonitor matches a
  Service, but its `endpoints[].port` is not the name of one of the Service's ports (it
  must be the port's `name`, not its number), or the Service has no ready endpoints.
  The dropped target's `__meta_kubernetes_endpoint_port_name` shows the real port name.
- **The job exists, no targets at all, nothing dropped**: `spec.selector` matches no
  Service, or `namespaceSelector` leaves the Service's namespace out.
- **A target `down` with `server returned HTTP status 404 Not Found`**: the path is
  wrong (`endpoints[].path`, default `/metrics`). Other `lastError` values are in
  [references/targets-down.md](references/targets-down.md).
- **An event `InvalidConfiguration`, `"<name>" was rejected due to invalid
  configuration: ...`**: the operator refused the object; the message says why.

State the cause in one sentence, then the evidence you saw (the selector and labels, the
port names, the target's health and error), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Patching a ServiceMonitor, PodMonitor or PrometheusRule (labels, port, path) is
reversible, so it goes under "Ask first" and runs only after the user says yes.
Changing the Prometheus or Alertmanager resource (selectors, resources, retention),
Alertmanager's configuration and anything with Secrets are never run by you: hand them
to the user as proposed fixes. Monitors usually come from the app's Helm chart or
manifests; fix them there too. Write each undo with the values you found.

Give a ServiceMonitor the label the Prometheus selects:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl label servicemonitor my-app -n my-namespace release=my-prometheus
# Undo: kubectl label servicemonitor my-app -n my-namespace release-
```

Point a ServiceMonitor at the Service's real port name:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch servicemonitor my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/endpoints/0/port", "value": "http"}]'
# Undo: kubectl patch servicemonitor my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/endpoints/0/port", "value": "metrics"}]'
```

Prometheus picks up the change by itself within a minute or two; check `scrape_pools`
and the targets again.

## Sources

Checked against the Prometheus Operator 0.94 and Prometheus 3.14 documentation and
source:

- [Prometheus Operator troubleshooting](https://prometheus-operator.dev/docs/platform/troubleshooting/):
  selection, port names, events; its step that decodes the configuration Secret is
  left out here.
- [API reference](https://prometheus-operator.dev/docs/api-reference/api/): selector
  semantics (empty versus null), ServiceMonitor endpoints.
- [RBAC for the CRDs](https://prometheus-operator.dev/docs/platform/rbac-crd/) and
  [storage](https://prometheus-operator.dev/docs/platform/storage/).
- Prometheus [HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/)
  (targets, scrape pools, rules, alerts, TSDB status),
  [storage](https://prometheus.io/docs/prometheus/latest/storage/) and the
  [3.0 migration guide](https://prometheus.io/docs/prometheus/latest/migration/).
- [Manually constructing API server proxy URLs](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster-services/#manually-constructing-apiserver-proxy-urls).
- Messages from the source:
  [resource_selector.go](https://github.com/prometheus-operator/prometheus-operator/blob/v0.94.2/pkg/prometheus/resource_selector.go),
  [operator.go](https://github.com/prometheus-operator/prometheus-operator/blob/v0.94.2/pkg/operator/operator.go),
  [scrape.go](https://github.com/prometheus/prometheus/blob/v3.14.0/scrape/scrape.go).
  The behaviour and messages quoted here were also seen on a Kubernetes 1.37 kind
  cluster with Prometheus Operator 0.94.2 and Prometheus 3.14.0.
