---
name: yugabytedb-k8s-submariner
description: >
  Connect two Kubernetes clusters with Submariner (broker, gateway, Lighthouse service discovery)
  and deploy one independent YugabyteDB universe per cluster with the yugabyte Helm chart, so the
  universes can be joined with xCluster replication (source -> target / DR). Covers kind cluster
  configs with non-overlapping CIDRs, subctl deploy-broker / join (clusterid, cable driver, NAT-T,
  gateway labelling), Helm values (multicluster.createServiceExports, kubernetesClusterId,
  masterAddresses, totalMasters), svc.clusterset.local DNS checks, subctl verify/diagnose, and
  yb-admin xCluster setup. Use when the user mentions Submariner or Lighthouse with YugabyteDB,
  subctl with yb-masters / yb-tservers, xCluster between Kubernetes clusters without a shared CNI
  mesh, or clusterset.local addresses with Submariner. For Cilium Cluster Mesh use
  yugabytedb-k8s-cilium. Does NOT cover the YugabyteDB Kubernetes Operator or YBA-managed DR (use
  yb-k8s-operator), or a single universe stretched across clusters.
---

# YugabyteDB xCluster over Submariner

Two Kubernetes clusters (`s1` = source, `s2` = target) joined by Submariner. Each cluster runs its
**own** universe. Submariner gives pod-to-pod routing between the clusters through a gateway
node on each side, and Lighthouse publishes exported services under `clusterset.local`. xCluster
needs both: target tservers pull changes straight from source tservers, so every source pod
address must be resolvable and routable from the target.

```
kind-s1 (pods 10.30/16, svc 10.130/16)                 kind-s2 (pods 10.40/16, svc 10.140/16)
  broker (submariner-k8s-broker ns)
  gateway: s1-worker  <════ IPsec / WireGuard / VXLAN tunnel ════>  gateway: s2-worker
  yb-master-0.s1.yb-masters.<ns>.svc.clusterset.local   <— Lighthouse —>   yb-master-0.s2...
  yb-tserver-0.s1.yb-tservers.<ns>.svc.clusterset.local                    yb-tserver-0.s2...
        source universe  ─────────────── xCluster ───────────────>  target universe
```

Bundled files (paths relative to this skill):

| File | Purpose |
|---|---|
| `assets/kind-s1.yaml`, `assets/kind-s2.yaml` | kind clusters (default kindnet CNI), unique pod/service CIDRs, one worker for the gateway |
| `scripts/submariner-up.sh` | Creates both clusters, deploys the broker, labels gateways, joins both clusters (idempotent) |
| `assets/rp-filter-ds.yaml` | DaemonSet that keeps `rp_filter` loose on every node (invariant 8) |
| `assets/values-s1.yaml`, `assets/values-s2.yaml` | yugabyte Helm values for each universe |
| `scripts/check-mcs-dns.sh` | Checks cross-cluster DNS and TCP to every master/tserver |
| `references/troubleshooting.md` | Symptoms → causes |

Verified end to end with yugabyte chart 2026.1.2, Submariner 0.25.0 (libreswan cable), kind 0.33
on macOS: tunnel up, both universes formed, cross-cluster DNS/TCP from gateway and
non-gateway nodes, and semi-automatic xCluster replicating rows with sub-second lag. Automatic-DDL mode was not verified (it needs a
backup/restore; see step 5). Before using with other versions, run `helm show values
yugabytedb/yugabyte` and `subctl join --help` and check that the keys and flags still exist.

## Invariants (most failures come from breaking one of these)

1. **Unique per cluster:** Submariner `--clusterid` (a DNS-1123 label), pod CIDR, service CIDR.
   Neither may overlap the other cluster's, or the node network. If they must overlap, deploy the
   broker with `--globalnet` (see below) instead.
2. **CIDRs given to `subctl join` match the cluster:** `--clustercidr` == kind `podSubnet`,
   `--servicecidr` == kind `serviceSubnet`. subctl auto-detects them on most clusters; pass them
   explicitly anyway so a wrong guess fails loudly.
3. **`multicluster.kubernetesClusterId` == `subctl join --clusterid`.** That ID is the `<cluster>`
   label in `<pod>.<cluster>.<svc>.<ns>.svc.clusterset.local`.
4. **`masterAddresses` lists exactly the masters that exist, using the clusterset names.** With
   `multicluster.createServiceExports: true` and `oldNamingStyle: true`, the chart sets each
   master's `--server_broadcast_addresses` to `${HOSTNAME}.<clusterId>.yb-masters.${NAMESPACE}.svc.clusterset.local:7100`.
   `masterAddresses` must use the same names, or masters can't recognise themselves in the list.
5. **`replicas.totalMasters` == number of entries in `masterAddresses`.** When `isMultiAz: true`,
   the chart sets `--replication_factor` from `totalMasters`, which defaults to **3**. If you set
   `replicas.master: 1` and leave `totalMasters` at its default, the universe expects RF 3 and
   never becomes healthy.
6. **The namespace must be the same in both clusters.** Lighthouse merges a ServiceExport only
   with exports of the same name in the same namespace, and the clusterset names embed it.
7. **kube-proxy runs in iptables mode.** Submariner does not support IPVS. kind's default is iptables.
8. **Loose reverse-path filtering (`rp_filter=2`) on every node.** Pods on non-gateway nodes reach the
   other cluster over `vx-submariner`, but replies arrive from the gateway on `eth0`. The kernel
   applies the stricter of `net.ipv4.conf.all` and the interface value, and Submariner only loosens
   `vx-submariner` and the CNI interface. So when `all=1` (inherited from the host kernel), the replies
   are dropped. Only pods on the gateway node keep working, which hides the problem until a pod lands
   elsewhere. Submariner has no option for this. `assets/rp-filter-ds.yaml` (applied by the script)
   is a privileged DaemonSet that sets it on every node and keeps it set across node restarts.
   On real clusters, set it in the node OS (`/etc/sysctl.d`) or node image instead.
9. `${NAMESPACE}` / `${HOSTNAME}` in values stay **literal**. The pod's startup script expands
   them with `envsubst`, so don't let your shell expand them (use `'…'` heredocs).

## Workflow

### 1. Prerequisites

`docker`, `kind`, `kubectl`, `helm`. On kind, **don't run a host-installed `subctl`**: the script runs
`subctl` from the `quay.io/submariner/subctl:<version>` image on the docker `kind` network with kind's
internal kubeconfigs (`kind get kubeconfig --internal`). A host-run `subctl deploy-broker` records the
broker URL as `https://127.0.0.1:<port>`, which the other cluster's pods can't reach, and on macOS
the host binary may also fail with `x509: certificate is not trusted` or `connect: no route to host`.
For real clusters, install `subctl` on the host (`curl -Ls https://get.submariner.io | VERSION=0.25.0 bash`,
lands in `~/.local/bin`; ask before installing it for the user). For two clusters (2 nodes each) plus two RF1 universes, give Docker Desktop at least about
6 CPU and 10 GiB of memory. On Linux hosts, raise `fs.inotify.max_user_instances` (for example to
512), or kind nodes fail with "too many open files".

For real (non-kind) clusters, skip kind. Open UDP 4500 (IPsec NAT-T) and 4490 (NAT discovery)
between the gateway nodes, and UDP 4800 between all nodes inside each cluster (non-gateway nodes
tunnel to their gateway on it). Keep `--natt` at its default (on) when the gateways sit behind
NAT, as on most clouds. Calico needs VXLAN mode; see `references/troubleshooting.md`.

### 2. Connect the clusters

```bash
scripts/submariner-up.sh            # add --skip-verify to save several minutes
```

The script runs these steps (run them by hand if the user wants to see each one):

```bash
kind create cluster --name s1 --config assets/kind-s1.yaml
kind create cluster --name s2 --config assets/kind-s2.yaml

# subctl in a container on the kind network, with internal kubeconfigs (https://s1-control-plane:6443)
kind get kubeconfig --internal --name s1 > k1; kind get kubeconfig --internal --name s2 > k2
KUBECONFIG=k1:k2 kubectl config view --flatten > kubeconfig-internal
subctl() { docker run --rm --network kind --user "$(id -u)" -v "$PWD:/work" -w /work \
  -e KUBECONFIG=/work/kubeconfig-internal -e HOME=/work quay.io/submariner/subctl:0.25.0 /subctl "$@"; }

subctl deploy-broker --context kind-s1          # writes ./broker-info.subm (contains the IPsec PSK)

kubectl --context kind-s1 apply -f assets/rp-filter-ds.yaml   # loose rp_filter on every node
kubectl --context kind-s2 apply -f assets/rp-filter-ds.yaml

kubectl --context kind-s1 label node s1-worker submariner.io/gateway=true
subctl join broker-info.subm --context kind-s1 --clusterid s1 \
  --clustercidr 10.30.0.0/16 --servicecidr 10.130.0.0/16 \
  --natt=false --label-gateway=false
# same for s2: s2-worker, --clusterid s2, 10.40.0.0/16, 10.140.0.0/16

subctl show connections --context kind-s1        # STATUS: connected
subctl verify --context kind-s1 --tocontext kind-s2 --only connectivity,service-discovery --verbose
```

Flag notes:
- The broker is just a namespace of CRDs that both clusters sync through. It can live on either
  cluster or a third one. `broker-info.subm` holds credentials and the IPsec PSK: don't commit it.
- `--natt=false`: kind nodes share the docker `kind` network, so there's no NAT between gateways.
- `--cable-driver`: `libreswan` (IPsec, default), `wireguard`, or `vxlan` (unencrypted). If the
  IPsec tunnel won't come up on a Docker Desktop host, rerun with `CABLE_DRIVER=vxlan`.
- `--label-gateway=false` stops join from prompting for a gateway node; the label is applied first.
- Lighthouse adds a `clusterset.local` forward to the cluster's CoreDNS during join.

The gateway, route-agent and Lighthouse pods appear a minute or two after `join` returns (image
pulls); until then `subctl show connections` says "No gateways detected" or "No connections found".
Done when `subctl show connections` shows `connected` from both sides and `subctl verify` passes.
If not, run `subctl diagnose all --context kind-s1` (and for `kind-s2`) before continuing.

### 3. Deploy the universes

```bash
NS=yb
helm repo add yugabytedb https://charts.yugabyte.com && helm repo update yugabytedb
for c in s1 s2; do
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
- The chart's `ServiceExport`s use `multicluster.x-k8s.io/v1alpha1`, which is what Submariner
  serves. Check with `kubectl get crd serviceexports.multicluster.x-k8s.io`.
- The masters resolve their **own** clusterset name at startup. The chart's headless services set
  `publishNotReadyAddresses: true`, and Lighthouse (0.16+) publishes not-ready pods for such
  services, so this works. On older Submariner the masters can deadlock waiting for DNS.
- Check that the universe formed before moving on:
  `kubectl --context kind-s1 -n $NS exec yb-master-0 -c yb-master -- yb-admin --master_addresses yb-master-0.s1.yb-masters.$NS.svc.clusterset.local:7100 list_all_tablet_servers`

### 4. Verify cross-cluster reachability

```bash
scripts/check-mcs-dns.sh yb 1 1     # namespace, masters, tservers
```

Each direction must resolve and connect to every remote master (7100) and tserver (9100).
`kubectl get serviceexports -n yb -o yaml` should show the `Valid` and `Ready` conditions as `True`,
and `kubectl get serviceimports -n yb` should list `yb-masters` and `yb-tservers` in both clusters.
If anything fails, stop here and go to `references/troubleshooting.md`. Don't continue to xCluster.

### 5. Configure xCluster

Run `yb-admin` from a master pod. The names below assume namespace `yb` and RF1:

```bash
SRC=yb-master-0.s1.yb-masters.yb.svc.clusterset.local:7100
TGT=yb-master-0.s2.yb-masters.yb.svc.clusterset.local:7100
src() { kubectl --context kind-s1 -n yb exec yb-master-0 -c yb-master -- yb-admin --master_addresses $SRC "$@"; }
tgt() { kubectl --context kind-s2 -n yb exec yb-master-0 -c yb-master -- yb-admin --master_addresses $TGT "$@"; }
```

**Transactional, database-scoped xCluster, semi-automatic mode (YSQL; verified with this skill):**

1. Create the database and an identical schema on **both** universes, while the source is still empty:
   `sql() { kubectl --context kind-$1 -n yb exec yb-tserver-0 -c yb-tserver -- ysqlsh -h yb-tserver-0.$1.yb-tservers.yb.svc.clusterset.local -d $2 -c "$3"; }`
   then `sql s1 yugabyte 'CREATE DATABASE app'`, `sql s1 app 'CREATE TABLE …'`, and the same for `s2`.
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
helm uninstall yb-s1 -n yb --kube-context kind-s1; helm uninstall yb-s2 -n yb --kube-context kind-s2
kind delete cluster --name s1; kind delete cluster --name s2; rm -f broker-info.subm kubeconfig-internal
```
On real clusters, remove Submariner with `subctl uninstall --context <ctx>` instead of deleting the cluster.
PVCs survive `helm uninstall`. Delete them, or delete the namespace, before reinstalling with
different master addresses, because old master data pins the previous config.

## Overlapping CIDRs: Globalnet

If the clusters' pod or service CIDRs overlap and can't be changed, deploy the broker with
`subctl deploy-broker --globalnet` (default global range 242.0.0.0/8; avoid it with Calico,
which uses it internally). Each headless-service pod then gets a global IP used for both ingress
and egress, and Lighthouse answers `clusterset.local` queries with those IPs, so the Helm values
don't change. Globalnet creates Services with `externalIPs`; disable the `DenyServiceExternalIPs`
admission plugin if it is on. IPv6 is not supported. Prefer non-overlapping CIDRs when you can
choose them: Globalnet adds NAT on every cross-cluster hop.

## Reviewing a user's own config

When the user pastes their kind, subctl or Helm config, check each invariant above. The most common mistakes:
- `replicas.master` is lowered without setting `replicas.totalMasters`, so RF stays at 3.
- `masterAddresses` lists more masters than exist, or uses `svc.cluster.local` names while
  ServiceExports are on.
- `kubernetesClusterId` doesn't match `subctl join --clusterid`.
- The two clusters' CIDRs overlap without Globalnet, or overlap the node network.
- Different namespaces on the two sides, or kube-proxy in IPVS mode.
- On kind: `subctl` run from the host, so `broker-info.subm` points at `https://127.0.0.1:<port>`.
- Nodes left at `rp_filter=1`, so pods off the gateway node can't reach the other cluster.
- Automatic-DDL xCluster set up with a hand-created target database instead of a backup/restore.
