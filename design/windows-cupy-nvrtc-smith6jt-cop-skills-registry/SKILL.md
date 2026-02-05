---
name: windows-cupy-nvrtc
description: "Fix CuPy NVRTC compilation errors on Windows. Trigger: NVRTC_ERROR_BUILTIN_OPERATION_FAILURE, nvrtc-builtins64 not found"
author: KINTSUGI Team
date: 2025-12-11
---

# Windows CuPy NVRTC Fix

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-11 |
| **Goal** | Fix CuPy GPU operations failing with NVRTC compilation errors on Windows |
| **Environment** | Windows 10/11, CUDA 12.1, CuPy 13.x, Conda environment |
| **Status** | Success |

## Context
CuPy uses NVRTC (NVIDIA Runtime Compiler) for JIT compilation of CUDA kernels. On Windows, the NVRTC DLLs are installed with CUDA but not automatically added to the system PATH. This causes CuPy operations to fail at runtime even when CUDA is properly installed.

### Error Signature
```
cupy.cuda.compiler.CompileException: nvrtc: error: failed to open nvrtc-builtins64_121.dll.
Make sure that nvrtc-builtins64_121.dll is installed correctly.
```

Or:
```
cupy_backends.cuda.libs.nvrtc.NVRTCError: NVRTC_ERROR_BUILTIN_OPERATION_FAILURE (7)
```

## Verified Workflow

### Solution 1: Add CUDA bin to PATH at runtime (Recommended)

```python
import os
import platform

def setup_cuda_path():
    """Setup CUDA PATH for CuPy on Windows."""
    if platform.system() != "Windows":
        return True

    # Common CUDA installation paths
    cuda_paths = [
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin",
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin",
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin",
    ]

    for cuda_bin in cuda_paths:
        if os.path.exists(cuda_bin):
            # Check for nvrtc DLLs
            nvrtc_files = [f for f in os.listdir(cuda_bin) if f.startswith('nvrtc')]
            if nvrtc_files:
                os.environ["PATH"] = cuda_bin + os.pathsep + os.environ.get("PATH", "")
                print(f"Added CUDA to PATH: {cuda_bin}")
                return True

    print("CUDA not found - GPU acceleration may not work")
    return False

# Call BEFORE importing CuPy-dependent code
setup_cuda_path()

# Now CuPy will work
import cupy as cp
```

### Solution 2: For Jupyter notebooks

Add this cell at the very beginning, before any other imports:

```python
import os
cuda_bin = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin"
os.environ["PATH"] = cuda_bin + os.pathsep + os.environ.get("PATH", "")
```

### Solution 3: System-wide fix (permanent)

Add the CUDA bin directory to your system PATH:
1. Open System Properties > Environment Variables
2. Edit the PATH variable
3. Add: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin`
4. Restart your terminal/IDE

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Installing cuda-nvrtc via conda | DLLs installed to conda env, but PATH not updated | Conda doesn't auto-add Library/bin to PATH |
| Setting CUDA_PATH env variable | CuPy doesn't read CUDA_PATH for runtime libs | Must modify PATH directly |
| Adding PATH after CuPy import | CuPy caches paths at import time | PATH must be set BEFORE any CuPy import |
| CPU fallback as workaround | User explicitly wanted GPU, not CPU | Fix the root cause, don't mask it |

## Key Insights

- **Order matters**: PATH must be modified before ANY import that touches CuPy
- **CUDA version matching**: The nvrtc DLL version (e.g., `nvrtc64_121.dll`) must match your CUDA toolkit
- **Conda environments**: Even with `cuda-nvrtc` package, you may need to add `$CONDA_PREFIX/Library/bin` to PATH
- **Multiple CUDA versions**: If you have multiple CUDA versions, ensure PATH points to the correct one for your CuPy version
- **Verification command**:
  ```python
  import cupy as cp
  x = cp.array([1, 2, 3])
  print(x * 2)  # Should work without errors
  ```

## Environment Details

Works with:
- CUDA Toolkit 11.x, 12.x
- CuPy 12.x, 13.x
- Windows 10, Windows 11
- Conda and pip installations

## References
- CuPy CUDA setup: https://docs.cupy.dev/en/stable/install.html
- NVIDIA CUDA Toolkit: https://developer.nvidia.com/cuda-toolkit
- Related GitHub issues: CuPy NVRTC errors are common on Windows
