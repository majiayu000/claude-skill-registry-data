---
name: mdad
description: Evaluates the reliability of micro-benchmarks in preserving pairwise model rankings compared to full benchmark performance. It quantifies the minimum accuracy gap required between two models for a small sampled subset to consistently rank them correctly. Use when the user has predictions and gold and needs to compute MDAD.
metadata:
  skill_kind: metric
  source_arxiv: 2510.08730
  bibtex_key: yauney2025microbenchmarkingreliability
  confidence: high
---

# mdad

> How Reliable is Language Model Micro-Benchmarking? — Yauney et al. (2025) (arXiv:2510.08730, 2025)

## What this evaluates

Evaluates the reliability of micro-benchmarks in preserving pairwise model rankings compared to full benchmark performance. It quantifies the minimum accuracy gap required between two models for a small sampled subset to consistently rank them correctly.

## Datasets

- **MMLU** — total ?; splits: test (-1)
- **MMLU-Pro** — total ?; splits: test (-1)
- **BBH** — total ?; splits: test (-1)
- **GPQA** — total ?; splits: test (-1)

## Metrics

- `MDAD` **(primary)** — range: percent
  - Minimum Detectable Ability Difference: the smallest accuracy difference between two models on the full benchmark such that a micro-benchmark correctly preserves their relative ranking with high probability. Lower values indicate higher reliability.
- `Agreement` — range: [0, 1]
  - Pairwise ranking preservation rate between micro-benchmark and full benchmark evaluations.
- `Mean estimation error` — range: percent
  - Average absolute difference between a single model's accuracy on the micro-benchmark versus the full benchmark.
- `Kendall’s tau rank correlation` — range: [-1, 1]
  - Correlation between the rank order of models on the micro-benchmark and the full benchmark.

## Input / output format

**Input**: Per-model accuracy scores computed on both the full benchmark and a sampled micro-benchmark subset.

**Output**: MDAD value (in percentage points) representing the minimum full-benchmark accuracy difference required for reliable pairwise ranking preservation on the micro-benchmark.

## Scoring recipe

```python
def compute_mdad(full_acc, micro_acc):
    pairs = [(m1, m2) for m1 in full_acc for m2 in full_acc if m1 < m2]
    diffs = sorted(set(abs(full_acc[m1] - full_acc[m2]) for m1, m2 in pairs))
    for d in diffs:
        matching = sum(1 for m1, m2 in pairs if abs(full_acc[m1]-full_acc[m2]) == d and 
                       (full_acc[m1] > full_acc[m2]) == (micro_acc[m1] > micro_acc[m2]))
        if matching / len(pairs) >= 0.5:
            return d
    return diffs[-1]
```

## Common pitfalls

- Confusing MDAD with mean estimation error, which only measures single-model bias and ignores consistent over/under-estimation across models that still preserve correct pairwise rankings.
- Assuming high aggregate rank correlation (Kendall's tau) implies reliable pairwise comparisons at small dataset sizes, whereas MDAD reveals that methods like random sampling can still fail to distinguish closely performing models.
- Ignoring that micro-benchmark reliability heavily depends on the accuracy gap between compared models; top-ranked models are easier to rank correctly than mid-tier models with similar scores.

## Evidence (verbatim from paper)

> When 10 examples are selected from BBH, Anchor Points achieves an MDAD of 6. If a model pair differs by more than 6 points on the full BBH then this micro-benchmark is likely to correctly rank these models. If a model pair has an accuracy difference on the full BBH of less than the MDAD, e.g. 2 points of accuracy, then this micro-benchmark is unlikely to correctly rank these models.

## Citation

```bibtex
@misc{yauney2025microbenchmarkingreliability,
  title={How Reliable is Language Model Micro-Benchmarking?},
  author={Yauney et al. (2025)},
  year={2025},
  note={arXiv:2510.08730}
}
```

- arXiv: 2510.08730
