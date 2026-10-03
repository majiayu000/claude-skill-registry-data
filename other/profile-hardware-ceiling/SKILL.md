---
name: profile-hardware-ceiling
description: Measure raw hardware bandwidth ceilings for all data paths (NVMe, GPU, memory, P2P, GDS, GDRCopy) on the current platform
argument-hint: "[output-dir]"
---

Measure the raw hardware bandwidth ceilings for every data path the Certus storage system
uses. This skill is portable — it auto-detects hardware, adapts to whatever GPUs/drives/tools
are present, and produces a comprehensive matrix report.

Output:
- `<output-dir>/hardware-ceiling-<YYYY-MM-DD>.md` (default output-dir: `profiling/`)
- `<output-dir>/hardware_profile_<YYYY-MM-DD>.yaml`

## Data Paths to Measure

Certus has multiple data paths depending on cold/hot and P2P vs memory-tier modes:

**Measured paths (active benchmarks):**
1. **NVMe → Host RAM read** (raw drive read bandwidth — also gives DMA IO size sweep)
2. **NVMe → Host RAM write** (raw drive sequential write bandwidth)
3. **Host RAM → GPU / GPU → Host RAM** (cudaMemcpy H2D + D2H, NUMA-local and cross-NUMA)
4. **GPU D2D** (staging ring → final destination, part of P2P pipeline)
5. **GDRCopy CPU ↔ GPU BAR1** (CPU-initiated BAR1 access, diagnostic)
6. **NVMe → GPU via GDS** (GPUDirect Storage — nvidia_fs/cuFile, if available)
7. **Host RAM memcpy** (baseline — same-NUMA and cross-NUMA)
8. **NVMe DMA → BAR1** (P2P microbenchmark — closest isolated cold-path hardware ceiling)

**Derived analysis (no additional benchmarks):**
9. **Topology-Aware P2P Matrix** (routes each drive-group/GPU pairing through the topology)

## Platform Detection (Step 1)

Auto-detect and record:
- CPU: model, cores, NUMA nodes, cache sizes (`lscpu`)
- Hostname: use `hostname -s` (short name only — strip domain suffix)
- OS: distro, kernel (`uname -r`, `/etc/os-release`)
- GPU(s): model, PCIe gen/width, BAR1 size, CUDA device index, PCI address
  - `nvidia-smi -q` for BAR1/memory
  - `lspci -vvs <addr>` for LnkSta (speed/width)
- NVMe drive(s): model, PCIe gen/width, PCI address
  - `lspci -vvs <addr>` for LnkSta
- PCIe topology: which root complex each device is on (`lspci -tv`)
  - Map which drives are "same-root" with which GPUs
- Available tools:
  - `nvidia_fs` module: `lsmod | grep nvidia_fs`
  - `gdsio`: `which gdsio` or `find /usr/local/cuda*/gds/tools/gdsio`
  - `gdrcopy_copybw`: `which gdrcopy_copybw` or find in `/usr/local/gdrcopy*/`
  - `nvcc`: find under `/usr/local/cuda*`
  - `spdk_nvme_perf`: find under `deps/spdk-build/bin/`
  - `nvme-bar1-bench`: find under `target/release/`
- Compute theoretical per-link bandwidth:
  - Gen3: 8 GT/s × lanes × 128/130 encoding
  - Gen4: 16 GT/s × lanes × 128/130 encoding
  - Gen5: 32 GT/s × lanes × 128/130 encoding

## Command Style (Important for Permissions)

To avoid permission prompts on compound commands, use ONE simple command per
Bash tool call. Do NOT chain with `&&`, `|`, or `2>&1` redirects. The project's
permission allowlist matches against the full command string — compound commands
won't match patterns like `Bash(ls /dev/vfio/)`.

Good: separate tool calls for `ls /dev/vfio/` and `ls /sys/bus/pci/drivers/vfio-pci/`
Bad: `ls /dev/vfio/ 2>&1 && ls /sys/bus/pci/drivers/vfio-pci/ 2>&1 | head -20`

## CPU Feature Check (Step 2)

Run `tools/check-amd-proc-features.py` to characterize the CPU's SIMD capabilities
relevant to hashing and KV cache integrity:

```
python3 tools/check-amd-proc-features.py
```

Capture and include the full output in the report. Key fields to extract into the YAML profile:
- CPU vendor/brand/Zen generation (if AMD)
- XXH3 throughput tier (AVX-512 / AVX2 / SSE2 / Scalar)
- SIMD flags present: avx512f, avx512bw, avx2, sse4_2, pclmulqdq, aes
- Certus algorithm recommendation

If `py-cpuinfo` is missing, note it and install: `pip install py-cpuinfo`.

## NVMe Device Inspection (Step 3)

For each NVMe drive detected (drives must be bound to the **kernel NVMe driver** for this step,
not vfio-pci), run `tools/inspect-nvme.py`. This characterizes drive behavior critical to
benchmark tuning:

```
sudo python3 tools/inspect-nvme.py /dev/nvme<N>n1 --skip-gc --skip-power
```

Use `--skip-gc` and `--skip-power` to skip the long-running settle and power-state tests
(those take 10–30 minutes per drive). Run the full inspection only when you have time:

```
sudo python3 tools/inspect-nvme.py /dev/nvme<N>n1
```

Key fields to extract into the YAML profile per drive:
- `model`, `firmware_rev`, `serial` (from `identify`)
- `capacity_bytes` → convert to TB: `capacity_tb = capacity_bytes / 1e12`
- `mdts_bytes`, `block_size` (from `identify`)
- `vwc_enabled`: `bool(identify['vwc'] & 0x1)` (volatile write cache)
- `has_read_cache`, `cache_speedup` (from `read_cache`, if run)
- `sustained_write_mbps` (from `gc_settle.sustained_write_mbps`, if run)
- `recommended_gc_settle_s` (from `gc_settle.recommended_gc_settle_s`, if run)
- `power_state_transitions_at_s` (first element of `power_states.power_state_transitions_at_s`, if run; null if empty list)
- Read latency: `read_profile` entries — extract avg_us for qd=1, qd=16, qd=32

After running inspect-nvme.py, rebind drives to vfio-pci before SPDK benchmarks.

## Setup (Step 4)

- Kill any running `certus-server-yaml` (it holds VFIO groups)
- Wait for VFIO groups to release (`fuser /dev/vfio/*`)
- Bind all NVMe drives to vfio-pci: run the SPDK setup script
  - Find it: `deps/spdk/scripts/setup.sh` or `deps/spdk-build/../scripts/setup.sh`
  - If not found, try `HUGEMEM=4096 scripts/setup.sh` from SPDK source dir
- Verify all detected NVMe drives appear in `/sys/bus/pci/drivers/vfio-pci/`

## Path 1: NVMe Sequential Read (Step 5)

Tool: `spdk_nvme_perf`

Every NVMe command in the SPDK path is a DMA transfer — the NVMe controller DMAs data
directly into the destination buffer (host RAM or BAR1) over PCIe using PRPs. The block
size passed to `spdk_nvme_perf` controls how many NVMe commands are grouped into one
logical IO, but each individual NVMe command is still bounded by MDTS (typically 128 KiB).
The block size matrix below therefore spans the full range from native MDTS size up through
large logical groupings, giving both the per-command efficiency curve and the link
saturation behavior in one pass.

Matrix dimensions:
- **Drive counts**: 1, 2 (if ≥2 drives), 4 (if ≥4), 6 (if ≥6), all-detected
- **Block sizes**: 4 KiB, 16 KiB, 64 KiB, 128 KiB, 256 KiB, 512 KiB, 1 MiB, 2 MiB, 4 MiB, 8 MiB
  - 4–16 KiB: well below MDTS — CPU submission overhead and PCIe TLP inefficiency dominate;
    throughput will be low but shows the floor and confirms MDTS is not the only factor
  - 64–128 KiB: sub-MDTS and at-MDTS — isolates per-command PCIe efficiency; at QD=32
    only 2–4 MiB in flight so the link may not yet be saturated at these sizes
  - 256 KiB–1 MiB: MDTS-straddling zone where logical IOs split into 2–8 NVMe commands;
    throughput typically plateaus here as the link saturates
  - 2–8 MiB: large logical groupings; throughput should match 1 MiB if link-saturated.
    Confirms saturation and exercises the logical IO grouping path.
  Note: at small block sizes (4–128 KiB), QD=32 may not fully saturate the link — this
  is expected and informative. The goal is to see where the throughput knee occurs, not
  to reach absolute peak at every size. QD=32 is sufficient to observe the knee clearly.
- **Queue depths**: 16, 32
  QD=16 typically saturates the PCIe Gen4 x4 link at block sizes ≥256 KiB. Include
  QD=32 to confirm saturation (identical throughput = link-bound) and to catch drives
  where QD=16 is insufficient (smaller MDTS, higher per-IO latency, or BAR1 targets
  with posted-write ordering delays).
- **Duration**: 5 seconds per run
- **Workload**: sequential read (`-w read`)

For multi-drive tests, pass multiple `-r 'trtype:pcie traddr:0000:XX:00.0'` flags.
Group drives by root complex when possible (test same-root groups and cross-root groups separately).

Parse output: the "Total" line gives IOPS, MiB/s, and average/min/max latency.
Convert MiB/s to decimal GB/s using: `GB/s = MiB/s × 1.048576 / 1000`.
Use this formula consistently across all paths — the evaluator compares percentages
against these numbers, so approximate conversions cause drift.

Output: Two matrices (throughput GB/s, latency us) with rows = (drives, block_size) and
columns = QD. Note the **optimal read chunk size**: the smallest block size that achieves
≥95% of the peak throughput for that drive count. This is the recommended `--chunk-size`
for `nvme-bar1-bench` and the NVMe command size in the dispatcher cold path.

If QD=16 and QD=32 produce identical throughput at a given size, note that the drive is
link-saturated at that size — deeper queuing adds only latency.

## Path 2: NVMe Sequential Write (Step 6)

Tool: `spdk_nvme_perf`

Same block size matrix as Path 1 — identical sizes allow direct read/write comparison
and the same efficiency-curve analysis. Write throughput is the ceiling for the Certus
write-through path (background flusher). Write efficiency vs size may differ from reads
due to FTL write amplification, especially at sub-MDTS sizes (64 KiB) where partial NAND
page writes increase write amplification.

Matrix dimensions:
- **Drive counts**: 1, 2 (if ≥2 drives), 4 (if ≥4), all-detected
  (6-drive write is less critical — the write path is single-drive-per-extent)
- **Block sizes**: 4 KiB, 16 KiB, 64 KiB, 128 KiB, 256 KiB, 512 KiB, 1 MiB, 2 MiB, 4 MiB, 8 MiB
- **Queue depths**: 16, 32
- **Duration**: 5 seconds per run
- **Workload**: sequential write (`-w write`)

```
sudo deps/spdk-build/bin/spdk_nvme_perf \
    -r 'trtype:pcie traddr:0000:XX:00.0' \
    -q 16 -o 131072 -w write -t 5
```

Parse output identically to the read path. Convert MiB/s to decimal GB/s.

Output: Two matrices (throughput GB/s, latency us) with rows = (drives, block_size) and
columns = QD. Note the **optimal write chunk size**: smallest block size achieving ≥95%
of peak write throughput. Compare peak write GB/s against the `inspect-nvme.py` sustained
write figure to verify SPDK and kernel-mode numbers are consistent.

## Path 3: GPU PCIe Bandwidth — cudaMemcpy (Step 7)

Source: `tools/hw-ceiling/cuda_bw_test.cu`. Binary output: `/tmp/cuda_bw_test`.

Build step:
```
# Preferred — source already in repo:
make -C tools/hw-ceiling OUTDIR=/tmp cuda_bw_test

# If tools/hw-ceiling/ is absent: write the source to tools/hw-ceiling/cuda_bw_test.cu
# (creating the directory), then run make as above. Do NOT write to /tmp/ only —
# saving to tools/hw-ceiling/ means future runs skip the write step entirely.
```

**NUMA locality matters here.** H2D bandwidth depends on where the pinned host buffer
is allocated relative to the GPU's root complex. If the GPU's PCIe root is on NUMA node 1
but the calling thread (and therefore `cudaMallocHost`) is on NUMA node 0, the DMA engine
must read the source buffer across the Infinity Fabric inter-socket link — this can reduce
H2D throughput by 2–3+ GB/s compared to a NUMA-local allocation. Run the benchmark twice:

```
# NUMA-local: pin to the NUMA node that owns the GPU's root complex
# First determine which NUMA node each GPU's PCIe root is on (from lspci/numactl --hardware)
numactl --cpunodebind=<gpu_numa_node> --membind=<gpu_numa_node> /tmp/cuda_bw_test

# Cross-NUMA: force host buffer onto the opposite NUMA node
numactl --cpunodebind=<other_numa_node> --membind=<other_numa_node> /tmp/cuda_bw_test
```

The difference between these two runs is the Infinity Fabric H2D penalty. The NUMA-local
result is the true hardware ceiling; the cross-NUMA result is what Certus sees if CPU
affinity is not set correctly.

Program behaviour:
- `cudaMallocHost` + `cudaMemcpy` (pinned host memory)
- Measure H2D and D2H
- Transfer sizes: 128 KiB, 512 KiB, 1 MiB, 2 MiB, 4 MiB, 8 MiB, 16 MiB, 32 MiB, 64 MiB, 256 MiB
- 50 iterations, 5 warmup
- `cudaEvent` timing
- Runs on ALL GPUs in a single invocation (loops over `cudaGetDeviceCount`)
- Also measures H2D with 2, 4, and 8 concurrent `cudaMemcpyAsync` on separate streams
  (each stream copies a different pinned buffer → different GPU destination).
  This matters because single-stream H2D at 4 MiB may only reach ~10 GB/s on a x16 link
  that can do ~25+ GB/s with concurrency.

Output: Per-GPU table for each NUMA binding: Size | H2D 1-stream (GB/s) | H2D 4-stream (GB/s) | D2H (GB/s).
Note the per-GPU NUMA-local vs cross-NUMA delta — this is the cost of incorrect CPU affinity.

## Path 4: GPU D2D Bandwidth — cudaMemcpyDeviceToDevice (Step 8)

Source: `tools/hw-ceiling/cuda_d2d_test.cu`. Binary output: `/tmp/cuda_d2d_test`.

Build step:
```
# Preferred — source already in repo:
make -C tools/hw-ceiling OUTDIR=/tmp cuda_d2d_test

# If tools/hw-ceiling/ is absent: write the source to tools/hw-ceiling/cuda_d2d_test.cu
# (creating the directory if needed), then run make as above.
```

The P2P cold path uses a staging ring (GDRCopy BAR1-mapped GPU memory) as the NVMe DMA
target, then does a D2D copy from staging → client's final GPU destination. This D2D
copy is part of the critical path and its bandwidth is a ceiling on throughput.

Program behaviour:
- Source: `cudaMalloc` region A; Destination: `cudaMalloc` region B
- Transfer sizes: 128 KiB, 512 KiB, 1 MiB, 2 MiB, 4 MiB, 8 MiB, 16 MiB
- 100 iterations, 10 warmup
- `cudaEvent` timing
- Runs on ALL GPUs in a single invocation
- Also measures with 2 and 4 concurrent async D2D copies on separate streams

This tells us whether D2D is fast enough to not bottleneck the pipeline,
and whether multiple streams can overlap.

Output: Table: Size | 1-stream D2D (GB/s) | 2-stream (GB/s) | 4-stream (GB/s).

## Path 5: GDRCopy BAR1 Mapping Bandwidth (Step 9)

GDRCopy provides the BAR1 mapping that makes NVMe P2P work. It also exposes
CPU-accessible bandwidth to GPU memory via BAR1, relevant for:
- Metadata writes to GPU memory
- Verifying BAR1 mapping is functional

**Important context**: In the Certus P2P path, GDRCopy is used for MAPPING SETUP
(gdr_pin_buffer + gdr_map + spdk_mem_register), NOT for data transfer. The actual
data transfer is NVMe DMA through the BAR1 aperture. But `gdrcopy_copybw` still
tells us the BAR1 aperture bandwidth from the CPU side, which is a useful diagnostic.

If `gdrcopy_copybw` or `gdrcopy_copylat` is found:
```
gdrcopy_copybw
gdrcopy_copylat
```

If not installed, try to find and compile from source:
```
find / -path "*/gdrcopy*/tests" -type d 2>/dev/null
# or from the kernel/modules/gdrcopy tree in this repo
cd kernel/modules/gdrcopy && make PREFIX=/tmp/gdrcopy lib lib_install
cd tests && make
```

If GDRCopy is not available at all, note in report and provide install instructions.

Output: Table of sizes vs H2D/D2H bandwidth (GB/s).
Note: CPU→BAR1 writes are often several GB/s to ~20+ GB/s depending on platform,
NUMA placement, PCIe generation, and write-combining behavior.
CPU←BAR1 reads are typically 1-5 GB/s (uncacheable reads, severe amplification).

## Path 6: GPUDirect Storage — gdsio (Step 10)

If `lsmod | grep nvidia_fs` succeeds AND `gdsio` binary is found:

Unbind drives from vfio-pci and rebind to kernel NVMe driver first:
```
deps/spdk/scripts/setup.sh reset
```

Then run gdsio for each topology pairing:
- Same-root drives → same-root GPU
- Cross-root drives → cross-root GPU (to measure penalty)

Matrix:
- Drive counts: 1, 2, 4
- Block sizes: 4M, 8M, 16M
- GPU: each available GPU
- IO depth: 16, 32

```
gdsio -f /dev/nvmeXn1 -d <gpu-index> -w 4 -s <block-size> -x 0 -I 1 -T 10
```

After GDS tests, rebind drives back to vfio-pci for other tests.

If nvidia_fs is NOT loaded, note in report:
```
GDS not available.
nvidia_fs module status: [not installed | installed but fails to load | loaded]
If not working, check driver version compatibility:
  modinfo nvidia | grep version
  modinfo nvidia-fs | grep version
Install: sudo dnf install nvidia-gds nvidia-fs-dkms
```

Output: Table with (drives, block_size, GPU, topology) → bandwidth GB/s.

## Path 7: Host RAM Bandwidth — memcpy baseline (Step 11)

Source: `tools/hw-ceiling/memcpy_bench.c`. Binary output: `/tmp/memcpy_bench`.

Build step:
```
# Preferred — source already in repo:
make -C tools/hw-ceiling OUTDIR=/tmp memcpy_bench

# If tools/hw-ceiling/ is absent: write the source to tools/hw-ceiling/memcpy_bench.c
# (creating the directory if needed), then run make as above.
```

Program behaviour:
- Same-NUMA memcpy (both allocs on node 0, via `numa_alloc_onnode`)
- Cross-NUMA memcpy (src on node 0, dst on node 1) — if ≥2 NUMA nodes
- Sizes: 4 MiB, 16 MiB, 64 MiB, 256 MiB
- 200 iters for ≤16 MiB, 50 iters for ≥64 MiB

This establishes the memory-tier ceiling when data is in host RAM (before GPU transfer).

Output: Table: Size | Same-NUMA (GB/s) | Cross-NUMA (GB/s).

## Path 8: Topology-Aware P2P Matrix (Step 12)

For each (drive-group, GPU) pairing, summarize the expected path:
- Same root complex: direct PCIe path
- Cross root complex: traverses CPU/Infinity Fabric
- Cross NUMA: traverses inter-socket link

Create a topology matrix showing the routing for every possible pairing.

## Path 9: NVMe DMA → BAR1 Microbenchmark (Step 13)

Tool: `nvme-bar1-bench` (`apps/nvme-bar1-bench/`)

This is the most important measurement — it gives the closest isolated P2P cold-path
hardware ceiling. Note: it still includes SPDK FFI, qpair behavior, poller
implementation, GDRCopy mapping, and VFIO/IOMMU effects — it is the practical
ceiling for Certus, not a pure PCIe-theoretical ceiling. It bypasses the actor/channel model and calls SPDK FFI directly. Each drive
gets a dedicated CPU-pinned poller thread with its own qpair. Runs two modes
back-to-back: host-ram (baseline) and bar1 (GDRCopy-mapped GPU memory).

Requires: `gdrdrv` kernel module loaded. Depending on the driver stack,
`nvidia_peermem` may also be required; detect and report whether it is loaded.
If `gdrdrv` is absent, skip this path and note in the report.

```
cargo build --release -p nvme-bar1-bench
```

**Critical: use a large total-bytes (≥2 GiB) to read past the drive's DRAM cache.**
Small streams (16–64 MiB) will report inflated numbers from cache hits.

**Critical: report exactly which drive BDFs were selected for each run.**
Do not interpret topology results unless the selected drives are shown. The
`--drive-count N` flag uses the first N discovered drives, which may not correspond
to the drives same-root with the target GPU.

**NUMA and topology pinning are critical for correct ceiling measurements.**
`nvme-bar1-bench` spawns one poller thread per drive. Those threads issue NVMe commands
and wait for completions — their NUMA locality determines where the host-RAM DMA target
buffer is allocated and which memory controller handles the PCIe read/write traffic.

- **NUMA-local run**: pin poller threads to the NUMA node that owns the target GPU's PCIe
  root complex, AND select drives from that same root complex. This gives the true hardware
  ceiling with no cross-fabric penalty.
- **Cross-NUMA run**: pin to the opposite NUMA node. Quantifies the Infinity Fabric penalty
  that Certus incurs when CPU affinity is not set. Required to understand observed production
  performance, not just the theoretical ceiling.

Use `sudo numactl --cpunodebind=N --membind=N` to wrap the benchmark. Determine the correct
NUMA node for each GPU from `numactl --hardware` and the GPU's PCI BDF (cross-reference
with `lspci -tv`). Verify that `--drive-count N` picks drives from the right root complex
by checking the BDFs printed in the benchmark output — the tool sorts drives by PCI address
and takes the first N, which may not be the same-root drives for the target GPU.

Run matrix:
```
# --- NUMA-local runs (true ceiling) ---
# Substitute <gpu0_numa> with the NUMA node of GPU 0's PCIe root complex.
# Verify BDFs in output confirm drives are same-root with GPU 0.

# 1 drive, NUMA-local, GPU 0
sudo numactl --cpunodebind=<gpu0_numa> --membind=<gpu0_numa> \
    target/release/nvme-bar1-bench --drive-count 1 --gpu 0 \
    --chunk-size 131072 --total-bytes 2147483648 --queue-depth 16 --iterations 3

# 4 drives, NUMA-local, GPU 0
sudo numactl --cpunodebind=<gpu0_numa> --membind=<gpu0_numa> \
    target/release/nvme-bar1-bench --drive-count 4 --gpu 0 \
    --chunk-size 131072 --total-bytes 2147483648 --queue-depth 32 --iterations 3

# 6 drives, NUMA-local, GPU 0
sudo numactl --cpunodebind=<gpu0_numa> --membind=<gpu0_numa> \
    target/release/nvme-bar1-bench --drive-count 6 --gpu 0 \
    --chunk-size 131072 --total-bytes 2147483648 --queue-depth 32 --iterations 3

# 4 drives, NUMA-local, GPU 1 (topology-best pairing for GPU 1)
sudo numactl --cpunodebind=<gpu1_numa> --membind=<gpu1_numa> \
    target/release/nvme-bar1-bench --drive-count 4 --gpu 1 \
    --chunk-size 131072 --total-bytes 2147483648 --queue-depth 32 --iterations 3

# --- Cross-NUMA run (quantify Infinity Fabric penalty) ---
# Pin to the NUMA node opposite to GPU 0's root complex.
# Same drive count and GPU as the NUMA-local 4-drive run for a direct apples-to-apples comparison.

# 4 drives, cross-NUMA, GPU 0
sudo numactl --cpunodebind=<other_numa> --membind=<other_numa> \
    target/release/nvme-bar1-bench --drive-count 4 --gpu 0 \
    --chunk-size 131072 --total-bytes 2147483648 --queue-depth 32 --iterations 3
```

CLI reference:
- `--drive-count N`: use first N discovered drives (sorted by PCI address)
- `--gpu INDEX`: CUDA device index for BAR1 target [default: 0]
- `--chunk-size BYTES`: NVMe IO size, must be ≤ drive MDTS (typically 128 KiB) [default: 131072]
- `--total-bytes BYTES`: total bytes per drive per iteration [default: 16 MiB — TOO SMALL, use 2G]
- `--queue-depth N`: in-flight commands per drive [default: 16]
- `--warmup N`: warmup iterations [default: 3]
- `--iterations N`: measured iterations [default: 20]

Sanity check: if 1-drive host-RAM result is >20% below the SPDK perf single-drive
number, the microbenchmark itself may be adding overhead (e.g. missing doorbell
batching). Note this in the report — the host-ram vs bar1 comparison remains valid
but the absolute numbers may understate the hardware ceiling.

Observed on current node (Intel Sentinel Rock, Gen4 x4, NVIDIA A30):
- 1 drive: host-ram ≈ bar1 ≈ 4.3 GB/s (0% BAR1 overhead)
- 4 drives: host-ram ≈ 24 GB/s, bar1 ≈ 20 GB/s (~17% BAR1 overhead)
- 6 drives: host-ram ≈ 35 GB/s, bar1 ≈ 21.5 GB/s (~39% overhead, GPU BAR1 saturates)

These are node-specific and should not be treated as universal expected values.

## Report Generation (Step 14)

Produce TWO outputs:

### 1. Markdown report: `<output-dir>/hardware-ceiling-<YYYY-MM-DD>.md`

Write the report with:
1. Platform section (all detected hardware, topology diagram)
2. CPU feature report (full output of `check-amd-proc-features.py`, formatted as a code block)
3. NVMe device inspection summary (from `inspect-nvme.py` per drive — key fields, not full output)
4. PCIe theoretical bandwidth table
5. Per-path matrices (Paths 1–8, each gets its own section; read and write matrices include the IO size knee annotation)
6. Topology routing matrix (Path 9 — derived, no additional benchmarks)
7. Summary table (see below)
8. Observations and recommendations

The summary must contain **four sub-tables**:

**Sub-table 1 — Raw hardware paths** (measured primitives, no dispatcher logic):
```
| Data Path                              | Peak BW (GB/s) | Limiting Factor              | Notes              |
|----------------------------------------|----------------|------------------------------|--------------------|
| NVMe → Host read (1 drive)             |                | Drive PCIe x4                |                    |
| NVMe → Host read (4 drives)            |                | 4× PCIe x4 aggregate         |                    |
| NVMe → Host read (6/7 drives)          |                | N× PCIe x4 aggregate         |                    |
| NVMe → Host write (1 drive)            |                | Drive PCIe x4 / FTL          |                    |
| NVMe → Host write (4 drives)           |                | 4× PCIe x4 aggregate / FTL   |                    |
| Optimal read chunk size                |                | (bytes — knee of curve)      |                    |
| Optimal write chunk size               |                | (bytes — knee of curve)      |                    |
| Host → GPU 0 H2D (NUMA-local, peak)    |                | GPU PCIe x16                 |                    |
| Host → GPU 0 H2D (cross-NUMA, peak)    |                | Infinity Fabric              | penalty vs local   |
| Host → GPU 1 H2D (NUMA-local, peak)    |                | GPU PCIe x16                 |                    |
| Host → GPU 1 H2D (cross-NUMA, peak)    |                | Infinity Fabric              | penalty vs local   |
| GPU N → Host (D2H)                     |                | PCIe read amplification      |                    |
| GPU D2D (1-stream sustained)           |                | HBM internal bus             |                    |
| GDRCopy CPU→BAR1 write                 |                | BAR1 write-combining         |                    |
| GDRCopy CPU←BAR1 read                  |                | BAR1 uncacheable reads       |                    |
| Host RAM same-NUMA (sustained)         |                | Memory controller            |                    |
| Host RAM cross-NUMA (sustained)        |                | Inter-socket link            |                    |
| GDS NVMe → GPU                         | N/A or XX.XX   | nvidia_fs / true P2P DMA     |                    |
```

**Sub-table 2 — `dispatcher` warm path** (both `dispatcher` and `dispatcher-p2p` share this):
```
Route: Memory-Tier (CUDA-pinned DRAM) ──H2D DMA──▶ GPU
Both components use memcpy_h2d_async from a DRAM memory-tier slot for warm hits.
Ceiling = H2D PCIe bandwidth (NVMe not involved).

| GPU | Ceiling (GB/s) | Bound by        |
|-----|----------------|-----------------|
| 0   |                | H2D PCIe x16    |
| 1   |                | H2D PCIe x16    |
```

**Sub-table 3 — `dispatcher` cold path** (NVMe → DRAM bounce → H2D):
```
Route: NVMe ──DMA──▶ Memory-Tier (DRAM) ──H2D DMA──▶ GPU
Two-stage pipeline. Ceiling = min(NVMe_aggregate, H2D). Crossover point where H2D
becomes the cap = H2D_ceiling / per_drive_bandwidth drives.

| Drives | GPU | Ceiling (GB/s) | Bound by                          |
|--------|-----|----------------|-----------------------------------|
| 1      | N   |                | NVMe x4                           |
| 4      | N   |                | NVMe aggregate (if < H2D ceiling) |
| 6      | N   |                | H2D PCIe x16 or NVMe aggregate    |
```

**Sub-table 4 — `dispatcher-p2p` cold path** (NVMe → BAR1 direct):
```
Route: NVMe ──DMA──▶ BAR1 (GDRCopy-mapped GPU memory)
Single-stage. Ceiling = nvme-bar1-bench BAR1 result (includes PCIe + BAR1 overhead).
BAR1 saturates around 21–22 GB/s on A30; adding drives beyond that point yields no gain.

| Drives | GPU | BAR1 ceiling (GB/s) | BAR1 overhead vs host-ram | Notes                    |
|--------|-----|---------------------|--------------------------|--------------------------|
| 1      | 0   |                     | ~0%                      | NUMA-local               |
| 4      | 0   |                     | measured %               | NUMA-local               |
| 4      | 0   |                     | measured %               | cross-NUMA (penalty run) |
| 4      | 1   |                     | measured %               | NUMA-local, topology-best|
| 6      | 0   |                     | measured %               | NUMA-local, saturated?   |
```

After the four sub-tables, add a **crossover comparison**:
```
| Drive count | dispatcher cold ceiling | dispatcher-p2p cold ceiling | Winner        |
|-------------|------------------------|-----------------------------|---------------|
| 1           |                        |                             |               |
| 4           |                        |                             | ~tie or one   |
| 6           |                        |                             | dispatcher or p2p |
```
This exposes the key insight: at low drive counts dispatcher-p2p may win on latency
(single-stage, no DRAM bounce) but at high drive counts dispatcher wins on throughput
(H2D cap > BAR1 saturation ceiling).

### 2. Machine-readable profile: `<output-dir>/hardware_profile_<YYYY-MM-DD>.yaml`

The filename includes the date so multiple profiles from different runs are preserved
side-by-side for comparison. Use only measured values — omit any path that was
skipped due to missing tools (do not fill with estimates or zeros).

```yaml
# Auto-generated by profile-hardware-ceiling skill
# Date: YYYY-MM-DD
# Node: <hostname>

platform:
  hostname: <hostname>
  cpu: <model>
  numa_nodes: <N>
  kernel: <version>
  os: <distro version>

cpu_features:
  vendor: <AuthenticAMD | GenuineIntel | ...>
  zen_generation: <1-5 or null>
  zen_label: <"Zen 4" or "N/A (non-AMD)">
  has_avx512: <true/false>
  has_avx2: <true/false>
  has_sse4_2: <true/false>
  has_pclmulqdq: <true/false>
  has_aes: <true/false>
  xxh3_tier: <"AVX-512" | "AVX2" | "SSE2" | "Scalar">
  xxh3_throughput_estimate: <"~40-50 GB/s" or similar string>
  certus_recommended_hash: <"XXH3_128bits (AVX-512 path)" or similar>

gpus:
  gpu0:
    model: <name>
    pcie_gen: 4
    pcie_width: 16
    bar1_gib: 32
    pci_bdf: "a1:00.0"
    numa_node: <int>                        # NUMA node of GPU's PCIe root complex
    # NUMA-local: cudaMallocHost on same NUMA node as GPU's root complex
    h2d_4m_1stream_numa_local_gbps: <measured>
    h2d_peak_numa_local_gbps: <measured at best transfer size>
    d2h_peak_numa_local_gbps: <measured>
    # Cross-NUMA: host buffer on opposite NUMA node
    h2d_4m_1stream_cross_numa_gbps: <measured>
    h2d_peak_cross_numa_gbps: <measured>
    cross_numa_h2d_penalty_gbps: <computed: local - cross>
    d2d_1stream_gbps: <measured>
    d2d_4stream_gbps: <measured>
  gpu1:
    # same structure

nvme:
  drives:
    - bdf: "61:00.0"
      model: <name>
      firmware_rev: <string>
      serial: <string>
      capacity_tb: <float>          # capacity_bytes / 1e12
      mdts_bytes: 131072
      pcie_gen: 4
      pcie_width: 4
      numa_node: <int>              # from sysfs numa_node attribute
      vwc_enabled: <true/false>     # bool(vwc & 0x1)
      has_read_cache: <true/false>
      # from inspect-nvme.py gc_settle (if run):
      sustained_write_mbps: <measured or null>
      recommended_gc_settle_s: <int or null>
      # from inspect-nvme.py power_states (if run):
      power_state_transition_at_s: <int or null>
      # from inspect-nvme.py read_profile (if run):
      read_latency_qd1_us: <float or null>
      read_latency_qd16_us: <float or null>
      read_latency_qd32_us: <float or null>
    - bdf: "62:00.0"
      # ...
  mdts_bytes: 131072         # representative MDTS (use smallest across all drives)
  raw_read_gbps:
    1_drive: <measured>
    4_drive: <measured>
    6_drive: <measured>
  raw_write_gbps:
    1_drive: <measured>
    4_drive: <measured>
  # IO size sweep: 1 drive, QD=32. Read and write use the same sizes.
  # Derived from Path 1 (read) and Path 2 (write) 1-drive QD=32 rows.
  io_size_sweep_read_gbps:
    4kib: <measured>
    16kib: <measured>
    64kib: <measured>
    128kib: <measured>
    256kib: <measured>
    512kib: <measured>
    1mib: <measured>
    2mib: <measured>
    4mib: <measured>
    8mib: <measured>
    optimal_bytes: <int — smallest size achieving ≥95% of peak>
  io_size_sweep_write_gbps:      # 1 drive, QD=32
    4kib: <measured>
    16kib: <measured>
    64kib: <measured>
    128kib: <measured>
    256kib: <measured>
    512kib: <measured>
    1mib: <measured>
    2mib: <measured>
    4mib: <measured>
    8mib: <measured>
    optimal_bytes: <int>

bar1:
  # nvme-bar1-bench results (per GPU target)
  # Each entry has numa_local (cpunodebind = GPU's NUMA node) and cross_numa variants.
  # The numa_local result is the true hardware ceiling.
  # The cross_numa result quantifies the Infinity Fabric penalty.
  gpu0:
    numa_local:
      host_ram_1drive_gbps: <measured>
      host_ram_4drive_gbps: <measured>
      host_ram_6drive_gbps: <measured>
      bar1_1drive_gbps: <measured>
      bar1_4drive_gbps: <measured>
      bar1_6drive_gbps: <measured>
      overhead_4drive_pct: <computed>
      overhead_6drive_pct: <computed>
    cross_numa:
      host_ram_4drive_gbps: <measured>
      bar1_4drive_gbps: <measured>
      penalty_vs_local_pct: <computed>
  gpu1:
    numa_local:
      host_ram_1drive_gbps: <measured>
      host_ram_4drive_gbps: <measured>
      bar1_1drive_gbps: <measured>
      bar1_4drive_gbps: <measured>
      overhead_4drive_pct: <computed>

gdrcopy:
  cpu_to_bar1_gbps: <measured or null>
  bar1_to_cpu_gbps: <measured or null>

gds:
  available: <true/false>
  # if available:
  1drive_gbps: <measured>
  4drive_gbps: <measured>

host_ram:
  same_numa_gbps: <measured>
  cross_numa_gbps: <measured or null>

topology:
  # Which drives share a root complex with which GPU
  gpu0_same_root_drives: ["c1:00.0", "c2:00.0"]
  gpu1_same_root_drives: ["61:00.0", "62:00.0", "63:00.0", "64:00.0"]

# Derived ceilings — keyed by Certus dispatcher path, for investigator/evaluator
#
# Certus has two dispatchers, each with a warm and cold path:
#
#   dispatcher (memory-tier DRAM bounce):
#     warm:  Memory-Tier (DRAM) ──H2D──▶ GPU           ceiling = H2D bandwidth
#     cold:  NVMe ──DMA──▶ Memory-Tier ──H2D──▶ GPU    ceiling = min(NVMe_agg, H2D)
#
#   dispatcher-p2p (direct BAR1, no DRAM):
#     warm:  Memory-Tier (DRAM) ──H2D──▶ GPU           ceiling = H2D bandwidth (same as above)
#     cold:  NVMe ──DMA──▶ BAR1 (GPU)                  ceiling = bar1 result from nvme-bar1-bench
#
ceilings:
  # All ceiling values use NUMA-local measurements (true hardware ceiling).
  # Cross-NUMA penalty fields show the cost of incorrect CPU affinity in production.

  # --- warm path (shared by both dispatchers) ---
  # Use NUMA-local H2D — this is the ceiling Certus achieves with correct affinity.
  warm_gpu0_gbps: <gpus.gpu0.h2d_4m_1stream_numa_local_gbps>
  warm_gpu0_peak_gbps: <gpus.gpu0.h2d_peak_numa_local_gbps>
  warm_gpu1_gbps: <gpus.gpu1.h2d_4m_1stream_numa_local_gbps>
  warm_gpu1_peak_gbps: <gpus.gpu1.h2d_peak_numa_local_gbps>
  # Penalty if affinity is wrong:
  warm_gpu0_cross_numa_penalty_gbps: <gpus.gpu0.cross_numa_h2d_penalty_gbps>
  warm_gpu1_cross_numa_penalty_gbps: <gpus.gpu1.cross_numa_h2d_penalty_gbps>

  # --- dispatcher cold path: NVMe → DRAM → H2D ---
  dispatcher_cold_1drive_gbps: <min(nvme.raw_read_gbps.1_drive, warm_gpuX_peak_gbps)>
  dispatcher_cold_4drive_gbps: <min(nvme.raw_read_gbps.4_drive, warm_gpuX_peak_gbps)>
  dispatcher_cold_6drive_gbps: <min(nvme.raw_read_gbps.6_drive, warm_gpuX_peak_gbps)>
  dispatcher_cold_bottleneck_at_4drive: <"nvme" or "h2d">
  dispatcher_cold_bottleneck_at_6drive: <"nvme" or "h2d">
  dispatcher_cold_crossover_drives: <computed: h2d_peak_gbps / per_drive_gbps>

  # --- dispatcher-p2p cold path: NVMe → BAR1 (NUMA-local) ---
  p2p_cold_1drive_gbps: <bar1.gpuX.numa_local.bar1_1drive_gbps>
  p2p_cold_4drive_gpu0_gbps: <bar1.gpu0.numa_local.bar1_4drive_gbps>
  p2p_cold_4drive_gpu1_gbps: <bar1.gpu1.numa_local.bar1_4drive_gbps>
  p2p_cold_6drive_gbps: <bar1.gpuX.numa_local.bar1_6drive_gbps>
  p2p_cold_bar1_saturated: <true if adding drives past N yields <5% gain>
  # Cross-NUMA penalty:
  p2p_cold_4drive_gpu0_cross_numa_gbps: <bar1.gpu0.cross_numa.bar1_4drive_gbps>
  p2p_cold_cross_numa_penalty_pct: <bar1.gpu0.cross_numa.penalty_vs_local_pct>

  # --- NVMe raw (no GPU overhead, reference) ---
  nvme_raw_1drive_read_gbps: <nvme.raw_read_gbps.1_drive>
  nvme_raw_4drive_read_gbps: <nvme.raw_read_gbps.4_drive>
  nvme_raw_6drive_read_gbps: <nvme.raw_read_gbps.6_drive>
  nvme_raw_1drive_write_gbps: <nvme.raw_write_gbps.1_drive>
  nvme_raw_4drive_write_gbps: <nvme.raw_write_gbps.4_drive>

  # --- DMA chunk size recommendation ---
  nvme_optimal_read_chunk_bytes: <nvme.io_size_sweep_read_gbps.optimal_bytes>
  nvme_optimal_write_chunk_bytes: <nvme.io_size_sweep_write_gbps.optimal_bytes>

  # --- D2D (GPU internal; not a bottleneck for either dispatcher) ---
  gpu_d2d_sustained_gbps: <gpus.gpuX.d2d_1stream_gbps at 8 MiB>

  # --- Host RAM ---
  host_ram_same_numa_gbps: <host_ram.same_numa_gbps>
  host_ram_cross_numa_gbps: <host_ram.cross_numa_gbps>
```

The `ceilings` section is consumed by:
- **Rule-based investigator**: `efficiency = certus_measured / ceiling[relevant_path]`
- **Evaluation function**: pick the ceiling matching the active dispatch mode and drive count

Only populate entries where measurements succeeded. Use topology-correct GPU/drive pairings
(same-NUMA where available). Omit rather than estimate for skipped paths.

## Notes for Portability

- Do NOT hardcode PCI addresses — detect them from `lspci`
- Do NOT hardcode drive counts — use what's available
- Do NOT assume specific GPU models — query capabilities
- If a tool is missing (nvcc, gdsio, gdrcopy_copybw, spdk_nvme_perf, nvme-bar1-bench),
  skip that path and note in the report with install/build instructions
- Handle single-GPU and multi-GPU systems
- Handle single-NUMA and multi-NUMA systems
- **CUDA/C benchmark sources live in `tools/hw-ceiling/`** (`cuda_bw_test.cu`,
  `cuda_d2d_test.cu`, `memcpy_bench.c`, `Makefile`). Always use these.
  Build with `make -C tools/hw-ceiling OUTDIR=/tmp <target>` — binaries go to `/tmp/`.
  Only write sources to `/tmp/` if the repo checkout is somehow read-only (rare).
- The YAML profile must be valid YAML parseable by any standard library
- `inspect-nvme.py` requires drives bound to the **kernel NVMe driver** (not vfio-pci).
  Run it before the SPDK setup step, or after GDS tests when drives are already rebound.
- `check-amd-proc-features.py` requires `py-cpuinfo` (`pip install py-cpuinfo`).
  It is read-only and can run at any point without affecting drive binding state.

### Permissions setup for new users

The repo's `.claude/settings.json` pre-allows read-only detection commands (lscpu,
lspci, nvidia-smi, cargo, etc.). The sudo/hardware commands needed for actual
benchmarking require a per-user `.claude/settings.local.json` (gitignored).

To run this skill without permission prompts, create `.claude/settings.local.json`:
```json
{
  "permissions": {
    "allow": [
      "Bash(sudo lspci*)",
      "Bash(sudo modprobe *)",
      "Bash(sudo pkill*certus*)",
      "Bash(sudo kill*)",
      "Bash(sudo chmod * /dev/vfio/*)",
      "Bash(sudo fuser /dev/vfio/*)",
      "Bash(sudo */deps/spdk*/scripts/setup.sh*)",
      "Bash(sudo */deps/spdk-build/bin/spdk_nvme_perf*)",
      "Bash(sudo */target/release/nvme-bar1-bench*)",
      "Bash(sudo numactl*)",
      "Bash(sudo */target/release/certus-server-yaml*)",
      "Bash(sudo python3 tools/inspect-nvme.py*)",
      "Bash(python3 tools/check-amd-proc-features.py*)",
      "Bash(make -C tools/hw-ceiling*)",
      "Bash(/usr/local/cuda*/bin/nvcc*)",
      "Bash(CUDA_VISIBLE_DEVICES=* /tmp/*)",
      "Bash(/tmp/*)",
      "Bash(find / -name *gdrcopy*)",
      "Bash(find / -name *gdsio*)",
      "Bash(ls /sys/bus/pci/drivers/vfio-pci/)",
      "Bash(ls /dev/vfio/)",
      "Write(*/profiling/*)",
      "Write(/tmp/*)"
    ]
  }
}
```

Or let Claude prompt you on first run and approve each category once.

## Cleanup (Step 15)

Leave drives in whatever state the last test needed (vfio-pci if GDS was not run,
kernel driver if GDS was run last). Do NOT restart certus-server — leave the system
ready for the user to run further tests. Report which driver the drives are currently bound to.
