---
name: swe-rm-verifier
title: "SWE-RM: Execution-Free Feedback for SWE Agents"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.21919
keywords: [reward-model, software-engineering, reinforcement-learning, verification]
description: "Improve SWE agent RL via execution-free reward models optimized for three metrics beyond TTS: discriminative ability (AUC) and calibration (ECE). Shows TTS alone insufficient—models must distinguish correct/incorrect trajectories and align confidence with actual correctness—improving SWE-Bench Verified by 7-10 points with 30B MoE verifier."
---

## Overview

SWE-RM shows that reward model evaluation requires three complementary metrics.

## Core Technique

**Three-Metric Evaluation:**

```python
# Not just TTS (top-1 ranking)
tts_score = rank_best_solution_first(predictions)

# Also discriminative ability
auc_score = compute_auc(correct_vs_incorrect)

# And calibration
ece_score = expected_calibration_error(confidence, accuracy)
```

## When to Use

Use when: SWE agent training, RL reward modeling, importance of calibration.

## References

- Discriminative ability vs ranking metrics
- Calibration error measurement
- Multi-objective reward model design
