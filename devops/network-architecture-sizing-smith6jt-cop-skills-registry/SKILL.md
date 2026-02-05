---
name: network-architecture-sizing
description: "PPO network architecture sizing for trading models. Trigger: (1) model files are unexpectedly small/large, (2) choosing hidden_dims for training, (3) balancing model capacity vs inference speed."
author: Claude Code
date: 2025-12-18
---

# Network Architecture Sizing - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-18 |
| **Goal** | Understand relationship between hidden_dims and model file size |
| **Environment** | Google Colab A100, PyTorch 2.x, NativePPOTrainer |
| **Status** | Documented |

## Context
Training runs produced models at ~72 MB instead of expected ~148 MB. Investigation revealed the `hidden_dims` configuration determines model size, with the first layer dominating total parameter count due to multiplication with observation dimensions.

## Architecture Comparison

### Model Size vs Architecture

| Architecture | hidden_dims | Layers | Total Params | File Size | First Layer Size |
|--------------|-------------|--------|--------------|-----------|------------------|
| Large (v2.2) | (2048, 1024, 512, 256) | 4 | 12.6M | ~148 MB | 2048 × obs_dim |
| Medium (v2.3) | (1024, 512, 256) | 3 | 6.1M | ~72 MB | 1024 × obs_dim |
| Small | (512, 256, 128) | 3 | ~1.5M | ~18 MB | 512 × obs_dim |
| Tiny | (256, 128, 64) | 3 | ~0.4M | ~5 MB | 256 × obs_dim |

### Why First Layer Dominates

With 53 features × 100 lookback = 5,300 input dimensions:
- Large: `2048 × 5300 = 10.9M params` (86% of network)
- Medium: `1024 × 5300 = 5.4M params` (89% of network)
- Small: `512 × 5300 = 2.7M params` (90% of network)

**Key insight**: The first hidden layer dimension has exponentially more impact on model size than deeper layers.

## Configuration Locations

Current defaults in `ppo_trainer_native.py`:

| Function | GPU Tier | hidden_dims |
|----------|----------|-------------|
| `get_auto_config()` | H100 | (1024, 512, 256) |
| `get_auto_config()` | A100 | (1024, 512, 256) |
| `get_auto_config()` | high (40GB+) | (512, 256, 128) |
| `get_auto_config()` | medium (20-40GB) | (512, 256, 128) |
| `get_auto_config()` | low (<20GB) | (256, 128, 64) |
| `get_a100_config()` | A100-80GB | (1024, 512, 256) |
| `get_a100_config()` | A100-40GB | (512, 256, 128) |

## Verified Workflow

### To use larger architecture (148 MB models):
```python
from alpaca_trading.gpu.ppo_trainer_native import get_auto_config

config = get_auto_config(total_timesteps=200_000_000, training_mode='production')
config.hidden_dims = (2048, 1024, 512, 256)  # Override to 4-layer large

trainer = NativePPOTrainer(env, config)
```

### To verify model architecture before training:
```python
import torch

# Check expected size
obs_dim = 5300  # 53 features × 100 lookback
hidden_dims = (2048, 1024, 512, 256)

params = obs_dim * hidden_dims[0]  # First layer
for i in range(len(hidden_dims) - 1):
    params += hidden_dims[i] * hidden_dims[i+1]
params += hidden_dims[-1] * 64 * 2  # Actor + critic heads

print(f"Expected params: {params:,}")
print(f"Expected size: ~{params * 4 * 3 / 1024 / 1024:.0f} MB")  # float32 × 3 (weights + optimizer state)
```

### To inspect existing model:
```python
import torch

ckpt = torch.load('model.pt', map_location='cpu', weights_only=False)
print(f"hidden_dims: {ckpt['config'].hidden_dims}")
print(f"Total params: {sum(v.numel() for v in ckpt['policy_state_dict'].values()):,}")
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Assuming all configs use same architecture | Different GPU tiers have different defaults | Always check `hidden_dims` in config before training |
| Only checking layer count | 3-layer (1024,512,256) vs 4-layer (2048,1024,512,256) | First layer width matters more than depth |
| Not saving config with model | Couldn't reproduce training | Always save full config in checkpoint |
| Using large architecture on small GPU | OOM errors | Match architecture to available VRAM |
| Assuming bigger = better | Overfitting on small datasets | Larger models need more data/regularization |

## Performance Considerations

### Larger Architecture (2048, 1024, 512, 256)
**Pros:**
- Higher model capacity for complex patterns
- Better for symbols with rich feature interactions
- May capture longer-term dependencies

**Cons:**
- 2x file size (~148 MB vs ~72 MB)
- Slower inference (~1.5-2x)
- Higher VRAM usage during training
- More prone to overfitting with limited data

### Smaller Architecture (1024, 512, 256)
**Pros:**
- Faster inference (important for live trading)
- Lower VRAM requirements
- Faster training iterations
- Better generalization on limited data

**Cons:**
- May underfit complex market dynamics
- Less capacity for feature interactions

## Recommended Architecture by Use Case

| Use Case | Recommended hidden_dims | Rationale |
|----------|------------------------|-----------|
| Quick iteration/testing | (512, 256, 128) | Fast training, low memory |
| Standard production | (1024, 512, 256) | Good balance |
| Complex symbols (crypto) | (2048, 1024, 512, 256) | Higher volatility patterns |
| Limited training data (<1 year) | (512, 256, 128) | Reduce overfitting |
| Extended training (500M+ steps) | (2048, 1024, 512, 256) | Capacity for more learning |

## Key Insights

- **First layer width dominates model size** - doubling first layer ~doubles total params
- **File size ≈ params × 12 bytes** (float32 weights + Adam optimizer moments)
- **Current v2.3 defaults favor smaller models** - optimized for speed over capacity
- **Architecture mismatch = inference failure** - models trained with different hidden_dims are incompatible
- **Always log hidden_dims** - critical for reproducibility and debugging

## Diagnostic Commands

```python
# Compare two model architectures
def compare_models(path1, path2):
    m1 = torch.load(path1, map_location='cpu', weights_only=False)
    m2 = torch.load(path2, map_location='cpu', weights_only=False)

    print(f"Model 1: {m1['config'].hidden_dims}")
    print(f"Model 2: {m2['config'].hidden_dims}")
    print(f"Params 1: {sum(v.numel() for v in m1['policy_state_dict'].values()):,}")
    print(f"Params 2: {sum(v.numel() for v in m2['policy_state_dict'].values()):,}")
```

## References
- `alpaca_trading/gpu/ppo_trainer_native.py`: Lines 1314, 1339, 1726, 1760
- `alpaca_trading/gpu/ppo_trainer_native.py`: NativeActorCritic class (line 305)
- CLAUDE.md: GPU Optimized Settings table
