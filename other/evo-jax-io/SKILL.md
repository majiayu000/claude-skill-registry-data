---
name: evo-jax-io
description: Handles loading problem.json, reading .npy/.npz input files into JAX arrays, and saving JAX array results back to .npy files with proper numpy conversion.
---

# evo-jax-io

All file I/O for JAX computation tasks: parsing problem.json, loading numpy/npz data files and converting to JAX arrays, and safely serializing JAX arrays to .npy output files.

## Quick Start

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-jax-io/scripts')
from io_utils import load_problem_json, load_input_data, save_jax_array

# Load task definitions
tasks = load_problem_json('/app/problem.json')

# Load input data (.npy returns JAX array, .npz returns dict of JAX arrays)
data = load_input_data('/app/data/x.npy')       # single JAX array
data = load_input_data('/app/data/logistic.npz') # dict of JAX arrays

# Save result
save_jax_array('/app/basic_reduce.npy', result_array)
```

## Key Functions

### load_problem_json(path: str) -> list
Load and parse problem.json. Returns list of task dicts with keys: id, description, input, output.

### load_input_data(file_path: str) -> JAX array or dict
Load .npy or .npz file. For .npy: returns single JAX array. For .npz: returns dict mapping names to JAX arrays.

### save_jax_array(path: str, jax_array) -> None
Safely save JAX array to .npy file using np.asarray() for proper conversion.
Creates output directory if needed. Must be called outside jax.jit boundaries.

## Domain Knowledge

- JAX has no native disk I/O; always load with numpy then convert with jnp.asarray()
- JAX defaults to float32 precision; loaded float64 arrays get downcast unless jax_enable_x64 is True
- For saving: np.asarray(jax_array) is preferred over np.array() to avoid unnecessary copies
- Never call np.save() inside jax.jit - Tracer objects cause ConcretizationTypeError
- .npz files are loaded with np.load() which returns NpzFile dict-like object
