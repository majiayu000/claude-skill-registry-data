---
name: repo-wan21
description: How to run Wan2.1 (Wan-Video/Wan2.1), Alibaba's open-source video foundation models for text-to-video, image-to-video, first-last-frame-to-video, VACE editing and text-to-image. Use when a user wants to self-host AI video generation, pick the 1.3B vs 14B model, or script generate.py.
---

# Wan2.1 (`Wan-Video/Wan2.1`)

Licence: Apache-2.0. Cloned shallow for review at `/home/user/wan-video/wan2.1` (re-clone with `git clone --depth 1 https://github.com/Wan-Video/Wan2.1` if the path is missing). Weights are not in the repo.

## What it is
Open suite of video models: T2V (1.3B and 14B), I2V-14B (480P/720P), FLF2V-14B (first and last frame), VACE (all-in-one creation/editing), plus Wan-VAE. Also integrated in ComfyUI and Diffusers. README claims the T2V-1.3B model needs about 8.19 GB VRAM and makes a 5-second 480P clip on an RTX 4090 in roughly 4 minutes.

## Setup
```bash
git clone https://github.com/Wan-Video/Wan2.1 && cd Wan2.1
pip install -r requirements.txt          # check INSTALL.md for torch/flash-attn pins
pip install "huggingface_hub[cli]"
huggingface-cli download Wan-AI/Wan2.1-T2V-1.3B --local-dir ./Wan2.1-T2V-1.3B
```

## Generate
```bash
# small GPU (480P)
python generate.py --task t2v-1.3B --size 832*480 --ckpt_dir ./Wan2.1-T2V-1.3B \
  --offload_model True --t5_cpu --sample_shift 8 --sample_guide_scale 6 --prompt "..."
# 720P text-to-video
python generate.py --task t2v-14B --size 1280*720 --ckpt_dir ./Wan2.1-T2V-14B --prompt "..."
# image-to-video
python generate.py --task i2v-14B --size 1280*720 --ckpt_dir ./Wan2.1-I2V-14B-720P --image in.jpg --prompt "..."
# first/last frame
python generate.py --task flf2v-14B --size 1280*720 --ckpt_dir ./Wan2.1-FLF2V-14B-720P --first_frame a.png --last_frame b.png --prompt "..."
```
Multi-GPU: `torchrun --nproc_per_node=8 generate.py ... --dit_fsdp --t5_fsdp --ulysses_size 8` (needs `xfuser>=0.4.1`). Prompt extension: `--use_prompt_extend` with a local Qwen model or DashScope (needs `DASH_API_KEY`).

## Guidance
- Pick 1.3B for a single consumer GPU, 14B only with large VRAM or multi-GPU.
- Prompt structure: `ai-video-image-prompt-structure`.
- Check the Hugging Face model card licence before commercial use; likeness and voice rules in `ai-video-generators` apply.

## Related
`ai-video-generators`, `repo-hunyuanvideo`, `repo-cogvideo`, `repo-pinokio` (one-click local launcher).
