---
name: hf-job-submit
description: Submit training jobs to Hugging Face cloud GPUs
---

# HF Job Submit

Submit a Python training script to run on Hugging Face's cloud GPU infrastructure.

## How to Use

```bash
$CLAUDE_CONFIG_DIR/skills/hf-job-submit/scripts/hf-job-submit.sh <script_path> <hardware> <packages>
```

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `script_path` | Path to Python training script | `/home/user/workspace/train.py` |
| `hardware` | GPU hardware type | `t4-small`, `a10g-large` |
| `packages` | Space-separated pip packages | `"trl transformers datasets"` |

## Hardware Options

| Type | GPU | VRAM | Best For |
|------|-----|------|----------|
| `t4-small` | T4 | 16GB | Models < 1B |
| `t4-medium` | T4 | 16GB | Models 1-3B |
| `a10g-small` | A10G | 24GB | Models 1-3B |
| `a10g-large` | A10G | 24GB | Models 3-7B (LoRA) |
| `a100-large` | A100 | 40GB | Models 3-7B (LoRA) |

## Prerequisites

- `HF_TOKEN` environment variable must be set
- Hugging Face Pro or Team account with GPU Jobs access

## Output

Returns the Job ID on success, which can be used with `hf-job-status` and `hf-job-logs`.

## Example

```bash
$CLAUDE_CONFIG_DIR/skills/hf-job-submit/scripts/hf-job-submit.sh \
  "/home/user/workspace/train.py" \
  "t4-small" \
  "trl transformers datasets peft accelerate"
```
