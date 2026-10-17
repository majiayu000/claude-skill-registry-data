---
name: longhorn
description: Longhorn block storage configuration, StorageClasses, NVMe vs eMMC disks, and DiskPressure troubleshooting
---

# Longhorn Storage Skill

## Overview
Longhorn provides distributed block storage (`longhorn-nvme` StorageClass) for PVC-backed services on the RK1 nodes (OpenClaw, Hermes, NPU pool).

## Disk Topology (Crucial for RK1 Nodes)
Each Turing Pi 2 RK1 node has two disks:
- `/dev/mmcblk0p2` (eMMC, ~29 GB): Mounted at `/` (rootfs). Contains Longhorn's default path `/var/lib/longhorn/`.
- `/dev/nvme0n1` (NVMe, ~500 GB): Mounted at `/mnt/nvme`.

### The "DiskPressure" Trap
By default, Longhorn groups all available disks on a node into its storage pool and scatters replicas randomly. If `default-disk` (`/var/lib/longhorn/`) is enabled, Longhorn will write replicas to the tiny eMMC drive. 

When deploying heavy models (like the 8.6 GB Llama model for the NPU pool with 3 replicas), Longhorn will fill the eMMC to 85%, triggering Kubernetes **DiskPressure**. This causes the node to evict pods (e.g., `hermes-agent-mcp`), leading to cascading failures (e.g., OpenClaw crashing).

### The Fix: Forcing NVMe
1. **Helm Values (`longhorn-values.yaml.j2`)**:
   Always set `createDefaultDiskLabeledNodes: true` in `defaultSettings`. This forces Longhorn to respect node annotations (`node.longhorn.io/default-disks-config`) which define the `nvme-fs` disk.

2. **StorageClass (`storageclass-v2.yaml.j2`)**:
   Always include `diskSelector: "nvme"` in the StorageClass parameters. This guarantees that Longhorn will **only** schedule replicas to disks tagged with `nvme` (which we set via node annotations).

3. **Emergency Eviction (API Patch)**:
   If replicas are already trapped on the eMMC, patch the Longhorn nodes to disable scheduling and request eviction on the default disk:
   ```python
   # Disable scheduling and request eviction on default-disk
   patch_disks["default-disk-..."] = {
       "allowScheduling": False,
       "evictionRequested": True
   }
   ```
   Longhorn will immediately rebuild the replicas on the NVMe disk and free up the eMMC.
