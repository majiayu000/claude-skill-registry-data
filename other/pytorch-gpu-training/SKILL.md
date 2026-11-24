---
name: pytorch-gpu-training
description: Use when training or debugging PyTorch on GPUs.
---

# PyTorch GPU training

## FSDP2

- Backward prefetch targets the unit whose forward ran just before the current unit. A frozen unit between trainable units receives this prefetch and skips backward, so its parameters stay unsharded until the backward ends and each trainable unit's all-gather goes out on demand. When frozen units run between trainable units, call `set_modules_to_backward_prefetch([next_trainable_unit])` on each unit once at setup, in backward order.
- Check a mixed-precision policy through the unit's policy or communication dtype; master storage keeps its own dtype. When assigning submodule policies, verify every intended parameter belongs to an FSDP unit: parameters outside all units receive local updates without the intended cross-device synchronization.
- When a wrapped forward exposes the same leaf Parameter on each call, return a fresh non-leaf tensor instead. FSDP2 attaches pre-backward hooks to returned tensors, and reusing that leaf retains hooks across steps. Diagnose with growing `param._backward_hooks` and `AccumulateGrad` self time; a clone preserves gradient flow while giving the hook a step-local lifetime. A bare view has separate FSDP2 restrictions.
- The root-group reshard-after-forward override applies only when `reshard_after_forward` is None (`auto_reshard_after_forward`); an explicit `True` reshards and regathers the root every microbatch inside `FSDP::pre_backward`.
- Classify root all-gathers in a profiler trace by the enclosing FSDP hook annotation (`FSDP::pre_forward`, `FSDP::pre_backward`, or none for an explicit call), not by autograd-op proximity.
- When you set the all-reduce flag, call `set_requires_all_reduce` after `set_requires_gradient_sync(True)`, because `set_requires_gradient_sync` also writes the all-reduce flag.

## DTensor

- `DTensor.record_stream` raises `NotImplementedError` (`aten::record_stream` has no registered sharding strategy). For allocator safety when a wrapper-subclass tensor is consumed on a side stream, call `tensor._local_tensor.record_stream(stream)`.
- In torch 2.14, `DTensor.full_tensor()` returns a plain Tensor, not a DTensor.

## torch.compile boundaries

- A class-level `__call__` override runs eagerly outside the module's own `Module.compile()`, and backward hooks stay eager there too. `record_function` spans inside the compiled region are dropped, so mark with an op instead.
- Hooks and wrappers enter the graph when the module is called inside a parent's compiled frame. In that frame the backward-hook path raises only when `compiled_autograd` is enabled.
- Verify the compile boundary in the target revision before relying on either behavior.

## Selective activation checkpointing around compiled regions

- Compile the checkpointed region as one graph, so the AOT autograd partitioner applies the SAC policy at graph level. Where memory allows, leave the checkpointed block eager instead.
- In torch 2.14, SAC stores a saved op output as an alias that shares the op output's storage. When the checkpoint wraps a separately compiled region, inductor can reuse that output's buffer later in the same forward graph. A kernel that writes through a raw pointer bypasses SAC's version-counter mutation check, so the recomputation reads the overwritten tensor: the forward output and the loss stay correct, and the gradients come out wrong.
- To check a stack for this defect, compare its gradients against an eager run with checkpointing off on a small model.

## Distributed checkpoint saves

- Without plan caching, every `dcp.save` makes rank 0 unpickle the local save plans of all ranks, and that rank-0 cost grows linearly with rank count. Measure save planning on a multi-node run, where the cost shows.
- Pass `DefaultSavePlanner(enable_plan_caching=True)` to repeated saves. From the second save on, a rank with an unchanged plan sends an empty plan, and rank 0 reuses the cached global plan.

## Non-finite checks under AMP

- Use read-only norms and `isfinite` to locate non-finite values. The AMP helper `torch._amp_foreach_non_finite_check_and_unscale_` also rescales its inputs, so it changes the data being diagnosed.

## foreach operand lists

- Keep foreach operand lists in one dtype to preserve the batched fast path; bool masks can trigger per-tensor work.
- For finite inputs, `clamp_min(sign(x), 0)` implements `x > 0`, not `x >= 0`; test zero and non-finite behavior against the actual contract.
- Resolve the supported foreach operators from the installed framework.

## Sync-free training steps

- Keep steady-state training steps free of GPU synchronization and blocking device-to-host reads; stage scalar readback asynchronously outside that path.
- Boundary waits for teardown or final checkpoints are allowed.

## Data-loop stalls and garbage collection

- Compare the period of a repeating stall with the data-pass length implied by the live sampler and batch configuration; periodicity alone does not identify the cause.
- Confirm a suspected Python generation-2 collection with `gc.callbacks` timing before applying `gc.freeze()` after warmup.

## Profiler traces and kernel-to-launch correlation

- torch.profiler taxes the CPU thread. That tax lands one-to-one on step time only when the CPU lane is the longer lane; take steady-state step KPIs from unprofiled steps.
- Bin all-rank host profiles over time to drop the stock profiler window.
- Bind a GPU kernel to its CPU launch by the kineto correlation id.
- Join device-side collectives through the CPU `record_param_comms` events and ac2g links: host windows shift across groups. A compile delay can appear in the other group's following step, so filter both steps and join the logs by step key.
- Compare step-time arms paired by step under fixed seeding: step-time distributions are multimodal. Judge a step-localized gain by the mean paired delta.

## Kernel measurement on multi-die GPUs

- When profiling counters are admin-only (`ncu` fails with `RmProfilingAdminOnly`), read kernel activity counters through NVML GPM, which works from an unprivileged job: take two `nvmlGpmSampleGet` samples, then call `nvmlGpmMetricsGet`.
- Compare kernel variants on one GPU inside one job. Sample the SM clock and power in a side thread: a power cap moves the SM clock between kernels of equal FLOPs, and clocks also differ between GPUs of one node.
- On multi-die parts, each die's L2 caches only what that die's SMs read, so an operand that both dies read takes L2 space twice. Budget a shared operand against roughly half of `cudaDevAttrL2CacheSize`.
- Measure die membership per GPU from L2 latency: `%smid` interleaves dies at TPC granularity, and floorsweeping differs per chip.

## torch C++ extension JIT builds

- On torch 2.13 and earlier, a loader killed mid-build strands `<build dir>/lock` and `.ninja_lock`: later loaders wait silently until they hit their time limit. Once the builder has finished, delete both locks and rebuild.
- From torch 2.14 the build holds a `filelock.FileLock` on the same path, released when the holder dies, so the next loader rebuilds. Leave the `lock` file in place: deleting it mid-build lets two builds write one directory.
