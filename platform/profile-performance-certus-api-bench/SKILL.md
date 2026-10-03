---
name: profile-performance-certus-api-bench
description: Measure system performance of this platform using
argument-hint: "[output-dir]"
---

The purpose of this skill is to capture a snapshot of performance by running certus-server (release build) and certus-api-bench.py.

Create the output directory from the output-dir argument, for example:
  mkdir -p <output-dir>
Write PROFILE.md to <output-dir>/PROFILE.md.

Collect data for combinations of the following parameters:
1. SSD device count D (1..N), where N is the number of detected SSD PCI devices.
   Detect available SSDs via `lspci -d <vendor>:<device>` or equivalent, sort PCI addresses lexicographically,
   and use the first D addresses.
   Pass each selected device as repeated flags:
     --device-pci <PCI1> --device-pci <PCI2> ... --device-pci <PCID>
   If D > N, skip that combination and record `SKIPPED: requested D > available N` in PROFILE.md.
2. Memory tier size: 4GB, 8GB, 16GB with `--memory-tier-size <bytes>` (use bytes, e.g. 4294967296).
3. Number of clients: 1, 2, 4, 8, 16 with `certus-api-bench --clients <count>`.
4. Cache block size: 1MB, 2MB, 4MB, 5MB with `certus-api-bench --block-size <bytes>` (use bytes, e.g. 1048576).
5. Batch size: 8, 16, 32, 64 with `certus-api-bench --batch-size <count>`.
6. Objects per lookup batch: 16, 32 with `certus-api-bench --num-objects <count>`.
7. Iterations: 10, 20, 50 with `certus-api-bench --iterations <count>`.

Other requirements:
- Run certus-server with `--format`.
- Run a full factorial Cartesian product across the listed values. If the total number of combinations exceeds 200, sample uniformly at random to 200 combinations and document the strategy in PROFILE.md.
- Execute experiments sequentially by default, restarting certus-server between combinations and avoiding parallel runs.
- For each combination:
  a. Stop any running certus-server.
  b. Start certus-server with the selected `--device-pci` flags, `--memory-tier-size`, and `--format`.
  c. Retry startup up to 3 times with a 5s delay if it fails. If startup still fails, record the combination as FAILED in PROFILE.md with stderr and continue.
  d. After a healthy start, run a 1-iteration warm-up of certus-api-bench before measurement.
  e. Run the measured iterations.
  f. If certus-api-bench exits non-zero, capture stdout/stderr to `<output-dir>/logs/<run-name>.log`, mark the run as ERROR in PROFILE.md, retry once, and if still failing continue to the next combination.
  g. Stop certus-server and collect logs.
- For each run write raw JSON to:
    <output-dir>/results/devicecount-<D>_mem-<M>_clients-<C>_bs-<B>_batch-<X>_objs-<O>_iter-<I>.json
  and a human-readable log to:
    <output-dir>/logs/devicecount-<D>_mem-<M>_clients-<C>_bs-<B>_batch-<X>_objs-<O>_iter-<I>.log

Run combinatorial experiments and build a result table in <output-dir>/PROFILE.md.

PROFILE.md must include a table with columns:
  device_count | pci_list | memory_tier_size_bytes | clients | block_size_bytes | batch_size | num_objects | iterations | throughput_GB_per_sec (populate) | throughput_GB_per_sec (hot lookup) | throughput_GB_per_sec (cold lookup) | notes

Include raw output file links and log links in PROFILE.md.

Summarize the data and identify performance anomalies.

Create a plot with Y-axis throughput, X-axis device_count for:
1. Populate
2. Lookup (hot)
3. Lookup (cold)

Save plot in output directory.
