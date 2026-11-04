---
name: k8s-velero-troubleshooting
description: >-
  Use when Velero backups or restores in Kubernetes fail or do not happen: a
  BackupStorageLocation that is Unavailable ("is unavailable", NoSuchBucket,
  AccessDenied, a wrong endpoint or region), a Backup in FailedValidation, Failed or
  PartiallyFailed, or stuck in New, Queued or InProgress, a Schedule in FailedValidation
  ("invalid schedule") or that makes no backups, a Restore that is Completed with
  warnings but did not bring objects back ("already exists", "the in-cluster version is
  different than the backed-up version"), a PartiallyFailed restore, volume data from
  File System Backup (PodVolumeBackup, node-agent) or the CSI data mover (DataUpload)
  that fails, and backups missing from a cluster. Investigates with kubectl get,
  describe and the Velero server logs, never reading Secrets or backup contents, and
  proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, velero 1.18, velero-plugin-for-aws 1.14"
  verified-on: "2026-10-31"
---

# Velero troubleshooting

Find out why a Velero backup, schedule or restore did not do what the user expected,
from Velero's own objects and its server log, and propose a fix. **Read first, ask
before changing.** Run the investigation commands freely. Run a command under an "Ask
first" line only after the user approves that exact command; if your credentials do not
allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the user.

How Velero works, in the parts that fail:

- The **Velero server** (Deployment `velero`, usually in the namespace `velero`) runs
  every controller. Provider plugins (`velero-plugin-for-aws`, `-gcp`,
  `-microsoft-azure`) are init containers that copy themselves into it.
- A **BackupStorageLocation** (BSL) is the bucket and prefix where backups go. The
  server checks each BSL regularly and sets its phase to `Available` or `Unavailable`.
  A **VolumeSnapshotLocation** says where the provider's volume snapshots go.
- A **Backup** writes the selected Kubernetes objects (Secrets included) as a tarball
  to its BSL, plus volume data by one of three ways: provider snapshots, CSI snapshots
  (optionally moved to the BSL by the data mover, as **DataUploads**), or File System
  Backup (**PodVolumeBackups**, run by the `node-agent` DaemonSet).
- A **Schedule** creates a Backup from its `template` on a cron schedule.
- A **Restore** recreates objects from a Backup. By default it **never overwrites**: an
  object that already exists is skipped with a warning, and the Restore still ends
  `Completed`.

The commands use placeholders: `velero` (Velero's namespace), `my-namespace` (the
backed-up namespace), `my-app-backup`, `my-app-restore`, `my-app-daily` (a Schedule),
`my-backups` (a BSL) and `my-app-config`. Replace them with the real names. Write the
kinds with their group (`backups.velero.io`): other operators define kinds with the same
names, and CloudNativePG's `backups` wins a plain `kubectl get backups`. The built-in
`view` role cannot read Velero's objects (Velero ships no read role); if they are
forbidden, say so and ask the user for them.

**Never read Secrets or backup contents.** Not the credentials Secret the BSL or the
server uses (its status says whether it works), not the Secrets inside a backup, and
not DownloadRequests: their status is a signed link to a backup's files. The `velero`
CLI's `describe --details` and `logs` create DownloadRequests and fetch files from the
bucket, so you give those commands to the user (step 6).

## When to use

- `kubectl get backups.velero.io -n velero` shows `FailedValidation`, `Failed` or
  `PartiallyFailed`, or a backup never leaves `New`, `Queued` or `InProgress`.
- A Schedule exists but no new backups appear.
- A restore finished, but objects did not come back or still have the wrong content.
- A BSL is `Unavailable`, or backups made in another cluster do not show up here.
- Volume data is missing from a restore, or a PodVolumeBackup or DataUpload failed.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The Velero or node-agent pod itself does not start (image pull, crash, resources):
  `k8s-workload-troubleshooting`.
- Restored PVCs stay `Pending`, or CSI snapshots are not ready: `k8s-storage-troubleshooting`.
- A restore is refused by an admission webhook or a policy:
  `k8s-api-troubleshooting`, `k8s-kyverno-troubleshooting`, `k8s-gatekeeper-troubleshooting`.
- Restored apps start but fail: `k8s-workload-troubleshooting`.
- The objects were restored, but a GitOps tool reverts them: `k8s-argocd-troubleshooting`,
  `k8s-flux-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the server and its locations.**

```bash
kubectl get deployments,daemonsets,pods -n velero
kubectl get backupstoragelocations.velero.io,volumesnapshotlocations -n velero
kubectl get backupstoragelocation.velero.io my-backups -n velero -o jsonpath='{.status.phase}{" "}{.status.lastValidationTime}{"\n"}{.status.message}{"\n"}{.spec.provider}{" bucket="}{.spec.objectStorage.bucket}{" prefix="}{.spec.objectStorage.prefix}{" config="}{.spec.config}{" credential="}{.spec.credential}{" accessMode="}{.spec.accessMode}{"\n"}'
```

Read the `message` of every `Unavailable` location: it holds the provider's error.

**2. List the backups, newest last, and read the one in question.**

```bash
kubectl get backups.velero.io -n velero --sort-by=.metadata.creationTimestamp -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.phase}{" errors="}{.status.errors}{" warnings="}{.status.warnings}{" location="}{.spec.storageLocation}{" schedule="}{.metadata.labels.velero\.io/schedule-name}{" "}{.metadata.creationTimestamp}{"\n"}{end}'
kubectl get backup.velero.io my-app-backup -n velero -o jsonpath='{.status.phase}{" "}{.status.failureReason}{"\nvalidation: "}{.status.validationErrors}{"\nprogress: "}{.status.progress}{"\nerrors="}{.status.errors}{" warnings="}{.status.warnings}{"\nqueue="}{.status.queuePosition}{"\n"}'
kubectl get backup.velero.io my-app-backup -n velero -o jsonpath='{.spec}{"\n"}'
```

**3. For a schedule**: its phase, validation errors and last backup.

```bash
kubectl get schedules.velero.io -n velero
kubectl get schedule.velero.io my-app-daily -n velero -o jsonpath='{.spec.schedule}{" paused="}{.spec.paused}{" location="}{.spec.template.storageLocation}{"\n"}{.status.phase}{" last="}{.status.lastBackup}{"\n"}{.status.validationErrors}{"\n"}'
```

**4. For a restore**: its phase, counts, and what it was asked to restore.

```bash
kubectl get restores.velero.io -n velero
kubectl get restore.velero.io my-app-restore -n velero -o jsonpath='{.status.phase}{" "}{.status.failureReason}{"\nvalidation: "}{.status.validationErrors}{"\nprogress: "}{.status.progress}{"\nerrors="}{.status.errors}{" warnings="}{.status.warnings}{"\n"}'
kubectl get restore.velero.io my-app-restore -n velero -o jsonpath='{.spec.backupName}{" "}{.spec.scheduleName}{"\nnamespaces="}{.spec.includedNamespaces}{" mapping="}{.spec.namespaceMapping}{"\nexistingResourcePolicy="}{.spec.existingResourcePolicy}{"\nresources="}{.spec.includedResources}{" excluded="}{.spec.excludedResources}{"\n"}'
```

A restore with `warnings` above 0 has skipped or changed something; step 5 says what.

**5. Read the server log** for the backup or restore. The server logs the same errors and
warnings it counts in the status.

```bash
kubectl logs deployment/velero -n velero -c velero --since=24h | grep my-app-restore | grep -E "level=(warning|error)"
kubectl logs deployment/velero -n velero -c velero --since=24h | grep my-app-backup | grep -E "level=(warning|error)"
kubectl logs deployment/velero -n velero -c velero --since=1h | grep -E "level=(warning|error)" | tail -n 30
```

For volume data, also read the node-agent and its objects:

```bash
kubectl get podvolumebackups.velero.io,podvolumerestores.velero.io,datauploads.velero.io,datadownloads.velero.io -n velero
kubectl logs daemonset/node-agent -n velero --since=24h | grep -E "level=(warning|error)" | tail -n 30
```

**6. If the log has rotated**, ask the user for the CLI's view. These commands only read,
but they create a DownloadRequest and fetch the backup's log and result files from the
bucket, so they are for the user. Say so when you hand them over.

> Proposed fix: review before running. The agent does not run this.

```bash
velero backup describe my-app-backup -n velero --details
velero backup logs my-app-backup -n velero | grep -E "level=(warning|error)"
velero restore describe my-app-restore -n velero --details
velero restore logs my-app-restore -n velero | grep -E "level=(warning|error)"
# Undo: nothing to undo, these only read (they are for the user because they fetch files from the backup bucket)
```

**7. Open the matching reference** for volume data:
[references/volume-data.md](references/volume-data.md) (File System Backup,
PodVolumeBackups, CSI snapshots and the data mover).

## Read the results

**Locations.**

- **BSL `Unavailable`**, message `BackupStorageLocation "my-backups" is unavailable: ...`
  followed by the provider's error. `NoSuchBucket: The specified bucket does not exist`:
  the bucket name (or the account it belongs to) is wrong. `AccessDenied`, `403`,
  `InvalidAccessKeyId`, `SignatureDoesNotMatch`: the credentials or their permissions.
  `no such host`, `connection refused`, `i/o timeout`: the endpoint (`config.s3Url`) or
  the network to it. A wrong `region` gives redirects or `AuthorizationHeaderMalformed`.
  Compare the BSL's bucket, prefix and config with what the user expects; the error
  names which part is wrong.
- **Every backup to that location fails at once** with `FailedValidation`:
  `backup can't be created because BackupStorageLocation my-backups is in Unavailable
  status.` Fix the location, not the backup.
- **A location with `accessMode: ReadOnly`** (often set during a restore or migration)
  refuses new backups: `FailedValidation`, `backup can't be created because backup
  storage location my-backups is currently in read-only mode`.
- **Backups from another cluster do not appear**: the server syncs Backup objects from
  every BSL it has. The other cluster's backups appear only if this cluster has a BSL
  with the same provider, bucket and prefix, and it is `Available`.

**Backups.**

- **`FailedValidation`** with `validationErrors`: the request itself is wrong (the
  location is unavailable or does not exist, a namespace or resource filter conflicts,
  a VolumeSnapshotLocation is missing). The message names it.
- **Stuck in `New`**: the server is not running or not reconciling; check step 1. In
  `Queued` or `ReadyToStart`, it waits behind other backups (`queuePosition`).
- **Stuck in `InProgress`** after the Velero pod restarted: Velero cannot resume an
  interrupted backup. It uploaded nothing; it can be deleted and run again.
- **`WaitingForPluginOperations`**: async work (CSI snapshots, the data mover) is still
  running; see the reference.
- **`PartiallyFailed`**: the backup was written, but some items or volumes failed. The
  log's `level=error` lines name them. The backup is usable for everything else.
- **`Failed`** with `failureReason`: the whole backup failed (often the upload to the
  bucket). `Completed` with `warnings`: usually items Velero could not back up as asked.
- **A namespace that is not in the backup**: `progress.totalItems` is small or 0, and
  `spec.includedNamespaces` does not name it (or a label selector matches nothing).

**Schedules.**

- **`FailedValidation`** with `invalid schedule: ...`: the cron expression is invalid,
  for example `end of range (25) above maximum (23)` for an hour of 25. A schedule in
  that phase never creates a backup. The expression is standard 5-field cron, in the
  Velero server's time zone unless it starts with `CRON_TZ=<timezone>`.
- **`Enabled` but no recent backups**: `spec.paused: true`, or the backups it created
  failed (they carry the label `velero.io/schedule-name`).

**Restores.**

- **`Completed` with `warnings`, and an object still has the wrong content**: the object
  already existed, so Velero skipped it. The log line is `could not restore,
  ConfigMap:my-app-config already exists. Warning: the in-cluster version is different
  than the backed-up version`. This is the default (`existingResourcePolicy` unset or
  `none`), not a failure. `existingResourcePolicy: update` makes Velero patch existing
  objects to match the backup instead (best effort; it does not rewrite data inside
  volumes). Only ServiceAccounts are merged by default.
- **`PartiallyFailed`**: some objects could not be created; the `level=error` lines say
  why (a webhook refused them, a CRD was missing, a namespace was terminating).
- **`FailedValidation`**: `Error retrieving backup: can't find backup
  velero/my-app-backup` (the backup is not in this cluster: check that its location is
  here and `Available`, step 1), or the filters are invalid.
- **Restored into the wrong namespace**, or not at all: check `namespaceMapping` and
  `includedNamespaces` against the backup's namespaces.

## Proposed fix

Point a location at the right bucket (the user names the right one; check it with the
location's next validation, which runs about once a minute):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch backupstoragelocation.velero.io my-backups -n velero --type=merge -p '{"spec":{"objectStorage":{"bucket":"my-app-backups-prod"}}}'
# Undo: kubectl patch backupstoragelocation.velero.io my-backups -n velero --type=merge -p '{"spec":{"objectStorage":{"bucket":"my-app-backups"}}}'
```

Fix a schedule's cron expression (here: every day at 02:00, server time):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch schedule.velero.io my-app-daily -n velero --type=merge -p '{"spec":{"schedule":"0 2 * * *"}}'
# Undo: kubectl patch schedule.velero.io my-app-daily -n velero --type=merge -p '{"spec":{"schedule":"0 25 * * *"}}'
```

Restore again, this time updating objects that exist (limit it to what should change).
Velero overwrites the live objects with the backup's version, so the user should be sure
the backup has the content they want:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl apply -f - <<'YAML'
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: my-app-restore-update
  namespace: velero
spec:
  backupName: my-app-backup
  includedNamespaces: [my-namespace]
  includedResources: [configmaps]
  existingResourcePolicy: update
YAML
# Undo: Velero has no undo for a restore; re-apply the objects from your own manifests, or restore them from a backup taken before this restore
```

A backup stuck `InProgress` after the server restarted uploaded nothing; delete it and
run it again:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl delete backup.velero.io my-app-backup -n velero
# Undo: nothing to restore, the interrupted backup wrote no data; create the backup again
```

## Sources

- [Troubleshooting](https://velero.io/docs/v1.18/troubleshooting/),
  [debugging restores](https://velero.io/docs/v1.18/debugging-restores/) and
  [how Velero works](https://velero.io/docs/v1.18/how-velero-works/).
- [Backup storage locations](https://velero.io/docs/v1.18/locations/) and the
  [BackupStorageLocation API](https://velero.io/docs/v1.18/api-types/backupstoragelocation/).
- [Backup reference](https://velero.io/docs/v1.18/backup-reference/), the
  [Backup API](https://velero.io/docs/v1.18/api-types/backup/) and the
  [Schedule API](https://velero.io/docs/v1.18/api-types/schedule/).
- [Restore reference](https://velero.io/docs/v1.18/restore-reference/) (existing
  resource policy, namespace mapping) and the
  [Restore API](https://velero.io/docs/v1.18/api-types/restore/).
- [File System Backup](https://velero.io/docs/v1.18/file-system-backup/),
  [CSI snapshots](https://velero.io/docs/v1.18/csi/) and
  [CSI snapshot data movement](https://velero.io/docs/v1.18/csi-snapshot-data-movement/).
- Phases and status fields from the CRDs of Velero 1.18.4, and messages seen on kind
  with `velero-plugin-for-aws` 1.14.4.
