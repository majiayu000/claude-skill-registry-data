---
name: "zram-optimizer"
description: "A-to-Z zram swap optimization skill. Install zram-config from GitHub, benchmark compression algorithms and kernel parameters with a deterministic evaluator, and deploy the optimal 'raw-RAM-like' high-speed swap configuration for any Linux system. Use when setting up swap, optimizing memory, tuning zram, or replacing disk-based swap."
version: "1.0.0"
author: "Human Skill Team"
tags: ["zram", "swap", "memory", "optimization", "linux", "performance", "kernel-tuning"]
trigger_patterns:
 - "zram"
 - "swap"
 - "memory optimization"
 - "swap setup"
 - "zram setup"
 - "optimize swap"
 - "replace swap"
 - "ram optimization"
 - "memory pressure"
 - "swappiness"
---

# zram-optimizer — High-Performance Swap Engine Skill

## When to Use

Activate this skill when:
- Setting up or replacing swap on a Linux system
- Optimizing zram for maximum responsiveness
- Benchmarking compression algorithms (`lz4`, `lzo-rle`, `zstd`)
- Tuning kernel VM parameters (`swappiness`, `page-cluster`)
- Replacing slow disk-based swap with in-memory compressed swap
- The user wants a "raw-RAM-like" or "near-RAM-speed" swap experience

## Overview

This skill provides a complete, **deterministic**, data-driven workflow for deploying a high-performance zram swap engine on any Linux system. It follows the **OpenEvolve pattern**: build an evaluator, test all combinations, and deploy the empirically proven winner.

### Key Principle: No Guesswork

Instead of using generic defaults, this skill:
1. **Detects** the system's hardware (RAM, CPU cores)
2. **Benchmarks** every relevant zram parameter combination
3. **Ranks** configurations by a deterministic fitness score
4. **Deploys** the objectively fastest profile

## Prerequisites

### Install `zram-config` from GitHub

```bash
# 1. Clone the repository
sudo git clone https://github.com/ecdye/zram-config /opt/zram-config

# 2. Install
cd /opt/zram-config
sudo ./install.bash

# 3. Verify installation
systemctl status zram-config
cat /etc/ztab
```

> [!IMPORTANT]
> The `/etc/ztab` file is the single source of truth for zram configuration. All changes are made here and applied by `systemctl restart zram-config`.

### System Requirements
- Linux kernel 4.14+ (for `lz4` and `zstd` support)
- `zramctl` utility (part of `util-linux`)
- Root/sudo access
- Python 3.8+

## Workflow

```
Step 1: Detect Hardware → Step 2: Run Evaluator → Step 3: Analyze Results → Step 4: Deploy Winner
```

### Step 1: Detect System Hardware

```bash
# Get total RAM
FREE_RAM=$(free -g | awk '/^Mem:/{print $2}')
echo "Total RAM: ${FREE_RAM}G"

# Get CPU cores (used for zram streams)
CORES=$(nproc)
echo "CPU Cores: $CORES"

# Check supported algorithms
cat /sys/block/zram0/comp_algorithm 2>/dev/null || echo "zram not loaded"
```

**Sizing Rule:** For systems with ≤16GB RAM, set `disk_size` equal to ~50-60% of total RAM. For systems with >16GB RAM, 8GB is usually sufficient.

### Step 2: Run the Deterministic Evaluator

Use the combined `zram_optimizer.py` CLI to benchmark all configurations:

```bash
# Run the full benchmark suite
sudo human-skills '{
    "tool_name": "zram_optimizer",
    "tool_args": {
        "command": "bench"
    }
}'
```

The `bench` command will:
1. Iterate through all algorithm × swappiness × page-cluster combinations
2. For each combination, set up a fresh zram device
3. Run the `run` command as a subprocess to stress-test it with deterministic memory patterns
4. Record the fitness score to a CSV file
5. Clean up the zram device for the next test

### Step 3: Analyze Results

The benchmark produces a CSV file (`results.csv`) with columns:
```
Rank,Algorithm,Priority,Swappiness,PageCluster,FinalScore,...
```

**Higher score = better performance.** The agent should:
1. Sort by `Score` descending
2. Identify the top configuration
3. Present the results to the user

### Step 4: Deploy the Winner

```bash
# Example: Apply the winning configuration
sudo human-skills '{
    "tool_name": "zram_optimizer",
    "tool_args": {
        "command": "deploy",
        "algorithm": "lz4",
        "disk_size": "8G",
        "priority": 1000,
        "swappiness": 180,
        "page_cluster": 0
    }
}'
```

This command will:
1. Disable all existing swap
2. Write the optimized `/etc/ztab`
3. Restart `zram-config`
4. Automatically run `status` to verify the deployment

## Script Reference

### `scripts/zram_optimizer.py` — Unified CLI Tool

**Purpose:** Comprehensive zram tuning suite containing the memory evaluator, benchmark harness, and deployment automation.

**Commands Overview:**
```bash
# Review current zram/swap mappings
human-skills '{
    "tool_name": "zram_optimizer",
    "tool_args": {
        "command": "status"
    }
}'

# Low-level memory throughput test
human-skills '{
    "tool_name": "zram_optimizer",
    "tool_args": {
        "command": "run",
        "pressure_gb": "4.0"
    }
}'
```

## Understanding the Parameters

| Parameter | What It Does | Recommended |
|-----------|-------------|-------------|
| **Algorithm** | Compression codec. `lz4` = fastest decompression, `zstd` = best ratio, `lzo-rle` = balanced. | `lz4` for speed, `zstd` for memory-constrained |
| **disk_size** | Virtual swap capacity. Can exceed physical RAM because data is compressed. | 50-60% of RAM, or 8G for ≥16G systems |
| **mem_limit** | Physical RAM zram can consume. Should equal `disk_size` for full-speed operation. | Same as `disk_size` |
| **swappiness** | How aggressively the kernel uses swap. `60`=default, `180`=very aggressive zram usage. | `150-200` for zram (it's fast, so use it early) |
| **page-cluster** | Read-ahead pages. `0`=single page (best for zram), `3`=default (designed for spinning disks). | `0` always for zram |
| **swap_priority** | Higher = used first. Set high to prefer zram over any disk swap. | `100` or higher |

## Best Practices

### 1. Always Benchmark First
Never deploy a configuration without testing it. Even similar systems can behave differently.

### 2. Use Deterministic Evaluation
The evaluator must produce the same score for the same configuration every time. Never use `random` in the benchmark.

### 3. Nuclear Cleanup Between Tests
Each benchmark iteration must start from a completely clean state. The `bench` command handles this automatically.

### 4. Don't Oversize
Setting `disk_size` larger than necessary wastes CPU on compression without benefit. Match it to your actual usage pattern.

### 5. Monitor After Deployment
```bash
# Check compression ratio
human-skills '{
    "tool_name": "zram_optimizer",
    "tool_args": {
        "command": "status"
    }
}'
```

## Troubleshooting

### "Device or resource busy"
**Cause:** A process is still using the swap device.
**Fix:** The scripts handle cleanup automatically, but if stuck manually:
```bash
sudo swapoff /dev/zramX
sudo zramctl --reset /dev/zramX
```

### `zram-config` service fails to start
**Cause:** Stale zram devices from a previous run.
**Fix:** Disable zram completely then restart:
```bash
sudo swapoff -a
for dev in /dev/zram*; do sudo zramctl --reset "$dev" 2>/dev/null; done
sudo systemctl restart zram-config
```

## Example: Full Optimization Run

```bash
# 1. Install zram-config
sudo git clone https://github.com/ecdye/zram-config /opt/zram-config
cd /opt/zram-config && sudo ./install.bash

# 2. Run the benchmark (takes ~10-20 minutes)
sudo human-skills '{
    "tool_name": "zram_optimizer",
    "tool_args": {
        "command": "bench"
    }
}'

# 3. Check results
cat results.csv | sort -t, -k6 -rn | head -5

# 4. Deploy the winner (example: lz4, 8G, priority 1000, swappiness 180, page-cluster 0)
sudo human-skills '{
    "tool_name": "zram_optimizer",
    "tool_args": {
        "command": "deploy",
        "algorithm": "lz4",
        "disk_size": "8G",
        "priority": 1000,
        "swappiness": 180,
        "page_cluster": 0
    }
}'

# 5. Verify
human-skills '{
    "tool_name": "zram_optimizer",
    "tool_args": {
        "command": "status"
    }
}'
```

## Summary

| Step | Action | Tool |
|------|--------|------|
| 1 | Install `zram-config` | `git clone` + `install.bash` |
| 2 | Detect hardware | `free -g`, `nproc` |
| 3 | Benchmark all profiles | `zram_optimizer.py bench` → `zram_optimizer.py run` |
| 4 | Analyze CSV results | Sort by Score column |
| 5 | Deploy winner to `/etc/ztab` | `zram_optimizer.py deploy` |
| 6 | Verify deployment | `zram_optimizer.py status` |
