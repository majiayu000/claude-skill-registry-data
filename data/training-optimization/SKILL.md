---
name: training-optimization
description: Advanced techniques for optimizing LLM fine-tuning. Covers learning rates, LoRA configuration, batch sizes, gradient strategies, hyperparameter tuning, and monitoring. Use when fine-tuning models for best performance.
---

# Training Optimization

Master advanced techniques for efficient, high-quality LLM fine-tuning.

## Overview

Fine-tuning is an art. Optimize:

- **Learning rates** - Schedulers, warmup, optimal values
- **LoRA configuration** - Rank, alpha, target modules
- **Batch optimization** - Size, accumulation, sequence length
- **Precision** - FP16, BF16, mixed precision
- **Gradient strategies** - Checkpointing, clipping, accumulation
- **Hyperparameter tuning** - Grid search, Bayesian optimization
- **Monitoring** - WandB, TensorBoard, loss curves
- **Quality** - Prevent overfitting, improve convergence

## Quick Start

### Optimal Default Configuration

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments

# Load model
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Llama-3.2-7B-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
    use_gradient_checkpointing="unsloth"  # Memory efficient
)

# Configure LoRA (optimal defaults)
model = FastLanguageModel.get_peft_model(
    model,
    r=16,                    # LoRA rank (8-64)
    lora_alpha=16,          # Alpha = rank typically works well
    lora_dropout=0,         # 0 for Unsloth (already efficient)
    target_modules=[        # All attention + MLP for best quality
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    bias="none",
    use_gradient_checkpointing="unsloth"
)

# Training arguments (optimal defaults)
training_args = TrainingArguments(
    output_dir="./outputs",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,        # Effective batch = 2*4 = 8
    num_train_epochs=3,
    learning_rate=2e-4,                   # 2e-4 is a sweet spot
    lr_scheduler_type="cosine",           # Cosine decay
    warmup_ratio=0.03,                    # 3% warmup
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),  # BF16 if available
    logging_steps=10,
    optim="adamw_8bit",                   # 8-bit AdamW (memory efficient)
    save_strategy="epoch",
    save_total_limit=3
)

# Train
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    max_seq_length=2048,
    args=training_args
)

trainer.train()
```

## Learning Rate Optimization

### Finding Optimal LR (Learning Rate Finder)

```python
from transformers.trainer_utils import IntervalStrategy

def find_learning_rate(model, tokenizer, dataset, min_lr=1e-7, max_lr=1):
    """Run LR finder to find optimal learning rate"""

    learning_rates = []
    losses = []

    # Try different learning rates
    for lr in [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3]:
        print(f"Testing LR: {lr}")

        args = TrainingArguments(
            output_dir=f"./lr_test_{lr}",
            learning_rate=lr,
            max_steps=100,
            per_device_train_batch_size=2,
            logging_steps=10
        )

        trainer = SFTTrainer(
            model=model,
            tokenizer=tokenizer,
            train_dataset=dataset.select(range(200)),  # Small subset
            args=args
        )

        result = trainer.train()
        learning_rates.append(lr)
        losses.append(result.training_loss)

    # Plot results
    import matplotlib.pyplot as plt
    plt.plot(learning_rates, losses)
    plt.xscale('log')
    plt.xlabel('Learning Rate')
    plt.ylabel('Loss')
    plt.title('Learning Rate Finder')
    plt.savefig('lr_finder.png')

    # Optimal LR is typically where loss decreases fastest
    optimal_idx = np.argmin(np.gradient(losses))
    optimal_lr = learning_rates[optimal_idx]

    print(f"Optimal LR: {optimal_lr}")
    return optimal_lr
```

### Learning Rate Schedules

```python
# 1. Cosine Decay (Recommended)
training_args = TrainingArguments(
    lr_scheduler_type="cosine",
    learning_rate=2e-4,
    warmup_ratio=0.03  # 3% warmup, then cosine decay
)

# 2. Linear Decay
training_args = TrainingArguments(
    lr_scheduler_type="linear",
    learning_rate=2e-4,
    warmup_steps=100
)

# 3. Constant with Warmup
training_args = TrainingArguments(
    lr_scheduler_type="constant_with_warmup",
    learning_rate=2e-4,
    warmup_ratio=0.05
)

# 4. Polynomial Decay
training_args = TrainingArguments(
    lr_scheduler_type="polynomial",
    learning_rate=2e-4,
    warmup_ratio=0.03
)

# 5. Cosine with Restarts
training_args = TrainingArguments(
    lr_scheduler_type="cosine_with_restarts",
    learning_rate=2e-4,
    warmup_ratio=0.03
)
```

### LR Guidelines by Model Size

| Model Size | Learning Rate | Warmup Steps | Batch Size |
| ---------- | ------------- | ------------ | ---------- |
| 1-3B       | 5e-4 to 1e-3  | 50-100       | 8-16       |
| 7B         | 2e-4 to 5e-4  | 100-200      | 4-8        |
| 13B        | 1e-4 to 2e-4  | 200-300      | 2-4        |
| 30B+       | 5e-5 to 1e-4  | 300-500      | 1-2        |

## LoRA Configuration

### LoRA Rank Optimization

```python
# Rank (r) controls capacity and parameter count

# Low rank (r=4-8): Fast, memory efficient, less capacity
model = FastLanguageModel.get_peft_model(
    model,
    r=8,
    lora_alpha=16,  # Alpha typically 1-2x rank
    # Use for: Simple tasks, limited data
)

# Medium rank (r=16-32): Balanced (recommended)
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=16,
    # Use for: Most tasks, default choice
)

# High rank (r=64-128): Max capacity, slower
model = FastLanguageModel.get_peft_model(
    model,
    r=64,
    lora_alpha=64,
    # Use for: Complex tasks, lots of data
)
```

### LoRA Alpha Guidelines

```python
# Alpha controls the scaling of LoRA updates

# Conservative (alpha = rank/2)
lora_alpha = 8  # for r=16
# Result: Slow adaptation, stable

# Standard (alpha = rank)
lora_alpha = 16  # for r=16
# Result: Balanced (recommended)

# Aggressive (alpha = 2*rank)
lora_alpha = 32  # for r=16
# Result: Fast adaptation, may be unstable
```

### Target Modules Selection

```python
# Minimal (attention only): Fast, less capacity
target_modules = ["q_proj", "v_proj"]

# Standard (all attention): Good balance
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]

# Extended (attention + MLP): Best quality (recommended)
target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj"
]

# Full (everything): Maximum capacity
target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
    "embed_tokens", "lm_head"
]
```

### LoRA Parameter Count

```python
def calculate_lora_params(base_model_size, rank, num_target_modules):
    """
    Estimate trainable parameters with LoRA
    """
    # For a 7B model with r=16 and 4 target modules:
    # ~16M trainable parameters (0.2% of base model)

    params_per_module = rank * 2 * 4096  # Approximate
    total_lora_params = params_per_module * num_target_modules

    return {
        "lora_params": total_lora_params,
        "base_params": base_model_size * 1e9,
        "trainable_percent": (total_lora_params / (base_model_size * 1e9)) * 100
    }

# Example
params = calculate_lora_params(
    base_model_size=7,      # 7B model
    rank=16,
    num_target_modules=7    # All attention + MLP
)
print(f"Trainable: {params['trainable_percent']:.2f}%")
```

## Batch Size & Gradient Accumulation

### Effective Batch Size

```python
# Effective batch = per_device_batch * gradient_accumulation * num_gpus

# Example 1: Limited VRAM
training_args = TrainingArguments(
    per_device_train_batch_size=1,    # Very small
    gradient_accumulation_steps=8,    # Accumulate 8 steps
    # Effective batch = 1 * 8 = 8
)

# Example 2: More VRAM
training_args = TrainingArguments(
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    # Effective batch = 4 * 2 = 8 (same effective batch)
)

# Example 3: Multi-GPU
training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=2,
    # With 2 GPUs: 2 * 2 * 2 = 8
)
```

### Optimal Batch Size Guidelines

| Model Size | Min Effective Batch | Recommended | Max (if possible) |
| ---------- | ------------------- | ----------- | ----------------- |
| 1-3B       | 4                   | 8-16        | 32                |
| 7B         | 8                   | 16-32       | 64                |
| 13B        | 16                  | 32-64       | 128               |
| 30B+       | 32                  | 64-128      | 256               |

### Sequence Length Optimization

```python
# Balance memory, speed, and quality

# Short sequences (faster, less memory)
max_seq_length = 512
# Use for: Short-form content, Q&A

# Medium sequences (balanced)
max_seq_length = 2048
# Use for: Most tasks (recommended)

# Long sequences (slower, more memory)
max_seq_length = 4096
# Use for: Long-form content, documents

# Very long (requires optimization)
max_seq_length = 8192
# Use for: Full documents, requires packing
```

### Dynamic Batch Size

```python
# Adjust batch size based on sequence length
def get_dynamic_batch_size(seq_length, gpu_memory=24):
    """Calculate optimal batch size for sequence length"""

    if seq_length <= 512:
        return 8 if gpu_memory >= 16 else 4
    elif seq_length <= 1024:
        return 4 if gpu_memory >= 16 else 2
    elif seq_length <= 2048:
        return 2 if gpu_memory >= 24 else 1
    else:  # > 2048
        return 1

# Usage
batch_size = get_dynamic_batch_size(
    seq_length=2048,
    gpu_memory=24  # GB
)
```

## Mixed Precision Training

### BF16 vs FP16

```python
import torch

# BF16 (preferred if available)
training_args = TrainingArguments(
    bf16=torch.cuda.is_bf16_supported(),  # Auto-detect
    # Better numerical stability than FP16
    # Same memory savings as FP16
    # Recommended for: A100, H100, 4090
)

# FP16 (fallback)
training_args = TrainingArguments(
    fp16=not torch.cuda.is_bf16_supported(),
    fp16_opt_level="O1",  # O1, O2, or O3
    # Good for: V100, older GPUs
)

# FP32 (full precision, not recommended)
# Use only for debugging
```

### Gradient Scaler (for FP16)

```python
# Prevent underflow with FP16
from torch.cuda.amp import GradScaler

training_args = TrainingArguments(
    fp16=True,
    fp16_full_eval=True,
    fp16_opt_level="O2",  # More aggressive optimization
)

# Unsloth handles this automatically
```

## Gradient Optimization

### Gradient Checkpointing

```python
# Trade computation for memory
model = FastLanguageModel.get_peft_model(
    model,
    use_gradient_checkpointing="unsloth"  # Unsloth-optimized
    # Saves ~30-50% memory
    # Adds ~10-20% training time
)

# Without gradient checkpointing (more memory, faster)
model = FastLanguageModel.get_peft_model(
    model,
    use_gradient_checkpointing=False
)
```

### Gradient Clipping

```python
# Prevent exploding gradients
training_args = TrainingArguments(
    max_grad_norm=1.0,  # Clip gradients above this norm
    # Lower (0.5): More conservative
    # Default (1.0): Standard (recommended)
    # Higher (2.0): Less clipping
)

# Disable clipping
training_args = TrainingArguments(
    max_grad_norm=0.0  # No clipping
)
```

### Gradient Accumulation Steps

```python
# Accumulate gradients for larger effective batch

# Calculate accumulation steps
def calculate_accumulation(
    target_batch_size: int,
    per_device_batch: int,
    num_gpus: int = 1
):
    """Calculate gradient accumulation steps"""
    return target_batch_size // (per_device_batch * num_gpus)

# Example: Want batch=32, have 1 GPU, can fit batch=4
accumulation_steps = calculate_accumulation(
    target_batch_size=32,
    per_device_batch=4,
    num_gpus=1
)  # Returns 8

training_args = TrainingArguments(
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8
)
```

## Hyperparameter Tuning

### Grid Search

```python
from itertools import product

# Define search space
search_space = {
    'learning_rate': [1e-4, 2e-4, 5e-4],
    'lora_rank': [8, 16, 32],
    'lora_alpha': [8, 16, 32],
    'batch_size': [4, 8]
}

# Grid search
best_loss = float('inf')
best_params = None

for lr, rank, alpha, batch in product(*search_space.values()):
    print(f"Testing: lr={lr}, rank={rank}, alpha={alpha}, batch={batch}")

    # Configure model
    model = configure_lora(rank=rank, alpha=alpha)

    # Train
    trainer = SFTTrainer(
        model=model,
        args=TrainingArguments(
            learning_rate=lr,
            per_device_train_batch_size=batch,
            num_train_epochs=1  # Quick test
        )
    )

    result = trainer.train()

    if result.training_loss < best_loss:
        best_loss = result.training_loss
        best_params = (lr, rank, alpha, batch)

print(f"Best params: {best_params}")
```

### Bayesian Optimization (Optuna)

```python
import optuna

def objective(trial):
    """Optuna objective function"""

    # Suggest hyperparameters
    lr = trial.suggest_float('learning_rate', 1e-5, 1e-3, log=True)
    rank = trial.suggest_int('lora_rank', 8, 64, step=8)
    alpha = trial.suggest_int('lora_alpha', 8, 64, step=8)
    batch = trial.suggest_categorical('batch_size', [2, 4, 8])

    # Configure and train
    model = configure_lora(rank=rank, alpha=alpha)

    trainer = SFTTrainer(
        model=model,
        args=TrainingArguments(
            learning_rate=lr,
            per_device_train_batch_size=batch,
            num_train_epochs=1
        )
    )

    result = trainer.train()

    return result.training_loss

# Run optimization
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=20)

print(f"Best params: {study.best_params}")
print(f"Best loss: {study.best_value}")
```

### W&B Sweeps

```python
import wandb

# Define sweep config
sweep_config = {
    'method': 'bayes',  # or 'grid', 'random'
    'metric': {
        'name': 'train_loss',
        'goal': 'minimize'
    },
    'parameters': {
        'learning_rate': {
            'distribution': 'log_uniform',
            'min': -9.21,  # ln(1e-4)
            'max': -6.91   # ln(1e-3)
        },
        'lora_rank': {
            'values': [8, 16, 32, 64]
        },
        'batch_size': {
            'values': [2, 4, 8]
        }
    }
}

# Initialize sweep
sweep_id = wandb.sweep(sweep_config, project="llm-tuning")

# Run sweep
def train_sweep():
    wandb.init()
    config = wandb.config

    # Train with config
    trainer = SFTTrainer(...)
    trainer.train()

wandb.agent(sweep_id, train_sweep, count=10)
```

## Training Monitoring

### Weights & Biases Integration

```python
import wandb

# Initialize
wandb.init(
    project="llm-finetuning",
    config={
        "learning_rate": 2e-4,
        "lora_rank": 16,
        "batch_size": 8,
        "model": "Llama-3.2-7B"
    }
)

# Training args with W&B
training_args = TrainingArguments(
    output_dir="./outputs",
    report_to="wandb",  # Enable W&B logging
    logging_steps=10,
    run_name="medical-model-v1"
)

# W&B will automatically log:
# - Training loss
# - Learning rate
# - Gradient norms
# - System metrics (GPU, CPU, RAM)

# Custom logging
wandb.log({"custom_metric": value})
```

### TensorBoard Integration

```python
training_args = TrainingArguments(
    output_dir="./outputs",
    logging_dir="./logs",
    report_to="tensorboard",
    logging_steps=10
)

# View with: tensorboard --logdir=./logs
```

### Loss Curve Interpretation

```python
# Monitoring during training

# Good signs:
# ✓ Steady decrease in loss
# ✓ Smooth curve (no spikes)
# ✓ Validation loss tracks training loss
# ✓ Learning rate schedule working

# Warning signs:
# ✗ Loss plateaus early → increase LR or model capacity
# ✗ Loss spikes → reduce LR or clip gradients
# ✗ Val loss >> train loss → overfitting (see below)
# ✗ Loss explodes → reduce LR, check data

def analyze_training(log_history):
    """Analyze training progress"""

    losses = [log['loss'] for log in log_history if 'loss' in log]

    # Check convergence
    recent_losses = losses[-10:]
    improvement = (recent_losses[0] - recent_losses[-1]) / recent_losses[0]

    if improvement < 0.01:
        print("⚠️ Training has plateaued")
        print("Consider: increase LR, train longer, add data")

    # Check stability
    loss_std = np.std(losses[-50:])
    if loss_std > 0.1:
        print("⚠️ Training is unstable")
        print("Consider: reduce LR, clip gradients")

    # Check overfitting
    # (Requires validation loss - see below)
```

## Preventing Overfitting

### Early Stopping

```python
from transformers import EarlyStoppingCallback

# Stop if validation loss doesn't improve
training_args = TrainingArguments(
    evaluation_strategy="steps",
    eval_steps=100,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
)
```

### Regularization Techniques

```python
# 1. LoRA Dropout (if not using Unsloth optimization)
model = FastLanguageModel.get_peft_model(
    model,
    lora_dropout=0.05,  # 5% dropout
    # Note: Unsloth recommends 0 for optimal speed
)

# 2. Weight Decay
training_args = TrainingArguments(
    weight_decay=0.01,  # L2 regularization
    # Default: 0.0
    # Typical range: 0.01-0.1
)

# 3. Gradient Noise
# Adds noise to gradients (reduces overfitting)
# Not directly supported, but can be implemented
```

### Data Augmentation

```python
# See dataset-engineering skill for:
# - Paraphrase augmentation
# - Back-translation
# - Synthetic data generation

# During training, use data augmentation to increase diversity
```

### Validation Strategy

```python
# Monitor validation loss

training_args = TrainingArguments(
    evaluation_strategy="steps",
    eval_steps=100,  # Evaluate every 100 steps
    save_strategy="steps",
    save_steps=100,
    load_best_model_at_end=True  # Load best checkpoint
)

# Train/val split
from sklearn.model_selection import train_test_split

train_data, val_data = train_test_split(
    dataset,
    test_size=0.1,
    random_state=42
)

trainer = SFTTrainer(
    train_dataset=train_data,
    eval_dataset=val_data,
    # ...
)
```

## Advanced Techniques

### Curriculum Learning

```python
def curriculum_training(model, tokenizer, dataset):
    """Train on easy examples first, then harder ones"""

    # Sort by difficulty (e.g., output length)
    sorted_dataset = sorted(
        dataset,
        key=lambda x: len(x['output'])
    )

    # Train in stages
    stages = [
        (0, len(sorted_dataset) // 3, 1),      # Easy, 1 epoch
        (0, 2 * len(sorted_dataset) // 3, 1),  # Easy+Medium, 1 epoch
        (0, len(sorted_dataset), 2)             # All, 2 epochs
    ]

    for start, end, epochs in stages:
        print(f"Stage: examples {start}-{end}, {epochs} epochs")

        stage_dataset = sorted_dataset[start:end]

        trainer = SFTTrainer(
            model=model,
            train_dataset=stage_dataset,
            args=TrainingArguments(num_train_epochs=epochs)
        )

        trainer.train()
```

### Progressive Sequence Length

```python
# Start with shorter sequences, gradually increase

def progressive_training(model, tokenizer, dataset):
    """Increase sequence length during training"""

    stages = [
        (512, 1),   # 512 tokens, 1 epoch
        (1024, 1),  # 1024 tokens, 1 epoch
        (2048, 2)   # 2048 tokens, 2 epochs
    ]

    for seq_len, epochs in stages:
        print(f"Training with max_seq_length={seq_len}")

        trainer = SFTTrainer(
            model=model,
            tokenizer=tokenizer,
            train_dataset=dataset,
            max_seq_length=seq_len,
            args=TrainingArguments(num_train_epochs=epochs)
        )

        trainer.train()
```

### Learning Rate Warmup + Decay

```python
# Optimal schedule for most cases
training_args = TrainingArguments(
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,  # 3% of total steps
    # This creates:
    # 1. Linear warmup (0 → 2e-4) for 3% of steps
    # 2. Cosine decay (2e-4 → 0) for remaining 97%
)

# Manual warmup steps
training_args = TrainingArguments(
    learning_rate=2e-4,
    warmup_steps=100,  # Explicit number
    # Instead of warmup_ratio
)
```

## Memory Optimization

### Reduce Memory Usage

```python
# 1. Gradient checkpointing
use_gradient_checkpointing="unsloth"

# 2. Smaller batch size + gradient accumulation
per_device_train_batch_size=1
gradient_accumulation_steps=8

# 3. Lower precision
bf16=True  # or fp16=True

# 4. Optimize target modules (fewer = less memory)
target_modules=["q_proj", "v_proj"]  # Instead of all 7

# 5. Lower LoRA rank
r=8  # Instead of r=16 or r=32

# 6. Reduce sequence length
max_seq_length=1024  # Instead of 2048

# 7. Use 8-bit optimizer
optim="adamw_8bit"

# 8. Quantized model
load_in_4bit=True  # Already using this with Unsloth
```

### Memory Calculation

```python
def estimate_memory(
    model_size_b: float,
    lora_rank: int,
    batch_size: int,
    seq_length: int,
    precision: str = "bf16"
):
    """Estimate GPU memory requirements"""

    # Model memory (4-bit quantized)
    model_memory = model_size_b * 0.5  # GB (4-bit = 0.5 bytes/param)

    # LoRA adapters
    lora_params = lora_rank * 2 * 4096 * 7  # Approximate
    lora_memory = (lora_params * 2) / 1e9  # FP16

    # Activations (depends on batch size and seq length)
    activation_memory = batch_size * seq_length * model_size_b * 0.002

    # Optimizer states (8-bit)
    optimizer_memory = lora_memory * 1  # 8-bit Adam

    total = model_memory + lora_memory + activation_memory + optimizer_memory

    return {
        'model': model_memory,
        'lora': lora_memory,
        'activations': activation_memory,
        'optimizer': optimizer_memory,
        'total': total,
        'recommended_gpu': '16GB' if total < 14 else '24GB' if total < 22 else '48GB'
    }

# Example
mem = estimate_memory(
    model_size_b=7,
    lora_rank=16,
    batch_size=2,
    seq_length=2048
)
print(f"Estimated memory: {mem['total']:.1f} GB")
print(f"Recommended GPU: {mem['recommended_gpu']}")
```

## Troubleshooting

### Issue: Training is Slow

**Solutions:**

```python
# 1. Disable gradient checkpointing (if you have VRAM)
use_gradient_checkpointing=False

# 2. Increase batch size
per_device_train_batch_size=4  # Instead of 2

# 3. Use BF16/FP16
bf16=True

# 4. Reduce validation frequency
eval_steps=500  # Instead of 100

# 5. Use fewer target modules
target_modules=["q_proj", "v_proj"]  # Instead of all 7

# 6. Use Unsloth optimizations (already included)
```

### Issue: Out of Memory

**Solutions:**

```python
# See "Memory Optimization" section above

# Quick fix:
per_device_train_batch_size=1
gradient_accumulation_steps=8
use_gradient_checkpointing="unsloth"
max_seq_length=1024  # Instead of 2048
```

### Issue: Loss Not Decreasing

**Solutions:**

```python
# 1. Increase learning rate
learning_rate=5e-4  # Instead of 2e-4

# 2. Increase LoRA rank
r=32  # Instead of r=16

# 3. Train longer
num_train_epochs=5  # Instead of 3

# 4. Check data quality (see dataset-engineering skill)

# 5. Remove weight decay
weight_decay=0.0

# 6. Try different scheduler
lr_scheduler_type="linear"  # Instead of cosine
```

### Issue: Model Overfitting

**Solutions:**

```python
# 1. Add more training data
# See dataset-engineering skill

# 2. Reduce model capacity
r=8  # Instead of r=16

# 3. Add weight decay
weight_decay=0.01

# 4. Use validation set + early stopping
# See "Preventing Overfitting" section

# 5. Train for fewer epochs
num_train_epochs=1  # Instead of 3

# 6. Use data augmentation
# See dataset-engineering skill
```

## Best Practices

### 1. Start with Defaults

```python
# Use the "Optimal Default Configuration" from Quick Start
# Only tune if you have specific issues
```

### 2. Monitor Everything

```python
# Use W&B or TensorBoard
# Watch: loss, LR, gradient norms, memory usage
```

### 3. Save Checkpoints

```python
training_args = TrainingArguments(
    save_strategy="epoch",
    save_total_limit=3,  # Keep last 3 checkpoints
    load_best_model_at_end=True
)
```

### 4. Validate During Training

```python
# Always use validation set
# Catch overfitting early
```

### 5. Document Experiments

```python
# Track what you tried
# Use W&B or experiment tracking tool
# Record: hyperparams, results, observations
```

## Summary

Training optimization workflow:

1. ✓ Start with optimal defaults
2. ✓ Monitor training (W&B/TensorBoard)
3. ✓ Adjust if needed (LR, batch size, LoRA rank)
4. ✓ Prevent overfitting (validation, early stopping)
5. ✓ Optimize memory (checkpointing, quantization)
6. ✓ Fine-tune hyperparameters (grid search/Bayesian)
7. ✓ Document everything

Remember: Most models work well with defaults. Only optimize if you have specific issues.

**Default Recipe (works 90% of the time):**

- Learning rate: 2e-4
- LoRA rank: 16
- LoRA alpha: 16
- Batch size: 8 (effective)
- Scheduler: cosine with 3% warmup
- Precision: BF16
- Epochs: 3
- Target modules: All attention + MLP
