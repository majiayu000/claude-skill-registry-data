---
name: dior
description: Quantifies how sensitive a language model benchmark's reliability and ranking stability are to specific design choices, such as the selection of scenarios, subscenarios, examples, and few-shot prompts. Use when the user has predictions and gold and needs to compute DIoR.
metadata:
  skill_kind: metric
  source_arxiv: 2308.11696
  bibtex_key: perlitz2023efficientbenchmarking
  confidence: high
---

# dior

> Efficient Benchmarking of Language Models — Perlitz et al. (2023) (arXiv:2308.11696, 2023)

## What this evaluates

Quantifies how sensitive a language model benchmark's reliability and ranking stability are to specific design choices, such as the selection of scenarios, subscenarios, examples, and few-shot prompts.

## Datasets

- **HELM** — total ?; splits: test (-1)

## Metrics

- `DIoR` **(primary)** — range: [0, 1]
  - Decision Impact on Reliability measures the change in benchmark reliability (e.g., ranking stability or score variance) when a specific design choice is perturbed. It is computed via bootstrapping simulations that repeatedly resample the design choice and measure the probability of rank switches or score deviations across models.

## Input / output format

**Input**: A benchmark's design configuration (e.g., set of scenarios, subscenarios, examples, or few-shot prompt seeds) and the resulting model scores/rankings across these configurations.

**Output**: A DIoR reliability score indicating the sensitivity of the benchmark's outcomes to the perturbed design choice, typically expressed as a probability or stability metric.

## Scoring recipe

```python
def compute_dior(design_config, model_scores, n_iterations=1000):
    reliability_scores = []
    for _ in range(n_iterations):
        perturbed_config = bootstrap_sample(design_config)
        new_scores = evaluate_models(perturbed_config)
        reliability_scores.append(calculate_rank_stability(model_scores, new_scores))
    return 1 - mean(reliability_scores)
```

## Common pitfalls

- Treating DIoR as a direct measure of model capability rather than benchmark design sensitivity.
- Assuming that reducing the number of scenarios or subscenarios saves compute without penalty; the paper shows it drastically drops reliability.
- Using full cross-product evaluation for few-shot prompts instead of uniform sampling across the example-prompt space, which the paper shows yields lower reliability for the same compute budget.

## Evidence (verbatim from paper)

> proposes Decision Impact on Reliability (DIoR) to quantify how design choices affect reliability.

## Citation

```bibtex
@misc{perlitz2023efficientbenchmarking,
  title={Efficient Benchmarking of Language Models},
  author={Perlitz et al. (2023)},
  year={2023},
  note={arXiv:2308.11696}
}
```

- arXiv: 2308.11696
