---
name: latency
description: Measures the inference latency of binarized, 8-bit, and 32-bit convolutional layers on edge devices to evaluate the efficiency and speedup of the Larq Compute Engine framework compared to standard implementations. Use when the user has predictions and gold and needs to compute latency.
metadata:
  skill_kind: metric
  source_arxiv: 2011.09398
  bibtex_key: bannink2020larq
  confidence: high
---

# latency

> Larq Compute Engine: Design, Benchmark, and Deploy State-of-the-Art Binarized Neural Networks — Bannink et al. (2020) (arXiv:2011.09398, 2020)

## What this evaluates

Measures the inference latency of binarized, 8-bit, and 32-bit convolutional layers on edge devices to evaluate the efficiency and speedup of the Larq Compute Engine framework compared to standard implementations.

## Datasets

- **Synthetic-Conv-Dimensions** — total ?; splits: test (-1)

## Metrics

- `latency` **(primary)** — range: ms
  - Wall-clock execution time for a single forward pass of a convolutional layer on the target hardware.

## Input / output format

**Input**: Convolutional layer specifications: input height, input width, input channels, output channels, and kernel size (3x3 or 5x5).

**Output**: Execution latency in milliseconds (ms).

## Scoring recipe

```python
def compute_latency(conv_specs, framework, device):
    times = []
    for spec in conv_specs:
        model = build_conv_layer(spec)
        framework.load(model)
        framework.run(model, dummy_input)  # warmup
        start = time.perf_counter()
        framework.run(model, dummy_input)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # convert to ms
    return sum(times) / len(times)
```

## Common pitfalls

- Latency is highly platform-dependent and varies significantly across different hardware architectures, instruction sets, and inference frameworks.
- Overheads from bitpacking, im2col, and memory reads can cause deviations from theoretical MAC-based speedup predictions, especially for smaller convolutions.
- Framework fallbacks (e.g., to slower full-precision code) can dominate measured latency if not detected or disabled.

## Evidence (verbatim from paper)

> The measurements were taken on a Pixel 1 phone as well as a Raspberry Pi Model 4B with a 64-bit OS (Ubuntu LTS 20.04). ... Binarization reduces latency by 12-17x compared to the floating-point implementation, with the largest performance gains being in the layers with the most channels.

## Citation

```bibtex
@misc{bannink2020larq,
  title={Larq Compute Engine: Design, Benchmark, and Deploy State-of-the-Art Binarized Neural Networks},
  author={Bannink et al. (2020)},
  year={2020},
  note={arXiv:2011.09398}
}
```

- arXiv: 2011.09398
