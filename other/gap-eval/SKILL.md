---
name: gap-eval
description: Evaluates a model's ability to resolve gendered ambiguous pronouns to their correct antecedent names in natural text. It specifically probes for gender bias and the reliance on syntactic or contextual cues over surface-level heuristics. Use when the user wants to benchmark on GAP, or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1810.05201
  bibtex_key: webster2018mindthegap
  confidence: high
---

# gap-eval

> Mind the GAP: A Balanced Corpus of Gendered Ambiguous Pronouns — Webster et al. (2018) (arXiv:1810.05201, 2018)

## What this evaluates

Evaluates a model's ability to resolve gendered ambiguous pronouns to their correct antecedent names in natural text. It specifically probes for gender bias and the reliance on syntactic or contextual cues over surface-level heuristics.

## Datasets

- **GAP** — total 8908; splits: dev (4000), test (4000), val (908)

## Metrics

- `F1 score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall for pronoun-antecedent matching. Precision is TP/(TP+FP) and recall is TP/(TP+FN), where TP/FP/FN are counts of correct/incorrect/missed name predictions based on mention alignment. Computed Overall and separately for Masculine and Feminine pronouns.
- `Bias` — range: [0, 1]
  - Ratio of Feminine F1 score to Masculine F1 score. Values are typically less than one, indicating a systematic bias toward resolving masculine pronouns more accurately.

## Input / output format

**Input**: A text snippet or full page context containing a target pronoun and candidate name spans. Optionally includes the source Wikipedia URL depending on the evaluation setting (snippet-context vs page-context).

**Output**: A single predicted name/antecedent span corresponding to the target pronoun.

## Scoring recipe

```python
def compute_f1(preds, golds):
    tp = sum(1 for p, g in zip(preds, golds) if mention_match(p, g))
    fp = sum(1 for p, g in zip(preds, golds) if not mention_match(p, g))
    fn = sum(1 for p, g in zip(preds, golds) if g not in [p for p, _ in zip(preds, golds) if mention_match(p, g)])
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    return 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0

def compute_bias(f1_fem, f1_masc):
    return f1_fem / f1_masc if f1_masc > 0 else 0
```

## Common pitfalls

- Models trained on OntoNotes are overly conservative, yielding low recall because they assume pronouns are rarely anaphoric in out-of-domain text.
- Mention alignment does not require exact string matches; substring overlaps between predicted and gold names count as correct.
- Systems should not rely on gold mention spans as a Winograd-style shortcut; they must detect candidates automatically.

## Evidence (verbatim from paper)

> GAP is an evaluation corpus and we segment the final dataset into a development and test set of 4,000 examples each; we reserve the remaining 908 examples as a small validation set for parameter tuning. ... To reward unbiased modeling, we define two evaluation metrics: F1 score and Bias. Concretely, we calculate F1 score Overall as well as by the gender of the pronoun (Masculine and Feminine). Bias is calculated by taking the ratio of feminine to masculine F1 scores, typically less than one.

## Citation

```bibtex
@misc{webster2018mindthegap,
  title={Mind the GAP: A Balanced Corpus of Gendered Ambiguous Pronouns},
  author={Webster et al. (2018)},
  year={2018},
  note={arXiv:1810.05201}
}
```

- arXiv: 1810.05201
