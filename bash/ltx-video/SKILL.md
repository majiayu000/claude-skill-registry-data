---
name: ltx-video
category: video
description: >
  Set up, configure, and run LTX-2/LTX-2.3 (Lightricks) for AI video and audio generation.
  Use when: (1) Installing LTX-2 locally or via ComfyUI, (2) Generating video from text, image,
  audio, or keyframes, (3) Running inference with the 22B dev/distilled models, (4) Fine-tuning
  with LoRA/IC-LoRA, (5) Configuring upscalers (spatial/temporal), (6) Optimizing VRAM usage
  (FP8, quantization, low-VRAM modes), (7) Building content-generation pipelines with LTX-2,
  (8) Writing prompts for video generation, (9) Integrating LTX-2 into ComfyUI workflows.
  Triggers on: ltx, ltx-video, ltx-2, lightricks video, text-to-video generation, video diffusion model.
---

# LTX-2 Video Generation

LTX-2.3 is the first DiT-based audio-video foundation model — 22B parameters, synchronized
audio+video, real-time capable. Developed by Lightricks.

- **Paper:** arXiv:2601.03233
- **Repo:** https://github.com/Lightricks/LTX-2
- **Models:** https://huggingface.co/Lightricks/LTX-2.3
- **ComfyUI:** https://github.com/Lightricks/ComfyUI-LTXVideo

## Quick Setup

```bash
# Clone and install (requires Python >=3.12, CUDA >12.7, uv)
git clone https://github.com/Lightricks/LTX-2.git
cd LTX-2
uv sync --frozen
source .venv/bin/activate
```

Or run `scripts/setup-ltx.sh` for automated setup with model downloads.

## Model Selection

| Model | Steps | Speed | Quality | Min VRAM |
|-------|-------|-------|---------|----------|
| `ltx-2.3-22b-dev` | 40 | Baseline | Highest | 24 GB |
| `ltx-2.3-22b-distilled` | 8 | ~3x faster | Very good | 16 GB |
| `ltx-2.3-22b-distilled` + FP8 | 8 | ~3x faster | Very good | 12 GB |

**Supporting models (download alongside):**
- `ltx-2.3-spatial-upscaler-x2-1.1` — 2x resolution enhancement
- `ltx-2.3-spatial-upscaler-x1.5-1.0` — 1.5x resolution (less VRAM)
- `ltx-2.3-temporal-upscaler-x2-1.0` — doubles FPS (smoother motion)
- `ltx-2.3-22b-distilled-lora-384` — distilled LoRA for dev model
- Gemma 3 text encoder (12B) — required for all pipelines

## Pipelines

Choose based on use case:

| Pipeline | Use Case | Notes |
|----------|----------|-------|
| `TI2VidTwoStagesPipeline` | **Default production** — text/image to video | 2x spatial upsampling, best quality |
| `TI2VidTwoStagesHQPipeline` | Higher quality, fewer steps needed | Second-order sampling |
| `TI2VidOneStagePipeline` | Quick prototyping | Lower res, faster |
| `DistilledPipeline` | Fastest inference | 8 fixed steps, CFG=1 |
| `ICLoraPipeline` | Video/image transformations | Style transfer, control |
| `KeyframeInterpolationPipeline` | Animate between keyframes | Start/end frame interpolation |
| `A2VidPipelineTwoStage` | Audio-conditioned video | Synced audio+video |
| `RetakePipeline` | Regenerate video regions | Selective re-generation |

## Running Inference

### CLI

```bash
# Text-to-video (recommended two-stage pipeline)
python -m ltx_pipelines.run \
  --config configs/ltx-2.3-22b-dev-2stage.yaml \
  --prompt "A golden retriever running through autumn leaves in a park" \
  --height 704 --width 1216 \
  --num_frames 97 \
  --output output.mp4

# Image-to-video
python -m ltx_pipelines.run \
  --config configs/ltx-2.3-22b-dev-2stage.yaml \
  --prompt "The scene comes alive with motion..." \
  --conditioning_image path/to/image.png \
  --height 704 --width 1216 \
  --num_frames 97 \
  --output output.mp4

# Distilled (fast mode)
python -m ltx_pipelines.run \
  --config configs/ltx-2.3-22b-distilled-2stage.yaml \
  --prompt "..." \
  --output output.mp4

# FP8 quantization for lower VRAM
python -m ltx_pipelines.run \
  --config configs/ltx-2.3-22b-dev-2stage.yaml \
  --quantization fp8-cast \
  --prompt "..." \
  --output output.mp4
```

### Python API

```python
from ltx_video.inference import infer, InferenceConfig

infer(InferenceConfig(
    pipeline_config="configs/ltx-2.3-22b-dev-2stage.yaml",
    prompt="A cinematic shot of ocean waves crashing on volcanic rocks at sunset",
    height=704,
    width=1216,
    num_frames=97,
    output_path="output.mp4",
    enhance_prompt=True,  # auto-enhance with Gemma 3
))
```

## Resolution & Frame Rules

- **Width/height:** must be divisible by 32 (e.g., 480x832, 704x1216, 768x512)
- **Frame count:** must be `8n + 1` (e.g., 33, 65, 97, 129, 257)
- **Default:** 1216x704 at 30 FPS
- **Max frames:** 1,441 (long-form with distilled models)
- **FPS:** 1-60, default 24-30

## Prompting

Write detailed, chronological scene descriptions in ~200 words. Include:
- Main action and specific movements
- Character/object appearance details
- Environment and setting
- Camera angle and movement
- Lighting and atmosphere
- Notable transitions or changes

Use `enhance_prompt=True` for automatic prompt elaboration.

See `references/prompting-guide.md` for advanced techniques and examples.

## VRAM Optimization

| Technique | Savings | Flag/Config |
|-----------|---------|-------------|
| FP8 quantization | ~40% | `--quantization fp8-cast` |
| FP8 scaled (Hopper GPUs) | ~45% | `--quantization fp8-scaled-mm` |
| Single-stage pipeline | ~30% | Use `OneStagePipeline` config |
| Distilled model | Fewer steps = less peak VRAM | Use distilled config |
| xFormers attention | ~15% | Install xformers, auto-detected |
| Flash Attention 3 | ~20% | Hopper GPUs, auto-detected |
| Gradient estimation | Reduce steps 40 to 20 | `--gradient_estimation` |

## Apple Silicon (MLX)

LTX-2 runs on Apple Silicon via MLX-native ports or the MPS PyTorch backend. Q4 quantized
models fit on 24 GB machines; full precision needs 64 GB+. Pin PyTorch to 2.4.1 for MPS
(2.5+ has Conv3d regression). See `references/apple-silicon.md` for setup, patches, and memory tables.

## Cloud API

Use hosted APIs when local hardware is insufficient: LTX API ($0.04-0.08/sec, official),
fal.ai (~$0.20/video), or Replicate (~$0.10/run). For self-hosted cloud, RunPod H100 runs
at ~$2.49/hr and Vast.ai from ~$0.50/hr. See `references/cloud-api.md` for Python examples and cost comparison.

## Low-VRAM CUDA (12 GB)

Run LTX-2 on 12 GB GPUs (RTX 4070, 3060 12GB) by combining three techniques:

1. **FP8 quantization** (`--quantization fp8-cast`) -- reduces model memory ~40%
2. **Distilled model** (`ltx-2.3-22b-distilled`) -- 8 fixed steps instead of 40, lower peak VRAM
3. **Single-stage pipeline** (`TI2VidOneStagePipeline` or `DistilledPipeline`) -- avoids loading the spatial upscaler

```bash
python -m ltx_pipelines.run \
  --config configs/ltx-2.3-22b-distilled-1stage.yaml \
  --quantization fp8-cast \
  --prompt "A cat sitting on a windowsill watching rain" \
  --height 480 --width 832 \
  --num_frames 33 \
  --output output.mp4
```

At 480x832 with 33 frames, this fits comfortably in 12 GB. Increase resolution or frame
count only if monitoring shows headroom. Adding xFormers (`pip install xformers`) saves
another ~15% VRAM when available.

## LoRA & Fine-Tuning

Train custom LoRAs in <1 hour for motion, style, or likeness:

```bash
# See packages/ltx-trainer/README.md for full training guide
cd packages/ltx-trainer
python train.py --config configs/lora_training.yaml \
  --data_dir /path/to/videos \
  --output_dir /path/to/output
```

**Specialized control LoRAs available:**
- Union IC-LoRA (depth + Canny edge)
- Motion tracking, Detailer, Pose control, Camera movement LoRAs

## ComfyUI Integration

See `references/comfyui-setup.md` for full ComfyUI workflow setup.

Quick start: ComfyUI Manager → Install Custom Nodes → search "LTXVideo" → Install.
Requires: CUDA GPU with 32GB+ VRAM, 100GB+ disk space.

## Troubleshooting

- **CUDA OOM:** Add `--quantization fp8-cast`, use distilled model, or reduce resolution
- **Slow generation:** Use distilled pipeline (8 steps vs 40), enable xFormers
- **Poor quality:** Write longer prompts (~200 words), enable `enhance_prompt`, use two-stage pipeline
- **Audio issues:** Audio quality lower without speech; provide audio conditioning when possible
- **Frame count error:** Ensure frames = 8n+1 (33, 65, 97, 129...)
- **Resolution error:** Ensure width/height divisible by 32
