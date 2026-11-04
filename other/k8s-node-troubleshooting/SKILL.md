---
name: k8s-node-troubleshooting
description: >-
  Use when a Kubernetes node is unhealthy or pods will not go onto it: a node NotReady
  or Unknown, MemoryPressure, DiskPressure or PIDPressure, pods Evicted, pods Pending
  with "untolerated taint(s)", "Insufficient cpu" or "Insufficient memory" while the
  node looks idle, a node cordoned (SchedulingDisabled), or the cluster autoscaler not
  adding or removing nodes. Investigates with kubectl get, describe and events, and
  proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37"
  verified-on: "2026-10-24"
---

# Kubernetes node troubleshooting

Find out why a node is unhealthy, or why pods will not be scheduled onto it, and propose
a fix. **Read first, ask before changing.** Run the investigation commands freely. Run
a command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed
fix"; hand it to the user.

You see the node only through the Kubernetes API. Checks on the node itself (the
kubelet, the container runtime, the disk) need someone with access to the machine, so
they are always proposed fixes for a human.

The commands use placeholders: `my-node`, `my-namespace`, `my-app` and `my-pod`.
Replace them with the real names. Never read Secrets. If output contains passwords,
tokens or keys, do not repeat them.

## When to use

- `kubectl get nodes` shows a node `NotReady`, `Unknown` or `SchedulingDisabled`.
- A node reports `MemoryPressure`, `DiskPressure` or `PIDPressure`, or pods were
  `Evicted`.
- Pods stay `Pending` and the `FailedScheduling` event names taints, `Insufficient cpu`
  or `Insufficient memory`, or unschedulable nodes.
- The cluster autoscaler does not add a node for Pending pods, or does not remove an
  empty one.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The nodes are healthy and have room, and the pod itself fails (crash, image, probe,
  quota): `k8s-workload-troubleshooting`.
- A volume cannot attach or mount on the node: `k8s-storage-troubleshooting`.
- `NetworkUnavailable` is `True`, or the CNI pods on the node fail:
  `k8s-network-troubleshooting`.
- On AKS, a node pool or the cluster is `Failed`, or an upgrade or scale fails in Azure
  (quota, VM capacity, a drain blocked by a PodDisruptionBudget): `k8s-aks-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. List the nodes.** `STATUS` shows `Ready`, `NotReady` or `Unknown`, plus
`SchedulingDisabled` when a node is cordoned.

```bash
kubectl get nodes -o wide
```

**2. Describe the node.** Read `Conditions` (status, reason, `LastHeartbeatTime`),
`Taints`, `Unschedulable`, `Lease` (`RenewTime`), `Capacity` and `Allocatable`,
`Non-terminated Pods` with their requests, and `Allocated resources`.

```bash
kubectl describe node my-node
```

**3. See the pods on the node**, in every namespace you can read.

```bash
kubectl get pods -A -o wide --field-selector spec.nodeName=my-node
kubectl get pods -A --field-selector spec.nodeName=my-node,status.phase=Failed
```

The second command lists failed pods there, which include `Evicted` ones.

**4. Read the node's events and its heartbeat.** Node events are kept in the `default`
namespace; the heartbeat is a Lease named after the node. The built-in `view` role
cannot read Leases; if the second command is forbidden, use `LastHeartbeatTime` of the
conditions in `describe node` instead.

```bash
kubectl get events -A --field-selector involvedObject.kind=Node,involvedObject.name=my-node
kubectl get lease my-node -n kube-node-lease
```

**5. For a Pending pod, read why the scheduler refused it**, and what it asks for.

```bash
kubectl describe pod my-pod -n my-namespace
kubectl get pod my-pod -n my-namespace -o jsonpath='{.spec.nodeSelector}{"\n"}{.spec.tolerations}{"\n"}{.spec.containers[*].resources.requests}'
```

**6. Look at usage**, if the cluster has metrics-server. `top` shows usage, not
requests; the scheduler uses requests. Without metrics-server it fails with "Metrics API
not available"; say so and go on.

```bash
kubectl top node my-node
```

**7. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| `NotReady`, `Unknown`, "Kubelet stopped posting node status" | [references/not-ready.md](references/not-ready.md) |
| `MemoryPressure`, `DiskPressure`, `PIDPressure`, `Evicted` pods | [references/pressure.md](references/pressure.md) |
| `Insufficient cpu` or `Insufficient memory`, requests near Allocatable | [references/capacity.md](references/capacity.md) |
| `untolerated taint(s)`, `SchedulingDisabled`, `node(s) were unschedulable` | [references/taints.md](references/taints.md) |
| Pending pods but no new node, or an empty node that stays | [references/autoscaler.md](references/autoscaler.md) |

## Read the results

What the common findings mean (Kubernetes 1.37):

- **`Ready` `Unknown`**: the node controller has not heard from the kubelet within
  `node-monitor-grace-period` (50 seconds by default). The kubelet is down, or the node
  cannot reach the API server. The Lease in `kube-node-lease`, normally renewed every
  10 seconds, stops changing. The node gets the `node.kubernetes.io/unreachable` taints.
- **`Ready` `False`**: the kubelet is running and reports the node is not healthy (for
  example the container runtime or the network plugin is not ready). The reason and
  message say which. The node gets the `node.kubernetes.io/not-ready` taint.
- **Pods on a `NotReady` node** keep their status for a while. Pods tolerate the
  `not-ready` and `unreachable` `NoExecute` taints for 300 seconds by default (added by
  the DefaultTolerationSeconds admission controller), then they are evicted. DaemonSet
  pods tolerate them without a time limit and are not evicted.
- **`MemoryPressure`, `DiskPressure` or `PIDPressure` `True`**: the kubelet crossed an
  eviction threshold. It adds a `NoSchedule` taint for that pressure, frees resources,
  then evicts pods. Node-pressure eviction does not respect PodDisruptionBudgets.
- **`FailedScheduling` with `0/N nodes are available: ...`**: each part counts the nodes
  refused for one reason, for example `1 node(s) had untolerated taint(s)`,
  `2 Insufficient cpu` or `1 node(s) were unschedulable`. The text after `preemption:`
  says whether evicting lower-priority pods could help.
- **`Insufficient cpu` on an idle node**: the scheduler adds up the requests of the pods
  on the node and compares them with `Allocatable`, not with actual use. `Allocated
  resources` in `describe node` shows the requests as a percentage of Allocatable.
- **`SchedulingDisabled`, `Unschedulable: true`**: the node is cordoned. New pods do not
  go there; pods already there keep running.

State the cause in one sentence, then the evidence you saw (the condition and its
message, the taint, the event, the numbers), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Cordoning, uncordoning, adding or removing a `NoSchedule` taint and labelling a node are
reversible, so they go under "Ask first" and run only after the user says yes. Draining
or deleting a node, force-deleting pods and anything on the node host are never run by
you: hand them to the user as proposed fixes and say why. Prefer fixing the source the
workload or the node pool is managed from when there is one. Write each undo with the
values you found.

Uncordon a node whose maintenance is over and that is `Ready`:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl uncordon my-node
# Undo: kubectl cordon my-node
```

Remove a taint left from a maintenance that is over (the key, value and effect exactly
as `describe node` shows them):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl taint nodes my-node example.com/maintenance=true:NoSchedule-
# Undo: kubectl taint nodes my-node example.com/maintenance=true:NoSchedule
```

Check the kubelet on a node that stopped reporting. This runs on the node, which you
cannot reach; a person with access to the machine runs it:

> Proposed fix: review before running. The agent does not run this.

```bash
systemctl status kubelet
journalctl -u kubelet --since "30 min ago" --no-pager | tail -n 50
sudo systemctl restart kubelet
# Undo: nothing to undo for the first two lines, they only read; a restart cannot be undone, the kubelet just starts again
```

Move the pods off a node that will not come back soon. Draining evicts every pod that
is not a DaemonSet pod and deletes `emptyDir` data, so never run it yourself:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl drain my-node --ignore-daemonsets --delete-emptydir-data
# Undo: kubectl uncordon my-node (the evicted pods are recreated by their controllers, not moved back)
```

## Sources

Checked against the Kubernetes 1.37 documentation:

- [Node Status](https://kubernetes.io/docs/reference/node/node-status/): conditions, the
  50-second `node-monitor-grace-period`, Leases in `kube-node-lease` and their 10-second
  renewal.
- [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/): cordon and
  `spec.unschedulable`.
- [Force Delete StatefulSet Pods](https://kubernetes.io/docs/tasks/run-application/force-delete-stateful-set-pod/):
  StatefulSet pods on an unreachable node are not replaced on their own.
- [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
  and [Well-Known Labels, Annotations and Taints](https://kubernetes.io/docs/reference/labels-annotations-taints/):
  taint effects, the `node.kubernetes.io/*` taints, taint removal.
- [Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/):
  DefaultTolerationSeconds and the 300-second default.
- [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/):
  tolerations DaemonSet pods get.
- [Node-pressure Eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/):
  signals, default thresholds, reclaim order, no PDBs.
- [Reserve Compute Resources for System Daemons](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/)
  and [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/):
  Allocatable, scheduling by requests.
- [kubectl drain](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/),
  [kubectl cordon](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_cordon/),
  [kubectl taint](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_taint/)
  and [kubectl top node](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_top/kubectl_top_node/).
- [Resource metrics pipeline](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/)
  and [Troubleshooting Clusters](https://kubernetes.io/docs/tasks/debug/debug-cluster/):
  metrics-server, `describe node` output.
- [Cluster Autoscaler FAQ](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md):
  scale-up and scale-down rules, events, the status ConfigMap, annotations.
- The `FailedScheduling` reason texts are from the Kubernetes 1.37 scheduler source
  ([tainttoleration plugin](https://github.com/kubernetes/kubernetes/blob/release-1.37/pkg/scheduler/framework/plugins/tainttoleration/taint_toleration.go)),
  because the docs show only an older example.
