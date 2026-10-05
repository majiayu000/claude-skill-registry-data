---
name: TEC
description: Evaluates the joint optimization of AI service placement and resource allocation in mobile edge computing by measuring the trade-off between computation time and energy consumption across varying network scales and task characteristics. Use when the user has predictions and gold and needs to compute TEC.
metadata:
  skill_kind: metric
  source_arxiv: 2011.05708
  bibtex_key: lin2020optimizing
  confidence: high
---

# TEC

> Optimizing AI Service Placement and Resource Allocation in Mobile Edge Intelligence Systems — Lin et al. (2020) (arXiv:2011.05708, 2020)

## What this evaluates

Evaluates the joint optimization of AI service placement and resource allocation in mobile edge computing by measuring the trade-off between computation time and energy consumption across varying network scales and task characteristics.

## Datasets

- (no dataset; pure metric skill)

## Metrics

- `TEC` **(primary)** — range: other
  - Weighted sum of total computation time and total energy consumption: $\beta \times \text{Time} + (1-\beta) \times \text{Energy}$, where $\beta$ is a user-defined weighting parameter balancing the two objectives.

## Input / output format

**Input**: System configuration parameters including number of users $K$, program size $S$, per-user task data size $I_k$, channel gains $g_k$ and $h_k$, computing workload $C$, bandwidth $W$, noise power $N_0$, and power constraints.

**Output**: Per-user decisions on service placement (local compute vs. offload), uplink/downlink bandwidth allocation fractions, and edge CPU frequency allocation.

## Scoring recipe

```python
def compute_tec(total_time, total_energy, beta):
    tec = beta * total_time + (1 - beta) * total_energy
    return tec
```

## Common pitfalls

- The TEC metric is a weighted sum, not a physical quantity; changing $\beta$ drastically shifts the optimal scheme and trade-off curve.
- The 'Optimal' baseline is only computationally tractable for small $K$ (≤10); comparisons for larger $K$ must exclude it due to exponential complexity.
- Channel models use specific Rayleigh fading parameters and a 0.75 correlation coefficient between uplink and downlink that must be replicated exactly for fair comparison.

## Evidence (verbatim from paper)

> In Fig. 4, we compare the TEC performance achieved by different schemes when the program size $S$ varies. Besides, we present the TEC performance comparison when the task data size $I$ varies in Fig. 5. From both figures, we observe that the TEC performance achieved by the proposed greedy search and ADMM-based methods are extremely close to the optimal scheme.

## Citation

```bibtex
@misc{lin2020optimizing,
  title={Optimizing AI Service Placement and Resource Allocation in Mobile Edge Intelligence Systems},
  author={Lin et al. (2020)},
  year={2020},
  note={arXiv:2011.05708}
}
```

- arXiv: 2011.05708
