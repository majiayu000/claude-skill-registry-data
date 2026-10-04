---
name: hyper-v
description: "Hyper-V on Windows Server across versions 2016-2025: hypervisor architecture, VM generations, memory management, virtual networking, virtual storage, integration services, checkpoints, live migration, replication, and GPU partitioning. Use when: \"Hyper-V\", \"virtual machine\", \"VM\", \"live migration\", \"virtual switch\", \"VHDX\", \"VHD\", \"Hyper-V Replica\", \"checkpoint\", \"nested virtualization\", \"GPU-P\", \"GPU partitioning\", \"vSwitch\", \"SET teaming\", \"SR-IOV\", \"dynamic memory\", \"vTPM\", \"shielded VM\", \"Gen1 VM\", \"Gen2 VM\", \"NUMA\", \"DDA\", \"discrete device assignment\". Do NOT use for VMware vSphere/ESXi, Proxmox, KVM, or other non-Microsoft hypervisors, and do NOT use for general hypervisor comparison/selection questions (\"which hypervisor should I use\") — use the `virtualization` plugin. Do NOT use for cluster quorum/CSV mechanics — use the `failover-clustering` skill."
license: MIT
---

# Hyper-V on Windows Server

This skill covers Hyper-V on Windows Server across versions 2016, 2019, 2022, and 2025. It provides deep knowledge of:

- Type-1 hypervisor architecture (parent/child partitions, VMBus, enlightenments)
- VM generations (Gen1 BIOS vs Gen2 UEFI), configuration versions, and upgrade paths
- Memory management (static, dynamic memory, NUMA topology, hot-add, Smart Paging)
- Virtual networking (vSwitch types, Switch Embedded Teaming, SR-IOV, VLAN, bandwidth management)
- Virtual storage (VHD/VHDX, disk types, Storage QoS, shared VHDX, VHD Sets)
- Integration services (Windows and Linux guests, KVP, heartbeat, VSS)
- Checkpoints (standard vs production, differencing chains, performance impact)
- Live migration (shared storage, shared-nothing, storage migration, RDMA)
- Hyper-V Replica (asynchronous DR replication, planned/unplanned failover)
- GPU partitioning (GPU-P), Discrete Device Assignment (DDA), nested virtualization
- Failover Clustering integration for VM high availability

When a question is version-specific, note the relevant version differences. When the version is unknown, provide general guidance and flag where behavior varies. For general Windows Server administration, see the `windows-server` skill.

## How to Approach Tasks

Route by request type: **troubleshooting** → `references/diagnostics.md`; **architecture** → `references/architecture.md`; **best practices/config** → `references/best-practices.md`; **performance analysis** → the diagnostic scripts; **administration** → apply Hyper-V management expertise directly.

**Identify the Windows Server version first** — feature availability shifts by version (nested virt on AMD requires 2022+, GPU-P live migration requires 2025). Reason from NUMA topology, I/O paths, hypervisor overhead, and guest enlightenments — not generic virtualization advice. Validate with performance counters, event logs, `Test-VMMigration`, and `Get-VHD` checks.

## Core Expertise

### Hypervisor Architecture

Hyper-V is a Type-1 (bare-metal) hypervisor. When the role is installed and the system reboots, the hypervisor (`hvax64.exe`) takes control of the hardware ring-0 layer. The Windows Server installation becomes the **parent partition** -- a privileged VM that retains direct driver access. All other VMs are **child partitions** that access hardware through synthetic (VMBus) or emulated paths.

Key components:
- **VMBus**: High-speed inter-partition communication channel using ring buffers. All synthetic device I/O traverses VMBus.
- **Virtualization Service Providers (VSPs)**: Run in the parent partition, handle physical device access.
- **Virtualization Service Clients (VSCs)**: Run in child partitions, route I/O through VMBus to VSPs.
- **Enlightenments**: Guest OS modifications that eliminate hardware emulation overhead (synthetic MSRs, relaxed timer, enlightened spinlock, APIC enlightenment).

### VM Generations

| Aspect | Gen1 | Gen2 |
|---|---|---|
| Firmware | BIOS (emulated) | UEFI |
| Boot device | IDE controller | SCSI (synthetic, VMBus) |
| Secure Boot | Not supported | Supported (default: on) |
| vTPM | Not supported | Supported |
| Max boot VHDX | 2 TB (MBR) | 64 TB (GPT) |
| Hot-add NIC/Memory | Not supported | Supported (2016+) |
| Use for | Legacy OS, 32-bit guests | All new deployments |

Use Gen2 for all new VMs. Gen1 only for legacy OS compatibility (Windows Server 2008 R2 or older, 32-bit guests, or specific emulated hardware requirements).

### Memory Management

**Static Memory**: Fixed allocation at startup. Best for database servers (SQL Server, Oracle) where the application manages its own memory cache and the DM balloon driver would compete.

**Dynamic Memory**: Hyper-V balances memory among VMs using a balloon driver.
- **Startup RAM**: Allocated at boot (before the balancer engages)
- **Minimum RAM**: Floor -- the VM is guaranteed at least this amount
- **Maximum RAM**: Ceiling -- the VM can never exceed this
- **Memory Buffer**: Percentage of headroom above current demand (default: 20%)
- **Memory Weight**: Priority (0-10000) when host memory is scarce (default: 5000)

**NUMA alignment**: Hyper-V schedules all vCPUs and memory for a VM within a single NUMA node by default. This eliminates remote memory access latency. NUMA spanning can be enabled for VMs that exceed a single node's capacity, but incurs cross-NUMA latency.

```powershell
Get-VMHostNumaNode | Select-Object NodeId, MemoryTotal, MemoryAvailable, ProcessorsAvailable
(Get-VMHost).NumaSpanningEnabled
```

### Virtual Networking

**Virtual Switch Types**:
| Type | VM-to-External | Host-to-VM | VM-to-VM | Isolation |
|---|---|---|---|---|
| External | Yes | Yes | Yes | None |
| Internal | No | Yes | Yes | Host-only |
| Private | No | No | Yes | Complete |

**Switch Embedded Teaming (SET)**: Replaces legacy NIC teaming (LBFO) for Hyper-V. Integrates into the vSwitch, supports 1-8 NICs, RDMA, and SR-IOV. Required for S2D deployments.

**SR-IOV**: Hardware-level NIC virtualization. Physical NIC exposes Virtual Functions (VFs) directly to VMs, bypassing the software vSwitch. Near line-rate throughput with minimal CPU overhead. VF is released during live migration (falls back to synthetic NIC).

**Bandwidth management**: Set minimum guaranteed and maximum bandwidth per vNIC to prevent noisy-neighbor issues.

### Virtual Storage

| Property | VHD (Legacy) | VHDX |
|---|---|---|
| Max size | 2 TB | 64 TB |
| Sector size | 512 bytes | 4 KB (aligned to modern drives) |
| Metadata | Vulnerable to power-loss corruption | Journaled (transaction-safe) |
| Online resize | No | Yes |
| Trim/Unmap | No | Yes |

Use VHDX for all new disks. Fixed-size VHDX for latency-sensitive workloads (databases, high-transaction apps); dynamic VHDX for general use on fast storage (overhead is negligible on all-flash).

**Shared storage for guest clusters**:
- **Shared VHDX** (2012 R2+): Multiple VMs attach to the same VHDX via SCSI. Limited -- no host-side VSS backup.
- **VHD Sets (.vhds)** (2016+): Preferred format. Supports host-side VSS backup, online checkpoints, and resize.

**Storage QoS**: Controls IOPS per VHDX to prevent noisy-neighbor effects:
```powershell
Set-VMHardDiskDrive -VMName "VM1" -ControllerType SCSI -ControllerNumber 0 -ControllerLocation 0 `
    -MinimumIOPS 500 -MaximumIOPS 5000
```

**Virtual Fibre Channel (vFC)**: Allows VMs to connect directly to FC SANs through host HBAs using N_Port ID Virtualization (NPIV). Requires NPIV-capable HBAs and SAN zoning for the VM's virtual WWN pair.

### Checkpoints

| Type | Mechanism | Application Consistency | Production Use |
|---|---|---|---|
| Standard | Saved state (memory snapshot) | No (crash-consistent) | No |
| Production (default 2016+) | VSS in guest / file system freeze | Yes | Yes (with caveats) |

When a checkpoint is created, a differencing VHDX (.avhdx) is created. All writes go to the differencing disk. Deep checkpoint chains (>3) measurably increase I/O latency. Delete checkpoints promptly -- the avhdx merge consumes I/O in the background.

```powershell
Set-VM -VMName "VM1" -CheckpointType Production
```

### Live Migration

Types:
- **Standard (shared storage)**: Only VM state transfers; storage stays in place. Fastest.
- **Shared-Nothing**: Transfers both VM state and storage. No shared storage required.
- **Storage Migration**: Moves VHDX files while the VM runs. No host migration.

Performance options: SMBTransport (fastest on RDMA/10 GbE+) > Compression (faster on slow networks) > TCP (default).

Prerequisites: Both hosts in the same domain (Kerberos) or CredSSP configured; compatible processors or Compatibility Mode enabled; firewall rules for TCP 6600 (live migration) and TCP 445 (SMB).

```powershell
Set-VMHost -VirtualMachineMigrationPerformanceOption SMBTransport
Set-VMHost -MaximumVirtualMachineMigrations 4
```

### Hyper-V Replica

Asynchronous VM replication to a secondary host for disaster recovery.

Key settings:
- **Replication interval**: 30 seconds (default), 5 minutes, or 15 minutes
- **Recovery points**: Up to 24 additional hourly snapshots at the replica
- **Authentication**: Kerberos (same domain) or certificate (workgroup/DMZ)

Extended Replication: Primary -> Replica -> Extended Replica (three-site chain).

```powershell
Enable-VMReplication -VMName "VM1" -ReplicaServerName "DR-HOST" `
    -ReplicaServerPort 8080 -AuthenticationType Kerberos `
    -ReplicationFrequencySec 300 -CompressionEnabled $true
Measure-VMReplication -VMName "VM1"
```

### Integration Services

Integration Services enable the synthetic device stack (VMBus) and cooperative hypervisor features. Starting with Windows Server 2016, IS for Windows guests are delivered via Windows Update -- no separate installer or VM downtime needed.

Key components: Operating System Shutdown, Time Synchronization, Data Exchange (KVP), Heartbeat, VSS (backup coordination), Guest Services (PowerShell Direct file copy), Dynamic Memory balloon driver.

Linux guests: Enlightenment drivers are built into the mainline Linux kernel since 3.4+ (hv_vmbus, hv_storvsc, hv_netvsc, hv_utils). RHEL 7+, Ubuntu 16.04+, SUSE 12+ include them out of the box.

## Version-Specific Changes

| Feature | 2016 | 2019 | 2022 | 2025 |
|---|---|---|---|---|
| Config Version | 8.0 | 9.0 | 10.0 | 12.0 |
| Nested Virtualization | Intel only | Intel only | Intel + AMD | Improved perf |
| Production Checkpoints | Introduced (default) | -- | -- | -- |
| Hot-add vNIC/Memory (Gen2) | Introduced | Broader | -- | -- |
| Shielded VMs | Windows only | Windows + Linux | -- | -- |
| DDA (PCIe passthrough) | Introduced | -- | -- | -- |
| PowerShell Direct | Introduced | -- | -- | -- |
| RDMA Live Migration | Basic | Improved | -- | Enhanced SR-IOV |
| vTPM for Linux | -- | -- | Introduced | -- |
| AMD Nested Virt | -- | -- | Introduced | -- |
| SMB over QUIC | -- | -- | Introduced | -- |
| Secured-core / HVCI | -- | -- | Introduced | -- |
| GPU-P Live Migration | -- | -- | -- | Introduced |
| GPU-P with Clustering | -- | -- | -- | Introduced |
| Max vCPUs per VM | 240 | 240 | 1024 | 2048 |
| Max RAM per VM | 12 TB | 12 TB | 12 TB | 240 TB |
| WAC (built-in) | -- | Separate install | Separate install | Integrated |

### Windows Server 2016 Highlights

- **Nested Virtualization (Intel VT-x only)**: Run Hyper-V inside a VM. Enable with `Set-VMProcessor -ExposeVirtualizationExtensions $true`. Requires Gen2 VM, static memory, MAC spoofing enabled.
- **Production Checkpoints (default)**: VSS-based checkpoints replace saved-state as default. Application-consistent.
- **VM Configuration Version 8.0**: New binary format (.vmcx/.vmrs) replaces XML. Faster, atomic writes, reduced corruption.
- **Hot-add vNIC and Memory (Gen2)**: Add vNICs and increase memory on running Gen2 VMs.
- **Shielded VMs**: Encrypted VMs protected by Host Guardian Service (HGS). Uses vTPM + BitLocker.
- **Discrete Device Assignment (DDA)**: Pass PCIe devices (GPU, NVMe, FPGA) directly to a VM. Not live-migratable.
- **PowerShell Direct**: Run commands inside a VM via VMBus without network. `Enter-PSSession -VMName "VM1"`.
- **Container Integration**: Hyper-V isolation containers introduced.

### Windows Server 2019 Highlights

- **Improved RDMA**: Better SMB Direct for live migration and CSV. 25/40/100 GbE RDMA consistency.
- **VM CPU/Memory Hot-Resize (Gen2)**: More scenarios for online vCPU and memory addition.
- **Shielded VMs for Linux**: Ubuntu 16.04+, RHEL 7.3+ can be protected by HGS.
- **S2D Improvements**: Better resync, mixed media tiers, deduplication on ReFS.
- **Windows Admin Center**: Full Hyper-V management through browser-based WAC interface.

### Windows Server 2022 Highlights

- **Nested Virtualization on AMD**: AMD EPYC/Ryzen processors now support nested Hyper-V.
- **vTPM for Linux VMs**: Linux guests can use virtual TPM 2.0 for dm-crypt/LUKS encryption.
- **SMB over QUIC**: File share access over QUIC protocol without VPN.
- **Azure Arc Integration**: Hyper-V hosts register with Azure Arc for hybrid management.
- **Secured-core Server**: HVCI (Hypervisor-Protected Code Integrity) for hardware-based security.
- **ARM64 Guest Support (preview)**: Early support for ARM64 VMs.

### Windows Server 2025 Highlights

- **GPU Partitioning (GPU-P) with Live Migration**: GPU partitions live-migrate between hosts. Enables VDI and AI/ML workloads with HA.
- **GPU-P with Failover Clustering**: GPU-enabled VMs participate fully in cluster failover.
- **2048 vCPUs per VM**: Doubled from 1024 in 2022. Enables extreme in-memory computing.
- **240 TB RAM per VM**: Increased from 12 TB. Targets SAP HANA, Oracle TimesTen at extreme scale.
- **NUMA Performance**: Improved automatic NUMA-aware VM placement algorithms.
- **Windows Admin Center (built-in)**: WAC integrated without separate download.

## GPU Partitioning (GPU-P) and Discrete Device Assignment (DDA)

**Discrete Device Assignment (DDA)** (2016+) passes an entire PCIe device (GPU, NVMe, FPGA) directly to a VM. The host loses access to the device. DDA VMs cannot be live-migrated because the PCIe device is physically bound to the host.

**GPU Partitioning (GPU-P)** shares a single GPU across multiple VMs by creating partitions. Each VM gets a fraction of the GPU's compute and memory resources. Starting in Windows Server 2025, GPU-P supports live migration and failover clustering, enabling GPU-accelerated VMs to benefit from HA.

GPU-P requirements:
- Compatible GPU hardware (consult the GPU vendor's Hyper-V GPU-P support list)
- Matching GPU driver versions on all cluster hosts (for live migration)
- Windows Server 2025 for GPU-P live migration and clustering

```powershell
# View GPU partitioning capability
Get-VMHostPartitionableGpu | Select-Object Name, ValidPartitionCounts

# Assign GPU partition to a VM
Set-VMGpuPartitionAdapter -VMName "GPU-VM" -MinPartitionVRAM 80000000 `
    -MaxPartitionVRAM 100000000 -OptimalPartitionVRAM 100000000
```

## Nested Virtualization

Nested virtualization allows running Hyper-V inside a Hyper-V VM. This is valuable for lab environments, CI/CD testing, and container host development.

Requirements:
- Intel VT-x hosts (2016+) or AMD-V hosts (2022+)
- Gen2 VM recommended
- Static memory (Dynamic Memory must be disabled for the nested VM)
- MAC spoofing enabled on the VM's vNIC if nested VMs need network access
- Minimum 4 GB RAM, 2 vCPUs recommended

```powershell
# Enable nested virtualization (VM must be stopped)
Set-VMProcessor -VMName "NestedHost" -ExposeVirtualizationExtensions $true

# Enable MAC spoofing for nested VM networking
Set-VMNetworkAdapter -VMName "NestedHost" -MacAddressSpoofing On
```

Performance considerations: Nested virtualization adds hypervisor overhead to every VMEXIT in the nested guest. It is suitable for development and testing but not recommended for production workloads where performance is critical.

## Shielded VMs

Shielded VMs (2016+) protect VMs from unauthorized inspection or tampering, even by host administrators. They use:

- **Virtual TPM (vTPM)**: Software TPM 2.0 backed by the Host Guardian Service (HGS)
- **BitLocker**: Full disk encryption inside the guest, keyed to the vTPM
- **Key protector**: Ensures the VM can only start on HGS-attested hosts

Shielded VMs for Windows guests are available since 2016. Linux guest support (Ubuntu, RHEL) was added in 2019.

## Common Pitfalls

**1. Gen1 VMs for new deployments**
Gen1 VMs use emulated IDE for boot (slower) and lack Secure Boot, vTPM, and hot-add capabilities. Always use Gen2 for new VMs on supported guest OSes.

**2. Dynamic Memory for database servers**
SQL Server and Oracle manage their own memory caches. The DM balloon driver reclaims memory that the application believes is committed, causing cache pressure and performance degradation. Use static memory for database VMs.

**3. Deep checkpoint chains in production**
Checkpoint differencing chains >3 deep measurably increase disk latency. Create checkpoints only before specific operations, and delete them promptly after use.

**4. Live migration on the management NIC**
Defaulting live migration to the management NIC saturates the admin network and results in extremely slow migrations. Dedicate a 10 GbE+ NIC for migration traffic and configure network binding.

**5. Upgrading VM configuration version prematurely**
`Update-VMVersion` is irreversible. Once upgraded, the VM cannot run on an older host version. Confirm that the VM will never need to return to an older host before upgrading.

**6. AV scanning VHDX files on the host**
Anti-virus software scanning VHDX files on the host causes significant I/O overhead and can trigger false positives. Configure host-side AV exclusions for all virtual disk file types.

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Type-1 hypervisor internals, partitions, VMBus, enlightenments, Gen1 vs Gen2, memory architecture, virtual networking (vSwitch, SET, SR-IOV), virtual storage (VHD/VHDX, QoS), integration services. Read for "how does X work" questions.
- `references/diagnostics.md` -- VM health monitoring, performance diagnostics (CPU/memory/disk/network per VM), troubleshooting workflows (VM won't start, migration failure, slow VM, replication lag). Read when troubleshooting.
- `references/best-practices.md` -- VM sizing, NUMA placement, memory allocation, disk configuration, checkpoint practices, live migration config, replication setup, host configuration. Read for design and operations questions.

## Diagnostic Scripts

Run these for rapid Hyper-V assessment:

| Script | Purpose |
|---|---|
| `scripts/01-hyperv-host-health.ps1` | Host config, NUMA topology, overcommit ratios, feature status |
| `scripts/02-vm-inventory.ps1` | Full VM inventory: generation, config, CPU, memory, disks, NICs |
| `scripts/03-vm-performance.ps1` | Real-time per-VM CPU, memory pressure, disk latency, network I/O |
| `scripts/04-virtual-switch.ps1` | vSwitch config, SET teaming, SR-IOV, VLAN, bandwidth policies |
| `scripts/05-storage-health.ps1` | VHDX health, fragmentation, checkpoint chains, Storage QoS |
| `scripts/06-replication-health.ps1` | Replica status, RPO compliance, failover readiness |
| `scripts/07-live-migration.ps1` | Migration config, network binding, RDMA, compatibility mode |
| `scripts/08-checkpoint-audit.ps1` | Checkpoint inventory, age, disk impact, stale detection |
| `scripts/09-integration-services.ps1` | IS component health, version audit, KVP data |
| `scripts/10-nested-virt.ps1` | Nested virtualization prerequisites and configuration audit |

## Key Ports

| Port | Protocol | Purpose |
|---|---|---|
| 2179 | TCP | Hyper-V Remote Management (vmms) |
| 6600 | TCP | Live Migration |
| 445 | TCP | SMB (storage migration, CSV) |
| 135 | TCP | RPC Endpoint Mapper |
| 8080 | TCP | Hyper-V Replica (Kerberos, default) |
| 443 | TCP | Hyper-V Replica (certificate) |
| 3343 | UDP | Cluster Heartbeat |
