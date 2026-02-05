---
name: loop-vectorizer
description: Convert Python loops to vectorized PyTorch tensor operations for performance. This skill should be used when optimizing computational bottlenecks in PyTorch code during Phase 4 performance optimization.
---

# Loop Vectorizer

Convert inefficient Python loops into fast vectorized PyTorch tensor operations, achieving significant performance improvements.

## Purpose

Python loops are slow. PyTorch tensor operations are fast (especially on GPU). This skill systematically identifies loops that can be vectorized and converts them to efficient tensor operations.

## When to Use

Use this skill when:
- Profiling reveals loop bottlenecks
- Processing large batches or datasets
- Phase 4 (Performance Optimization) tasks
- Code has nested loops over arrays/tensors
- GPU utilization is low

## Performance Impact

Typical speedups:
- Simple loops: 10-100x faster
- Nested loops: 100-1000x faster
- With GPU: 100-10000x faster

## Vectorization Patterns

### Pattern 1: Element-wise Operations

```python
# Before - Python loop (SLOW)
result = []
for x in data:
    result.append(x ** 2 + 3 * x + 1)
result = torch.tensor(result)

# After - Vectorized (FAST)
result = data ** 2 + 3 * data + 1

# Speedup: ~100x
```

### Pattern 2: Batch Processing

```python
# Before - Loop over batch (SLOW)
outputs = []
for i in range(len(images)):
    output = model(images[i].unsqueeze(0))
    outputs.append(output)
outputs = torch.cat(outputs)

# After - Batch processing (FAST)
outputs = model(images)  # Process entire batch at once

# Speedup: ~50-100x (+ GPU optimization)
```

### Pattern 3: Conditional Operations

```python
# Before - Loop with condition (SLOW)
result = []
for x in data:
    if x > threshold:
        result.append(x * 2)
    else:
        result.append(x / 2)
result = torch.tensor(result)

# After - Vectorized with where (FAST)
result = torch.where(data > threshold, data * 2, data / 2)

# Speedup: ~50x
```

### Pattern 4: Reductions

```python
# Before - Loop for sum/mean (SLOW)
total = 0
for x in data:
    total += x ** 2
mean_square = total / len(data)

# After - Vectorized reduction (FAST)
mean_square = (data ** 2).mean()

# Or for multiple operations:
squared = data ** 2
total = squared.sum()
mean_square = squared.mean()

# Speedup: ~100x
```

### Pattern 5: Matrix Operations

```python
# Before - Nested loops for matrix multiply (VERY SLOW)
result = torch.zeros(m, n)
for i in range(m):
    for j in range(n):
        for k in range(p):
            result[i, j] += A[i, k] * B[k, j]

# After - Matrix multiplication (VERY FAST)
result = A @ B  # or torch.matmul(A, B)

# Speedup: ~1000x (10000x on GPU)
```

### Pattern 6: Broadcasting

```python
# Before - Loop to apply operation (SLOW)
result = torch.zeros(B, C, H, W)
for b in range(B):
    for c in range(C):
        result[b, c] = image[b, c] * mask  # mask is [H, W]

# After - Broadcasting (FAST)
result = image * mask  # Automatically broadcasts [H,W] to [B,C,H,W]

# Speedup: ~100x
```

## PRISM-Specific Vectorizations

### Telescope Sampling Loop

```python
# Before - Loop over measurement positions (SLOW)
measurements = []
for center in centers:  # 100 positions
    mask = telescope.create_mask(center, radius)  # [H, W]
    measurement = image * mask  # [1, 1, H, W] * [H, W]
    measurements.append(measurement)
measurements = torch.stack(measurements)  # [100, 1, 1, H, W]

# After - Vectorized mask creation (FAST)
def create_all_masks(centers: list[tuple], radius: float) -> Tensor:
    """Create all masks at once [N, H, W]."""
    N = len(centers)
    y, x = torch.meshgrid(
        torch.arange(H) - H//2,
        torch.arange(W) - W//2,
        indexing='ij'
    )  # [H, W]

    # Stack center coordinates [N, 2]
    centers_t = torch.tensor(centers)  # [N, 2]

    # Broadcast to compute distances [N, H, W]
    dy = y[None, :, :] - centers_t[:, 0, None, None]  # [N, H, W]
    dx = x[None, :, :] - centers_t[:, 1, None, None]  # [N, H, W]
    dist = torch.sqrt(dy**2 + dx**2)  # [N, H, W]

    masks = (dist <= radius).float()  # [N, H, W]
    return masks

# Use vectorized masks
masks = create_all_masks(centers, radius)  # [N, H, W]
measurements = image.unsqueeze(0) * masks.unsqueeze(1)  # [N, 1, H, W]

# Speedup: ~100x for 100 positions
```

### FFT on Multiple Images

```python
# Before - Loop over images (SLOW)
freq_images = []
for img in images:  # 100 images
    freq = torch.fft.fft2(img)
    freq_images.append(freq)
freq_images = torch.stack(freq_images)

# After - Batch FFT (FAST)
freq_images = torch.fft.fft2(images)  # Process all at once

# Speedup: ~50x (FFT is already optimized, but batch is faster)
```

### Loss Computation Over Measurements

```python
# Before - Loop over measurements (SLOW)
total_loss = 0
for i, (mask, target) in enumerate(zip(masks, targets)):
    pred_masked = prediction * mask
    loss = criterion(pred_masked, target)
    total_loss += loss

# After - Vectorized loss (FAST)
# Broadcast prediction [1, C, H, W] with masks [N, 1, H, W]
pred_masked = prediction.unsqueeze(0) * masks.unsqueeze(1)  # [N, C, H, W]

# Compute all losses at once
losses = criterion(pred_masked, targets)  # [N] or scalar depending on reduction

# Aggregate
total_loss = losses.sum()  # or .mean()

# Speedup: ~50x
```

## Advanced Vectorization

### Einstein Summation (einsum)

For complex tensor operations:

```python
# Before - Nested loops (VERY SLOW)
# Compute: output[b, o, h, w] = sum_i input[b, i, h, w] * weight[o, i]
output = torch.zeros(B, O, H, W)
for b in range(B):
    for o in range(O):
        for i in range(I):
            output[b, o] += input[b, i] * weight[o, i]

# After - einsum (VERY FAST)
output = torch.einsum('bihw,oi->bohw', input, weight)

# Speedup: ~1000x
```

Common einsum patterns:
```python
# Matrix multiply: C = A @ B
C = torch.einsum('ik,kj->ij', A, B)

# Batch matrix multiply
C = torch.einsum('bik,bkj->bij', A, B)

# Trace
trace = torch.einsum('ii->', A)

# Diagonal
diag = torch.einsum('ii->i', A)

# Outer product
outer = torch.einsum('i,j->ij', a, b)

# Attention weights: softmax(Q @ K^T / sqrt(d)) @ V
attn = torch.einsum('bqd,bkd->bqk', Q, K)  # Q @ K^T
scores = torch.softmax(attn / math.sqrt(d), dim=-1)
output = torch.einsum('bqk,bkd->bqd', scores, V)  # scores @ V
```

### Gather and Scatter Operations

For indexed operations:

```python
# Before - Loop with indexing (SLOW)
output = torch.zeros(N, D)
for i, idx in enumerate(indices):
    output[i] = data[idx]

# After - Gather (FAST)
output = data[indices]  # Advanced indexing

# Or for more complex cases:
output = torch.gather(data, dim=0, index=indices)

# Speedup: ~50x
```

### Masked Operations

```python
# Before - Loop with condition (SLOW)
valid_data = []
for i, (x, m) in enumerate(zip(data, mask)):
    if m:
        valid_data.append(x)
valid_data = torch.stack(valid_data)

# After - Boolean indexing (FAST)
valid_data = data[mask]

# Speedup: ~50x
```

## Vectorization Workflow

### Step 1: Identify Loop Bottlenecks

Profile to find slow loops:
```python
import time

start = time.time()
for x in data:
    result = process(x)
elapsed = time.time() - start
print(f"Loop time: {elapsed:.3f}s")
```

### Step 2: Analyze Loop Dependencies

Ask:
- Does iteration `i` depend on iteration `i-1`?
  - **No**: Can vectorize! ✅
  - **Yes**: May need different approach

- Are operations element-wise or reducible?
  - **Element-wise**: Use broadcasting
  - **Reduction**: Use `.sum()`, `.mean()`, etc.

### Step 3: Convert to Tensor Operations

Apply appropriate pattern:
1. Element-wise → Broadcasting
2. Nested loops → Matrix ops or einsum
3. Conditionals → `torch.where()` or boolean indexing
4. Reductions → `.sum()`, `.mean()`, `.max()`, etc.

### Step 4: Benchmark

Compare before and after:
```python
def benchmark(func, *args, n_runs=100):
    """Benchmark function."""
    # Warmup
    for _ in range(10):
        func(*args)

    torch.cuda.synchronize()
    start = time.time()

    for _ in range(n_runs):
        func(*args)

    torch.cuda.synchronize()
    elapsed = time.time() - start

    return elapsed / n_runs

old_time = benchmark(loop_version, data)
new_time = benchmark(vectorized_version, data)

print(f"Speedup: {old_time / new_time:.1f}x")
print(f"Old: {old_time*1000:.2f}ms, New: {new_time*1000:.2f}ms")
```

## Common Pitfalls

### Pitfall 1: Creating Too Many Intermediate Tensors

```python
# Bad - Creates many intermediate tensors
result = data.clone()
result = result + 1
result = result * 2
result = result / 3

# Good - Fused operations
result = (data + 1) * 2 / 3
```

### Pitfall 2: Unnecessary CPU-GPU Transfers

```python
# Bad - Transfer in loop
for x in data_cpu:
    x_gpu = x.cuda()
    result = model(x_gpu)
    result_cpu = result.cpu()

# Good - Transfer once
data_gpu = data_cpu.cuda()
results_gpu = model(data_gpu)
results_cpu = results_gpu.cpu()
```

### Pitfall 3: Not Using In-Place Operations

```python
# Bad - Creates new tensor
x = x + 1

# Good - In-place (when safe)
x += 1  # or x.add_(1)
```

### Pitfall 4: Ignoring Memory Usage

```python
# Bad - Creates huge tensor [N, M, H, W]
distances = torch.zeros(N, M, H, W)
for i in range(N):
    for j in range(M):
        distances[i, j] = compute_distance(points[i], points[j])

# Better - Compute in chunks
chunk_size = 100
for i in range(0, N, chunk_size):
    chunk = compute_distances(points[i:i+chunk_size], points)
    process(chunk)
```

## Special Cases: Non-Vectorizable Loops

Some loops cannot be fully vectorized:

### Sequential Dependencies

```python
# Cannot vectorize - depends on previous iteration
for i in range(1, len(data)):
    data[i] = data[i] + data[i-1]  # Cumulative sum

# Solution: Use torch.cumsum
data = torch.cumsum(data, dim=0)
```

### Dynamic Shapes

```python
# Hard to vectorize - different sizes
results = []
for x in data:
    # Each x may produce different size output
    result = process_variable_size(x)
    results.append(result)

# Solution: Pad to max size or use packed sequences
```

### Complex Control Flow

```python
# Hard to vectorize - complex branching
for x in data:
    if condition1(x):
        result = path1(x)
    elif condition2(x):
        result = path2(x)
    else:
        result = path3(x)

# Partial solution: Vectorize each path separately
mask1 = condition1(data)
mask2 = condition2(data)
mask3 = ~(mask1 | mask2)

result = torch.zeros_like(data)
result[mask1] = path1(data[mask1])
result[mask2] = path2(data[mask2])
result[mask3] = path3(data[mask3])
```

## Validation Checklist

After vectorization:
- [ ] Benchmark shows speedup
- [ ] Results are identical (or within numerical precision)
- [ ] Memory usage is acceptable
- [ ] Code is more readable (or at least not worse)
- [ ] GPU utilization improved (if using GPU)

## Verification

Always verify correctness:
```python
# Verify vectorized version matches loop version
torch.manual_seed(42)
data = torch.randn(100, 256, 256)

result_loop = loop_version(data)
result_vectorized = vectorized_version(data)

assert torch.allclose(result_loop, result_vectorized, rtol=1e-5)
print("✓ Results match!")
```
