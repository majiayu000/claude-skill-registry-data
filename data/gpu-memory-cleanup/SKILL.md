---
name: gpu-memory-cleanup
description: "Preventing Jupyter cell hangs with explicit CuPy GPU memory cleanup"
author: KINTSUGI Team
date: 2024-12-15
---

# GPU Memory Cleanup - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-15 |
| **Goal** | Prevent Jupyter notebook cells from hanging after GPU processing completes |
| **Environment** | KINTSUGI pipeline, CuPy, Jupyter, NVIDIA GPU |
| **Status** | Success |

## Context
Jupyter notebook cells using CuPy for GPU-accelerated processing can hang after the main computation completes. The cell shows "complete" in output but the execution indicator keeps running. This is caused by CuPy's lazy memory cleanup blocking the Python interpreter.

## Symptoms
- Cell output shows processing is "complete" or prints final summary
- Cell execution indicator (star `[*]` or spinning) remains active
- Kernel appears responsive but cell never finishes
- Interrupting the cell doesn't lose any work (files already saved)

## Verified Workflow

### Add Explicit GPU Cleanup at End of Processing Cells

```python
# After your main processing loop completes...

# Explicit GPU cleanup to prevent hang
try:
    import cupy as cp
    cp.get_default_memory_pool().free_all_blocks()
    cp.get_default_pinned_memory_pool().free_all_blocks()
    print("GPU memory cleared")
except Exception:
    pass

import gc
gc.collect()
print("Stage complete")
```

### Full Pattern for Processing Cells

```python
import gc
import time

# Your processing code here
for item in items:
    process_item(item)
    gc.collect()  # Incremental cleanup during processing

# Final timing
end_time = time.time()
print(f"Processing complete: {end_time - start_time:.1f}s")

# CRITICAL: Explicit GPU cleanup before cell ends
try:
    import cupy as cp
    cp.get_default_memory_pool().free_all_blocks()
    cp.get_default_pinned_memory_pool().free_all_blocks()
    print("GPU memory cleared")
except ImportError:
    pass  # CuPy not available (CPU mode)
except Exception as e:
    print(f"GPU cleanup warning: {e}")

gc.collect()
print("Stage complete")  # This line confirms cell finished cleanly
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Relying on automatic cleanup | CuPy lazy cleanup can block indefinitely | Always add explicit cleanup at end of GPU-heavy cells |
| Only using `gc.collect()` | Python GC doesn't release GPU memory pools | Must use CuPy's memory pool methods |
| Adding cleanup inside loops | Slows processing, doesn't fix end-of-cell hang | Cleanup belongs at the END of the cell, after all work |

## Final Parameters

### Minimal Cleanup Block
```python
try:
    import cupy as cp
    cp.get_default_memory_pool().free_all_blocks()
    cp.get_default_pinned_memory_pool().free_all_blocks()
except Exception:
    pass
gc.collect()
```

### With Logging
```python
try:
    import cupy as cp
    mempool = cp.get_default_memory_pool()
    pinned_mempool = cp.get_default_pinned_memory_pool()

    used_before = mempool.used_bytes()
    mempool.free_all_blocks()
    pinned_mempool.free_all_blocks()

    print(f"GPU memory freed: {used_before / 1e9:.2f} GB")
except Exception:
    pass
gc.collect()
```

## Key Insights
- CuPy uses lazy memory management for performance
- When cell ends, Python may wait for CuPy cleanup indefinitely
- Explicit cleanup forces immediate memory release
- This is especially important after long-running processing loops
- Interrupting a hung cell is safe if all files have been saved
- The cleanup block should be the LAST code in the cell

## When to Apply This Pattern
- After BaSiC illumination correction loops
- After deconvolution processing
- After any multi-GPU parallel processing
- After EDF (Extended Depth of Focus) processing
- Any cell with `>30 seconds` of GPU-intensive work

## References
- CuPy Memory Management: https://docs.cupy.dev/en/stable/user_guide/memory.html
- KINTSUGI Notebook 2 (Cycle Processing)
