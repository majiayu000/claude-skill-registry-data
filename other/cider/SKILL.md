---
name: CIDEr
description: Evaluates how well automatic image description metrics correlate with human consensus on sentence similarity. It probes the ability of generated or candidate sentences to accurately describe an image by measuring alignment with multiple human-generated reference descriptions. Use when the user has predictions and gold and needs to compute CIDEr.
metadata:
  skill_kind: metric
  source_arxiv: 1411.5726
  bibtex_key: vedantam2014cider
  confidence: high
---

# CIDEr

> CIDEr: Consensus-based Image Description Evaluation — Vedantam et al. (2014) (arXiv:1411.5726, 2014)

## What this evaluates

Evaluates how well automatic image description metrics correlate with human consensus on sentence similarity. It probes the ability of generated or candidate sentences to accurately describe an image by measuring alignment with multiple human-generated reference descriptions.

## Datasets

- **ABSTRACT-50S** — total ?; splits: test (-1)
- **PASCAL-50S** — total ?; splits: test (-1)

## Metrics

- `CIDEr` **(primary)** — range: [0, 1]
  - A consensus-based metric that measures how closely generated sentences align with human-generated descriptions using a triplet annotation method to capture human agreement. It computes a similarity score weighted by human consensus.
- `BLEU4` — range: [0, 1]
  - Computes an n-gram based precision (up to 4-grams) for the candidate sentence with respect to references, using clipping and a brevity penalty. Aggregated at the sentence level.
- `ROUGE1` — range: [0, 1]
  - Computes an n-gram based recall for the candidate sentence with respect to references. Aggregated at the sentence level.
- `METEOR` — range: [0, 1]
  - Computes an F-measure based on exact matches, stemming, and semantic similarity, optimizing over matches by minimizing chunkiness. Returns the maximum score over references. Uses version 1.5.

## Input / output format

**Input**: Candidate sentence (B) and reference sentence(s) (A) for a given image. For human evaluation, triplets (A, B, C) are used. For automatic evaluation, candidate sentences are compared against up to 48 reference sentences per image.

**Output**: A similarity/consensus score for the candidate relative to the references, or a pairwise comparison result indicating which of two candidates is more similar to the reference.

## Scoring recipe

```python
def compute_cider(candidate, references, human_consensus):
    sim = ngram_similarity(candidate, references)
    consensus_weight = average_human_agreement(candidate, references)
    return sim * consensus_weight

def compute_baseline(candidate, references, metric_name):
    if metric_name == 'BLEU4':
        return bleu4_sentence_level(candidate, references)
    elif metric_name == 'ROUGE1':
        return rouge1_sentence_level(candidate, references)
    elif metric_name == 'METEOR':
        return meteor_v15_sentence_level(candidate, references)
```

## Common pitfalls

- BLEU and ROUGE are traditionally computed at the corpus level for MT/summarization, but this protocol explicitly requires sentence-level aggregation, which yields poor human correlation.
- Using fewer than 48 reference sentences per image significantly degrades metric performance; the protocol mandates up to 50 diverse references.
- Failing to distinguish between human-human, human-machine, and machine-machine candidate pairs when evaluating consensus, as each pair type requires different annotation and scoring treatment.

## Evidence (verbatim from paper)

> The existing metrics used in the community for evaluation of image description approaches are BLEU, ROUGE and METEOR. ... We implement all the metrics, except for METEOR, for which we use version 1.5. Similar to BLEU, we also aggregate METEOR scores at the sentence level.

## Citation

```bibtex
@misc{vedantam2014cider,
  title={CIDEr: Consensus-based Image Description Evaluation},
  author={Vedantam et al. (2014)},
  year={2014},
  note={arXiv:1411.5726}
}
```

- arXiv: 1411.5726
