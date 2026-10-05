---
name: nlp-gradient-checkpointing
description: >
  Trades compute for memory by recomputing intermediate activations during backprop instead of storing them, reducing memory from O(n) to O(sqrt(n)).
---
# Gradient Checkpointing

## Overview

Large transformer models store all intermediate activations for backpropagation, consuming massive GPU memory. Gradient checkpointing discards most activations during the forward pass and recomputes them on-the-fly during backward. This reduces activation memory from O(n_layers) to O(sqrt(n_layers)) at the cost of ~30% slower training. Essential for fine-tuning large models on limited GPU memory.

## Quick Start

```python
from transformers import AutoModel

model = AutoModel.from_pretrained("microsoft/deberta-v3-base")
model.gradient_checkpointing_enable()

# Now train as usual — memory usage drops significantly
# Pair with mixed precision for maximum memory savings
```

## Workflow

1. Load your pretrained transformer model
2. Call `model.gradient_checkpointing_enable()` before training
3. Train as normal — PyTorch handles activation recomputation automatically
4. Optionally combine with mixed precision (`torch.cuda.amp`) for further savings

## Key Decisions

- **When to use**: When model doesn't fit in GPU memory at your desired batch size
- **Speed cost**: ~25-35% slower per step; offset by enabling larger batch sizes
- **Combine with**: Mixed precision (FP16/BF16), gradient accumulation, frozen layers
- **PyTorch native**: `torch.utils.checkpoint.checkpoint()` for custom models
- **Disable for inference**: Only needed during training; no effect at eval time

## References

- [Optimization approaches for Transformers](https://www.kaggle.com/code/vad13irt/optimization-approaches-for-transformers)
