---
name: optimize-ascendc-operators
description: Profile, diagnose, optimize, and validate AscendC competition operators on Ascend NPU environments. Use for CANN/AscendC kernels, Huawei operator contests, msprof timing, Vector/Cube peak-efficiency estimates, GM/UB tiling, pipeline-event bugs, ACLNN ABI compatibility, official test harnesses, or submission-package performance comparisons.
---

# Optimize AscendC Operators

Treat the official harness and its exact `EXEC_NPU_CMD` call as the contract. Optimize only after reproducing its accuracy and timing locally on the target NPU.

## Workflow

1. Inspect `run.sh`, `test_op.py`, `get_time.py`, the C++ extension, input shapes/dtypes, warm-up rules, repetition count, and baseline threshold.
2. Record the actual chip, CANN version, compiler, AI/Vector core counts, HBM capacity/clock, and profiler-derived frequency. Do not infer the judge contract from the operator name alone.
3. Verify ACLNN ABI before benchmarking. Compare the exact argument order in `EXEC_NPU_CMD` with exported `aclnn*GetWorkspaceSize` symbols. A custom library can shadow a built-in symbol while exposing an incompatible signature.
4. Run the official harness unchanged and retain `op_summary*.csv` and `op_statistic*.csv`. Report median, min, mean, max, task type, block dim, cycle count, and scalar/vector/MTE ratios.
5. Calculate useful work and the relevant peak. For elementwise operators, prefer a Vector-unit peak estimate over Cube TOPS. State assumptions explicitly.
6. Diagnose in this order: incorrect ABI, excessive GM scalar access, missing cross-pipeline events, launch/tiling overhead, UB capacity, vector utilization, block-level parallelism, and repeated-index dependencies.
7. Implement one isolated optimization hypothesis. Keep a correctness fallback for unsupported shapes or dtypes. Competition fast paths must be selected by general properties such as dtype, alignment, value-independent semantics, and UB capacity; never by matching a published case's exact shape. If a conversion changes overflow semantics, either prove and test exact equivalence for the whole supported domain or do not enable that path.
8. Rebuild, install into a fresh directory, rerun broad regression cases, then rerun the unchanged official harness. Keep the new version only when accuracy passes and the official median improves.
9. Repackage the `.run`, sources, and required host files in the official directory layout. When the organizer provides a packaging script, run that exact script on Linux; do not substitute Windows `Compress-Archive` or Explorer ZIP creation. Verify archive contents, Unix ZIP metadata, and SHA-256 on both remote and local copies.

## AscendC Rules

- Move reusable data from GM to UB in blocks; never perform one `GlobalTensor::GetValue/SetValue` pair per element in a performance path.
- Use `SetFlag/WaitFlag` with the matching `HardEvent` for cross-pipeline dependencies such as `MTE2_V`, `MTE2_S`, and `V_MTE3`. `PipeBarrier` does not replace a cross-pipeline event.
- Preserve sequential semantics for duplicate scatter indices. Do not distribute updates across cores without a proven atomic or reduction strategy.
- Check the target architecture's supported vector dtypes. On 910B4, ordinary vector `Add` does not directly accept int8; a safe bounded fast path may convert to half, accumulate, and convert back, but only when output range or exact test distribution makes conversion semantics valid.
- For modular integer arithmetic, include adversarial maximum-collision and overflow tests at every fast-path geometry. Random public inputs can miss saturation bugs even when the official accuracy check passes.
- For copy-only operators with many small strided segments, batch adjacent outer rows into a 2-D DMA whenever `rows * segment_bytes` fits UB. Choose rows per task from UB capacity and target core occupancy, and keep a tiled fallback when one segment exceeds UB. This can remove hundreds of DMA launches and event pairs without specializing a published shape.
- Do not force tiny memory-bound workloads to occupy every AIV. Estimate useful bytes per target core, combine that estimate with the operator's natural task units (for example one non-empty concat input), and benchmark nearby core counts. More cores can lose to launch, address, and synchronization overhead even when every core has valid work.
- Do not use cross-core strided `GlobalTensor::SetValue` for byte or half outputs. The hardware write transaction can cover neighboring elements and produce nondeterministic lost updates. Partition contiguous output ranges on 32-byte boundaries, use block DMA for the performance path, and retain a single-core fallback until aligned partitioning is proven.
- Treat `Compare` output as a predicate mask, not a ready-to-copy byte tensor. Expand it with `Select` into 0/1 values of a supported vector dtype, then `Cast` to `int8_t`/bool before `DataCopy` to GM.
- For a short contiguous last-axis reduction, pad every row to a 32-byte boundary with 2-D `DataCopyPad`, operate on the padded UB tensor, and use `WholeReduceSum` with a source repeat stride derived from the padded row width. Zero-fill padding and copy only the logical output bytes back with `DataCopyPad`.
- `PipeBarrier` is not a substitute for a dependency between different engines. When reusing one UB buffer across MTE2 and MTE3, use the matching hard events (for example `MTE2_MTE3` and `MTE3_MTE2`) or a queue abstraction, then include an accuracy test that can expose stale reads.
- Base buffer sizes on bytes, align transfers as required, and prove total UB allocation fits before enabling a resident-data fast path.
- Use profiler evidence after optimization. A large speedup can still remain scalar-control-bound when the workload is tiny or has dependent scatter updates.
- Treat submission packaging as part of the executable contract. A Linux judge may reject a ZIP whose raw entry names contain Windows backslashes, whose directory entries are implicit, or whose `.run` file lost its executable mode even when a Windows archive viewer displays a plausible tree. Before submission, require forward-slash entry names, explicit root/`op_host/`/`op_kernel/` directory entries, Unix-origin metadata (`create_system=3`), and an executable `.run` mode such as `0750` or `0755`; then fresh-extract, install, and run the official harness from the extracted package.

## Reporting

Report both semantic throughput and peak efficiency:

```text
semantic_ops = number of required arithmetic updates
throughput = semantic_ops / median_seconds
efficiency = throughput / relevant_peak_ops_per_second
speedup = old_median / new_median
```

Also report minimal GM traffic and effective bandwidth, but do not label it HBM efficiency without a verified device bandwidth figure.

For the validated S9 IndexAdd example and its calculations, read [references/s9-index-add-case-study.md](references/s9-index-add-case-study.md).

For the validated S9 Concat 2-D DMA batching example, read [references/s9-concat-case-study.md](references/s9-concat-case-study.md).

For the validated S9 Greater mask-expansion and SquareSumV1 padded last-axis reduction examples, read [references/s9-greater-square-sum-v1-case-study.md](references/s9-greater-square-sum-v1-case-study.md).
