---
name: hare
description: Evaluates the clinical quality and diagnostic alignment of machine-generated histopathology reports by measuring semantic alignment of extracted pathological entities and their interrelations against ground truth reports. It probes a model's ability to accurately capture domain-specific terminology, diagnostic conclusions, and their contextual connections. Use when the user has predictions and gold and needs to compute HARE Score.
metadata:
  skill_kind: metric
  source_arxiv: 2509.16326
  bibtex_key: kim2025hare
  confidence: high
---

# hare

> HARE: an entity and relation centric evaluation framework for histopathology reports — Kim et al. (2025) (arXiv:2509.16326, 2025)

## What this evaluates

Evaluates the clinical quality and diagnostic alignment of machine-generated histopathology reports by measuring semantic alignment of extracted pathological entities and their interrelations against ground truth reports. It probes a model's ability to accurately capture domain-specific terminology, diagnostic conclusions, and their contextual connections.

## Datasets

- **Hospital & TCGA Histopathology Reports** — total 1465; splits: train (-1), test (-1); repo https://github.com/knowlab/HARE

## Metrics

- `HARE Score` **(primary)** — range: [0, 2]
  - HARE Score = F1_e + F1_r, where F1_e is the harmonic mean of entity precision and recall computed via max cosine similarity of GatorTronS+SapBERT embeddings, and F1_r is the standard F1-score on exact relation pair matches.

## Input / output format

**Input**: Pair of histopathology reports: a candidate (generated) report and a reference (ground truth) report.

**Output**: A single scalar HARE Score (0 to 2) representing the sum of entity and relation F1-scores.

## Scoring recipe

```python
def compute_hare_score(candidate_report, reference_report):
    e_cand, r_cand = extract_entities_and_relations(candidate_report, threshold=0.7)
    e_ref, r_ref = extract_entities_and_relations(reference_report, threshold=0.7)
    emb_cand = embed_entities(e_cand)  # GatorTronS + SapBERT
    emb_ref = embed_entities(e_ref)
    prec_e = sum(max(cosine_sim(c, r) for r in emb_ref) for c in emb_cand) / len(emb_cand)
    rec_e = sum(max(cosine_sim(r, c) for c in emb_cand) for r in emb_ref) / len(emb_ref)
    f1_e = 2 * (prec_e * rec_e) / (prec_e + rec_e)
    f1_r = f1_score(r_cand, r_ref)
    return f1_e + f1_r
```

## Common pitfalls

- Evaluating relation extraction using predicted entities instead of gold-standard entities (the protocol explicitly requires gold entities for RE evaluation).
- Failing to normalize the HARE Score to a 0-1 scale before correlating with expert scores (0-5), as the raw score ranges from 0 to 2.
- Ignoring the 0.7 confidence threshold for entity/relation extraction, which filters out low-confidence predictions and significantly impacts precision/recall calculations.

## Evidence (verbatim from paper)

> The final HARE score is defined as the sum of the entity and relation F1-scores: HARE Score = F1_e + F1_r. This ensures that both precision and recall are considered equally, providing a balanced measure of the alignment between ground truth and predicted entities.

## Citation

```bibtex
@misc{kim2025hare,
  title={HARE: an entity and relation centric evaluation framework for histopathology reports},
  author={Kim et al. (2025)},
  year={2025},
  note={arXiv:2509.16326}
}
```

- arXiv: 2509.16326
