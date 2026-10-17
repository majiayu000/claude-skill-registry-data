---
name: storage
description: >
  Storage on K3s. Default is longhorn-nvme (NVMe block storage on RK1 nodes).
  smb-nas and rclone-webdav are opt-in only — no role depends on them by default.
  Covers StorageClasses, dependency pattern, and PVC migration.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, storage, longhorn, smb, cifs, csi, nas, pv, pvc, storageclass, dependency-pattern]
---

# Storage Skill

## StorageClasses in use (2026-05-26)

| StorageClass | Driver | Access | Use |
|---|---|---|---|
| `longhorn-nvme` | driver.longhorn.io | RWO | **Default for all new PVCs** — NVMe-backed, 3 replicas on RK1 nodes |
| `local-path` | rancher.io/local-path | RWO | K3s built-in, node-local. Used only for pihole (SQLite) and build workspaces |
| `smb-nas` | smb.csi.k8s.io | RWX | **Opt-in only** (`make storage-smb`). NAS LG N2R1 (192.168.178.102, SMBv1). Not installed by default. |
| `rclone-webdav` | rclone.csi.veloxpack.io | RWO | **Opt-in only** (`make storage-rclone`). Nextcloud WebDAV. Not installed by default. |

**No role depends on `smb-nas` or `rclone-webdav` by default.**
All service PVCs use `longhorn-nvme` or `local-path`.

---

## Storage Dependency Pattern

Every role that uses a non-local-path SC self-installs its storage backend as its first task.
This makes each role independently deployable.

### Role defaults

```yaml
# Default — longhorn-nvme (no storage_role needed):
<role>_storage_class: "longhorn-nvme"
# storage_role is NOT defined → guard skips automatically

# Opt-in SMB NAS:
<role>_storage_class: "smb-nas"
<role>_storage_role: "install-cifs-nas"
```

### First task in tasks/main.yml

```yaml
- name: Ensure custom Storage backend is installed before deploying <Service>
  ansible.builtin.include_role:
    name: "{{ <role>_storage_role }}"
  when: <role>_storage_class != 'local-path' and <role>_storage_role is defined and <role>_storage_role != ''
```

The `when` condition:
- `local-path` → skip (K3s built-in)
- `storage_role` undefined or empty (longhorn-nvme default) → skip (Longhorn is always installed)
- `storage_role` set (smb-nas opt-in) → run `install-cifs-nas`

### Current role storage classes

| Role | StorageClass | storage_role |
|---|---|---|
| `install-registry` | `longhorn-nvme` | — |
| `install-hermes-agent-image` | `longhorn-nvme` | — |
| `install-hermes-agent` | `longhorn-nvme` | — |
| `install-kubernetes-mcp-server-image` | `longhorn-nvme` | — |
| `install-kube-prometheus-stack` | `longhorn-nvme` | — |
| `install-loki` | `longhorn-nvme` | — |
| `install-tempo` | `longhorn-nvme` | — |
| `install-kagent` | `longhorn-nvme` | — |
| `install-leloir` | `longhorn-nvme` | — |
| `install-honcho` | `longhorn-nvme` | — |
| `install-openclaw` | `longhorn-nvme` | — |
| `install-neuvector` | `local-path` | — |
| `install-pihole` | `local-path` (FORCED) | — |

### How to add longhorn-nvme to a new role

1. In `defaults/main.yml` — just the storage class (no storage_role):
   ```yaml
   <role>_storage_class: "longhorn-nvme"
   <role>_storage_size: "10Gi"
   ```

2. First task in `tasks/main.yml` (guard handles future smb-nas override):
   ```yaml
   - name: Ensure custom Storage backend is installed before deploying <Service>
     ansible.builtin.include_role:
       name: "{{ <role>_storage_role }}"
     when: <role>_storage_class != 'local-path' and <role>_storage_role is defined and <role>_storage_role != ''
   ```

3. Reference `{{ <role>_storage_class }}` in PVC definition.

---

## Optional NAS backends

### SMB NAS (smb-nas)

Role: `roles/install-cifs-nas/`
Bootstrap tag: `storage-smb` (opt-in, not in default flow)
Make target: `make storage-smb`

**When to use:** Only for RWX (ReadWriteMany) — multiple pods writing the same volume.

To opt a role into smb-nas:
```yaml
# In roles/<name>/defaults/main.yml:
<role>_storage_class: "smb-nas"
<role>_storage_role: "install-cifs-nas"
```

Key defaults:
```yaml
cifs_nas_ip: "192.168.178.102"
cifs_nas_mac: "00:e0:91:80:fb:f0"     # Wake-on-LAN
cifs_nas_share: "service"
cifs_enable_static: false              # opt-in: static PV/PVC + write test
cifs_enable_dynamic_test: false        # opt-in: dynamic test pod
cifs_storage_class_name: "smb-nas"
```

### WebDAV / Nextcloud (rclone-webdav)

Role: `roles/install-csi-rclone/`
Bootstrap tag: `storage-rclone` (opt-in, not in default flow)
Make target: `make storage-rclone`

Credentials go in `roles/install-csi-rclone/defaults/secrets.yml` (gitignored):
```yaml
csi_rclone_webdav_url: "https://your-nextcloud/remote.php/dav/files/user/"
csi_rclone_webdav_user: "user"
csi_rclone_webdav_pass: "app-password"
```

---

## PVC Migration history (smb-nas → longhorn-nvme, 2026-05-25/26)

All services migrated from smb-nas to longhorn-nvme. Pattern used:

```bash
# StatefulSet (Prometheus, Loki, Tempo): volumeClaimTemplates are immutable
kubectl delete pvc <old-pvc> -n <ns>   # triggers PV → Released
kubectl delete pv <old-pv>             # Retain policy → manual cleanup
# Edit role defaults: storage_class = longhorn-nvme, remove storage_role
make <service>                         # recreates with longhorn-nvme

# Deployment (registry, kaniko caches): simpler
kubectl delete pvc <old-pvc> -n <ns>
# Edit defaults
make <service>

# StatefulSets with data (kagent-pg, leloir-pg):
# backup first, then recreate fresh (data was non-critical)
```

---

## Troubleshooting

### PVC stuck Pending on longhorn-nvme
1. `kubectl get events -n <ns> --sort-by=.lastTimestamp`
2. Check CSI plugin runs on the target node: `kubectl get pods -n longhorn-system -l app=longhorn-csi-plugin`
3. CSI plugin must run on ALL nodes: `kubectl get ds longhorn-csi-plugin -n longhorn-system`

### CSINode stale after csi-plugin deploy
Pod stays in `AttachVolume.Attach failed — CSINode does not contain driver`:
```bash
kubectl delete pod <stuck-pod>   # force reschedule; CSINode refreshes on next attach
```

### smb-nas mount error 111 (Connection refused)
Port 445 closed — NAS SMB service is down or sleeping.
The `install-cifs-nas` role sends WoL automatically; wait ~60s after WoL for SMB to start.
