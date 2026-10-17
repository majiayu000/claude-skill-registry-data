---
name: aiwf-gpu-runtime-diagnostics
description: AIWF GPU runtime diagnostics skill for CUDA, ROCm, NVIDIA driver, PyTorch, torchvision, xformers, flash-attn, bitsandbytes, TensorRT, DirectML, VRAM, device visibility, Windows PATH, DLL load, quantization runtime, and local inference or training smoke failures. Use before changing GPU runtime code or reinstalling packages.
---

# AIWF GPU Runtime Diagnostics

Use this skill when local AI work fails at the hardware/runtime boundary. The job is to identify whether the problem is driver, Python environment, package ABI, CUDA or ROCm version, DLL/PATH loading, VRAM pressure, attention backend, or model-runtime configuration.

## Workflow

1. Preserve the failing command, error text, model/runtime name, and environment path.
2. Collect a read-only runtime snapshot before reinstalling packages.
3. Compare driver/runtime/package versions against the repo's pinned requirements.
4. Separate environment failure from model failure:
   - device invisible
   - package import failure
   - CUDA/ROCm ABI mismatch
   - missing DLL
   - out of memory
   - unsupported dtype or quantization
   - attention backend mismatch
   - TensorRT engine/runtime mismatch
5. Patch or recommend the smallest repo-native fix.
6. Prove with a bounded smoke receipt. Do not run VRAM-heavy generation or training unless Shawn asks.

Use `scripts/collect_gpu_runtime_snapshot.py` for a read-only local snapshot when Python is available. Read `references/gpu-diagnostics.md` for triage patterns and smoke guidance.

## Guardrails

- Do not install or upgrade GPU packages as a hidden side effect.
- Do not download large models to test the runtime unless requested.
- Do not assume CUDA latest is correct for the repo.
- Do not mix PyTorch CUDA wheels, TensorRT, xformers, flash-attn, or bitsandbytes versions without checking compatibility.
- Do not treat OOM as a code bug until batch size, dtype, resolution, context length, and existing GPU memory are checked.

## Final Add-On

For GPU/runtime work, include:

```text
Runtime checked:
- Driver/GPU: <value or not checked>
- Python env: <value or not checked>
- Torch/CUDA/ROCm: <value or not checked>
- Runtime package: <value or not checked>

Smoke:
- <command> -> passed/failed/not run

Residual risk:
- <remaining issue or none>
```
