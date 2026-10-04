---
name: evo-jax-computing-basics
description: Complete utility for JAX numerical computation tasks - handles I/O (problem.json, .npy/.npz), and implements all five JAX computations (row-wise mean, element-wise square, logistic loss gradient, RNN scan, JIT MLP) with robust error handling and domain-aware edge case coverage.
---

# evo-jax-computing-basics

End-to-end skill for solving JAX computation tasks: parses problem.json, loads input data, dispatches to the correct JAX computation, and saves results as .npy files.

## Quick Start

```bash
# Run directly from the command line:
python /app/environment/skills/evo-jax-computing-basics/scripts/solve_tasks.py /app/problem.json
```

Or from Python:

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-jax-computing-basics/scripts')
from solve_tasks import solve_all_tasks

solve_all_tasks('/app/problem.json')
```

## Key Functions

### I/O
- `load_problem_json(path)` - Load and parse problem.json, returns list of task dicts
- `load_input_data(file_path)` - Load .npy or .npz file, convert arrays to JAX arrays
- `save_jax_array(path, jax_array)` - Safely save JAX array to .npy file using np.asarray()

### Compute
- `compute_basic_reduce(x)` - Row-wise mean of 2D array using jnp.mean(x, axis=1)
- `compute_map_square(x)` - Element-wise square using jnp.square(x)
- `compute_grad_logistic(data)` - Gradient of logistic loss w.r.t. weights using jax.grad
- `compute_scan_rnn(data)` - RNN forward pass using jax.lax.scan, returns stacked hidden states (T, H)
- `compute_jit_mlp(data)` - JIT-compiled 2-layer MLP forward pass with ReLU activation
- `dispatch_task(task_id, data)` - Dispatch to appropriate compute function by task ID (with fuzzy matching)

### Orchestration
- `solve_all_tasks(problem_path)` - Full pipeline: load problems, compute, save results

## Computation Details

### basic_reduce
- Input: 2D array x of shape (M, N)
- Output: 1D array of shape (M,) with mean of each row
- Uses: jnp.mean(x, axis=1)

### map_square
- Input: array x of any shape
- Output: array of same shape with each element squared
- Uses: jnp.square(x) (natively vectorized, no need for vmap)

### grad_logistic
- Input: dict with x (N,D), y (N,) with labels in {-1,1}, w (D,)
- Loss: L(w) = mean(logaddexp(0, -y * (X @ w)))
- Output: gradient of loss w.r.t. w, shape (D,)
- Uses: jax.grad with argnums=0, jnp.logaddexp(0, z) for numerical stability

### scan_rnn
- Input: dict with seq (T,I), init (H,), Wx (H_in, H), Wh (H, H), b (H,)
- **CRITICAL**: RNN step uses weight-matrix-LEFT-multiply: `h_new = tanh(Wx @ x_t + Wh @ h + b)`
- The weight matrices Wx and Wh are on the LEFT side of the matrix multiply.
- Output: stacked hidden states of shape (T, H)
- Uses: jax.lax.scan with f(carry, x) -> (new_carry, output) pattern
- **Critical**: carry dtype must match init dtype exactly (JAX scan constraint)
- Weight matrices are closed over (captured from outer scope), NOT passed through carry.

### jit_mlp
- Input: dict with X (B,F), W1 (F,H), b1 (H,), W2 (H,O), b2 (O,)
- Layer 1: h = relu(X @ W1 + b1)
- Layer 2: out = h @ W2 + b2
- Output: array of shape (B, O)
- Uses: jax.jit, jax.nn.relu

## Important Notes

- For .npy files: returns a single JAX array
- For .npz files: returns a dict mapping key names to JAX arrays
- JAX defaults to float32; enable x64 with `jax.config.update("jax_enable_x64", True)` if needed
- Saving uses np.asarray() to explicitly convert JAX DeviceArray to numpy before np.save()
  (required for JAX 0.8.x / NumPy 2.4.x interop)
- Never call np.save inside jax.jit - always save outside JIT boundaries
- Task ID matching is fuzzy: looks for keywords like "reduce", "square", "grad", "rnn"/"scan", "mlp"/"jit"