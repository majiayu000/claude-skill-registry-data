---
name: inference
description: |
  Fast inference with Unsloth and vLLM backend. Covers model loading, fast_generate(),
  thinking model output parsing, and memory management for efficient inference.
---

# Fast Inference

## Overview

Unsloth provides optimized inference through the vLLM backend, enabling 2x faster generation compared to standard HuggingFace inference. This skill covers fast inference setup, thinking model output parsing, and memory management.

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `fast_inference=True` | Enable vLLM backend for 2x speedup |
| `model.fast_generate()` | vLLM-accelerated generation |
| `SamplingParams` | Control generation (temperature, top_p, etc.) |
| `FastLanguageModel.for_inference()` | Merge LoRA adapters for inference |
| Token ID 151668 | `</think>` boundary for Qwen3-Thinking models |

## Critical Environment Setup

```python
import os
from dotenv import load_dotenv
load_dotenv()
```

## Critical Import Order

```python
# CRITICAL: Import unsloth FIRST for proper TRL patching
import unsloth
from unsloth import FastLanguageModel, is_bf16_supported

import torch
import vllm
from vllm import SamplingParams
```

## Environment Verification

Before inference, verify your environment is correctly configured:

```python
import unsloth
from unsloth import FastLanguageModel
import torch
import vllm

# Check versions
print(f"unsloth: {unsloth.__version__}")
print(f"vLLM: {vllm.__version__}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"CUDA version: {torch.version.cuda}")
```

## Standard Inference (No vLLM)

### Load Model

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-4B-Thinking-2507-unsloth-bnb-4bit",
    max_seq_length=1024,
    load_in_4bit=True,
)

# Prepare for inference (merges LoRA adapters if present)
FastLanguageModel.for_inference(model)
```

### Generate Response

```python
messages = [{"role": "user", "content": "What is machine learning?"}]
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

outputs = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.7,
    top_p=0.95,
    do_sample=True,
    pad_token_id=tokenizer.pad_token_id,
)

# Decode only new tokens
input_length = inputs["input_ids"].shape[1]
response = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
print(response)
```

## Fast Inference (vLLM Backend)

### Load Model with Fast Inference

```python
from unsloth import FastLanguageModel
from vllm import SamplingParams

MODEL_NAME = "unsloth/Qwen3-4B-Thinking-2507-unsloth-bnb-4bit"

model, tokenizer = FastLanguageModel.from_pretrained(
    MODEL_NAME,
    max_seq_length=1024,
    load_in_4bit=True,
    fast_inference=True,  # Enable vLLM backend
)
```

### Fast Generate

```python
FastLanguageModel.for_inference(model)

messages = [{"role": "user", "content": "What is 15 + 27? Show your thinking."}]
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

sampling_params = SamplingParams(
    temperature=0.6,      # Recommended for thinking models
    top_p=0.95,
    top_k=20,
    max_tokens=2048,      # Increased for thinking + response
)

# Use fast_generate instead of generate
outputs = model.fast_generate([prompt], sampling_params=sampling_params)

# Extract output
raw_output = outputs[0].outputs[0].text
output_token_ids = outputs[0].outputs[0].token_ids
print(raw_output)
```

### Sampling Parameters

```python
from vllm import SamplingParams

# Conservative (factual responses)
conservative = SamplingParams(
    temperature=0.3,
    top_p=0.9,
    max_tokens=512,
)

# Balanced (general use)
balanced = SamplingParams(
    temperature=0.6,
    top_p=0.95,
    top_k=20,
    max_tokens=1024,
)

# Creative (diverse outputs)
creative = SamplingParams(
    temperature=0.9,
    top_p=0.95,
    top_k=50,
    max_tokens=2048,
)

# Thinking models (allow long reasoning)
thinking = SamplingParams(
    temperature=0.6,
    top_p=0.95,
    top_k=20,
    max_tokens=2048,  # Extra space for <think> content
)
```

## Thinking Model Output Parsing

Qwen3-Thinking models use `<think>...</think>` tags to separate reasoning from final responses. Use token-based parsing for accuracy.

### Token-Based Parsing (Recommended)

```python
THINK_END_TOKEN_ID = 151668  # </think> token for Qwen3-Thinking models

def parse_thinking_response(token_ids, tokenizer):
    """
    Parse thinking model output using token ID boundary.

    With Thinking models + add_generation_prompt=True:
    - Template adds <think> to prompt
    - Model output starts with thinking content
    - Model outputs </think> (token 151668) when done
    - Final response follows </think>

    Args:
        token_ids: Output token IDs from generation
        tokenizer: Model tokenizer

    Returns:
        tuple: (thinking_content, response_content)
    """
    token_list = list(token_ids)

    if THINK_END_TOKEN_ID in token_list:
        end_idx = token_list.index(THINK_END_TOKEN_ID)
        thinking_tokens = token_list[:end_idx]
        response_tokens = token_list[end_idx + 1:]

        thinking = tokenizer.decode(thinking_tokens, skip_special_tokens=True).strip()
        response = tokenizer.decode(response_tokens, skip_special_tokens=True).strip()
    else:
        # No </think> found - model may still be thinking
        thinking = tokenizer.decode(token_list, skip_special_tokens=True).strip()
        response = "(Model did not complete thinking - increase max_tokens)"

    return thinking, response
```

### Usage Example

```python
# Generate with fast_inference
outputs = model.fast_generate([prompt], sampling_params=sampling_params)
output_token_ids = outputs[0].outputs[0].token_ids

# Parse thinking and response
thinking, response = parse_thinking_response(output_token_ids, tokenizer)

print("=== THINKING ===")
print(thinking)
print("\n=== RESPONSE ===")
print(response)
```

### Verification

```python
# Verify parsing worked correctly
think_tag_found = THINK_END_TOKEN_ID in list(output_token_ids)
has_thinking = bool(thinking) and "did not complete" not in response
has_response = bool(response) and "did not complete" not in response

print(f"</think> token found: {'Yes' if think_tag_found else 'No'}")
print(f"Thinking extracted: {'Yes' if has_thinking else 'No'}")
print(f"Response extracted: {'Yes' if has_response else 'No'}")

if not think_tag_found:
    print("Tip: Increase max_tokens in SamplingParams")
```

## Batch Inference

### Multiple Prompts

```python
prompts = [
    "What is recursion?",
    "Explain machine learning in simple terms.",
    "What is the difference between Python and JavaScript?",
]

# Format all prompts
formatted_prompts = [
    tokenizer.apply_chat_template(
        [{"role": "user", "content": p}],
        tokenize=False,
        add_generation_prompt=True
    )
    for p in prompts
]

# Batch generate (vLLM handles parallelization)
sampling_params = SamplingParams(temperature=0.6, max_tokens=512)
outputs = model.fast_generate(formatted_prompts, sampling_params=sampling_params)

# Process results
for i, output in enumerate(outputs):
    print(f"\n=== Prompt {i+1} ===")
    print(f"Q: {prompts[i]}")
    print(f"A: {output.outputs[0].text}")
```

## Memory Management

### GPU Memory Monitoring

```python
import subprocess

def measure_gpu_memory():
    """Measure current GPU memory usage in MB."""
    result = subprocess.run(
        ['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'],
        capture_output=True, text=True
    )
    return int(result.stdout.strip().split('\n')[0])

# Usage
print(f"GPU memory used: {measure_gpu_memory()} MB")
```

### Memory Cleanup

```python
import gc
import torch

def cleanup_memory():
    """Force garbage collection and clear CUDA cache."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

# Usage after inference
cleanup_memory()
print(f"GPU memory after cleanup: {measure_gpu_memory()} MB")
```

### Jupyter Kernel Shutdown (Critical for vLLM)

**vLLM does NOT release GPU memory within a Jupyter session.** Kernel restart is required between model tests:

```python
import IPython
print("Shutting down kernel to release GPU memory...")
app = IPython.Application.instance()
app.kernel.do_shutdown(restart=False)
```

**Important**: Always run this at the end of notebooks that use `fast_inference=True`. Without kernel shutdown, loading a different model will fail with OOM.

**Notebook pattern**: All finetuning notebooks end with a shutdown cell.

## Model Loading Patterns

### Pre-Quantized Models (Recommended)

```python
# Fast loading with pre-quantized models
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-4B-Thinking-2507-unsloth-bnb-4bit",  # Pre-quantized
    max_seq_length=1024,
    load_in_4bit=True,
    fast_inference=True,
)
```

### On-Demand Quantization

```python
# Quantize during loading (slower initial load)
model, tokenizer = FastLanguageModel.from_pretrained(
    "Qwen/Qwen3-4B-Thinking-2507",  # Full precision
    max_seq_length=1024,
    load_in_4bit=True,  # Quantize on load
    fast_inference=True,
)
```

### Post-Training Inference

```python
# After SFT/GRPO/DPO training
FastLanguageModel.for_inference(model)  # Merge LoRA adapters

# Then generate as normal
outputs = model.generate(**inputs, max_new_tokens=512)
```

## Supported Models

| Model | Path | Parameters | Use Case |
|-------|------|------------|----------|
| Qwen3-4B-Thinking | `unsloth/Qwen3-4B-Thinking-2507-unsloth-bnb-4bit` | 4B | Reasoning, chain-of-thought |
| Ministral-3B-Reasoning | `unsloth/Ministral-3-3B-Reasoning-2512` | 3B | Fast reasoning |
| Qwen3-4B | `unsloth/Qwen3-4B-unsloth-bnb-4bit` | 4B | General instruction following |
| Llama-3.2-3B | `unsloth/Llama-3.2-3B-Instruct-bnb-4bit` | 3B | General instruction following |

## Troubleshooting

### vLLM Not Available

**Symptom:** `fast_inference=True` fails or falls back to standard inference

**Fix:**
```python
# Check vLLM installation
import inspect
sig = inspect.signature(FastLanguageModel.from_pretrained)
if 'fast_inference' in sig.parameters:
    print("fast_inference parameter available")
else:
    print("vLLM not available - using standard inference")
```

### Out of Memory

**Symptom:** CUDA out of memory during inference

**Fix:**
- Use 4-bit quantization (`load_in_4bit=True`)
- Reduce `max_seq_length`
- Reduce `max_tokens` in SamplingParams
- Use `cleanup_memory()` between batches

### Incomplete Thinking

**Symptom:** `</think>` token not found in output

**Fix:**
- Increase `max_tokens` in SamplingParams (try 2048+)
- Check that model is a Thinking variant
- Verify `add_generation_prompt=True` in chat template

### GPU Memory Not Released

**Symptom:** Memory stays high after inference

**Fix:**
- Call `cleanup_memory()`
- Restart Jupyter kernel between model tests
- Use `del model` then `cleanup_memory()`

## When to Use This Skill

Use when:
- Running inference on fine-tuned models
- Need fast batch inference
- Working with thinking/reasoning models
- Optimizing inference latency
- Parsing chain-of-thought outputs

## Cross-References

- `bazzite-ai-jupyter:sft` - Supervised fine-tuning (train before inference)
- `bazzite-ai-jupyter:peft` - LoRA adapter loading
- `bazzite-ai-jupyter:quantization` - Quantization options
- `bazzite-ai-jupyter:transformers` - Transformer architecture background
- `bazzite-ai-ollama:api` - Ollama deployment for production
