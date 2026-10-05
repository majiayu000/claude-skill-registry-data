---
name: visor
description: Evaluates whether text-to-image models correctly render spatial relationships between objects mentioned in a prompt. It disentangles object generation accuracy from spatial correctness to reveal model biases like object priority and merging. Use when the user has predictions and gold and needs to compute VISOR.
metadata:
  skill_kind: metric
  source_arxiv: 2212.10015
  bibtex_key: gokhale2022visor
  confidence: high
---

# visor

> Benchmarking Spatial Relationships in Text-to-Image Generation — Gokhale et al. (2022) (arXiv:2212.10015, 2022)

## What this evaluates

Evaluates whether text-to-image models correctly render spatial relationships between objects mentioned in a prompt. It disentangles object generation accuracy from spatial correctness to reveal model biases like object priority and merging.

## Datasets

- **SR2D** — total ?; splits: (unstated); repo https://github.com/microsoft/VISOR

## Metrics

- `VISOR` **(primary)** — range: [0, 1]
  - Measures spatial relationship accuracy. VISORuncond scores all prompts. VISORcond scores only prompts where both objects are correctly detected. VISORn variants score specific spatial relations.
- `OA` — range: [0, 1]
  - Object Accuracy: percentage of prompts where both mentioned objects are correctly detected in the generated image.
- `Δ_s` — range: other
  - Average difference between metric score for original prompt t and flipped prompt t_flip: E_t[s^t - s^t_flip]. Measures sensitivity to spatial relationships.

## Input / output format

**Input**: Text prompt t specifying two objects and their spatial relationship.

**Output**: Generated image x from the text-to-image model.

## Scoring recipe

```python
def compute_metrics(prompt, image):
    obj_a, obj_b, rel = parse_prompt(prompt)
    detected = detect_objects(image)
    a_present = obj_a in detected
    b_present = obj_b in detected
    rel_detected = detect_spatial_relation(image)
    
    oa = 1.0 if (a_present and b_present) else 0.0
    visor_cond = 1.0 if (a_present and b_present and rel_detected == rel) else 0.0
    visor_uncond = 1.0 if (rel_detected == rel) else 0.0
    return oa, visor_cond, visor_uncond
```

## Common pitfalls

- Existing metrics like CLIPScore and FID ignore text or spatial relations, yielding Δ_s ≈ 0.
- Object Accuracy (OA) penalizes spatial failures if one object is missing, conflating generation and spatial reasoning.
- Human studies show high inter-annotator agreement but reveal models often merge objects (32.46% for DALLE-v2).

## Evidence (verbatim from paper)

> We generate N=4 images for each text prompt from our SR2D dataset, to obtain 126,720 images per model and compare performance in terms of OA, VISOR, VISORcond, and VISOR1/2/3/4.

## Citation

```bibtex
@misc{gokhale2022visor,
  title={Benchmarking Spatial Relationships in Text-to-Image Generation},
  author={Gokhale et al. (2022)},
  year={2022},
  note={arXiv:2212.10015}
}
```

- arXiv: 2212.10015
