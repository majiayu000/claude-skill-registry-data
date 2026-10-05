---
name: spice
description: Evaluates the semantic propositional content of image captions by transforming them into scene graphs that encode objects, attributes, and relations. It computes an F-score over these logical propositions to measure how well a generated caption captures the underlying meaning of an image compared to human references. Use when the user has predictions and gold and needs to compute SPICE.
metadata:
  skill_kind: metric
  source_arxiv: 1607.08822
  bibtex_key: anderson2016spice
  confidence: high
---

# spice

> SPICE: Semantic Propositional Image Caption Evaluation — Anderson et al. (2016) (arXiv:1607.08822, 2016)

## What this evaluates

Evaluates the semantic propositional content of image captions by transforming them into scene graphs that encode objects, attributes, and relations. It computes an F-score over these logical propositions to measure how well a generated caption captures the underlying meaning of an image compared to human references.

## Datasets

- **Microsoft COCO 2014** — total 123293; splits: train (82783), val (40504), test (40775)
- **Flickr 8K** — total 8092; splits: (unstated)
- **Composite Dataset** — total 11985; splits: (unstated)
- **PASCAL-50S** — total 1000; splits: (unstated)

## Metrics

- `SPICE` **(primary)** — range: [0, 1]
  - F-score computed over scene graph tuples (objects, attributes, relations) extracted from the candidate and reference captions. Precision is the fraction of candidate tuples found in references; recall is the fraction of reference tuples found in the candidate. Synonym matching via WordNet is applied during tuple alignment.
- `SPICE-exact` — range: [0, 1]
  - Same as SPICE but uses exact string matching for tuples instead of synonym matching.

## Input / output format

**Input**: A candidate image caption (generated or human) and one or more reference captions for the same image.

**Output**: A single floating-point F-score value between 0 and 1 representing the semantic match between the candidate and reference scene graphs.

## Scoring recipe

```python
def compute_spice(candidate_caption, reference_captions):
    G_c = parse_scene_graph(candidate_caption)
    G_r = union([parse_scene_graph(ref) for ref in reference_captions])
    intersection = len(G_c & G_r)
    precision = intersection / len(G_c) if len(G_c) > 0 else 0
    recall = intersection / len(G_r) if len(G_r) > 0 else 0
    if precision + recall > 0:
        f_score = 2 * (precision * recall) / (precision + recall)
    else:
        f_score = 0.0
    return f_score
```

## Common pitfalls

- Relies on a semantic parser to convert text to scene graphs; parser errors directly degrade the metric score regardless of actual caption quality.
- Performance is sensitive to the number of reference captions; fewer references lower recall and thus the F-score.
- System-level evaluation uses Pearson's ρ correlation, while caption-level uses Kendall's τ; applying the wrong coefficient misrepresents results.

## Evidence (verbatim from paper)

> SPICE significantly outperforms existing metrics, reaching a correlation coefficient of 0.88 with human quality judgments (M1), compared to 0.43 for CIDEr and 0.53 for METEOR.

## Citation

```bibtex
@misc{anderson2016spice,
  title={SPICE: Semantic Propositional Image Caption Evaluation},
  author={Anderson et al. (2016)},
  year={2016},
  note={arXiv:1607.08822}
}
```

- arXiv: 1607.08822
