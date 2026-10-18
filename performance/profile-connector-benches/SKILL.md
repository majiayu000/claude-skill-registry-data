---
name: profile-connector-benches
description: Run certus-connector-bench and cputier-connector-bench with identical workload parameters, then write an HTML report comparing the two KV-offload backends side by side (throughput, IOPS, per-phase latency, parameter parity).
argument-hint: "<output-html-path>"
---

# profile-connector-benches

Benchmark the two KV-offload connector backends with the same workload and present
them side by side:

| Arm | Bench | Backend |
|---|---|---|
| certus | `tools/certus-connector-bench/bench_connector_lifecycle.py` (host) | `certus-server` over `/dev/shm/certus-shmq`, SPDK NVMe |
| cputier | `tools/cputier-connector-bench/run-in-container.sh` (vLLM ≥ 0.30 image) | vLLM `TieringOffloadingSpec`: pinned CPU tier + `fs` disk tier |

All work is done by `run_compare.sh` in this skill's directory. It takes every
workload flag **once** and forwards the same list to both benches, so the arms
cannot drift. The DRAM tier size `--dram` becomes certus-server's
`--memory-tier-size` and cputier's `--cpu-bytes` (and the container's
`CPU_BYTES`). `make_report.py` then checks parity from the columns each bench
actually wrote to its CSV and flags any difference in red.

## Argument

- `<output-html-path>` (required): where to write the HTML report, e.g.
  `bench-results/connector-compare.html`. If it is missing, ask for it. Raw
  artifacts (params.json, both CSVs, both bench logs, server.log) go to the
  sibling directory `<path-without-.html>.d/`.

The fs-tier path, the certus SSD count and the memory tier size are asked for
interactively (step 3). Everything else has working defaults. Pass through any extra flags the user
gives (see `run_compare.sh --help`): `--mode` (default `all`), `--bs`,
`--num-blocks`, `--block-bytes`, `--min-duration`, `--warmup`, `--working-set`,
`--pipeline-depth`, `--direction`, `--hit-ratio`, `--requests-per-step`,
`--num-sessions`, `--lookup-order`, `--gpu`, `--tp`, `--dram`; certus-only
`--device-pci`/`--drive-count`, `--eviction-threshold`, `--workers`,
`--channels`; cputier-only `--fs-tier`, `--image`.

## Steps for Claude

1. **Resolve the output path** from the argument. Make it absolute relative to the
   repo root if it is relative.

2. **Gather facts** to offer as answer options in step 3:
   - GPU: `nvidia-smi --query-gpu=index,name,memory.used --format=csv` and its
     NUMA node (`nvidia-smi topo -m`).
   - NVMe SSDs for certus: `lspci -Dnd ::0108`, with each device's NUMA node
     (`/sys/bus/pci/devices/<addr>/numa_node`) and driver (`basename $(readlink
     /sys/bus/pci/devices/<addr>/driver)`; SPDK needs `vfio-pci` or `uio_pci_generic`).
   - Hugepages: `grep -i huge /proc/meminfo` (free hugepage bytes cap the
     certus memory tier).
   - Free host RAM: `free -g` (caps the cputier CPU tier, which lives in the
     container's `/dev/shm`).
   - Candidate cputier fs-tier filesystems: `df -hT` mounts that are local
     block devices (xfs/ext4), and for each the backing device type
     (`lsblk -s -o NAME,TYPE,TRAN,MODEL <source>`) so the user can see which are NVMe.

3. **Ask the user** with one AskUserQuestion call holding these three questions
   (skip any the invocation already answered via `--fs-tier`, `--device-pci` /
   `--drive-count`, or `--dram`):
   - **cputier fs-tier path** — options: the default `~/cputier-bench-fs-tier`
     (state its filesystem and backing device, e.g. "xfs on SAS SSD LVM"), plus
     up to two other candidate mounts from step 2, preferring NVMe-backed ones
     (a directory `<mount>/cputier-bench-fs-tier`). Note that an NVMe-backed fs
     tier gives the fairest cold-path comparison with certus, and that it must
     not be overlay storage (no `O_DIRECT`). "Other" lets the user type a path.
   - **Number of certus SSDs** — options `1`, `2`, ... up to the number of
     SPDK-bound NVMe devices found (max 4 options; recommend all devices on the
     GPU's NUMA node, or 1 if none are). Then pick that many devices, GPU-NUMA
     node first, and pass each as `--device-pci`. Warn if any chosen SSD is on
     a different NUMA node from the GPU.
   - **Memory tier size** (applies to both arms: certus `--memory-tier-size`
     and cputier `--cpu-bytes`) — options `4G` (recommended, the default),
     `8G`, `16G`, filtered to sizes that fit both the free hugepages and free
     RAM (less ~4G headroom for the container's `/dev/shm`). Remind the user
     that `--working-set` (default 512 × 2 MiB = 1 GiB) must exceed it for the
     mixed-eviction phase to apply pressure, and offer to scale `--working-set`
     with it (e.g. 2 × tier ÷ `--block-bytes`), passed to both arms.
     **Cap it by GPU memory:** the certus bench allocates two GPU buffers of
     `max(num_blocks, working_set) × block_bytes` each at startup, so
     `2 × working_set × block_bytes` must fit in the GPU's free memory with
     ~1 GiB to spare, or the certus arm dies with CUDA OOM before writing any
     results (8192 × 2 MiB blocks needs 32 GiB; an A30 has 24). If no working
     set both fits the GPU and exceeds the tier, say so and only offer tier
     sizes that leave room for one.

   If the chosen fs-tier directory does not exist, create it (`mkdir -p`).

4. **Preflight** and tell the user what will run, with the answers from step 3:
   - GPU free (no memory in use).
   - certus arm: `target/release/certus-server` exists and is newer than the
     last commit touching `apps/certus-server`, `components` or `lib` (otherwise
     rebuild: `cargo build -p certus-server --release`); it runs as the current
     user, no sudo. Make sure no other `certus-server` is running (it would own
     `/dev/shm/certus-shmq`).
   - cputier arm: `podman image exists docker.io/vllm/vllm-openai:v0.30.0`
     (or `--image`).
   - If a prerequisite for one arm is missing, offer `--skip-certus` or
     `--skip-cputier` instead of aborting; the report then shows that arm as
     having no results.

5. **Launch** in the background (a `--mode all` run is several minutes per arm;
   the arms run one after the other because they share the GPU):
   ```bash
   .claude/skills/profile-connector-benches/run_compare.sh --out <output-html-path> \
       --fs-tier <answer> --device-pci <addr> [--device-pci <addr> ...] \
       --dram <answer> [--working-set N] [flags]
   ```
   Wait for it to finish. The script stops certus-server (SIGTERM, then SIGKILL
   after 8 s) on exit, including on failure.

6. **Report.** Give the user the HTML path and a short summary taken from the
   CSVs in `<path>.d/`: which backend wins each result row and by how much,
   and anything notable in the per-phase latency (for example cputier's
   `lookup_wait` on the cold path, or cputier store drops in its log). If
   `make_report.py` printed a parameter mismatch warning, or an arm failed,
   say so first and point at the log under `<path>.d/`. To re-render the HTML
   from existing artifacts, run `run_compare.sh --out <path> --report-only`
   with the same flags.

## What is and is not held equal

- Equal (forwarded identically): mode, `bs`, `num_blocks`, `block_bytes`,
  `min_duration`, `warmup`, `working_set`, `pipeline_depth`, `direction`,
  `hit_ratio`, `requests_per_step`, `num_sessions`, `lookup_order`, `tp`, GPU(s),
  DRAM tier size.
- Inherently different: the disk tier (SPDK raw NVMe vs fs files), and options
  only one bench has: certus `--workers`, `--channels`, eviction threshold,
  `--prefix-sharing` (left at its default, `shared`, which is how cputier
  behaves); cputier `--layers`, `--blocks-per-chunk`, fs thread counts (left at
  their defaults). The report lists these under "Backend-specific settings".
- Read cputier store throughput with care: it excludes the per-pass fs
  write-through drain (see `tools/cputier-connector-bench/README.md`).
