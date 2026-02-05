---
name: peft
description: |
  Parameter-efficient fine-tuning with LoRA and Unsloth. Covers LoraConfig,
  target module selection, QLoRA for 4-bit training, adapter merging, and
  Unsloth optimizations for 2x faster training.
---

# Parameter-Efficient Fine-Tuning (PEFT)

## Overview

PEFT methods like LoRA train only a small number of adapter parameters instead of the full model, reducing memory by 10-100x while maintaining quality.

## Quick Reference

| Method | Memory | Speed | Quality |
|--------|--------|-------|---------|
| Full Fine-tune | High | Slow | Best |
| LoRA | Low | Fast | Very Good |
| QLoRA | Very Low | Fast | Good |
| Unsloth | Very Low | 2x Faster | Good |

## LoRA Concepts

### How LoRA Works

```
Original weight matrix W (frozen):     d x k
LoRA adapters A and B:                 d x r, r x k (where r << min(d,k))

Forward pass:
  output = x @ W + x @ A @ B * (alpha / r)

Trainable params: 2 * r * d  (instead of d * k)
```

### Memory Savings

```python
def lora_savings(d, k, r):
    original = d * k
    lora = 2 * r * max(d, k)
    reduction = (1 - lora / original) * 100
    return reduction

# Example: 4096 x 4096 matrix with rank 8
print(f"Memory reduction: {lora_savings(4096, 4096, 8):.1f}%")
# Output: ~99.6% reduction
```

## Basic LoRA Setup

### Configure LoRA

```python
from peft import LoraConfig, get_peft_model, TaskType

lora_config = LoraConfig(
    r=8,                          # Rank (capacity)
    lora_alpha=16,                # Scaling factor
    target_modules=["q_proj", "v_proj"],  # Which layers
    lora_dropout=0.05,            # Regularization
    bias="none",                  # Don't train biases
    task_type=TaskType.CAUSAL_LM  # Task type
)
```

### Apply to Model

```python
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto"
)

model = get_peft_model(model, lora_config)

# Check trainable parameters
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 1,100,048,384 || trainable%: 0.38%
```

## LoRA Parameters

### Key Parameters

| Parameter | Values | Effect |
|-----------|--------|--------|
| `r` | 4, 8, 16, 32 | Adapter capacity |
| `lora_alpha` | r to 2*r | Scaling (higher = stronger) |
| `target_modules` | List | Which layers to adapt |
| `lora_dropout` | 0.0-0.1 | Regularization |

### Target Modules

```python
# Common target modules for different models

# LLaMA / Mistral / TinyLlama
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]

# GPT-2
target_modules = ["c_attn", "c_proj"]

# BLOOM
target_modules = ["query_key_value", "dense"]

# All linear layers (most aggressive)
target_modules = "all-linear"
```

### Rank Selection Guide

| Rank (r) | Use Case |
|----------|----------|
| 4 | Simple tasks, small datasets |
| 8 | General purpose (recommended) |
| 16 | Complex tasks, more capacity |
| 32+ | Near full fine-tune quality |

## QLoRA (Quantized LoRA)

### Setup

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

# 4-bit quantization config
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    quantization_config=quantization_config,
    device_map="auto"
)

# Prepare for k-bit training (important!)
model = prepare_model_for_kbit_training(model)

# Add LoRA adapters
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

## Training with PEFT

### Using SFTTrainer

```python
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

dataset = load_dataset("timdettmers/openassistant-guanaco")

sft_config = SFTConfig(
    output_dir="./lora_checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-4,  # Higher LR for LoRA
    logging_steps=10,
    save_steps=500,
    max_seq_length=512,
    gradient_accumulation_steps=4,
)

trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
    dataset_text_field="text",
    peft_config=lora_config,  # Pass LoRA config
)

trainer.train()
```

## Unsloth (2x Faster Training)

### Setup

```python
from unsloth import FastLanguageModel

# Load model with Unsloth optimizations
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/tinyllama-chat-bnb-4bit",  # Pre-quantized
    max_seq_length=2048,
    dtype=None,  # Auto-detect
    load_in_4bit=True,
)

# Add LoRA with Unsloth
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing=True,
    random_state=42,
)
```

### Train with Unsloth

```python
from trl import SFTTrainer, SFTConfig

sft_config = SFTConfig(
    output_dir="./unsloth_output",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=5,
    max_steps=100,
    learning_rate=2e-4,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    logging_steps=1,
    optim="adamw_8bit",  # Memory-efficient optimizer
    weight_decay=0.01,
    lr_scheduler_type="linear",
    seed=42,
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=sft_config,
)

trainer.train()
```

## Save and Load Adapters

### Save Adapters Only

```python
# Save just the LoRA weights (small!)
model.save_pretrained("./lora_adapters")
```

### Load Adapters

```python
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto"
)

model = PeftModel.from_pretrained(base_model, "./lora_adapters")
```

### Merge Adapters into Base Model

```python
# Merge LoRA weights into base model (for deployment)
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("./merged_model")
```

## Inference with Adapters

```python
from peft import PeftModel

# Load base + adapters
base_model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
model = PeftModel.from_pretrained(base_model, "./lora_adapters")

# Generate
model.eval()
inputs = tokenizer("What is Python?", return_tensors="pt")

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=100)

print(tokenizer.decode(outputs[0]))
```

## Multi-Adapter Hot-Swapping

Train task-specific adapters and swap them at inference time without reloading the base model.

### Train Multiple Adapters

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig

TASK_DATASETS = {
    "technical": technical_data,   # Precise, factual responses
    "creative": creative_data,     # Imaginative, expressive responses
    "code": code_data,             # Code-focused analysis
}

for task_name, task_data in TASK_DATASETS.items():
    # Load fresh model
    model, tokenizer = FastLanguageModel.from_pretrained(
        "unsloth/Qwen3-4B-Thinking-2507-unsloth-bnb-4bit",
        max_seq_length=512,
        load_in_4bit=True,
    )

    # Apply LoRA
    model = FastLanguageModel.get_peft_model(
        model, r=16, lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    )

    # Train on task-specific data
    trainer = SFTTrainer(model=model, train_dataset=task_data, ...)
    trainer.train()

    # Save lightweight adapter (~130MB each)
    model.save_pretrained(f"./adapters/{task_name}")
```

### Hot-Swap at Inference

```python
from peft import PeftModel
from unsloth import FastLanguageModel

# Load base model ONCE
base_model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-4B-Thinking-2507-unsloth-bnb-4bit",
    max_seq_length=512,
    load_in_4bit=True,
)

def load_and_generate(adapter_path, prompt):
    """Load adapter and generate response."""
    # Hot-swap adapter onto base model
    adapted_model = PeftModel.from_pretrained(base_model, adapter_path)
    FastLanguageModel.for_inference(adapted_model)

    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    ).to(adapted_model.device)

    outputs = adapted_model.generate(input_ids=inputs, max_new_tokens=128)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Use different adapters for different tasks
technical_response = load_and_generate("./adapters/technical", "Explain TCP vs UDP")
creative_response = load_and_generate("./adapters/creative", "Write a haiku about coding")
code_response = load_and_generate("./adapters/code", "Explain Python decorators")
```

### Adapter Storage Efficiency

| Component | Size |
|-----------|------|
| Base model (4-bit) | ~8GB |
| Each adapter | ~130MB |
| 10 adapters total | ~1.3GB |

**Multi-adapter approach**: 8GB + 1.3GB = 9.3GB total
**vs 10 full models**: 80GB total

## Comparison: Full vs LoRA vs QLoRA

| Aspect | Full Fine-tune | LoRA | QLoRA |
|--------|----------------|------|-------|
| Trainable % | 100% | ~0.1-1% | ~0.1-1% |
| Memory | 4x model | ~1.2x model | ~0.5x model |
| Training speed | Slow | Fast | Fast |
| Quality | Best | Very Good | Good |
| 7B model | 28GB+ | ~16GB | ~6GB |

## Troubleshooting

### Out of Memory

**Fix:**

```python
# Use gradient checkpointing
model.gradient_checkpointing_enable()

# Use smaller batch with accumulation
per_device_train_batch_size=1
gradient_accumulation_steps=8
```

### Poor Quality

**Fix:**

- Increase `r` (rank)
- Add more target modules
- Train longer
- Check data quality

### NaN Loss

**Fix:**

- Lower learning rate
- Use gradient clipping
- Check for data issues

## When to Use This Skill

Use when:

- GPU memory is limited
- Fine-tuning large models (7B+)
- Need fast training iterations
- Want to swap adapters for different tasks

## Cross-References

- `bazzite-ai-jupyter:qlora` - Advanced QLoRA experiments (alpha, rank, modules)
- `bazzite-ai-jupyter:finetuning` - Full fine-tuning basics
- `bazzite-ai-jupyter:quantization` - Quantization for QLoRA
- `bazzite-ai-jupyter:sft` - SFT training with LoRA
- `bazzite-ai-jupyter:inference` - Fast inference with adapters
- `bazzite-ai-jupyter:transformers` - Target module selection
