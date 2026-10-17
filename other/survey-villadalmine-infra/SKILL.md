---
name: survey
description: >
  gather-node-info role: hardware/software survey for cluster planning.
  Collects CPU, RAM, storage, GPU/NPU, network, K8s-readiness, NTP, security,
  and network storage info from every node. Output: human-readable + JSON per node.
metadata:
  tags: [survey, hardware, planning, gather-node-info, json]
---

# survey — Node Hardware Survey

## Run

```bash
make survey
# Output: survey/<hostname>.json (one file per node)
# Also prints human-readable summary per node during run
```

Runs `roles/gather-node-info` against all nodes in inventory.

---

## What It Collects

| Section | Fields | Why it matters |
|---------|--------|----------------|
| `board` | device tree / DMI model | identifies SBC vs server |
| `os` / `kernel` / `arch` | distro, kernel version, aarch64/x86 | compatibility checks |
| `cpu.cores` / `mhz_per_cluster` | count + per-cluster frequency | big.LITTLE detection (RK3588S) |
| `ram.total_gb` / `ram.type` | total GB, DDR type if available | control-plane requires ≥4GB |
| `swap.enabled` | bool | K8s requires swap off (warns if on) |
| `storage.devices` | lsblk output: name, size, transport | NVMe vs eMMC vs USB |
| `storage.write_latency` | ms/op via dd | etcd needs <5ms; warns if exceeded |
| `storage.root_df` / `varlib_df` | disk space on / and /var/lib | container image space |
| `gpu_npu` | /dev/rknpu0, /dev/mali0, /dev/dri/* | AI workload capability |
| `network.interfaces` | NIC speed, driver, MAC | bandwidth planning |
| `network.inter_node_latency` | ping rtt to all peers | etcd quorum health (<2ms ideal) |
| `network.is_nat` / `public_ip` | NAT detection | edge node classification |
| `dns.servers` / `dns.type` | nameservers, local vs public | Pi-hole detection |
| `ntp.synced` | bool | etcd dies with clock skew >1s |
| `k8s_readiness.cgroups_version` | v1 or v2 | Cilium requires v2 |
| `k8s_readiness.ebpf_capable` | bool | required for Cilium |
| `k8s_readiness.modules` | br_netfilter, overlay, ip_vs... | K8s networking |
| `k8s_readiness.port_conflicts` | ports 6443, 2379, 2380... | detects existing services |
| `k8s_readiness.container_runtime` | containerd version if present | warns if K3s may conflict |
| `k8s_readiness.k3s_installed` | version if installed | clean install recommended if set |
| `security.apparmor` / `selinux` | status | cluster security baseline |
| `net_storage.network_scan` | NFS/SMB/iSCSI/Ceph/MinIO detection | CSI driver planning |
| `warnings` | list of issues | actionable pre-install checklist |

---

## Reading the JSON Output

```bash
# All nodes
ls survey/

# Quick summary of a node
cat survey/srv-rk1-nvme-01.json | python3 -m json.tool | less

# Find nodes with NVMe
grep -l '"nvme"' survey/*.json

# Find nodes with warnings
python3 -c "
import json, glob
for f in glob.glob('survey/*.json'):
    d = json.load(open(f))
    if d['warnings']:
        print(f.split('/')[-1].replace('.json',''), d['warnings'])
"

# Node comparison — RAM
python3 -c "
import json, glob
for f in sorted(glob.glob('survey/*.json')):
    d = json.load(open(f))
    name = f.split('/')[-1].replace('.json','')
    print(f'{name:35s} {d[\"ram\"][\"total_gb\"]:>5}GB  {d[\"storage\"][\"write_latency\"]}')
"
```

---

## Interpreting Warnings

| Warning | Meaning | Action |
|---------|---------|--------|
| `K3s already installed` | node has leftover K3s | run `make clean` first or accept risk |
| `Existing container runtime` | containerd/docker present | may conflict with K3s bundled containerd |
| `Swap enabled` | swap is on | K8s needs swap off: `swapoff -a` + remove from fstab |
| `cgroups v1` | old kernel/config | Cilium requires v2; upgrade kernel |
| `Port XXXX in use` | something using K8s ports | investigate before bootstrap |
| `disk write > 4ms` | slow storage | not suitable for control-plane/etcd |
| `NTP not synced` | clock drift | fix before etcd; `timedatectl set-ntp true` |

---

## Node Profiles (from survey data)

Use this to classify nodes before assigning K8s roles:

| Profile | Criteria |
|---------|----------|
| **control-plane** | cgroups v2, eBPF, write_latency <5ms, ≥4GB RAM, NVMe preferred |
| **worker-general** | cgroups v2, any storage, ≥2GB RAM |
| **worker-ai** | has `/dev/rknpu0` (Rockchip NPU) or `/dev/mali0`, ≥16GB RAM |
| **worker-storage** | large disk, SMB/NFS reachable in network scan |
| **edge** | `is_nat: false` (direct public IP) |
| **standalone** | any combination — not recommended for cluster |

---

## Fallback Chain (how data is collected)

The role uses multi-level fallbacks — no tool is required:

```
lscpu → /proc/cpuinfo
lsblk → /sys/block/*
free  → /proc/meminfo
ethtool → /sys/class/net/*/device/uevent
resolvectl → /etc/resolv.conf
timedatectl → chronyc → ntpq
curl → wget → python3 urllib
nc → /dev/tcp (bash builtin)
```

This means the survey runs on any Linux ≥4.x with any package set.

---

## Role Structure

```
roles/gather-node-info/tasks/
  main.yml          ← orchestrator: includes all sub-tasks + consolidates + saves JSON
  os.yml            ← OS, kernel, arch, uptime
  cpu.yml           ← model, cores, MHz per cpufreq policy (big.LITTLE aware)
  memory.yml        ← RAM stats + type, swap + warning
  storage.yml       ← lsblk, boot device, root/varlib df, eMMC type
  storage-iops.yml  ← dd write latency test (etcd suitability)
  gpu.yml           ← /dev/rknpu0, /dev/mali0, /dev/dri/*
  network.yml       ← per-NIC speed/driver/MAC + inter-node ping latency
  nat.yml           ← local IPs, gateway, public IP, NAT detection
  dns.yml           ← nameservers, type, resolution test
  ntp.yml           ← timedatectl/chronyc/ntpq sync status
  k8s-readiness.yml ← cgroups, modules, ip_forward, BPF, kernel params, ulimits, ports, runtime
  security.yml      ← AppArmor, SELinux, firewall
  netstore.yml      ← mounts, daemons, dirs, modules, port scan
```

---

## Adding New Data Points

1. Add tasks to the relevant sub-task file (or create a new one)
2. Add `include_tasks: newfile.yml` to `main.yml`
3. Add the new fact to the `node_survey` dict consolidation block in `main.yml`
4. The next `make survey` run will include the new field in all JSON outputs
