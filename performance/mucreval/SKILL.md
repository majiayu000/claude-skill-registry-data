---
name: mucreval
description: Evaluates vision-language models' ability to infer causal relationships across text and image modalities using siamese image-text pairs. It probes cross-modal generalization and visual cue identification in causal reasoning tasks. Use when the user wants to benchmark on MuCR, or asks about evaluating this task. Reports C2E score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2408.08105
  bibtex_key: li2024mucreval
  confidence: high
---

# mucreval

> Multimodal Causal Reasoning Benchmark: Challenging Vision Large Language Models to Discern Causal Links Across Modalities — Li et al. (2024) (arXiv:2408.08105, 2024)

## What this evaluates

Evaluates vision-language models' ability to infer causal relationships across text and image modalities using siamese image-text pairs. It probes cross-modal generalization and visual cue identification in causal reasoning tasks.

## Datasets

- **MuCR** — total ?; splits: test (-1); repo https://github.com/Zhiyuan-Li-John/MuCR

## Metrics

- `C2E score` **(primary)** — range: percent
  - Accuracy percentage of correctly identifying causal links in the Cause-to-Effect (C2E) condition.
- `CP score` — range: percent
  - Accuracy percentage for the CP (Cause-Presence) condition.
- `EXP score` — range: percent
  - Accuracy percentage for the EXP (Effect/Experimental) condition.

## Input / output format

**Input**: Siamese image-text pairs presented as a composite image containing multiple smaller images alongside corresponding text prompts.

**Output**: Selection of the correct causal relationship from a multiple-choice set (implied 4 options based on 25% random baseline).

## Scoring recipe

```python
def calculate_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return (correct / len(gold_labels)) * 100
```

## Common pitfalls

- Models are evaluated on composite images rather than single images, which may affect performance compared to standard single-image benchmarks.
- Human baseline is averaged over ten attempts per volunteer, which may not reflect single-attempt model performance.
- The paper notes a 25% random baseline, implying 4-choice questions, but does not explicitly state the exact prompt format or option structure.

## Evidence (verbatim from paper)

> We evaluated several popular MLLMs on our MuCR benchmark... Finally, we established a human performance baseline on the MuCR benchmark using crowd workers for comparison. ... GPT-o1 achieves the highest scores, with 94% on C2E score, 75% on CP score, and 93% on EXP score in the text condition, while 87% on C2E, 62% on CP, and 78% on EXP in the multimodal condition.

## Citation

```bibtex
@misc{li2024mucreval,
  title={Multimodal Causal Reasoning Benchmark: Challenging Vision Large Language Models to Discern Causal Links Across Modalities},
  author={Li et al. (2024)},
  year={2024},
  note={arXiv:2408.08105}
}
```

- arXiv: 2408.08105
