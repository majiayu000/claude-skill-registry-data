---
name: dftracer-io-optimization
description: Key literature, bottleneck-to-optimization mappings, and strategies for the dftracer I/O optimization pipeline
---

## Key Reference Papers

### WisIO (primary bottleneck → optimization guide)

**Citation:** Yildirim, Izzet, Hariharan Devarajan, Anthony Kougkas, Xian-He Sun, and
Kathryn Mohror. "WisIO: Automated I/O Bottleneck Detection with Multi-Perspective Views
for HPC Workflows." In *Proceedings of the 39th ACM International Conference on
Supercomputing*, pp. 749–763. 2025.

**What it provides:**
- Multi-perspective bottleneck taxonomy covering: sequentiality, small-I/O,
  read/write time fraction, metadata overhead, fetch pressure, stragglers
- Per-category root cause + optimization strategy mapping
- Quantified thresholds for high/critical classification

**Bottleneck → optimization mapping from WisIO:**

| WisIO category      | Metric in dfdiagnoser | Primary fix (L1→L3)                              |
|---------------------|-----------------------|--------------------------------------------------|
| small-io            | small_io_pct          | L1: buffer reads; L2: collective I/O; L3: stripe |
| sequentiality       | rand_pct / seq_pct    | L1: sort access; L2: prefetch hint; L3: readahead|
| read-time           | read_time_pct         | L1: async I/O; L2: cb_buffer; L3: blockdev setra |
| write-time          | write_time_pct        | L1: async write; L2: dirty tuning; L3: vm.dirty  |
| metadata            | metadata_time_pct     | L1: cache stats; L2: HDF5 metadata opt; L3: MDT  |
| fetch-pressure      | fetch_pressure        | L1: DataLoader workers; L2: prefetch_factor       |
| stragglers          | epoch_straggler       | L1: sort by size; L2: persistent_workers          |


### Drishti (user-facing optimization guidance)

**Citation:** Bez, Jean Luca, Hammad Ather, and Suren Byna. "Drishti: Guiding
end-users in the I/O optimization journey." In *2022 IEEE/ACM International Parallel
Data Systems Workshop (PDSW)*, pp. 1–6. IEEE, 2022.

**What it provides:**
- End-user-facing optimization suggestions organized by I/O category
- Three-level suggestion structure (application / library / system) matching our L1/L2/L3
- Estimated improvement ranges per suggestion type

**Drishti suggestion model:**

| Drishti category | L1 (app)                     | L2 (software)               | L3 (system)                |
|------------------|------------------------------|-----------------------------|----------------------------|
| small-io         | buffer reads, batch writes   | ROMIO cb_buffer, HDF5 chunks| lfs setstripe -S 4m        |
| metadata         | cache stat(), open once      | H5Pset_coll_metadata_write  | lfs mkdir -c N (DNE)       |
| sequentiality    | sort indices, posix_fadvise  | romio_ds_read=enable        | blockdev --setra 4096      |
| shared-file      | independent file per rank    | romio_cb_read=enable        | increase OST count         |


## Optimization Metric Selection Guide

Use this when the agent must suggest which metric to optimize:

| Dominant bottleneck(s)              | Recommended metric | Rationale                        |
|-------------------------------------|--------------------|----------------------------------|
| read_time_pct or write_time_pct ≥4  | time               | Latency is the binding constraint|
| read_bw_mean or write_bw_mean low   | bandwidth          | Throughput is the binding limit  |
| small_io_pct or rand_pct ≥4         | iops               | Operation rate limits throughput |
| metadata_time_pct ≥4                | metadata_ops       | Metadata is the bottleneck       |
| multiple ≥4                         | time (default)     | Most general; addresses all      |


## Common Parameter Recommendations (from WisIO + Drishti)

- **Buffer size:** 4 MB aligned to Lustre stripe size (1 MB default stripe)
- **ROMIO collective buffer:** 64 MB (`cb_buffer_size=67108864`)
- **Lustre stripe count:** 4–8 for files < 10 GB; 16+ for very large files
- **Linux readahead:** 2–8 MB (`blockdev --setra 4096` to `16384`)
- **DataLoader workers:** `cpu_count // 2` with `prefetch_factor=4`
- **PyTorch checkpoint:** async save in background thread; use lz4 compression
- **vm.dirty_ratio:** 10–20% for write-heavy; 5–10% for checkpoint workloads


## Artifact Files Produced by optimize.yaml

| File                        | Contents                                     |
|-----------------------------|----------------------------------------------|
| `optimization_context.json` | Metric, bottlenecks, papers — shared context |
| `opt_l1_results.json`       | L1 proposals, status, files modified         |
| `opt_l2_results.json`       | L2 proposals, env vars applied               |
| `opt_l2_env.sh`             | Source before each run to keep L2 settings   |
| `opt_l3_results.json`       | L3 changes + rollback commands               |
| `optimization_papers.json`  | Full literature search results               |
