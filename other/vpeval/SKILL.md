---
name: vpeval
description: Evaluates text-to-image generation models by decomposing assessment into five specialized skills (object presence, count, spatial relations, scale, and text rendering) and open-ended prompts, producing interpretable binary scores with visual and textual explanations. Use when the user has predictions and gold and needs to compute vpeval.
metadata:
  skill_kind: metric
  source_arxiv: 2305.15328
  bibtex_key: cho2023visualprogramming
  confidence: high
---

# vpeval

> Visual Programming for Text-to-Image Generation and Evaluation — Cho et al. (2023) (arXiv:2305.15328, 2023)

## What this evaluates

Evaluates text-to-image generation models by decomposing assessment into five specialized skills (object presence, count, spatial relations, scale, and text rendering) and open-ended prompts, producing interpretable binary scores with visual and textual explanations.

## Datasets

- **TIFA160** — total 160; splits: test (160)

## Metrics

- `vpeval` **(primary)** — range: [0, 1]
  - Average of binary pass/fail scores from specialized visual modules (objectEval, countEval, spatialEval, scaleEval, textEval). Each module returns 1 if the generated image satisfies the prompt constraint, 0 otherwise.

## Input / output format

**Input**: Text prompt and the corresponding generated image.

**Output**: Binary score per module, visual bounding boxes on the image, textual explanation of the result, and a final averaged score.

## Scoring recipe

```python
def vpeval(prompt, image):
    modules = get_program(prompt)  # predefined for skill-based, LLM-generated for open-ended
    scores = []
    for mod in modules:
        scores.append(mod.run(image, prompt))  # returns 0 or 1
    return sum(scores) / len(scores)
```

## Common pitfalls

- Binary scoring discards partial credit (e.g., detecting 2 objects instead of 3 yields 0).
- Relies entirely on the accuracy of underlying expert modules (Grounding DINO, EasyOCR, BLIP-2); module failures directly lower the score.
- Open-ended evaluation uses LLM-generated programs via in-context learning, which may introduce non-determinism or program generation errors.

## Evidence (verbatim from paper)

> VPEval is a novel interpretable/explainable evaluation framework for T2I generation models, based on visual programming.

## Citation

```bibtex
@misc{cho2023visualprogramming,
  title={Visual Programming for Text-to-Image Generation and Evaluation},
  author={Cho et al. (2023)},
  year={2023},
  note={arXiv:2305.15328}
}
```

- arXiv: 2305.15328
