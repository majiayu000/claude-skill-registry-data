---
name: score
description: This framework audits medical LLM benchmarks across five lifecycle phases using 46 medically tailored criteria to assess clinical relevance, data integrity, safety-critical capabilities, validity, and governance. Use when the user has predictions and gold and needs to compute score.
metadata:
  skill_kind: metric
  source_arxiv: 2508.04325
  bibtex_key: ma2025beyond
  confidence: high
---

# score

> Beyond the Leaderboard: Rethinking Medical Benchmarks for Large Language Models — Ma et al. (2025) (arXiv:2508.04325, 2025)

## What this evaluates

This framework audits medical LLM benchmarks across five lifecycle phases using 46 medically tailored criteria to assess clinical relevance, data integrity, safety-critical capabilities, validity, and governance.

## Datasets

- (no dataset; pure metric skill)

## Metrics

- `score` **(primary)** — range: percent
  - Count of satisfied criteria out of 46 total across five phases (Design, Dataset Construction, Technical Implementation, Benchmark Validity, Documentation/Governance), reported as a percentage.

## Input / output format

**Input**: Documentation and design details of a medical LLM benchmark to be audited.

**Output**: Binary or categorical assessment for each of the 46 MedCheck criteria.

## Scoring recipe

```python
def compute_score(benchmark):
    satisfied = sum(1 for c in criteria if benchmark.meets(c))
    return (satisfied / 46) * 100
```

## Common pitfalls

- Scoring relies on qualitative expert judgment rather than automated computation, risking subjectivity.
- The score evaluates benchmark design quality, not model inference performance, so it cannot replace standard accuracy metrics.

## Evidence (verbatim from paper)

> This phase is the most underdeveloped in our analysis (average score: 52.4%), revealing a profound gap between current practice and the requirements for reliable medical AI.

## Citation

```bibtex
@misc{ma2025beyond,
  title={Beyond the Leaderboard: Rethinking Medical Benchmarks for Large Language Models},
  author={Ma et al. (2025)},
  year={2025},
  note={arXiv:2508.04325}
}
```

- arXiv: 2508.04325
