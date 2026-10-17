---
name: nas-admin
description: >
  NAS PV/PVC admin panel for the LG N2R1 SMBv1 NAS.
  FastAPI + HTMX + Tailwind CDN app deployed as a Helm chart.
  Covers the app source, Kaniko build pattern, Helm chart structure,
  auth options (basic/oidc), and iteration workflow.
---

# NAS Admin Panel

Web admin panel for managing Kubernetes PersistentVolumes and PersistentVolumeClaims
backed by the cluster's SMB NAS (LG N2R1, `192.168.178.102`, SMBv1 only).

## Why it exists

The LG N2R1's built-in web UI shows disk usage but has no visibility into which
K8s workloads own which volumes. Over time, PVs/PVCs accumulate (released,
unused, or orphaned). This panel provides that visibility and a delete action.

## Key paths

| Path | Purpose |
|------|---------|
| `apps/nas-admin/main.py` | FastAPI app — edit here to change backend logic |
| `apps/nas-admin/templates/` | Jinja2 + HTMX HTML — edit here to change UI |
| `apps/nas-admin/Dockerfile` | Docker build — identical to what Kaniko uses |
| `charts/nas-admin/values.yaml` | All knobs: auth, hostname, PVC, resources |
| `roles/install-nas-admin-image/` | Kaniko in-cluster ARM64 build |
| `roles/install-nas-admin/` | Helm install/upgrade via `kubernetes.core.helm` |

## Makefile targets

```bash
make nas-admin-build        # Kaniko build → registry.registry:5000/ai/nas-admin:latest (~2 min)
                            # Uses playbooks/build-nas-admin.yml (standalone, no cluster bootstrap)
make nas-admin-build-logs   # Tail build logs while Kaniko runs (separate terminal)
make nas-admin              # Helm install/upgrade (no rebuild)
make nas-admin-all          # build + deploy (idempotent)
```

The `nas-admin-build` target uses a **standalone playbook** (`playbooks/build-nas-admin.yml`)
that runs only the `install-nas-admin-image` role with `gather_facts: false`.
This is faster than `bootstrap.yml --tags nas-admin-build` for quick iteration.

## Iteration workflow

**Fast local test (no cluster deploy):**
```bash
docker build -t nas-admin:test ./infra/apps/nas-admin/
docker run -p 8080:8080 -v ~/.kube/config:/root/.kube/config:ro nas-admin:test
# open http://localhost:8080
```

**Change HTML/Python → test locally → push to cluster:**
```bash
# 1. edit apps/nas-admin/
# 2. make nas-admin-build    (Kaniko re-reads files from role ConfigMap via lookup('file', ...))
# 3. make nas-admin          (Helm upgrade, rolling restart)
```

**Change only config (auth mode, password, hostname) → no rebuild needed:**
```bash
# edit roles/install-nas-admin/defaults/main.yml (or secrets.yml for passwords)
make nas-admin   # only helm upgrade
```

## Features

- **PV view** (`/pvs`): all SMB-backed PVs, status badges, NAS share path, bound claim, age. Orphaned PVs (Released/Available/Failed) highlighted amber. **Delete button** visible only on orphaned rows — removes K8s object, NAS data untouched (Retain policy).
- **PVC view** (`/pvcs`): all PVCs cross-namespace (or SMB-only filter). Shows which pod(s) mount each PVC. "Unused" PVCs (bound but no running pod) highlighted. Delete button with HTMX `hx-confirm`.
- **NAS browser** (`/browse`): HTMX-driven directory navigation. Reads from `/mnt/nas` (NAS PVC mounted ReadOnly). No direct SMBv1 connection from Python.
- **Health** (`/health`): returns `{"status":"ok"}` — used by liveness/readiness probes.

### PV/PVC cleanup flow

When you delete a PVC from the UI with `Retain` policy:
1. PVC is deleted → pod can no longer mount it
2. PV status changes `Bound → Released` — row turns amber
3. Click **Delete** on the PV row → `DELETE /api/pvs/{name}` → K8s PV object removed
4. NAS share data (`//192.168.178.102/service/...`) is **not touched** — only the K8s object is gone

For dynamic PVs (StorageClass `smb-nas` with `Delete` reclaim policy), deleting the PVC also deletes the PV automatically — no manual PV cleanup needed.

## Authentication

Configured via `auth.mode` in `values.yaml` or Ansible `nas_admin_auth_mode`.

### Basic auth (default)

```yaml
auth:
  mode: basic
  basic:
    username: admin
    password: "changeme"   # set in roles/install-nas-admin/defaults/secrets.yml (gitignored)
```

The Helm chart creates a K8s `Secret` → pod reads `AUTH_USERNAME` / `AUTH_PASSWORD` env vars.
FastAPI uses `HTTPBasic` with constant-time comparison (`secrets.compare_digest`).

### OIDC via GitHub (oauth2-proxy sidecar)

```yaml
auth:
  mode: oidc
  oidc:
    clientId: "..."
    clientSecret: "..."
    cookieSecret: "..."    # openssl rand -base64 32
    emailDomain: "*"
```

When `auth.mode == "oidc"`:
- A `quay.io/oauth2-proxy/oauth2-proxy:v7.6.0` sidecar is added to the Deployment
- The sidecar listens on port 4180, proxies authenticated traffic to `localhost:8080`
- The Service and HTTPRoute point to port 4180 (not 8080)
- A `Secret` with `clientId`, `clientSecret`, `cookieSecret` is created

**Prerequisite:** GitHub OAuth App with callback URL `https://nas-admin.cluster.home/oauth2/callback`.
Works on `*.cluster.home` as long as the browser resolves it via Pi-hole DNS on the local network.

## Helm chart parameters

All configurable via `charts/nas-admin/values.yaml` or `--set`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `image.repository` | `registry.registry:5000/ai/nas-admin` | Image registry path |
| `image.tag` | `latest` | Image tag |
| `hostname` | `nas-admin.cluster.home` | HTTPRoute hostname |
| `nasPvc.enabled` | `true` | Mount smb-nas-pvc for file browser |
| `nasPvc.claimName` | `nas-admin-nas-pvc` | PVC to mount (dedicated PV in `storage` ns) |
| `nasPvc.mountPath` | `/mnt/nas` | Mount path in pod |
| `auth.mode` | `basic` | `basic` \| `oidc` \| `none` |
| `auth.basic.username` | `admin` | Basic auth username |
| `auth.basic.password` | `changeme` | Basic auth password |
| `replicaCount` | `1` | Number of replicas |

## Kaniko build details

Source files are read by Ansible from `apps/nas-admin/` via `lookup('file', ...)` and
injected as two ConfigMaps (`nas-admin-source`, `nas-admin-templates`).
A `busybox` initContainer copies them into a `local-path` workspace PVC before Kaniko runs.

The Dockerfile is the same file used for local `docker build` — no divergence between
local and cluster builds.

Estimated build time: **~2 min** (python:3.12-slim + ~5 small packages).

## RBAC

ClusterRole grants:
- `persistentvolumes` — get, list, watch, **delete** (for orphaned PV cleanup)
- `persistentvolumeclaims` — get, list, watch, **delete**
- `pods`, `events`, `storageclasses` — get, list, watch only

## Namespace

Deployed in namespace `storage` (created by the Ansible role if missing).

## Gotchas

### Cross-namespace PVC access

PVCs are namespace-scoped. The pod runs in `storage` but `smb-nas-pvc` lives in `default` — it cannot be mounted cross-namespace.

Fix: `install-nas-admin` creates a **dedicated static PV** (`nas-admin-browse-pv`) pointing to `//192.168.178.102/service` with `nodeStageSecretRef: {name: smbcreds, namespace: default}`, plus a matching PVC (`nas-admin-nas-pvc`) in the `storage` namespace. The `smbcreds` Secret lives in `default` (created by `install-cifs-nas`) but the CSI driver reads it directly — no cross-namespace issue.

Variables that control this: `nas_admin_nas_ip` (default `192.168.178.102`), `nas_admin_nas_share` (default `service`), `nas_admin_nas_pvc_name` (default `nas-admin-nas-pvc`).

### Forcing Helm to re-apply ClusterRole changes

Without `helm-diff` plugin installed, `kubernetes.core.helm` reports `changed=0` and skips upgrades when no values changed. To force a re-apply after editing chart templates (e.g., RBAC verbs), bump `version` in `Chart.yaml` — Helm will detect a chart version change and do the upgrade.

### Helm chart version vs image tag

The chart version (`Chart.yaml`) tracks chart structure changes. The image tag is always `latest` with `pullPolicy: Always`. After a code-only change (`make nas-admin-build`), run `kubectl rollout restart deployment/nas-admin -n storage` to pull the new image — Helm won't detect the rebuild.

## Related skills

- `storage` — CIFS/SMB CSI driver, PV/PVC patterns, StorageClass variants
- `gateway` — HTTPRoute + shared Gateway pattern used by the HTTPRoute in this chart
