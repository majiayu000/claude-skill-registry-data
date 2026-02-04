---
name: gpu-parallel-scheduling
description: "GPU-safe parallel processing patterns for KINTSUGI to prevent OOM crashes and ensure Jupyter-compatible progress output"
author: KINTSUGI Team
date: 2025-12-15
---

# GPU Parallel Scheduling - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-15 |
| **Goal** | Fix kernel crashes during parallel GPU processing in Notebook 2 |
| **Environment** | KINTSUGI pipeline, CuPy, multi-GPU HPC, Jupyter notebooks |
| **Status** | Success |

## Context
Notebook 2 (Cycle Processing) was crashing after Channel 1 completed when attempting to process remaining channels in parallel. The crash occurred immediately after the message "[PARALLEL] Processing channels [2, 3, 4] across GPUs..." with no further output.

## Root Cause Analysis

### Problem 1: Nested ThreadPoolExecutor Causing GPU Thread Explosion

The code structure was:
```python
# OUTER: Parallel channel processing
with ThreadPoolExecutor(max_workers=len(GPU_DEVICE_IDS)) as executor:
    for ch in channels:
        # INNER: Each channel spawns parallel z-plane workers
        process_channel_zplanes_parallel(ch, ...)
            # Inside this function:
            with ThreadPoolExecutor(max_workers=ZPLANES_PER_GPU) as inner_executor:
                # Process z-planes in parallel
```

With 2 GPUs, 3 channels, and `ZPLANES_PER_GPU=4`:
- Channel assignment: CH2→GPU0, CH3→GPU1, CH4→GPU0 (round-robin)
- GPU0 gets CH2 + CH4 simultaneously
- Each channel spawns 4 z-plane workers
- GPU0 runs 2 × 4 = 8 concurrent BaSiC corrections → **OOM CRASH**

### Problem 2: Jupyter Thread Output Suppression

Print statements from worker threads don't appear in Jupyter notebook output until the cell completes (or never). This made debugging difficult as processing appeared to stall.

### Problem 3: Missing GPU Memory Cleanup Between Channels

GPU memory from Channel 1 wasn't being freed before Channel 2 started, causing cumulative memory pressure.

## Verified Workflow

### Solution: Queue-Based GPU Allocation

Use a GPU queue to ensure **exactly 1 channel per GPU** at any time:

```python
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed

# Create pool of available GPUs
gpu_queue = queue.Queue()
for dev_id in GPU_DEVICE_IDS:
    gpu_queue.put(dev_id)

def process_channel_with_gpu(ch):
    """Process channel, acquiring and releasing GPU from queue."""
    # ACQUIRE: Block until a GPU is available
    dev_id = gpu_queue.get()
    ch_start = time.time()

    try:
        process_channel_zplanes_parallel(
            ...,
            device_id=dev_id,
            zplanes_per_gpu=ZPLANES_PER_GPU,
            ...
        )
        elapsed = time.time() - ch_start

        # GPU cleanup before releasing
        try:
            import cupy as cp
            with cp.cuda.Device(dev_id):
                cp.get_default_memory_pool().free_all_blocks()
                cp.get_default_pinned_memory_pool().free_all_blocks()
        except Exception:
            pass
        gc.collect()

        return (ch, dev_id, elapsed, None)
    except Exception as e:
        return (ch, dev_id, time.time() - ch_start, str(e))
    finally:
        # RELEASE: Return GPU to pool for next channel
        gpu_queue.put(dev_id)

# Process with max_workers = number of GPUs
with ThreadPoolExecutor(max_workers=len(GPU_DEVICE_IDS)) as executor:
    futures = {executor.submit(process_channel_with_gpu, ch): ch
               for ch in remaining_channels}

    # Main thread prints progress (Jupyter-compatible)
    for future in as_completed(futures):
        ch, dev_id, elapsed, error = future.result()
        if error:
            log(f"  [GPU{dev_id}] Channel {ch} ERROR: {error}")
        else:
            log(f"  [GPU{dev_id}] Channel {ch} COMPLETE ({elapsed:.1f}s)")
```

### Key Principles

1. **max_workers = n_gpus**: Never more concurrent channels than GPUs
2. **Queue acquisition**: Each channel blocks until it gets a GPU
3. **Queue release in finally**: GPU always returns to pool, even on error
4. **GPU cleanup before release**: Free memory before another channel uses the GPU
5. **Main-thread progress**: Use `as_completed()` to print from main thread

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Parallel channels with `iter_cycle(GPU_DEVICE_IDS)` | Pre-assigned GPUs didn't prevent multiple channels on same GPU | Need dynamic GPU allocation, not static assignment |
| `max_workers=len(GPU_DEVICE_IDS)` without queue | Channels could start on any GPU regardless of assignment | Queue ensures 1:1 GPU:channel mapping |
| Printing progress from worker threads | Output lost in Jupyter (thread stdout not captured) | Always print from main thread using `as_completed()` |
| GPU cleanup only at end of cell | Memory exhausted before cell completes | Cleanup after EACH channel, before releasing GPU |
| Nested ThreadPoolExecutor | Thread explosion: outer × inner workers | Inner parallelism is OK; outer must be limited to n_gpus |
| Adding status monitoring thread | Monitoring thread output also lost in Jupyter | Only main thread output is reliable in notebooks |

## Final Parameters

### GPU Queue Pattern
```python
# Initialize
gpu_queue = queue.Queue()
for dev_id in GPU_DEVICE_IDS:
    gpu_queue.put(dev_id)

# In worker
dev_id = gpu_queue.get()  # Blocks until available
try:
    # ... GPU work ...
finally:
    gpu_queue.put(dev_id)  # Always return
```

### Progress Output Pattern (Jupyter-safe)
```python
with ThreadPoolExecutor(max_workers=n_gpus) as executor:
    futures = {executor.submit(work_fn, item): item for item in items}

    for future in as_completed(futures):
        result = future.result()
        print(f"Completed: {result}")  # Main thread - visible in Jupyter
```

### GPU Cleanup Pattern
```python
try:
    import cupy as cp
    with cp.cuda.Device(device_id):
        cp.get_default_memory_pool().free_all_blocks()
        cp.get_default_pinned_memory_pool().free_all_blocks()
except Exception:
    pass
gc.collect()
```

## Key Insights

- **CuPy is not thread-safe** for concurrent operations on the same GPU
- **Jupyter suppresses thread output** - always use main thread for progress
- **Queue > static assignment** for dynamic GPU allocation
- **Cleanup before release** prevents memory accumulation
- **Inner parallelism is safe** (z-planes on single GPU) when outer is controlled
- **1 channel per GPU** rule prevents all OOM issues from parallel processing

## When to Apply This Pattern

- Multi-GPU parallel processing in Jupyter notebooks
- Any CuPy-based batch processing with parallelism
- When kernel crashes after first item completes in parallel loop
- When progress output disappears in parallel processing
- When OOM occurs despite having enough total GPU memory

## References

- CuPy Memory Management: https://docs.cupy.dev/en/stable/user_guide/memory.html
- Python concurrent.futures: https://docs.python.org/3/library/concurrent.futures.html
- KINTSUGI Notebook 2: Cycle Processing
- Related skill: `gpu-memory-cleanup` (per-channel cleanup pattern)
