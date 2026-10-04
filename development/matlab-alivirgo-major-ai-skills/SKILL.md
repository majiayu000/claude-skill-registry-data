---
name: matlab
description: "Automate MATLAB and Simulink workflows with Python integration, parallel loops, and MEX compilation."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["matlab", "matlab-engine-python", "simulink", "parallel-computing-parfor", "mex-c", "numerical-analysis", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# MathWorks MATLAB Numerical Computing & Algorithm AI Skill Guide (Claude)

## Overview & Engine Architecture
MathWorks MATLAB is the global standard for high-performance numerical computing, algorithm development, signal processing, and model-based systems simulation (Simulink). Built upon a **Just-In-Time (JIT) execution engine** and multi-threaded **Intel MKL / OpenBLAS LAPACK libraries**, MATLAB supports **Parallel Computing (`parfor` / `spmd`)**, **MEX C/C++ acceleration**, **Out-of-Core big data structures (`tall` arrays & `datastore`)**, and the **MATLAB Engine API for Python (`matlab.engine`)**. Claude operates as a Principal Computational Software Architect and Mathematical Systems Engineer, specializing in **vectorized M-code optimization**, **MATLAB-Python interoperability**, **MEX compilation setup**, and **FlexLM license diagnostics**.

### MATLAB Computational Architecture & Engine Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 MATLAB System Architecture                  │
│                                                             │
│  Interactive Development & Modeling Layer                   │
│  ├── MATLAB Desktop IDE (Editor, Workspace, Variable Viewer)│
│  ├── Live Editor Notebooks (`.mlx` Interactive Rich Media)  │
│  └── Simulink Model-Based Design (Block Diagram Solvers)    │
│                                                             │
│  JIT Compiler & Numerical Core (MKL/LAPACK)                 │
│  ├── JIT Accelerator & Native Vectorized Array Engine       │
│  ├── Parallel Computing Toolbox (`parfor`, GPU `gpuArray`)  │
│  └── Out-of-Core Processing (`tall` arrays, `matfile`)      │
│                                                             │
│  Extensibility & External Automation                        │
│  ├── MATLAB Engine API for Python (`import matlab.engine`)  │
│  ├── MEX Interface (Native C/C++/Fortran Dynamic Libraries) │
│  └── Headless Batch CLI (`matlab -batch "script.m"`)        │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **MATLAB Engine API for Python Automation**: Author Python scripts interfacing with `matlab.engine` to launch synchronous/asynchronous MATLAB sessions, pass multidimensional NumPy arrays, and execute toolbox routines.
2. **Vectorization & Memory Optimization**: Refactor slow, nested `for` loops into vectorized array operations (`bsxfun`, matrix multiplication, logical indexing) and pre-allocate arrays (`zeros()`) to eliminate JIT reallocation penalties.
3. **`parfor` Parallel Computing Triage**: Diagnose and resolve parallel loop variable classification errors (*sliced, broadcast, reduction, loop, and private variables*).
4. **MEX C/C++ Compiler Configuration**: Configure `mex -setup` with Microsoft Visual Studio (MSVC) or GCC/Clang to build high-speed native MEX binaries (`.mexw64` / `.mexmaci64`).

---

## Production Python Automation: MATLAB Engine for Python Data Processor (`matlab.engine`)

Save this script as `matlab_python_bridge.py` (requires `pip install matlabengine`):

```python
"""
MATLAB Engine API for Python: Asynchronous Matrix Processor
Launches MATLAB in the background, transfers NumPy matrices, runs Singular Value Decomposition (SVD), and returns data.
"""

import sys
import numpy as np
import matlab.engine

def execute_matlab_svd():
    print("--- [INITIALIZING MATLAB ENGINE API FOR PYTHON] ---")
    
    # 1. Start Background MATLAB Session
    print("Starting MATLAB engine instance...")
    eng = matlab.engine.start_matlab("-nodisplay -nosplash")
    print("✅ MATLAB Engine connected successfully!")

    try:
        # 2. Generate Test Matrix in NumPy (1000x500 random floats)
        np_matrix = np.random.randn(1000, 500).astype(np.float64)
        print(f"Generated NumPy Array: {np_matrix.shape} elements")

        # 3. Convert NumPy array to MATLAB double format
        mat_matrix = matlab.double(np_matrix.tolist())

        # 4. Execute Vectorized Matrix SVD in MATLAB
        print("Executing Singular Value Decomposition (SVD) inside MATLAB...")
        U, S, V = eng.svd(mat_matrix, nargout=3)

        # Convert result back to NumPy array
        singular_values = np.array(S).diagonal()
        top_5_sv = singular_values[:5]

        print("\n--- [RESULTS FROM MATLAB ENGINE] ---")
        print(f"• U Matrix Dimensions: {np.array(U).shape}")
        print(f"• Top 5 Singular Values: {top_5_sv}")
        print(f"• Matrix 2-Norm:         {top_5_sv[0]:.4f}")
        print("✅ MATLAB processing pass completed successfully.")

    finally:
        # 5. Terminate MATLAB Process
        eng.quit()
        print("MATLAB engine instance closed.")

if __name__ == "__main__":
    execute_matlab_svd()
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **"License checkout failed: Error -15 or -96"** | FlexLM license manager daemon (`lmgrd`) is unreachable on port 27000 or license expired. | 1. In terminal, verify license server: `lmutil lmstat -a -c 27000@licenseserver`.<br>2. Update `license.lic` in `C:\Program Files\MATLAB\R2025a\licenses\`. |
| **"Out of memory. Type 'help memory' for tips"** | Contiguous RAM allocation exhausted by double-precision ($64\text{-bit}$) array expansion. | 1. Pre-allocate array bounds before loops: `A = zeros(N, M, 'single');`.<br>2. Use `matfile('bigdata.mat', 'Writable', true)` to load and save array chunks partially without filling RAM. |
| **`parfor` Error: "Variable cannot be classified"** | Loop variable indexed across non-contiguous array slices or modified ambiguously across parallel workers. | Separate communication into pure sliced variables (e.g. `A(i, :)`) and reduction operations (e.g. `total = total + sum(A(i,:))`). |
| **MEX Compilation Fails: `No supported compiler found`** | C/C++ build tools not detected in system path. | In MATLAB Command Window, run `mex -setup C++` and install Microsoft Visual C++ Build Tools or Xcode Command Line Tools. |

---

## Command Line Syntax & Batch Execution Recipes

```bash
# 1. Execute Headless MATLAB Batch Script (Recommended R2019a+)
matlab -batch "run('C:\Scripts\RunAlgorithm.m'); exit"

# 2. Legacy Headless Execution with Output Logging
matlab -nodisplay -nosplash -r "try, run('analysis.m'), catch, exit(1), end; exit(0);" -logfile "matlab_run.log"

# 3. Compile Standalone Application via MATLAB Compiler (mcc)
mcc -m "MyAlgorithm.m" -d "C:\Deploy" -o "StandaloneRunner"
```

### Essential File Locations
- **Startup Script**: `%USERPROFILE%\Documents\MATLAB\startup.m`
- **Preferences Directory**: `%APPDATA%\MathWorks\MATLAB\R2025a\`
- **Path Definition**: `<MATLAB_ROOT>\toolbox\local\pathdef.m`

---

## Agent Operational Directive
> **MANDATORY**: Always pre-allocate matrix memory with `zeros()` or `ones()` before entering loops in MATLAB to prevent dynamic array reallocation from degrading JIT compiler performance.
