---
name: k8s-fluent-bit-troubleshooting
description: >-
  Use when Fluent Bit on Kubernetes does not deliver logs: the DaemonSet crashes on a
  config error ("tried to instance a plugin name that doesn't exist", "unknown
  configuration property", "configuration file contains errors"), an output fails
  ("failed to flush chunk", "cannot be retried", "no upstream connections available",
  "getaddrinfo", "Connection refused"), records arrive without Kubernetes metadata
  ("could not get meta for POD"), lines arrive unparsed or not at all (tail path, parser,
  CRI versus Docker format), or inputs pause ("paused (mem buf overlimit"). Covers the
  Helm chart and the Fluent Operator. Investigates with kubectl get, logs and Fluent Bit's
  read-only HTTP endpoints, and proposes fixes. Reads first and asks before changing
  anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, fluent-bit 5.1"
  verified-on: "2026-10-25"
---

# Fluent Bit troubleshooting

Find out why Fluent Bit does not ship logs, and propose a fix. **Read first, ask before
changing.** Run the investigation commands freely. Run a command under an "Ask first"
line only after the user approves that exact command; if your credentials do not allow
it, give it to the user to run. Never run a "Proposed fix"; hand it to the user.

Fluent Bit runs as a DaemonSet: on every node a **tail** input reads the container log
files under `/var/log/containers/`, the **kubernetes** filter adds pod metadata from the
API server, and **outputs** send the records to a backend (Elasticsearch, Loki, an HTTP
endpoint, a forwarder). Its own log names each part as `[input:tail:tail.0]`,
`[filter:kubernetes:kubernetes.0]`, `[output:http:http.0]`, so the log usually names the
cause. The Helm chart keeps the config in a ConfigMap (`fluent-bit.conf`); the **Fluent
Operator** builds it from custom resources into a Secret.

The commands use placeholders: `my-namespace`, `my-fluent-bit` (the DaemonSet, its
ConfigMap and its ServiceAccount), `my-fluent-bit-pod` (one of its pods) and
`my-backend` (the Service an output sends to). Replace them with the real names. Never
read Secrets: not the Fluent Operator's rendered config, not Secrets that outputs take
credentials from. The ConfigMap may hold credentials inline (`HTTP_Passwd`,
`http_api_key`, `cloud_auth`, `bearer_token`, AWS keys): read it, but never repeat those
values. Avoid `kubectl describe pod` on Fluent Bit: it prints literal environment
values. Never request `/api/v1/trace/...` (a GET turns tracing on) and never POST to
`/api/v2/reload`.

## When to use

- Logs are missing, late, or incomplete at the log backend.
- Fluent Bit pods crash, restart, or are not Ready.
- Records arrive without `kubernetes` fields, or with the raw `<time> stdout F <line>`
  text in `log`.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The backend refuses what Fluent Bit sends (Loki 400, 401, 429):
  `k8s-loki-troubleshooting`.
- The backend's Service has no endpoints or a NetworkPolicy blocks it:
  `k8s-network-troubleshooting`.
- The kubernetes filter is refused by RBAC: `k8s-rbac-troubleshooting`.
- Pods are Pending, OOMKilled or evicted: `k8s-workload-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the DaemonSet and its pods**: ready on every node, restarts.

```bash
kubectl get daemonsets -A -l app.kubernetes.io/name=fluent-bit
kubectl get pods -n my-namespace -l app.kubernetes.io/name=fluent-bit -o wide
```

**2. Read Fluent Bit's log**, current and before the last restart. Errors and warnings
name the input, filter or output.

```bash
kubectl logs -n my-namespace daemonset/my-fluent-bit --tail=100
kubectl logs -n my-namespace daemonset/my-fluent-bit --previous --tail=50
kubectl logs -n my-namespace daemonset/my-fluent-bit --tail=500 | grep -E '\[ ?(error|warn)\]'
```

**3. Read the config**: inputs (`Path`, parsers), filters, outputs (`Name`, `Host`,
`Port`, `Match`). Do not repeat credentials you see.

```bash
kubectl get daemonset my-fluent-bit -n my-namespace -o jsonpath='{.spec.template.spec.containers[0].args}{"\n"}{range .spec.template.spec.volumes[*]}{.name}{" "}{.configMap.name}{.secret.secretName}{.hostPath.path}{"\n"}{end}'
kubectl get configmap my-fluent-bit -n my-namespace -o yaml
```

**4. Check what the outputs and the kubernetes filter depend on**: the backend's
Service, and the ServiceAccount's access to pods and namespaces.

```bash
kubectl get services,endpointslices -A | grep -i my-backend
kubectl get clusterrolebindings -o wide | grep my-fluent-bit
kubectl auth can-i list pods --as=system:serviceaccount:my-namespace:my-fluent-bit
```

**5. Ask Fluent Bit itself** (port 2020, if `HTTP_Server` is on), through the API
server's pod proxy, if your credentials allow `get` on `pods/proxy` (the built-in `view`
role does not). Each pod reports for its own node.

```bash
kubectl get --raw /api/v1/namespaces/my-namespace/pods/my-fluent-bit-pod:2020/proxy/api/v2/health
kubectl get --raw /api/v1/namespaces/my-namespace/pods/my-fluent-bit-pod:2020/proxy/api/v1/metrics
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A crash at start, config errors, the Fluent Operator's resources, hot reload | [references/config-and-operator.md](references/config-and-operator.md) |
| Outputs failing, retries, dropped chunks, backpressure, missing metadata, tail and parsers, the HTTP endpoints | [references/pipeline.md](references/pipeline.md) |

## Read the results

What the common findings mean (Fluent Bit 5.1):

- **`[config] section 'htttp' tried to instance a plugin name that doesn't exist`** then
  `configuration file contains errors, aborting.`: a misspelled plugin `Name`; the pod
  exits and goes to CrashLoopBackOff.
- **`[net] getaddrinfo(host='...', err=4): Domain name not found`** with
  `[output:http:http.0] no upstream connections available to ...`: the output's `Host`
  does not resolve. Then `[engine] failed to flush chunk '...', retry in N seconds` and,
  once retries run out, `chunk '...' cannot be retried`: those logs are dropped. The
  default `Retry_Limit` is 1; the Helm chart sets `False` (retry forever).
- **`[net] TCP connection failed: host:port (Connection refused)`**: the name resolves,
  but nothing listens there (the backend is down, or the port is wrong).
- **`[filter:kubernetes:kubernetes.0] could not get meta for POD ...`**: the filter cannot
  read pod metadata (RBAC, `Kube_URL`, the API server unreachable). Fluent Bit keeps
  running and ships records **without** `kubernetes` fields; the HTTP status is only
  logged at debug level.
- **Records with `log` holding `2026-... stdout F <line>`**: the parser does not match
  the runtime's log format; containerd and CRI-O write CRI lines, so use
  `multiline.parser docker, cri`.
- **`[input] tail.0 paused (mem buf overlimit`**: the output cannot keep up, and the
  tail input stops reading until memory frees; lines can be lost on rotation.

State the cause in one sentence, then the evidence you saw (the log lines with their
plugin prefix, the config entries), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Fluent Bit's config and RBAC serve every node and every workload's logs: never change
them yourself; hand them to the user as proposed fixes. Prefer fixing the source (the
Helm values or the Fluent Operator's resources). Fluent Bit reads its config only at
start unless hot reload is on, so a changed ConfigMap needs a restart. Write each undo
with the values you found.

Fix the config in its source, apply it, and restart the DaemonSet so it reads it:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl apply -f my-fluent-bit-configmap.yaml
kubectl rollout restart daemonset/my-fluent-bit -n my-namespace
# Undo: kubectl apply -f my-fluent-bit-configmap-before.yaml, then restart the DaemonSet again
```

Bind the role the kubernetes filter needs (read on `pods` and `namespaces`) to Fluent
Bit's ServiceAccount:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl create clusterrolebinding my-fluent-bit --clusterrole=my-fluent-bit --serviceaccount=my-namespace:my-fluent-bit
# Undo: kubectl delete clusterrolebinding my-fluent-bit
```

Once the config or the access is fixed, restart Fluent Bit so it picks it up:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout restart daemonset/my-fluent-bit -n my-namespace
# Undo: none needed; the restart only recreates the pods with the same template
```

## Sources

Checked against the Fluent Bit 5.1 documentation and source (v5.1.5), the Helm chart
fluent-bit 0.58.3 and the Fluent Operator v3.10.1:

- [Kubernetes installation](https://docs.fluentbit.io/manual/installation/downloads/kubernetes)
  and the [Kubernetes filter](https://docs.fluentbit.io/manual/data-pipeline/filters/kubernetes),
  including its troubleshooting section.
- [Tail input](https://docs.fluentbit.io/manual/data-pipeline/inputs/tail),
  [HTTP output](https://docs.fluentbit.io/manual/data-pipeline/outputs/http),
  [scheduling and retries](https://docs.fluentbit.io/manual/administration/scheduling-and-retries),
  [backpressure](https://docs.fluentbit.io/manual/administration/backpressure),
  [monitoring](https://docs.fluentbit.io/manual/administration/monitoring) and
  [hot reload](https://docs.fluentbit.io/manual/administration/hot-reload).
- The [Helm chart](https://github.com/fluent/helm-charts/tree/fluent-bit-0.58.3/charts/fluent-bit)
  and the [Fluent Operator](https://github.com/fluent/fluent-operator/blob/v3.10.1/README.md).
- Messages from the source:
  [flb_config.c](https://github.com/fluent/fluent-bit/blob/v5.1.5/src/flb_config.c),
  [flb_engine.c](https://github.com/fluent/fluent-bit/blob/v5.1.5/src/flb_engine.c) and
  [kube_meta.c](https://github.com/fluent/fluent-bit/blob/v5.1.5/plugins/filter_kubernetes/kube_meta.c).
  The log lines quoted here were seen on a Kubernetes 1.37 kind cluster with Fluent Bit
  5.1.5.
