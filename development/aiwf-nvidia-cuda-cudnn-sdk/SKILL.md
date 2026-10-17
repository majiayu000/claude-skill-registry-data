---
name: aiwf-nvidia-cuda-cudnn-sdk
description: Use for CUDA, cuDNN, TensorRT, SDK Manager, NVIDIA SDK, nvcc, kernel, and GPU-accelerated coding work.
---

# AIWF NVIDIA CUDA cuDNN SDK

## Core Rule

Verify the local NVIDIA stack before changing GPU code. Match driver, CUDA Toolkit, `nvcc`, cuDNN, TensorRT, PyTorch or framework wheels, compute capability, OS, and SDK target. Do not download SDKs, install drivers, or run VRAM-heavy work unless Shawn explicitly asks.

## Workflow

1. Inspect local environment first: `nvidia-smi`, `nvcc --version`, framework CUDA reports, CMake CUDA settings, `CUDAToolkit`, cuDNN/TensorRT headers, and SDK install paths.
2. Identify whether the code uses CUDA Runtime API, CUDA Driver API, cuDNN frontend/backend APIs, TensorRT, NCCL, Nsight, or SDK Manager-managed Jetson/DRIVE components.
3. Patch the smallest boundary: kernel code, host launch code, memory transfer, stream/sync logic, descriptor setup, CMake discovery, or package metadata.
4. Add error checks where missing: kernel launch errors, async errors after synchronization, cuDNN/TensorRT status returns, and allocation failures.
5. Validate with a cheap compile, device query, import probe, or unit test before any heavy benchmark.

## NVIDIA Guardrails

- Keep host/device code separation clear. Do not call host-only APIs from device code or assume unified memory behavior without checking target support.
- Always account for streams and synchronization. Many CUDA failures surface after the launch, not at the launch call.
- Check memory ownership, alignment, pitch, tensor layout, dtype, and workspace lifetime before changing kernels or cuDNN calls.
- Match architecture flags to the deployment GPU. Avoid hard-coding one `sm_` target unless the project intentionally does so.
- Do not mix runtime and driver API assumptions casually. When both are present, trace context ownership.
- By default, treat TensorRT plans as tied to the build/runtime version, platform, GPU characteristics, precision, plugins, and build settings. Version, hardware, or cross-platform compatibility exists only when the plan was built with the corresponding compatibility mode; verify the target support matrix and expected performance tradeoff.
- Deserialize TensorRT plans only from a trusted source. They contain executable compiled tactics.
- For SDK Manager projects, separate host setup, target flashing, and deploy/runtime validation.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
nvidia-smi
nvcc --version
cmake --build <build-dir> --config Release
ctest --test-dir <build-dir> --output-on-failure
python -c "import torch; print(torch.version.cuda); print(torch.cuda.is_available())"
```

Run only cheap probes unless asked. If the machine lacks an NVIDIA GPU or toolkit, report the missing component and validate with static/build checks where possible.

## Primary Source Anchors

- CUDA Programming Guide: https://docs.nvidia.com/cuda/cuda-programming-guide/index.html
- cuDNN documentation: https://docs.nvidia.com/deeplearning/cudnn/latest/
- TensorRT documentation: https://docs.nvidia.com/deeplearning/tensorrt/latest/
- TensorRT engine compatibility: https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/engine-compatibility.html
- NVIDIA SDK Manager documentation: https://docs.nvidia.com/sdk-manager/

NVIDIA version compatibility changes often. Verify the current official docs or installed headers before making a version-specific claim.
