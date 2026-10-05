---
name: qqe
description: Evaluates whether citation growth outpaces publication expansion across leading AI/NLP conferences, measuring the elasticity of scholarly impact relative to scale-driven growth over a decade. Use when the user has predictions and gold and needs to compute QQE.
metadata:
  skill_kind: metric
  source_arxiv: 2512.04448
  bibtex_key: ma2025hasacllostitscrown
  confidence: high
---

# qqe

> Has ACL Lost Its Crown? A Decade-Long Quantitative Analysis of Scale and Impact Across Leading AI Conferences — Ma et al. (2025) (arXiv:2512.04448, 2025)

## What this evaluates

Evaluates whether citation growth outpaces publication expansion across leading AI/NLP conferences, measuring the elasticity of scholarly impact relative to scale-driven growth over a decade.

## Datasets

- **Leading AI/NLP Conferences (ACL, EMNLP, NAACL, AAAI, IJCAI, ICLR, NeurIPS)** — total ?; splits: 2014-2024 (-1)

## Metrics

- `QQE` **(primary)** — range: other (unitless ratio)
  - Quality-Quantity Elasticity; measures the elasticity of citation growth relative to publication/acceptance growth. Calculated as the ratio of annual citation growth rate to annual publication growth rate.
- `AC` — range: other
  - Average citations per paper; total citations divided by total accepted papers.
- `MC` — range: other
  - Median citations per paper; the middle value of the citation distribution.
- `HCR` — range: percent
  - Highly-cited ratio; percentage of papers exceeding a citation threshold.
- `ZCR` — range: percent
  - Zero-cited ratio; percentage of papers with zero citations.
- `Gini` — range: [0, 1]
  - Gini coefficient; measures inequality in the distribution of citations across papers.

## Input / output format

**Input**: Annual counts of accepted papers and their subsequent citation counts for each conference from 2014 to 2024.

**Output**: Computed bibliometric indices per conference, including QQE, average/median citations, highly-cited/zero-cited ratios, H-index variants, and citation network shares.

## Scoring recipe

```python
def compute_bibliometrics(papers):
    pub_count = len(papers)
    cite_counts = [p.citations for p in papers]
    ac = sum(cite_counts) / pub_count
    mc = sorted(cite_counts)[pub_count // 2]
    hcr = sum(1 for c in cite_counts if c > threshold) / pub_count
    zcr = sum(1 for c in cite_counts if c == 0) / pub_count
    return {'AC': ac, 'MC': mc, 'HCR': hcr, 'ZCR': zcr}

def compute_qqe(pub_series, cite_series):
    pub_growth = (pub_series[-1] - pub_series[0]) / pub_series[0]
    cite_growth = (cite_series[-1] - cite_series[0]) / cite_series[0]
    return cite_growth / pub_growth if pub_growth != 0 else float('inf')
```

## Common pitfalls

- QQE values fluctuate significantly year-to-year (e.g., negative values in some years), so trend analysis requires smoothing or long-term windows.
- Normalized metrics (e.g., Norm-H) adjust for scale, making direct comparison with absolute metrics (e.g., H-index) misleading without context.
- Citation counts depend heavily on the observation window; newer conferences or recent years will appear artificially low.

## Evidence (verbatim from paper)

> The QQE index evaluates whether citation growth outpaces publication expansion. All venues exhibit QQE > 1.0, indicating that scale growth has not diluted impact density.

## Citation

```bibtex
@misc{ma2025hasacllostitscrown,
  title={Has ACL Lost Its Crown? A Decade-Long Quantitative Analysis of Scale and Impact Across Leading AI Conferences},
  author={Ma et al. (2025)},
  year={2025},
  note={arXiv:2512.04448}
}
```

- arXiv: 2512.04448
