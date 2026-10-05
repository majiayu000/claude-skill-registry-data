---
name: posh
description: Evaluates how well automated metrics and vision-language models can identify granular errors (attribute/relation misattachments) in detailed image descriptions and correctly rank paired descriptions against human judgments. Use when the user has predictions and gold and needs to compute macro F1, Spearman rank ρ.
metadata:
  skill_kind: metric
  source_arxiv: 2510.19060
  bibtex_key: ananthram2025posh
  confidence: high
---

# posh

> PoSh: Using Scene Graphs To Guide LLMs-as-a-Judge For Detailed Image Descriptions — Amith Ananthram et al. (2025) (arXiv:2510.19060, 2025)

## What this evaluates

Evaluates how well automated metrics and vision-language models can identify granular errors (attribute/relation misattachments) in detailed image descriptions and correctly rank paired descriptions against human judgments.

## Datasets

- **DOCENT** — total ?; splits: train (1000), test_granular (300), test_coarse (600); repo https://github.com/amith-ananthram/posh
- **CapArena** — total 3361; splits: test (5599)

## Metrics

- `macro F1` **(primary)** — range: [0, 1]
  - Token-level F1 score for identifying annotated mistake and omission spans in candidate descriptions. Credits or penalizes predictions per token.
- `pairwise accuracy` — range: [0, 1]
  - Percentage of pairs where the metric correctly predicts the better text or a tie. Uses a tie threshold inferred from the gold tie rate.
- `Spearman rank ρ` **(primary)** — range: [-1, 1]
  - Rank correlation between the metric's score difference (m(text1)−m(text2)) and the human gold score difference.
- `Kendall's τ` — range: [-1, 1]
  - Rank correlation measuring the concordance between metric predictions and human gold judgments on paired descriptions.

## Input / output format

**Input**: Image, candidate description text, gold reference description text, and scene graph components extracted from the text.

**Output**: Per scene graph component: a presence score (1-5) derived from weighted token logits. Per pair: a preference label (better/tie) or rank correlation value. Per span: a binary/mask score for mistakes/omissions.

## Scoring recipe

```python
def score_posh(image, candidate, reference):
    # 1. Extract sentence-level scene graphs & resolve co-references
    graphs = extract_scene_graphs(candidate, reference)
    # 2. Prompt LLM (qwen-3-14b) for templated presence questions
    logits = prompt_llm(graphs, candidate, reference)
    # 3. Compute presence scores via weighted avg over token logits for 1-5
    scores = weighted_avg_token_logits(logits, range=[1,5])
    # 4. Apply threshold of 2 for object presence
    presence = scores >= 2.0
    # 5. Compute granular macro F1 on token spans
    f1 = compute_macro_f1(predicted_spans=presence, gold_spans=annotated_mistakes)
    # 6. Compute coarse metrics for pairs
    acc = pairwise_accuracy(metric_diff, gold_diff, tie_thresh=gold_tie_rate)
    rho = spearman_corr(metric_diff, gold_diff)
    tau = kendall_tau(metric_diff, gold_diff)
    return f1, acc, rho, tau
```

## Common pitfalls

- The tie threshold for pairwise accuracy is not fixed; it must be inferred from the gold tie rate in the dataset.
- Granular F1 operates at the token level, so results are highly sensitive to the tokenizer used for the candidate and reference texts.
- CapArena contains significantly simpler images than DOCENT; high performance on CapArena does not guarantee robustness on complex, dynamic scenes.

## Evidence (verbatim from paper)

> We evaluate granular metrics on this benchmark using macro F1 where we credit/penalize a model for predicting each annotated/unannotated token. Our coarse judgments are in the form (text1, text2, score) where score indicates how much better or worse text1 is than text2. We evaluate each coarse metric m by calculating its 1) pairwise accuracy (whether it picks the better text or a tie, using a tie threshold inferred from the gold tie rate) and 2) Spearman rank ρ and Kendall's τ correlations between m(text1)−m(text2) and score, a common practice in machine translation metric evaluation (Kocmi et al., 2021).

## Citation

```bibtex
@misc{ananthram2025posh,
  title={PoSh: Using Scene Graphs To Guide LLMs-as-a-Judge For Detailed Image Descriptions},
  author={Amith Ananthram et al. (2025)},
  year={2025},
  note={arXiv:2510.19060}
}
```

- arXiv: 2510.19060
