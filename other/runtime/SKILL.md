---
name: runtime
description: Evaluates the inference latency and computational runtime of transformer models and individual MLX operations across different hardware platforms (Apple Silicon vs NVIDIA GPU) and input configurations. Use when the user has predictions and gold and needs to compute runtime.
metadata:
  skill_kind: metric
  source_arxiv: 2510.18921
  bibtex_key: ajayi2025mlxbenchmark
  confidence: high
---

# runtime

> Benchmarking On-Device Machine Learning on Apple Silicon with MLX — Ajayi et al. (2025) (arXiv:2510.18921, 2025)

## What this evaluates

Evaluates the inference latency and computational runtime of transformer models and individual MLX operations across different hardware platforms (Apple Silicon vs NVIDIA GPU) and input configurations.

## Datasets

- **Hugging Face datasets (synthetic inputs)** — total ?; splits: (unstated)

## Metrics

- `runtime` **(primary)** — range: other
  - The wall-clock time required to complete a single forward pass or operation, measured in seconds or milliseconds. Reported as both per-iteration detailed runtime and mean runtime across multiple iterations.

## Input / output format

**Input**: Text sequences of specified character lengths (50, 100, 200, 500) grouped into batches of size 1, 16, or 32.

**Output**: Numerical runtime values (latency) per model, backend, input length, and batch size.

## Scoring recipe

```python
def compute_metric(predictions, gold):
    # predictions: list of raw runtimes per iteration
    # gold: metadata dict (model, backend, length, batch_size)
    mean_runtime = sum(predictions) / len(predictions)
    return {"mean_runtime": mean_runtime, "iterations": len(predictions)}
```

## Common pitfalls

- Hardware thermal throttling on laptops can cause runtime variability across iterations.
- Comparisons across backends (mlx-cpu, mlx-gpu, torch-cpu, torch-cuda) may be confounded by differing framework optimizations and memory management strategies.
- Synthetic/random inputs do not reflect real-world distributional characteristics of standard NLP benchmarks.

## Evidence (verbatim from paper)

> We presented our results in two formats: Detailed Benchmarks, which provide runtime for each individual experiment, and Average Runtime Benchmarks, which calculate the mean runtime across iterations. The comprehensive results are available in the appendices.

## Citation

```bibtex
@misc{ajayi2025mlxbenchmark,
  title={Benchmarking On-Device Machine Learning on Apple Silicon with MLX},
  author={Ajayi et al. (2025)},
  year={2025},
  note={arXiv:2510.18921}
}
```

- arXiv: 2510.18921
