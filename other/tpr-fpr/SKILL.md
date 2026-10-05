---
name: tpr@fpr
description: Evaluates the discriminative capability of a speaker verification model by measuring the true positive rate at fixed false positive rate thresholds. It probes how well the model's embedding space separates same-speaker pairs from different-speaker pairs under controlled error constraints. Use when the user has predictions and gold and needs to compute TPR@FPR.
metadata:
  skill_kind: metric
  source_arxiv: 2406.19243
  bibtex_key: borodin2024asv
  confidence: high
---

# tpr@fpr

> Application of ASV for Voice Identification after VC and Duration Predictor Improvement in TTS Models — Borodin Kirill Nikolayevich et al. (2024) (arXiv:2406.19243, 2024)

## What this evaluates

Evaluates the discriminative capability of a speaker verification model by measuring the true positive rate at fixed false positive rate thresholds. It probes how well the model's embedding space separates same-speaker pairs from different-speaker pairs under controlled error constraints.

## Datasets

- **Custom 5-speaker dataset** — total 7500; splits: test (7500)
- **CMU ARCTIC** — total ?; splits: test (-1)

## Metrics

- `TPR@FPR` **(primary)** — range: [0, 1]
  - Given a fixed FPR threshold N, compute cosine similarity for all positive and negative pairs. Determine the similarity value at the N-th false positive pair when negative similarities are sorted descending. TPR@FPR=N is the ratio of positive pairs exceeding this threshold to the total positive pairs.
- `WDER` — range: other
  - Weighted Duration Error Rate for phoneme duration prediction. Applies a penalty of 1 if error ≤ 1 frame, otherwise applies |x - x_hat|^(-1). Averaged over N phonemes.
- `MAE` — range: other
  - Mean Absolute Error between predicted and ground-truth phoneme durations.
- `RMSE` — range: other
  - Root Mean Squared Error between predicted and ground-truth phoneme durations.
- `CCC` — range: other
  - Concordance Correlation Coefficient measuring agreement between predicted and actual durations.

## Input / output format

**Input**: Pairs of audio utterances (positive pairs share the same speaker, negative pairs have different speakers) processed through the ASV model to produce speaker embeddings.

**Output**: Cosine similarity scores between embeddings, aggregated to compute TPR@FPR at specified thresholds (0.5, 0.2, 0.1, 0.05, 0.01).

## Scoring recipe

```python
def compute_tpr_at_fpr(pos_sims, neg_sims, n):
    k = n * len(neg_sims)
    sorted_neg = sorted(neg_sims, reverse=True)
    threshold = sorted_neg[k]
    tpr = sum(1 for s in pos_sims if s >= threshold) / len(pos_sims)
    return tpr

def compute_wder(x, x_hat):
    err = abs(x - x_hat)
    return 1.0 if err <= 1 else err ** -1

wder = sum(compute_wder(x, x_hat) for x, x_hat in zip(targets, preds)) / len(targets)
```

## Common pitfalls

- Tables contain a typo 'FRP' instead of 'FPR' in metric column headers.
- The custom test dataset only contains 5 speakers, which the authors explicitly note is insufficient for robust ASV evaluation.
- Step 6 of the metric definition mentions 'cosine distance' while the rest of the algorithm uses 'cosine similarity', which may cause implementation confusion.

## Evidence (verbatim from paper)

> We chose TPR @ FPR. The idea behind this metric is that, given a fixed rate of false positive pairs, we count how many true positive pairs we have before this last allowed false positive pair, and then divide the resulting number by the total number of true positive pairs. The algorithm used to calculate this metric: 1. Fixing the threshold value TPR @ FPR = N. 2. Calculate the cosine similarity between all positive pairs. 3. Calculate the cosine similarity between all negative pairs. 4. Calculate how many elements make up N times the number of false positive pairs. This number is k. 5. Sort all cosine similarity values of false pairs in descending order. The K-th number is the threshold distance. 6. Count the number of positive pairs whose cosine distance is less than the threshold distance. 7. Divide the number obtained by the total number of positive pairs.

## Citation

```bibtex
@misc{borodin2024asv,
  title={Application of ASV for Voice Identification after VC and Duration Predictor Improvement in TTS Models},
  author={Borodin Kirill Nikolayevich et al. (2024)},
  year={2024},
  note={arXiv:2406.19243}
}
```

- arXiv: 2406.19243
