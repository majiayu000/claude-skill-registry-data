---
name: k8s-aks-troubleshooting
description: >-
  Use when a problem is specific to Azure Kubernetes Service (AKS): a cluster or node pool
  in "Failed" state, an upgrade or scale that fails ("UpgradeFailed", "violate the pod's
  disruption budget", "QuotaExceeded", "AllocationFailed"), a LoadBalancer Service stuck
  at <pending> ("SyncLoadBalancerFailed", "AuthorizationFailed"), an Azure Disk or Files
  PVC that fails ("ProvisioningFailed", "volume node affinity conflict", "Multi-Attach
  error", "Mount error(13)"), workload identity errors ("AADSTS700016", "AADSTS70021"),
  CoreDNS edits that AKS reverts, "error dialing backend", Azure Policy denials, or API
  server access (authorized IP ranges, private clusters, kubelogin, "User does not have
  access to the resource in Azure"). Investigates with kubectl and read-only az commands,
  and proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "aks, kubernetes 1.33"
  verified-on: "2026-10-25"
---

# AKS troubleshooting

Find out why something that depends on Azure fails in an AKS cluster, and propose a fix.
**Read first, ask before changing.** Run the investigation commands freely: kubectl reads
and the read-only `az` commands below (`show`, `list`, `get`). Run a command under an "Ask
first" line only after the user approves that exact command; if your credentials do not
allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the user.
Every `az` change (update, upgrade, role assignments, anything that writes) is a proposed
fix.

An AKS cluster lives in two places. Kubernetes objects are in the cluster; the cluster
itself, its **node pools** (virtual machine scale sets), load balancers, public IPs, disks
and identities are Azure resources. The cluster resource is in the user's resource group;
the resources AKS manages for it are in a separate **node resource group** (by default
`MC_<resource group>_<cluster>_<region>`). Many AKS failures show in Kubernetes only as a
short event, while the real error is in Azure: in the cluster's `provisioningState`, in
the latest operation, or in the activity log.

The commands use placeholders: `my-resource-group` and `my-cluster` (the cluster),
`my-node-resource-group`, `my-nodepool`, `my-namespace`, `my-app`, `my-pvc`, `my-pod`,
`my-node` and `my-identity`. Replace them with the real names. The `az` commands need an
Azure CLI login (`az account show` tells which subscription it uses). Never read Secrets,
and do not print tokens, keys or client secrets from any source.

## When to use

- The cluster or a node pool shows `Failed`, or an upgrade, scale or update failed.
- A LoadBalancer Service has no `EXTERNAL-IP`, or traffic through it fails.
- A PVC on an Azure Disk or Azure Files class stays `Pending`, or a pod cannot mount it.
- A pod using workload identity cannot get an Azure token.
- A change to the `coredns` ConfigMap disappears, `kubectl logs` or `exec` fail with
  `error dialing backend`, or Azure Policy denies a pod.
- kubectl cannot reach or log in to the cluster.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- A pod that crashes for its own reasons (its logs, probes, OOMKilled):
  `k8s-workload-troubleshooting`. A node that is NotReady or full, or pods that do not
  fit: `k8s-node-troubleshooting`.
- A PVC problem that is not about Azure (no StorageClass, access modes, a full volume):
  `k8s-storage-troubleshooting`.
- A Service with no endpoints, or a NetworkPolicy: `k8s-network-troubleshooting`. The
  Corefile itself: `k8s-coredns-troubleshooting`.
- A `Forbidden` that comes from Kubernetes RBAC (no Azure suffix):
  `k8s-rbac-troubleshooting`. Webhook or admission errors that are not Azure Policy:
  `k8s-api-troubleshooting`; Gatekeeper constraints themselves:
  `k8s-gatekeeper-troubleshooting`.
- Before an upgrade, a check of everything in the cluster that would block or break it
  (PDBs, unmanaged pods, webhooks, deprecated APIs, add-ons): `k8s-upgrade-readiness`.

## Investigate

**1. Find the cluster and its state.** If the user did not name it, list the clusters
the login can see, then read the one in question:

```bash
az aks list -o table
az aks show -g my-resource-group -n my-cluster --query "{state:provisioningState, power:powerState.code, version:kubernetesVersion, nodeResourceGroup:nodeResourceGroup, network:networkProfile.networkPlugin, networkMode:networkProfile.networkPluginMode, outbound:networkProfile.outboundType, private:apiServerAccessProfile.enablePrivateCluster, authorizedIpRanges:apiServerAccessProfile.authorizedIpRanges, azureRbac:aadProfile.enableAzureRbac, localAccountsDisabled:disableLocalAccounts, oidcIssuer:oidcIssuerProfile.issuerUrl, workloadIdentity:securityProfile.workloadIdentity.enabled}" -o json
```

**2. Node pools and recent operations.** A `Failed` state is about the last operation, not
the running workloads:

```bash
az aks nodepool list -g my-resource-group --cluster-name my-cluster --query "[].{name:name, mode:mode, state:provisioningState, power:powerState.code, count:count, min:minCount, max:maxCount, autoscale:enableAutoScaling, vmSize:vmSize, zones:availabilityZones, version:currentOrchestratorVersion, maxSurge:upgradeSettings.maxSurge}" -o table
az monitor activity-log list -g my-resource-group --offset 3d --status Failed --query "[].{time:eventTimestamp, operation:operationName.value, status:status.value, message:properties.statusMessage}" -o json
az aks operation show-latest -g my-resource-group -n my-cluster
```

`az aks operation show-latest` needs the `aks-preview` extension; if it is missing, the
activity log has the same error.

**3. The Kubernetes side.**

```bash
kubectl get nodes -L kubernetes.azure.com/agentpool,topology.kubernetes.io/zone,node.kubernetes.io/instance-type
kubectl events -A --types=Warning
kubectl get pods -n kube-system -o wide
```

**4. Follow the symptom** to its reference, which has the commands for that area:

| Symptom | Read |
|---|---|
| Cluster or node pool `Failed`, upgrade or scale errors, quota and VM capacity, autoscaler, node auto-repair, versions | [references/nodepools-upgrades.md](references/nodepools-upgrades.md) |
| LoadBalancer Service `<pending>` or unreachable, `SyncLoadBalancerFailed`, static IPs, internal load balancers, health probes, SNAT | [references/load-balancers.md](references/load-balancers.md) |
| Azure Disk or Azure Files PVC `Pending` or not mounting, zones, attach limits; workload identity and `AADSTS` errors | [references/storage-identity.md](references/storage-identity.md) |
| CoreDNS customization, `error dialing backend`, Azure Policy, other managed add-ons; API server reachability, Entra ID login, Azure RBAC | [references/addons-access.md](references/addons-access.md) |

## Read the results

- **`provisioningState` is `Failed` while nodes and pods run normally**: the last Azure
  operation on the cluster failed; the cluster itself usually keeps working. The activity
  log's `statusMessage` names the cause, often nested: an outer code such as
  `ResourceOperationFailure`, `UpgradeVMSSAgentPoolFailed` or `CreateOrUpdateExtensionFailed`
  wraps the real one in `details`. **`Update failed for this resource, as there is a
  conflicting operation in progress`** means two operations overlapped (for example an
  add-on update during a scale); nothing else needs fixing. Fix the real cause first, then
  reconcile the cluster (see Proposed fix). A reconcile does not fix an unresolved quota,
  policy, network or capacity error.
- **`(UpgradeFailed) Drain node ... failed when evicting pod ... Cannot evict pod as it
  would violate the pod's disruption budget`**: a PodDisruptionBudget allows 0
  disruptions; see [references/nodepools-upgrades.md](references/nodepools-upgrades.md).
- **`QuotaExceeded`**, **`AllocationFailed`**, **`ZonalAllocationFailed`**,
  **`SkuNotAvailable`**: Azure could not create the virtual machines, the subscription's
  quota or the region's capacity, not Kubernetes.
- **A LoadBalancer Service stays `<pending>` with `SyncLoadBalancerFailed`**: the event's
  message is the Azure error from the cloud provider. **`AuthorizationFailed ... does not
  have authorization to perform action 'Microsoft.Network/virtualNetworks/subnets/read'
  over scope '.../subnets/my-subnet' or the scope is invalid`** on an internal load
  balancer usually means that **subnet does not exist** (a typo in
  `azure-load-balancer-internal-subnet`): the cluster identity can read only the subnets
  it was granted, so a missing one looks like missing permission. Check the subnet exists
  before granting any role.
- **A PVC `Pending` with `ProvisioningFailed ... RESPONSE 400 ... InvalidParameter`**: Azure
  refused the disk itself, for example **`The value 40960 of parameter 'disk.diskSizeGb' is
  out of range. The value must be between '1' and '32767', inclusive.`** (an Azure Disk is
  at most 32 TiB). The message after `ERROR CODE` is Azure's; the rest is the CSI driver.
- **A workload identity pod logs `AADSTS700016: Application with identifier '<client ID>'
  was not found in the directory`**: the client ID in the ServiceAccount annotation
  `azure.workload.identity/client-id` belongs to no identity in that tenant. **`AADSTS70021:
  No matching federated identity record found for presented assertion`**: the identity
  exists, but no federated credential matches the token's issuer and subject
  (`system:serviceaccount:my-namespace:my-app`). See
  [references/storage-identity.md](references/storage-identity.md).
- **`Error from server: error dialing backend: dial tcp <node ip>:10250: i/o timeout`** on
  `kubectl logs` or `exec`, while `get` works: the API server cannot reach the kubelet
  through the konnectivity tunnel; see
  [references/addons-access.md](references/addons-access.md).
- **`... User does not have access to the resource in Azure. Update role assignment to
  allow access.`**: the cluster uses Azure RBAC for Kubernetes, and the caller's Azure role
  assignments, not Kubernetes RoleBindings, decide.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it. Every
change to an Azure resource is a proposed fix the user runs; make it in the cluster's
source of truth (Bicep, Terraform, ARM templates, a pipeline) when there is one, since a
later deployment would undo a change made by hand. Kubernetes objects such as Services,
PVCs and ServiceAccounts belong in the workload's manifests or chart.

After the cause of a `Failed` state is fixed, a reconcile re-applies the cluster's current
configuration without changing it:

> Proposed fix: review before running. The agent does not run this.

```bash
az aks update -g my-resource-group -n my-cluster --yes
# Undo: none needed; it re-applies the existing configuration
```

For a node pool in `Failed`:

> Proposed fix: review before running. The agent does not run this.

```bash
az aks nodepool update -g my-resource-group --cluster-name my-cluster -n my-nodepool
# Undo: none needed; it re-applies the existing node pool configuration
```

Never start another operation while one is still running (`az aks operation show-latest`
shows `InProgress`), and never edit the scale sets, load balancers or disks in the node
resource group by hand: AKS owns them, reverts such changes, and they are not supported.
The fixes for each area, with their undo, are in the references.

## Sources

Checked against AKS with Kubernetes 1.33 (a private cluster with Azure CNI, Entra ID and
Azure RBAC, workload identity and the Azure Policy add-on) and the Microsoft Learn pages
below, as of October 2026:

- [Troubleshoot AKS upgrade, scaling and failed-state errors](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/availability-performance/cluster-node-virtual-machine-failed-state),
  [PodDrainFailure](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/create-upgrade-delete/error-code-poddrainfailure),
  [QuotaExceeded](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/error-codes/quota-exceeded-error)
  and [ZonalAllocationFailed and AllocationFailed](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/error-codes/zonalallocation-allocationfailed-error).
- [Supported Kubernetes versions](https://learn.microsoft.com/azure/aks/supported-kubernetes-versions),
  [upgrade options](https://learn.microsoft.com/azure/aks/upgrade-options),
  [upgrade rules and version skew](https://learn.microsoft.com/azure/aks/upgrade-aks-control-plane#kubernetes-version-upgrade-rules),
  [node auto-repair](https://learn.microsoft.com/azure/aks/node-auto-repair) and
  [cluster autoscaler](https://learn.microsoft.com/azure/aks/cluster-autoscaler).
- [Standard load balancer](https://learn.microsoft.com/azure/aks/configure-load-balancer-standard),
  [internal load balancer](https://learn.microsoft.com/azure/aks/internal-lb),
  [static public IP](https://learn.microsoft.com/azure/aks/static-ip) and
  [SNAT](https://learn.microsoft.com/azure/aks/troubleshoot-source-network-address-translation).
- [Storage concepts](https://learn.microsoft.com/azure/aks/concepts-storage),
  [Azure Disk mount failures](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/storage/fail-to-mount-azure-disk-volume)
  and [Azure Files mount failures](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/storage/fail-to-mount-azure-file-share).
- [Workload identity](https://learn.microsoft.com/azure/aks/workload-identity-overview).
- [CoreDNS customization](https://learn.microsoft.com/azure/aks/coredns-custom),
  [tunnel connectivity](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/connectivity/tunnel-connectivity-issues),
  [API server connection issues](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/connectivity/troubleshoot-cluster-connection-issues-api-server),
  [kubelogin](https://learn.microsoft.com/azure/aks/kubelogin-authentication) and
  [Azure RBAC for Kubernetes](https://learn.microsoft.com/azure/aks/manage-azure-rbac).
- Messages quoted from the test cluster: the internal load balancer `AuthorizationFailed`
  for a missing subnet, the Azure Disk `InvalidParameter` size error, `AADSTS700016` from
  a workload identity pod, and a `Failed` cluster after `CreateOrUpdateExtensionFailed`
  with `conflicting operation in progress`.
