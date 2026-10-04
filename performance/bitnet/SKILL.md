---
name: bitnet
category: models
description: "Microsoft BitNet — 1-bit LLM setup, inference, and benchmarking on CPU. Automates the full workflow: clone bitnet.cpp, create conda env, download GGUF models from HuggingFace, build optimized ternary kernels, and run inference. Supports official Microsoft models (2B) and community models (0.7B-10B). Use when: (1) setting up BitNet/bitnet.cpp for local CPU inference, (2) downloading and running 1-bit/ternary LLMs, (3) benchmarking BitNet vs full-precision models, (4) building edge/agentic inference pipelines without GPU, (5) converting HuggingFace models to GGUF for bitnet.cpp. Triggers on: 'bitnet', '1-bit llm', '1.58-bit', 'ternary model', 'ternary weights', 'edge inference', 'cpu inference', 'bitnet.cpp', 'bitlinear', 'no gpu inference'."
---

# BitNet — 1-Bit LLM Operations

Set up and run Microsoft's BitNet (1.58-bit ternary LLMs) for efficient CPU inference. Models use weights of {-1, 0, +1} — no GPU required.

## Quick Start

```bash
# Full setup in 5 commands
./scripts/install-bitnet.sh
./scripts/download-model.sh microsoft/BitNet-b1.58-2B-4T-gguf
./scripts/build-bitnet.sh
./scripts/run-inference.sh -p "You are a helpful assistant" -cnv
```

Or manually:

```bash
git clone --recursive https://github.com/microsoft/BitNet.git ~/BitNet
cd ~/BitNet
conda create -n bitnet-cpp python=3.9 -y && conda activate bitnet-cpp
pip install -r requirements.txt
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
python run_inference.py -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf -p "Hello" -n 128
```

## Prerequisites

| Tool | Install | Required |
|------|---------|----------|
| Python 3.9+ | `brew install python@3.9` or conda | Yes |
| CMake 3.22+ | `brew install cmake` | Yes |
| Clang 18+ | `brew install llvm` | Yes |
| conda | `brew install --cask miniconda` | Yes |
| huggingface-cli | `pip install huggingface-hub` | Yes |

## Operations

### Install BitNet

```bash
./scripts/install-bitnet.sh [--dir ~/BitNet]
```

Clones the BitNet repo, creates `bitnet-cpp` conda environment, installs Python dependencies.

### Download a Model

```bash
./scripts/download-model.sh <model-id> [--dir ~/BitNet]
```

Downloads a GGUF model from HuggingFace into the BitNet models directory.

**Recommended models** (see [references/models.md](references/models.md) for full catalog):

| Model | Params | Memory | Quality | Best For |
|-------|--------|--------|---------|----------|
| `microsoft/BitNet-b1.58-2B-4T-gguf` | 2B | 0.4 GB | Good | Default, edge agents |
| `1bitLLM/bitnet_b1_58-3B` | 3.3B | 0.7 GB | Better | General use |
| `HF1BitLLM/Llama3-8B-1.58-100B-tokens` | 8B | 1.6 GB | Best | Quality-focused |

### Build for Your CPU

```bash
./scripts/build-bitnet.sh [--dir ~/BitNet] [--model-dir models/BitNet-b1.58-2B-4T]
```

Compiles bitnet.cpp with optimized LUT kernels for the local CPU architecture (ARM NEON/DOTPROD or x86 AVX2).

### Run Inference

```bash
# Chat mode
./scripts/run-inference.sh -p "You are a helpful assistant" -cnv

# Single prompt
./scripts/run-inference.sh -p "Explain ternary quantization" -n 256

# Custom model
./scripts/run-inference.sh --model models/custom/ggml-model-i2_s.gguf -p "Hello"
```

Key flags: `-cnv` (chat mode), `-n N` (max tokens), `-t N` (threads), `-temp F` (temperature), `-c N` (context size, max 4096).

### Benchmark

```bash
./scripts/benchmark.sh [--dir ~/BitNet]
```

Runs throughput and latency benchmarks, reports tokens/sec and energy per token.

### Convert HuggingFace Models to GGUF

For models in safetensors/BF16 format:

```bash
cd ~/BitNet
huggingface-cli download microsoft/bitnet-b1.58-2B-4T-bf16 --local-dir models/bf16
python utils/convert-helper-bitnet.py models/bf16
```

### HuggingFace Transformers (No Speed Benefit)

For prototyping only — no ternary kernel optimization:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/bitnet-b1.58-2B-4T", torch_dtype=torch.bfloat16
)
tokenizer = AutoTokenizer.from_pretrained("microsoft/bitnet-b1.58-2B-4T")

messages = [{"role": "user", "content": "What are ternary weights?"}]
inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
output = model.generate(inputs, max_new_tokens=200)
print(tokenizer.decode(output[0][inputs.shape[-1]:], skip_special_tokens=True))
```

## Performance Reference

| Metric | BitNet 2B | LLaMA 3.2 1B | Qwen2.5 1.5B |
|--------|-----------|-------------|-------------|
| Memory | **0.4 GB** | 2.0 GB | 2.6 GB |
| Decode latency | **29 ms** | 48 ms | 65 ms |
| Energy/token | **0.028 J** | 0.258 J | 0.347 J |
| ARC-Challenge | **49.91** | 38.40 | 46.33 |
| GSM8K | **58.38** | 28.05 | 55.50 |

CPU speedups via bitnet.cpp: ARM 1.37-5.07x, x86 2.37-6.17x.

## Agentic Use Cases

**Dual-model architecture**: Use BitNet as the fast local brain (29ms/step) for tool selection, routing, and guard rails. Escalate complex reasoning to a cloud LLM.

**Agent swarm**: 10 BitNet 2B agents = ~4 GB total RAM. No API costs, no rate limits, works offline.

**Edge deployment**: Raspberry Pi, air-gapped environments, continuous monitoring agents.

## Limitations

- 4,096 token context limit
- Research-stage only (Microsoft's disclaimer)
- Fine-tuning requires native ternary training (can't quantize existing models)
- GPU support limited to NVIDIA A100
- One official model (2B); community models vary in quality
