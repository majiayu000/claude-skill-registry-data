---
name: profile-compare-with
description: Compare performance of the current branch against another branch (default unstable)
argument-hint: "[branch-name]"
---

Compare the performance of the current branch against a reference branch using `certus-api-bench_v2.py`. The benchmark runs on the local node with identical parameters for both branches, producing a side-by-side comparison.

## Arguments

- `branch-name` (optional): The branch to compare against. Defaults to `unstable`.

## Interactive Configuration

Before starting, ask the user for the **server profile** to use:

- **Profile name**: Which `CERTUS_PROFILE` to build with (e.g., `full`, `full-remote`, `full-fs-block`, `full-kernel-block`).
  Available profiles can be listed from `apps/certus-server-yaml/profiles/`.
- **Cargo features** (optional): Extra features to pass (e.g., `--features rdma`). Default: none beyond what the profile implies.

If the user doesn't specify, default to `CERTUS_PROFILE=full`.

## Workflow

### 1. Pre-flight

- Record the current branch name: `CURRENT_BRANCH=$(git branch --show-current)`
- Record the comparison branch: `COMPARE_BRANCH` (from argument, default `unstable`)
- Check for uncommitted changes. If any exist, auto-commit them:
  ```bash
  git add -A && git commit -m "wip: auto-save before performance comparison"
  ```
- Verify both branches exist locally (fetch if needed):
  ```bash
  git fetch origin $COMPARE_BRANCH 2>/dev/null || true
  ```

### 2. Hardware Detection (if profile requires real SSDs)

If the selected profile uses a real block device backend (any profile other than those using `--device-path`), detect available NVMe SSDs:

```bash
# Detect NVMe SSDs via lspci (Samsung, Intel, Kioxia common vendor IDs)
# or use the SPDK-detected devices from a quick probe
lspci -Dnd ::0108 | sort
```

**Select up to 4 SSDs** from those available. For each device, determine its NUMA node:

```bash
cat /sys/bus/pci/devices/<PCI_ADDR>/numa_node
```

**NUMA warning**: If any selected SSD is outside NUMA node 0, print:
```
⚠️  WARNING: SSD <PCI_ADDR> is on NUMA node <N> (not node 0).
   Performance may be reduced due to cross-NUMA memory access.
   Consider using only NUMA-0 devices for accurate benchmarking.
```

Pass the selected devices as:
```bash
--device-pci <PCI1> --device-pci <PCI2> --device-pci <PCI3> --device-pci <PCI4>
```

If the profile can use `--device-path /dev/null` (no real SSD needed), use that instead and skip hardware detection.

### 3. Build and Benchmark Current Branch

- Build release:
  ```bash
  CERTUS_PROFILE=$PROFILE cargo build -p certus-server-yaml --release $FEATURES
  ```
- Start the server:
  ```bash
  target/release/certus-server-yaml $DEVICE_FLAGS --format --memory-tier-size 4G &
  SERVER_PID=$!
  sleep 5
  ```
- Run the benchmark:
  ```bash
  cd apps/python
  python3 certus-api-bench_v2.py \
      --clients 1 \
      --num-objects 32 \
      --iterations 20 \
      --block-size 4M \
      --batch-size 16 \
      --pipeline-depth 4 \
      --memory-tier-size 2G
  ```
- Capture the full output (including throughput numbers) to `CURRENT_RESULTS`
- Stop the server:
  ```bash
  kill $SERVER_PID && wait $SERVER_PID 2>/dev/null
  ```

### 4. Switch to Comparison Branch, Build and Benchmark

- Checkout the comparison branch:
  ```bash
  git checkout $COMPARE_BRANCH
  ```
- Build release (same profile and features):
  ```bash
  CERTUS_PROFILE=$PROFILE cargo build -p certus-server-yaml --release $FEATURES
  ```
- Start the server (same device flags and memory-tier size):
  ```bash
  target/release/certus-server-yaml $DEVICE_FLAGS --format --memory-tier-size 4G &
  SERVER_PID=$!
  sleep 5
  ```
- Run the same benchmark with identical parameters (including `--memory-tier-size 2G`)
- Capture output to `COMPARE_RESULTS`
- Stop the server

### 5. Return to Original Branch

```bash
git checkout $CURRENT_BRANCH
```

### 6. Report

Print a comparison table with the key metrics extracted from both runs:

```
================================================================
Performance Comparison: $CURRENT_BRANCH vs $COMPARE_BRANCH
================================================================

Profile: $PROFILE  Features: $FEATURES
Devices: $DEVICE_FLAGS
Benchmark: certus-api-bench_v2.py
Parameters: --clients 1 --num-objects 32 --iterations 20 --block-size 4M --batch-size 16 --pipeline-depth 4

                          Current ($CURRENT_BRANCH)    Reference ($COMPARE_BRANCH)    Delta
Populate throughput:      X.XX GB/s                    Y.YY GB/s                      +/-Z.Z%
Hot lookup throughput:    X.XX GB/s                    Y.YY GB/s                      +/-Z.Z%
Cold lookup throughput:   X.XX GB/s                    Y.YY GB/s                      +/-Z.Z%
Hot lookup latency (p50): X.XX ms                     Y.YY ms                        +/-Z.Z%
Hot lookup latency (p99): X.XX ms                     Y.YY ms                        +/-Z.Z%
```

Mark regressions (>5% slower) with ⚠️ and improvements (>5% faster) with ✓.

## Important Notes

- If the comparison branch does not compile with the selected profile, report the build error and skip its benchmark.
- Always return to the original branch at the end, even if something fails.
- The benchmark parameters above are defaults — the user may override them in their invocation message.
- Both builds use the SAME profile and features to ensure apples-to-apples comparison.
- When using real SSDs, always pass `--format` to start fresh (avoids stale data affecting results).
- The `--device-path /dev/null` mode only exercises the hot path (memory-tier). Use real SSDs to benchmark the cold path (SSD read + promote).
