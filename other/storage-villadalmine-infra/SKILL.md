---
name: storage
description: >
  CIFS/SMB storage on K3s for a legacy SMB1 NAS using csi-driver-smb.
  Covers static PV/PVC mounts, optional dynamic StorageClass testing, and
  the required mount options and troubleshooting for permission issues.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, storage, smb, cifs, csi, nas, pv, pvc, smb1]
---

# Storage Skill

## Cluster Context

This cluster uses `csi-driver-smb` for a legacy NAS that only supports SMB1.

Role: `install-cifs-nas`
Tag: `storage`

Current tested values:

| Key | Value |
|---|---|
| NAS IP | `192.168.178.102` |
| Share | `//192.168.178.102/service` |
| Dynamic source | `//192.168.178.102/service/Torrent` |
| Static PV | `smb-nas-pv` |
| Static PVC | `smb-nas-pvc` |
| Dynamic SC | `smb-nas` |
| Dynamic PVC | `smb-nas-dynamic-pvc` |

### Flags

- `cifs_enable_static=true` enables the static PV/PVC/pod test
- `cifs_enable_dynamic_test=true` enables the dynamic StorageClass/PVC/pod test

---

## Static flow

The static path binds a fixed PV to a fixed PVC.

- `storageClassName: ""`
- `volumeName: smb-nas-pv`
- `mountOptions` must include:
  - `vers=1.0`
  - `uid=1000`
  - `gid=1000`
  - `file_mode=0777`
  - `dir_mode=0777`
  - `noperm`

Test pod:
- `smb-test-pod`
- mounts `subPath: Torrent`

---

## Dynamic flow

The dynamic path provisions a PVC through a `StorageClass`.

Important:
- `source` must point to a writable subdirectory, not the share root
- tested working value: `//192.168.178.102/service/Torrent`
- the upstream example options `mfsymlinks`, `cache=strict`, and `noserverino` are kept for the CSI test path

Dynamic test pod:
- `smb-dynamic-test-pod`
- writes to `/mnt/smb/prueba-escritura-dinamica.txt`

---

## Usage

```bash
make storage
```

Or directly:

```bash
ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini --tags storage
```

---

## Troubleshooting

### `failed to make subdirectory: permission denied`
- The `StorageClass.source` points to a path the NAS does not allow the CSI driver to create under.
- Use a known writable subdirectory like `//192.168.178.102/service/Torrent`.

### PVC stays Pending
1. Check that `StorageClass` exists: `kubectl get sc`
2. Check events: `kubectl get events -n default --sort-by=.lastTimestamp`
3. Verify the SMB CSI driver pod is running in `kube-system`

### Mount works statically but not dynamically
- Static PV/PVC and dynamic CSI provisioning are separate paths.
- Check `cifs_enable_static` and `cifs_enable_dynamic_test`.

### High I/O wait causing `CrashLoopBackOff` in databases (e.g. PostgreSQL)
- **Symptom**: Pods using `smb-nas` (or `smb-nas-pg`) for database data get killed by Kubernetes before they finish starting up (e.g., during `pre-fsync` directory syncing).
- **Cause**: The NAS SMB v1 share introduces immense network I/O latency, causing initialization routines to exceed the default `livenessProbe` timeout.
- **Fix**: Patch the deployment's `livenessProbe.initialDelaySeconds` to a very high value (e.g., `600` seconds) to give the application enough time to traverse and sync the thousands of files without being prematurely SIGKILLed.
