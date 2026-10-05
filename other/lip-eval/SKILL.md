---
name: lip-eval
description: Evaluates a model's ability to perform joint human semantic part segmentation and 16-keypoint pose estimation on diverse, unconstrained images with varying appearances, occlusions, and backgrounds. It probes the model's capacity to leverage structural body priors to resolve ambiguities in part boundaries and joint localization. Use when the user wants to benchmark on LIP, PASCAL-Person-Part, MPII Human Pose, ATR, or asks about evaluating this task. Reports mean IoU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1804.01984
  bibtex_key: liang2018lookintoperson
  confidence: high
---

# lip-eval

> Look into Person: Joint Body Parsing & Pose Estimation Network and A New Benchmark — Liang et al. (2018) (arXiv:1804.01984, 2018)

## What this evaluates

Evaluates a model's ability to perform joint human semantic part segmentation and 16-keypoint pose estimation on diverse, unconstrained images with varying appearances, occlusions, and backgrounds. It probes the model's capacity to leverage structural body priors to resolve ambiguities in part boundaries and joint localization.

## Datasets

- **LIP** — total 50462; splits: train (-1), val (-1), test (-1)
- **PASCAL-Person-Part** — total 3533; splits: train (1716), test (1817)
- **MPII Human Pose** — total 25000; splits: train (18079), test (11431)
- **ATR** — total ?; splits: test (-1)

## Metrics

- `mean IoU` **(primary)** — range: [0, 1]
  - Intersection over Union computed per semantic class, then averaged across all classes. Values are reported as percentages in the paper.
- `PCKh` — range: percent
  - Percentage of Correct Keypoints at a normalized distance threshold of 0.5. A keypoint is correct if its Euclidean distance to the ground truth is less than 0.5 times a normalized body size.

## Input / output format

**Input**: RGB image, scaled to 384×384 (JPPNet) or 321×321 (SS-JPPNet). During inference, multi-scale inputs (0.75, 0.5, 1.25) and left-right flipped versions are processed.

**Output**: Per-pixel semantic part labels (19 classes) and 16 body joint coordinates. Final parsing uses averaged probabilities from all stages; final pose uses averaged probabilities from the last stage only.

## Scoring recipe

```python
# Human Parsing: mean IoU
ious = []
for c in range(num_classes):
    pred = (predictions == c)
    gt = (ground_truth == c)
    inter = np.logical_and(pred, gt).sum()
    union = np.logical_or(pred, gt).sum()
    ious.append(inter / union if union > 0 else 0.0)
mean_iou = np.mean(ious)

# Pose Estimation: PCKh
correct = 0
for joint in range(num_joints):
    dist = np.linalg.norm(pred_joints[joint] - gt_joints[joint])
    if dist < 0.5 * normalized_body_size:
        correct += 1
pckh = (correct / num_joints) * 100
```

## Common pitfalls

- Multi-scale inference requires averaging probabilities across scales (0.75, 0.5, 1.25) and flipped images, not just taking the largest scale.
- Pose estimation only uses the final stage's output for scoring, whereas parsing aggregates all stages.
- Cross-dataset evaluation (e.g., on ATR) requires mapping 20 LIP classes to 16 common classes, excluding hat, hair, sunglasses, and scarf.

## Evidence (verbatim from paper)

> We report the results and the comparisons with five state-of-the-art methods on the LIP validation set and test set in Table II and Table III. ... Table XI: Human pose estimation comparison between different variants of the proposed JPPNet on the LIP test set using the PCKh metric.

## Citation

```bibtex
@misc{liang2018lookintoperson,
  title={Look into Person: Joint Body Parsing & Pose Estimation Network and A New Benchmark},
  author={Liang et al. (2018)},
  year={2018},
  note={arXiv:1804.01984}
}
```

- arXiv: 1804.01984
