---
name: k8s-storage-troubleshooting
description: >-
  Use when Kubernetes storage blocks a workload: a PersistentVolumeClaim stuck in
  Pending, ProvisioningFailed events, a StorageClass that does not exist or a
  provisioner that cannot provide the access mode, pods Pending with "unbound immediate
  PersistentVolumeClaims", FailedAttachVolume, FailedMount or Multi-Attach errors, a
  PVC or PV stuck Terminating or Released, or a volume that is full or will not expand.
  Investigates with kubectl get, describe and events, and proposes fixes. Reads first
  and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37"
  verified-on: "2026-10-24"
---

# Kubernetes storage troubleshooting

Find out why a volume does not get to a pod, or why it does not work once it is there,
and propose a fix. **Read first, ask before changing.** Run the investigation commands
freely. Run a command under an "Ask first" line only after the user approves that exact
command; if your credentials do not allow it, give it to the user to run. Never run a
"Proposed fix"; hand it to the user.

Volumes hold data, and many storage changes cannot be undone: a volume cannot shrink, a
deleted claim can take its data with it, and most of a claim's spec cannot change after
it is created. So most fixes here are proposed fixes, with the reason said.

The commands use placeholders: `my-namespace`, `my-app`, `my-pod`, `my-data` (the PVC),
`my-pv`, `my-class` and `my-node`. Replace them with the real names. Never read Secrets
(a StorageClass or CSI driver may reference some; read their names only). If output
contains passwords, tokens or keys, do not repeat them.

## When to use

- A PVC is `Pending`, or a pod is `Pending` because of its PVC.
- `ProvisioningFailed`, `FailedAttachVolume`, `FailedMount` or `Multi-Attach error`
  events.
- A PVC or PV is stuck `Terminating`, or a PV is `Released` and not reused.
- A volume is full, or a PVC resize does not finish.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The pod is Pending for CPU, memory, taints or node selectors, not its volume:
  `k8s-node-troubleshooting`.
- The volume is mounted and the app still fails (crash, permissions it logs, probes):
  `k8s-workload-troubleshooting`.
- On AKS, Azure refuses the disk or share (an Azure error code in `ProvisioningFailed` or
  `FailedAttachVolume`, a disk zone conflict, Azure Files mount errors):
  `k8s-aks-troubleshooting`.
- The PVC belongs to a CloudNativePG Cluster (named after an instance, `my-db-1`, with
  the label `cnpg.io/cluster`) and the Cluster's own status matters:
  `k8s-cloudnative-pg-troubleshooting`.
- The volume data is missing after a Velero restore, or a Velero volume backup failed:
  `k8s-velero-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the claims and their status**, and which StorageClass each one asks for.

```bash
kubectl get pvc -n my-namespace
kubectl describe pvc my-data -n my-namespace
kubectl events -n my-namespace --for persistentvolumeclaim/my-data
```

**2. See the StorageClasses**: which exist, which is the default, the provisioner, the
binding mode and whether volumes can expand. StorageClasses and PVs are cluster-scoped,
and the built-in `view` role cannot read them; if these commands are forbidden, say so,
and read the class and the provisioner from `describe pvc` (its `StorageClass` and the
`volume.kubernetes.io/storage-provisioner` annotation) and from the events.

```bash
kubectl get storageclass
kubectl describe storageclass my-class
```

**3. See the PersistentVolumes**, if the claim is bound or should bind to an existing
one.

```bash
kubectl get pv
kubectl describe pv my-pv
```

**4. See the pods that use the claim** and their events. A claim waits for its first
pod when the class uses `WaitForFirstConsumer`.

```bash
kubectl get pods -n my-namespace -o wide
kubectl describe pod my-pod -n my-namespace
kubectl get deployment my-app -n my-namespace -o jsonpath='{.spec.replicas}{"\n"}{.spec.template.spec.volumes}{"\n"}'
```

**5. For attach or mount errors**, look at the CSI side: the attachment for each node,
the drivers and the driver's pods.

```bash
kubectl get volumeattachments
kubectl get csidrivers
kubectl get csinode my-node -o yaml
kubectl get pods -A -o wide | grep -i csi
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| PVC `Pending`, `ProvisioningFailed`, `WaitForFirstConsumer`, `Released` PV | [references/pending.md](references/pending.md) |
| `FailedAttachVolume`, `FailedMount`, `Multi-Attach error`, `Terminating` | [references/attach-mount.md](references/attach-mount.md) |
| Volume full, `No space left on device`, resize not finishing, evictions for ephemeral storage | [references/space-and-expansion.md](references/space-and-expansion.md) |

## Read the results

What the common findings mean (Kubernetes 1.37):

- **PVC `Pending` with `WaitForFirstConsumer`**: the class binds and provisions only when
  a pod that uses the claim is scheduled. With no such pod (a Deployment at 0 replicas,
  a claim created ahead of time), Pending is expected, not a fault.
- **PVC `Pending` with `ProvisioningFailed`**: the provisioner refused. The message says
  why: the class does not exist (`storageclass.storage.k8s.io "my-class" not found`), the
  access mode is not supported, the size or a parameter is invalid, or a cloud quota.
- **No `storageClassName`** gets the default class (annotation
  `storageclass.kubernetes.io/is-default-class: "true"`). If no default existed when the
  claim was created, the claim gets one later, when a default appears.
  `storageClassName: ""` means no provisioning: only a PV with no class can bind.
- **A pod `Pending` with `pod has unbound immediate PersistentVolumeClaims`** (the
  scheduler's message on Kubernetes 1.37): fix the claim first; the pod follows.
- **Access modes**: `ReadWriteOnce` (one node at a time; several pods on that node can
  share it), `ReadOnlyMany`, `ReadWriteMany`, `ReadWriteOncePod` (one pod; CSI volumes
  only). The driver decides which it supports; many block-storage drivers have no
  `ReadWriteMany`.
- **Most of a claim's spec cannot change** after it is created: the API server rejects
  changes to the class or the access modes. Only the storage request (up, if the class
  allows expansion) and `volumeAttributesClassName` can change. A different class or
  mode means a new claim.
- **`Terminating`** for a claim in use: deletion waits for the
  `kubernetes.io/pvc-protection` finalizer until no pod uses it. That protects the data;
  it is not a fault.

State the cause in one sentence, then the evidence you saw (the event and its message,
the class, the access mode, the binding mode), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Scaling a workload is reversible, so it goes under "Ask first" and runs only after the
user says yes. Deleting or recreating a claim or a PV, removing a finalizer, rebinding
a PV and expanding a volume cannot be undone: never run them yourself; hand them to the
user as proposed fixes and say why. Prefer fixing the source the workload is deployed
from (manifest, Helm values, GitOps repository): a claim's class and access mode are
set there.

Start the first pod of a claim that waits for its consumer, if the user wants it bound
now (write the undo with the replicas you found):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl scale deployment/my-app --replicas=1 -n my-namespace
# Undo: kubectl scale deployment/my-app --replicas=0 -n my-namespace
```

Recreate a claim that asks for a class this cluster does not have. The class cannot be
changed in place, and deleting a claim can delete its volume, so a human runs this, and
only for a claim that never bound (no data):

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl get pvc my-data -n my-namespace -o yaml > my-data-pvc.yaml
kubectl delete pvc my-data -n my-namespace
# Copy my-data-pvc.yaml to my-data-new.yaml and edit the copy: set spec.storageClassName to an
# existing class; remove status, metadata.uid, metadata.resourceVersion,
# metadata.creationTimestamp and the volume.kubernetes.io/* annotations. Then:
kubectl apply -f my-data-new.yaml
# Undo: kubectl delete pvc my-data -n my-namespace, then apply my-data-pvc.yaml with the same metadata and status fields removed
```

Better: fix `storageClassName` in the app's source and let the next deploy create the
claim.

## Sources

Checked against the Kubernetes 1.37 documentation:

- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/):
  binding, classes and the default class, retroactive default assignment, access modes,
  phases, reclaim policies, in-use protection, expansion and recovery from failed
  expansion.
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/):
  provisioners, the default class, `volumeBindingMode`, `allowVolumeExpansion`.
- [PersistentVolumeClaim API](https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/persistent-volume-claim-v1/):
  which fields can change, `allocatedResourceStatuses`.
- [Volume Attributes Classes](https://kubernetes.io/docs/concepts/storage/volume-attributes-classes/).
- [VolumeAttachment](https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/volume-attachment-v1/),
  [CSIDriver](https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/csi-driver-v1/),
  [CSINode](https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/csi-node-v1/)
  and [Deploying a CSI driver](https://kubernetes-csi.github.io/docs/deploying.html):
  the controller and node parts of a driver.
- [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/) and
  [Ephemeral Storage](https://kubernetes.io/docs/concepts/storage/ephemeral-storage/):
  `emptyDir` `sizeLimit`, ephemeral storage limits and eviction.
- [Kubernetes Metrics Reference](https://kubernetes.io/docs/reference/instrumentation/metrics/):
  `kubelet_volume_stats_*`.
- kind's default StorageClass is defined in
  [const_storage.go](https://github.com/kubernetes-sigs/kind/blob/main/pkg/build/nodeimage/const_storage.go);
  the local-path provisioner's limits are in its
  [README](https://github.com/rancher/local-path-provisioner/blob/master/README.md).
  Event and scheduler messages quoted here were seen on a Kubernetes 1.37 kind cluster;
  the docs do not list them.
