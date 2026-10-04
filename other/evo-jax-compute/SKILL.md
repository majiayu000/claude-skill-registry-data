---
name: evo-jax-compute
description: Implements all five JAX computation tasks - row-wise mean reduction, element-wise squaring, logistic loss gradient via jax.grad, RNN forward pass via jax.lax.scan, and JIT-compiled 2-layer MLP forward pass.
---

# evo-jax-compute

All JAX computation logic for the five problem tasks, dispatching by problem ID.

## Quick Start

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-jax-compute/scripts')
from compute_utils import dispatch_task, compute_basic_reduce, compute_scan_rnn

# Dispatch by task ID
result = dispatch_task('basic_reduce', 'compute mean of each row', jax_data)

# Or call directly
result = compute_basic_reduce(x_array)
```

## Key Functions

### compute_basic_reduce(x)
Row-wise mean: `jnp.mean(x, axis=1)`. Input (M,N) -> Output (M,).

### compute_map_square(x)
Element-wise square: `jnp.square(x)`. Same shape in/out.

### compute_grad_logistic(data)
Gradient of logistic loss w.r.t. weights.
- Loss: `L(w) = mean(logaddexp(0, -y * (X @ w)))`
- Uses `jax.grad(loss_fn, argnums=0)` to differentiate w.r.t. w
- `jnp.logaddexp(0, z)` for numerical stability (scalar 0 auto-promotes)
- Input: dict with keys 'x'/'X' (N,D), 'y' (N,), 'w' (D,)
- Output: gradient array (D,)

### compute_scan_rnn(data)
RNN forward pass using `jax.lax.scan`.
- **CRITICAL**: Uses weight-RIGHT-multiply: `h_new = tanh(x_t @ Wx + h @ Wh + b)`
- x_t is on LEFT of Wx, h is on LEFT of Wh (standard doc convention)
- Weight matrices are closed over, NOT passed through carry
- Carry dtype must match init dtype exactly
- Input: dict with 'seq' (T,I), 'init' (H,), 'Wx', 'Wh', 'b'
- Output: stacked hidden states (T, H)

### compute_jit_mlp(data)
JIT-compiled 2-layer MLP.
- Layer 1: `h = relu(X @ W1 + b1)` using `jax.nn.relu`
- Layer 2: `out = h @ W2 + b2`
- Uses `@jax.jit` decorator
- Input: dict with 'X' (B,F), 'W1' (F,H), 'b1' (H,), 'W2' (H,O), 'b2' (O,)
- Output: (B, O)

### dispatch_task(task_id, description, data)
Dispatch to correct compute function by exact ID match or fuzzy keyword matching.

## Domain Knowledge

- RNN uses RIGHT-multiply (x_t @ Wx), verified against reference outputs
- jnp.logaddexp(0, x) safely computes log(1+exp(x)) without overflow
- jax.grad requires scalar return; use jnp.mean() to aggregate
- jax.lax.scan carry must maintain identical dtype/shape across iterations
- JIT may cause ~1e-7 float differences due to XLA operation reordering
- jax.nn.relu is canonical; derivative at 0 is defined as 0
