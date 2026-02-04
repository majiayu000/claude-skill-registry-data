---
name: unsloth-finetuning
description: Fine-tune LLMs 2x faster with 80% less memory using Unsloth. Use when the user wants to fine-tune models like Llama, Mistral, Phi, or Gemma. Handles model loading, LoRA configuration, training, and model export.
---

# Unsloth Fine-Tuning

Expert guidance for fine-tuning Large Language Models using Unsloth's optimized library.

## Core Capabilities

- Load models with 4-bit quantization and gradient checkpointing
- Configure LoRA/QLoRA for efficient fine-tuning
- Train on custom or Hugging Face datasets
- Export models to GGUF, Ollama, vLLM, or Hugging Face formats
- Monitor training with progress tracking
- Optimize for different hardware configurations

## Quick Start

### 1. Load a Model

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-1B-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
    use_gradient_checkpointing="unsloth"
)
```

**Supported Models:**

- Llama 3.3 (70B), 3.2 (1B, 3B), 3.1 (8B)
- Mistral v0.3 (7B), Small Instruct
- Phi 3.5 mini, Phi 3 medium
- Gemma 2 (9B, 27B)
- Qwen 2.5 (7B)

### 2. Apply LoRA

```python
model = FastLanguageModel.get_peft_model(
    model,
    r=16,                    # LoRA rank (8-64)
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,          # Scaling factor
    use_gradient_checkpointing="unsloth",
    random_state=3407,
    max_seq_length=2048
)
```

### 3. Configure Training

```python
from trl import SFTTrainer, SFTConfig

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
    args=SFTConfig(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        max_steps=100,
        learning_rate=2e-4,
        logging_steps=1,
        output_dir="./output",
        optim="adamw_8bit",
        seed=3407
    )
)
```

### 4. Train

```python
trainer.train()
```

### 5. Export

```python
# GGUF format
model.save_pretrained_gguf(
    "model",
    tokenizer,
    quantization_method="q4_k_m"
)

# Hugging Face format
model.save_pretrained("./hf_model")
tokenizer.save_pretrained("./hf_model")
```

## Performance Optimization

### Memory Optimization

**Out of Memory? Try:**

1. Reduce `per_device_train_batch_size` to 1
2. Increase `gradient_accumulation_steps` to 8
3. Reduce `max_seq_length` to 1024
4. Use smaller model (1B instead of 3B)

### Speed Optimization

**Training too slow? Check:**

1. GPU is being used: `nvidia-smi`
2. Batch size isn't too small
3. Using `load_in_4bit=True`
4. Using `use_gradient_checkpointing="unsloth"`

### Quality Optimization

**Poor results? Adjust:**

1. Increase `max_steps` to 500-1000
2. Try learning rates: 1e-4, 2e-4, 5e-4
3. Increase dataset quality/size
4. Use larger model if resources allow

## Hardware Requirements

### Minimum (1B models)

- GPU: RTX 3060 (12GB VRAM)
- RAM: 16GB
- Training time: 20-40 min for 100 steps

### Recommended (3B-7B models)

- GPU: RTX 4090 or A100
- RAM: 32GB+
- Training time: 10-30 min for 100 steps

### Budget (Small experiments)

- GPU: RTX 3060 Ti (8GB)
- Use: Llama-1B or Phi-3-mini
- Reduce batch_size=1, max_seq_length=1024

## Common Patterns

### Pattern 1: Quick Prototype

```python
# Minimal setup for fast experimentation
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Llama-3.2-1B-bnb-4bit",
    max_seq_length=1024,    # Shorter for speed
    load_in_4bit=True
)

model = FastLanguageModel.get_peft_model(model, r=8)  # Lower rank

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
    args=SFTConfig(
        per_device_train_batch_size=2,
        max_steps=50,        # Few steps
        learning_rate=2e-4,
        output_dir="./quick_test"
    )
)
```

### Pattern 2: Production Quality

```python
# Full setup for best results
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Llama-3.1-8B-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
    use_gradient_checkpointing="unsloth"
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,                   # Standard rank
    lora_alpha=16,
    use_gradient_checkpointing="unsloth"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
    args=SFTConfig(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        max_steps=500,       # More steps
        learning_rate=2e-4,
        warmup_steps=10,
        logging_steps=10,
        save_steps=100,
        output_dir="./production_model"
    )
)
```

### Pattern 3: Large Model (70B)

```python
# Special settings for very large models
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Llama-3.3-70B-Instruct-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
    use_gradient_checkpointing="unsloth"
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Fewer targets
    use_gradient_checkpointing="unsloth"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
    args=SFTConfig(
        per_device_train_batch_size=1,    # Must be 1
        gradient_accumulation_steps=8,    # Compensate
        max_steps=200,
        learning_rate=1e-4,               # Lower LR
        output_dir="./large_model"
    )
)
```

## Troubleshooting

### Error: "CUDA out of memory"

**Solution:**

```python
# Reduce memory usage
batch_size = 1
max_seq_length = 1024
gradient_accumulation_steps = 8
# Or use smaller model
```

### Error: "Model not found"

**Solution:**

- Check model name spelling
- Verify internet connection
- Try with Hugging Face token: `export HF_TOKEN=your_token`

### Error: "Training loss not decreasing"

**Solution:**

```python
# Adjust hyperparameters
learning_rate = 5e-4  # Try higher
max_steps = 500       # Train longer
# Or check dataset quality
```

## Best Practices

1. **Always use 4-bit quantization** unless you have >80GB VRAM
2. **Start with small models** (1B) for experimentation
3. **Monitor GPU usage** with `nvidia-smi`
4. **Save checkpoints** every 100 steps
5. **Validate on test set** before exporting
6. **Use appropriate LoRA rank**: 8 for experiments, 16 for production, 32 for complex tasks

## Dataset Format

Unsloth works with Hugging Face datasets. Example format:

```json
{
  "text": "### Instruction: Explain quantum computing\n### Response: Quantum computing uses quantum bits..."
}
```

Or instruction format:

```json
{
  "instruction": "Explain quantum computing",
  "input": "",
  "output": "Quantum computing uses quantum bits..."
}
```

## Performance Benchmarks

| Model         | VRAM  | Speed (vs standard) | Memory Reduction |
| ------------- | ----- | ------------------- | ---------------- |
| Llama 3.2 1B  | ~2GB  | 2x faster           | 80% less         |
| Llama 3.2 3B  | ~4GB  | 2x faster           | 75% less         |
| Llama 3.1 8B  | ~6GB  | 2x faster           | 70% less         |
| Llama 3.3 70B | ~40GB | 2x faster           | 75% less         |

## Additional Resources

For more advanced topics, see:

- [ADVANCED.md](ADVANCED.md) - Multi-GPU, custom optimizers, advanced LoRA
- [DATASETS.md](DATASETS.md) - Dataset preparation and formatting
- [EXPORT.md](EXPORT.md) - Detailed export options and formats

## Version Compatibility

- Python: 3.10, 3.11, 3.12 (not 3.13)
- CUDA: 11.8 or 12.1+
- PyTorch: 2.0+
- Transformers: 4.37+
