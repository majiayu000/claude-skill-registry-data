---
name: NDCG@10
description: Evaluates how well internal model representations (hidden states) can predict token-level information importance in summarization tasks. It probes whether specific transformer layers or cross-layer combinations encode salience distributions consistent with empirical importance derived from summary persistence. Use when the user has predictions and gold and needs to compute NDCG@10.
metadata:
  skill_kind: metric
  source_arxiv: 2602.00459
  bibtex_key: zhou2026whatmatters
  confidence: high
---

# NDCG@10

> What Matters to an LLM? Behavioral and Computational Evidences from Summarization — Zhou et al. (2026) (arXiv:2602.00459, 2026)

## What this evaluates

Evaluates how well internal model representations (hidden states) can predict token-level information importance in summarization tasks. It probes whether specific transformer layers or cross-layer combinations encode salience distributions consistent with empirical importance derived from summary persistence.

## Datasets

- **CNN/DailyMail** — total ?; splits: (unstated)
- **SAMSum** — total ?; splits: (unstated)

## Metrics

- `NDCG@10` **(primary)** — range: [0, 1]
  - Normalized Discounted Cumulative Gain at rank 10. Measures the quality of the top-10 ranked tokens based on predicted importance scores relative to ground truth importance, normalized by the ideal ranking (IDCG).
- `Spearman’s rank correlation` — range: [0, 1]
  - Non-parametric measure of rank correlation. Computes the Pearson correlation between the rank-transformed predicted importance scores and true importance scores across all tokens.

## Input / output format

**Input**: Hidden state vectors associated with individual tokens at a specified transformer layer (or concatenated across all layers). For words occurring multiple times, their hidden state vectors are averaged to yield a single representation per word.

**Output**: A scalar importance score per token (or per averaged word representation).

## Scoring recipe

```python
def compute_ndcg10(pred_scores, true_scores):
    top_k = 10
    pred_rank = np.argsort(-pred_scores)[:top_k]
    true_rank = np.argsort(-true_scores)[:top_k]
    dcg = sum(1.0 / np.log2(i + 2) for i, idx in enumerate(pred_rank) if true_scores[idx] > 0)
    idcg = sum(1.0 / np.log2(i + 2) for i, idx in enumerate(true_rank) if true_scores[idx] > 0)
    return dcg / idcg if idcg > 0 else 0.0

def compute_spearman(pred_scores, true_scores):
    return scipy.stats.spearmanr(pred_scores, true_scores).correlation
```

## Common pitfalls

- Confusing the probe's internal 60:20:20 train/validation/test split with the dataset's official split.
- Averaging hidden states for repeated words before probing changes token-level granularity, making direct comparison with standard token-wise probing baselines invalid.
- NDCG@10 only evaluates the top-10 tokens, potentially masking poor performance on the remainder of the document, unlike Spearman which uses all tokens.

## Evidence (verbatim from paper)

> Performance is reported on the test set using Spearman’s rank correlation and NDCG@10. Further results for all model–dataset pairs are reported in Appendix Tables[5] and[6].

## Citation

```bibtex
@misc{zhou2026whatmatters,
  title={What Matters to an LLM? Behavioral and Computational Evidences from Summarization},
  author={Zhou et al. (2026)},
  year={2026},
  note={arXiv:2602.00459}
}
```

- arXiv: 2602.00459
