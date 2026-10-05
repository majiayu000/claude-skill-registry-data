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


## Built-in Citations

These two references are always available and must be used when their coverage matches the bottleneck being addressed.

### WisIO (Yildirim et al., ICS 2025)

- **Authors:** Izzet Yildirim, Hariharan Devarajan, Anthony Kougkas, Xian-He Sun, Kathryn Mohror
- **Title:** "WisIO: Automated I/O Bottleneck Detection with Multi-Perspective Views for HPC Workflows"
- **Venue:** Proceedings of the 39th ACM International Conference on Supercomputing (ICS 2025), pp. 749–763
- **URL:** https://dl.acm.org/doi/10.1145/3721145.3730395
- **Covers:** small_io, rand/seq (sequentiality), read_time, write_time, metadata_time, fetch_pressure, epoch_straggler

### Drishti (Bez et al., PDSW 2022)

- **Authors:** Jean Luca Bez, Hammad Ather, Suren Byna
- **Title:** "Drishti: Guiding end-users in the I/O optimization journey"
- **Venue:** 2022 IEEE/ACM International Parallel Data Systems Workshop (PDSW), pp. 1–6. IEEE, 2022
- **URL:** https://ieeexplore.ieee.org/document/10027503
- **Covers:** small-io buffering, metadata caching, sequentiality hints, collective I/O (maps to L1/L2/L3 suggestion layers)


## Metric to Optimization Goal Mapping

Use this table to translate the chosen metric into the dftracer analysis fields that must improve:

| Metric        | Goal                        | Target dftracer fields                                          |
|---------------|-----------------------------|-----------------------------------------------------------------|
| `time`        | Minimize I/O latency        | `read_time_pct`, `write_time_pct`, `metadata_time_pct`         |
| `bandwidth`   | Maximize throughput         | `read_bw_mean`, `write_bw_mean`, `seq_pct`                     |
| `iops`        | Maximize I/O operations/sec | `small_io_pct`, `rand_pct`, `intensity_mean`                   |
| `metadata_ops`| Reduce metadata overhead    | `metadata_time_pct`, `metadata_time_frac_parent`               |

When multiple bottleneck scores are >= 4, default to `time` as the most general metric that addresses all dimensions.


## L1 Application Strategies

These are source-code-level changes (applied under `<WS>/annotated/`). No system or middleware config changes at this layer.

### small_io / small_read / small_write  (metric: bandwidth or iops)

- Coalesce small reads into a single larger read with a staging buffer
- Replace per-element writes with batch writes to a pre-allocated buffer
- Use `readv`/`writev` (scatter/gather) instead of loops of `read`/`write`
- For Python: increase `chunk_size` in file iteration; use `np.fromfile` over loops

### rand / low seq_pct  (metric: bandwidth or time)

- Reorder access so items are read in file-offset order (sort indices before I/O)
- Add `posix_fadvise(fd, 0, 0, POSIX_FADV_SEQUENTIAL)` before sequential reads
- Use `mmap` for random access patterns to let the OS handle page faults
- For deep learning: sort dataset by file size, shuffle only indices in memory

### read_time / write_time  (metric: time)

- Pre-open files and keep file descriptors open across iterations
- Use `O_DIRECT` for cache-bypassing when data reuse is low
- Add async I/O: `io_uring` (C/C++) or `aiofiles`/`asyncio` (Python)
- Pre-allocate file size with `fallocate` before writing to avoid fragmentation

### metadata_time  (metric: metadata_ops)

- Cache `stat()` results; avoid repeated `lstat`/`stat` on the same paths
- Open files once per epoch, not once per sample
- Replace `readdir()` loops with pre-built file-list caches
- For Python: replace `os.path.exists()` in hot loops with `try`/`except`

### fetch_pressure / epoch_straggler  (metric: time or bandwidth — deep learning)

- Increase DataLoader `num_workers` (recommend: `cpu_count // 2`)
- Set `prefetch_factor=4` (PyTorch >= 1.7) or use `tf.data.AUTOTUNE`
- Pre-fetch next batch while compute runs the current one
- Use `persistent_workers=True` to avoid worker respawn overhead

### intensity / checkpoint  (metric: time)

- Write checkpoints asynchronously (background thread or process)
- Use memory-mapped files for checkpoint buffers before flushing to disk
- Compress checkpoints in-memory before writing (lz4 is fast enough)


## L2 Software/Middleware Strategies

These are configuration-level changes: environment variables, library hint files, and runtime config. No source code changes. All changes must be reversible (document the original value).

### MPI-IO / ROMIO  (bottleneck: small_io or rand_pct high — metric: bandwidth or time)

- Enable collective buffering: `ROMIO_HINTS=cb_buffer_size=67108864;romio_cb_read=enable`
- Set data sieving: `romio_ds_read=enable;romio_ds_write=enable`
- Increase aggregator count: `cb_nodes=<num_nodes>`
- Write a hints file at `<WS>/romio_hints.txt` and set the `ROMIO_HINTS` env var to its path

### HDF5  (bottleneck: small_io high — metric: bandwidth or iops)

- Set chunk dimensions to align with collective I/O buffer (e.g. 1 MB chunks)
- Enable HDF5 collective metadata: `H5Pset_coll_metadata_write`, `H5Pset_all_coll_metadata_ops`
- Set chunk cache: `H5Pset_cache(fapl, 0, 521, 64*1024*1024, 1.0)`
- For parallel HDF5: set PHDF5 alignment (`H5Pset_alignment`) to stripe size

### HDF5 metadata  (bottleneck: metadata_time high — metric: metadata_ops)

- Disable HDF5 metadata cache evictions during write-heavy phases
- Batch attribute writes with `H5Pset_object_track_times(False)`

### NetCDF / PnetCDF

- Set `nc_set_default_format(NC_FORMAT_NETCDF4_CLASSIC)` for better performance
- Enable collective I/O: `nc_var_par_access(ncid, varid, NC_COLLECTIVE)`

### PyTorch / Deep Learning  (bottleneck: fetch_pressure or small_io high — metric: time or bandwidth)

- DataLoader: `num_workers = cpu_count // 2`, `prefetch_factor = 4`
- DataLoader: `pin_memory = True` (when GPU is present)
- DataLoader: `persistent_workers = True` (avoids respawn per epoch)
- For datasets: use `worker_init_fn` to pre-open file handles per worker
- `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128` (reduces alloc fragmentation)

### PyTorch epoch stragglers  (bottleneck: epoch_straggler high — metric: time)

- Sort dataset by sample size before training to reduce tail latency per batch
- Use `DistributedSampler` with `shuffle=False`; pre-shuffle indices once

### PyTorch checkpoints  (bottleneck: checkpoint high — metric: time)

- `torch.save` with `_use_new_zipfile_serialization=False` for faster writes
- Async checkpoint: `torch.save` in a separate thread
- Set `TORCH_HOME` to a fast local scratch directory

### TensorFlow

- `tf.data.AUTOTUNE` for prefetch buffer sizes
- `tf.data.experimental.AUTOTUNE` for interleave `cycle_length`
- Set `TF_CUDNN_USE_AUTOTUNE=1`, `TF_GPU_THREAD_MODE=gpu_private`

### General I/O libraries  (bottleneck: rand_pct high — metric: bandwidth)

- Set POSIX readahead: `POSIX_FADV_SEQUENTIAL` via `posix_fadvise` (env-level wrapper)
- Configure library-level read-ahead buffer (if applicable)

### Environment variable wrapper script (general)

- `OMP_NUM_THREADS`, `MKL_NUM_THREADS`: set to physical core count for I/O threading
- `MALLOC_ARENA_MAX=2`: reduce glibc arena fragmentation for I/O-heavy apps
- `HBWMALLOC_POLICY=transparent`: use high-bandwidth NUMA memory when available
- Collect all L2 env vars in `<WS>/opt_l2_env.sh`; source before every run


## L3 OS/Filesystem Strategies

These are OS- and filesystem-level tuning changes. Many require `sudo` or storage-admin access. Every proposal MUST include a rollback command and a privilege classification (`no-sudo | sudo | admin-only`).

### Lustre parallel filesystem  (bottleneck: any_io or bandwidth — metric: bandwidth or iops)

- **Stripe count** (no sudo, per-directory):
  `lfs setstripe -c <N> <WS>/traces/`
  Rollback: `lfs setstripe -c 1 <WS>/traces/`
  Recommendation: N = OST count, capped at 8 for files < 1 GB; 16+ for very large files
- **Stripe size** (no sudo):
  `lfs setstripe -S 4m <WS>/traces/`  (4 MB aligns to ROMIO collective buffer)
  Rollback: `lfs setstripe -S 1m <WS>/traces/`
- **OST pool** (no sudo, if NVMe/SSD pool available):
  `lfs setstripe --pool flash <WS>/`
- **Per-file stripe before write** (no sudo):
  `lfs setstripe -c 4 -S 4m <WS>/traces/<file>` before writing

### Lustre metadata  (bottleneck: metadata_time high — metric: metadata_ops)

- Disable file creation time tracking: `lfs setstripe --mdt-count 1` (for small dirs)
- Use DNE (Distributed Namespace): `lfs mkdir -c <N>` (admin-only)
- Client-side: mount with `-o localflock` to reduce lock traffic (requires remount — admin)

### Linux kernel readahead  (bottleneck: read_time or seq_pct low — metric: time or bandwidth)

- **Per-device** (sudo):
  `sudo blockdev --setra <KB> /dev/<dev>`
  Default: 128 (64 KB); recommended: 4096–16384 (2–8 MB)
  Rollback: `sudo blockdev --setra 128 /dev/<dev>`
  Side effect: affects all processes reading from this device
- **Per-process** (no sudo — cross-layer L1 reinforcement):
  `posix_fadvise(fd, 0, 0, POSIX_FADV_SEQUENTIAL)` in source code
- **Persistent** (sudo): `/etc/udev/rules.d/60-readahead.rules`

### VM and page cache tuning  (bottleneck: write_time or checkpoint high — metric: time)

- `sudo sysctl -w vm.dirty_ratio=20`
  (flush dirty pages when 20% of RAM is dirty; tune to 10–40)
  Rollback: `sudo sysctl -w vm.dirty_ratio=20`
- `sudo sysctl -w vm.dirty_background_ratio=5`
  (start background flush at 5%; reduces write stalls; default 10)
- `sudo sysctl -w vm.dirty_expire_centisecs=3000` (30 s dirty page lifetime)
- `sudo sysctl -w vm.dirty_writeback_centisecs=500` (flush every 5 s)
- Side effect: affects all dirty-page behavior on the node

### VM page cache (read-heavy)  (bottleneck: read_time high, data fits in RAM)

- `sudo sysctl -w vm.vfs_cache_pressure=50`
  (reduce kernel tendency to reclaim page cache; default 100)
  Rollback: `sudo sysctl -w vm.vfs_cache_pressure=100`

### I/O scheduler  (bottleneck: rand_pct high on SSD/NVMe — metric: iops or time)

- Check current scheduler: `cat /sys/block/<dev>/queue/scheduler`
- For NVMe (no scheduler overhead): `echo none | sudo tee /sys/block/<dev>/queue/scheduler`
- For HDD: `echo mq-deadline | sudo tee /sys/block/<dev>/queue/scheduler`
- Rollback: `echo <original_scheduler> | sudo tee /sys/block/<dev>/queue/scheduler`

### NUMA memory binding  (bottleneck: fetch_pressure or intensity high — metric: time or bandwidth)

- Check topology: `numactl --hardware`
- Pin process to NUMA node with local memory (no persistent side effect):
  `numactl --cpunodebind=0 --membind=0 <run_command>`
- For MPI: `mpirun --map-by numa:pe=<cores_per_node>` (OpenMPI)

### Network filesystems (NFS, GPFS, BeeGFS)  (bottleneck: read_time or metadata_time high)

These typically require storage admin action — surface as MANUAL RECOMMENDATIONS only.
- NFS: mount with `rsize=1048576,wsize=1048576,async`
- GPFS: `mmchattr -r pagePool=<size>` (admin tool)
- BeeGFS: `beegfs-ctl --settuning --clientNumWorkerThreads=16` (admin)


## Citation Rule

Every optimization proposal presented to the user MUST include a verifiable citation with a URL (arXiv link, DOI, or stable webpage). Follow this search order for each unique bottleneck type:

1. Check `PAPERS` from `optimization_context.json` first (already fetched during pipeline setup).
2. Search arXiv: `dftracer__search_arxiv(query="<bottleneck_type> optimization HPC parallel I/O MPI", max_results=5, category="cs.DC")`
3. Search Semantic Scholar / combined: `dftracer__search_papers_combined(query="<bottleneck_type> I/O tuning parallel filesystem", max_results=5)`
4. For any promising arXiv hit, fetch the full record: `dftracer__get_arxiv_paper(paper_id="<arxiv_id>")`

For every citation record:
- authors, title, venue/journal, year
- URL: arXiv link, DOI, or page URL (e.g. `https://arxiv.org/abs/XXXX.XXXXX`)
- the specific finding or section that supports the proposed change (1–2 sentences)

**If no verifiable citation with a URL can be found for a proposal, that proposal MUST be skipped.** Do not present uncited proposals to the user. Instead, write "no L\<N\> fix — no citation available" for that bottleneck.
