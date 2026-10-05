---
name: qruiq-cos-storage
description: |
  Mount a Tencent Cloud COS bucket into a TKE pod as a ReadWriteMany PVC via
  the cosfs CSI driver, so the app reads/writes user uploads (or any
  persisted blobs) through a normal filesystem path. Covers PV/PVC/Secret
  manifests, the `<name>-<AppId>` bucket-naming rule, the internal-vs-public
  endpoint billing trap, the cosfs POSIX caveats (no atomic rename, no
  append, no fsync — don't put a database here), and IAM scoping. `coscli`
  for one-off batch uploads is mentioned only as an appendix.
  Use when asked to "add file storage", "set up COS", "挂个 COS bucket",
  "用户上传存哪里", "持久化上传文件", "mount COS to pod", "configure cosfs",
  or any request to add object/file storage to a TKE workload.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
---

# qruiq-cos-storage

Mount a Tencent COS bucket as a ReadWriteMany PVC in a TKE pod via the cosfs CSI driver. The app then reads and writes through a regular filesystem path (e.g. `/app/public/uploads`), and the bytes land in COS.

This is the right answer when:

- pods are ephemeral and you can't keep user uploads on local disk;
- multiple pod replicas need to see the same files (CBS doesn't do RWX);
- the data is **blobs written once and read many** — images, exports, generated PDFs, snapshots.

This is the **wrong** answer when:

- the app needs POSIX guarantees (database files, lock files, append-only logs, build caches) — use CBS `cloud-premium` (RWO) instead;
- the cluster is outside Tencent Cloud — use S3 / R2 / MinIO.

## Prerequisites

- TKE cluster with the COS CSI add-on installed (see Step 1).
- A COS bucket in the **same region as the cluster** (cross-region traffic is billed and slow).
- `tccli` configured (used for inspection only; the bucket itself is usually created via console).
- Tencent **AppId** (10-digit number, same across all your buckets — find in console → 账号信息).

## Bucket naming — the `-AppId` suffix is mandatory

Tencent COS bucket names are **`<name>-<AppId>`**, e.g. `x-invoory-1252401919`. The "name" you pick in the console is what you choose; Tencent appends `-<AppId>` automatically. Use the **full** name everywhere — `bucket:` in the PV, IAM ARNs, anywhere.

## Step 1 — Confirm the CSI driver is installed

cosfs is **not** built into TKE — it's an add-on. Check:

```bash
kubectl get pods -n kube-system -l 'app in (csi-cosplugin,csi-coslauncher)'
```

Expect `csi-coslauncher-*` and `csi-cosplugin-*` running on every node (DaemonSets). If missing: TKE console → 集群 → 组件管理 → 安装 `cos` CSI 组件. **Without this, your PVC will hang at `Pending` forever with no useful error.**

## Step 2 — Create cos-secret in the workload's namespace

The CSI driver authenticates to COS using a Secret referenced by the PV. The Secret **must live in the same namespace as the pod that mounts the PVC** — namespace cross-references aren't supported.

Mint a **dedicated CAM sub-user with bucket-scoped policy** (see Step 6). Don't use the master key. Then:

```bash
kubectl -n <ns> create secret generic cos-secret \
  --from-literal=SecretId="$COS_SECRET_ID" \
  --from-literal=SecretKey="$COS_SECRET_KEY"
```

Reuse one Secret per (namespace, bucket) pair.

## Step 3 — PV + PVC manifest

Drop into `k8s/cosfs-storage.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: <project>-cosfs-pv
spec:
  capacity:
    storage: 10Gi              # cosfs ignores this; k8s requires a value
  accessModes:
    - ReadWriteMany            # the whole point of using cosfs
  persistentVolumeReclaimPolicy: Retain
  storageClassName: cosfs
  volumeMode: Filesystem
  mountOptions:
    - allow_other
  csi:
    driver: com.tencent.cloud.csi.cosfs
    volumeHandle: <project>-cosfs-pv     # MUST be unique cluster-wide
    nodePublishSecretRef:
      name: cos-secret
      namespace: <ns>
    volumeAttributes:
      bucket: x-invoory-1252401919       # full name with -AppId
      path: /uploads                     # subdirectory inside the bucket
      url: http://cos-internal.ap-singapore.tencentcos.cn   # see Step 4
      additional_args: -oallow_other
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <project>-cosfs-pvc
  namespace: <ns>
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: cosfs
  volumeName: <project>-cosfs-pv         # bind directly to the PV above
```

Critical fields:

- **`volumeHandle`** must be unique cluster-wide. Reusing the same handle across two PVs makes one of them silently unmountable. Prefix with the project name.
- **`path:`** lets multiple workloads share one bucket via different prefixes. **Always set it** — don't mount `/`, you'll see every other project's files.
- **`volumeName`** on the PVC pins the binding. Without it the PVC may bind to some other RWX PV that happens to match.
- **`storage: 10Gi`** is a lie cosfs has to tell to satisfy the k8s API — COS is unlimited, this number doesn't gate anything.

## Step 4 — Internal vs public endpoint (billing trap)

| URL | When | Cost |
|---|---|---|
| `http://cos.<region>.myqcloud.com` | Pod is **outside** the bucket's Tencent region (cross-region cluster, local dev) | Public egress + request fees |
| `http://cos-internal.<region>.tencentcos.cn` | Pod is **inside** same Tencent region as the bucket | **No traffic charge**, only request fees |

For a TKE cluster in `ap-singapore` reading a bucket in `ap-singapore`, **always use the internal endpoint**. The public endpoint works but you pay outbound traffic on every read — easy to miss and expensive at scale.

If you find an existing manifest with `cos.<region>.myqcloud.com` while the cluster is in the same region, it's a misconfiguration — flag it.

## Step 5 — Mount it in the Deployment

```yaml
spec:
  template:
    spec:
      containers:
      - name: web
        volumeMounts:
        - name: uploads
          mountPath: /app/public/uploads     # whatever path the app expects
      volumes:
      - name: uploads
        persistentVolumeClaim:
          claimName: <project>-cosfs-pvc
```

Apply: `kubectl apply -f k8s/cosfs-storage.yaml -f k8s/deployment.yaml`. Watch: `kubectl -n <ns> get pvc -w` until `Bound`, then `kubectl -n <ns> get pods -w`.

If pods stay `ContainerCreating` with events like `MountVolume.SetUp failed for volume "..." : rpc error`:

- `cos-secret` exists in the right namespace? (`kubectl -n <ns> get secret cos-secret`)
- bucket name has the `-<AppId>` suffix?
- region in `url:` matches the bucket's region? (mismatch produces auth-looking errors)
- CSI plugin pods running on the scheduled node?

## Step 6 — IAM: bucket-scoped sub-user

The CAM key in `cos-secret` should be a **sub-user with bucket-scoped policy**, not the master key. Minimum policy for an app that reads & writes `/uploads/*`:

```json
{
  "version": "2.0",
  "statement": [{
    "effect": "allow",
    "action": ["cos:GetObject","cos:PutObject","cos:DeleteObject","cos:HeadObject","cos:GetBucket"],
    "resource": ["qcs::cos:ap-singapore:uid/1252401919:x-invoory-1252401919/uploads/*",
                 "qcs::cos:ap-singapore:uid/1252401919:x-invoory-1252401919"]
  }]
}
```

`uid/<AppId>` and the full bucket name (with `-<AppId>` suffix) are both required in the ARN. `cos:GetBucket` on the bare bucket is needed for `ListObjects`, which cosfs uses for `readdir`.

## cosfs is **not** POSIX — know the lies

cosfs presents COS as a filesystem, but COS is object storage. The mismatch leaks through. **Don't promise the developer these will work like a real disk:**

- **No atomic rename across "directories".** A `mv` is copy + delete; readers can see neither, both, or partial. Don't rely on rename for atomic publish.
- **No append.** Apps that open files `O_APPEND` (some loggers, SQLite WAL) will misbehave or rewrite the whole object. Don't put a database here.
- **`fsync` doesn't durably flush** the way you think. cosfs buffers and uploads in chunks.
- **Listing a "directory" is `ListObjects`.** Slow once you have ≥10k objects in one prefix. Don't `ls /mnt/cosfs/uploads/` on a million-file tree — it pages forever.
- **No hard links, no symlinks, weak permission semantics.** Anything depending on chmod / chown / inode numbers will break or no-op.
- **Concurrent writers to the same object will overwrite each other** — last writer wins, no locking. cosfs is RWX in the k8s sense (multi-pod read-write) but the *consistency contract* is per-object eventual.
- **Don't use cosfs for a database, a queue, or a build cache.** Use it for blobs that are written once and read many: user uploads, exports, image renders, snapshots.

If the app needs POSIX guarantees, use CBS (`cloud-premium`) and accept RWO instead.

## Public vs private bucket access

- **Private bucket + signed URL** for user-uploaded files (default; safer). The app generates a presigned URL via `cos-nodejs-sdk-v5` for client downloads.
- **Public-read bucket** only for static assets you'd put on a CDN anyway. **Don't make a user-upload bucket public** — privacy incident waiting to happen.
- Public-read is set in console: bucket → 权限管理 → 访问权限 → 公有读私有写. Public endpoint is required for browser access, internal endpoint is private-network-only.

## Cleanup / dev hygiene

- When dropping a workload, **don't** also delete the PV (it has `persistentVolumeReclaimPolicy: Retain`). Leaving the PV without the bucket is fine; deleting the bucket while a PV references it makes future mounts fail until the PV is deleted.
- Full teardown: delete PVC → delete PV → optionally clear bucket contents.

## Gotchas (quick reference)

- **Bucket name without `-<AppId>`** → mount errors that look like auth failures.
- **Wrong region in `url:`** → same auth-looking error.
- **`cos.<region>.myqcloud.com` instead of `cos-internal.<region>.tencentcos.cn`** in same-region cluster → quietly bills public traffic on every read.
- **CSI plugin not installed** → PVC stuck `Pending` with no obvious error in pod events.
- **`cos-secret` in wrong namespace** → mount fails. Each namespace mounting needs its own copy.
- **`volumeHandle` collision** across two PVs → silent breakage.
- **Treating cosfs as POSIX** → see "cosfs is not POSIX". No SQLite / BoltDB / lock files / mmap.
- **Master CAM key in `cos-secret`** → over-privileged; use a bucket-scoped sub-user.
- **Public endpoint is correct for static-public-read assets** — internal endpoint isn't reachable from browsers. Internal-vs-public is per-traffic-direction, not per-bucket.

## What NOT to do

- Don't put a database (SQLite, LMDB, BoltDB) on a cosfs mount.
- Don't enable public-read on a user-upload bucket.
- Don't reuse the master CAM key for runtime workloads.
- Don't omit `path:` — never mount the bucket root if other workloads share it.
- Don't delete the PV before the PVC; it'll hang in `Terminating`.
- Don't paste `SecretId`/`SecretKey` into chat. `kubectl create secret` reads from env or files directly.
- Don't pick a bucket region different from the cluster region "to save on storage" — you'll lose the savings on traffic many times over.

---

## Appendix — `coscli` for one-off uploads

For batch uploads from a dev box or CI (publishing static assets, one-shot migrations, backups), use `coscli` instead of writing to the mounted PVC. Both can target the same bucket — runtime app writes via cosfs, dev box pushes via coscli.

```bash
brew install coscli   # mac, or grab a release from github.com/tencentyun/coscli

coscli config add \
  --bucket x-invoory-1252401919 \
  --region ap-singapore \
  --alias invoory \
  --secret-id "$COS_SECRET_ID" \
  --secret-key "$COS_SECRET_KEY"

coscli ls   cos://invoory/
coscli cp   public/uploads/  cos://invoory/uploads/  -r
coscli sync ./dist/          cos://invoory/static/   -r
```

Notes:

- The `coscli` alias (`invoory`) is *just a local nickname* — it has no relationship to the actual bucket name. Don't confuse the two when reading scripts.
- `coscli` writes `./coscli.log` and `./coscli_output/<timestamp>/process.log`. Useful for CI artifacts; **gitignore them** in repos.
- For CI, use a bucket-scoped sub-user key in repo secrets — same IAM principle as Step 6.
- Same `-<AppId>` suffix rule applies in `--bucket`.
