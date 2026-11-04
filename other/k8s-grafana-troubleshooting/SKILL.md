---
name: k8s-grafana-troubleshooting
description: >-
  Use when Grafana on Kubernetes fails: the Grafana pod crash-loops after a change to its
  provisioning ("Datasource provisioning error", "Only one datasource per organization
  can be marked as default", "failed to parse"), a provisioned dashboard or datasource
  does not appear ("failed to load dashboard from", sidecar ConfigMap labels), panels
  show "No data" or the datasource returns "Bad Gateway" or "connection refused",
  "database is locked" with several replicas, permission errors on the data volume,
  admin login or sidecar "401 Unauthorized", or grafana-operator resources with
  "NoMatchingInstance". Investigates with kubectl get, describe, events and logs, never
  reading Grafana's Secrets, and proposes fixes. Reads first and asks before changing
  anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, grafana 13.2"
  verified-on: "2026-10-24"
---

# Grafana troubleshooting

Find out why Grafana does not start, does not show a datasource or dashboard, or shows
no data, and propose a fix. **Read first, ask before changing.** Run the investigation
commands freely. Run a command under an "Ask first" line only after the user approves
that exact command; if your credentials do not allow it, give it to the user to run.
Never run a "Proposed fix"; hand it to the user.

On Kubernetes, Grafana is usually **provisioned**: datasources and dashboard providers
are YAML files under `/etc/grafana/provisioning/`, and dashboards are JSON files, all
mounted from ConfigMaps. With the Grafana Helm chart (also inside kube-prometheus-stack)
a **sidecar** container copies ConfigMaps labelled `grafana_dashboard` or
`grafana_datasource` into the pod. With the **grafana-operator**, `Grafana`,
`GrafanaDashboard` and `GrafanaDatasource` resources do the same.

The commands use placeholders: `monitoring` (where Grafana runs), `my-grafana` (its
Deployment and Service), `my-grafana-datasources` and `my-grafana-dashboards` (its
ConfigMaps) and `my-app` (a dashboard). Replace them with the real names.

Never read Secrets: not the admin password, not datasource credentials, not
`grafana.ini` values kept in Secrets. The sidecar can also read Secrets with the same
labels; look only at ConfigMaps. Do not log in to Grafana's API with the admin
password; its `/api/health` needs no login.

## When to use

- The Grafana pod is in CrashLoopBackOff or not Ready, often right after a change.
- A provisioned datasource or dashboard is missing in the UI.
- Panels show "No data", or a datasource test fails.
- Logins fail, or the sidecar logs `401 Unauthorized`.
- grafana-operator resources do not sync.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- Grafana runs and reaches Prometheus, but Prometheus has no data for the query:
  `k8s-prometheus-troubleshooting`.
- The datasource's Service exists but traffic does not reach it (NetworkPolicy, DNS):
  `k8s-network-troubleshooting`.
- The pod is Pending or its volume does not mount: `k8s-workload-troubleshooting`,
  `k8s-storage-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the pods.** During a rollout the old pod can keep running while the new one
crashes; look at each pod, not only the Deployment.

```bash
kubectl get deployments,pods -n monitoring -l app=my-grafana -o wide
kubectl get pods -n monitoring -l app=my-grafana -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.phase}{"\n"}{range .status.containerStatuses[*]}{"  "}{.name}{" ready="}{.ready}{" restarts="}{.restartCount}{" last="}{.lastState.terminated.reason}{"\n"}{end}{end}'
kubectl events -n monitoring
```

Avoid `kubectl describe pod` here: it prints the containers' environment values, and
Grafana pods often carry passwords there. If you see a credential anyway, do not repeat
it.

The chart labels its pods `app.kubernetes.io/name=grafana`; use that selector there.

**2. Read the logs of the failing pod**, the previous run if it restarted. Each pod has
the `grafana` container, and with the chart one container per sidecar
(`grafana-sc-dashboard`, `grafana-sc-datasources`).

```bash
kubectl logs -n monitoring my-grafana-0 -c grafana --previous --tail=50
kubectl logs -n monitoring deployment/my-grafana -c grafana --tail=200 | grep -E "level=error|level=warn|Error:"
kubectl logs -n monitoring deployment/my-grafana -c grafana --tail=500 | grep logger=provisioning
```

Replace `my-grafana-0` with the failing pod's name from step 1.

**3. Read the provisioning ConfigMaps** the pod mounts.

```bash
kubectl get deployment my-grafana -n monitoring -o jsonpath='{range .spec.template.spec.volumes[*]}{.name}{" "}{.configMap.name}{"\n"}{end}'
kubectl get configmap my-grafana-datasources -n monitoring -o yaml
kubectl get configmaps -n monitoring -l grafana_dashboard
kubectl get configmaps -n monitoring -l grafana_datasource
```

**4. For "No data" or a failing datasource, check the address it uses** against the
Services that exist.

```bash
kubectl get services -A | grep -i -E "prometheus|loki|tempo"
kubectl get endpointslices -n monitoring
kubectl get --raw '/api/v1/namespaces/monitoring/services/my-grafana:http/proxy/api/health'
```

The last command needs `get` on `services/proxy`; if it is forbidden, skip it.

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| CrashLoopBackOff, `Datasource provisioning error`, `failed to parse`, a datasource or dashboard missing, sidecar not picking up ConfigMaps | [references/provisioning.md](references/provisioning.md) |
| "No data", Bad Gateway, `connection refused`, wrong datasource UID in a dashboard | [references/datasources-no-data.md](references/datasources-no-data.md) |
| `database is locked`, permission errors, plugins, login and `401 Unauthorized`, grafana-operator `NoMatchingInstance` | [references/runtime-and-operator.md](references/runtime-and-operator.md) |

## Read the results

What the common findings mean (Grafana 13.2):

- **The new pod exits with `Error: ✗ invalid service state: Failed ... Datasource
  provisioning error: <reason>`**: Grafana refuses a provisioned datasource file and
  stops; the pod crash-loops. `datasource.yaml config is invalid. Only one datasource
  per organization can be marked as default` means two datasources have `isDefault:
  true`. A YAML error or an unknown field shows up the same way.
- **`logger=provisioning.dashboard ... level=error msg="failed to load dashboard from "
  file=<path> error=<JSON error>`**: that dashboard file is not valid JSON. Grafana
  skips it and keeps running, so only that dashboard is missing.
- **`the same UID is used more than once`** or `dashboard title is not unique in
  folder`: two files define the same dashboard; only one wins.
- **A datasource whose URL names a Service that does not exist** (or the wrong port):
  Grafana starts normally; every query fails, shown in the UI as "Bad Gateway" or a
  connection error, and in the log only when a query runs.
- **`/api/health` returns `"database": "ok"`**: Grafana itself is up; `failing` (HTTP
  503) means its database is not reachable.

State the cause in one sentence, then the evidence you saw (the log line, the ConfigMap
entry, the Services), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Provisioning lives in ConfigMaps that come from a Helm chart, kube-prometheus-stack
values or a GitOps repository: fix it there. Patching a ConfigMap that only holds
provisioning or dashboards, and restarting Grafana to reload it, are reversible, so
they go under "Ask first" and run only after the user says yes. Anything with Secrets
(admin password, datasource credentials), Grafana's database, its volume and the
replica count are never run by you: hand them to the user as proposed fixes. Write each
undo with the values you found.

Restart Grafana after its provisioning ConfigMap is fixed (Grafana reads datasource
files only at start):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout restart deployment/my-grafana -n monitoring
# Undo: kubectl rollout undo deployment/my-grafana -n monitoring
```

## Sources

Checked against the Grafana 13.2 documentation and source (v13.2.4), the Grafana Helm
chart 14.0 and grafana-operator 5.25:

- [Troubleshooting](https://grafana.com/docs/grafana/latest/troubleshooting/) and
  [Grafana on Kubernetes](https://grafana.com/docs/grafana/latest/setup-grafana/installation/kubernetes/).
- [Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/):
  datasource and dashboard files, `isDefault`, providers.
- [Prometheus datasource troubleshooting](https://grafana.com/docs/grafana/latest/datasources/prometheus/troubleshooting/).
- [High availability](https://grafana.com/docs/grafana/latest/setup-grafana/set-up-for-high-availability/):
  a shared database for several replicas.
- [Upgrade to Grafana 13](https://grafana.com/docs/grafana/latest/upgrade-guide/upgrade-v13.0/).
- The [Grafana Helm chart](https://github.com/grafana-community/helm-charts/tree/main/charts/grafana)
  (sidecar labels, image, admin password) and the
  [grafana-operator documentation](https://grafana.github.io/grafana-operator/docs/).
- Messages from the source:
  [provisioning.go](https://github.com/grafana/grafana/blob/v13.2.4/pkg/services/provisioning/provisioning.go),
  [datasources config_reader.go](https://github.com/grafana/grafana/blob/v13.2.4/pkg/services/provisioning/datasources/config_reader.go),
  [dashboards file_reader.go](https://github.com/grafana/grafana/blob/v13.2.4/pkg/services/provisioning/dashboards/file_reader.go).
  The messages quoted here were seen with Grafana 13.2.4 on a Kubernetes 1.37 kind
  cluster; the exact wording of the start-up error differs from older releases.
