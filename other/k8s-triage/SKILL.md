---
name: k8s-triage
description: >-
  Use when something is wrong in a cluster and it is not yet clear where: "the cluster
  is broken", "a lot of pods are failing", "users say the app is down", "something is
  off after the upgrade", or any problem report that names no workload. Sweeps nodes,
  pods in every namespace, recent Warning events and CPU and memory use, ranks what it
  finds by severity, proposes a first fix for each issue and names the skill that goes
  deeper. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37"
  verified-on: "2026-10-23"
---

# Kubernetes triage

Find out where a cluster is unhealthy when nobody knows yet, rank the problems, and hand
each one to the right place. **Read first, ask before changing.** Run the investigation
commands freely. Run a command under an "Ask first" line only after the user approves
that exact command; if your credentials do not allow it, give it to the user to run.
Never run a "Proposed fix"; hand it to the user.

Triage is a first look, not a root-cause analysis. For each problem, report it, show the
evidence, propose a first fix, and name the skill that investigates it fully. Do not
dig deeper than the short first look this skill describes.

The commands use placeholders: `my-namespace`, `my-app`, `my-pod` and `my-node`. Replace
them with the real names. Never read Secrets. If output contains passwords, tokens or
keys, do not repeat them.

## When to use

- The user reports a problem without naming a workload: "the cluster is broken",
  "everything is slow", "lots of pods are failing", "users say the app is down".
- Something changed cluster-wide (an upgrade, a new node pool, a network change) and
  "something is off".
- You were asked for a general health check of a cluster.

When the user names one workload that is unhealthy, start with
`k8s-workload-troubleshooting` instead.

Hand-offs, by skill name. For each issue you find, name the skill that goes deeper. If it
is not installed, give the issue, its evidence, a first fix and the short first look
below, then tell the user which skill would help, and stop there:

- Pods crash, restart, stay `Pending`, fail probes, or a rollout or Job is stuck:
  `k8s-workload-troubleshooting`.
- A node is `NotReady`, under memory, disk or PID pressure, cordoned, or pods are being
  evicted: `k8s-node-troubleshooting`.
- Pods are healthy but traffic does not arrive (Service with no endpoints, DNS,
  NetworkPolicy, Ingress): `k8s-network-troubleshooting`.
- A PersistentVolumeClaim is `Pending`, or volumes fail to attach or mount:
  `k8s-storage-troubleshooting`.
- The API server refuses requests (`failed calling webhook`, an APIService that is not
  `True`, a namespace stuck `Terminating`): `k8s-api-troubleshooting`.
- On AKS, the error comes from Azure (`SyncLoadBalancerFailed`, a `ProvisioningFailed`
  with an Azure error code, `AADSTS` errors, a cluster or node pool `Failed`):
  `k8s-aks-troubleshooting`.

## Investigate

Work through the steps in order. They are cheap and cluster-wide; do all of them before
you rank anything.

**1. Check what you can see.** A user with access to one namespace cannot list nodes or
other namespaces. Know this before you read any result.

```bash
kubectl auth can-i list nodes
kubectl auth can-i list pods --all-namespaces
kubectl auth can-i list events --all-namespaces
```

If a check says `no`, or a command below fails with `Forbidden`, say exactly what you
could not see, and narrow the sweep to the namespaces you can read. Start with the
namespace your kubeconfig points at: commands without `-n` use it, and users with access
to one namespace usually have it set.

```bash
kubectl auth can-i list pods
kubectl get pods
kubectl auth can-i list pods -n my-namespace
```

If none of these works and you know no namespace, ask the user which one to look at.
Never report something you could not see as healthy.

**2. Nodes.** Look at `STATUS` (`Ready`, `NotReady`, and `SchedulingDisabled` for a
cordoned node), then describe every node that is not plainly `Ready`, and read its
`Conditions`, `Taints` and `Allocated resources`.

```bash
kubectl get nodes -o wide
kubectl describe node my-node
```

**3. Pods that are not running.** Across every namespace you can read:

```bash
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded
kubectl get pods -A | grep -v -E "Running|Completed"
kubectl get pods -A --sort-by='.status.containerStatuses[0].restartCount'
```

The first command finds `Pending`, `Failed` and `Unknown` pods. The second also catches
pods whose phase is `Running` but whose `STATUS` column says `CrashLoopBackOff`,
`ImagePullBackOff`, `Error` or `Terminating`. The third puts the most restarted pods
last. Also look for `Running` pods that are not ready, such as `0/1` in the `READY`
column.

When a node is not `Ready`, list the pods on it:

```bash
kubectl get pods -A --field-selector=spec.nodeName=my-node -o wide
```

**4. Warning events.** For each one, check whether the object it is about is still
unhealthy now. Only those count as issues; a Warning about an object that has since
recovered is history, even if it is recent (a new cluster has several from start-up).

```bash
kubectl events -A --types=Warning
```

**5. CPU and memory.** `kubectl top` works only when metrics-server is installed and
running. If it fails, write "metrics not available" in the overall status and go on;
`Allocated resources` from step 2 still shows requests and limits against capacity.

```bash
kubectl top nodes
kubectl top pods -A --sort-by=memory
kubectl top pods -A --sort-by=cpu
```

**6. Controllers short of replicas.** A Deployment, StatefulSet or DaemonSet whose ready
count is below the desired count is affected even when its pods look fine one by one.

```bash
kubectl get deployments -A
kubectl get statefulsets -A
kubectl get daemonsets -A
```

**7. PersistentVolumeClaims and Services**, only if steps 3 and 4 point there (pods
`Pending` with volume events, or an app that is up but unreachable):

```bash
kubectl get pvc -A
kubectl get endpointslices -n my-namespace
```

**8. Pick the area of each issue** and its next skill, from this table:

| What you see | Tier | Next skill |
|---|---|---|
| Node `NotReady` or `Unknown`, a pressure condition `True`, `NetworkUnavailable`, `SchedulingDisabled` | 1 | `k8s-node-troubleshooting` |
| `CrashLoopBackOff`, `OOMKilled`, `Error`, `ErrImagePull`, `ImagePullBackOff`, `CreateContainerConfigError` | 2 | `k8s-workload-troubleshooting` |
| `Pending`, `Running` but not ready, a controller short of replicas | 3 | `k8s-workload-troubleshooting` (or `k8s-storage-troubleshooting` for an unbound PVC) |
| Warning events about objects that are still unhealthy, a node near its memory or CPU capacity, pods at their limits | 4 | the area the event belongs to |
| Service with no ready endpoints while its pods are healthy, DNS failures | 3 | `k8s-network-troubleshooting` |
| CoreDNS pods crashing or not Ready, CoreDNS errors in its logs | 2 | `k8s-coredns-troubleshooting` |
| `FailedCreate` events that name a webhook, an APIService that is not `True`, a namespace stuck `Terminating` | 3 | `k8s-api-troubleshooting` |
| On AKS: `SyncLoadBalancerFailed`, Azure error codes in `ProvisioningFailed` or `FailedAttachVolume`, `AADSTS` errors in logs | 3 | `k8s-aks-troubleshooting` |

A short first look inside a container can confirm a network issue. Ask first: show the
command, and run it only after the user agrees (pick a running pod in the namespace that
has `nslookup`; many minimal images do not):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl exec my-pod -n my-namespace -- nslookup my-app.my-namespace.svc.cluster.local
```

## Read the results

**Rank by severity.** Report issues in this order, most urgent first:

1. **Nodes.** `NotReady` or `Unknown`, `MemoryPressure`, `DiskPressure` or `PIDPressure`
   `True`, `NetworkUnavailable`, cordoned (`SchedulingDisabled`).
2. **Crashing pods.** `CrashLoopBackOff`, `OOMKilled`, `Error`, `ErrImagePull` or
   `ImagePullBackOff`, `CreateContainerConfigError`.
3. **Pods that do not become ready.** `Pending`, `Running` but not ready, controllers
   with fewer ready replicas than desired, Services without ready endpoints.
4. **Early warnings.** Warning events about objects that are still unhealthy, and
   resource pressure that has not broken anything yet (a node above about 90% of its
   memory, pods at their CPU or memory limit).

Within a tier, more affected nodes or pods rank higher. **One cause, one issue:** when a
node problem explains pod symptoms (the pods on a `NotReady` node show `Unknown`,
`Terminating`, or are being recreated elsewhere), report the node issue once and list
the pods as its evidence. Do not report those pods as separate application failures.

**Read nodes.** `Ready` is `Unknown` when the node controller has not heard from the
node within its grace period (50 seconds by default): the kubelet is down or the node is
unreachable. `Ready` is `False` when the kubelet reports the node is not healthy. A
pressure condition `True` means the kubelet may evict pods from that node. The taints
`node.kubernetes.io/not-ready`, `node.kubernetes.io/unreachable` and
`node.kubernetes.io/unschedulable` (a cordoned node) show the same state to the
scheduler. By default, pods on a `NotReady` or unreachable node are evicted after five
minutes; until then they look stuck, and pods of a StatefulSet can stay `Terminating`.

**Read events.** Typical reasons: `FailedScheduling`, `BackOff`, `Failed` (image pull),
`Unhealthy` (probes), `FailedMount`, `Evicted`, `NodeNotReady`, `OOMKilling`. An event
is evidence only when its object is unhealthy now: a `Running`, ready pod that once
failed a readiness probe is not an issue.

**Write the report** in this shape:

1. **Overall status.** Nodes (how many, how many `Ready`), pods (how many are not
   healthy, in how many namespaces), metrics (available or not), and what you could
   not see because of access.
2. **Issues**, ranked. For each: one sentence for the issue, the evidence you saw (the
   status, the condition, the event reason and message, the number), the next skill, and
   a first fix in the format under [Proposed fix](#proposed-fix).
3. **When the sweep is clean**, do not invent a problem. Say what you checked and that
   it looked healthy from where you could see, then ask the user to narrow it down: which
   app, namespace or URL, what exactly they saw (an error message, a timeout, slowness),
   and since when.

## Proposed fix

Triage proposes first fixes only. Show each one to the user first: what it changes and
how to undo it. A reversible fix goes under "Ask first" and runs only after the user
says yes. Anything destructive or hard to undo is never run by you; say why and hand it
over. Prefer fixing the source the workload is deployed from (manifest, Helm values,
GitOps repository) when there is one. Write each undo with the values you found.

Uncordon a node that was left cordoned after maintenance and is otherwise healthy:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl uncordon my-node
# Undo: kubectl cordon my-node
```

Roll back a Deployment whose pods started failing right after a rollout. First note the
current revision with `kubectl rollout history deployment/my-app -n my-namespace`; the
undo below returns to it by number (here revision 3), so it holds even if another rollout
happens in between:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout undo deployment/my-app -n my-namespace
# Undo: kubectl rollout undo deployment/my-app -n my-namespace --to-revision=3
```

Force-delete a pod stuck `Terminating` on a node that is gone for good. Never run this
yourself: for a StatefulSet pod it can start a second copy while the first still runs
on a node that is only unreachable. A human must first confirm the node is really gone.

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl delete pod my-pod -n my-namespace --force --grace-period=0
# Undo: none; the pod's controller recreates it on another node
```

For a node that stays `NotReady`, a workload that keeps crashing, a Service without
endpoints or a stuck volume, the fix needs the deeper skill named in the issue.

## Sources

Checked against the Kubernetes 1.37 documentation:

- [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) and
  [Node Status](https://kubernetes.io/docs/reference/node/node-status/): conditions,
  the 50-second grace period before `Unknown`, cordoned nodes shown as
  `SchedulingDisabled`, eviction five minutes after `Unknown`.
- [Node-pressure Eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/):
  pressure conditions and eviction signals.
- [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/):
  the `node.kubernetes.io/*` taints, the default 300-second tolerations, pods still
  running on a partitioned node.
- [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/):
  pod phases (`Unknown` when the node cannot be reached), `Terminating`,
  `CrashLoopBackOff`.
- [Field Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/):
  `status.phase` and `spec.nodeName` for pods.
- [kubectl events](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/):
  `--types`, `-A`.
- [Resource metrics pipeline](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/)
  and [kubectl top](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_top/):
  `kubectl top` needs metrics-server.
- [Troubleshooting Clusters](https://kubernetes.io/docs/tasks/debug/debug-cluster/):
  listing and describing nodes.
- [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/):
  the `view` role and `kubectl auth can-i`.
