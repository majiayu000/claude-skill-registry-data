---
name: yugabytedb-k8s-cilium
description: >
  Set up a Cilium Cluster Mesh with Multi-Cluster Services (MCS-API) between two Kubernetes
  clusters and deploy one independent YugabyteDB universe per cluster with the yugabyte Helm
  chart, so the universes can be joined with xCluster replication (source -> target / DR).
  Covers kind cluster configs with non-overlapping CIDRs, cilium install with clustermesh.mcsapi,
  clustermesh enable/connect, Helm values (multicluster.createServiceExports, kubernetesClusterId,
  masterAddresses, totalMasters), svc.clusterset.local DNS checks, and yb-admin xCluster setup.
  Use when the user mentions Cilium Cluster Mesh with YugabyteDB, xCluster on Kubernetes across
  clusters, cross-cluster YugabyteDB on kind, ServiceExport/ServiceImport for yb-masters or
  yb-tservers, or clusterset.local addresses for YugabyteDB. Does NOT cover the YugabyteDB
  Kubernetes Operator or YBA-managed DR (use yb-k8s-operator), or a single universe stretched
  across clusters.
---

# YugabyteDB xCluster over a Cilium Cluster Mesh

Two Kubernetes clusters (`c1` = source, `c2` = target), joined by Cilium Cluster Mesh with MCS-API.
Each cluster runs its **own** universe. The mesh lets the target's tservers reach the source's
masters and tservers directly, which xCluster needs: target tservers pull changes straight from
source tservers, so every source pod address must be resolvable and routable from the target.

```
kind-c1 (Cilium id 1, pods 10.10/16)          kind-c2 (Cilium id 2, pods 10.20/16)
  yb-master-0.c1.yb-masters.<ns>.svc.clusterset.local   <— MCS-API —>   yb-master-0.c2...
  yb-tserver-0.c1.yb-tservers.<ns>.svc.clusterset.local                 yb-tserver-0.c2...
        source universe  ───────── xCluster ─────────>  target universe
```

Bundled files (paths relative to this skill):

| File | Purpose |
|---|---|
| `assets/kind-c1.yaml`, `assets/kind-c2.yaml` | kind clusters, no default CNI, unique pod/service CIDRs |
| `scripts/mesh-up.sh` | Creates both clusters, installs Cilium, enables and connects the mesh (idempotent) |
| `assets/values-c1.yaml`, `assets/values-c2.yaml` | yugabyte Helm values for each universe |
| `scripts/check-mcs-dns.sh` | Checks cross-cluster DNS and TCP to every master/tserver |
| `references/troubleshooting.md` | Symptoms → causes |

Verified with yugabyte chart 2026.1.2, Cilium 1.20.3 (cilium-cli 0.20.x), kind 0.33.
Before using with other versions, run `helm show values` and check that the keys still exist.

## Invariants (most failures come from breaking one of these)

1. **Unique per cluster:** Cilium `cluster.name`, `cluster.id` (1–255), pod CIDR, service CIDR.
   **Shared across clusters:** the `cilium-ca` secret. Copy it from c1 before installing Cilium on c2.
2. **Pod CIDR agreement:** kind `podSubnet` == Cilium `ipam.operator.clusterPoolIPv4PodCIDRList`.
3. **`multicluster.kubernetesClusterId` == Cilium `cluster.name`.** That ID is the `<cluster>`
   label in `<pod>.<cluster>.<svc>.<ns>.svc.clusterset.local`.
4. **`masterAddresses` lists exactly the masters that exist, using the clusterset names.** With
   `multicluster.createServiceExports: true` and `oldNamingStyle: true`, the chart sets each
   master's `--server_broadcast_addresses` to `${HOSTNAME}.<clusterId>.yb-masters.${NAMESPACE}.svc.clusterset.local:7100`.
   `masterAddresses` must use the same names, or masters can't recognise themselves in the list.
5. **`replicas.totalMasters` == number of entries in `masterAddresses`.** When `isMultiAz: true`,
   the chart sets `--replication_factor` from `totalMasters`, which defaults to **3**. If you set
   `replicas.master: 1` and leave `totalMasters` at its default, the universe expects RF 3 and
   never becomes healthy.
6. **The namespace must be the same in both clusters** and must be global in the mesh. Cilium's
   `clustermesh.defaultGlobalNamespace` defaults to `true`; if it was turned off, annotate the
   namespace with `clustermesh.cilium.io/global=true`.
7. `${NAMESPACE}` / `${HOSTNAME}` in values stay **literal**. The pod's startup script expands
   them with `envsubst`, so don't let your shell expand them (use `'…'` heredocs).

## Workflow

### 1. Prerequisites

`docker`, `kind`, `kubectl`, `helm`, `cilium` CLI. For two clusters plus two RF1 universes, give
Docker Desktop at least about 6 CPU and 10 GiB of memory. On Linux hosts, raise
`fs.inotify.max_user_instances` (for example to 512), or kind nodes fail with "too many open files".

For real (non-kind) clusters, skip kind. Use the same Cilium flags with each cluster's actual
pod CIDR, and make the node and pod networks routable between clusters. Expose clustermesh-apiserver
with `--service-type LoadBalancer` instead of NodePort.

### 2. Build the mesh

```bash
scripts/mesh-up.sh            # add --skip-connectivity-test to save ~10 minutes
```

The script runs these steps (run them by hand if the user wants to see each one):

```bash
kind create cluster --name c1 --config assets/kind-c1.yaml
kind create cluster --name c2 --config assets/kind-c2.yaml

cilium install --context kind-c1 \
  --set cluster.name=c1 --set cluster.id=1 \
  --set ipam.operator.clusterPoolIPv4PodCIDRList=10.10.0.0/16 \
  --set clustermesh.mcsapi.enabled=true \
  --set clustermesh.mcsapi.corednsAutoConfigure.enabled=true \
  --set clustermesh.enableEndpointSliceSynchronization=true
cilium status --context kind-c1 --wait

# Share c1's CA with c2 BEFORE installing Cilium on c2
kubectl --context kind-c1 -n kube-system get secret cilium-ca -o yaml \
  | sed -E '/^  (resourceVersion|uid|creationTimestamp):/d' \
  | kubectl --context kind-c2 create -f -

# then install on c2: cluster.name=c2, cluster.id=2, CIDR 10.20.0.0/16

cilium clustermesh enable --context kind-c1 --service-type NodePort
cilium clustermesh enable --context kind-c2 --service-type NodePort
cilium clustermesh connect --context kind-c1 --destination-context kind-c2   # bidirectional
cilium clustermesh status --context kind-c1 --wait
cilium connectivity test --context kind-c1 --multi-cluster kind-c2
```

Shared CA: all clusters in the mesh must use the same `cilium-ca`. Then the certificates each
cluster issues (clustermesh-apiserver, Hubble) are trusted across the mesh, and cross-cluster mTLS
and Hubble Relay work. Copy it after Cilium is on c1 and **before** `cilium install` on c2. The copy
keeps the secret's Helm labels and annotations, so Helm adopts it rather than generating a new CA.
The `sed` drops server-set metadata, which `kubectl create` may reject. If c2 already has Cilium
with its own CA, run `cilium uninstall --context kind-c2`, copy the secret, and reinstall.

Flag notes:
- `clustermesh.mcsapi.enabled`: Cilium watches ServiceExport and creates matching ServiceImport plus
  derived services. Since 1.18, `clustermesh.mcsapi.installCRDs` (default `true`) installs the
  MCS-API CRDs. On older Cilium, apply the `sigs.k8s.io/mcs-api` CRDs first.
- `corednsAutoConfigure`: adds the `clusterset.local` zone to CoreDNS. This needs CoreDNS ≥ 1.12.2.
  On older CoreDNS, `*.svc.clusterset.local` fails to resolve.
- `enableEndpointSliceSynchronization`: syncs EndpointSlices across clusters. YugabyteDB's
  `yb-masters` and `yb-tservers` are headless, and per-pod DNS records depend on these slices.

Done when `cilium clustermesh status` shows both clusters connected and the connectivity test passes.

### 3. Deploy the universes

```bash
NS=yb
helm repo add yugabytedb https://charts.yugabyte.com && helm repo update yugabytedb
for c in c1 c2; do
  kubectl --context kind-$c create namespace $NS
  helm install yb-$c yugabytedb/yugabyte -n $NS --kube-context kind-$c \
    -f assets/values-$c.yaml --wait --timeout 15m
done
```

Points to tell the user about the values files:
- They are **RF1 demo** universes. For RF3, set `replicas.master: 3`, `replicas.tserver: 3`,
  `replicas.totalMasters: 3`, and list three clusterset master addresses (`yb-master-0/1/2.<c>.yb-masters…`).
  Remove the `resource`/`storage` overrides on real hardware.
- `isMultiAz: true` is only there so the chart uses `masterAddresses` and `totalMasters`. Each
  cluster still runs a separate universe. Never put the other cluster's masters into
  `masterAddresses`; that would build one stretched universe, not xCluster.
- Check that the universe formed before moving on:
  `kubectl --context kind-c1 -n $NS exec yb-master-0 -c yb-master -- yb-admin --master_addresses yb-master-0.c1.yb-masters.$NS.svc.clusterset.local:7100 list_all_tablet_servers`

### 4. Verify cross-cluster reachability

```bash
scripts/check-mcs-dns.sh yb 1 1     # namespace, masters, tservers
```

Each direction must resolve and connect to every remote master (7100) and tserver (9100).
`kubectl get serviceimports -n yb` should list `yb-masters` and `yb-tservers` in both clusters.
If anything fails, stop here and go to `references/troubleshooting.md`. Don't continue to xCluster.

### 5. Configure xCluster

Run `yb-admin` from a master pod. The names below assume namespace `yb` and RF1:

```bash
SRC=yb-master-0.c1.yb-masters.yb.svc.clusterset.local:7100
TGT=yb-master-0.c2.yb-masters.yb.svc.clusterset.local:7100
src() { kubectl --context kind-c1 -n yb exec yb-master-0 -c yb-master -- yb-admin --master_addresses $SRC "$@"; }
tgt() { kubectl --context kind-c2 -n yb exec yb-master-0 -c yb-master -- yb-admin --master_addresses $TGT "$@"; }
```

**Transactional, database-scoped xCluster, semi-automatic mode (YSQL):**

1. Create the database and an identical schema on **both** universes, while the source is still empty:
   `sql() { kubectl --context kind-$1 -n yb exec yb-tserver-0 -c yb-tserver -- ysqlsh -h yb-tserver-0.$1.yb-tservers.yb.svc.clusterset.local -d $2 -c "$3"; }`
   then `sql c1 yugabyte 'CREATE DATABASE app'`, `sql c1 app 'CREATE TABLE …'`, and the same for `c2`.
2. `src create_xcluster_checkpoint app_rg app`. It reports whether a bootstrap is needed. For empty
   tables it only asks you to create the same objects on the target (done in step 1).
   If the source already has data, back up and restore the database to the target first.
3. `src setup_xcluster_replication app_rg $TGT`
4. Verify: `tgt get_replication_status` (no errors) and `tgt get_xcluster_safe_time include_lag_and_skew`
   (lag around 1 s). Insert rows on the source and count them on the target.
5. Later DDL: run it on the source first, then on the target (see the YugabyteDB semi-automatic docs
   for the order per statement type).

**Automatic mode (`automatic_ddl_mode`, v2025.1+) always requires a full copy.** Even for an empty
database, run `create_xcluster_checkpoint app_rg app automatic_ddl_mode`, then a **distributed
backup of the source database restored to the target**, then `setup_xcluster_replication`. Creating
the target database by hand isn't enough, because Postgres OIDs won't match. If you skip the
restore, setup still succeeds, but the first replicated DDL stalls: xCluster safe time freezes, the
table never appears on the target, and the stall also blocks other replication groups on the same
tservers. Recover with `src drop_xcluster_replication <group> $TGT`. A Helm-only deployment has no
built-in backup target, so use YBA (DrConfig via `yb-k8s-operator`) or set up distributed backups
before choosing automatic mode.

**Table-level (non-transactional, or YCQL):** get the table IDs with `src list_tables include_table_id`
and the source universe UUID with `src get_universe_config`, then run
`tgt setup_universe_replication <source_uuid>_<name> $SRC <table_id,…>`.

Planned switchover, failover and DR orchestration are out of scope. For YBA-managed DR, use
the `yb-k8s-operator` (DrConfig) or `yba-api` skills.

### 6. Teardown

```bash
helm uninstall yb-c1 -n yb --kube-context kind-c1; helm uninstall yb-c2 -n yb --kube-context kind-c2
kind delete cluster --name c1; kind delete cluster --name c2
```
PVCs survive `helm uninstall`. Delete them, or delete the namespace, before reinstalling with
different master addresses, because old master data pins the previous config.

## Reviewing a user's own config

When the user pastes their kind, Cilium or Helm config, check each invariant above. The most common mistakes:
- `replicas.master` is lowered without setting `replicas.totalMasters`, so RF stays at 3.
- `masterAddresses` lists more masters than exist, or uses `svc.cluster.local` names while
  ServiceExports are on.
- `kubernetesClusterId` doesn't match Cilium `cluster.name`.
- The Cilium pod CIDR doesn't match kind `podSubnet`, or the two clusters' CIDRs overlap.
- Automatic-DDL xCluster set up with a hand-created target database instead of a backup/restore.
