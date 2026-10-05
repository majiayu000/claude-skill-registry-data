---
name: feqa
description: Evaluates the faithfulness of abstractive summaries by generating questions from summary sentences and verifying if the answers can be extracted from the source document. It probes a model's ability to avoid hallucination and maintain factual grounding relative to the source text. Use when the user has predictions and gold and needs to compute FEQA.
metadata:
  skill_kind: metric
  source_arxiv: 2005.03754
  bibtex_key: durmus2020feqa
  confidence: high
---

# feqa

> FEQA: A Question Answering Evaluation Framework for Faithfulness Assessment in Abstractive Summarization — Durmus et al. (2020) (arXiv:2005.03754, 2020)

## What this evaluates

Evaluates the faithfulness of abstractive summaries by generating questions from summary sentences and verifying if the answers can be extracted from the source document. It probes a model's ability to avoid hallucination and maintain factual grounding relative to the source text.

## Datasets

- **CNN/DM** — total 748; splits: test (748); repo https://github.com/esdurmus/summary-faithfulness
- **XSum** — total 286; splits: test (286); repo https://github.com/esdurmus/summary-faithfulness

## Metrics

- `FEQA` **(primary)** — range: [-1, 1]
  - Generates questions from summary sentences, extracts answers from both the summary and the source document, and computes a match score (exact match or F1) between them. The final evaluation reports Pearson and Spearman correlation coefficients between these scores and human-annotated faithfulness judgments.

## Input / output format

**Input**: Document and summary sentence pairs (without reference summaries). Human-annotated faithfulness scores serve as ground truth.

**Output**: Per pair: a faithfulness score derived from the match between summary-derived and source-derived answers. Aggregated: Pearson and Spearman correlation coefficients against human scores.

## Scoring recipe

```python
def compute_feqa_evaluation(metric_scores, human_scores):
    # metric_scores: list of per-sentence faithfulness scores from FEQA
    # human_scores: list of corresponding human-annotated faithfulness scores
    pearson = pearsonr(metric_scores, human_scores)
    spearman = spearmanr(metric_scores, human_scores)
    return {"pearson": pearson, "spearman": spearman}
```

## Common pitfalls

- ROUGE and word-overlap metrics show high correlation with human faithfulness on extractive datasets (CNN/DM) but fail completely on abstractive ones (XSum).
- Entailment models often rely on lexical overlap heuristics, giving high scores to unfaithful summaries that share many words with the source.
- Content selection metrics (ROUGE vs reference) are frequently conflated with faithfulness metrics (ROUGE vs source), but they measure fundamentally different properties.

## Evidence (verbatim from paper)

> Table 7: Pearson (P) and Spearman (S) correlation between human-annotated faithfulness scores and the metric scores. *,** indicates p-values < 0.05, < 0.001, respectively. FEQA has the highest correlation with human scores for both CNN/DM and XSum.

## Citation

```bibtex
@misc{durmus2020feqa,
  title={FEQA: A Question Answering Evaluation Framework for Faithfulness Assessment in Abstractive Summarization},
  author={Durmus et al. (2020)},
  year={2020},
  note={arXiv:2005.03754}
}
```

- arXiv: 2005.03754
