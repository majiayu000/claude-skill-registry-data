---
name: mcr-eval
description: Evaluates large language models' ability to perform compositional relation reasoning across multiple languages. It tests whether models can infer a transitive relationship (R∘S) from two given relations (R and S) using multiple-choice questions covering positional, comparative, personal, mathematical, identity, and other logical relations. Use when the user wants to benchmark on Multilingual Compositional Relation (MCR), or asks about evaluating this task. Reports Accuracy (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2403.02615
  bibtex_key: zhao2024exploring
  confidence: high
---

# mcr-eval

> Exploring the Limitations of Large Language Models in Compositional Relation Reasoning — Zhao et al. (2024) (arXiv:2403.02615, 2024)

## What this evaluates

Evaluates large language models' ability to perform compositional relation reasoning across multiple languages. It tests whether models can infer a transitive relationship (R∘S) from two given relations (R and S) using multiple-choice questions covering positional, comparative, personal, mathematical, identity, and other logical relations.

## Datasets

- **Multilingual Compositional Relation (MCR)** — total 1500; splits: test (1500)

## Metrics

- `Accuracy (%)` **(primary)** — range: percent
  - Percentage of correctly answered multiple-choice questions. Calculated as (number of correct predictions / total number of questions) × 100.

## Input / output format

**Input**: A multiple-choice question containing two or more compositional relations (e.g., 'A is related to B via R, B is related to C via S') followed by 3 to 5 labeled options (A, B, C, etc.) asking for the inferred relationship between A and C.

**Output**: The model must select the single most appropriate option from the provided choices (e.g., 'A', 'B', 'C', or the full text of the option).

## Scoring recipe

```python
correct = 0
for pred, gold in zip(predictions, gold_labels):
    if pred.strip().upper() == gold.strip().upper():
        correct += 1
accuracy = (correct / len(gold_labels)) * 100
```

## Common pitfalls

- Questions are strictly self-contained and require no external knowledge; model failures typically indicate reasoning breakdowns rather than factual gaps.
- Some questions belong to multiple categories, so performance should be analyzed per category rather than relying solely on overall accuracy.

## Evidence (verbatim from paper)

> Each MCQ has only one most appropriate answer. If the likelihood of a model failed to choose the most appropriate answer, then the model is considered less effective in compositional relation reasoning. Table 3: Accuracy (%) on Multilingual Compositional Relation benchmark on state-of-the-art LLMs via zero-shot (ZS) and zero-shot chain-of-thought (ZSC) prompting settings.

## Citation

```bibtex
@misc{zhao2024exploring,
  title={Exploring the Limitations of Large Language Models in Compositional Relation Reasoning},
  author={Zhao et al. (2024)},
  year={2024},
  note={arXiv:2403.02615}
}
```

- arXiv: 2403.02615
