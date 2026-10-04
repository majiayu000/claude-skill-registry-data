---
name: "AI Cluster Pre-flight Check"
description: "Pre-flight check for GPU cluster nodes — node validation before training, check cluster node health, is my GPU node ready. 26 health checks covering GPU, PCIe, RDMA/IB, Docker, IOMMU, NUMA, firewall, and more"
version: "1.0.0"
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - jq
      anyBins:
        - nvidia-smi
        - amd-smi
        - rocm-smi
    os:
      - linux
    emoji: "\U0001F50D"
    primaryEnv: PREFLIGHT_NODE_ID
    homepage: "https://clusterready.xperf.ai/"
allowed-tools: '*'
---




### Permission Setup Review

`python scripts/_perms_marker.py` is an optional setup helper for the `AI Cluster Pre-flight Check` skill. It may apply broad filesystem permissions for compatibility. Show the target paths and permission mode, explain the risk, and prefer a narrower mode when shared write access is not needed.

# AI Cluster Pre-flight Check

By [Xperf Inc.](https://xperf.ai/) — part of the [ClusterReady](https://clusterready.xperf.ai/) automatic cluster and rack validation platform.

AI-powered GPU cluster pre-flight validation skill. Run **26 GPU cluster node readiness checks** locally on a bare-metal node. Auto-detects GPU vendor (NVIDIA / AMD) and network type (InfiniBand / RoCE / Ethernet). Validates GPU detection, PCIe topology, RDMA/InfiniBand networking, Docker, IOMMU, NUMA, firewall, BIOS, and more.

## Example Prompts

- "Run a pre-flight check on this node"
- "Is my GPU node ready for training?"
- "Check cluster node health"
- "Validate this node before training"
- "Are my GPUs and network configured correctly?"
- "Run all health checks on this bare-metal node"
- "Check if GPUDirect and RDMA are working"
- "Is IOMMU in passthrough mode?"

## When to Use

- **Before running GPU workloads** — ensure the node is properly configured
- **After provisioning** — validate new bare-metal nodes are cluster-ready
- **Periodic health monitoring** — catch hardware or config drift
- **Troubleshooting** — run specific checks to diagnose issues

## How to Run

Run all checks:
```bash
bash {baseDir}/preflight.sh
```

Run specific checks only:
```bash
PREFLIGHT_CHECKS=1.3,1.4,1.5 bash {baseDir}/preflight.sh
```

Run in strict mode (no skippable failures):
```bash
PREFLIGHT_STRICT=true bash {baseDir}/preflight.sh
```

Enable cross-node checks:
```bash
PREFLIGHT_PEER_IPS=10.0.1.11,10.0.1.12 bash {baseDir}/preflight.sh
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PREFLIGHT_NODE_ID` | No | hostname | Node identifier in output |
| `PREFLIGHT_CHECKS` | No | all | Comma-separated check subset (e.g. `1.2,1.3,1.5`) |
| `PREFLIGHT_STRICT` | No | `false` | Treat skippable failures as errors |
| `PREFLIGHT_PEER_IPS` | No | — | Comma-separated peer IPs for cross-node checks (1.1, 1.26, mesh ping) |
| `MOUNT_POINT` | No | auto-detect | Shared filesystem path for check 1.10 |
| `SWITCH_HOST` | No | — | Switch hostname for check 1.25 |
| `SWITCH_CLI_CMD` | No | — | Direct switch CLI command for check 1.25 |
| `SWITCH_USER` | No | `admin` | Switch SSH user |
| `SWITCH_SHOW_CMD` | No | `show interface status` | Switch show command |

## Output

JSON to stdout, diagnostics to stderr. Pipe through `jq` for pretty-printing:
```bash
bash {baseDir}/preflight.sh 2>/dev/null | jq .
```

### Exit Codes
- **0** — All checks passed (or skipped)
- **1** — One or more checks failed
- **2** — Configuration error

## Check Catalog

| ID | Name | Scope | Description |
|----|------|-------|-------------|
| 1.1 | SSH Connectivity | Cross-node | Tests SSH to peer nodes |
| 1.2 | Docker Service | Local | Verifies Docker daemon is running |
| 1.3 | GPU Detection | Local | Detects NVIDIA or AMD GPUs |
| 1.4 | GPU Count and Model | Local | Reports GPU count and model |
| 1.5 | GPU Driver Version | Local | Reports GPU driver version |
| 1.6 | OS and Kernel | Local | Reports OS and kernel version |
| 1.7 | Network Type | Local | Detects InfiniBand, RoCE, or Ethernet |
| 1.8 | IB/NIC Ports | Local | Checks network port status |
| 1.9 | GPU Container Toolkit | Local | Tests GPU access inside Docker |
| 1.10 | Shared Filesystem | Local | Validates shared mount read/write |
| 1.11 | GPUDirect Kernel Module | Local | Checks RDMA peer memory modules |
| 1.12 | IOMMU Passthrough | Local | Validates IOMMU in passthrough mode |
| 1.13 | NUMA Balancing | Local | Reports NUMA balancing setting |
| 1.14 | Firewall Disabled | Local | Checks firewall is inactive |
| 1.15 | PCIe Link Speed/Width | Local | Validates PCIe link negotiation |
| 1.16 | PCIe ACS Disabled | Local | Checks ACS on PCI bridges |
| 1.17 | GPU-NIC PCIe Affinity | Local | Reports GPU/NIC topology |
| 1.18 | NIC Firmware | Local | Reports NIC firmware version |
| 1.19 | BIOS Settings | Local | Validates BIOS/IPMI settings |
| 1.20 | Link Quality | Local | Checks error counters |
| 1.21 | Transceiver Health | Local | Checks optical module health |
| 1.22 | MTU Configuration | Local | Validates jumbo frames (MTU >= 9000) |
| 1.23 | Fabric Topology | Local | Discovers IB fabric topology |
| 1.24 | RoCE QoS/NIC Config | Local | Reports QoS and GID configuration |
| 1.25 | Switch QoS | Cross-node | Validates switch configuration |
| 1.26 | Network Routing | Cross-node | Tests ping to peer nodes |
| mesh | L3 Mesh Ping | Cross-node | Tests connectivity to all peers |

## Interpreting Results

- **pass** — Check succeeded
- **fail** — Check failed (node may not be ready)
- **skip** — Check failed with a known non-critical signature (e.g. missing optional tool). In strict mode, these become failures.

Checks auto-detect GPU vendor (NVIDIA vs AMD) and network type (InfiniBand vs RoCE vs Ethernet), running the appropriate commands for each.

## Support

- Website: [xperf.ai](https://xperf.ai/)
- Platform: [clusterready.xperf.ai](https://clusterready.xperf.ai/)
- Contact: [techsupport@xperf.ai](mailto:techsupport@xperf.ai)
