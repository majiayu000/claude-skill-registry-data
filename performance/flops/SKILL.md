---
name: flops
description: This protocol evaluates the computational throughput and real-time efficiency of embedded CPU and GPU platforms. It measures peak floating-point operations per second (FLOPS) using a controlled matrix rotation kernel, and assesses practical system performance via end-to-end inference latency and power consumption on a robotic vision pipeline. Use when the user has predictions and gold and needs to compute FLOPS.
metadata:
  skill_kind: metric
  source_arxiv: 1809.03668
  bibtex_key: biddulph2018comparing
  confidence: high
---

# flops

> Comparing Computing Platforms for Deep Learning on a Humanoid Robot — Biddulph et al. (2018) (arXiv:1809.03668, 2018)

## What this evaluates

This protocol evaluates the computational throughput and real-time efficiency of embedded CPU and GPU platforms. It measures peak floating-point operations per second (FLOPS) using a controlled matrix rotation kernel, and assesses practical system performance via end-to-end inference latency and power consumption on a robotic vision pipeline.

## Datasets

- **MS COCO (pre-training source)** — total ?; splits: (unstated)

## Metrics

- `FLOPS` **(primary)** — range: other
  - Calculated as (6 * D * N * W) / t, where D is data dimensionality, N is iterations (40,000), W is number of workers (256 to 1,024,000), and t is elapsed time in seconds. Measures peak floating-point throughput without main memory access bottlenecks.
- `inference_latency` — range: other
  - End-to-end processing time per frame through the demosaicing, reprojection, and SSD MobileNet detection pipeline.
- `power_consumption` — range: other
  - Electrical power drawn by the computing platform during pipeline execution, measured via current draw from the power supply.

## Input / output format

**Input**: FLOPS benchmark: 2D rotation matrices and vectors with configurable dimensionality (1D, 2D, 4D). Vision pipeline: 1280×1024 Bayer-format images streamed at up to 60 fps from a 195° FOV equidistant camera.

**Output**: FLOPS benchmark: Final scalar output from the kernel to prevent compiler optimization. Vision pipeline: Rectilinear RGB images and pedestrian bounding boxes; system-level power/current readings.

## Scoring recipe

```python
# FLOPS Calculation
D = dimensionality  # 1, 2, or 4
N = 40000           # iterations
W = num_workers     # 256 to 1,024,000
t = elapsed_time_seconds
flops = (6 * D * N * W) / t

# Latency & Power
latency = (end_timestamp - start_timestamp) / num_frames
power = current_draw_amps * supply_voltage_volts
```

## Common pitfalls

- Data transfer overheads between host memory and device memory can dwarf actual computation time, making GPU usage ineffective if not accounted for.
- Compilers may optimize away redundant calculations; a dummy output operation is required to force full execution and accurate timing.
- Power measurements must be taken under sustained load from the power supply, as idle or burst measurements misrepresent embedded robotic constraints.

## Evidence (verbatim from paper)

> The FLOPS measure is calculated using a 2D matrix multiplication operation. First, a 2D rotation matrix is created, and a 2D vector is rotated multiple times. Factoring in the dimensionality of the data (D), the number of iterations (N), the number of workers (W), and the time taken to complete all iterations (t), we can derive a formula for the number of floating point operations that the GPU can perform per second FLOPS = (6DNW)/t.

## Citation

```bibtex
@misc{biddulph2018comparing,
  title={Comparing Computing Platforms for Deep Learning on a Humanoid Robot},
  author={Biddulph et al. (2018)},
  year={2018},
  note={arXiv:1809.03668}
}
```

- arXiv: 1809.03668
