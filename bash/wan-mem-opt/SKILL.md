---
name: wan-mem-opt
description: Run Wan2.1 T2V 1.3B with optimized memory usage on AMD UMA/ROCm. Use when the user says /wan-mem-opt, wants low-memory Wan 2.1 1.3B video generation, CPU UMT5/text-encoder placement, tiled VAE decode, or UMA memory profiling for Wan.
tags: [wan, wan2.1, memory, rocm, uma, pytorch, comfyui, video]
---

# /wan-mem-opt — low-memory Wan2.1 1.3B runner

This skill runs **Wan2.1 T2V 1.3B** in a direct Python process using ComfyUI's PyTorch backend, without launching the ComfyUI web server/API.

It is optimized for this AMD APU/iGPU UMA machine:

1. Default low-memory mode keeps **UMT5 / CLIP text encoder on CPU** to avoid the GPU text-encoder transient peak.
2. Alternative faster mode: `--clip-device default --free-clip-after-encode` loads UMT5 on GPU, encodes prompts, then immediately deletes it and calls `torch.cuda.empty_cache()`.
3. Use **tiled VAE decode by default** to reduce VAE decode peak.
4. Measure real UMA memory pressure via `/proc/meminfo` `MemAvailable` drop.

## Installed files

```text
/home/chihmin/.pi/agent/skills/wan-mem-opt/SKILL.md
/home/chihmin/.pi/agent/skills/wan-mem-opt/scripts/wan_mem_opt.sh
/home/chihmin/.pi/agent/skills/wan-mem-opt/scripts/run_wan21_direct_optimized.py
/home/chihmin/.pi/agent/skills/wan-mem-opt/scripts/profile_uma_memory.py
```

## Required local environment

Expected paths:

```text
/home/chihmin/src/ComfyUI
/home/chihmin/src/ComfyUI/.venv/bin/python
/home/chihmin/src/ComfyUI/models/diffusion_models/wan2.1_t2v_1.3B_fp16.safetensors
/home/chihmin/src/ComfyUI/models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors
/home/chihmin/src/ComfyUI/models/vae/wan_2.1_vae.safetensors
```

The model is **not GGUF**. It is a PyTorch/safetensors fp16 model:

```text
wan2.1_t2v_1.3B_fp16.safetensors
```

## Environment variables set by the launcher

The wrapper sets these defaults:

```bash
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
export MIOPEN_FIND_MODE=FAST
export MIOPEN_USER_DB_PATH=/home/chihmin/.cache/miopen-wan21
export PYTHONUTF8=1
```

Override if needed:

```bash
COMFY_PY=/path/to/python \
COMFY_DIR=/path/to/ComfyUI \
MIOPEN_USER_DB_PATH=/custom/cache \
/home/chihmin/.pi/agent/skills/wan-mem-opt/scripts/wan_mem_opt.sh ...
```

## Quick run

Lowest-memory default cat run, with UMA profile:

```bash
/home/chihmin/.pi/agent/skills/wan-mem-opt/scripts/wan_mem_opt.sh \
  --profile \
  --output /home/chihmin/generated/wan21_memopt_cat.mp4 \
  --steps 12 \
  --vae-mode tiled \
  --tile-size 256
```

If no runner args are provided, the wrapper generates a default cat video into a timestamped output directory.

## Warmup / precompile mode

Use `--warmup` to run an unsaved same-shape warmup pass **inside the same Python process** before the real generation. This is safer than `torch.compile` for the Comfy/Wan graph and helps populate ROCm/Triton/MIOpen caches for the exact resolution/frame shape.

```bash
/home/chihmin/.pi/agent/skills/wan-mem-opt/scripts/wan_mem_opt.sh \
  --profile \
  --warmup \
  --warmup-steps 1 \
  --output /home/chihmin/generated/wan21_memopt_warm.mp4 \
  --steps 12 \
  --clip-device default \
  --free-clip-after-encode \
  --vae-mode tiled --tile-size 256
```

Warmup behavior:

```text
same width/height/frames/vae mode as the real run
1 warmup sampling step by default
VAE warmup decode enabled by default
warmup output is not saved
warmup tensors are deleted and torch.cuda.empty_cache() is called before the real run
```

The first `--warmup` run can take longer overall because it includes the warmup pass. The benefit is mainly for repeated same-shape runs or avoiding first-use kernel/cache stalls during the measured real generation.

## Custom prompt

```bash
/home/chihmin/.pi/agent/skills/wan-mem-opt/scripts/wan_mem_opt.sh \
  --profile \
  --output /home/chihmin/generated/wan21_custom.mp4 \
  --prompt 'A cute cat is eating food from a small bowl on a cozy kitchen floor, close-up, realistic soft fur, gentle chewing motion, warm natural light, cinematic, stable camera, high quality video' \
  --width 832 --height 480 --frames 17 --fps 16 \
  --steps 12 --seed 2026070118 \
  --clip-device cpu \
  --vae-mode tiled --tile-size 256 --overlap 64 --temporal-size 16 --temporal-overlap 4
```

Frame rule: Wan video length should be `4n+1`, e.g. `17`, `49`, `73`.

## Runner options

Important options:

```text
--clip-device cpu                 Lowest peak memory. Keep UMT5 on CPU.
--clip-device default             Faster prompt encoding; loads UMT5 on GPU temporarily.
--free-clip-after-encode          Default. Delete UMT5/CLIP after pos/neg prompt encoding and call empty_cache().
--no-free-clip-after-encode       Debug only; keeps text encoder resident and wastes memory.
--warmup                          Wrapper option: append --warmup-steps 1 for same-process cache/kernel warmup.
--warmup-steps N                  Number of unsaved warmup sampling steps before the real run.
--warmup-decode                   Default. Also warm VAE decode kernels.
--no-warmup-decode                Warm sampler only, skip warmup VAE decode.
--vae-mode regular                Faster VAE decode, higher peak memory.
--vae-mode tiled                  Default. Lower peak memory, slower decode.
--tile-size 256                   Known-good low-memory tile size.
--steps 12                        Visual sanity quality; 1 step is only for profiling/kernel tests.
```

GPU text encoder with explicit cleanup works and is faster if you have enough transient headroom:

```bash
/home/chihmin/.pi/agent/skills/wan-mem-opt/scripts/wan_mem_opt.sh \
  --profile \
  --output /home/chihmin/generated/wan21_gpuclip_free.mp4 \
  --steps 12 \
  --clip-device default \
  --free-clip-after-encode \
  --vae-mode tiled --tile-size 256
```

## Known benchmark on this host

All runs: `832x480`, `17 frames`, `12 steps`.

| Setup | Actual UMA RAM drop | Peak ROCm GTT | Runtime |
|---|---:|---:|---:|
| Original default: GPU CLIP + regular VAE | ~19.82 GiB | ~18.55 GiB | ~48.7 s |
| CPU CLIP + regular VAE | ~13.73 GiB | ~12.28 GiB | ~57.2 s |
| CPU CLIP + tiled VAE | **~7.60 GiB** | **~5.53 GiB** | ~62.7 s |

Primary metric for UMA systems:

```text
actual UMA memory cost = baseline MemAvailable - minimum MemAvailable
```

Do **not** blindly add GTT + RSS on UMA; they are different accounting views and can overlap.

## Output/profile files

With `--profile`, the wrapper writes:

```text
<outdir>/uma_profile.csv
<outdir>/uma_profile.csv.summary
<outdir>/uma_profile.csv.stdout
<outdir>/uma_profile.csv.stderr
```

The `.summary` file contains:

```text
baseline_MemAvailable_GiB
min_MemAvailable_GiB
MemAvailable_drop_GiB
peak_rss_GiB
peak_rocm_gtt_GiB
peak_rocm_vram_GiB
```

## Troubleshooting

- If model files are missing, the launcher prints the missing path and exits.
- If output is low quality, increase `--steps`; memory should not grow much with steps, but runtime scales.
- If memory is still too high, ensure `--clip-device cpu` and `--vae-mode tiled` are both set.
- If tiled VAE has seams or differences, compare with `--vae-mode regular`; the tested 0.55s frame mean RGB diff was small (~2–3/255).
