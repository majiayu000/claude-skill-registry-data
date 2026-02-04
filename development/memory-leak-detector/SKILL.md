---
name: memory-leak-detector
description: Detect and fix memory leaks in Python and PyTorch code, especially matplotlib figures and unreleased tensors. This skill should be used during Phase 4 performance optimization when memory usage grows over time.
---

# Memory Leak Detector

Identify and fix memory leaks in Python/PyTorch code, with special focus on matplotlib figures, tensor accumulation, and GPU memory issues.

## Purpose

Memory leaks cause programs to consume increasing memory over time, eventually leading to crashes or degraded performance. This skill systematically identifies and fixes common memory leak patterns in scientific Python code.

## When to Use

Use this skill when:
- Memory usage grows continuously during execution
- Out-of-memory errors after many iterations
- GPU memory fills up during training
- Phase 4 (Performance Optimization) tasks
- Long-running experiments crash

## Common Memory Leak Patterns

### 1. Matplotlib Figure Leaks ⭐⭐⭐ MOST COMMON

```python
# LEAK - Figures never closed
for epoch in range(1000):
    plt.figure()
    plt.plot(losses)
    plt.savefig(f'loss_{epoch}.png')
    # Figure stays in memory!

# Memory usage: Grows continuously (100MB+ per hour)

# FIX - Close figures
for epoch in range(1000):
    fig, ax = plt.subplots()
    ax.plot(losses)
    fig.savefig(f'loss_{epoch}.png')
    plt.close(fig)  # ✓ Free memory

# Or use context manager (Python 3.11+)
for epoch in range(1000):
    with plt.rc_context():
        fig, ax = plt.subplots()
        ax.plot(losses)
        fig.savefig(f'loss_{epoch}.png')
        plt.close(fig)
```

### 2. Tensor Gradient Accumulation

```python
# LEAK - Gradients accumulate
for epoch in range(1000):
    loss = model(data)
    loss.backward()  # Gradients add up!
    # No optimizer.step() or zero_grad()

# FIX - Clear gradients
for epoch in range(1000):
    optimizer.zero_grad()  # ✓ Clear old gradients
    loss = model(data)
    loss.backward()
    optimizer.step()
```

### 3. Holding Tensor References

```python
# LEAK - Keeps computational graph
results = []
for batch in dataloader:
    output = model(batch)
    results.append(output)  # Stores tensor with gradients!

# Memory usage: Grows with number of batches

# FIX - Detach from graph
results = []
for batch in dataloader:
    output = model(batch)
    results.append(output.detach().cpu())  # ✓ No gradients, on CPU

# Or just store values
results.append(output.item())  # For scalars
```

### 4. GPU Memory Not Released

```python
# LEAK - Tensors stay on GPU
for i in range(1000):
    data_gpu = data.cuda()
    result_gpu = model(data_gpu)
    # Tensors accumulate on GPU!

# FIX - Move back to CPU
for i in range(1000):
    data_gpu = data.cuda()
    result_gpu = model(data_gpu)
    result_cpu = result_gpu.cpu()  # ✓ Free GPU memory
    del data_gpu, result_gpu  # Explicit cleanup
    torch.cuda.empty_cache()  # Optionally clear cache
```

### 5. Circular References

```python
# LEAK - Circular reference prevents GC
class Node:
    def __init__(self):
        self.children = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self  # Circular reference!

# FIX - Use weak references
import weakref

class Node:
    def __init__(self):
        self.children = []
        self._parent = None

    @property
    def parent(self):
        return self._parent() if self._parent else None

    @parent.setter
    def parent(self, value):
        self._parent = weakref.ref(value) if value else None  # ✓ Weak ref
```

### 6. Global State Accumulation

```python
# LEAK - Appending to global list
global_results = []

def process(data):
    result = expensive_computation(data)
    global_results.append(result)  # Never cleared!

# FIX - Clear periodically or use local storage
def process(data, results_list):
    result = expensive_computation(data)
    results_list.append(result)
    return result

# Or clear when done
global_results = []
process_all(data)
# ... use results ...
global_results.clear()  # ✓ Free memory
```

## Detection Tools

### 1. Memory Profiler

```bash
# Install
uv add --dev memory-profiler

# Use decorator
from memory_profiler import profile

@profile
def train_model():
    for epoch in range(100):
        # Training code
        pass

# Run and see line-by-line memory usage
python -m memory_profiler script.py
```

### 2. tracemalloc (Built-in)

```python
import tracemalloc

# Start tracing
tracemalloc.start()

# Your code
for i in range(100):
    process_data()

    if i % 10 == 0:
        # Check memory usage
        current, peak = tracemalloc.get_traced_memory()
        print(f"Iteration {i}: "
              f"Current: {current / 1024 / 1024:.1f}MB "
              f"Peak: {peak / 1024 / 1024:.1f}MB")

# Get top memory allocations
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Top 10 memory allocations:")
for stat in top_stats[:10]:
    print(stat)

tracemalloc.stop()
```

### 3. PyTorch GPU Memory Tracking

```python
import torch

def print_gpu_memory():
    """Print current GPU memory usage."""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**2
        reserved = torch.cuda.memory_reserved() / 1024**2
        print(f"GPU Memory: Allocated={allocated:.1f}MB, "
              f"Reserved={reserved:.1f}MB")

# Use during training
for epoch in range(100):
    train_epoch()

    if epoch % 10 == 0:
        print_gpu_memory()
        print(torch.cuda.memory_summary())  # Detailed stats
```

### 4. objgraph (Find Reference Cycles)

```bash
uv add --dev objgraph
```

```python
import objgraph
import gc

# Create some objects
model = MyModel()
# ... use model ...

# Find objects that might leak
objgraph.show_most_common_types(limit=20)

# Find references to specific object
objgraph.show_refs([model], filename='refs.png')

# Find garbage (objects with circular refs)
gc.collect()
objgraph.show_most_common_types(limit=20)
```

## PRISM-Specific Leak Patterns

### Visualization Loops

```python
# LEAK - PRISM visualization during training
for sample_idx in range(n_samples):
    measurement = telescope.measure(image, centers[sample_idx])

    # Visualize current state
    vis.plot_meas_agg(meas_agg, current_rec)  # Creates figures!

    loss = criterion(prediction, measurement)
    loss.backward()

# FIX - Close figures or disable visualization
for sample_idx in range(n_samples):
    measurement = telescope.measure(image, centers[sample_idx])

    # Only visualize occasionally
    if sample_idx % 10 == 0 and not args.debug:
        fig = vis.plot_meas_agg(meas_agg, current_rec)
        plt.close(fig)  # ✓ Close figure

    loss = criterion(prediction, measurement)
    loss.backward()
```

### Measurement Accumulation

```python
# LEAK - Storing all measurements
class TelescopeAgg:
    def __init__(self):
        self.measurements = []  # Grows without bound!

    def add_measurement(self, meas):
        self.measurements.append(meas)  # Keeps full history

# FIX - Only store what's needed
class TelescopeAgg:
    def __init__(self, max_history=100):
        self.measurements = []
        self.max_history = max_history

    def add_measurement(self, meas):
        # Store measurement efficiently
        self.measurements.append(meas.detach().cpu())  # ✓ Detach

        # Limit history
        if len(self.measurements) > self.max_history:
            self.measurements.pop(0)  # ✓ Remove old
```

### Loss Aggregation

```python
# LEAK - LossAgg keeps full computational graph
class LossAgg:
    def __init__(self):
        self.losses = []

    def add_loss(self, loss):
        self.losses.append(loss)  # Keeps gradients!

    def total_loss(self):
        return sum(self.losses)

# FIX - Detach or accumulate immediately
class LossAgg:
    def __init__(self):
        self.total = 0
        self.count = 0

    def add_loss(self, loss):
        self.total += loss.detach().item()  # ✓ Just the value
        self.count += 1

    def mean_loss(self):
        return self.total / self.count if self.count > 0 else 0
```

## Detection Workflow

### Step 1: Monitor Memory Over Time

```python
import psutil
import os

def get_memory_usage():
    """Get current process memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 ** 2

# Monitor during execution
memory_samples = []
for i in range(1000):
    process_batch(data[i])

    if i % 10 == 0:
        mem = get_memory_usage()
        memory_samples.append(mem)
        print(f"Iteration {i}: {mem:.1f}MB")

# Check if memory grows
import numpy as np
trend = np.polyfit(range(len(memory_samples)), memory_samples, 1)[0]
if trend > 1:  # Growing > 1MB per 10 iterations
    print(f"⚠ Memory leak detected! Growth rate: {trend:.2f}MB per 10 iters")
```

### Step 2: Profile Suspicious Code

Use memory_profiler on functions with memory growth:

```python
@profile
def suspicious_function():
    # Code that might leak
    pass
```

### Step 3: Check Common Leak Sources

1. **Matplotlib figures**: Search for `plt.figure()` without `plt.close()`
2. **Tensor lists**: Search for `.append(tensor)` - should be `.append(tensor.detach().cpu())`
3. **Global lists**: Search for `global` variables that accumulate
4. **Missing optimizer.zero_grad()**: Every training loop should have it

### Step 4: Fix and Verify

After fixing:
```python
# Before fix
initial_mem = get_memory_usage()
for i in range(1000):
    process_batch(data[i])
final_mem = get_memory_usage()
growth = final_mem - initial_mem
print(f"Memory growth: {growth:.1f}MB")  # Should be near 0
```

## Best Practices

### Use Context Managers

```python
# Good pattern for resources
class ResourceManager:
    def __enter__(self):
        self.resource = allocate_resource()
        return self.resource

    def __exit__(self, *args):
        free_resource(self.resource)  # Always cleaned up

with ResourceManager() as resource:
    use(resource)
# Guaranteed cleanup
```

### Periodic Cleanup

```python
# Clear caches periodically
for epoch in range(1000):
    train_epoch()

    if epoch % 100 == 0:
        torch.cuda.empty_cache()  # Clear CUDA cache
        gc.collect()  # Run garbage collector
```

### Limit History Size

```python
# Don't keep unlimited history
class Tracker:
    def __init__(self, max_size=1000):
        self.history = deque(maxlen=max_size)  # ✓ Bounded

    def add(self, value):
        self.history.append(value)  # Old values auto-removed
```

### Use torch.no_grad() for Inference

```python
# Inference doesn't need gradients
@torch.no_grad()
def evaluate(model, data):
    predictions = model(data)  # No computational graph!
    return predictions
```

## Validation Checklist

Memory leak fixed when:
- [ ] Memory usage is stable over time (no growth trend)
- [ ] GPU memory doesn't fill up during training
- [ ] No OutOfMemoryError after many iterations
- [ ] Memory profiler shows no continuous allocation
- [ ] Figures are properly closed
- [ ] Gradients are cleared each iteration
- [ ] Tensors are detached when storing
- [ ] GPU tensors moved to CPU when done

## Emergency Fixes

If memory leak is severe but fix is complex:

```python
# Temporary workaround - restart periodically
for epoch in range(total_epochs):
    train_epoch()

    # Save checkpoint every N epochs
    if epoch % 100 == 0:
        save_checkpoint(model, epoch)

        # Restart process (clears all memory)
        # Then load checkpoint and continue
        if epoch < total_epochs - 1:
            import sys
            os.execv(sys.executable, ['python'] + sys.argv)
```

Better: Fix the actual leak!
