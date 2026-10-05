---
name: dom-eval
description: Evaluates robotic policies on dynamic object manipulation, measuring their ability to react to moving objects, perceive visual/spatial/motion cues, and generalize across novel objects, scenes, and motion patterns. It specifically probes closed-loop reactivity, dynamic adaptation, long-horizon sequencing, and robustness to disturbances. Use when the user wants to benchmark on DOM, or asks about evaluating this task. Reports Success Rate (SR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.22153
  bibtex_key: xie2026dynamicvla
  confidence: high
---

# dom-eval

> DynamicVLA: A Vision-Language-Action Model for Dynamic Object Manipulation — Haozhe Xie et al. (2026) (arXiv:2601.22153, 2026)

## What this evaluates

Evaluates robotic policies on dynamic object manipulation, measuring their ability to react to moving objects, perceive visual/spatial/motion cues, and generalize across novel objects, scenes, and motion patterns. It specifically probes closed-loop reactivity, dynamic adaptation, long-horizon sequencing, and robustness to disturbances.

## Datasets

- **DOM** — total 202000; splits: test (1800)

## Metrics

- `Success Rate (SR)` **(primary)** — range: percent
  - Percentage of episodes where the robot successfully completes the four-stage manipulation routine (approach, grasp & lift, approach target & place, reset) within the task constraints. Averaged over 20 trials per dimension.
- `Path Length` — range: other
  - Total distance (in meters) traveled by the robot's end-effector during the task. Lower values indicate more efficient trajectories.
- `Task Completion Time` — range: other
  - Total duration (in seconds) from task initiation to successful placement or failure. Lower values indicate faster response and execution.

## Input / output format

**Input**: Multi-view RGB images (480×360 at 25 FPS from front, left, and wrist cameras) and real-time 6D object pose/velocity states (ground-truth in simulation, estimated via RGB-D sensors in real-world).

**Output**: Continuous end-effector action commands for a four-stage manipulation routine: approach object, grasp & lift, approach target & place, and reset.

## Scoring recipe

```python
def compute_metrics(predictions, gold):
    success = 1.0 if predictions['final_state'] == gold['target_state'] else 0.0
    sr = success * 100.0
    path_len = sum(l2_dist(predictions[i], predictions[i-1]) for i in range(1, len(predictions)))
    time = len(predictions) / 25.0  # 25 Hz control frequency
    return sr, path_len, time
# Aggregate SR, Path Length, and Time across 1,800 trials (10 scenes × 9 dimensions × 20 trials)
```

## Common pitfalls

- Teleoperation is explicitly noted as ineffective for fast-moving objects; evaluation relies on automated state-machine controllers or learned policies, not human demonstrations.
- Simulation uses noise-free ground-truth 6D states, while real-world evaluation uses estimated states from RGB-D sensors; mixing these setups invalidates direct comparison.
- Overall SR is an average across 9 distinct sub-dimensions (CR, DA, LS, VU, SR, MP, VG, MG, DR); reporting only the aggregate masks critical capability gaps in specific interaction or perception categories.

## Evidence (verbatim from paper)

> Average success rates (SR, %) are reported across nine evaluation sub-dimensions, organized under three categories: Interaction, Perception, and Generalization. In addition, overall average SR (%), path length (Path Len, meters), and task completion time (Time, seconds) are reported. Each method is evaluated over 1,800 trials (10 scenes × 9 dimensions × 20 trials).

## Citation

```bibtex
@misc{xie2026dynamicvla,
  title={DynamicVLA: A Vision-Language-Action Model for Dynamic Object Manipulation},
  author={Haozhe Xie et al. (2026)},
  year={2026},
  note={arXiv:2601.22153}
}
```

- arXiv: 2601.22153
