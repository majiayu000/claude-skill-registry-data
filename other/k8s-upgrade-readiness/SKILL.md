---
name: k8s-upgrade-readiness
description: >-
  Use when a Kubernetes cluster is about to be upgraded to its next minor version, or
  someone asks "is the cluster ready to upgrade?", "what will break when we upgrade?" or
  why a node drain hangs during an upgrade: PodDisruptionBudgets with ALLOWED
  DISRUPTIONS 0, pods with no controller ("cannot delete Pods that declare no
  controller"), admission webhooks with failurePolicy Fail and no endpoints, deprecated
  or removed APIs still in use (apiserver_requested_deprecated_apis, CRD versions marked
  deprecated), kubelet and control plane version skew, nodes on cgroup v1 or containerd
  1.x, and add-ons that do not support the target version. Reports what to fix first.
  Read-only: never upgrades, drains or changes anything itself.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37"
  verified-on: "2026-10-31"
---

# Upgrade readiness

Check a cluster before a Kubernetes minor version upgrade, and report what has to be
fixed first. **Read only.** Run the investigation commands freely. Never upgrade,
drain, cordon or evict anything, and never change a workload, a PodDisruptionBudget or a
webhook yourself: everything here is a proposed fix for the user and the owners of each
object. Never read Secrets.

An upgrade replaces the control plane first, one minor version at a time, and then
every node: each node is cordoned and drained (its pods are evicted and recreated
elsewhere), then replaced or upgraded. Managed clusters (AKS, EKS, GKE) do both for you,
but they drain nodes the same way. So most of what breaks an upgrade is in the cluster:
pods that cannot be evicted, pods that cannot be recreated, and clients or add-ons that
use an API or a node setup the new version no longer supports.

The commands use placeholders: `my-namespace`, `my-app`, `my-node`. Replace them with
the real names. Some checks need more than the built-in `view` role (nodes, CRDs,
webhook configurations, the API server's metrics); if a command is forbidden, say which
check it was and give the user the command to run.

## When to use

- Before a minor version upgrade, or when planning one.
- A node drain during an upgrade hangs, or a managed upgrade fails or stalls on
  evictions.
- After an upgrade, clients fail with `no matches for kind` or `the server could not
  find the requested resource`.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- On AKS: available versions, node pool upgrades and upgrades that failed:
  `k8s-aks-troubleshooting`.
- A webhook or an APIService is already failing requests today: `k8s-api-troubleshooting`.
- A node is NotReady or under pressure today: `k8s-node-troubleshooting`.
- Pods are already failing today: `k8s-workload-troubleshooting`, or `k8s-triage` for a
  first look.
- The Gateway API CRDs and their versions: `k8s-gateway-api-troubleshooting`.

## Investigate

Run every step: the goal is a complete list, not the first problem. Note the current
version and the target version (the next minor) first.

**1. Versions and skew**: the API server, every kubelet, the container runtime, the
kernel and the OS image.

```bash
kubectl version
kubectl get nodes -o wide
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{" kubelet="}{.status.nodeInfo.kubeletVersion}{" runtime="}{.status.nodeInfo.containerRuntimeVersion}{" kernel="}{.status.nodeInfo.kernelVersion}{" os="}{.status.nodeInfo.osImage}{"\n"}{end}'
kubectl get pods -n kube-system -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.spec.containers[*].image}{"\n"}{end}'
```

**2. Nodes that are not ready, cordoned or under pressure.**

```bash
kubectl get nodes
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{" unschedulable="}{.spec.unschedulable}{" "}{range .status.conditions[?(@.status=="True")]}{.type}{" "}{end}{"\n"}{end}'
```

**3. What a drain cannot evict**: PodDisruptionBudgets that allow no disruption, and
pods with no controller.

```bash
kubectl get pdb -A
kubectl get pdb -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{" allowed="}{.status.disruptionsAllowed}{" healthy="}{.status.currentHealthy}/{.status.desiredHealthy}{" selector="}{.spec.selector}{" unhealthyPodEvictionPolicy="}{.spec.unhealthyPodEvictionPolicy}{"\n"}{end}'
kubectl get pods -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,OWNER:.metadata.ownerReferences[0].kind,NODE:.spec.nodeName
kubectl get deployments,statefulsets -A
```

**4. What would refuse the recreated pods**: admission webhooks that fail closed, and
whether their Services have endpoints.

```bash
kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations
kubectl get validatingwebhookconfigurations -o jsonpath='{range .items[*]}{range .webhooks[*]}{.name}{" failurePolicy="}{.failurePolicy}{" service="}{.clientConfig.service.namespace}/{.clientConfig.service.name}{" rules="}{.rules}{" namespaceSelector="}{.namespaceSelector}{"\n"}{end}{end}'
kubectl get mutatingwebhookconfigurations -o jsonpath='{range .items[*]}{range .webhooks[*]}{.name}{" failurePolicy="}{.failurePolicy}{" service="}{.clientConfig.service.namespace}/{.clientConfig.service.name}{" rules="}{.rules}{" namespaceSelector="}{.namespaceSelector}{"\n"}{end}{end}'
kubectl get endpointslices -n my-namespace
```

**5. Deprecated APIs still in use**: requests the API server has served for deprecated
versions since it started, and custom resource versions marked deprecated or still
stored.

```bash
kubectl get --raw /metrics | grep apiserver_requested_deprecated_apis
kubectl get crds -o jsonpath='{range .items[*]}{.metadata.name}{" stored="}{.status.storedVersions}{" deprecated="}{.spec.versions[?(@.deprecated==true)].name}{"\n"}{end}'
kubectl api-versions
```

**6. Add-ons and their versions**: what runs as part of the cluster, to check against
each project's supported Kubernetes versions.

```bash
kubectl get deployments,daemonsets,statefulsets -A -o jsonpath='{range .items[*]}{.kind}{" "}{.metadata.namespace}/{.metadata.name}{" "}{.spec.template.spec.containers[*].image}{"\n"}{end}'
kubectl get apiservices
```

**7. Open the matching reference** for the details:

| What you check | Reference |
|---|---|
| Version skew, the upgrade order, cgroup v1, containerd 1.x, deprecated and removed APIs, CRD stored versions, add-on compatibility | [references/versions-and-apis.md](references/versions-and-apis.md) |
| PodDisruptionBudgets, unmanaged pods, local storage, single replicas, webhooks during a drain | [references/drains.md](references/drains.md) |

## Read the results

What the common findings mean (Kubernetes 1.37):

- **A PDB with `ALLOWED DISRUPTIONS` `0`** while its pods are healthy (for example
  `minAvailable` equal to the replicas, or `maxUnavailable: 0`): no pod it selects can
  be evicted, so a drain of a node running one of them waits forever, and managed
  upgrades stall or fail on it. A PDB with 0 because pods are unhealthy blocks the same
  way unless its `unhealthyPodEvictionPolicy` is `AlwaysAllow`.
- **A pod with no owner** (`OWNER` `<none>`): kubectl drain refuses it with `cannot
  delete Pods that declare no controller (use --force to override)`; with `--force` it
  is deleted and nothing recreates it. Pods owned by a `Node` are static (mirror) pods,
  and DaemonSet pods are skipped by drains; both are fine.
- **A pod with an `emptyDir` volume**: drain refuses it with `cannot delete Pods with
  local storage (use --delete-emptydir-data to override)`; the data is lost on eviction.
  Usually expected; say so only if the data matters.
- **A webhook with `failurePolicy: Fail` whose Service has no endpoints**: requests it
  matches are refused. If it matches pods, every pod a drain evicts in those namespaces
  cannot be recreated, although the running ones look fine today.
- **A kubelet newer than the API server, or more than three minor versions older**:
  outside the version skew policy. Its upgrade order is stricter: before the API server
  moves to the target, every kubelet should be at most two minor versions older than
  the target. Upgrade those nodes first. The API server itself moves one minor version
  at a time.
- **A `containerRuntimeVersion` of `containerd://1.x`** with a target of 1.36 or later:
  the kubelet no longer supports containerd 1.x; upgrade containerd to 2.0 or later
  first. A **kernel older than 5.8**, or an OS image that still uses cgroup v1: since
  1.35 the kubelet does not start on cgroup v1 by default.
- **`apiserver_requested_deprecated_apis` lines**: a client used that group, version
  and resource since the API server started. A `removed_release` at or below the target
  version means that client breaks after the upgrade. `version="v1"` `resource="endpoints"`
  is the core Endpoints API, deprecated in favour of EndpointSlices with no removal
  planned.
- **A CRD whose `storedVersions` contains a version marked `deprecated`**, or a version
  the next release of its add-on drops: objects are still stored in that version. They
  must be migrated, and `storedVersions` trimmed, before the add-on removes it.
- **Add-on versions**: compare each against the project's compatibility table for the
  target version; an add-on that does not support it is upgraded first.

Report the result as a list, most important first: blockers (the upgrade will fail or
cause an outage), then risks (downtime, data loss, a client that will break), then what
was checked and found fine. For each, the object, the evidence and the proposed fix.

## Proposed fix

Show each fix to the user; the agent runs none of them. Every finding here belongs to
the owner of the object (an application team, a platform team), and changing a PDB, a
webhook or a workload's replicas during an upgrade window affects availability. Write
each undo with the values you found.

Let a single-replica app keep a pod running while another starts (two or more replicas;
the PDB then allows one disruption):

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl scale deployment my-app -n my-namespace --replicas=2
# Undo: kubectl scale deployment my-app -n my-namespace --replicas=1
```

Allow one disruption instead of keeping every pod (for the app's owners; prefer the
change in the app's source):

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl patch pdb my-app -n my-namespace --type=json -p '[{"op": "remove", "path": "/spec/minAvailable"}, {"op": "add", "path": "/spec/maxUnavailable", "value": 1}]'
# Undo: kubectl patch pdb my-app -n my-namespace --type=json -p '[{"op": "remove", "path": "/spec/maxUnavailable"}, {"op": "add", "path": "/spec/minAvailable", "value": 1}]'
```

A pod with no controller is recreated under a Deployment (or a Job) by its owner, or
deleted if nobody needs it, before the upgrade. A webhook without endpoints gets its
backend back before the upgrade (see `k8s-api-troubleshooting`). Clients and manifests
that use a removed API are moved to its replacement version first. The references give
the commands for each.

## Sources

Checked against the Kubernetes 1.37 documentation, and on a Kubernetes 1.37 kind
cluster:

- [Version Skew Policy](https://kubernetes.io/releases/version-skew-policy/): the
  skew for each component and the upgrade order.
- [Deprecated API Migration Guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/)
  and [Kubernetes Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/).
- [Warning: Helpful Warnings Ahead](https://kubernetes.io/blog/2020/09/03/warnings/):
  deprecation warnings and the `apiserver_requested_deprecated_apis` metric.
- [Safely Drain a Node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/),
  [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) and
  [Specifying a Disruption Budget](https://kubernetes.io/docs/tasks/run-application/configure-pdb/):
  evictions, PDBs, `unhealthyPodEvictionPolicy`.
- [About cgroup v2](https://kubernetes.io/docs/concepts/architecture/cgroups/): cgroup
  v1 deprecated in 1.35, the kubelet's `failCgroupV1`, the kernel 5.8 requirement.
- [Kubernetes v1.34: Autoconfiguration for Node Cgroup Driver Goes GA](https://kubernetes.io/blog/2025/09/12/kubernetes-v1-34-cri-cgroup-driver-lookup-now-GA/):
  containerd 1.x supported until 1.35, the `kubelet_cri_losing_support` metric.
- [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/):
  `failurePolicy` and `matchPolicy`.
- [Versions in CustomResourceDefinitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/):
  deprecated versions and `storedVersions`.
- The drain messages and the metric lines quoted were seen on the kind cluster with
  a server-side dry-run drain, run by the test kit's admin, not the agent.
