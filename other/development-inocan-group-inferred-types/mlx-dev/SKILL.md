---
name: mlx-dev
description: Write correct, idiomatic Apple MLX code for Apple Silicon ML. Use when working with MLX arrays, neural networks, training loops, lazy evaluation, unified memory, mx.eval, mx.compile, Metal GPU, memory optimization, quantization, or Apple Silicon performance. Covers critical API differences from PyTorch/NumPy, array indexing gotchas (lists must be mx.array, slices create copies), NHWC format for Conv2d, __call__ not forward(), float64 CPU-only, mlx-lm integration, and debugging patterns.
---

# MLX Development Guide

## Environment Setup

Use `uv` for Python environment and package management:

```bash
# Install MLX
uv add mlx

# Run MLX scripts
uv run python train.py

# Run with specific dependencies
uv run --with mlx python script.py
```

## Critical Rules

### 1. Lazy Evaluation - Always Evaluate at Loop Boundaries

Operations build a graph; nothing computes until `mx.eval()`:

```python
# CORRECT: Evaluate at iteration boundaries
for batch in dataset:
    loss, grads = value_and_grad_fn(model, batch)
    optimizer.update(model, grads)
    mx.eval(loss, model.parameters())  # ALL computation here

# WRONG: Evaluating too frequently
for _ in range(100):
    a = a + b
    mx.eval(a)  # Massive overhead!
```

Implicit eval triggers: `print(a)`, `a.item()`, `np.array(a)`, `if a > 0:`.

### 2. Array Indexing Differs from NumPy

```python
# Lists must be mx.array
a[[0, 1]]              # ValueError!
a[mx.array([0, 1])]    # Works

# Slice indices must be Python ints
i = mx.array(2)
x[i:i+2]               # ValueError!
x[i.item():i.item()+2] # Works (forces eval)

# Slices create COPIES, not views (opposite of NumPy)
b = a[:]
b[2] = 0  # a is unchanged!

# Boolean mask READS not supported
a[mask]  # Not supported - use mx.where()

# No bounds checking - out-of-bounds returns garbage
```

For accumulating updates, use `at[]` syntax:
```python
a = a.at[idx].add(1)  # Properly accumulates at duplicate indices
```

See [references/array-indexing.md](references/array-indexing.md) for complete patterns.

### 3. Neural Networks: NHWC Format and __call__

```python
# Conv2d uses NHWC (not NCHW like PyTorch)
x_mlx = mx.array(x_torch.numpy().transpose(0, 2, 3, 1))

# Override __call__, not forward()
class MyModel(nn.Module):
    def __call__(self, x):  # NOT forward()
        return self.layer(x)

# No dtype in constructors - use set_dtype()
layer = nn.Linear(10, 10)
layer.set_dtype(mx.bfloat16)
```

See [references/neural-networks.md](references/neural-networks.md) for layer equivalents.

### 4. Data Types: float64 is CPU-Only

```python
a = mx.array([1.0], dtype=mx.float64)
mx.exp(a, stream=mx.gpu)  # RuntimeError!

# Solutions:
mx.exp(a, stream=mx.cpu)
mx.exp(a.astype(mx.float32))

# bfloat16 from external sources gets misinterpreted
from ml_dtypes import bfloat16
x = np.array(1., dtype=bfloat16)
mx.array(x)  # Returns complex64!
mx.array(x.astype(np.float32), dtype=mx.bfloat16)  # Correct
```

See [references/dtypes.md](references/dtypes.md) for full type support table.

### 5. Compilation: Capture All Mutable State

```python
from functools import partial

state = [model.state, optimizer.state, mx.random.state]  # Include random!

@partial(mx.compile, inputs=state, outputs=state)
def train_step(x, y):
    loss, grads = nn.value_and_grad(model, loss_fn)(model, x, y)
    optimizer.update(model, grads)
    return loss

# No print() in compiled functions - crashes during tracing
# String decoding triggers recompilation - decode outside loop
```

See [references/compilation.md](references/compilation.md) for recompilation triggers.

## Quick Reference Tables

### Dtype Support

| Type | GPU | Notes |
|------|-----|-------|
| float32 | Yes | Default float |
| float16 | Yes | |
| bfloat16 | Yes | M3+ recommended |
| float64 | **CPU only** | GPU throws! |
| int8-64, uint8-64 | Yes | |
| complex64 | Partial | No matmul |

### PyTorch → MLX Equivalents

| PyTorch | MLX |
|---------|-----|
| `tensor.to('cuda')` | Not needed (unified memory) |
| `nn.forward()` | `nn.__call__()` |
| NCHW format | NHWC format |
| `torch.gather()` | `mx.take_along_axis()` |
| `torch.scatter_add_()` | `arr.at[idx].add()` |

### Not Available in MLX

- `np.nonzero()` - restructure algorithm
- `np.unique()` - pre-sort or use dicts
- `arr[bool_mask]` read - use `mx.where()`
- `np.linalg.det()`, `np.linalg.lstsq()`

## Performance Notes

- **Transformers**: MLX typically 2-3x faster than PyTorch MPS
- **Convolutions**: 10-150x SLOWER than PyTorch MPS (known limitation)
- **LLM inference**: Excellent, especially quantized
- Use float16/bfloat16 for 2x memory bandwidth
- Use 4-bit quantization for LLMs (4x bandwidth)

## See Also

- [references/array-indexing.md](references/array-indexing.md) - Complete indexing patterns, at[] syntax, gather/scatter
- [references/neural-networks.md](references/neural-networks.md) - nn module, layers, weight format
- [references/compilation.md](references/compilation.md) - mx.compile patterns, state capture, recompilation
- [references/memory-management.md](references/memory-management.md) - Memory APIs, debugging leaks
- [references/dtypes.md](references/dtypes.md) - Type support, conversion patterns
- [references/random.md](references/random.md) - Seed vs key, splitting patterns
- [references/gradients.md](references/gradients.md) - Autodiff, value_and_grad, control flow
- [references/pytorch-migration.md](references/pytorch-migration.md) - Weight conversion, format changes
- [references/error-decoder.md](references/error-decoder.md) - Common errors → solutions

## Idiomatic Training Example

```python
import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
from functools import partial

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = [nn.Linear(784, 256), nn.Linear(256, 10)]

    def __call__(self, x):
        for layer in self.layers[:-1]:
            x = mx.maximum(layer(x), 0)
        return self.layers[-1](x)

def loss_fn(model, x, y):
    return nn.losses.cross_entropy(model(x), y, reduction="mean")

model = Model()
optimizer = optim.AdamW(learning_rate=1e-3)

state = [model.state, optimizer.state, mx.random.state]

@partial(mx.compile, inputs=state, outputs=state)
def train_step(x, y):
    loss, grads = nn.value_and_grad(model, loss_fn)(model, x, y)
    optimizer.update(model, grads)
    return loss

for epoch in range(num_epochs):
    for x_batch, y_batch in dataloader:
        loss = train_step(x_batch, y_batch)
        mx.eval(state)
    print(f"Epoch {epoch}: {loss.item():.4f}")
```
