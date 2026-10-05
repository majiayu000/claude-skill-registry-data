---
name: tom-eval
description: Probes a model's ability to perform first- and second-order Theory of Mind reasoning by tracking agents' true and false beliefs about object locations. It specifically tests whether models can distinguish objective reality from subjective mental states while resisting heuristic shortcuts. Use when the user wants to benchmark on ToMi, or asks about evaluating this task. Reports aggregate accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.02378
  bibtex_key: liu2025modeling
  confidence: high
---

# tom-eval

> Modeling the Mental World for Embodied AI: A Comprehensive Review — Liu et al. (2025) (arXiv:2601.02378, 2025)

## What this evaluates

Probes a model's ability to perform first- and second-order Theory of Mind reasoning by tracking agents' true and false beliefs about object locations. It specifically tests whether models can distinguish objective reality from subjective mental states while resisting heuristic shortcuts.

## Datasets

- **ToMi** — total ?; splits: test (-1)

## Metrics

- `aggregate accuracy` **(primary)** — range: [0, 1]
  - Calculated as the proportion of stories where the model correctly answers all associated questions (Reality, Memory, first-order belief, second-order belief). A story counts as correct only if every question is answered correctly.

## Input / output format

**Input**: A synthetic narrative story describing agent actions, object locations, and beliefs, followed by multiple questions targeting different belief states.

**Output**: Text responses or selected options for each question associated with the story.

## Scoring recipe

```python
def aggregate_accuracy(predictions, gold):
    correct_stories = 0
    for pred, gold_q in zip(predictions, gold):
        if all(p == g for p, g in zip(pred, gold_q)):
            correct_stories += 1
    return correct_stories / len(predictions)
```

## Common pitfalls

- Models can achieve perfect scores by exploiting rigid templates or heuristics (e.g., checking for the word 'exited' or tracking first/last object positions) without genuine mental state reasoning.
- The dataset uses fully synthetic, low-complexity stories that lack coreference resolution and commonsense associations, limiting real-world generalizability.

## Evidence (verbatim from paper)

> ToMi [102] proposed a systematic improvement scheme with three key components: ... it innovatively proposed an aggregate accuracy evaluation metric: a story was deemed successfully reasoned only if all its associated questions were answered correctly. This metric ensured that models truly distinguish between the objective state of the world and the subjective mental states of agents.

## Citation

```bibtex
@misc{liu2025modeling,
  title={Modeling the Mental World for Embodied AI: A Comprehensive Review},
  author={Liu et al. (2025)},
  year={2025},
  note={arXiv:2601.02378}
}
```

- arXiv: 2601.02378
