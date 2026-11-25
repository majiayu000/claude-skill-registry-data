---
name: k8s-cluster-review
description: >-
  Use when nothing is broken but someone wants to know whether a Kubernetes cluster, or
  one namespace, is still in good shape: "review the cluster", "check it against best
  practices", "what drifted since we deployed it?", after taking over a cluster, or
  before a busy period. Reviews the live objects, not manifests in a repository, in
  three groups. Reliability: workloads with one replica, no readiness probe or no
  requests, PodDisruptionBudgets that allow 0 disruptions or match no pod, all replicas
  on one node or zone. Security: privileged or root containers, hostPath and
  hostNetwork, namespaces without Pod Security labels, cluster-admin bound to users or
  ServiceAccounts, namespaces without NetworkPolicies, :latest images. Hygiene and cost:
  PVCs no pod mounts, Released PVs, Services without endpoints, LoadBalancers, workloads
  at 0 replicas, failed Jobs, stale CronJobs. Reports each finding once per workload,
  with why it matters and when it is fine. Read-only: never changes anything itself.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37"
  verified-on: "2026-11-11"
---

# Cluster review

Review a running cluster for what drifted in after it was deployed: settings that do
not break anything today, but hurt during the next drain, load spike or incident, or
cost money for nothing. **Read only.** Run the investigation commands freely. Never
change, scale, label or delete anything yourself: every fix here is a proposed fix for
the user or the owner of the object. Never read Secrets, and never `exec` into a pod;
the review needs neither.

Manifest linters (kube-linter, Polaris, kube-score) check what is in a repository.
This review checks what ended up in the cluster. If the user already has output from
one of those tools, use it as extra evidence; never install them.

The commands use placeholders: `my-namespace`, `my-app`, `my-node`. Replace them with
the real names. Cluster-wide checks need read access to nodes, PersistentVolumes and
the RBAC objects, which the built-in `view` role leaves out. If a command is forbidden,
do not treat it as "nothing found": put the check in the report's Skipped section with
the command for the user to run.

## When to use

- A periodic review: monthly, before a busy period or a launch, after taking over a
  cluster or a namespace from another team.
- Someone asks whether the cluster follows good practice, or what is risky or wasteful
  in it, and nothing is broken.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- Something is broken today (pods in CrashLoopBackOff or Pending, a node NotReady):
  the matching troubleshooting skill, or `k8s-triage` for a first look. A review is
  not the place to debug it.
- Deprecated or removed APIs, version skew, anything about the next upgrade:
  `k8s-upgrade-readiness`. A PDB that allows 0 disruptions is reported here in one line,
  with a pointer there for what it does to a drain.
- Certificates that expire or fail to renew: `k8s-cert-manager-troubleshooting`.
- Who can do what in detail, and why a request is forbidden: `k8s-rbac-troubleshooting`.

## Investigate

Run every step: the goal is a complete, short list, not the first finding.

**0. Scope.** Review the whole cluster unless the user names a namespace; then add
`-n my-namespace` instead of `-A` to every namespaced command, and skip the cluster-wide
checks that do not concern it (nodes are still read for the spread check). Always skip
`kube-system`, `kube-public` and `kube-node-lease`. If other namespaces look like
add-ons installed with the cluster (for example `local-path-storage`, `cert-manager`,
`monitoring`), name them, say you treat them as system, and let the user say otherwise.

```bash
kubectl get namespaces --show-labels
kubectl get nodes -L topology.kubernetes.io/zone
kubectl get daemonsets -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{" "}{.spec.template.spec.containers[*].image}{"\n"}{end}'
```

**1. Reliability**: replicas, probes, requests, PodDisruptionBudgets and spread.

```bash
kubectl get deployments,statefulsets -A -o custom-columns='KIND:.kind,NAMESPACE:.metadata.namespace,NAME:.metadata.name,REPLICAS:.spec.replicas'
kubectl get deployments,statefulsets,daemonsets -A -o jsonpath='{range .items[*]}{.kind}{" "}{.metadata.namespace}/{.metadata.name}{"\n"}{range .spec.template.spec.containers[*]}{"  "}{.name}{" readiness="}{.readinessProbe}{" requests="}{.resources.requests}{"\n"}{end}{end}'
kubectl get pdb -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{" allowed="}{.status.disruptionsAllowed}{" healthy="}{.status.currentHealthy}/{.status.desiredHealthy}{" expected="}{.status.expectedPods}{" minAvailable="}{.spec.minAvailable}{" maxUnavailable="}{.spec.maxUnavailable}{"\n"}{end}'
kubectl get pods -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,OWNER:.metadata.ownerReferences[0].kind,OWNER_NAME:.metadata.ownerReferences[0].name,NODE:.spec.nodeName,PHASE:.status.phase'
```

**2. Security**: what pods may do, Pod Security labels, cluster-admin, NetworkPolicies
and image tags.

```bash
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{" owner="}{.metadata.ownerReferences[0].kind}/{.metadata.ownerReferences[0].name}{" pod.runAsNonRoot="}{.spec.securityContext.runAsNonRoot}{" pod.runAsUser="}{.spec.securityContext.runAsUser}{" hostNetwork="}{.spec.hostNetwork}{" hostPID="}{.spec.hostPID}{" hostIPC="}{.spec.hostIPC}{" hostPath="}{.spec.volumes[*].hostPath.path}{"\n"}{range .spec.containers[*]}{"  "}{.name}{" image="}{.image}{" privileged="}{.securityContext.privileged}{" allowPrivilegeEscalation="}{.securityContext.allowPrivilegeEscalation}{" runAsNonRoot="}{.securityContext.runAsNonRoot}{" runAsUser="}{.securityContext.runAsUser}{"\n"}{end}{end}'
kubectl get namespaces -o jsonpath='{range .items[*]}{.metadata.name}{" enforce="}{.metadata.labels.pod-security\.kubernetes\.io/enforce}{" warn="}{.metadata.labels.pod-security\.kubernetes\.io/warn}{"\n"}{end}'
kubectl get clusterrolebindings -o jsonpath='{range .items[*]}{.metadata.name}{" role="}{.roleRef.name}{" subjects="}{.subjects}{"\n"}{end}'
kubectl get rolebindings -A -o jsonpath='{range .items[?(@.roleRef.name=="cluster-admin")]}{.metadata.namespace}/{.metadata.name}{" subjects="}{.subjects}{"\n"}{end}'
kubectl get clusterroles -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.rules}{"\n"}{end}'
kubectl get networkpolicies -A
```

**3. Hygiene and cost**: volumes, Services, idle workloads, Jobs and CronJobs.

```bash
kubectl get pvc -A
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{" "}{.spec.volumes[*].persistentVolumeClaim.claimName}{"\n"}{end}'
kubectl get pv -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,CLAIM:.spec.claimRef.namespace,CLAIM_NAME:.spec.claimRef.name,RECLAIM:.spec.persistentVolumeReclaimPolicy,SIZE:.spec.capacity.storage'
kubectl get services -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,TYPE:.spec.type,CLUSTER-IP:.spec.clusterIP,SELECTOR:.spec.selector'
kubectl get endpointslices -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.labels.kubernetes\.io/service-name}{" ready="}{.endpoints[?(@.conditions.ready==true)].addresses}{"\n"}{end}'
kubectl get jobs -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{" owner="}{.metadata.ownerReferences[0].kind}{" failed="}{.status.failed}{" conditions="}{.status.conditions[*].type}{"\n"}{end}'
kubectl get cronjobs -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,SCHEDULE:.spec.schedule,SUSPEND:.spec.suspend,LAST_SCHEDULE:.status.lastScheduleTime,LAST_SUCCESS:.status.lastSuccessfulTime'
```

**4. Open the matching reference** for the field details and edge cases of a check:

| Group | Reference |
|---|---|
| Replicas, probes, requests, PDBs, spread over nodes and zones | [references/reliability.md](references/reliability.md) |
| securityContext, host access, Pod Security labels, RBAC, NetworkPolicies, image tags | [references/security.md](references/security.md) |
| PVCs, PVs, Services, LoadBalancers, idle workloads, Jobs, CronJobs | [references/hygiene.md](references/hygiene.md) |

## Read the results

Each check, what it means, and when it is fine (Kubernetes 1.37). Report a finding
once per workload (Deployment, StatefulSet, DaemonSet, CronJob), not once per pod: group
pods by their owner, and for a ReplicaSet name the Deployment it belongs to. A pod with
no owner (a debug pod someone started by hand, for example) is reported by its own name, as
a bare pod: nothing recreates it, which is a finding of its own.

### Reliability

- **One replica** (Deployment or StatefulSet, `replicas: 1`): the app is down while its
  pod is replaced by a drain, an upgrade or a crash. Fine for batch tools, dev
  namespaces and singletons by design (a controller with leader election, a database
  run as one instance on purpose). DaemonSets and Jobs are not counted.
- **No readiness probe**: the Service sends traffic to a pod as soon as it starts, and
  keeps sending it while the app cannot answer. A missing liveness probe is not a
  finding. Fine for workers that take no traffic through a Service.
- **No CPU or memory requests**: the scheduler places the pod as if it needs nothing,
  and it is the first to be evicted under node pressure (QoS BestEffort). Fine for
  rare one-off pods.
- **A PDB with `allowed=0` while every pod is healthy**: no pod it selects can be
  evicted, so a drain waits on it forever. Report it in one line and point to
  `k8s-upgrade-readiness`. **A PDB with `expected=0`**: it matches no pod; stale.
- **All replicas of a workload with 2 or more replicas on one node** (or in one zone,
  when nodes carry `topology.kubernetes.io/zone`): one node or zone failure takes the
  whole app down. On a one-node cluster this cannot be checked: put it in Skipped, not
  in the findings or the counts.

### Security

- **`privileged=true`**, **`hostNetwork`, `hostPID`, `hostIPC`** or a **`hostPath`
  volume**: the container can reach the node and everything on it. Fine for node agents
  that need it (CNI, CSI, log and metrics collectors), usually DaemonSets in an add-on
  namespace.
- **`allowPrivilegeEscalation` not `false`**, or **running as root** (`runAsNonRoot` not
  `true` at pod or container level and no non-zero `runAsUser`): a process that breaks
  out of the app gets more rights than it needs. Name it in the evidence even when the
  same container is privileged. The image may still set a non-root user; say that the
  field does not show it.
- **A namespace without `pod-security.kubernetes.io/enforce`**: nothing stops a
  privileged pod from being created there. Fine for system namespaces; a label `warn`
  or `audit` only reports.
- **`cluster-admin`, or a ClusterRole with `*` verbs on `*` resources, bound to a user or a
  group whose name does not start with `system:`, or to a ServiceAccount outside the
  system and add-on namespaces**: that subject can do anything, including read every
  Secret. Installer defaults (kubeadm's `kubeadm:cluster-admins` group, a managed
  cloud's admin group, a ServiceAccount of `kube-system` or of an add-on namespace) are
  fine if intended: name them as such, not as a problem.
- **A namespace with workloads and no NetworkPolicy**: every pod can reach every other
  pod. A finding only when the CNI enforces NetworkPolicy. Decide from the CNI's
  DaemonSet (step 0; an operator-installed Calico runs in `calico-system`, Flannel in
  `kube-flannel`): Cilium, Calico and Antrea enforce, and so does kindnet on current kind
  releases (seen on the 1.37 node image; on an old kind cluster, treat it as unknown);
  Flannel alone does not. On managed clusters it depends on an
  option (EKS `aws-node` only with its network policy agent, AKS only with a policy
  engine): unless you see that option, treat it as unknown. If you cannot tell, report
  "no NetworkPolicy; matters only if the CNI enforces them" in Skipped, not as a
  finding.
- **An image with `:latest` or no tag** (a `@sha256:` digest is fine): which version
  runs depends on when the node pulled it, and a rollback cannot go back to it.

### Hygiene and cost

- **A PVC that no pod mounts**: its volume is paid for and holds data nobody reads.
  Fine if a Job or a CronJob mounts it from time to time; check their templates.
- **A PV in phase `Released`**: its claim was deleted and `Retain` kept the volume. It
  is never bound again by itself.
- **A Service (not headless, not `ExternalName`) with no ready endpoints**: its selector
  matches no ready pod. Traffic to it fails. Fine if its app is scaled to 0 on purpose.
- **LoadBalancer Services**: list them for a second look (each one is a cloud load
  balancer and usually a public address); do not call them wrong.
- **A Deployment or StatefulSet at 0 replicas**, **a failed Job** (condition `Failed`,
  not owned by a CronJob that has since succeeded), **a CronJob that is suspended** or
  whose `LAST_SUCCESS` is older than several schedule periods: leftovers, or a task that
  stopped working without anyone noticing.

Report the result in this shape, findings ordered by impact within each group. Stay
quiet about what is fine: fewer findings with reasons beat a long list.

```text
Summary: Reliability 2, Security 3, Hygiene and cost 1 (scope: whole cluster)

Security
- Deployment my-namespace/my-app: privileged container and a hostPath volume (/var/log).
  Evidence: privileged=true, hostPath=/var/log. Why it matters: ... Fine when: ...
  Proposed fix: ... (below)

Skipped
- kube-system, kube-public, kube-node-lease; local-path-storage (treated as an add-on).
- ClusterRoleBindings: forbidden for this user (run: kubectl get clusterrolebindings).
```

## Proposed fix

Show each fix to the user; the agent runs none of them. Every finding belongs to the
owner of the object, and a fix made in the cluster is undone by the next deploy unless
the source (the manifest, the Helm values, the Git repository) changes too: prefer the
change in the source. Write each undo with the values you found.

Give a single-replica app a second pod:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl scale deployment my-app -n my-namespace --replicas=2
# Undo: kubectl scale deployment my-app -n my-namespace --replicas=1
```

Add a readiness probe and requests (use the app's real health path, port and usage).
A JSON patch `add` replaces the whole field: if the container already has some requests,
put them in the value too:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl patch deployment my-app -n my-namespace --type=json -p '[{"op": "add", "path": "/spec/template/spec/containers/0/readinessProbe", "value": {"httpGet": {"path": "/healthz", "port": 8080}}}, {"op": "add", "path": "/spec/template/spec/containers/0/resources/requests", "value": {"cpu": "100m", "memory": "128Mi"}}]'
# Undo: kubectl rollout undo deployment my-app -n my-namespace
```

Let one pod of a PDB be evicted:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl patch pdb my-app -n my-namespace --type=json -p '[{"op": "remove", "path": "/spec/minAvailable"}, {"op": "add", "path": "/spec/maxUnavailable", "value": 1}]'
# Undo: kubectl patch pdb my-app -n my-namespace --type=json -p '[{"op": "remove", "path": "/spec/maxUnavailable"}, {"op": "add", "path": "/spec/minAvailable", "value": 1}]'
```

Drop privileges from a container (only once its owner confirms the app runs without
them; a container that needs root fails to start). The patch replaces the container's
whole `securityContext`: copy the fields it already has into the value. A `hostPath`
volume found with it is removed in the source, with its volume mount:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl patch deployment my-app -n my-namespace --type=json -p '[{"op": "add", "path": "/spec/template/spec/containers/0/securityContext", "value": {"privileged": false, "allowPrivilegeEscalation": false, "runAsNonRoot": true, "capabilities": {"drop": ["ALL"]}}}]'
# Undo: kubectl rollout undo deployment my-app -n my-namespace
```

Enforce a Pod Security level on a namespace. Check first what it would refuse: the
server-side dry run below only prints warnings and changes nothing.

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl label --dry-run=server --overwrite namespace my-namespace pod-security.kubernetes.io/enforce=baseline
kubectl label namespace my-namespace pod-security.kubernetes.io/enforce=baseline
# Undo: kubectl label namespace my-namespace pod-security.kubernetes.io/enforce-
```

Remove a `cluster-admin` binding that is not needed (save it first; give the subject a
narrower role before, if it still needs some access):

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl get clusterrolebinding my-app-admin -o yaml > my-app-admin.yaml
kubectl delete clusterrolebinding my-app-admin
# Undo: kubectl create -f my-app-admin.yaml
```

Delete leftovers once their owner confirms nobody needs them:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl delete job my-job -n my-namespace
kubectl get service my-app -n my-namespace -o yaml > my-app-service.yaml
kubectl delete service my-app -n my-namespace
# Undo: re-run the Job from its source; kubectl create -f my-app-service.yaml (it asks for the same ClusterIP again, and fails if another Service took it: remove spec.clusterIP and spec.clusterIPs from the file to get a new one)
```

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl delete pvc my-data -n my-namespace
# Undo: not reversible. With reclaim policy Delete the volume and its data are deleted;
# with Retain the PV stays Released and needs an admin to bind it again.
```

Add a default-deny NetworkPolicy, and the allow rules the apps need, through their
owners: see [references/security.md](references/security.md). A `Released` PV is
deleted or bound again by an admin: see [references/hygiene.md](references/hygiene.md).

## Sources

Checked against the Kubernetes 1.37 documentation, and on a Kubernetes 1.37 kind
cluster:

- [Configuration Good Practices](https://kubernetes.io/docs/concepts/configuration/overview/).
- [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).
- [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
  and [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/).
- [Specifying a Disruption Budget](https://kubernetes.io/docs/tasks/run-application/configure-pdb/).
- [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
  and [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/).
- [Configure a Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/).
- [Role Based Access Control Good Practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/).
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
- [Images](https://kubernetes.io/docs/concepts/containers/images/): tags, digests and
  `imagePullPolicy`.
- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/):
  reclaim policies and the `Released` phase.
- [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) and
  [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/).
- That kindnet enforces NetworkPolicy was seen on the kind cluster: a default-deny
  policy stopped traffic that reached the pod before it.
