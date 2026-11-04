---
name: k8s-autoscaling-troubleshooting
description: >-
  Use when Kubernetes autoscaling does not scale as expected: a HorizontalPodAutoscaler
  whose TARGETS show "<unknown>", "missing request for cpu", "unable to get metrics for
  resource cpu" or "FailedGetResourceMetric", an HPA stuck at maxReplicas
  ("TooManyReplicas") or not scaling down, "Metrics API not available" from kubectl top,
  metrics-server not Ready, a KEDA ScaledObject that is not Ready
  ("ScaledObjectCheckFailed") or creates no HPA, KEDA scalers failing, two autoscalers on
  one workload, or a VerticalPodAutoscaler without recommendations. Investigates with
  kubectl get, describe, events, logs and top, and proposes fixes. Reads first and asks
  before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, metrics-server 0.9, keda 2.21"
  verified-on: "2026-10-25"
---

# Autoscaling troubleshooting

Find out why a workload does not scale the way it should, and propose a fix. **Read
first, ask before changing.** Run the investigation commands freely. Run a command under
an "Ask first" line only after the user approves that exact command; if your credentials
do not allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the
user.

A **HorizontalPodAutoscaler** (HPA) sets the replica count of a Deployment or
StatefulSet every 15 seconds from metrics: CPU and memory from **metrics-server**
(`metrics.k8s.io`), or custom and external metrics from an adapter. **KEDA** turns a
**ScaledObject** into an HPA named `keda-hpa-<name>` and serves its triggers as external
metrics (`external.metrics.k8s.io`). A **VerticalPodAutoscaler** (VPA) changes requests
instead of replicas. The HPA writes what it decided, and why, into three status
conditions (AbleToScale, ScalingActive, ScalingLimited) and its events, so they usually
name the cause.

The commands use placeholders: `my-namespace`, `my-app` (the workload, its HPA and its
ScaledObject). Replace them with the real names. The built-in `view` role can read HPAs
and KEDA's objects, but not APIServices or VPAs; if they are forbidden, say so and ask
the user for them. Never read Secrets, nor the Secrets a KEDA TriggerAuthentication
names. Do not print TriggerAuthentications or ScaledObjects with `-o yaml` or
`describe`: some hold credentials inline (a Vault token, a password in trigger metadata);
read them with the fields below.

## When to use

- `kubectl get hpa` shows `<unknown>` in TARGETS, or REPLICAS do not change under load.
- The workload stays at `maxReplicas`, or never scales down.
- `kubectl top` fails, or metrics-server is not Ready.
- A ScaledObject or ScaledJob is not Ready or not Active, or its HPA is missing.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The HPA asks for more replicas, but the new pods stay Pending or crash:
  `k8s-workload-troubleshooting`, `k8s-node-troubleshooting`.
- Custom metrics come from Prometheus (prometheus-adapter or a KEDA `prometheus`
  trigger) and the query returns nothing: `k8s-prometheus-troubleshooting`.
- A refusal (`Forbidden`) in the KEDA or metrics-server logs: `k8s-rbac-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Read the HPA**: targets, replicas, and the three conditions with their reasons.

```bash
kubectl get hpa -n my-namespace
kubectl get hpa my-app -n my-namespace -o jsonpath='{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}'
kubectl get hpa my-app -n my-namespace -o jsonpath='{.spec.scaleTargetRef}{"\n"}{.spec.minReplicas} {.spec.maxReplicas}{"\n"}{.spec.metrics}{"\n"}{.spec.behavior}{"\n"}'
kubectl get events -n my-namespace --field-selector involvedObject.kind=HorizontalPodAutoscaler
```

**2. Compare with the target workload**: its replicas, its pods' resource requests
(utilization is usage divided by request) and the pods' current usage.

```bash
kubectl get deployment my-app -n my-namespace -o jsonpath='{.spec.replicas} {.status.readyReplicas}{"\n"}{range .spec.template.spec.containers[*]}{.name}{" "}{.resources}{"\n"}{end}'
kubectl top pods -n my-namespace
kubectl get hpa -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,TARGET:.spec.scaleTargetRef.name
```

**3. Check the metrics pipeline**: metrics-server and the APIServices that serve
resource and external metrics.

```bash
kubectl get apiservices v1beta1.metrics.k8s.io v1beta1.external.metrics.k8s.io
kubectl get deployment metrics-server -n kube-system
kubectl logs -n kube-system deployment/metrics-server --tail=50
```

**4. If KEDA scales the workload**, read the ScaledObject's status and KEDA's operator
log.

```bash
kubectl get scaledobjects,scaledjobs,triggerauthentications -n my-namespace
kubectl get scaledobject my-app -n my-namespace -o jsonpath='{.spec.scaleTargetRef}{"\n"}{.spec.minReplicaCount} {.spec.maxReplicaCount}{"\n"}{range .spec.triggers[*]}{.type}{"\n"}{end}{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}'
kubectl get events -n my-namespace --field-selector involvedObject.kind=ScaledObject
kubectl logs -n keda deployment/keda-operator --tail=100
```

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| HPA conditions and events, `<unknown>` targets, min and max, behavior, tolerance, two HPAs on one workload | [references/hpa.md](references/hpa.md) |
| metrics-server, `kubectl top`, APIServices, KEDA ScaledObjects, scalers and its webhook, the VPA | [references/metrics-keda-vpa.md](references/metrics-keda-vpa.md) |

## Read the results

What the common findings mean (Kubernetes 1.37, metrics-server 0.9, KEDA 2.21):

- **TARGETS `cpu: <unknown>/50%` and `ScalingActive False FailedGetResourceMetric`**
  with `failed to get cpu utilization: missing request for cpu in container app of Pod
  ...`: a container has no CPU request, so utilization is undefined and the HPA does
  nothing for that metric. Every container of the pod needs the request.
- **The same reason with `unable to get metrics for resource cpu: ...`**: no metrics.
  `no metrics returned from resource metrics API` is normal for a minute after a pod
  starts; if it stays, or the message names the resource metrics API, check
  metrics-server and `v1beta1.metrics.k8s.io`.
- **`ScalingLimited True TooManyReplicas`** (`the desired replica count is more than the
  maximum replica count`): the HPA wants more pods than `maxReplicas`. Either the limit is
  too low, or each pod is too small for the load (its CPU limit caps usage far above its
  request). `TooFewReplicas` is the same at `minReplicas`.
- **`AbleToScale False FailedGetScale`**: the HPA's `scaleTargetRef` names a workload that
  does not exist (or has no `/scale`).
- **`ScalingActive False AmbiguousSelector`**: two HPAs select the same pods.
- **ScaledObject `Ready False ScaledObjectCheckFailed`** with `ScaledObject doesn't have
  correct scaleTargetRef specification: deployments.apps "..." not found`: KEDA cannot find
  the target and creates no HPA, so the workload is not scaled at all.
- **HPA scales up, then the replicas fall back**: something else sets `spec.replicas` (a
  GitOps tool, or applying a manifest that sets `replicas`), or scale-down waits out
  its stabilization window (5 minutes by default).

State the cause in one sentence, then the evidence you saw (the condition, reason and
message, the spec fields, the requests), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Changing an HPA's `minReplicas` or `maxReplicas` is reversible and only changes scaling,
so it goes under "Ask first" and runs only after the user says yes. Changing a workload's
requests restarts its pods, and changing ScaledObjects, triggers, metrics-server or KEDA
affects scaling for others: hand those to the user as proposed fixes. Prefer fixing the
source (the manifest in Git, the Helm values); a live change is overwritten by the next
deploy. Write each undo with the values you found.

Raise the HPA's maximum, when the cluster has room for more pods:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch hpa my-app -n my-namespace --type=merge -p '{"spec":{"maxReplicas":6}}'
# Undo: kubectl patch hpa my-app -n my-namespace --type=merge -p '{"spec":{"maxReplicas":3}}'
```

Give every container a CPU request, in the workload's source (this rolls the pods):

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl set resources deployment/my-app -n my-namespace -c app --requests=cpu=100m
# Undo: kubectl rollout undo deployment/my-app -n my-namespace
```

Point a ScaledObject at the workload that exists, in its source:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl patch scaledobject my-app -n my-namespace --type=merge -p '{"spec":{"scaleTargetRef":{"name":"my-app"}}}'
# Undo: kubectl patch scaledobject my-app -n my-namespace --type=merge -p '{"spec":{"scaleTargetRef":{"name":"my-app-v2"}}}'
```

## Sources

Checked against the Kubernetes 1.37 documentation and source (v1.37.1), metrics-server
v0.9.0 and KEDA v2.21.0:

- [Horizontal Pod Autoscaling](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/):
  the algorithm, tolerance, behavior and stabilization, missing requests.
- HPA conditions and messages from the source:
  [horizontal.go](https://github.com/kubernetes/kubernetes/blob/v1.37.1/pkg/controller/podautoscaler/horizontal.go)
  and [replica_calculator.go](https://github.com/kubernetes/kubernetes/blob/v1.37.1/pkg/controller/podautoscaler/replica_calculator.go).
  The walkthrough's appendix still shows older condition messages.
- [metrics-server README](https://github.com/kubernetes-sigs/metrics-server/blob/v0.9.0/README.md)
  and [known issues](https://github.com/kubernetes-sigs/metrics-server/blob/v0.9.0/KNOWN_ISSUES.md).
- KEDA [scaling deployments](https://keda.sh/docs/2.21/concepts/scaling-deployments/),
  [admission webhooks](https://keda.sh/docs/2.21/concepts/admission-webhooks/),
  [troubleshooting](https://keda.sh/docs/2.21/concepts/troubleshooting/),
  [cron scaler](https://keda.sh/docs/2.21/scalers/cron/) and
  [Kubernetes compatibility](https://keda.sh/docs/2.21/operate/cluster/#kubernetes-compatibility):
  2.21 lists Kubernetes 1.34 to 1.36; it ran fine on 1.37 here.
- [VPA known limitations](https://github.com/kubernetes/autoscaler/blob/vertical-pod-autoscaler-1.8.1/vertical-pod-autoscaler/docs/known-limitations.md).
- The conditions and events quoted here were seen on a Kubernetes 1.37 kind cluster with
  metrics-server 0.9.0 and KEDA 2.21.0.
