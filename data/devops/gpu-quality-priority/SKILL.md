---
name: gpu-quality-priority
description: "KINTSUGI processing principles: Never sacrifice quality for speed, always use GPU when available. Trigger: performance optimization, CPU/GPU choice, fast mode, quality vs speed."
author: KINTSUGI Team
date: 2025-12-14
---

# GPU-Only and Quality-First Processing Principles

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-14 |
| **Goal** | Establish processing principles for KINTSUGI batch processing |
| **Environment** | HiPerGator, multi-GPU (NVIDIA), CuPy, KINTSUGI pipeline |
| **Status** | Policy Established |

## Context

During performance optimization of Notebook 2 (Cycle Processing), a "fast mode" was proposed that would reduce BaSiC iteration parameters to speed up processing. The user explicitly rejected this approach, establishing core principles for KINTSUGI processing.

**Scientific imaging requires quality-first processing.** Unlike consumer applications where "good enough" may be acceptable, multiplex immunofluorescence analysis depends on accurate quantification. Quality degradation compounds through the pipeline: illumination correction errors affect stitching, which affects deconvolution, which affects segmentation, which affects all downstream analysis.

## Core Principles

### 1. NEVER Sacrifice Quality for Speed

Quality parameters must remain at their scientifically-validated defaults unless the quality impact is **negligible** (verified, not assumed).

```python
# CORRECT: Quality parameters (do not reduce)
BASIC_IF_DARKFIELD = True
BASIC_MAX_ITERATIONS = 500
BASIC_OPTIMIZATION_TOLERANCE = 1e-6
BASIC_MAX_REWEIGHT_ITERATIONS = 25
BASIC_REWEIGHT_TOLERANCE = 1e-3
```

### 2. ALWAYS Use GPU When Available - No CPU Fallback

If a GPU is available, it must be used. CPU fallback options should be disabled or removed.

```python
# CORRECT: GPU enforcement
if not USE_GPU:
    raise RuntimeError(
        "GPU not available but required for processing.\n"
        "Check GPU status with: from kintsugi.gpu import get_gpu_manager; "
        "print(get_gpu_manager().summary())"
    )
use_gpu = True  # Always True - GPU required
```

### 3. Remove CPU Options When GPU Exists

Don't provide `use_cpu` or `use_gpu=False` options. If the system has a GPU, use it.

```python
# WRONG: Providing CPU option
def process(use_gpu=True):  # Allows use_gpu=False
    ...

# CORRECT: GPU-only
def process(device_id=None):  # GPU assumed, only device selection
    if device_id is None:
        device_id = GPU_DEVICE_IDS[0]
    ...
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Added `BASIC_FAST_MODE` with reduced iterations (200/10) | User rejected - quality is non-negotiable | Never propose quality/speed tradeoffs without explicit request |
| Added `use_gpu_basic=True/False` parameter | Creates temptation to use CPU | Remove CPU options entirely when GPU is available |
| Proposed "fast mode for testing" | Testing should use production parameters | If testing finds issues, they should be found with real parameters |
| Suggested relaxed tolerances (1e-5, 1e-2) | Even "slightly" relaxed tolerances compound errors | Keep validated parameters exactly as specified |

## Acceptable Optimizations

These optimizations improve speed WITHOUT sacrificing quality:

| Optimization | Impact | Safe? |
|-------------|--------|-------|
| Parallel image loading (ThreadPoolExecutor) | 10-20x faster I/O | YES - same data, faster loading |
| Parallel image resizing | 10-20x faster preprocessing | YES - same resize algorithm |
| GPU-accelerated computation | 10-50x faster | YES - same algorithm, faster hardware |
| Multi-GPU parallelism | Linear scaling | YES - same computation, more hardware |
| Optimized DCT (dctn vs sequential dct) | 2-3x faster | YES - mathematically equivalent |
| Power iteration for SVD | 10x faster | YES - sufficient for top singular value |

## Key Insights

- **Quality is non-negotiable** - Scientific imaging requires accurate quantification
- **Speed comes from better hardware, not shortcuts** - Invest in GPUs, not reduced iterations
- **Errors compound** - A 5% error in illumination correction becomes 10%+ by segmentation
- **"Fast mode for testing" is a trap** - Test with production parameters or you'll miss production issues
- **CPU fallback is never needed** - If no GPU, the user should know immediately, not get silent degradation

## Implementation Pattern

```python
# GPU enforcement at module level
if not USE_GPU:
    raise RuntimeError("GPU required for KINTSUGI processing")

# Function signatures - no CPU options
def process_zplane(
    ...,
    device_id: int = None,  # Which GPU, not whether to use GPU
):
    """GPU is REQUIRED - no CPU fallback."""
    if device_id is None:
        device_id = GPU_DEVICE_IDS[0]

    # Use validated quality parameters
    corrector = KCorrectGPU(use_gpu=True, device_id=device_id)
    flatfield, darkfield = corrector.fit(
        images,
        max_iterations=500,           # Quality parameter - DO NOT REDUCE
        max_reweight_iterations=25,   # Quality parameter - DO NOT REDUCE
        optimization_tolerance=1e-6,  # Quality parameter - DO NOT REDUCE
    )
```

## References

- KINTSUGI Notebook 2: Cycle Processing
- BaSiC paper: Peng et al., Nature Communications 2017
- Skills Registry: `basic-caching-evaluation` (another quality-compromising approach that failed)
