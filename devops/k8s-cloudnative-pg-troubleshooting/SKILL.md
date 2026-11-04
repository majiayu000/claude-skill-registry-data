---
name: k8s-cloudnative-pg-troubleshooting
description: >-
  Use when a CloudNativePG (CNPG) PostgreSQL Cluster in Kubernetes is not healthy: a
  Cluster stuck in "Setting up primary", "Creating a new replica" or "Waiting for the
  instances to become active", fewer ready instances than requested, an initdb or join
  pod that is Pending or in CreateContainerConfigError, PVCs that stay Pending, a
  bootstrap Secret that is missing, a replica that cannot be scheduled (pod
  anti-affinity, nodeSelector, taints), "Not enough disk space", failing WAL archiving
  or backups (ContinuousArchiving, LastBackupSucceeded False), a failover or switchover
  that does not finish, "Invalid cluster definition" or "Cluster is unrecoverable", and
  operator errors. Investigates with kubectl get, describe, events and logs, never
  reading Secrets, and proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, cloudnative-pg 1.30"
  verified-on: "2026-10-31"
---

# CloudNativePG troubleshooting

Find out why a CloudNativePG PostgreSQL cluster is not healthy, from the Cluster's
status, its pods, PVCs and events and the operator's log, and propose a fix. **Read
first, ask before changing.** Run the investigation commands freely. Run a command under
an "Ask first" line only after the user approves that exact command; if your
credentials do not allow it, give it to the user to run. Never run a "Proposed fix";
hand it to the user.

How CloudNativePG works, in the parts that fail:

- The **operator** (Deployment `cnpg-controller-manager`, usually in `cnpg-system`)
  reconciles every `Cluster` (`clusters.postgresql.cnpg.io`). It creates the instance
  pods and their PVCs directly, without a StatefulSet.
- Instances are numbered: `my-db-1`, `my-db-2`, and so on, each with its own PVC of the
  same name (plus `my-db-1-wal` with separate WAL storage). The first instance is made
  by an **initdb** (or recovery) job, pod `my-db-1-initdb-...`; each replica by a
  **join** job, pod `my-db-2-join-...`. A job's pod must run before the instance exists.
- One instance is the **primary**; the others stream from it. The Services `my-db-rw`
  (primary), `my-db-ro` (replicas) and `my-db-r` (any) point at them.
- The Cluster's `status.phase` is a sentence ("Cluster in healthy state", "Setting up
  primary") that says what the operator is doing now; `status.phaseReason` sometimes
  says why.

The commands use placeholders: `my-namespace`, `my-db` (the Cluster) and `my-db-1`,
`my-db-2` (its instances). Replace them with the real names. Write the kinds with their
group (`clusters.postgresql.cnpg.io`, `backups.postgresql.cnpg.io`): other projects
define `clusters` and `backups` too. The built-in `view` role cannot read CloudNativePG's
objects (it ships no read role); if they are forbidden, say so and ask the user for them.

**Never read Secrets.** Not `my-db-app` or `my-db-superuser` (passwords and connection
strings), not the certificates, not a bootstrap or backup credentials Secret the
Cluster names. Do not list them either: listing Secrets returns every Secret in the
namespace with its data, even when you print only the names. Whether a Secret is missing shows in the
pod's events (`secret "..." not found`); that event is the evidence.
Do not connect to PostgreSQL and do not run `psql` in a pod. If the user has the `cnpg`
kubectl plugin, its `status` command gives a summary they can paste; you do not need it.

## When to use

- `kubectl get clusters.postgresql.cnpg.io -A` shows a status other than `Cluster in
  healthy state`, or `READY` lower than `INSTANCES`.
- A new Cluster never gets a primary, or a scaled-up Cluster never gets its replica.
- Pods of the Cluster are `Pending`, crash, or the `-initdb` or `-join` pod fails.
- Backups or WAL archiving fail, or a failover or switchover hangs.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- PVCs stay `Pending` for a reason outside the Cluster (the provisioner, CSI driver,
  quota, a volume that does not attach): `k8s-storage-troubleshooting`.
- Pods cannot be placed for node reasons (nodes NotReady, taints you did not expect,
  node pressure): `k8s-node-troubleshooting`.
- Image pulls fail, or containers crash for reasons outside PostgreSQL:
  `k8s-workload-troubleshooting`.
- The operator cannot reach the instances (`Cannot extract Pod status`, `i/o timeout`
  to port 8000) and NetworkPolicies are involved: `k8s-network-troubleshooting`.
- Applying a Cluster is refused by a webhook you did not expect:
  `k8s-api-troubleshooting`.
- Backups go through Velero rather than CloudNativePG: `k8s-velero-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the Clusters and their phase.**

```bash
kubectl get clusters.postgresql.cnpg.io -A
kubectl get clusters.postgresql.cnpg.io my-db -n my-namespace -o jsonpath='{.status.phase}{" | "}{.status.phaseReason}{"\ninstances="}{.spec.instances}{" ready="}{.status.readyInstances}{" primary="}{.status.currentPrimary}{" target="}{.status.targetPrimary}{"\n"}{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}'
kubectl get clusters.postgresql.cnpg.io my-db -n my-namespace -o jsonpath='{.status.instancesStatus}{"\nhealthy="}{.status.healthyPVC}{" initializing="}{.status.initializingPVC}{" dangling="}{.status.danglingPVC}{" unusable="}{.status.unusablePVC}{"\n"}'
```

**2. See the pods, PVCs and jobs of the Cluster**, and read any pod that is not Running
and Ready.

```bash
kubectl get pods,pvc,jobs -n my-namespace -l cnpg.io/cluster=my-db -o wide
kubectl describe pod my-db-1 -n my-namespace
kubectl get events -n my-namespace --sort-by=.lastTimestamp
```

The job pods are named after the instance they make (`my-db-1-initdb-...`,
`my-db-2-join-...`); describe the one that is not Completed.

**3. Read how the Cluster asks for storage, bootstrap and placement.**

```bash
kubectl get clusters.postgresql.cnpg.io my-db -n my-namespace -o jsonpath='storage: {.spec.storage}{"\nwal: "}{.spec.walStorage}{"\nbootstrap: "}{.spec.bootstrap}{"\naffinity: "}{.spec.affinity}{"\nresources: "}{.spec.resources}{"\nimage: "}{.spec.imageName}{" catalog="}{.spec.imageCatalogRef}{"\n"}'
kubectl get storageclasses
kubectl get nodes -o wide
```

**4. Read the logs**: the operator's for the Cluster, and the instance's or job's own.

```bash
kubectl logs deployment/cnpg-controller-manager -n cnpg-system --since=1h | grep '"name":"my-db"' | grep -v '"level":"info"' | tail -n 30
kubectl logs my-db-1 -n my-namespace -c postgres --tail=50
kubectl logs my-db-2-join-abcde -n my-namespace --tail=50
```

Instance logs are JSON lines from the instance manager and PostgreSQL; `"level":"error"`
and PostgreSQL's `FATAL` and `PANIC` lines matter.

**5. For backups and WAL archiving**: the conditions from step 1, then the Backup
objects.

```bash
kubectl get backups.postgresql.cnpg.io,scheduledbackups.postgresql.cnpg.io -n my-namespace
kubectl get backups.postgresql.cnpg.io -n my-namespace -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.phase}{" method="}{.spec.method}{" "}{.status.error}{"\n"}{end}'
kubectl get clusters.postgresql.cnpg.io my-db -n my-namespace -o jsonpath='{.spec.backup}{"\n"}{.spec.plugins}{"\n"}'
```

## Read the results

**Phases** (`status.phase`, from the operator's source):

- **`Setting up primary`** for minutes on a new Cluster: the first instance is not made
  yet. Look at the `-initdb` pod (or the recovery pod) and the PVC `my-db-1`.
- **`Creating a new replica`**: a `-join` pod is not done; look at it and its PVC.
- **`Waiting for the instances to become active`**: an instance pod exists but is not
  ready; read its log.
- **`Failing over`**, **`Switchover in progress`**: the operator is promoting another
  instance; it is stuck if `targetPrimary` stays different from `currentPrimary`.
- **`Invalid cluster definition`**, **`Unable to create required cluster objects`**,
  **`Cluster has incomplete or invalid image catalog`**: the spec or what it refers to;
  `phaseReason` and the operator's log say what.
- **`Cluster is unrecoverable and needs manual intervention`**: the operator stopped
  acting on its own; read `phaseReason` and hand it to the user.
- **`Not enough disk space`**: a volume, often the WAL volume, is full and the instance
  crash-loops.
- The condition `Initialized` can read `True` (`BootstrapCompleted`) while the first
  instance is still being made (seen on 1.30.1). Do not take it as proof that a primary
  exists; `currentPrimary` and the pods are.

**Pods and PVCs.**

- **PVC `Pending`, event `ProvisioningFailed: storageclass.storage.k8s.io "fast-ssd" not
  found`**, and the job pod `Pending` with `pod has unbound immediate
  PersistentVolumeClaims`: `spec.storage.storageClass` (or `walStorage.storageClass`)
  names a class that does not exist. Compare with `kubectl get storageclasses`.
- **Job pod `CreateContainerConfigError`, event `Error: secret "my-db-credentials" not
  found`**: `spec.bootstrap.initdb.secret` (the owner's password), the superuser
  Secret, or a `postInitSQLRefs` Secret names a Secret that does not exist in the
  namespace. The event is the proof; do not look for the Secret yourself. The pod waits,
  and starts once the Secret exists. The Secret must be of type
  `kubernetes.io/basic-auth`, with a `username` equal to the owner (`postgres` for the
  superuser).
- **Pod `Pending`, `didn't match pod anti-affinity rules`**: `affinity.podAntiAffinityType:
  required` (the default is `preferred`) with fewer suitable nodes than instances. Each
  instance needs its own node (its own zone with `topologyKey:
  topology.kubernetes.io/zone`). Other `FailedScheduling` reasons: a `nodeSelector` or
  tolerations in `spec.affinity` that match no node, or requests in `spec.resources`
  that no node can fit.
- **A replica that never catches up, `could not receive data from WAL stream`, or
  `pg_rewind: error: could not open file`**: the WAL it needs is gone from the primary
  and there is no backup to fetch it from. The replica has to be rebuilt (proposed fix).
- **Operator log `Cannot extract Pod status` with `i/o timeout` to port 8000**, and
  `Instance Status Extraction Error: HTTP communication issue`: the operator cannot
  reach the instance manager, usually a NetworkPolicy.
- **The initdb pod hangs with `error while waiting for the API server to be reachable`**:
  the job cannot reach the API server (network, or an injected sidecar such as Istio's).

**Backups and archiving.**

- **`ContinuousArchiving` `False`, reason `ContinuousArchivingFailing`**: WAL files are
  not reaching the object store; the instance log names the error (credentials,
  bucket, endpoint). Archiving is done either by the Barman Cloud plugin
  (`spec.plugins`, the recommended way) or natively through the deprecated
  `spec.backup.barmanObjectStore`; with the plugin, its own objects and logs hold the
  details.
- **`LastBackupSucceeded` `False`**: the latest Backup object is `failed`; its
  `status.error` says why.

## Proposed fix

A new Cluster that never got its first instance stores no data yet. If its storage class
is wrong, the simplest fix is to delete and recreate it with the right
`spec.storage.storageClass` (an existing PVC keeps its class, so a patch alone does not
help):

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl delete clusters.postgresql.cnpg.io my-db -n my-namespace
kubectl apply -f my-db.yaml
# Undo: kubectl apply -f the saved original manifest (the old Cluster had no data: its first instance was never created)
```

A missing bootstrap Secret: the user creates it the way they manage Secrets (GitOps,
External Secrets, or by hand), of type `kubernetes.io/basic-auth` with `username` equal
to the owner (`app` here) and a password they choose. Never ask for the password in the
chat, and do not write the Secret's command for them. The waiting job pod starts by
itself once the Secret exists. A Cluster that does not need a chosen password can drop
`bootstrap.initdb.secret` (recreate it, as above) and let the operator generate one in
`my-db-app`.

A replica that cannot be placed because anti-affinity is `required` and there are too
few nodes: the fix that keeps the guarantee is more nodes (or zones), which is the
platform team's change. Do not propose switching to `preferred` on the running Cluster
as a quick fix: the waiting join pod, its PVC and the running primary keep the old
rule, so the replica stays Pending (seen on 1.30.1, where the Cluster then stayed in
"Waiting for the instances to become active"). For a Cluster that holds no data yet, the
user can recreate it with `podAntiAffinityType: preferred` or fewer instances, as with
the storage class above.

Rebuilding a replica that cannot catch up (it deletes that replica's data, which the
operator then copies again from the primary; never on the primary):

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl delete pod/my-db-2 pvc/my-db-2 -n my-namespace
# Undo: none; the operator re-creates the replica from the primary
```

## Sources

- [Troubleshooting](https://cloudnative-pg.io/docs/1.30/troubleshooting/) (known
  issues: storage full, Pending pods, replicas out of sync, network policies, bootstrap
  job hangs).
- [Bootstrap](https://cloudnative-pg.io/docs/1.30/bootstrap/) (initdb, the owner's
  basic-auth Secret).
- [Storage](https://cloudnative-pg.io/docs/1.30/storage/) and
  [scheduling](https://cloudnative-pg.io/docs/1.30/scheduling/) (anti-affinity defaults,
  `podAntiAffinityType: required`).
- [Replication](https://cloudnative-pg.io/docs/1.30/replication/),
  [failover](https://cloudnative-pg.io/docs/1.30/failover/) and
  [WAL archiving](https://cloudnative-pg.io/docs/1.30/wal_archiving/).
- [API reference](https://cloudnative-pg.io/docs/1.30/cloudnative-pg.v1/) and the
  phase and condition names in
  [cluster_types.go](https://github.com/cloudnative-pg/cloudnative-pg/blob/v1.30.1/api/v1/cluster_types.go).
- Messages seen on kind with CloudNativePG 1.30.1 and PostgreSQL 18.
