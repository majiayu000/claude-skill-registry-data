---
name: polos
description: Evaluates the alignment and quality of generated image captions relative to reference captions and source images. It measures how well a learned metric correlates with human judgments, specifically probing hallucination robustness and open-vocabulary caption evaluation. Use when the user has predictions and gold and needs to compute Polos.
metadata:
  skill_kind: metric
  source_arxiv: 2402.18091
  bibtex_key: wada2024polos
  confidence: medium
---

# polos

> Polos: Multimodal Metric Learning from Human Feedback for Image Captioning — Wada et al. (2024) (arXiv:2402.18091, 2024)

## What this evaluates

Evaluates the alignment and quality of generated image captions relative to reference captions and source images. It measures how well a learned metric correlates with human judgments, specifically probing hallucination robustness and open-vocabulary caption evaluation.

## Datasets

- **Polaris** — total 131000; splits: full (-1)

## Metrics

- `Polos` **(primary)** — range: [0, 1]
  - A scalar score output by the Polos model, trained via the M²LHF framework to align with human feedback. It jointly models text-image and text-text relationships using parallel SimCSE and CLIP embeddings.

## Input / output format

**Input**: Image, reference caption ($x_{\mathrm{ref}}^{(1)}$), and candidate caption ($x_{\mathrm{cand}}$).

**Output**: A single scalar score representing caption quality/alignment.

## Scoring recipe

```python
def compute_polos_score(image, ref_caption, cand_caption):
    # Extract features using parallel encoders
    img_feat = clip_encoder(image)
    ref_feat = simcse_encoder(ref_caption)
    cand_feat = simcse_encoder(cand_caption)
    # Pass through trained M²LHF head to get alignment score
    score = model_head(img_feat, ref_feat, cand_feat)
    return score
```

## Common pitfalls

- CLIPScore family metrics tend to overestimate scores, especially for longer captions.
- Reference-with-image metrics (e.g., RefCLIP-S, RefPAC-S) may fail to effectively compare references and candidates.

## Evidence (verbatim from paper)

> Fig.5 and Fig.6 provide additional comparisons between the CLIPScore family and Polos. We observed that the CLIP-Score family tends to overestimate scores. Specifically, RefCLIP-S and RefPAC-S may not effectively compare references and a candidate. Although CLIP-S could not show overestimation, this does not imply adequacy in caption evaluation.

## Citation

```bibtex
@misc{wada2024polos,
  title={Polos: Multimodal Metric Learning from Human Feedback for Image Captioning},
  author={Wada et al. (2024)},
  year={2024},
  note={arXiv:2402.18091}
}
```

- arXiv: 2402.18091
