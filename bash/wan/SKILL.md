---
name: wan
description: Run Wan2.2 TI2V locally on this ROCm/gfx1151 machine using the official Wan2.2 repo, including the required ROCm environment variables, VAE Conv3D tiling workaround, numeric correctness checks, profiling, and known-good prompt/video generation commands.
version: 1.0.0
author: Hermes Agent
license: MIT
prerequisites:
  commands: [ffmpeg, ffprobe, timeout]
  paths:
    - /home/chihmin/src/Wan2.2
    - /home/chihmin/src/Wan2.2/.venv-rocm72
    - /home/chihmin/src/Wan2.2-deploy/wan22_cli.sh
    - /home/chihmin/models/Wan2.2-TI2V-5B
metadata:
  hermes:
    tags: [wan, wan2.2, video, text-to-video, ti2v, rocm, amd, gfx1151, conv3d, miopen]
    related_skills: [create-video, create-image, systematic-debugging]
---

# Wan2.2 on local ROCm GPU — official TI2V CLI

Use this skill when the user asks to run **Wan**, **Wan2.2**, **Wan TI2V**, or to generate/test/debug Wan videos on this machine.

This host has the official Wan2.2 repo deployed and patched for local ROCm behavior. The primary entrypoint is:

```bash
/home/chihmin/src/Wan2.2-deploy/wan22_cli.sh
```

## Machine-specific deployment

- Official repo: `/home/chihmin/src/Wan2.2`
- Deployment/helper folder: `/home/chihmin/src/Wan2.2-deploy`
- Python venv: `/home/chihmin/src/Wan2.2/.venv-rocm72`
- Model dir: `/home/chihmin/models/Wan2.2-TI2V-5B`
- Default output dir: `/home/chihmin/generated/wan22`
- GPU: `AMD Radeon 8060S` / gfx1151
- PyTorch: `2.12.1+rocm7.2`
- HIP: `7.2.53211`
- VAE checkpoint: `/home/chihmin/models/Wan2.2-TI2V-5B/Wan2.2_VAE.pth`

Verify environment:

```bash
/home/chihmin/src/Wan2.2-deploy/check_wan22_env.sh
/home/chihmin/src/Wan2.2/.venv-rocm72/bin/python - <<'PY'
import torch
print('torch', torch.__version__)
print('hip', torch.version.hip)
print('cuda_available', torch.cuda.is_available())
print('device', torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
PY
```

## Important local ROCm workaround

Wan2.2 multi-frame generation originally failed after denoising, inside VAE decode, in large MIOpen `Conv3D` kernels.

Evidence-backed failing path:

- Not T5
- Not DiT denoise
- Not video save
- Failure/hang occurred at `vae.decode`
- Microbench isolated large VAE `Conv3D`, e.g.
  - `input=(1,1024,6,178,322), weight=(512,1024,3,3,3)`
  - `input=(1,512,6,354,642), weight=(256,512,3,3,3)`
- Native/untiled MIOpen large Conv3D can throw `Failed to launch kernel: unspecified launch failure` on this host.

Patch in:

```text
/home/chihmin/src/Wan2.2/wan/modules/vae2_2.py
```

`CausalConv3d.forward()` supports output-height tiling when `WAN22_VAE_CONV3D_TILE_H > 0`.

Default wrapper settings:

```bash
export WAN22_VAE_DEVICE=cuda
export WAN22_VAE_DTYPE=bfloat16
export WAN22_VAE_CONV3D_TILE_H=44
```

Why it is correct: convolution output rows are independent except for the kernel-height input window. The tiler splits output height into stripes, includes `kernel_h - 1` input overlap for each stripe, runs normal `F.conv3d`, then concatenates along output height.

Do **not** disable tiling on 720p multi-frame tests unless specifically debugging MIOpen failure:

```bash
--vae-conv3d-tile-h 0   # disables workaround; may crash on this machine
```

Slow fallback if GPU VAE is suspect:

```bash
--vae-device cpu        # stable but very slow; 25f decode was ~220s in testing
```

## Wrapper usage

Show help:

```bash
/home/chihmin/src/Wan2.2-deploy/wan22_cli.sh --help
```

Key options:

```text
--prompt TEXT
--image PATH                 optional image-to-video source
--save-file PATH
--size '1280*704'            official TI2V-5B landscape size
--size '704*1280'            official TI2V-5B portrait size
--frame-num N
--steps N
--seed N
--guide-scale N
--vae-device cpu|cuda
--vae-dtype float32|bfloat16
--vae-conv3d-tile-h N
```

The wrapper already sets:

```bash
unset HSA_OVERRIDE_GFX_VERSION
export HF_XET_HIGH_PERFORMANCE=1
export MIOPEN_FIND_MODE=FAST
export MIOPEN_USER_DB_PATH=$HOME/.cache/miopen-wan22
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
export WAN22_VAE_DEVICE=cuda
export WAN22_VAE_DTYPE=bfloat16
export WAN22_VAE_CONV3D_TILE_H=44
```

It calls official `generate.py` with:

```bash
--task ti2v-5B
--ckpt_dir /home/chihmin/models/Wan2.2-TI2V-5B
--offload_model True
--convert_model_dtype
--t5_cpu
```

## Known-good visual test: cinematic realistic cat

Use this when the user wants a normal visible prompt, not just a kernel smoke test.

```bash
/home/chihmin/src/Wan2.2-deploy/wan22_cli.sh \
  --prompt 'A photorealistic orange tabby cat sitting on a cozy sunlit kitchen windowsill, warm cinematic morning light, detailed soft fur, bright natural colors, shallow depth of field, slow dolly-in camera, gentle tail movement, realistic film photography, 24 fps' \
  --size '1280*704' \
  --frame-num 25 \
  --steps 12 \
  --seed 424242 \
  --save-file /home/chihmin/generated/wan22/wan_cat_sunlit_25f_step12_gpuvae_tiled.mp4
```

Known result on this host:

- Total time: about `3:21`
- GPU VAE tiled decode: about `10.7s`
- Output: `/home/chihmin/generated/wan22/wan_cat_sunlit_25f_step12_gpuvae_tiled.mp4`
- Extracted frame brightness was normal: mean RGB around `[165, 155, 103]`

Attach output in Discord with:

```text
[[file: /home/chihmin/generated/wan22/wan_cat_sunlit_25f_step12_gpuvae_tiled.mp4]]
```

## Kernel/runtime smoke test vs visual-quality test

Do not judge visual quality from 1 sampling step.

- `--steps 1`: useful for kernel/runtime/profiling only; output can be near-black or unformed.
- `--steps 12`: short visual sanity test; usable for checking that content appears.
- More steps should improve quality but costs roughly linearly in denoise time.

Example 1-step 73-frame kernel test:

```bash
env WAN22_PROFILE=1 \
/home/chihmin/src/Wan2.2-deploy/wan22_cli.sh \
  --prompt 'A small red ball rolls across a wooden table, cinematic lighting, slow camera push-in' \
  --size '1280*704' \
  --frame-num 73 \
  --steps 1 \
  --seed 4242 \
  --save-file /home/chihmin/generated/wan22/wan_3s_73f_step1_gpuvae_tiled.mp4
```

Known result:

- Total: about `4:58`
- `vae.decode device=cuda`
- VAE decode: about `74.7s`
- No MIOpen crash

## Profiling

Enable high-level Wan stage timing:

```bash
WAN22_PROFILE=1 /home/chihmin/src/Wan2.2-deploy/wan22_cli.sh ...
```

Optional synchronized profiling, slower but more exact around GPU kernels:

```bash
WAN22_PROFILE=1 WAN22_PROFILE_SYNC=1 /home/chihmin/src/Wan2.2-deploy/wan22_cli.sh ...
```

Useful HIP/MIOpen debug envs:

```bash
AMD_SERIALIZE_KERNEL=3
HIP_LAUNCH_BLOCKING=1
TORCH_SHOW_CPP_STACKTRACES=1
MIOPEN_FIND_MODE=FAST
MIOPEN_USER_DB_PATH=/home/chihmin/.cache/miopen-wan22
```

Example debug wrapper:

```bash
rm -f /home/chihmin/generated/wan22/profile/wan_debug.*
/usr/bin/time -f 'ELAPSED=%E EXIT=%x' \
  -o /home/chihmin/generated/wan22/profile/wan_debug.time \
  timeout --kill-after=20s 900s \
  env WAN22_PROFILE=1 HIP_LAUNCH_BLOCKING=1 TORCH_SHOW_CPP_STACKTRACES=1 \
  /home/chihmin/src/Wan2.2-deploy/wan22_cli.sh \
    --prompt 'A photorealistic orange tabby cat sitting on a cozy sunlit kitchen windowsill, warm cinematic morning light, detailed soft fur, bright natural colors, shallow depth of field, slow dolly-in camera, gentle tail movement, realistic film photography, 24 fps' \
    --size '1280*704' \
    --frame-num 25 \
    --steps 12 \
    --seed 424242 \
    --save-file /home/chihmin/generated/wan22/debug_cat.mp4 \
  > /home/chihmin/generated/wan22/profile/wan_debug.stdout \
  2> /home/chihmin/generated/wan22/profile/wan_debug.stderr
```

Inspect profile lines:

```bash
grep -h 'WAN22_PROFILE\|Saving generated\|Finished\|Traceback\|MIOpen\|RuntimeError\|Error\|Exception' \
  /home/chihmin/generated/wan22/profile/wan_debug.stdout \
  /home/chihmin/generated/wan22/profile/wan_debug.stderr | tail -160
```

Check GPU/kernel logs after a failure:

```bash
journalctl -k --since '10 minutes ago' | grep -iE 'amdgpu|ring|timeout|oom|kfd|gpuvm|reset'
```

## ROCm profiler E2E bottleneck notes

`rocprofv3` and `rocprofv2` can abort during PyTorch import on this host:

```text
rocprofv3: api registration failed with error code 16: Configuration request occurred outside of valid rocprofiler configuration period
rocprofv2: terminate called without an active exception
```

The working profiler path is legacy `rocprof` with ROCm bin in `PATH` so postprocessing can find `rocminfo`:

```bash
OUTDIR=/home/chihmin/generated/wan22/rocprof/e2e_25f_step12_rocprof_manual
mkdir -p "$OUTDIR"
cd /home/chihmin/src/Wan2.2
/usr/bin/time -f 'ELAPSED=%e EXIT=%x MAXRSS_KB=%M' -o "$OUTDIR/time.txt" \
  timeout --kill-after=30s 1400s \
  env -u HSA_OVERRIDE_GFX_VERSION \
    PATH=/opt/rocm-7.2.2/bin:$PATH \
    WAN22_PROFILE=1 WAN22_PROFILE_SYNC=1 \
    WAN22_VAE_DEVICE=cuda WAN22_VAE_DTYPE=bfloat16 WAN22_VAE_CONV3D_TILE_H=44 \
    HF_XET_HIGH_PERFORMANCE=1 MIOPEN_FIND_MODE=FAST \
    MIOPEN_USER_DB_PATH=/home/chihmin/.cache/miopen-wan22 \
    TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 \
    /opt/rocm-7.2.2/bin/rocprof \
      --sys-trace --stats --timestamp on --basenames on \
      -d "$OUTDIR/data" -o "$OUTDIR/trace.csv" \
      /home/chihmin/src/Wan2.2/.venv-rocm72/bin/python /home/chihmin/src/Wan2.2/generate.py \
        --task ti2v-5B --size '1280*704' \
        --ckpt_dir /home/chihmin/models/Wan2.2-TI2V-5B \
        --prompt 'A photorealistic orange tabby cat sitting on a cozy sunlit kitchen windowsill, warm cinematic morning light, detailed soft fur, bright natural colors, shallow depth of field, slow dolly-in camera, gentle tail movement, realistic film photography, 24 fps' \
        --frame_num 25 --offload_model True --convert_model_dtype --t5_cpu \
        --save_file "$OUTDIR/wan_cat_sunlit_25f_step12_rocprof.mp4" \
        --base_seed 424242 --sample_steps 12 \
  > "$OUTDIR/stdout.txt" 2> "$OUTDIR/stderr.txt"
```

Known 25f/12step ROCm profiler run:

```text
/home/chihmin/generated/wan22/rocprof/e2e_25f_step12_rocprof_20260629_151944/
```

Stage timing from `WAN22_PROFILE_SYNC=1` in that run:

```text
pipeline_create -> load_t5:          22.503s
load_t5 -> load_vae:                  2.407s
load_vae -> load_dit:                 0.773s
t2v text encode:                      2.864s
model.to(device):                     1.004s
DiT denoise loop:                   123.988s
model.cpu:                            0.887s
VAE decode:                          41.707s
save video:                           0.943s
```

ROCm `trace.stats.csv` aggregate for 25f/12step:

```text
Total GPU kernel time:       158.328s
rocBLAS GEMM:                 77.318s  48.83%  calls=8283
Elementwise/cast/gate:        42.100s  26.59%  calls=62990
Flash attention:              20.185s  12.75%  calls=1440
MIOpen Conv3D im2col:         15.112s   9.54%  calls=763
Norm/reduction:                3.069s   1.94%  calls=5281
```

Timeline interpretation:

- Main DiT cluster: wall about `129.8s`, kernel sum about `129.2s`.
  - GEMM about `63.7s`
  - elementwise/cast/gate about `34.2s`
  - flash attention about `20.2s`
  - copies about `7.3s`
  - norm/reduce about `2.9s`
- VAE decode clusters: wall about `37s`, kernel sum about `36.6s`.
  - Conv3D im2col about `14.3s`
  - GEMM about `13.6s`
  - elementwise about `7.8s`

E2E bottleneck conclusion: for real visual runs (`12` steps), DiT denoising dominates wall time and GPU time; VAE is second. Within DiT, rocBLAS GEMM is the largest bucket, but the most suspicious inefficiency is still the large elementwise/cast/gate bucket and high kernel count, not attention.

## VAE microbenchmark and correctness checks

VAE Conv3D microbench:

```bash
/home/chihmin/src/Wan2.2/.venv-rocm72/bin/python \
  /home/chihmin/src/Wan2.2-deploy/wan22_vae_decode_microbench.py \
  --frames 25 --height 704 --width 1280 \
  --dtype bfloat16 --device cuda --chunk-output-height 44
```

Known result:

- `MICRO decode_done mode=official out=(3,25,704,1280)`
- Tiled bf16 GPU VAE: about `43.8s` in standalone microbench
- CPU VAE: about `220s`

Numeric correctness check for tiling:

```bash
/home/chihmin/src/Wan2.2/.venv-rocm72/bin/python \
  /home/chihmin/src/Wan2.2-deploy/wan22_conv3d_tiling_correctness.py
```

Known result:

```text
ALL_CORRECTNESS_CHECKS_PASSED
```

Covered checks:

- raw `F.conv3d`: tiled vs native
- `CausalConv3d.forward()`: with padding and cache path
- small Wan VAE decode: tile on vs tile off
- CPU fp32, CUDA fp32, CUDA bf16 where applicable

Example observed errors:

```text
raw_conv3d cuda fp32: max_abs <= 9.3e-06
raw_conv3d cuda bf16: max_abs <= 0.015625
causal_conv3d cuda bf16: max_abs = 0
vae_decode_small bf16 cuda tile_on_vs_off: max_abs = 0.0175781
```

## Checking whether a video is black/empty

If the user says the video has no visible content, verify with ffprobe + extracted frame statistics.

```bash
VID=/home/chihmin/generated/wan22/wan_cat_sunlit_25f_step12_gpuvae_tiled.mp4
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,nb_frames,duration,r_frame_rate,avg_frame_rate \
  -of default=nw=1 "$VID"

mkdir -p /home/chihmin/generated/wan22/inspect
ffmpeg -y -v error -i "$VID" \
  -vf 'select=eq(n\,0)+eq(n\,12)+eq(n\,24)' -vsync 0 \
  /home/chihmin/generated/wan22/inspect/frame_%03d.png

/home/chihmin/src/Wan2.2/.venv-rocm72/bin/python - <<'PY'
from PIL import Image, ImageStat
from pathlib import Path
for p in sorted(Path('/home/chihmin/generated/wan22/inspect').glob('*.png')):
    im = Image.open(p).convert('RGB')
    st = ImageStat.Stat(im)
    print(p.name, 'mean=', [round(x, 2) for x in st.mean], 'std=', [round(x, 2) for x in st.stddev], 'minmax=', im.getextrema())
PY
```

A previous 1-step night-cat video was genuinely near-black, with frame means around `[0.1, 3.5, 2.0]`. That was a sampling-steps/content issue, not a file/playback issue.

## qwen / llama-server co-residency guard

Multi-frame Wan can be destabilized if the local qwen llama-server is also resident on the GPU/GTT. The wrapper refuses multi-frame runs when qwen appears active unless overridden.

Service:

```bash
qwen-mtp.service
```

Stop qwen before Wan profiling/generation if needed:

```bash
sudo -n systemctl stop qwen-mtp.service
```

Override guard only if you intentionally accept risk:

```bash
WAN22_ALLOW_QWEN_CORESIDENT=1 /home/chihmin/src/Wan2.2-deploy/wan22_cli.sh ...
```

## DiT profiling and experimental optimization knobs

The 25f/12-step synchronized profile showed the DiT denoise loop is the main bottleneck:

- Total wall: about `203.61s`
- DiT denoise loop: about `124.23s` / `61%`
- GPU tiled VAE decode: about `41.65s` / `20.5%`
- Pre-t2v init/load: about `32.30s` / `15.9%`
- Average DiT model forward: about `5.16s`
- 12 steps = 24 DiT forwards because cond and uncond CFG are separate by default.

PyTorch trace for one 25f DiT step:

```text
/home/chihmin/generated/wan22/profile/dit_kernel_profile_step0/step0_cond.json
/home/chihmin/generated/wan22/profile/dit_kernel_profile_step0/step0_uncond.json
```

Approximate kernel mix per DiT forward:

```text
GEMM / Linear:              ~2.6s, 47-48%
elementwise / dtype / copy: ~1.4s, 25-26%
flash attention:            ~0.84s, 15-16%
copyBuffer:                 ~0.17s, 3%
norm/reduce:                ~0.12s, 2%
```

Experimental env knobs added for A/B only; do not enable by default unless intentionally testing:

```bash
WAN22_BATCH_CFG=1       # batch cond/uncond CFG into one DiT forward; measured ~3% E2E speedup on 25f/12step
WAN22_FAST_ROPE=1       # float32 real-valued RoPE; numerically close but not faster on this host
WAN22_FAST_NORM=1       # avoids explicit fp32 upcast in WanLayerNorm/WanRMSNorm; tiny speed change, RMSNorm differs by bf16-scale max_abs ~0.015625
WAN22_SDPA_NO_CONTIG=1  # skips explicit q/k/v .contiguous() before SDPA; small attention test bit-exact, no meaningful speedup measured
```

Measured 25f/1step synchronized timings after testing `WAN22_FAST_NORM` and `WAN22_SDPA_NO_CONTIG`:

```text
baseline:                    ELAPSED=87.71s, denoise loop done +14.367s
WAN22_FAST_NORM=1:           ELAPSED=87.87s, denoise loop done +14.320s
WAN22_SDPA_NO_CONTIG=1:      ELAPSED=87.68s, denoise loop done +14.364s
both:                        ELAPSED=87.61s, denoise loop done +14.309s
```

Conclusion: simple dtype/layout tweaks do not materially fix the DiT bottleneck. Real gains likely need fused norm/modulation/RoPE kernels, better SDPA layout integration, or a more invasive CFG/DiT execution rewrite.

## Source files changed in the local Wan clone

- `/home/chihmin/src/Wan2.2/wan/modules/model.py`
  - Adds `WAN22_FAST_ROPE` experiment for real-valued float32 RoPE.
  - Adds `WAN22_FAST_NORM` experiment for avoiding explicit norm fp32 upcast.
- `/home/chihmin/src/Wan2.2/wan/modules/attention.py`
  - Uses PyTorch `scaled_dot_product_attention` fallback when `flash_attn` is unavailable.
  - Adds `.contiguous()` around q/k/v for ROCm SDPA by default.
  - Adds `WAN22_SDPA_NO_CONTIG` experiment to skip explicit q/k/v `.contiguous()`.
- `/home/chihmin/src/Wan2.2/wan/__init__.py`
  - Lazy imports S2V/Animate classes so TI2V does not require S2V-only packages like `decord`, `librosa`, `peft`.
- `/home/chihmin/src/Wan2.2/wan/modules/vae2_2.py`
  - Casts padded tensors back to convolution weight dtype.
  - Adds optional output-height tiling for CUDA `Conv3D` via `WAN22_VAE_CONV3D_TILE_H`.
- `/home/chihmin/src/Wan2.2/wan/textimage2video.py`
  - Adds `WAN22_PROFILE` timing.
  - Adds `WAN22_TORCH_PROFILE_DIR` / `WAN22_TORCH_PROFILE_STEP` DiT forward trace export.
  - Adds `WAN22_BATCH_CFG` experiment for batched cond/uncond CFG.
  - Supports `WAN22_VAE_DEVICE` and `WAN22_VAE_DTYPE`.
- `/home/chihmin/src/Wan2.2/generate.py`
  - Has local profiling hooks used during debug.

## Gotchas

- Official TI2V-5B supports fixed sizes such as `1280*704` and `704*1280`; do not invent arbitrary 320p/1080p sizes for Wan official CLI tests.
- 1-step output can be black/unformed. Use 12+ steps for visual checks.
- If native GPU VAE crashes, do not assume OOM. Check profile lines and kernel logs; the proven local issue was large VAE MIOpen Conv3D launch failure.
- `WAN22_VAE_CONV3D_TILE_H=44` is the known-good default. Output-channel chunking was tested and is much slower; spatial height tiling is preferred.
- CPU VAE fallback works but is slow.
- Always attach the real output file in Discord via `[[file: /absolute/path.mp4]]` after confirming it exists.
